from flask import Flask, redirect, url_for, render_template, Blueprint ,request, flash
from Server.users.forms import LoginForm, UserProfile, RequestResetForm, ResetPasswordForm
from Server import db, bcrypt, Net_CDN
from flask_security import login_user, current_user, logout_user, login_required
from Server.models import User
from Server.users.utilty import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route('/user/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    form = UserProfile()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            print(picture_file)
        current_user.username = form.username.data
        current_user.first_name = form.firstname.data
        current_user.last_name = form.lastname.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.user_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.firstname.data = current_user.first_name
        form.lastname.data = current_user.last_name
        form.state.data = current_user.state
        form.locality.data = current_user.locality

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('Users/user_profile.html', page_title="User Profile", form =form,  image_file=image_file)


@users.route("/reset", methods=['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for(users.login))
    return render_template('Users/reset_request.html', page_title="Request Password Reset", forma=True, form=form)


@users.route("/reset/<token>", methods=['POST', 'GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password =hashed_password
        db.session.commit()
        flash(f'Your password updated !', 'success')
        return redirect(url_for(users.login))
    return render_template('Users/reset_token.html', page_title="Reset Password", forma=True, form=form)