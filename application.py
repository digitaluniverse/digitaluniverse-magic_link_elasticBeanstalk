
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, Length
from twilio_verify.verify import verifications, verification_checks,get_channel_configuration
from decouple import config


application = Flask(__name__)
application.config['SECRET_KEY']=config('FLASK_SECRET_KEY')


class CreateUserForm(FlaskForm):
    email = StringField(label=('Email'), validators=[DataRequired(), Email(), Length(max=120)])

    submit = SubmitField(label=('Submit'))



@application.route('/', methods=('GET', 'POST'))
def index():
    path = request.path
    # protocol = 'http' if config('DOMAIN_NAME').startswith('localhost') else 'https'
    protocol = 'http'
    callback_url = f"{protocol}://{config('DOMAIN_NAME')}{path[0:path.rindex('/')]}/{config('CALLBACK_PATH')}"
    print(callback_url)
    form = CreateUserForm()
    if form.validate_on_submit():
        email = form.email.data
        success_message= "Email sent to {}. Check your email to complete verification.".format(email)
        try:
            channel_configuration= get_channel_configuration(email, callback_url)
            verifications(email,channel_configuration)
            return render_template('index.html', form=form, success_message=success_message)
        except Exception as error:
            return render_template('index.html', form=form, error_message=str(error))
    return render_template('index.html', form=form)

@application.route('/verify')
def verify():
    valid = False
    missing_params = []
    token = request.args.get('token')
    result = ''
    to = request.args.get('to')
    if token is None:
        missing_params.append('token')
        if to is None:
            missing_params.append('to')
        return render_template('verify.html', result=f"Missing Paramaters {missing_params}", valid=valid)
    try:
        valid = True if verification_checks(to,token).status =='approved' else False
        if valid:
            result = 'Verification Success.'
        else:
            result = "Incorrect Token"
        return render_template('verify.html', result=result, valid=valid)
    except Exception as error:
        return render_template('verify.html', valid=valid, result=error.msg)


if __name__ == "__main__":
    application.debug = True
    application.run(host='0.0.0.0')