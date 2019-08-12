# from __future__ import print_function
# import pickle
# import os.path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request

# # If modifying these scopes, delete the file token.pickle.
# # NOTE: read & write scope for slides 
# SCOPES = ['https://www.googleapis.com/auth/presentations']

# # The ID of a sample presentation.
# PRESENTATION_ID = '1Xmu4jLetkmwN2ig_cZWb95uYYrKyYdHzMcviwJPWWdU'

# def main():
#     """Shows basic usage of the Slides API.
#     Prints the number of slides and elments in a sample presentation.
#     """
#     creds = None
#     # The file token.pickle stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server()
#         # Save the credentials for the next run
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)

#     # NOTE: service point for our slides API 
#     service = build('slides', 'v1', credentials=creds)

#     # Call the Slides API
#     presentation = service.presentations().get(
#         presentationId=PRESENTATION_ID).execute()
#     slides = presentation.get('slides')

#     print('The presentation contains {} slides:'.format(len(slides)))
#     for i, slide in enumerate(slides):
#         print('- Slide #{} contains {} elements.'.format(
#             i + 1, len(slide.get('pageElements'))))



#     # """Shows basci usage of the Slides API. 
#     # Print "Hello World" slide to the sample presentation
#     # """

#     requests = [
#         {
#             'createSlide': {
#                 'objectId': 1,
#                 'insertionIndex' : '1',
#                 'slideLayoutReference' : {
#                     'predefinedLayout' : 'TITLE_AND_TWO_COLUMNS'
#                 }
#             }
#         }
#     ]

#     # Populate the slide with elements
#     # Add element create requests here, along with the page_id

#     # Execute request
#     body = {
#         'requests': requests
#     }
#     #ERROR HERE! message: 
#     #in original code, it does "response = slides_service.presentations.batchUpdate(presentationId = presentation_id, body = body).execute()"

#     response = service.presentations().batchUpdate(presentationId = PRESENTATION_ID, body = body).execute()
#     create_slide_response = response.get('replies')[0].get('createSlide')
#     print('Created slide with ID: {0}'.format(
#         create_slide_response.get('objectId')))

# # def create_slide(self, presentation_id, page_id):
# #     slides_service = self.service

# #     requests = [
# #         {
# #             'createSlide': {
# #                 'objectId': 1,
# #                 'insertionIndex' : '1',
# #                 'slideLayoutReference' : {
# #                     'predefinedLayout' : 'TITLE_AND_TWO_COLUMNS'
# #                 }
# #             }
# #         }
# #     ]

# #     # Execute request
# #     body = {
# #         'requests': requests
# #     }
# #     response = slides_service.prsentations() \
# #         .batchUpdate(presentationId = prsentation_id, body = body).execute()
# #     create_slide_response = response.get('replies')[0].get('createSlide')
# #     print('Created slide with ID: {0}'.format(
# #         create_slide_response.get('objectId')))
# #     return reponse



# if __name__ == '__main__':
#     main()
#     #create_slide('1Xmu4jLetkmwN2ig_cZWb95uYYrKyYdHzMcviwJPWWdU', 1,1)


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
    {'insertText': {'objectId': smileID, 'text': 'FUCK!!!!!'}},
    {'insertText': {'objectId': str24ID, 'text': 'ADFADFASDFADSFASDF!'}},
    {'insertText': {'objectId': arwbxID, 'text': "An uber bizarre arrow box!"}},

    #Operation (1): Read slide object IDs

    #Operation (2): Read element object IDs from a page

    #Operation (3): Read shape elements from a page
]
SLIDES.presentations().batchUpdate(body={'requests': reqs},
        presentationId=deckID).execute()


#simplement request
# request = [
#     {'createSlide': {
#         'objectId': mdSlideID,
#     }}
#     {'insertText': {'objectId': randId, 'text': 'Hello world!'}}
# ]

# # Operation (1): Read slide object IDs
# # Explanation: Retrieve data of a Google Slide (source: https://github.com/googleapis/google-api-python-client/issues/424)
# slideObjectId = SLIDES.presentations().get(presentationId = deckID)
# print(slideObjectId.presentationId())
# # Operation (2): Read element object IDs
# # Explanation: Retrieve data of a Google Slide page 
# elementObjectId = SLIDES.presentations().pages().get(presentationId = deckID, pageObjectId = 1)
# print(type(elementObjectId))



print('DONE')
