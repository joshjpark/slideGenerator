import json

with open('bible.json') as json_file:
	data = json.load(json_file)

def getVerses(book, fromChapter, fromVerse, toChapter, toVerse):
	with open('bible.json') as json_file:
		data = json.load(json_file)
	
	result = []

	# same chapter
	if (fromChapter == toChapter):
		for i in range(int(fromVerse), int(toVerse) + 1):
			result.append(str(i) + " " + data[book][fromChapter][str(i)])
	
	# spans chapters
	else:
		for chapter in range(int(fromChapter), int(toChapter)+1):
			offset = len(data[book][str(chapter)])
			
			if chapter == int(fromChapter):
				for i in range(int(fromVerse), offset + 1):
					result.append(str(i) + " " + data[book][str(chapter)][str(i)])
			
			elif chapter == int(toChapter):
				for i in range(1, int(toVerse) + 1):
					result.append(str(i) + " " + data[book][str(chapter)][str(i)])
			
			else:
				for i in range(1, offset + 1):
					result.append(str(i) + " " + data[book][str(chapter)][str(i)])
	
	return result

