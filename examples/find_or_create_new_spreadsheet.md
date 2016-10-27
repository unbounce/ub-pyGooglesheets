# How to do a find or create of a spreadsheet by name

This requires using some techniques beyond just ub-pyGooglesheets, we'll also
need to create connections using the baseline google api client to access
Google Drive specific functionality. At a high level what we'll do is use Google
Drive to get the list of sheets we can access, check if any of those sheets have
the right name, and if not, use pygooglesheets to create a new spreadsheet.

**Step 1:** Create a connection to Google APIs and then get a Google Drive service.

*NOTE: You need to have a `service'account.json` file with real credentials. The
application the account is associated with also needs to have API permissions
granted for Google Drive **AND** Google Sheets*

    import pygooglesheets

    from oauth2client.service_account import ServiceAccountCredentials
    from apiclient import discovery
    import httplib2

    # The lowest level scope we can use is drive.metadata.readonly
    SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'service-account.json', scopes=SCOPES)
    http = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http=http)

**Step 2:** Once we have a drive service we can do all sorts of fun things. For now
let's get a list of files that match the mime type for Google Spreadsheets

    sheets = drive_service.files().list(q="mimeType='application/vnd.google-apps.spreadsheet'").execute()

**Step 3:** Now we can spin through the sheets to see if any of them match the name we are interested in (here we hardcode the name to `'My Spreadsheet'`)

    matching_sheets = [ sheet for sheet in sheets['files'] if sheet['name'] == 'My Spreadsheet']

**Step 4:** If there are matching sheets - instantiate a
`pygooglesheets.Spreadsheet` object from its `id`
and we're done! Otherwise, create a new `pygooglesheets.Spreadsheet` using the
`pygooglesheets.collection.create` factory

*NOTE: If there are multiple matching sheets you probably don't want to just randomly grab the first... but this is an example so we're ignoring the problem*

    if matching_sheets:
        target_sheet = pygooglesheets.Spreadsheet(id=matching_sheets[0]['id'])
    else:
        connection = pygooglesheets.Connection(credentials='service-account-private.json',
            permissions='readwrite')
        target_sheet = pygooglesheets.collection.create(connection=connection, name='My Spreadsheet')

**Step 5:** Do fun things with your sheet!
