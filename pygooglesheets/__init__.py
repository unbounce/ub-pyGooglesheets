import pygooglesheets.collection
from .connection import pygooglesheets.Connection
from .spreadsheet import pygooglesheets.Spreadsheet


# Example code
# import pygooglesheets
#
# write_connection = pygooglesheets.Connection(
#   credentials = 'service_account.json'),
#   permissions = 'readwrite' )
# spreadsheet = pygooglesheets.Spreadsheet(
#   '1fgOEqugOhbsV_Ntq53xqY40i3otkA-4Qq-uzQaT1q3M')
# data = pygooglesheets.data.dataframe(df)
# spreadsheet.update(write_connection, data)
