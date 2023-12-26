from flask import Flask, render_template, url_for, redirect, request, abort, flash
from flask_bootstrap import Bootstrap5
from form import ContactForm, RegisterForm, LoginForm, PostProjectForm, AdminProfileForm
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
# from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user
from smtplib import SMTP
from functools import wraps
from dotenv import load_dotenv
import os


'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''


load_dotenv()


my_mail = os.environ.get("MY_EMAIL")
password = os.environ.get("PASSWORD")

# initialize Flask-App
app = Flask(__name__)

# csrf protection
# csrf = CSRFProtect(app)


# flaskform secret-key
app.config['SECRET_KEY'] = os.environ.get("FLASK_FORM_KEY")

# SQLAlchemy database uri
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///project.db")

# configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# initialize bootstrap with app
bootstrap = Bootstrap5(app)

# ckeditor
ckeditor = CKEditor(app)

# creating database extension
db = SQLAlchemy()

# initialize database extension with app
db.init_app(app)


# table creation
class ProjectPost(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(75), unique=True, nullable=False)
    technology_used_summary = db.Column(db.String, nullable=False)
    git_hub_url = db.Column(db.String(250), nullable=False)
    website_url = db.Column(db.String(250), nullable=True)
    project_img_url = db.Column(db.String(250), nullable=False)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email_id = db.Column(db.String(75), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Profile(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    profile_img_url = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(30), nullable=True)
    admin_intro = db.Column(db.String, nullable=False)


# Create Table Schema in the Database
with app.app_context():
    db.create_all()


# with app.app_context():
#     project_post = ProjectPost(
#         id=1,
#         project_name="Tinder Bot",
#         technology_used_summary="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor"
#                                 " incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud "
#                                 "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure "
#                                 "dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
#                                 "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt "
#                                 "mollit anim id est laborum.",
#         project_img_url="https://media.giphy.com/media/vVzH2XY3Y0Ar6/giphy.gif?cid=82a1493bx4ldiliiwvy8oepncs4ztv9i8rf4kkm5hsprukak&ep=v1_gifs_trending&rid=giphy.gif&ct=g",
#     )
#     db.session.add(project_post)
#     db.session.commit()


# admin login decorator-function
def admin_login(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated:
                return func(*args, **kwargs)
            else:
                return abort(403)
        return decorated_function


@app.route("/")
def home():
    admin_profile = Profile.query.first()
    if not admin_profile:
        return render_template("index.html")
    else:
        return render_template("index.html", admin_profile=admin_profile)


@app.route("/project")
def project():
    result = ProjectPost.query.all()
    return render_template("Project.html", posts=result)


# create register
@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    existing_user = User.query.first()
    if register_form.validate_on_submit():
        if existing_user:
            flash("Sorry, only one user allowed. User already exists")
            return redirect(url_for("register"))
        else:
            user = User(
                name=register_form.name.data,
                email_id=register_form.email.data,
                password=generate_password_hash(
                    password=register_form.password.data,
                    method='pbkdf2:sha256',
                    salt_length=8,
                )
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))

    return render_template("register.html", form=register_form)


# login-form
@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        user = db.session.query(User).filter_by(email_id=email).first()
        if not check_password_hash(user.password, password=login_form.password.data):
            flash("Password is incorrect")
            return redirect(url_for("login"))
        else:
            check_password_hash(user.password, password=login_form.password.data)
            login_user(user=user)
            return redirect(url_for("home"))
    return render_template("login.html", form=login_form)


# Post-Project
@app.route("/post-project", methods=["GET", "POST"])
@admin_login
def post_project():
    post_project_form = PostProjectForm()
    if post_project_form.validate_on_submit():
        project_post = ProjectPost(
            project_name=post_project_form.project_title.data,
            technology_used_summary=post_project_form.project_summary.data,
            git_hub_url=post_project_form.project_github_url.data,
            website_url=post_project_form.project_website_url.data,
            project_img_url=post_project_form.project_image_url.data,
        )
        db.session.add(project_post)
        db.session.commit()
        return redirect(url_for("project"))

    return render_template("post-project.html", form=post_project_form)


@app.route("/edit-project/<post_id>", methods=["GET", "POST"])
@admin_login
def edit_project(post_id):
    # id = request.args.get("post_id")
    project_to_edit = db.get_or_404(ProjectPost, post_id)
    form = PostProjectForm(
        project_title=project_to_edit.project_name,
        project_github_url=project_to_edit.git_hub_url,
        project_website_url=project_to_edit.website_url,
        project_image_url=project_to_edit.project_img_url,
        project_summary=project_to_edit.technology_used_summary,
    )
    if form.validate_on_submit():
        project_to_edit.project_name = form.project_title.data
        project_to_edit.git_hub_url = form.project_github_url.data
        project_to_edit.website_url = form.project_website_url.data
        project_to_edit.project_img_url = form.project_image_url.data
        project_to_edit.technology_used_summary = form.project_summary.data
        db.session.commit()
        return redirect(url_for("project_element", project_id=post_id))
    return render_template("post-project.html", form=form, is_edit=True)


@app.route("/delete/<post_id>")
@admin_login
def delete(post_id):
    post_to_delete = db.get_or_404(ProjectPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return render_template("project.html")


@app.route("/project-element/<int:project_id>")
def project_element(project_id):
    requested_project = db.session.query(ProjectPost).filter_by(id=project_id).first()
    web_link_button = requested_project.website_url
    return render_template("project-detail.html", project=requested_project,
                           web_button=web_link_button,
                           )


@app.route("/logout")
@admin_login
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if request.method == "POST":
        data = request.form
        message = (f"Subject:New-Message\n\nName: {data['name']}\nEmail:{data['email']}\nPhone: {data['phone']}\n"
                   f"Message: {data['message']}")
        send_message(message=message)
        return render_template("contact.html", msg_sent=True)

    return render_template("contact.html", form=form, msg_sent=False)


def send_message(message):
    with SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_mail, password=password)
        connection.sendmail(my_mail, my_mail, message)


@app.route("/edit-profile", methods=["GET", "POST"])
@admin_login
def edit_profile():
    form = AdminProfileForm()
    existing_user = Profile.query.first()
    if not existing_user:
        if form.validate_on_submit():
            profile = Profile(
                profile_img_url=form.profile_img_url.data,
                title=form.welcome_title.data,
                admin_intro=form.intro_of_admin.data,
            )
            db.session.add(profile)
            db.session.commit()
            return redirect(url_for("home"))
    else:
        existing_user = Profile.query.first()
        if form.validate_on_submit():
            existing_user.profile_img_url = form.profile_img_url.data
            existing_user.title = form.welcome_title.data
            existing_user.admin_intro = form.intro_of_admin.data
            db.session.commit()
            return redirect(url_for("home"))
    return render_template("edit-profile.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
