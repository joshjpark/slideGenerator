import requests

#grab the critical size and transform what you need
url = "https://slides.googleapis.com/v1/presentations/1Y1yyv5_sHS-OBnuqSu6xxx8HV4Ceslxar1QKOqqWgL8"

r = requests.get(url)

text = r.text

print(text)