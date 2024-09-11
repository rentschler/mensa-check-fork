from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from cachetools import cached, TTLCache
from bs4 import BeautifulSoup
import requests


cache = TTLCache(maxsize=1, ttl=3600)
app = FastAPI()
templates = Jinja2Templates(directory="template")

@cached(cache)
def checkMensa():
    print("Checking Mensa")
    
    url = 'https://seezeit.com/essen/speiseplaene/mensa-giessberg/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    today = soup.find('a', class_='heute')['rel'][0]
    today_menu = soup.find('div', id=f'tab{today}')
    meals = today_menu.find_all('div', class_='title')

    spaetzle = None
    for m in meals:
        if "Spätzle" in m.text:
            spaetzle = m
            break

    if spaetzle is not None:
        ingredients = spaetzle.find('sup').text
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

