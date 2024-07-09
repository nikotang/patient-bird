import json
import re
import requests
import random

joke_keywords = ['joke', 'funny', 'laugh', 'lol', 'lmao']
greet_keywords = ['hello', 'hi', 'hey', 'yo']
wiki_keywords = ['wiki']

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

def get_joke():
    response = requests.get(r"https://official-joke-api.appspot.com/random_ten")
    json_data = json.loads(response.text)
    for i in (json_data):
        setup = (i["setup"])
        punchline = (i["punchline"])
    return f'{setup}\n{punchline}'

def get_wiki():
    response = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/summary")
    json_data = json.loads(response.text)
    title = json_data['title']
    url = json_data['content_urls']['desktop']['page']
    return f'Check out {title}: \n{url}'

def detect_trivia(msg):
    msg_words = re.findall(r'\w+', msg.lower()) # look at whole words, only used for greetings and wiki

    if any(word in msg_words for word in greet_keywords):
        return f'{random.choice(greet_keywords).capitalize()}!'

    if msg.startswith('$inspire') or 'inspir' in msg.lower():
        return get_quote()

    if any(word in msg.lower() for word in joke_keywords):
        return get_joke()

    if any(word in msg_words for word in wiki_keywords):
        return get_wiki()
    return False

def random_trivia():
    return random.choice((get_quote(), get_joke(), get_wiki()))