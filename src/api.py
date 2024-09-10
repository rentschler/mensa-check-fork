from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
from cachetools import cached, TTLCache

cache = TTLCache(maxsize=1, ttl=3600)
app = FastAPI()
templates = Jinja2Templates(directory="template")

@cached(cache)
def checkMensa():
    print("Checking Mensa")
    url = 'https://seezeit.com/essen/speiseplaene/mensa-giessberg/'
    r = requests.get(url)
    text = r.text
    pos = text.find('Spätzle')
    if pos != -1:
        cut = r.text[r.text.find('Spätzle'):r.text.find('Spätzle')+50]
        ingredients = cut.split('(')[1].split(')')[0].split(',')
        if '28' in ingredients:
            answer = "Spätzle with egg today"
            color = "green"
            emoji = "✅"
        else:
            answer = "WARNING: Spätzle without egg today"
            color = "red"
            emoji = "❌"
    else:
        answer = "No Spätzle today "
        color = "grey"
        emoji = "🤷🏻‍♂️"

    return answer, color, emoji

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    answer, color, emoji = checkMensa()
    return templates.TemplateResponse(
        request=request, name="main.html", context={"text": answer, "color": color , "emoji": emoji}
    )

