from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, AboutForm
from flask_mongoengine import MongoEngine
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required
from models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = '4912660028b3df14ada55c3ead8e962c'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.config['MONGODB_SETTINGS'] = {
    'db': 'neuro_image_database',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.objects(id = id).first()

@app.route("/")
@app.route("/home")
@login_required
def home():
	return render_template('home.html')

@app.route("/about")
# ToDo: remove below testing purpose line
@login_required
def about():
    form = AboutForm()
    return render_template('about.html', title='About', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.objects(email = form.email.data).first()
        if user:
            flash('The entered email already exists. Please try again!', 'success')
            return redirect(url_for('home'))

        user = User(username = form.username.data, email = form.email.data, password = generate_password_hash(form.password.data))
        user.save()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	# if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email = form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            print('enter login(), ' + user.username + ' remember me = ' + str(form.remember.data), flush=True)
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug=True)