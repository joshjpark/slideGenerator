from slides import Slides
import random
import json
import bg

# sn.createVerses('James', '1', '8', '1', '15', '1', '9', 'James Message Title', 'https://upload.wikimedia.org/wikipedia/commons/8/85/Haliaeetus_pelagicus_%28Rausu%2C_Japan%29.jpg','https://upload.wikimedia.org/wikipedia/commons/8/85/Haliaeetus_pelagicus_%28Rausu%2C_Japan%29.jpg')

sn = Slides()
sn.Title('April 23rd 2020', bg.findRandomImg())
sn.createHymn(219, "hymn", bg.findRandomImg())
sn.createTransition('Silent Prayer', bg.findRandomImg())
sn.createRecital('Creed', bg.findRandomImg())
sn.createHymn(9, "hymn", bg.findRandomImg())
sn.createTransition("Representative prayer", bg.findRandomImg())
# sn.createVerses('Joshua', '1', '6', '2', '6', '1', '8', "Be strong and courageous",bg.findRandomImg(), bg.findRandomImg())
sn.createVerses('1 Corinthians', '4', '1', '4', '21', '4', '15', 'I became your father' , bg.findRandomImg(), bg.findRandomImg())
sn.createHymn(71, "hymn", bg.findRandomImg())
sn.createTransition('Announcement', bg.findRandomImg())
sn.createRecital('Prayer', bg.findRandomImg())
sn.batchExport()