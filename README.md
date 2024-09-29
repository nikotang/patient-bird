<h1 align="center">🐦 Patient Bird</h1>

<h2 align="center">A Discord chatbot powered by LLMs. Written in Python 🐍 with Discord.py 🤖 and Langchain 🦜🔗.</h2>

Less like an assistant and more like a bird that tweets along with your conversations.

Works out of the box, but also a good starting point for your own bot. An API key is all you need.

## 🔑 Key Features

✅ __Plug and play__: it works as long as you have an API key from Anthropic/Cohere/Deepinfra/Google AI/Groq/Huggingface/Mistral/OpenAI or you have Ollama installed.

✅ __Flexible__: Config your bot with other server members: you can edit your system prompt or change models even when it's already running. No need to decide everything in a config file.

✅ __Reads chat history__: a configurable amount of earlier messages are used as input (along with who sent the messages) to generate responses. 

❌ __Image generation__: Patient Bird doesn't paint. 

❌ __Read PDFs__: Patient Bird is no office admin.

## 📖 Contents

 - [Introduction](#Introduction)
 - [Set up](#Set-up)
 - [Run locally](#Run-locally)
 - [Usage](#Usage)

## 🤔 Introduction

There are quite some Discord integrations with LLMs, most being replicas of AI assistants, server moderators or chatbots focused on character adaptation.

This is something simple, a bot that feels like just another member in the server. Or a backbone/boilerplate that can be easily customised for servers with specific themes or purposes, because it has been a pain orienting around the Discord.py and Langchain docs.

## 🔧 Set up

You can configure the LLM you want to use by editing the `config.json` file, or not touch it and make changes via slash commands in Discord when the bot is already running.

## 🏠 Run locally

0. Create a Discord bot [here](https://discord.com/developers/applications). Select 'bot' in the OAuth2 URL Generator under OAuth2, then tick 'Read Messages/View Channels' under General Permissions, then you can check all Text Permissions for convenience. Paste and go to the URL with your browser to invite the bot to your server. [reference](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/)

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

## Usage

Mention `@YourBot` in a channel to talk to it. That's it.

`/set` to set the LLM provider (e.g. `openai`) and model (e.g. `gpt-turbo-3.5`) to use, if not specified in `configs.json`, or if you want to switch to another model.

View the current system prompt with `/prompt view`, and change it with `/prompt edit`.

See the chat history your bot sees with `/history view`.
Clear it with `/history clear`. Change the limit of chat entries to save with `/history limit` (saves your API quota). 

The chat history is trimmed upon initiating the next response, so `/history view` only reflects the change after the LLM made a response after the limit is changed. Increasing the limit will not retrospectively add previously unread chats into history.
