from __future__ import print_function
import uuid
import bib

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

def gen_uuid(): return str(uuid.uuid4())


class Slides:

    # initialize empty slides
    def __init__(self):
        SCOPES = 'https://www.googleapis.com/auth/presentations',
        store = file.Storage('storage.json')
        creds = store.get()

        # verify credentials
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        SLIDES = discovery.build('slides', 'v1', http=creds.authorize(Http()))

        # create empty batch
        print('** Create new slide deck & set up object IDs')
        rsp = SLIDES.presentations().create(
            body={'title': 'Worship Slides'}).execute()
        deckID = rsp['presentationId']
        SLIDES.presentations().batchUpdate()
        # deckID = rsp['presentationId']      # presentationID from https (url) address
    
    def createSlide(self):
        pass


    def batchRun(self):
        # run through the array and compile
        pass
        






    
