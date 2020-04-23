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
					
				
	# # verses in same chapter
	# if (fromChapter == toChapter):
	# 	for i in range(int(fromVerse), int(toVerse)+1):
	# 		retVerses.append(str(i) + " " + data[book][fromChapter][str(i)])

	# # verses in extending chapters 
	# else:
	# 	for currChapter in range(int(fromChapter), int(toChapter)+1): #loop through every chapter
	# 		offset = len(data[book][str(currChapter)])
	# 		if currChapter == int(fromChapter):
	# 			#read up the rest of the chapter
	# 			#offset = len(data[book][str(currChapter)])
	# 			for i in range(int(fromVerse), offset+1):
	# 				retVerses.append(str(i) + " " + data[book][str(currChapter)][str(i)])
	# 		elif currChapter == int(toChapter):
	# 			#read up to toVerse
	# 			for i in range(1, int(toVerse) + 1):
	# 				retVerses.append(str(i) + " " + data[book][str(currChapter)][str(i)])
	# 		else:
	# 			for i in range(1, offset+1):
	# 				retVerses.append(str(i) + " " + data[book][str(currChapter)][str(i)])
	# return retVerses

