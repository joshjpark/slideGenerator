'''
slideGenerator.py
Description: Automate the task of generating routine slides using Google Slides API. 
'''

# from __future__ import print_function
# import uuid
# import bib

# from apiclient import discovery
# from httplib2 import Http
# from oauth2client import file, client, tools

# generate random, unique UUID string


def gen_uuid(): return str(uuid.uuid4())


# obtain read / write authorization
SCOPES = 'https://www.googleapis.com/auth/presentations',
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
# create service end point for the slides API
SLIDES = discovery.build('slides', 'v1', http=creds.authorize(Http()))

# create slide start point
print('** Create new slide deck & set up object IDs')
rsp = SLIDES.presentations().create(
    body={'title': 'DEMO SLIDES'}).execute()
deckID = rsp['presentationId']      # presentationID from https (url) address
titleSlide = rsp['slides'][0]
# titleID = titleSlide['pageElements'][0]['objectId']
# subtitleID = titleSlide['pageElements'][1]['objectId']


def createGoodSlideTextFontBackground(phrase, font, size, url):
    """create textbox for hymnal with background url
    Kwargs:
    phrase      -- phrase to put in the textbox   
    font        -- text font
    size        -- size of text
    url         -- background image url
    """
    slideNewID = gen_uuid()
    textBoxID = gen_uuid()
    

    send_req = [
        {'createSlide': {
            'objectId': slideNewID
        }},
        {
            'createShape': {
                'objectId': textBoxID,
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slideNewID,
                    'size': {
                        'width': {'magnitude': 3000000, 'unit': 'EMU'},
                        'height': {'magnitude': 3000000, 'unit': 'EMU'}
                    },
                    'transform': {
                        'scaleX': 2.7492,
                        'scaleY': 1.5576,
                        'translateX': 448200,
                        'translateY': 235350,
                        'unit': 'EMU'
                    }
                }
            }
        },
        {
            'insertText': {'objectId': textBoxID, 'text': phrase}
        },
        {
            'updateTextStyle': {
                'objectId': textBoxID,
                'style': {
                    'fontFamily': font,
                    'fontSize': {'magnitude': size, 'unit': 'PT'}
                },
                'textRange': {'type': 'FIXED_RANGE', 'startIndex': 0, 'endIndex': len(phrase)},
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


def createWorshipSlideTextBox(phrase, font, size):
    """create slide with textbox of appropriate size
    Kwargs:
    phrase        -- phrase to put in the textbox
    font          -- text font
    size          -- size of text 
    """
    slideNewID = gen_uuid()
    textBoxID = gen_uuid()

    send_req = [
        {'createSlide': {
            'objectId': slideNewID
        }},
        {
            'createShape': {
                'objectId': textBoxID,
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slideNewID,
                    'size': {
                        'width': {'magnitude': 3000000, 'unit': 'EMU'},
                        'height': {'magnitude': 3000000, 'unit': 'EMU'}
                    },
                    'transform': {
                        'scaleX': 2.8402,
                        'scaleY': 1.1388,
                        'translateX': 311700,
                        'translateY': 745150,
                        'unit': 'EMU'
                    }
                }
            }
        },
        {
            'insertText': {
                'objectId': textBoxID,
                'insertionIndex': 0,
                'text': phrase
            }
        },
        {
            'updateTextStyle': {
                'objectId': textBoxID,
                'style': {
                    'fontFamily': font,
                    'fontSize': {'magnitude': size, 'unit': 'PT'}
                },
                'textRange': {'type': 'FIXED_RANGE', 'startIndex': 0, 'endIndex': len(phrase)},
                'fields': 'fontFamily, fontSize',
            }
        },
        {
            'updateParagraphStyle': {
                'objectId': textBoxID,
                'style': {'lineSpacing': 150},
                'fields': 'lineSpacing'
            }
        }
    ]
    SLIDES.presentations().batchUpdate(body={'requests': send_req},
                                       presentationId=deckID).execute()


def createWorshipServiceSlides(book, fromChapter, fromVerse, toChapter, toVerse, font, size):
    """create multiple slides of Bible verses.
    Kwargs: 
    book        -- the book in the Bible to fetch
    font        -- font of text in textbox
    size        -- font size of text in textbox
    """
    verses = bib.get_verses(book, fromChapter, fromVerse, toChapter, toVerse)
    temp = []

    for i in range(0, len(verses)):
        if i % 2 == 0:
            temp.append(verses[i])
            if i == len(verses)-1:
                createWorshipSlideTextBox(temp[0], font, size)
        elif i % 2 == 1:
            temp.append(verses[i])
            createWorshipSlideTextBox(temp[0] + '\n' + temp[1], font, size)
            temp = []


# createWorshipServiceSlides('John', '12', '12', '12', '19', 'Average', '28')

createGoodSlideTextFontBackground('Hello world', 'Average', '28',
                                  'https://images.unsplash.com/photo-1530688957198-8570b1819eeb?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&w=1000&q=80')


createWorshipServiceSlides('Joshua', '1', '6', '2', '13', 'Average', '20')
print('DONE')
