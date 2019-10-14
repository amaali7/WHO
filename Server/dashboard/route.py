from flask import Flask, redirect, url_for, render_template, Blueprint, flash, jsonify, request
from flask_security import login_user, current_user, logout_user, roles_required
from Server.models import State, Locality, WS_Data, Dashboard, Chart
from Server.dashboard.form import ChartPrepare, DashBoard
from Server.dashboard.data_analysis.main import GetData
from Server import db, Net_CDN
from flask import current_app
from random import sample

dashboard = Blueprint('dashboard', __name__)


@dashboard.route("/dashboard", methods=['GET', 'POST'])
@roles_required('superuser')
def dashboard_home():
    form = DashBoard()
    page = request.args.get('page', 1, type=int)
    dashboards = Dashboard.query.order_by(Dashboard.date.desc()).paginate(page=page, per_page=6)
    if form.validate_on_submit():
        dashboard = Dashboard(name=form.name.data, title=form.title.data, description=form.description.data, user_id=current_user.id)
        db.session.add(dashboard)
        db.session.commit()
        return redirect(url_for('dashboard.dashboard_home'))
    return render_template('dashboard/dashboard_home.html', page_title="Dashboard", forma=True, form=form, dashboards=dashboards)


@dashboard.route("/dashboard/dashboard/<int:dashboard_id>", methods=['GET', 'POST'])
@roles_required('superuser')
def dashboard_page(dashboard_id):
    dashboardin = Dashboard.query.filter_by(id=dashboard_id).first()
    chartsindb = Chart.query.filter_by(chart_in=dashboardin)

    form = ChartPrepare()
    form.statefilter.choices = [(state.state_name, state.state_name) for state in State.query.all()]
    form.localityfilter.choices = [(locality.locality_name, locality.locality_name) for locality in
                                   Locality.query.filter_by(state_in_id=1)]
    if form.validate_on_submit():
        chartdb = Chart(
            name=form.name.data, startdate=form.startdate.data, enddate=form.enddate.data, statefilter=form.statefilter.data, localityfilter=form.localityfilter.data, typefilter=form.typefilter.data, riskfilter=form.riskfilter.data, actionfilter=form.actionfilter.data, status=form.status.data,
            series1=form.series1.data, series1_background=form.series1_background.data, series1_border=form.series1_border.data,
            series2=form.series2.data, series2_background=form.series2_background.data, series2_border=form.series2_border.data,
            series3=form.series3.data, series3_background=form.series3_background.data, series3_border=form.series3_border.data,
            series4=form.series4.data, series4_background=form.series4_background.data, series4_border=form.series4_border.data,
        chart_type=form.chart_type.data, dashboard_in=dashboardin.id
        )
        db.session.add(chartdb)
        db.session.commit()

    data = WS_Data.query.filter_by(date > data.startdate).filter_by(date < data.enddate).filter_by(state=Khartoum)
    print(data)
    # for chart in chartsindb:
    #     data = GetData(chart)
    #     for d in data:
    #         print(d.f)

    return render_template('dashboard/dashboard.html', page_title="Dashboard", forma=True, form=form, dashboard=dashboard
                           ,chartsindb=chartsindb)


