import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
from pprint import pprint
import pandas as pd

scope = ['https://www.googleapis.com/auth/drive.readonly']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json',scope)
client = gspread.authorize(creds)

sheet = client.open('Test SFSF Accesos')
worksheet = sheet.worksheet('SFSF')

wsheet = worksheet.get_all_values()
df = pd.DataFrame.from_records(wsheet[1:])

# .values -> array o matriz
header = (df.loc[df[0] == 'Cliente']).values[0]
dataSet = (df.loc[df[0] != 'Cliente']).values

dff = pd.DataFrame.from_records(dataSet, columns = header)

cliente = dff.Cliente == 'Arauco'
ambiente = dff['Tipo Acceso'] == 'DEV'

dff.loc[cliente & ambiente]