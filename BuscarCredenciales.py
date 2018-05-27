import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas

config_file = open('./config.json','r')
config = json.load(config_file)

scope = config['scope']
creds = ServiceAccountCredentials.from_json_keyfile_name(config['pathClientSecret'],scope)
client = gspread.authorize(creds)

sheet = client.open(config['archivo']['credencialesSFSF']['sheet'])
worksheet = sheet.worksheet(config['archivo']['credencialesSFSF']['workSheet'])

wsheet = worksheet.get_all_values()

# header -> primera fila es un comentario
df = pandas.DataFrame.from_records(wsheet[1:])

# .values -> array o matriz
header = (df.loc[df[0] == 'Cliente']).values[0]
dataSet = (df.loc[df[0] != 'Cliente']).values

dff = pandas.DataFrame.from_records(dataSet, columns = header)

def BuscarCredenciales (cliente, ambiente = ''):
	cliente = dff.Cliente == cliente

	config.close()

	if (ambiente != ''):
		ambiente = dff['Tipo Acceso'] == ambiente

		return dff.loc[cliente & ambiente]
	else:
		return dff.loc[cliente]