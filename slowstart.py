#(1) Standard set up for Google Slides API 
from __future__ import print_function
import uuid

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
deckID = rsp['presentationId']      # presentationID from https (url) address
titleSlide  = rsp['slides'][0]      # title slide object IDs
titleID     = titleSlide['pageElements'][0]['objectId']
subtitleID  = titleSlide['pageElements'][1]['objectId']
'''create randomly generated object ID's as in line 9'''
mpSlideID   = gen_uuid()            # mainpoint IDs
mpTextboxID = gen_uuid()
smileID     = gen_uuid()            # shape IDs
str24ID     = gen_uuid()
arwbxID     = gen_uuid()
spSlideID   = gen_uuid()


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
    {'insertText': {'objectId': smileID, 'text': 'Put the nose somewhere here!'}},
    {'insertText': {'objectId': str24ID, 'text': 'Count 24 points on this star!'}},
    {'insertText': {'objectId': arwbxID, 'text': "An uber bizarre arrow box!"}},
]
SLIDES.presentations().batchUpdate(body={'requests': reqs},
        presentationId=deckID).execute()


''' 
create empty slide
@returns:   slideID of created slide
'''
def createEmptySlide():
    slideNewID = gen_uuid()
    send_req = [
        {'createSlide': {
            'objectId': slideNewID
        }}
    ]
    SLIDES.presentations().batchUpdate(body={'requests': send_req},
            presentationId=deckID).execute()
    return slideNewID


'''
create slide with text
@param:     msg 
'''
def createSlideWithText(msg):
    slideNewID = gen_uuid()
    textBoxID = gen_uuid()

    send_req = [
        {'createSlide': {
            'objectId': slideNewID,
            'slideLayoutReference': {'predefinedLayout': 'MAIN_POINT'},
            'placeholderIdMappings': [{
                'objectId': textBoxID,
                'layoutPlaceholder': {'type': 'TITLE', 'index': 0}
            }],
        }},

        {'insertText': {'objectId': textBoxID, 'text': msg}}
    ]
    SLIDES.presentations().batchUpdate(body={'requests': send_req},
            presentationId=deckID).execute()


'''
create slide with background
@param:     url of image to insert
'''
def createSlideWithBackground(url):
    slideNewID = gen_uuid()
    
    send_req = [
        {'createSlide': {
            'objectId': slideNewID            
        }}, 

        {
            'updatePageProperties': {
                'objectId': slideNewID,
                'pageProperties': {
                    'pageBackgroundFill': {
                        'stretchedPictureFill': {
                            'contentUrl': url
                        }
                    }
                },
                'fields': 'pageBackgroundFill'
            }
        }
    ]

    SLIDES.presentations().batchUpdate(body={'requests': send_req},
        presentationId=deckID).execute()


'''
create text with font
@param:     phrase
@param:     font
@param:     size
'''
def createSlideTextandFont(phrase, font, size):
    slideNewID = gen_uuid()
    textBoxID = gen_uuid()
    send_req = [
        {'createSlide': {
            'objectId': slideNewID,
            'slideLayoutReference': {'predefinedLayout': 'MAIN_POINT'},
            'placeholderIdMappings': [{
                'objectId': textBoxID,
                'layoutPlaceholder': {'type': 'TITLE', 'index':0}
            }],
        }},
        
        {
        'insertText': {'objectId': textBoxID, 'text': phrase}
        },
        
        {
        'updateTextStyle': {
            'objectId': textBoxID,
            'style': {
                'fontFamily': font,
                'fontSize': {
                    'magnitude':size,
                    'unit': 'PT'
            }
        },
            'textRange': {'type': 'FIXED_RANGE', 'startIndex' : 0, 'endIndex': len(phrase)},
            'fields': 'fontFamily, fontSize'
        }
        }
    ]
    SLIDES.presentations().batchUpdate(body={'requests': send_req},
    presentationId=deckID).execute()


def createSlideTextFontBackground(phrase, font, size, url):
    slideNewID = gen_uuid()
    textBoxID = gen_uuid()
    send_req = [
        {'createSlide': {
            'objectId': slideNewID,
            'slideLayoutReference': {'predefinedLayout': 'MAIN_POINT'},
            'placeholderIdMappings': [{
                'objectId': textBoxID,
                'layoutPlaceholder': {'type': 'TITLE', 'index':0}
            }],
        }},
        
        {
        'insertText': {'objectId': textBoxID, 'text': phrase}
        },
        
        {
        'updateTextStyle': {
            'objectId': textBoxID,
            'style': {
                'fontFamily': font,
                'fontSize': {
                    'magnitude':size,
                    'unit': 'PT'
            }
        },
            'textRange': {'type': 'FIXED_RANGE', 'startIndex' : 0, 'endIndex': len(phrase)},
            'fields': 'fontFamily, fontSize'
        }
        },

        {
            'updatePageProperties': {
                'objectId': slideNewID,
                'pageProperties': {
                    'pageBackgroundFill': {
                        'stretchedPictureFill': {
                            'contentUrl': url
                        }
                    }
                },
                'fields': 'pageBackgroundFill'
            }
        }
    ]
    SLIDES.presentations().batchUpdate(body={'requests': send_req},
    presentationId=deckID).execute()

'''
@param:     left_margin
@param:     top_margin
'''
def createTextBoxMargin():
    slideNewID = gen_uuid()
    textBoxID = gen_uuid()

    send_req = [    
    {'createSlide': {
        'objectId': slideNewID,
        # predefinedLayout : enum
        # layoutId : string Layout ID: the object ID of one of the layouts in the presentation
        'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_TWO_COLUMNS'},
        'placeholderIdMappings': [{
            'objectId': textBoxID,
            'layoutPlaceholder': {'type': 'BODY', 'index': 0}
        }]
    }},

    {'insertText': {'objectId': textBoxID,      'text': 'This is a sample margin'}}
    ]
    SLIDES.presentations().batchUpdate(body={'requests': send_req},
    presentationId=deckID).execute()
    

# further_req = [
#     {'createSlide': {
#         'objectId': mpSlideID,
#         'slideLayoutReference': {'predefinedLayout': 'MAIN_POINT'},
#         'placeholderIdMappings': [{
#             'objectId': mpTextboxID,
#             'layoutPlaceholder': {'type': 'TITLE', 'index': 0}
#         }],
#     }},
#     # add title & subtitle to title slide; add text to main point slide textbox
#     {'insertText': {'objectId': mpTextboxID, 'text': 'This is title message'}}
# ]
# SLIDES.presentations().batchUpdate(body={'requests': further_req},
#         presentationId=deckID).execute()



'''
add a text box
@param:     slideID
@param:     msg
'''
# def addTextBox(slideID, msg):
#     textboxID = gen_uuid()
#     send_req = [
#         {'createSlide': {
#             'objectId': slideID,
#             'slideLayoutReference': {'predefinedLayout': 'MAIN_POINT'},
#             'placeholderIdMappings': [{
#                 'objectId': textboxID, 
#                 'layoutPlaceholder': {'type':'TITLE', 'index': 0}    
#             }]
#         }}
#     ]
#     {
#         'insertText': {'objectId': textboxID, 'text': msg}
#     }
#     SLIDES.presentations().batchUpdate(body={'requests': send_req},
#             presentationId=deckID).execute()

# a = createEmptySlide()
# addTextBox(a, "hello world")    
# a = createEmptySlide()
createSlideWithText("hello world from Victoria!")
createSlideWithText("My name is Josh!")
createSlideWithBackground('https://visme.co/blog/wp-content/uploads/2017/07/50-Beautiful-and-Minimalist-Presentation-Backgrounds-025.jpg')
createSlideWithBackground('https://i.ytimg.com/vi/Yw6u6YkTgQ4/maxresdefault.jpg')
createSlideWithBackground('https://i2.wp.com/buildingontheword.org/wp-content/uploads/2014/08/peter-walking-on-water.jpg')
createSlideTextandFont("This is fun!", "Courier New", 25)
createSlideTextandFont("This is fun!", "Times New Roman", 20)
createSlideTextandFont("This is fun!", "Georgia", 100)
createSlideTextFontBackground("This is fun", "Courier New", 25, 'https://visme.co/blog/wp-content/uploads/2017/07/50-Beautiful-and-Minimalist-Presentation-Backgrounds-025.jpg')
createTextBoxMargin()
print('DONE')

#Use python3 to run 