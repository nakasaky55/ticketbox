from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests
from src import login_manager,db,app
user_blueprint = Blueprint('userbp', __name__, template_folder='../../templates')

from src.models import User
from itsdangerous import URLSafeTimedSerializer
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

##send email function
def send_simple_message(token, email, name):
	return requests.post(
		"https://api.mailgun.net/v3/mg.anhkhoa.dev/messages",
		auth=("api", app.config["API_MAIL_KEY"]),
		data={"from": "Mailgun Sandbox <postmaster@mg.anhkhoa.dev>",
			"to": f"<{email}>",
			"subject": f"Hello {name}",
		  "html": render_template("mails/recover.html", token = token)})

## 'host/user/'
@user_blueprint.route('/')
def root():
  return render_template('base/index.html')

@user_blueprint.route('/signup', methods=["GET", "POST"])
def signup():
  if current_user.is_authenticated:
    print("not need to login")
  if request.method == "POST":
    check_user = User.query.filter_by(email = request.form['email']).first()
    if not check_user:
      new_user = User(
          username = request.form['username'],
          email = request.form['email'],
          address = request.form['address']
      )
      new_user.set_password(request.form['password'])
      db.session.add(new_user)
      db.session.commit()
      return redirect(url_for("root"))
  return render_template('user/signup.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@user_blueprint.route('/login', methods=["GET", "POST"])
def login():
  if request.method == "GET":
    if current_user.is_authenticated:
        return redirect(url_for("app.root"))
  if request.method == "POST":
      user = User.query.filter_by(email = request.form['email']).first()
      if not user:
        flash("Email or password incorrect", "danger")
      elif user.check_password(request.form['password']):
        login_user(user)
        return redirect(url_for('root'))
  return render_template("user/login.html")

@user_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("root"))

@user_blueprint.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
  if request.method == "POST":
    check_user = User.query.filter_by(email = request.form['email']).first()
    if not check_user:
      flash("Email invalid", "warning")
    else:
      token = ts.dumps(request.form['email'], salt='recover-password-secret')
      custom_token = f"http://localhost:5000/user/new_password/{token}"
      response = send_simple_message(custom_token, request.form["email"], check_user.username)
      print("res", custom_token)
      flash("Please check your mailbox", "danger")
  return render_template("user/forgot.html")

@user_blueprint.route("/new_password/<token>", methods=["POST", "GET"])
def new_password(token):
  if current_user.is_authenticated:
    return "Please logout current user first"
  else:
    email_token = ts.loads(token, salt="recover-password-secret")
    user = User.query.filter_by(email = email_token).first()
    if request.method == "POST":
      if request.form['password'] == request.form['confirm']:
        user.set_password(request.form['password'])
        db.session.commit()
        flash("Set password successfully", "primary")
        return redirect(url_for("userbp.login"))
      else:
        flash("Password does not match", "warning")
        return redirect(url_for("userbp.new_password", token = token))
  return render_template("user/newpassword.html")
  
