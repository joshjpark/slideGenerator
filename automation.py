from __future__ import print_function
import uuid
import bib
import re

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

# Title page(Date, Background)

# Hymn (hymnNum, Title, Composer, Year)

# Silent Prayer (Background)

# Apostles' creed (Background)

# Representative Prayer (Person, Background)

# Today’s verses (chapter, keyVerse)

# CreateMessageTitlePage(chapter, fromChapter, toChapter, fromVerse, toVerse, keyVerse) 

# Offering()

# Announcement (announcer)

# The Lord’s prayer (Background) 

def gen_uuid(): return str(uuid.uuid4())

# get url for direct link to image from Google drive
def extractUrl(image_url):
    address = image_url.split('/d/')[1].split('/view')[0]
    return 'https://drive.google.com/uc?id=' + address
    
class Slides:
    def __init__(self, slide_name):
        SCOPES = 'https://www.googleapis.com/auth/presentations'
        store = file.Storage('storage.json')
        creds = store.get()

        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        
        self.SLIDES = discovery.build('slides', 'v1', http=creds.authorize(Http()))

        #create empty batch
        print(' ** Create new slide deck & set up object IDs ** ')
        rsp = self.SLIDES.presentations().create(body={'title' : slide_name}).execute()

        # presentationID from https (url) address
        self.deckID = rsp['presentationId']

    def createTitlePage(self, phrase, font, size, background_url):
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
                'insertText': {'objectId': textBoxID, 'text': phrase}
            },
            {
                'updateTextStyle': {
                    'objectId': textBoxID,
                    'style': {
                        'fontFamily': font,
                        'fontSize': {'magnitude': size, 'unit': 'PT'}
                    },
                    'textRange': {'type': 'FIXED_RANGE', 'startIndex':0, 'endIndex': len(phrase)},
                    'fields': 'fontFamily, fontSize',
                }
            },
            {
                'updatePageProperties': {
                    'objectId': slideNewID,
                    'pageProperties': {
                        'pageBackgroundFill': {
                            'stretchedPictureFill': {
                                'contentUrl': background_url
                            }
                        }
                    },
                    'fields': 'pageBackgroundFill'
                }
            }
        ]
        self.SLIDES.presentations().batchUpdate(body={'requests':send_req},
                                        presentationId=self.deckID).execute()
        
# slide = Slides("hello")
# slide.createTitlePage('Hello World', 'Average', '28', 'https://images.unsplash.com/photo-1530688957198-8570b1819eeb?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&w=1000&q=80')

