from flask import Flask, redirect, url_for, render_template, Blueprint, flash, jsonify, request
from flask_security import login_user, current_user, logout_user, login_required, roles_required, roles_accepted
from Server import db, bcrypt, user_datastore, Net_CDN
from Server.models import User, Role, State, Locality, AddNews
from Server.manager.form import (AddUser, AddRole, Add_News, Update_News, StateForm,
                                 ImportDataForm,
                                 LocalityForm, StateDeleteForm, LocalityDeleteForm)
from Server.users.utilty import save_image
from Server.manager.utilty import ImportData
from werkzeug.utils import secure_filename

manager = Blueprint('manager', __name__)

@manager.route("/manager/users", methods=['GET', 'POST'])
@roles_accepted('superuser', 'state_manager', 'locality_manager')
def users():
    form = AddUser()
    if current_user.has_role('superuser'):
        users = User.query.all()
    elif current_user.has_role('state_manager'):
        users = User.query.filter_by(state=current_user.state)
    else:
        users = User.query.filter_by(locality=current_user.locality)

    if current_user.has_role('superuser'):
        form.state.choices = [(state.state_name, state.state_name) for state in State.query.all()]
        form.locality.choices = [(locality.locality_name, locality.locality_name) for locality in Locality.query.all()]
        form.roles.choices = [('state_manager', 'state_manager'), ('locality_manager', 'locality_manager'), ('user', 'user')]
    elif current_user.has_role('state_manager'):
        start = State.query.filter_by(state_name=current_user.state).first()
        form.state.choices = [(current_user.state, current_user.state)]
        form.locality.choices = [(locality.locality_name, locality.locality_name) for locality in Locality.query.filter_by(state_in=start)]
        form.roles.choices = [('user', 'user'), ('locality_manager', 'locality_manager') ]
    else:
        users = User.query.filter_by(locality=current_user.locality)
        form.state.choices = [(current_user.state, current_user.state)]
        form.locality.choices = [(current_user.locality, current_user.locality)]
        form.roles.choices = [('user', 'user')]

    if form.validate_on_submit():
        user_datastore.create_user(username=form.username.data,
                       first_name=form.first_name.data,
                       last_name=form.last_name.data,
                       locality=form.locality.data,
                       state=form.state.data,
                       email=form.email.data,
                       password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
                       roles=[form.roles.data]
                       )
        db.session.commit()
        flash(f'User added successful !', 'success')
    return render_template('Manager/manager_users.html', page_title="Manage Users", users=users, form=form,forma=True, tablea=True)

# @manager.route("/manager/roles", methods=['GET', 'POST'])
# @roles_required('superuser')
# def roles():
#     roles = Role.query.all()
#     form = AddRole()
#     if form.validate_on_submit():
#         new_one = Role(name=form.name.data,
#                        description=form.description.data
#                        )
#         db.session.add(new_one)
#         db.session.commit()
#         flash(f'Role added successful !', 'success')
#     return render_template('Manager/manager_roles.html', page_title="Manage Roles", form=form, roles=roles, tablea=True)

@manager.route("/manager/add_news", methods=['GET', 'POST'])
@roles_required('superuser')
def add_news():
    form = Add_News()
    if form.validate_on_submit():
        if form.image.data:
            picture_file = save_image(form.image.data)
            news = AddNews(title=form.title.data, discription=form.discription.data, content=form.content.data, user_id=current_user.id, image=picture_file)
            db.session.add(news)
            db.session.commit()
        else:
            news = AddNews(title=form.title.data,discription=form.discription.data,content=form.content.data,user_id=current_user.id)
            db.session.add(news)
            db.session.commit()
        flash('The News  has been Added!', 'success')
        return redirect(url_for('main.home'))
    return render_template('Manager/add_news.html', page_title="Add news", form=form, forma=True)

@manager.route("/manager/<int:news_id>/update_news", methods=['GET', 'POST'])
@roles_required('superuser')
def update_news(news_id):
    form = Update_News()
    unews = AddNews.query.get_or_404(news_id)
    if form.validate_on_submit():
        if form.image.data:
            picture_file = save_image(form.image.data)
            unews.title=form.title.data
            unews.discription = form.discription.data
            unews.content = form.content.data
            unews.image = picture_file
            db.session.commit()
        else:
            unews.title = form.title.data
            unews.discription = form.discription.data
            unews.content = form.content.data
            db.session.commit()
        flash('The News  has been Added!', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.title.data = unews.title
        form.discription.data = unews.discription
        form.content.data = unews.content
    return render_template('Manager/add_news.html', page_title="Update news", form=form, forma=True)

@manager.route("/manager/news/<int:news_id>/delete", methods=['POST'])
@roles_required('superuser')
def delete_news(news_id):
    news = AddNews.query.get_or_404(news_id)
    db.session.delete(news)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.news'))

# @manager.route("/manager/role/<int:role_id>/delete", methods=['POST'])
# @roles_required('superuser')
# def delete_role(role_id):
#     role = Role.query.get_or_404(role_id)
#     db.session.delete(role)
#     db.session.commit()
#     flash('Your Role has been deleted!', 'success')
#     return redirect(url_for('manager.roles'))

@manager.route("/manager/user/<int:user_id>/delete", methods=['POST'])
@roles_required('superuser')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Your User has been deleted!', 'success')
    return redirect(url_for('manager.users'))

@manager.route("/data/main_data", methods=['GET','POST'])
@roles_required('superuser')
def main_data():
    st_form = StateForm()
    l_form = LocalityForm()
    l_form.l_state_name.choices = [(state.state_name, state.state_name) for state in State.query.all()]

    ds_form = StateDeleteForm()
    dl_form = LocalityDeleteForm()
    ds_form.stateslist.choices = [(state.state_name, state.state_name) for state in State.query.all()]
    dl_form.localityslist.choices = [(locality.locality_name, locality.locality_name) for locality in Locality.query.all()]
    dl_form.dstateslist.choices = [(state.state_name, state.state_name) for state in State.query.all()]

    if st_form.validate_on_submit():
        state = State(state_name=st_form.state_name.data)
        db.session.add(state)
        db.session.commit()
        flash(f'{st_form.state_name.data} State  added successful !', 'success')
        return redirect(url_for('manager.main_data'))

    if l_form.validate_on_submit():
        start = State.query.filter_by(state_name=l_form.l_state_name.data).first()
        locality = Locality(locality_name=l_form.locality_name.data, state_in = start)
        db.session.add(locality)
        db.session.commit()
        flash(f'{l_form.locality_name.data}  Locality added successful !', 'success')
        return redirect(url_for('manager.main_data'))

    if ds_form.validate_on_submit():
        state = State.query.filter_by(state_name=ds_form.stateslist.data).first()
        db.session.delete(state)
        db.session.commit()
        flash(f'{ds_form.stateslist.data} State Deleted successful !', 'success')
        return redirect(url_for('manager.main_data'))

    if dl_form.validate_on_submit():
        locality = Locality.query.filter_by(locality_name=dl_form.localityslist.data).first()
        db.session.delete(locality)
        db.session.commit()
        flash(f'  {dl_form.localityslist.data}  Locality Deleted successful !', 'success')
        return redirect(url_for('manager.main_data'))



    return render_template('Manager/main_data.html', page_title="Main Data", forma = True, st_form = st_form, l_form = l_form,  dl_form = dl_form, ds_form=ds_form)

@manager.route("/data/import", methods=['POST','GET'])
@roles_required('superuser')
def importData():
    form = ImportDataForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(
            app.instance_path, 'photos', filename
        ))
        new = ImportData(file=form.file.data,sheet=form.sheet.data,rows =form.skiprows.data)
        new.ReadData()
        flash(f'Sheet {form.sheet.data} has been added to system', category='success')
    return render_template('Manager/import_data.html', page_title="Import Data", forma = True, form = form)
