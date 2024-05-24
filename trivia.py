import json
import requests
import random

joke_keywords = ['joke', 'funny', 'laugh']
greet_keywords = ['hello', 'hi', 'hey', 'yo']
wiki_keywords = ['wiki', 'fact', 'learn', 'teach']

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

def joke():
    response = requests.get(r"https://official-joke-api.appspot.com/random_ten")
    json_data = json.loads(response.text)
    for i in (json_data):
        Setup = (i["setup"])
        Punchline = (i["punchline"])
    return(Setup, Punchline)  

def random_wiki():
    response = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/summary")
    json_data = json.loads(response.text)
    url = json_data['content_urls']['desktop']['page']
    return json_data['title'], url  

def get_trivia(msg):
    if any(word in msg.lower() for word in greet_keywords):
        return f'{random.choice(greet_keywords).capitalize()}!'

    if msg.startswith('$inspire') or 'inspir' in msg.lower():
        return get_quote()

    #to check if above message has required keywords
    if any(word in msg.lower() for word in joke_keywords):
        setup, punchline = joke()
        return f'{setup}\n{punchline}'

    if any(word in msg.lower() for word in wiki_keywords):
        title, url = random_wiki()
        return f'Check out {title}: \n{url}'
    return False