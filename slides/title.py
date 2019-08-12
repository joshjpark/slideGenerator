from __future__ import print_function
import uuid
import urllib.request, json

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

gen_uuid = lambda : str(uuid.uuid4())  # generate random, unique UUID string from a standard library

SCOPES = 'https://www.googleapis.com/auth/presentations', # read write authorization
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
SLIDES = discovery.build('slides', 'v1', http=creds.authorize(Http())) # create the service end point for the slides API 
'''create a brand new presentation, then grab the title and subtitle textbox IDs from the default title slide from the API response from lines 23 to 25'''
print('** Create new slide deck & set up object IDs')
rsp = SLIDES.presentations().create(
        body={'title': 'Adding text & shapes DEMO'}).execute()
deckID = rsp['presentationId']
titleSlide  = rsp['slides'][0]      # title slide object IDs
titleID     = titleSlide['pageElements'][0]['objectId']
subtitleID  = titleSlide['pageElements'][1]['objectId']
'''create randomly generated object ID's as in line 9'''
mpSlideID   = gen_uuid()            # mainpoint IDs
mpTextboxID = gen_uuid()
smileID     = gen_uuid()            # shape IDs
str24ID     = gen_uuid()
arwbxID     = gen_uuid()
mdSlideID   = gen_uuid()            # recent slide
mdTextboxID = gen_uuid()            # copied slide object ID

print('** Create "main point" slide, add text & logo')

request = [
    # create third slide
    {'createSlide': {
        'objectId': mdSlideID,
        'slideLayoutReference': {'predefinedLayout': 'MAIN_POINT'},
        'placeholderIdMappings': [{
            'objectId': mdTextboxID,
            'layoutPlaceholder': {'type': 'TITLE', 'index':0}
        }],
    }},

    # insert text 'this is created slide' into the objectId
    {
    'insertText': {'objectId': mdTextboxID, 'text': 'WORSHIP SERVICE'}
    },

    {
    'updateTextStyle': {
    	'objectId': mdTextboxID,
    	'style': {
    		'bold': True,
    		'fontFamily' : 'Courier New',
    		'fontSize': {
    			'magnitude': 14,
    			'unit': 'PT'
    		}
    	},
    	'textRange' : {'type': 'FIXED_RANGE', 'startIndex' : 0, 'endIndex': len('WO\nRSHIP SERVICE')},
    	'fields': 'fontFamily, fontSize, bold'
    	}
    }



    # change text style: enable italics, font to Courier New 
    # {
    # 'updateTextStyle': {
    #     'objectId': mdTextboxID,
    #     'style': {'fontFamily': 'Courier New'},
    #     'textRange': {'type': 'FIXED_RANGE'}
    #     }
    # }

   


]

SLIDES.presentations().batchUpdate(body={'requests': request},
        presentationId=deckID).execute()
