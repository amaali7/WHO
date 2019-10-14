import pandas as pd
from Server.models import WS_Data

def GetData(DataBase):
    if DataBase:
        data = DataBase
        cmd = 'WS_Data.query.filter_by(date > data.startdate).filter_by(date < data.enddate)'
        if data.statefilter != "None":
            cmd = cmd + f'.filter_by(state={data.statefilter})'
        elif data.localityfilter != "None":
            cmd = cmd + f'.filter_by(locality={data.statefilter})'
        elif data.typefilter != "None":
            cmd = cmd + f'.filter_by(type={data.typefilter})'
        elif data.riskfilter != "None":
            cmd = cmd + f'.filter_by(risk_analysis={data.riskfilter})'
        elif data.actionfilter != "None":
            cmd = cmd + f'.filter_by(action_take={data.actionfilter})'
        elif data.status != "None":
            cmd = cmd + f'.filter_by(state={data.status})'

        print(cmd)

    return exec(cmd)


