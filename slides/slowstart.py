#(1) Standard set up for Google Slides API 
from __future__ import print_function
import uuid
import urllib.request, json

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import requests

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
spSlideID   = gen_uuid()
mpTextboxID = gen_uuid()
smileID     = gen_uuid()            # shape IDs
str24ID     = gen_uuid()
arwbxID     = gen_uuid()
mdSlideID   = gen_uuid()            # recent slide
mdTextboxID = gen_uuid()            # copied slide object ID
reTextboxID = gen_uuid()            # grab textbox id




'''NOTE: Why should you generated using gen_uuid() rather than resorting to default 
values of API? Because you can use these for the remaining requests in a single batch. '''

'''request to create a new slide for our shapes'''

print('** Create "main point" slide, add text & interesting shapes')
reqs = [

    # create new "main point" layout slide, giving slide & textbox IDs; the placeholder ID mapping
    # is an array to provide the IDs for the elements that are part of that layout. In this example, we only have one element because it has only one largish textbox. 
    {'createSlide': {
        'objectId': mpSlideID,
        'slideLayoutReference': {'predefinedLayout': 'MAIN_POINT'},
        'placeholderIdMappings': [{
            'objectId': mpTextboxID,
            'layoutPlaceholder': {'type': 'TITLE', 'index': 0}
        }],
    }},
    # add title & subtitle to title slide; add text to main point slide textbox
    {'insertText': {'objectId': titleID,     'text': 'Hello world!'}},
    {'insertText': {'objectId': subtitleID,  'text': 'via the Google Slides API'}},
    {'insertText': {'objectId': mpTextboxID, 'text': 'text & shapes'}},
    # create smiley face
    # NOTE: take a look at the Page Elements page in the documentation as well as the Transforms Concept Guide for more details. 
    {'createShape': {
        'objectId': smileID,
        'shapeType': 'SMILEY_FACE',
        'elementProperties': {
            "pageObjectId": mpSlideID,
            'size': {
                'height': {'magnitude': 3000000, 'unit': 'EMU'},
                'width':  {'magnitude': 3000000, 'unit': 'EMU'}
            },
            'transform': {
                'unit': 'EMU', 'scaleX': 1.3449, 'scaleY': 1.3031,
                'translateX': 4671925, 'translateY': 450150,
            },
        },
    }},
    # create 24-point star
    {'createShape': {
        'objectId': str24ID,
        'shapeType': 'STAR_24',
        'elementProperties': {
            "pageObjectId": mpSlideID,
            'size': {
                'height': {'magnitude': 3000000, 'unit': 'EMU'},
                'width':  {'magnitude': 3000000, 'unit': 'EMU'}
            },
            'transform': {
                'unit': 'EMU', 'scaleX': 0.7079, 'scaleY': 0.6204,
                'translateX': 2036175, 'translateY': 237350,
            },
        },
    }},
    # create double left & right arrow w/textbox
    {'createShape': {
        'objectId': arwbxID,
        'shapeType': 'LEFT_RIGHT_ARROW_CALLOUT',
        'elementProperties': {
            "pageObjectId": mpSlideID,
            'size': {
                'height': {'magnitude': 3000000, 'unit': 'EMU'},
                'width':  {'magnitude': 3000000, 'unit': 'EMU'}
            },
            'transform': {
                'unit': 'EMU', 'scaleX': 1.1451, 'scaleY': 0.4539,
                'translateX': 1036825, 'translateY': 3235375,
            },
        },
    }},
    # add text to all 3 shapes
    {'insertText': {'objectId': smileID, 'text': 'FFKKK!'}},
    {'insertText': {'objectId': str24ID, 'text': 'Count 24 points on this star!'}},
    {'insertText': {'objectId': arwbxID, 'text': "An uber bizarre arrow box!"}},

    #Operation (1): Read slide object IDs

    #Operation (2): Read element object IDs from a page

    #Operation (3): Read shape elements from a page
]
SLIDES.presentations().batchUpdate(body={'requests': reqs},
        presentationId=deckID).execute()

# print(SLIDES.presentations().get(presentationId = deckID))
# print(dir(SLIDES.presentations()))


#simplement request
# request = [
#     {'createSlide': {
#         'objectId': mdSlideID,
#     }}
#     {'insertText': {'objectId': randId, 'text': 'Hello world!'}}
# ]

with urllib.request.urlopen("http://labs.bible.org/api/?passage=John%206:22-45&type=json&formatting=plain") as url:
    data = json.loads(url.read().decode())

print("Copy/paste verses 22...")
phrase = data[0]["verse"] + " " + data[0]["text"] + "\n\n" + data[1]["verse"] + " " + data[1]["text"]


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
    'insertText': {'objectId': mdTextboxID, 'text': phrase}
    },

    # change text style: enable italics, font to Courier New 
    # {
    # 'updateTextStyle': {
    #     'objectId': mdTextboxID,
    #     'style': {'fontFamily': 'Courier New'},
    #     'textRange': {'type': 'FIXED_RANGE'}
    #     }
    # }
    {
    'updateTextStyle': {
        'objectId': mdTextboxID,
        'style': {
            'fontFamily':'Courier New',
            'fontSize': {
                'magnitude':14,
                'unit': 'PT'
        }
    },
        'textRange': {'type': 'FIXED_RANGE', 'startIndex' : 0, 'endIndex': len(phrase)},
        'fields': 'fontFamily, fontSize'
    }


    },

    #insert image 
    {
    'updatePageProperties': {
        "objectId": mdSlideID, 
        'pageProperties': {
            'pageBackgroundFill': {
                'stretchedPictureFill': {
                    'contentUrl': 'https://visme.co/blog/wp-content/uploads/2017/07/50-Beautiful-and-Minimalist-Presentation-Backgrounds-025.jpg'
                    }
                }
            },
            'fields': 'pageBackgroundFill'
        }
    },

    {
    'updatePageProperties': {
        "objectId": mpSlideID, 
        'pageProperties': {
            'pageBackgroundFill': {
                'stretchedPictureFill': {
                    'contentUrl': 'https://visme.co/blog/wp-content/uploads/2017/07/50-Beautiful-and-Minimalist-Presentation-Backgrounds-025.jpg'
                    }
                }
            },
            'fields': 'pageBackgroundFill'
        }
    }


]

SLIDES.presentations().batchUpdate(body={'requests': request},
        presentationId=deckID).execute()

further_req = [
    {'createSlide': {
        'objectId': spSlideID
    }}

]

SLIDES.presentations().batchUpdate(body={'requests': further_req},
        presentationId=deckID).execute()

# further_req = [
#     {'createSlide': {
#         'objectId': mpSlideID,
#         'pageElements': [
#         {
#             'objectId': mpTextboxID,
#             'size': {
#                 'width': {
#                     'magnitude': 3000000,
#                     'unit': 'EMU'
#                 },
#                 'height': {
#                     'magnitude': 3000000,
#                     'unit': 'EMU'
#                 }
#             },
#             'transform': {
#                 'scaleX': 2.8402,
#                 'scaleY': 0.6842,
#                 'translateX': 311708.35000000003,
#                 'translateY': 744575,
#                 'unit': 'EMU'
#             },
#             'shape': {
#                 'shapeType': 'TEXT_BOX',
#                 'text': {
#                     'textElements': [
#                         {
#                             'endIndex': 7,
#                             'paragraphMarker': {
#                                 'style': {
#                                     'direction': 'LEFT_TO_RIGHT'
#                                 }
#                             }
#                         },
#                         {
#                         'endIndex': 7,
#                         'paragraphMarker': {
#                             'style': {
#                                 'direction': 'LEFT_TO_RIGHT'
#                             }
#                         }
#                         }, 
#                         {
#                         'endIndex': 7,
#                         'textRun': {
#                             'content': 'SUNDAY\n',
#                             'style': {
#                             'bold': True,
#                             'fontFamily': 'Georgia',
#                             'weightedFontFamily': {
#                                 'fontFamily': 'Georgia',
#                                 'weight': 700
#                             }
#                             }
#                         }
#                         }

#                     ]
#                 }
#             }
#         }
#         ]
#     }}
# ]

# SLIDES.presentations().batchUpdate(body={'requests': further_req},
#         presentationId=deckID).execute()


#Create a new slide with textbox in the middle
# requests = [
#     {'createSlide': {
#         'objectId': mpSlideID,
#         'pageElements': [

#         {'objectId': reTextboxID}]
#     }}

# ]


# further_request = [
#     {'slides': [
#         'objectId': mpSlideID,
#         'pageElements': [
#         {
#             'objectId': mpTextboxID,
#             'size': {
#                 'width': {
#                     'magnitude': 3000000,
#                     'unit': 'EMU'
#                 },
#                 'height': {
#                     'magnitude': 3000000,
#                     'unit': 'EMU'
#                 }
#             },
#             'transform': {
#                 'scaleX': 2.8402,
#                 'scaleY': 0.6842,
#                 'translateX': 311708.35000000003,
#                 'translateY': 744575,
#                 'unit': 'EMU'
#             },
#             'shape': {
#                 'shapeType': 'TEXT_BOX',
#                 'text': {
#                     'textElements': [
#                     {
#                         'endIndex': 7,
#                         'paragraphMarker': {
#                             'style': {
#                                 'direction': 'LEFT_TO_RIGHT'
#                             }
#                         }
#                     },
#                     {
#                     'endIndex': 7, 
#                     'paragraphMarker': {
#                         'style': {
#                             'direction': 'LEFT_TO_RIGHT'
#                         }
#                     }
#                     },
#                     {
#                     'endIndex': 7,
#                     'textRun': {
#                         'content': 'SUNDAY\n',
#                         'style': {
#                         'bold': true,
#                         'fontFamily': 'Georgia',
#                         'weightedFontFamily': {
#                             'fontFamily': 'Georgia',
#                             'weight': 700
#                         }
#                         }
#                     }


#                     }
#                     ]
#                 }
#             }
#         }
#         ]
#     ]
#     }

# ]


#The following code will create the title page



#a = SLIDES.presentations()
#a.get('https://slides.googleapis.com/v1/presentations/1k6MdXoCg-CVXCrONlH3IMs64JZwvNgGG0DoVx5MZaSk')


#Plan of Attack:

#(1) Think about APIs that need to be developed
#   Some I can think of right now:
#       (a) create_newSlides()
#       (b) create_titlePage(date = '2019-05-20', theme = 'calm')
#       (c) create_verses(verses = 'pass', theme = 'calm')
#       (c) 
#       (d) 
#       (e) 
#       (f) 
#       (g) 

# Parittioned into 
# title page -> read

#What I want to do now is to build something, and retrieve data from it from web page to code 

# # Operation (1): Read slide object IDs
# # Explanation: Retrieve data of a Google Slide (source: https://github.com/googleapis/google-api-python-client/issues/424)
# slideObjectId = SLIDES.presentations().get(presentationId = deckID)
# print(slideObjectId.presentationId())
# # Operation (2): Read element object IDs
# # Explanation: Retrieve data of a Google Slide page 
# elementObjectId = SLIDES.presentations().pages().get(presentationId = deckID, pageObjectId = 1)
# print(type(elementObjectId))


# Operations:
# (1) api_update()
# (2) 



print('DONE')
