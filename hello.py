from flask import Flask
from flask import Flask, render_template, flash, session, url_for, redirect
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from wtforms.validators import Required,Email
from wtforms.fields.html5 import EmailField

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    email = EmailField("What is your UofT Email address?", validators=[Required(), Email()])
    submit = SubmitField('Submit')

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'password'

@app.route('/', methods=['GET', 'POST'])
def index():
    submission = NameForm()
    if submission.validate_on_submit():
        old = session.get('name')
        email_old = session.get('email')
        if old != submission.name.data:
            flash("Looks like you've changed your name!")
        if email_old != submission.email.data:
            flash("Looks like you've changed your email!")
        session['name'] = submission.name.data
        session['email'] = submission.email.data
        session['is_uofT'] = ValidEmail(submission.email.data)
        return redirect(url_for('index'))
    return render_template("index.html", form=submission, name=session.get('name'),email=session.get('email'),is_uofT = session.get('is_uofT'))

def ValidEmail(email):
    b = email.split('@')
    return b[0].find('utoronto') != -1

@app.route('/user/<name>')
def user(name):
 return render_template("user.html", name=name,  current_time=datetime.utcnow())

if __name__ == '__main__':
    app.run(debug=True)
