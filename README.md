# ub-pyGooglesheets
Write data to google sheets from python

Step 1. Install on pyGooglesheets in sense: 
pip install git+ssh://git@github.com/unbounce/ub-pyGooglesheets.git@bi-1488-initial-version

Optional Step if you want to use in your own dev environment:

Step 2. Create a Google Service Account which is an account that doesn’t launch a browser and supports server-to-server interactions. The link can be found at https://developers.google.com/identity/protocols/OAuth2ServiceAccount
Ensure that your project in Google is enabled to allow server-to-server integration

Use this step in your dev environment (if you do not want to create a Google Service Account) and for production 

Step 3. Go to the Shared-Data Chapter folder in your Lastpass account

Step 4. Open the Sense Service Account  file and copy the contents between the { } brackets including the brackets	

Step 5. Paste the contents into file named service_account.json and put in sense console. Good practice is to have path “data/service_account.json” and copy that path

Step 6. Enter Google Service Account credentials from Step 2(dev) or Step 3(dev or prod) into their respective fields in the service_account.json file and save

Step 7. Share Google Sheets with the value of  the "client_email" attribute in the service_account.json

Sample Python Script 
# Write out to spreadsheet
import pygooglesheets

data = Snapshot_TotalConversionStats_ForAllTime_AsNow.toPandas()
credentials = 'data/pyGooglesheets/service_account.json'
connection = pygooglesheets.Connection(credentials=credentials,
  permissions="readwrite")
spreadsheet = pygooglesheets.Spreadsheet(
  '1FB53mvTmJmS_EM9rJwfZchkiKrKwf5WPBo7SewoTG54')
spreadsheet.update(connection, "conversions!A1:F2", numpy.vstack((data.keys(), data.values)))

data - dataframe in python derived (hiveSQL, etc)

credentials - your path to the service_account.json file saved in Step 6

connection - call to pygooglesheets connection function passing credentials and permissions(readwrite and w used for writing which is the only function at the moment)

spreadsheet - call to Spreadsheet function passing the Google Sheets Id associated with the document you want to write to. Ensure that Step 7 is complete. The Id is a series of alphanumeric characters between forward slashes

