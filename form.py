from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, IntegerField, PasswordField, URLField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField


class ContactForm(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired()])
    email = EmailField(label="Email Address", validators=[DataRequired()])
    phone = IntegerField(label="Phone Number", validators=[DataRequired()])
    message = StringField(label="Message", validators=[DataRequired()])
    submit = SubmitField(label="Send")


class RegisterForm(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired()])
    email = EmailField(label="Email Address", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Sign Up")


class LoginForm(FlaskForm):
    email = EmailField(label="Email Address", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Login")


# Post-Project
class PostProjectForm(FlaskForm):
    project_title = StringField(label="Project Title", validators=[DataRequired()])
    project_github_url = URLField(label="Project Git-hub Link", validators=[DataRequired()])
    project_website_url = URLField(label="Project Website Link (optional)")
    project_image_url = URLField(label="Project Image Url", validators=[DataRequired()])
    project_summary = CKEditorField(label="Project Summary", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


class AdminProfileForm(FlaskForm):
    profile_img_url = URLField(label="Image url", validators=[DataRequired()])
    welcome_title = StringField(label="Welcome Title (optional)")
    intro_of_admin = CKEditorField(label="Describe Profile", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


