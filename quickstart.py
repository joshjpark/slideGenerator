def createWorshipSlideTextBox(phrase, font, size):
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
                    'fontSize': {
                        'magnitude': size,
                        'unit': 'PT'
                    }
                },
                'textRange': {'type': 'FIXED_RANGE', 'startIndex': 0, 'endIndex': len(phrase)},
                'fields': 'fontFamily, fontSize',
            }
        },

        {
            'updateParagraphStyle': {
                'objectId': textBoxID,
                'style': {
                    'lineSpacing': 150
                },
                'fields': 'lineSpacing'
            }
        }
    ]

    SLIDES.presentations().batchUpdate(body={'requests': send_req},
    presentationId=deckID).execute()
