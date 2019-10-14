import pandas
class ImportData():
    def __init__(self, file, sheet, rows):
        self.file = file
        self.sheet = sheet
        self.rows = rows

    def ReadData(self):
        data = pandas.read_excel(self.file,sheet_name=self.sheet,skiprows=self.rows, header=0)
        dataframeN = pandas.DataFrame(data=data,  dtype=None)
        dataframe = dataframeN.where((pandas.notnull(dataframeN)), None)
        for index, row in dataframe.iterrows():

            database = WS_Data_EX(
                 state=str(row['State']), locality=row['Locality'],
                 settlement=row['Settlement English'], name=row['Name'], type=row['Type '],
                status=row['If Others, specify'], manage_by=row['Status'], longitude=row['Longitude'],
                latitude=row['Latitude'], date=row['Date'], e_coli=row['E.Coli/100 ml'], sis=row['Sanitary Inspection Score'],
                risk_analysis=row['Risk Analysis'], action_take=row['Action taken?'], frc=row['RFC'],
                turbidity=row['Turbidity'], ph=row['pH'], tds=row['TDS'], ec=row['E.C'], f=row['F'],
                no3=row['NO3'], cl2=row['CL2'], fe=row['Fe']
            )

            db.session.add(database)

        db.session.commit()
        print('Finish .......')


def savefile(file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    file_fn = random_hex + f_ext
    file_path = os.path.join(current_app.root_path, 'static/files', file_fn)

    return file_path