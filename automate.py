
from __future__ import print_function
import uuid
import bib

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

def gen_uuid(): return str(uuid.uuid4())
  
class Slides:
  def __init__(self):
   SCOPES = 'https://www.googleapis.com/auth/presentations',
  store = file.Storage('storage.json')
  creds = store.get()
  if not creds or creds.invalid:
      flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
      creds = tools.run_flow(flow, store)
  # create service end point for the slides API
  SLIDES = discovery.build('slides', 'v1', http=creds.authorize(Http()))

    

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