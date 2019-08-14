import bib

def createWorshipServiceSlides(book, fromChapter, fromVerse, toChapter, toVerse, font, size):  
    verses = bib.get_verses(book, fromChapter, fromVerse, toChapter, toVerse)
    temp = []

    for i in range(0,len(verses)):
        if i % 2 == 0 :
            temp.append(verses[i])
            if i == len(verses)-1:
                print(temp)
        elif i % 2 == 1:
            temp.append(verses[i])
            print(temp)
            temp = []
    

createWorshipServiceSlides('John', '1', '1', '1', '13', 'Average', '28')
