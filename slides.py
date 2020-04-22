from __future__ import print_function
import uuid 
import bib

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

logoSrc = 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSIrxH8cTa05cnvqh9os30fiB0qRxFRKQXNoY1C1UVwBvwmNVZd&usqp=CAU'

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
            # worship service title box
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
                        'bold' : 'true',
                        'foregroundColor' : {
                            'opaqueColor' : {
                                'rgbColor' : {
                                    'blue' : 1.0,
                                    'green' : 1.0,
                                    'red' : 1.0
                                }
                            }
                        }
                    },
                    'textRange' : {'type' : 'FIXED_RANGE', 'startIndex' : 0, 'endIndex' : 18},
                    'fields' : 'foregroundColor, fontFamily, fontSize, bold'
                }
            },
            # date box 
            {
                'createShape' : {
                    'objectId' : dateboxID,
                    'shapeType' : 'TEXT_BOX',
                    'elementProperties' : {
                        'pageObjectId' : slideNewID,
                        'size' : {
                            'width' : {'magnitude' : 3000000, 'unit' : 'EMU'},
                            'height' : {'magnitude' : 3000000, 'unit' : 'EMU'}
                        },
                        'transform' : {
                            'scaleX' : 0.6714,
                            'scaleY' : 0.1391,
                            'translateX' : 6933050,
                            'translateY' : 20600,
                            'unit' : 'EMU'
                        }
                    }
                }
            },
            {
                'insertText' : {
                    'objectId' : dateboxID,
                    'text' : date
                }
            },
            {
                'updateTextStyle' : {
                    'objectId' : dateboxID,
                    'style' : {
                        'fontFamily' : 'Montserrat',
                        'fontSize' : {'magnitude' : '14', 'unit' : 'PT'},
                        'foregroundColor' : {
                            'opaqueColor' : {
                                'rgbColor' : {
                                    'blue' : 1.0,
                                    'green' : 1.0,
                                    'red' : 1.0
                                }
                            }
                        }
                    },
                    'textRange' : {'type' : 'ALL'},
                    'fields' : 'foregroundColor, fontFamily, fontSize'
                }
            },
            # {
            #     'updateParagraphStyle' : {
            #         'objectId' : dateboxID,
            #         'alignment' : 'END'
            #     }
            # },
            # icon text box
            {
                'createShape' : {
                    'objectId' : icontextID,
                    'shapeType' : 'TEXT_BOX',
                    'elementProperties' : {
                        'pageObjectId' : slideNewID,
                        'size' : {
                            'width' : {'magnitude' : 3000000, 'unit' : 'EMU'},
                            'height' : {'magnitude' : 3000000, 'unit' : 'EMU'}
                        },
                        'transform' : {
                            'scaleX' : 0.4051,
                            'scaleY' : 0.2809,
                            'translateX' : 7731875,
                            'translateY' : 4204725,
                            'unit' : 'EMU'
                        }
                    }
                }
            }, 
            {
                'insertText' : {
                    'objectId' : icontextID,
                    'text' : 'University \nBible \nFellowship'
                }
            },
            {
                'updateTextStyle' : {
                    'objectId' : icontextID,
                    'style' : {
                        'fontFamily' : 'Montserrat',
                        'fontSize' : {'magnitude' : '14', 'unit' : 'PT'},
                        'foregroundColor' : {
                            'opaqueColor' : {
                                'rgbColor' : {
                                    'blue' : 1.0,
                                    'green' : 1.0,
                                    'red' : 1.0
                                }
                            }
                        }
                    },
                    'textRange' : {'type' : 'ALL'},
                    'fields' : 'foregroundColor, fontFamily, fontSize'
                }
            }, 
            {
                'updatePageProperties': {
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
            },
            # icon box
            {
                'createImage' : {
                    'objectId' : iconboxID,
                    'url' : logoSrc,
                    'elementProperties' : {
                        'pageObjectId' : slideNewID,
                        'size' : {
                            'width' : {'magnitude' : 3000000, 'unit' : 'EMU'},
                            'height' : {'magnitude' : 3000000, 'unit' : 'EMU'}
                        },
                        'transform' : {
                            'scaleX' : 0.3628,
                            'scaleY' : 0.2801,
                            'translateX' : 6643400,
                            'translateY' : 4187350,
                            'unit' : 'EMU'
                        }
                    }
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
        

