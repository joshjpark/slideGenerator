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

import json

with open('bible.json') as json_file:
	data = json.load(json_file)


'''
@param: 	book,fromChapter, fromVerse, toChapter, toVerse			
@return: 	retVerses		return read verses in an array
'''
def get_verses(book, fromChapter, fromVerse, toChapter, toVerse):
	with open('bible.json') as json_file:
		data = json.load(json_file)
	
	retVerses = []

	# verses in same chapter
	if (fromChapter == toChapter):
		for i in range(int(fromVerse), int(toVerse)+1):
			retVerses.append(str(i) + " " + data[book][fromChapter][str(i)])

	# verses in extending chapters 
	else:
		for currChapter in range(int(fromChapter), int(toChapter)+1): #loop through every chapter
			offset = len(data[book][str(currChapter)])
			if currChapter == int(fromChapter):
				#read up the rest of the chapter
				#offset = len(data[book][str(currChapter)])
				for i in range(int(fromVerse), offset+1):
					retVerses.append(str(i) + " " + data[book][str(currChapter)][str(i)])
			elif currChapter == int(toChapter):
				#read up to toVerse
				for i in range(1, int(toVerse) + 1):
					retVerses.append(str(i) + " " + data[book][str(currChapter)][str(i)])
			else:
				for i in range(1, offset+1):
					retVerses.append(str(i) + " " + data[book][str(currChapter)][str(i)])
	return retVerses

# verses = []
# verses = get_verses('1 Corinthians', '15', '35', '15', '38')
# for verse in verses:
# 	print(verse)

verses2 = get_verses('John', '6', '22', '8', '2')
for verse in verses2:
	print(verse)
#Case (1): All within the same chapter (This is no problem)
#Case (2): Verses expand through two chapters
#Case (3): Verses expand through mutliple chapters
#Case (4): Verses expand through multiple books (Do not consider this)

