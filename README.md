# 🐦 Patient Bird

A Discord chatbot powered by LLMs. Written in Python 🐍 with Discord.py 🤖 and Langchain 🦜🔗. Less like an assistant and more like a bird that tweets along with your conversations.

Works out of the box, but also a good starting point for your own bot. An API key is all you need.

## 🔑 Key Features

✅ 

❌ 


## 📖 Contents

 - [Introduction](#Introduction)
 - [Set up](#Set-up)
 - [Run locally](#Run-locally)
 - [Hosting](#Hosting)

## 🤔 Introduction

There are quite some Discord integrations with LLMs, most being replicas of AI assistants, server moderators or chatbots focused on character adaptation.

This is something simple, a bot that feels like just another member in the server. Or a backbone/boilerplate that can be easily customised for servers with specific themes or purposes, because it has been a pain orienting around the Discord.py and Langchain docs.

## 🔧 Set up

You can configure the bot by editing the `config.json` file, or make changes via slash commands in Discord when the bot is already running.

## 🏠 Run locally


## ☁️ Hosting

<details>
<summary>todo</summary>

### 📋 Todo List

- [x] Format chat to be stored in Chatbot.store_message()
- [x] Edit system message
- [x] Add other models
- [ ] document the code...
- [ ] trim message
- [ ] Add/drop misc APIs?
- [ ] reply to replies
- [ ] warn for wrong model or api key
- [ ] threads - add parent to session name?
- [ ] toggle
- [ ] restrict edit power to admin
- [ ] free flow mode (multi agent?)
- [ ] use your own key
- [ ] test ollama (local models)
- [ ] docker
- [ ] Make it work in DMs

```Python
  File "/Users/Me/Documents/lepatientparrot/main.py", line 73, in on_message
    session_id = message.channel.name
AttributeError: 'DMChannel' object has no attribute 'name'
```

</details>