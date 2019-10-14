from flask import Flask, redirect, url_for, render_template, Blueprint, flash, jsonify, request
from flask_security import login_user, current_user, logout_user, login_required
from Server.main.form import WForm, WFormUpdate
from Server.main.risk_analysis import JDataRead
from Server.models import State, Locality, WS_Data, AddNews, User
from Server import db
from flask import current_app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
@login_required
def home():

    news3 = AddNews.query.order_by(AddNews.date.desc()).limit(3)
    return render_template('home.html', page_title="Home", news3=news3)

@main.route("/news")
@login_required
def news():
    page = request.args.get('page', 1, type=int)
    news_a = AddNews.query.order_by(AddNews.date.desc()).paginate(page=page, per_page=6)
    return render_template('news.html', page_title="News", news_a=news_a)

@main.route("/news/<int:news>")
def news_fully(news):
    news_full = AddNews.query.get_or_404(news)
    return render_template('news_full.html', page_title="News Full", news=news_full)

@main.route("/data/data_entering", methods=['GET','POST'])
@login_required
def data_entering():
    form = WForm()
    form.state.data = current_user.state
    form.locality.data = current_user.locality
    if form.validate_on_submit():

        if form.action_take.data == "No":
            action = form.action_take.data
            yes_on_ongoing = ''

        else:
            yes_on_ongoing = form.if_yes.data
            action = form.action_take.data

        if form.type.data == "Other":
            type_ws = form.other_type.data
        else:
            type_ws = form.type.data
        saved_form = WS_Data(
            user_id=current_user.id, state=form.state.data, locality=form.locality.data,
            settlement=form.settlement.data, name=form.name.data, type=type_ws,
            status=form.status.data, manage_by=form.manage_by.data, longitude=form.longitude.data,
            latitude=form.latitude.data, date=form.date.data, e_coli=form.e_coli.data, sis=form.sis.data,
            risk_analysis=form.risk_analysis.data, action_take=action,if_yes_or_ongoing=yes_on_ongoing, frc=form.frc.data,
            turbidity=form.turbidity.data, ph=form.ph.data, tds=form.tds.data, ec=form.ec.data, f=form.f.data,
            no3=form.no3.data, cl2=form.cl2.data, fe=form.fe.data
        )
        db.session.add(saved_form)
        db.session.commit()
        flash(f'Form added successful !', 'success')
        return redirect(url_for('main.data_entering'))
    return render_template('Data/data_entering.html',main_title = "Data Entering", page_title="Water Sources Monitoring",
                           forma = True , form = form )

@main.route("/data", methods=['GET','POST'])
@login_required
def data():
    if current_user.has_role('superuser'):
        ws_data = WS_Data.query.all()
    elif current_user.has_role('state_manager'):
        ws_data = WS_Data.query.filter_by(state=current_user.state)
    elif current_user.has_role('locality_manager'):
        ws_data = WS_Data.query.filter_by(locality=current_user.locality)
    else:
        ws_data = WS_Data.query.filter_by(user_id=current_user.id)
    return render_template('Data/data.html', page_title="Data", tablea=True, ws_data=ws_data)

@main.route('/data/locality/<state>')
@login_required
def locality(state):
    start = State.query.filter_by(state_name=state).first()
    localitys = Locality.query.filter_by(state_in = start)

    localityArray = []

    for locality in localitys:
        localityObj = {}
        localityObj['id'] = locality.id
        localityObj['locality_name'] = locality.locality_name
        localityArray.append(localityObj)

    return jsonify({'localitys': localityArray})

@main.route('/data/function/<key>')
@login_required
def function(key):
    data = JDataRead()
    value = data[key]
    return jsonify({'value': value})

@main.route("/data/<int:data_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_data(data_id):
    data = WS_Data.query.get_or_404(data_id)
    # if data.editor != current_user:
    #     abort(403)
    form = WForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.action_take.data == "No":
                action = form.action_take.data
            elif form.action_take.data == "Yes":
                yes = form.if_yes.data
                try:
                    fyes = yes.split(' : ')
                    action = 'Yes : '+fyes[1]
                except:
                    action = 'Yes : ' + form.if_yes.data
            else:
                ongoing = form.if_yes.data
                try:
                    fongoing = ongoing.split(' : ')
                    action = 'On Going : ' + fongoing[1]
                except:
                    action = 'On Going : ' + form.if_yes.data

            if form.type.data == "Other":
                type_ws = form.other_type.data
            else:
                type_ws = form.type.data
            data.id = data_id
            data.state = form.state.data
            data.date_of_commet = datetime.utcnow()
            data.locality = form.locality.data
            data.settlement = form.settlement.data
            data.name = form.name.data
            data.type = type_ws
            data.status = form.status.data
            data.manage_by = form.manage_by.data
            data.longitude = form.longitude.data
            data.latitude = form.latitude.data
            data.date = form.date.data
            data.e_coli = form.e_coli.data
            data.sis = form.sis.data
            data.risk_analysis = form.risk_analysis.data
            data.action_take = action
            data.turbidity = form.turbidity.data
            data.ph = form.ph.data
            data.tds = form.tds.data
            data.ec = form.ec.data
            data.f = form.f.data
            data.no3 = form.no3.data
            data.cl2 = form.cl2.data
            data.fe = form.fe.data
            db.session.commit()
            flash('Your Data has been updated!', 'success')
            return redirect(url_for('main.data'))
    elif request.method == 'GET':
        if data.action_take == "No":
            form.action_take.data = data.action_take
        # else:
        #     form.action_take.data = "Yes"
        #     form.if_yes.data =data.action_take
        else:
            myaction = data.action_take
            faction = myaction.split(' : ')
            if faction[0] == "Yes":
                form.action_take.data = "Yes"
                form.if_yes.data = faction[1]
            else:
                form.action_take.data = "On Going"
                form.if_yes.data = faction[1]

        if data.type == "Borehole" or "H.P" or "O.D.W" or "Strong Tank" :
            form.type.data = data.type
        else:
            form.type.data = "Other"
            form.other_type.data = data.type
        form.state.data = data.state
        form.locality.data = data.locality
        form.settlement.data = data.settlement
        form.name.data = data.name
        form.status.data = data.status
        form.manage_by.data = data.manage_by
        form.longitude.data = data.longitude
        form.latitude.data = data.latitude
        form.date.data = data.date
        form.e_coli.data = data.e_coli
        form.sis.data = data.sis
        form.turbidity.data = data.turbidity
        form.ph.data = data.ph
        form.tds.data = data.tds
        form.ec.data = data.ec
        form.f.data = data.f
        form.no3.data = data.no3
        form.cl2.data = data.cl2
        form.fe.data = data.fe
        form.frc.data = data.frc
    return render_template('Data/data_entering.html',main_title = "Data Edit", page_title="Water Sources Monitoring",
                           forma = True , form = form )

@main.route("/data/<int:data_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_data(data_id):
    data = WS_Data.query.get_or_404(data_id)
    # if data.editor != current_user:
    #     abort(403)
    db.session.delete(data)
    db.session.commit()
    flash('Your Data has been deleted!', 'success')
    return redirect(url_for('main.data'))

@main.route("/data/<int:data_id>/update", methods=['GET', 'POST'])
@login_required
def update_data(data_id):
    data = WS_Data.query.get_or_404(data_id)
    form = WFormUpdate()
    if request.method == 'GET':
        if data.action_take == "No":
            form.action_take.data = data.action_take
        # else:
        #     form.action_take.data = "Yes"
        #     form.if_yes.data =data.action_take
        else:
            myaction = data.action_take
            faction = myaction.split(' : ')
            if faction[0] == "Yes":
                form.action_take.data = "Yes"
                form.if_yes.data = faction[1]
            else:
                form.action_take.data = "On Going"
                form.if_yes.data = faction[1]

        if data.type == "Borehole" or "H.P" or "O.D.W" or "Strong Tank":
            form.type.data = data.type
        else:
            form.type.data = "Other"
            form.other_type.data = data.type
        form.state.data = data.state
        form.locality.data = data.locality
        form.settlement.data = data.settlement
        form.name.data = data.name
        form.status.data = data.status
        form.manage_by.data = data.manage_by
        form.longitude.data = data.longitude
        form.latitude.data = data.latitude
        form.date.data = data.date
        form.e_coli.data = data.e_coli
        form.sis.data = data.sis
        form.turbidity.data = data.turbidity
        form.ph.data = data.ph
        form.tds.data = data.tds
        form.ec.data = data.ec
        form.f.data = data.f
        form.no3.data = data.no3
        form.cl2.data = data.cl2
        form.fe.data = data.fe
        form.frc.data = data.frc
    elif request.method == 'POST':
        if form.validate_on_submit():

            if form.action_take.data == "No":
                action = form.action_take.data
            elif form.action_take.data == "Yes":
                action = 'Yes : ' + form.if_yes.data
            else:
                action = 'On Going : ' + form.if_yes.data

            if form.type.data == "Other":
                type_ws = form.other_type.data
            else:
                type_ws = form.type.data
            saved_form = WS_Data(
                user_id=current_user.id, state=form.state.data, locality=form.locality.data,
                settlement=form.settlement.data, name=form.name.data, type=type_ws,
                status=form.status.data, manage_by=form.manage_by.data, longitude=form.longitude.data,
                latitude=form.latitude.data, date=form.date.data, e_coli=form.e_coli.data, sis=form.sis.data,
                risk_analysis=form.risk_analysis.data, action_take=action, frc=form.frc.data,
                turbidity=form.turbidity.data, ph=form.ph.data, tds=form.tds.data, ec=form.ec.data, f=form.f.data,
                no3=form.no3.data, cl2=form.cl2.data, fe=form.fe.data
            )
            db.session.add(saved_form)
            db.session.commit()
            flash(f'Form Updated successful !', 'success')
            return redirect(url_for('main.data'))
    return render_template('Data/data_entering.html', main_title="Data Update", page_title="Water Sources Monitoring",
                           forma=True, form=form)