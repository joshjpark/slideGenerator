from __future__ import print_function
import uuid 
import bib

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

def gen_uuid() : return str(uuid.uuid4())

class Slides:  
    
    def __init__(self):
        SCOPES = 'https://www.googleapis.com/auth/presentations', 
        store = file.Storage('storage.json')
        creds = store.get()

        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)

        self.SLIDES = discovery.build('slides', 'v1', http = creds.authorize(Http()))

        print('** Init new slide deck & obtain object IDs')
        rsp = self.SLIDES.presentations().create(body={'title' : 'title'}).execute()
        self.deckID = rsp['presentationId'] # uuid of presentation
        titleSlide = rsp['slides'][0]

        titleID = titleSlide['pageElements'][0]['objectId']
        subtitleID = titleSlide['pageElements'][1]['objectId']

        # clear init page
        send_req = [
            {'deleteObject' : {
                'objectId' : titleID
            }},
            {'deleteObject' : {
                'objectId' : subtitleID
            }}
        ]

        self.SLIDES.presentations().batchUpdate(body={'requests': send_req}, presentationId=self.deckID).execute()
    
    def createTitle(self, date, background):
        slideNewID = gen_uuid()
        dateboxID = gen_uuid()
        titleboxID = gen_uuid()
        iconboxID, icontextID = gen_uuid(), gen_uuid()

        send_req = [
            {
                'createSlide' : {'objectId' : slideNewID}
            }, 
            {
                'createShape' : {
                    'objectId' : titleboxID,
                    'shapeType' : 'TEXT_BOX',
                    'elementProperties' : {
                        'pageObjectId' : slideNewID,
                        'size' : {
                            'width' : {'magnitude' : 3000000, 'unit' : 'EMU'},
                            'height' : {'magnitude' : 3000000, 'unit' : 'EMU'}
                        },
                        'transform' : {
                            'scaleX' : 1.852,
                            'scaleY' : 0.5697,
                            'translateX' : 1794000,
                            'translateY' : 1717200,
                            'unit' : 'EMU'
                        }
                    }
                }
            },
            {
                'insertText' : {
                    'objectId' : titleboxID,
                    'text' : "WORSHIP \n SERVICE"
                }
            },
            {
                'updateTextStyle' : {
                    'objectId' : titleboxID,
                    'style' : {
                        'fontFamily' : 'Montserrat',
                        'fontSize' : {'magnitude' : '80', 'unit' : 'PT'},
                        'bold' : 'true'
                    },
                    'textRange' : {'type' : 'FIXED_RANGE', 'startIndex' : 0, 'endIndex' : 18},
                    'fields' : 'fontFamily, fontSize, bold'
                }
            }
        ]

        self.SLIDES.presentations().batchUpdate(body={'requests': send_req}, presentationId=self.deckID).execute()
    
    def createHymn(self, hymn, title, author, year, background, lyric):
        pass

    def createTransition(self, text, font, size, background):
        slideNewID = gen_uuid()
        textboxID = gen_uuid()

        send_req = [
            {
                'createSlide' : {'objectId' : slideNewID}
            },
            {
                'createShape' : {
                    'objectId' : textboxID,
                    'shapeType' : 'TEXT_BOX',
                    'elementProperties': {
                        'pageObjectId' : slideNewID,
                        'size' : {
                            'width' : {'magnitude' : 3000000, 'unit' : 'EMU'},
                            'height' : {'magnitude' : 3000000, 'unit' : 'EMU'}
                        },
                        'transform': {
                            'scaleX' : 2.7492,
                            'scaleY' : 1.5576,
                            'translateX' : 448200,
                            'translateY' : 235350,
                            'unit' : 'EMU'
                        }
                    }
                }
            },
            {
                'insertText' : {'objectId' : textboxID, 'text' : text}
            },
            {
                'updateTextStyle' : {
                    'objectId' : textboxID,
                    'style' : {
                        'fontFamily' : font,
                        'fontSize' : {'magnitude' : size, 'unit' : 'PT'}
                    },
                    'textRange' : {'type' : 'FIXED_RANGE', 'startIndex' : 0, 'endIndex' : len(text)},
                    'fields' : 'fontFamily, fontSize'
                }
            },
            {
                'updatePageProperties' : {
                    'objectId' : slideNewID,
                    'pageProperties' : {
                        'pageBackgroundFill' : {
                            'stretchedPictureFill' : {
                                'contentUrl' : background
                            }
                        }
                    },
                    'fields' : 'pageBackgroundFill'
                }
            }
        ]
        self.SLIDES.presentations().batchUpdate(body={'requests' : send_req}, presentationId=self.deckID).execute()

    def createApostleCreed(self, background):
        pass
    
    def createLordsPrayer(self, background):
        pass

    def createVerses(self, keyVerse, background):
        pass
        

