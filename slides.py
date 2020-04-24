from __future__ import print_function
import uuid 
import bib
import json

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

ubfLogoImg = 'https://i.ibb.co/HHczGzr/ubf-white-logo.png'
creed = ['Apostles\' Creed','I believe in God the Father Almighty, \nMaker of heaven and earth, and in Jesus Christ, \nHis only Son our Lord, who was conceived by the Holy Spirit, born of the Virgin Mary,\nSuffered under Pontius Pilate, was crucified, dead, and buried; \nHe descended into hell; \nThe third day He rose again from the dead;', 'He ascended into heaven, \nand sitteth on the right hand of god the Father Almighty;\nFrom thence He shall come to judge the quick and the dead.\nI believe in the holy spirit, the holy universal church, the communion of saints, the forgiveness of sins, the resurrection of the body. \nAnd the life everlasting. Amen']
prayer = ['Lord\'s Prayer','Our Father in heaven,\nHallowed be your name,\nYour kingdom come,\nYour will be done on earth as it is in heaven.\nGive us today our daily bread.\nForgive us our debts, as we also have forgiven our debtors.\n','And lead us not into temptation,\nBut deliver us from the evil one.\nFor yours is the kingdom, and the power,\nand the glory, forever, Amen.']

def gen_uuid() : return str(uuid.uuid4())

class Slides:  

    def __init__(self):
        SCOPES = 'https://www.googleapis.com/auth/presentations', 
        store = file.Storage('storage.json')
        creds = store.get()
        self.send_req = []

        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)

        self.SLIDES = discovery.build('slides', 'v1', http = creds.authorize(Http()))

        print('** Init new slide deck & obtain object IDs')
        rsp = self.SLIDES.presentations().create(body={'title' : 'title'}).execute()
        self.deckID = rsp['presentationId'] # uuid of presentation
        titleSlide = rsp['slides'][0]
        
        # clear init page
        self.send_req.append({'deleteObject' : {'objectId' : titleSlide['objectId']}})
            
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
            {
                'updateParagraphStyle' : {
                    'objectId' : titleboxID,
                    'style' : {'lineSpacing' : 90},
                    'fields' : 'lineSpacing'
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
            {
                'updateParagraphStyle' : {
                    'objectId' : dateboxID,
                    'style' : {'alignment' : 'END'},
                    'fields' : 'alignment'
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
                    'url' : ubfLogoImg,
                    'elementProperties' : {
                        'pageObjectId' : slideNewID,
                        'size' : {
                            'width' : {'magnitude' : 3000000, 'unit' : 'EMU'},
                            'height' : {'magnitude' : 3000000, 'unit' : 'EMU'}
                        },
                        'transform' : {
                            'scaleX' : 0.3028,
                            'scaleY' : 0.2801,
                            'translateX' : 6843400, # 6643400
                            'translateY' : 4187350,
                            'unit' : 'EMU'
                        }
                    }
                }
            }
        ]
        print('** title page created')
        self.send_req.append(send_req)
        # self.SLIDES.presentations().batchUpdate(body={'requests' : send_req}, presentationId=self.deckID).execute()
    
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
        print('** {} slide created'.format(text))
        self.send_req.append(send_req)

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
                            },
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
                    'updateParagraphStyle' : {
                        'objectId' : headerID,
                        'style' : {'alignment' : 'CENTER'},
                        'fields' : 'alignment'
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
                },
                {
                    'updateParagraphStyle': {
                        'objectId' : contentID,
                        'style' : {
                            'lineSpacing' : 150,
                            'alignment' : 'CENTER', 
                            },
                        'fields' : 'alignment , lineSpacing'
                    }
                }
            ]
            self.send_req.append(send_req)
        
        helper(recitalVersion, 1)
        helper(recitalVersion, 2)
        print("** {} slide created".format(recital))

    def createVerses(self, book, fromChapter, fromVerse, toChapter, toVerse, keyChapter, keyVerse, messageTitle, primaryBackground, secondaryBackground): #keyVerse, background):
        
        toFromHeader = (book + " " + fromChapter + ":" + fromVerse + "-" + toVerse + "\nKey verse " + keyChapter + ":" + keyVerse) if (fromChapter == toChapter) else (book + " " + fromChapter + ":" + fromVerse + "-" + toChapter + ":" + toVerse + "\nKey verse: " + keyChapter + ":" + keyVerse)

        # layout for verses
        def layoutHelper(phrase):

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
                            'fontSize' : {'magnitude' : '24', 'unit' : 'PT'}
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
                },
                # vertical center
                {
                    'updateShapeProperties' : {
                        'objectId' : textboxID,
                        'shapeProperties' : {
                            'contentAlignment' : 'MIDDLE'
                        },
                        'fields' : 'contentAlignment'
                    }
                }
            ]
            self.send_req.append(send_req)

        # main title layout 
        def layoutHelperTitle(book, fromChapter, fromVerse, toChapter, toVerse, toFromHeader, primaryBackground):
            
            slideNewID = gen_uuid()
            textboxID = gen_uuid()
            subtextboxID = gen_uuid()
                                
            send_req = [
                {'createSlide' : {
                    'objectId' : slideNewID
                }},
                # primary header box
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
                                'scaleX' : 3.048,
                                'scaleY' : 0.2755,
                                'translateX' : -50,
                                'translateY' : 1177225,
                                'unit' : 'EMU'
                            }
                        }
                    }
                },
                {
                    'insertText' : {
                        'objectId' : textboxID,
                        'insertionIndex' : 0,
                        'text' : 'Today\'s Verses'
                    }
                },
                {
                    'updateTextStyle' : {
                        'objectId' : textboxID,
                        'style' : {
                            'fontFamily' : 'Monstserrat',
                            'fontSize' : {'magnitude' : '40', 'unit' : 'PT'},
                            'foregroundColor' : {
                                'opaqueColor' : {
                                    'rgbColor' : {
                                        'blue' : 1.0,
                                        'green' : 1.0,
                                        'red' : 1.0
                                    }
                                }
                            },
                            'bold' : 'true'
                        },
                        'textRange' : {'type' : 'FIXED_RANGE', 'startIndex' : 0, 'endIndex' : len('Today\'s Verses')},
                        'fields' : 'foregroundColor, bold, fontFamily, fontSize'
                    }
                },
                {
                  'updateParagraphStyle' : {
                      'objectId' : textboxID, 
                      'style' : {'alignment' : 'CENTER'},
                      'fields' : 'alignment'
                  }  
                },
                # primary subtext box 
                {
                    'createShape' : {
                        'objectId' : subtextboxID,
                        'shapeType' : 'TEXT_BOX',
                        'elementProperties' : {
                            'pageObjectId' : slideNewID,
                            'size' : {
                                'width' : {'magnitude' : 3000000, 'unit' : 'EMU'},
                                'height' : {'magnitude' : 3000000, 'unit' : 'EMU'}
                            },
                            'transform' : {
                                'scaleX' : 1.7832,
                                'scaleY' : 0.3393,
                                'translateX' : 1897150,
                                'translateY' : 2062800,
                                'unit' : 'EMU'
                            }
                        }
                    }
                },
                {
                    'insertText' : {
                        'objectId' : subtextboxID,
                        'insertionIndex' : 0,
                        'text' : toFromHeader
                    }
                },
                {
                    'updateTextStyle' : {
                        'objectId' : subtextboxID,
                        'style' : {
                            'fontFamily' : 'Arial',
                            'fontSize' : {'magnitude' : '20', 'unit' : 'PT'},
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
                        'textRange' : {'type' : 'FIXED_RANGE', 'startIndex' : 0, 'endIndex' : len(toFromHeader)},
                        'fields' : 'foregroundColor, fontFamily, fontSize'
                    }
                }, 
                {
                    'updateParagraphStyle' : {
                        'objectId' : subtextboxID,
                        'style' : {'alignment' : 'CENTER'},
                        'fields' : 'alignment'
                    }
                },
                {
                    'updatePageProperties' : {
                        'objectId' : slideNewID,
                        'pageProperties' : {
                            'pageBackgroundFill' : {
                                'stretchedPictureFill' : {
                                    'contentUrl' : primaryBackground
                                }
                            }
                        },
                        'fields' : 'pageBackgroundFill'
                    }
                }
            ]
            # add background page and turn them into white characters
            self.send_req.append(send_req)
        
        # sub title layout
        def layoutHelperSubTitle(book, fromChapter, fromVerse, toChapter, toVerse, keyVerseText, tofromHeader, secondaryBackground):
            slideNewID = gen_uuid()
            subtitleID, rangeVerseID, verseKeyID = gen_uuid(), gen_uuid(), gen_uuid()

            send_req = [
                {
                    'createSlide' : {
                        'objectId' : slideNewID
                    }
                },
                # secondary header box
                {
                    'createShape' : {
                        'objectId' : subtitleID,
                        'shapeType' : 'TEXT_BOX',
                        'elementProperties' : {
                            'pageObjectId' : slideNewID,
                            'size' : {
                                'width' : {'magnitude' : 3000000, 'unit' : 'EMU'},
                                'height' : {'magnitude' : 3000000, 'unit' : 'EMU'}
                            },
                            'transform' : {
                                'scaleX' : 3.048,
                                'scaleY' : 0.2755,
                                'translateX' : -50,
                                'translateY' : 208275,
                                'unit' : 'EMU'
                            }
                        }
                    }
                },
                {
                    'insertText' : {
                        'objectId' : subtitleID, 
                        'insertionIndex' : 0,
                        'text' : messageTitle,
                    }
                },
                {
                    'updateTextStyle' : {
                        'objectId' : subtitleID,
                        'style' : {
                            'fontFamily' : 'Monstserrat',
                            'fontSize' : {'magnitude' : '40', 'unit' : 'PT'},
                            'foregroundColor' : {
                                'opaqueColor' : {
                                    'rgbColor' : {
                                        'blue' : 1.0,
                                        'green' : 1.0,
                                        'red' : 1.0
                                    }
                                }
                            },
                            'bold' : 'true'
                        },
                        'textRange' : {'type' : 'ALL'},
                        'fields' : 'foregroundColor, bold, fontFamily, fontSize'
                    }
                },
                {
                    'updateParagraphStyle' : {
                        'objectId' : subtitleID,
                        'style' : {'alignment' : 'CENTER'},
                        'fields' : 'alignment'
                    }
                },
                # range of verses header
                {
                    'createShape' : {
                        'objectId' : rangeVerseID,
                        'shapeType' : 'TEXT_BOX',
                        'elementProperties' : {
                            'pageObjectId' : slideNewID,
                            'size' : {
                                'width' : {'magnitude' : 3000000, 'unit' : 'EMU'},
                                'height' : {'magnitude' : 3000000, 'unit' : 'EMU'}
                            },
                            'transform' : {
                                'scaleX' : 1.2187,
                                'scaleY' : 0.3393,
                                'translateX' : 618775,
                                'translateY' : 1034775,
                                'unit' : 'EMU'
                            }
                        }
                    }
                },
                {
                    'insertText' : {
                        'objectId' : rangeVerseID,
                        'insertionIndex' : 0,
                        'text' : toFromHeader
                    }
                },
                {
                    'updateTextStyle' : {
                        'objectId' : rangeVerseID,
                        'style' : {
                            'fontFamily' : 'Arial',
                            'fontSize' : {'magnitude' : '20', 'unit' : 'PT'},
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
                        'textRange' : {'type' : 'FIXED_RANGE', 'startIndex' : 0, 'endIndex' : len(toFromHeader)},
                        'fields' : 'foregroundColor, fontFamily, fontSize'
                    }
                },
                # key verse box
                {
                    'createShape' : {
                        'objectId' : verseKeyID,
                        'shapeType' : 'TEXT_BOX',
                        'elementProperties' : {
                            'pageObjectId' : slideNewID,
                            'size' : {
                                'width' : {'magnitude' : 3000000, 'unit' : 'EMU'},
                                'height' : {'magnitude' : 3000000, 'unit' : 'EMU'}
                            },
                            'transform' : {
                                'scaleX' : 2.5867,
                                'scaleY' : 0.3393,
                                'translateX' : 691900,
                                'translateY' : 3620350,
                                'unit' : 'EMU'
                            }
                        }
                    }
                },
                {
                    'insertText' : {
                        'objectId' : verseKeyID,
                        'insertionIndex' : 0,
                        'text' : keyVerseText,
                    }
                },
                {
                    'updateTextStyle' : {
                        'objectId' : verseKeyID,
                        'style' : {
                            'fontFamily' : 'Arial',
                            'fontSize' : {'magnitude' : '20', 'unit' : 'PT'},
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
                        'textRange' : {'type' : 'ALL'},
                        'fields' : 'foregroundColor, fontFamily, fontSize'
                    }
                },
                {
                    'updateParagraphStyle' : {
                        'objectId' : verseKeyID,
                        'style' : {'alignment' : 'CENTER'},
                        'fields' : 'alignment'
                    }
                },
                {
                    'updatePageProperties' : {
                        'objectId' : slideNewID,
                        'pageProperties' : {
                            'pageBackgroundFill' : {
                                'stretchedPictureFill' : {
                                    'contentUrl' : secondaryBackground
                                }
                            }
                        },
                        'fields' : 'pageBackgroundFill'
                    }
                }
            ]
            self.send_req.append(send_req)

        # logic for verses print
        def versesGenerator():
            verses = bib.getVerses(book, fromChapter, fromVerse, toChapter, toVerse)
            result = []

            for i in range(len(verses)):
                if i % 2 == 0:
                    result.append(verses[i])
                    if i == len(verses) - 1:
                        layoutHelper(result[0])
                elif i % 2 == 1:
                    result.append(verses[i])
                    layoutHelper(result[0] + '\n' + result[1])
                    result = []
        
        # logic for finding verse
        def verseFinder(book, chapter, verse):
            with open('bible.json') as jsonFile:
                return json.load(jsonFile)[book][keyChapter][keyVerse].strip('\'\"')

        layoutHelperTitle(book, fromChapter, fromVerse, toChapter, toVerse, toFromHeader, primaryBackground)
        versesGenerator()
        layoutHelperSubTitle(book, fromChapter, fromVerse, toChapter, toVerse, verseFinder(book, keyChapter, keyVerse), toFromHeader, secondaryBackground)
        versesGenerator()
        print('** Verses slides from {} {}:{}-{}:{} created'.format(book, fromChapter, fromVerse, toChapter, toVerse))

    def createHymn(self, number, title, background):

        def hymnMainPageGenerator(json, background):
            number, title, author, year = json['hymnNumber'], json['title'], json['author'], json['year']
            
            slideNewID = gen_uuid()
            mainTextboxID = gen_uuid()
            subTextboxID = gen_uuid()

            send_req = [
                {
                    'createSlide' : {'objectId' : slideNewID}
                },
                {
                    'createShape' : {
                        'objectId' : mainTextboxID,
                        'shapeType' : 'TEXT_BOX',
                        'elementProperties' : {
                            'pageObjectId' : slideNewID,
                            'size' : {
                                'width' : {'magnitude' : 3000000, 'unit' : 'EMU'},
                                'height' : {'magnitude' : 3000000, 'unit' : 'EMU'}
                            },
                            'transform' : {
                                'scaleX' : 2.664,
                                'scaleY' : 0.2755,
                                'translateX' : 576000,
                                'translateY' : 3619350,
                                'unit' : 'EMU' 
                            }
                        }
                    }
                },
                {
                    'insertText' : {'objectId' : mainTextboxID, 'text' : str(number) + " " + title}
                },
                {
                    'updateTextStyle' : {
                        'objectId' : mainTextboxID,
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
                            }
                        },
                        'textRange' : {'type' : 'ALL'},
                        'fields' : 'foregroundColor, bold, fontFamily, fontSize'
                    }
                },
                {
                    'createShape' : {
                        'objectId' : subTextboxID,
                        'shapeType' : 'TEXT_BOX',
                        'elementProperties': {
                            'pageObjectId' : slideNewID,
                            'size' : {
                                'width' : {'magnitude' : 3000000, 'unit' : 'EMU'},
                                'height' : {'magnitude' : 3000000, 'unit' : 'EMU'}
                            },
                            'transform': {
                                'scaleX' : 1.5326,
                                'scaleY' : 0.1792,
                                'translateX' : 576000,
                                'translateY' : 4233150,
                                'unit' : 'EMU'
                            }
                        }
                    }
                },
                {
                    'insertText' : {'objectId' : subTextboxID, 'text' : author + ", " + str(year)}
                },
                {
                    'updateTextStyle' : {
                        'objectId' : subTextboxID,
                        'style' : {
                            'fontFamily' : 'Montserrat',
                            'fontSize' : {'magnitude' : 20, 'unit' : 'PT'},
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
            self.send_req.append(send_req)

        def hymnGenerator(hymn):
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
                        'elementProperties' : {
                            'pageObjectId' : slideNewID,
                            'size' : {
                                'width' : {'magnitude' : 3000000, 'unit' : 'EMU'},
                                'height' : {'magnitude' : 3000000, 'unit' : 'EMU'}
                            },
                            'transform' : {
                                'scaleX' : 3.048,
                                'scaleY' : 1.7063,
                                'translateX' : -15900,
                                'translateY' : 24600,
                                'unit' : 'EMU' 
                            }
                        }
                    }
                },
                {
                    'insertText' : {'objectId' : textboxID, 'text' : hymn}
                },
                {
                    'updateTextStyle' : {
                        'objectId' : textboxID,
                        'style' : {
                            'fontFamily' : 'Arial',
                            'fontSize' : {'magnitude' : 28, 'unit' : 'PT'},
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
                        'textRange' : {'type' : "ALL"},
                        'fields' : 'foregroundColor, fontFamily, fontSize'
                    }
                },
                {
                    'updateParagraphStyle' : {
                        'objectId' : textboxID,
                        'style' : {'alignment' : 'CENTER'},
                        'fields' : 'alignment'
                    }
                },
                {
            
                    'updateShapeProperties' : {
                        'objectId' : textboxID,
                        'shapeProperties' : {
                            'contentAlignment' : 'MIDDLE'
                        },
                        'fields' : 'contentAlignment'
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
            self.send_req.append(send_req)
        
        # search lyrics of given hymn
        def searchLyrics(hymns, num):
            for hymn in hymns:
                if hymn['hymnNumber'] == num:
                    return hymn['lyrics']

        # search hymn obj
        def searchHymn(hymns, num):
            for hymn in hymns:
                if hymn['hymnNumber'] == num:
                    return hymn

        # open file and fetch file
        f = open('./hymn_unnumbered.json') if number == 0 else open('./hymn_numbered.json')
        loadedJson = json.load(f)

        foundHymn = searchHymn(loadedJson, number)
        hymnMainPageGenerator(foundHymn, background)
        foundLyric = searchLyrics(loadedJson, number)

        for lyric in foundLyric:
            hymnGenerator(lyric)

    def batchExport(self):
        self.SLIDES.presentations().batchUpdate(body={'requests' : self.send_req}, presentationId=self.deckID).execute()
