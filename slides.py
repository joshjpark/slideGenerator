from __future__ import print_function
import uuid 
import bib

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

logoSrc = 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSIrxH8cTa05cnvqh9os30fiB0qRxFRKQXNoY1C1UVwBvwmNVZd&usqp=CAU'
creed = ['Apostles\' Creed','I believe in God the Father Almighty, \nMaker of heaven and earth, and in Jesus Christ, \nHis only Son our Lord, who was conceived by the Holy Spirit,\nSuffered under Pontius Pilate, was crucified, dead and buried; \nHe descended into hell; \nThe third day He rose again from the dead;', 'He ascended into heaven, \nand sitteth on the right hand of god the Father Almighty;\nFrom thence He shall come to judge the quick and the dead.\nI believe in the holy spirit, the holy universal church, the communion of saints, the forgiveness of sins, the resurrection of the body. \nAnd the life everlasting. Amen']
prayer = ['Lord\'s Prayer','Our Father in heaven,\nHallowed be your name,\nYour kingdom come,\nYour will be done on earth as it is in heaven.\nGive us today our daily bread.\nForgive us our debts, as we also have forgiven our debtors.\n','And lead us not into temptation,\nBut deliver us from the evil one.\nFor yours is the kingdom, and the power,\nand the glory, forever, Amen.']

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
            # icon text
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

        self.SLIDES.presentations().batchUpdate(body={'requests' : send_req}, presentationId=self.deckID).execute()
    
    def createHymn(self, hymn, title, author, year, background, lyric):
        pass

    def createTransition(self, text, background):
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
                            'scaleX' : 2.664,
                            'scaleY' : 0.2755,
                            'translateX' : 576000,
                            'translateY' : 3847950,
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
                        'fontFamily' : 'Montserrat',
                        'fontSize' : {'magnitude' : 40, 'unit' : 'PT'},
                        'bold' : 'true',
                        'foregroundColor' : {
                            'opaqueColor' : {
                                'rgbColor' : {
                                    'blue' : 1.0,
                                    'green' : 1.0,
                                    'red' : 1.0
                                }
                            }
                        },
                    },
                    'textRange' : {'type' : 'FIXED_RANGE', 'startIndex' : 0, 'endIndex' : len(text)},
                    'fields' : 'foregroundColor, bold, fontFamily, fontSize'
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

    def createRecital(self, recital, background):
        
        if recital == "Prayer": 
            recitalVersion = prayer
        else:
            recitalVersion = creed

        def helper(recite, i): 
            
            slideNewID = gen_uuid()
            headerID, contentID = gen_uuid(), gen_uuid()
            
            send_req = [
                {
                    'createSlide' : {'objectId' : slideNewID}
                },
                {
                    'createShape' : {
                        'objectId' : headerID,
                        'shapeType' : 'TEXT_BOX',
                        'elementProperties': {
                            'pageObjectId' : slideNewID,
                            'size' : {
                                'width' : {'magnitude' : 3000000, 'unit' : 'EMU'},
                                'height' : {'magnitude' : 3000000, 'unit' : 'EMU'}
                            },
                            'transform': {
                                'scaleX' : 2.8402,
                                'scaleY' : 0.1909,
                                'translateX' : 311700,
                                'translateY' : 63475,
                                'unit' : 'EMU'
                            }
                        }
                    }
                },
                {
                    'insertText' : {'objectId' : headerID, 'text' : recite[0]}
                },
                {
                    'updateTextStyle' : {
                        'objectId' : headerID,
                        'style' : {
                            'fontFamily' : 'Montserrat',
                            'fontSize' : {'magnitude' : 36, 'unit' : 'PT'},
                            'bold' : 'true',
                            'foregroundColor' : {
                                'opaqueColor' : {
                                    'rgbColor' : {
                                        'blue' : 1.0,
                                        'green' : 1.0,
                                        'red' : 1.0
                                    }
                                }
                            },
                        },
                        'textRange' : {'type' : 'FIXED_RANGE', 'startIndex' : 0, 'endIndex' : len(recite[0])},
                        'fields' : 'foregroundColor, bold, fontFamily, fontSize'
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
                },
                {
                    'createShape' : {
                        'objectId' : contentID,
                        'shapeType' : 'TEXT_BOX',
                        'elementProperties': {
                            'pageObjectId' : slideNewID,
                            'size' : {
                                'width' : {'magnitude' : 3000000, 'unit' : 'EMU'},
                                'height' : {'magnitude' : 3000000, 'unit' : 'EMU'}
                            },
                            'transform': {
                                'scaleX' : 3.048,
                                'scaleY' : 1.4361,
                                'translateY' : 835075,
                                'unit' : 'EMU'
                            }
                        }
                    }
                },
                {
                    'insertText' : {'objectId' : contentID, 'text' : recite[i]}
                }, 
                {
                    'updateTextStyle' : {
                        'objectId' : contentID,
                        'style' : {
                            'fontFamily' : 'Arial',
                            'fontSize' : {'magnitude' : 24, 'unit' : 'PT'},
                            'foregroundColor' : {
                                'opaqueColor' : {
                                    'rgbColor' : {
                                        'blue' : 1.0,
                                        'green' : 1.0,
                                        'red' : 1.0
                                    }
                                }
                            },
                        },
                        'textRange' : {'type' : 'FIXED_RANGE', 'startIndex' : 0, 'endIndex' : len(recite[i])},
                        'fields' : 'foregroundColor, fontFamily, fontSize'
                    }
                }
            ]
            self.SLIDES.presentations().batchUpdate(body={'requests' : send_req}, presentationId=self.deckID).execute()
        
        helper(recitalVersion, 1)
        helper(recitalVersion, 2)

    def createVerses(self, book, fromChapter, fromVerse, toChapter, toVerse): #keyVerse, background):
        
        def helper(phrase):

            slideNewID = gen_uuid()
            textboxID = gen_uuid()

            send_req = [
                {'createSlide' : {
                    'objectId' : slideNewID
                }},
                {
                    'createShape' : {
                        'objectId' : textboxID,
                        'shapeType' : 'TEXT_BOX',
                        'elementProperties' : {
                            'pageObjectId' : slideNewID,
                            'size' : {
                                'width' : {'magnitude' : 3000000, 'unit' : 'EMU'},
                                'height' : {'magnitude' : 3000000, 'unit' : 'EMU'}
                            },
                            'transform' : {
                                'scaleX' : 2.8402,
                                'scaleY' : 1.7145,
                                'translateX' : 311700,
                                'unit' : 'EMU'
                            }
                        }
                    }
                },
                {
                    'insertText' : {
                        'objectId' : textboxID,
                        'insertionIndex' : 0,
                        'text' : phrase
                    }
                },
                {
                    'updateTextStyle' : {
                        'objectId' : textboxID,
                        'style' : {
                            'fontFamily' : 'Average',
                            'fontSize' : {'magnitude' : '28', 'unit' : 'PT'}
                        },
                        'textRange' : {'type': 'FIXED_RANGE', 'startIndex' : 0, 'endIndex': len(phrase)},
                        'fields' : 'fontFamily, fontSize',
                    }
                },
                {
                    'updateParagraphStyle' : {
                        'objectId' : textboxID,
                        'style' : {'lineSpacing': 150},
                        'fields' : 'lineSpacing'
                    }
                }
            ]
            self.SLIDES.presentations().batchUpdate(body={'requests': send_req},
                                            presentationId=self.deckID).execute()
        
        verses = bib.getVerses(book, fromChapter, fromVerse, toChapter, toVerse)
        result = []

        for i in range(len(verses)):
            if i % 2 == 0:
                result.append(verses[i])
                if i == len(verses) - 1:
                    helper(result[0])
            elif i % 2 == 1:
                result.append(verses[i])
                helper(result[0] + '\n' + result[1])
                result = []

