from dotenv import load_dotenv
import os
from typing import Optional

from langchain_core.language_models.chat_models import BaseChatModel

load_dotenv()

def chat_model(provider, model=None, user_api_key=None) -> Optional[BaseChatModel]:
    """Returns the provider-specific Langchain ChatModel, e.g. ChatOpenAI. """
    if provider == "anthropic":
        try:
            from langchain_anthropic import ChatAnthropic
        except ImportError:
            raise ImportError("langchain_anthropic not installed.")
        api_key = user_api_key or os.getenv("ANTHROPIC_API_KEY")
        return ChatAnthropic(model=model, api_key=api_key) # TODO: model can't be None?
        
    elif provider == "cohere":
        try:
            from langchain_cohere import ChatCohere
        except ImportError:
            raise ImportError("langchain_cohere not installed.")
        api_key = user_api_key or os.getenv("COHERE_API_KEY")
        return ChatCohere(model=model, api_key=api_key)

    elif provider == "deepinfra":
        try:
            from langchain_community.chat_models import ChatDeepInfra
        except ImportError:
            raise ImportError("langchain_community not installed.")
        api_key = user_api_key or os.getenv("DEEPINFRA_API_KEY")
        return ChatDeepInfra(model=model, api_key=api_key)

    elif provider == "google":
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
        except ImportError:
            raise ImportError("langchain_google_genai not installed.")
        api_key = user_api_key or os.getenv("GOOGLE_API_KEY")
        return ChatGoogleGenerativeAI(model=model, api_key=api_key)
    
    elif provider == "groq":
        try:
            from langchain_groq import ChatGroq
        except ImportError:
            raise ImportError("langchain_groq not installed.")
        api_key = user_api_key or os.getenv("GROQ_API_KEY")
        return ChatGroq(model=model, api_key=api_key)
    
    elif provider == "mistral":
        try:
            from langchain_mistralai.chat_models import ChatMistralAI
        except ImportError:
            raise ImportError("langchain_mistralai not installed.")
        api_key = user_api_key or os.getenv("MISTRAL_API_KEY")
        return ChatMistralAI(model=model, api_key=api_key)

    elif provider == "huggingface":
        try:
            from langchain_huggingface import ChatHuggingFace
        except ImportError:
            raise ImportError("langchain_huggingface not installed.")
        api_key = user_api_key or os.getenv("HUGGINGFACE_API_KEY") or os.getenv("HF_TOKEN")
        return ChatHuggingFace(model=model, api_key=api_key)
      
    elif provider == "ollama":
        try:
            from langchain_community.chat_models import ChatOllama
        except ImportError:
            raise ImportError("langchain_community not installed.")
        return ChatOllama(model=model)

    elif provider == "openai":
        try:
            from langchain_openai import ChatOpenAI
        except ImportError:
            raise ImportError("langchain_openai not installed.")
        api_key = user_api_key or os.getenv("OPENAI_API_KEY")
        return ChatOpenAI(model=model, api_key=api_key)
    
    elif provider is None:
        return None

    else:
        raise ValueError(f"{provider} not supported.")
