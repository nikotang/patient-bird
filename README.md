# 🐦 Patient Bird

A Discord chatbot powered by LLMs. Written in Python 🐍 with Discord.py 🤖 and Langchain 🦜🔗. Less like an assistant and more like a bird that tweets along with your conversations.

Works out of the box, but also a good starting point for your own bot. An API key is all you need.

## 🔑 Key Features

✅ __Plug and play__: it works as long as you have an API key from Anthropic/Cohere/Deepinfra/Google AI/Mistral/Huggingface/OpenAI or you have Ollama installed.

✅ __Flexible__: you can edit your system prompt or change models even when it's already running.

✅ __Reads chat history__: a configurable amount of earlier messages are used as input (along with who sent the messages) to generate responses. 

❌ __Image generation__: Patient Bird doesn't paint. 

❌ __Read PDFs__: Patient Bird is no office admin.

## 📖 Contents

 - [Introduction](#Introduction)
 - [Set up](#Set-up)
 - [Run locally](#Run-locally)

## 🤔 Introduction

There are quite some Discord integrations with LLMs, most being replicas of AI assistants, server moderators or chatbots focused on character adaptation.

This is something simple, a bot that feels like just another member in the server. Or a backbone/boilerplate that can be easily customised for servers with specific themes or purposes, because it has been a pain orienting around the Discord.py and Langchain docs.

## 🔧 Set up

You can configure the LLM you want to use by editing the `config.json` file, or not touch it and make changes via slash commands in Discord when the bot is already running.

## 🏠 Run locally

1. Clone the repo and get in the directory.

```bash
git clone https://github.com/nikotang/patient-bird.git
cd patient-bird
```

2. (Create a virtual environment and) Install the requirements. 

```bash
pip install -r requirements.txt
```

`requirements_lite.txt` excludes all model-specific Langchain dependencies for a cleaner environment. You can then install the dependency only for the model(s) you want to use, e.g.:

```bash
pip install -r requirements_lite.txt
pip install langchain_openai
```

3. Rename `example.env` to `.env`. Inside, add your [Discord server ID](https://www.businessinsider.com/guides/tech/discord-id) to DISCORD_TOKEN and add the API key(s) of the LLM(s) you want to use.

```bash
mv example.env .env
```
```
DISCORD_TOKEN=server_id
XXX_API_KEY=your_api_key
```

4. Run `main.py`.

```bash
python main.py
```

## ☁️ Hosting

Maybe I will, but not soon.

<details>
<summary>todo</summary>

## 🎡 Trivia

asdf

### 📋 Todo List

- [x] Format chat to be stored in Chatbot.store_message()
- [x] Edit system message
- [x] Add other models
- [x] document the code...
- [ ] match key features and edit config.json params on Discord
- [ ] trim message
- [ ] Add/drop misc APIs?
- [ ] use cogs
- [ ] edit model for specific channel
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
- [ ] Incorporate server/channel/member info?
- [ ] multimedia understanding

```Python
  File "/Users/Me/Documents/lepatientparrot/main.py", line 73, in on_message
    session_id = message.channel.name
AttributeError: 'DMChannel' object has no attribute 'name'
```

</details>