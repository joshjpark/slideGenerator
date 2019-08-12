'''
NOTE: In case no internal json file available, import online bible API, to load json files.
An example bible api can be found at: http://labs.bible.org/api_web_service

import urllib.request, json
with urllib.request.urlopen("http://labs.bible.org/api/?passage=John%206:22-45&type=json&formatting=plain") as url:
	#print(url.read().decode())
	#data = json.loads(url.read().decode())
	data = json.loads(url.read().decode())
	#print(data)
	#print(data[0]["text"])
	#print(len(data))

	for verse in range(0,len(data)):
		print(data[verse]["verse"] + " " + data[verse]["text"])
'''
#Try John chapter 6:22-40


import json

with open('bible.json') as json_file:
	data = json.load(json_file)


def get_verses(book, fromChapter, fromVerse, toChapter, toVerse):
	with open('bible.json') as json_file:
		data = json.load(json_file)

	# if all verses in same chapter
	if (fromChapter == toChapter):
		for i in range(int(fromVerse), int(toVerse)+1):
			print(str(i) + " " + data[book][fromChapter][str(i)])


	# if verses in different chapters 
	else:
		for currChapter in range(int(fromChapter), int(toChapter)+1): #loop through every chapter
			offset = len(data[book][str(currChapter)])
			if currChapter == int(fromChapter):
				#read up the rest of the chapter
				#offset = len(data[book][str(currChapter)])
				for i in range(int(fromVerse), offset+1):
					print(str(i) + " " + data[book][str(currChapter)][str(i)])

			elif currChapter == int(toChapter):
				#read up to toVerse
				for i in range(1, int(toVerse) + 1):
					print(str(i) + " " + data[book][str(currChapter)][str(i)])

			else:
				for i in range(1, offset+1):
					print(str(i) + " " + data[book][str(currChapter)][str(i)])

def createSlide():
	pass

def createTitle(date):
	pass

def insert():
	pass


verses = []
verses = get_verses('1 Corinthians', '15', '35', '15', '38')
verses = get_verses("John", '6', '22', '6', '40')

#Case (1): All within the same chapter (This is no problem)
#Case (2): Verses expand through two chapters
#Case (3): Verses expand through mutliple chapters
#Case (4): Verses expand through multiple books (Do not consider this)

