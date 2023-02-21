from flask import Flask, request, redirect, url_for, flash, session, render_template
from flask_mail import Message, Mail
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import  login_user, LoginManager, login_required, logout_user, current_user, UserMixin
from flask_bcrypt import Bcrypt
import secrets
import string
from datetime import datetime, timedelta
from config import MAIL_PASSWORD, MAIL_PORT, MAIL_SERVER, MAIL_USE_SSL, MAIL_USE_TLS, MAIL_USERNAME, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATION
import emails
import random
app = Flask(__name__)
any = Bcrypt(app)

app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = MAIL_USE_SSL
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD

# app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://sql7597749:uQhpEUxsvZ@sql7.freesqldatabase.com/sql7597749'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = SQLALCHEMY_TRACK_MODIFICATION

app.config["SECRET_KEY"] = os.urandom(24)
mail = Mail(app)
db = SQLAlchemy(app)
loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "login"



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(10000), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    verification_token = db.Column(db.String(100))
    forget_password_token = db.Column(db.String(100))
    forget_password_expiry = db.Column(db.DateTime)
    expiry_date = db.Column(db.DateTime)
    occupation = db.Column(db.String(100))
    companyName = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    adress = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postalCode = db.Column(db.String(100))
    facebook = db.Column(db.String(100))
    twitter = db.Column(db.String(100))
    instagram = db.Column(db.String(100))
    linkedin = db.Column(db.String(100))

    def __init__(self, fullName, email, password, is_active = False):
        self.fullName = fullName
        self.email = email
        self.password = password
        self.is_active = is_active

@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
 

@app.errorhandler(Exception)
def handle_exception(e):
    return render_template("error-404.html")




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/updateprofile', methods=["POST"] )
@login_required
def updateProfile():
    current_user.occupation = request.form.get("occupation")
    current_user.companyName = request.form.get("companyName")
    current_user.phone = request.form.get("phone")
    current_user.adress = request.form.get("adress")
    current_user.city = request.form.get("city")
    current_user.state = request.form.get("state")
    current_user.postalCode = request.form.get("postalCode")
    current_user.facebook = request.form.get("facebook")
    current_user.twitter = request.form.get("twitter")
    current_user.instagram = request.form.get("instagram")
    current_user.linkedin = request.form.get("linkedin")

    db.session.commit()

    flash('Update successful.', 'success')

    return redirect("/dashboard#user-profile") 

@app.route('/updatePassword', methods=["POST"])
@login_required
def updatePassword():
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    repeated_new_password = request.form.get("new_password2")
    valid_password = current_user.password;

    if new_password == repeated_new_password:
        print("matched")
        if old_password == valid_password:
            print("valid pwd")
            current_user.password = new_password
            db.session.commit()
            flash("password updated successfully", "success")
        else:
            flash("Invalid password. Please try again.", 'danger')
    else:
        flash("passwords do not match. Try Again.", "warning")
    return redirect('/dashboard#user-profile') 

@app.route('/users/forgetpassword', methods=["GET", "POST"])
def forgetPassword():
    if 'login' in session:
        return redirect(url_for("/"))
    if request.method == "POST":
        email = request.form.get("email").lower()
        userFound = User.query.filter_by(email=email).first()
        if userFound:
            alphabet = string.ascii_letters + string.digits
            token = ''.join(secrets.choice(alphabet) for i in range(20))
            userFound.forget_password_token = token
            userFound.forget_password_expiry = datetime.now() + timedelta(hours=1)
            db.session.commit()
            msg = Message(subject=emails.email_forget_password_subject, body=emails.email_forget_password_body.format(userFound.fullName, token),
                          sender=emails.email_sender, recipients=[email])
            mail.send(msg)
            flash("Please check your email", 'success')
            return render_template("reset-password.html")
        flash("Your search did not return any results. Please try again with other information.", 'danger')

    return render_template('forget-password.html')

@app.route('/resetpassword', methods= ["POST"])
def reset_password():
    print("executed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    user_found = User.query.filter_by(forget_password_token=request.form.get('code')).first()
    if user_found :
        user_found.forget_password_token = None
        user_found.forget_password_expiry = None
        user_found.password = request.form.get('password')
        db.session.commit()
        flash("Your password has been successfully updated.", 'success')
        return render_template('login.html')
    flash("the verification code you entered is invalid. Please double-check the code and try again.", 'danger')
    return render_template('reset-password.html')


@app.route('/users/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("pwd")
        user_found = User.query.filter_by(email=email).first()
        if user_found:
            if password == user_found.password:
                login_user(user_found)
                return redirect(url_for("dashboard"))
        flash("Incorrect username or password", "danger")
    return render_template('login.html')


@app.route('/log_out')
@login_required
def log_out():
    logout_user()
    return redirect(url_for("login"))

@app.route("/users/verifyaccount", methods = ['GET'])
def verify():
    token = request.args.get('token')
    if verifyToken(token):
        return render_template('activated.html')
    return render_template('error-404.html')
    






@app.route('/users/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        fullName = request.form.get("dzName")
        email = request.form.get("email")
        password = request.form.get("pwd")
        user_found = User.query.filter_by(email=email).first()

        if not user_found:
            new_user = User(fullName=fullName, email=email,
                            password=password)
            code = generate_verification_code(new_user)
            db.session.add(new_user)
            db.session.commit()
            link = request.url_root + 'users/verifyaccount?token=' + code
            body = emails.email_validate_password_body.format(fullName, link)
            msg = Message(subject=emails.email_validate_password_subject, body=body,
            sender=emails.email_sender, recipients=[email])
            mail.send(msg)
            flash("Please check your email to activate your account", 'success')
            return redirect(url_for('login'))
        flash("This email is already in use. Please try with a different email.", 'danger')
    return render_template('register.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('/admin/index.html')


@app.route('/contact', methods=['GET'])
def contact():
    return redirect("/#contact-us")


@app.route('/contact', methods=['POST'])
def contact_us():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    subject = request.form.get("subject")
    message = request.form.get("message")
    validated = True

    if not validated:
        return render_template('error-404.html')
    body = emails.email_contact_me_body.format(name, subject, phone, email, message, name)
    msg = Message(subject=emails.email_contact_me_subject.format(name), body=body, sender=MAIL_USERNAME,
                  recipients=['noureddinelachgar9@gmail.com'])
    mail.send(msg)
    flash('mail send successfully', 'success')

    return redirect('/#contact-us')


def verifyToken(token: str) :
    if len(token) != 64:
        return False
    user_by_token:User = User.query.filter_by(verification_token=token).first()
    if user_by_token:
        user_by_token.is_active = True
        user_by_token.verification_token = None
        user_by_token.expiry_date = None
        db.session.commit()
        return True
    return False

def generate_verification_code(user: User):
    randomCode = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=64))
    expiryDate = datetime.now() + timedelta(hours = 5)
    user.verification_token = randomCode
    user.expiry_date = expiryDate
    user.is_active = False
    return randomCode