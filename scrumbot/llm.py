import os
from langchain_core.language_models.chat_models import BaseChatModel

def get_llm(model_name: str) -> BaseChatModel:
    """
    Factory function to get a Language Model.
    
    Args:
        model_name: Name of the model (e.g., 'gemini-1.5-pro', 'gpt-4o', 'claude-3-opus-20240229', 'llama3-70b').
        
    Returns:
        A LangChain ChatModel instance.
    """
    if "gemini" in model_name.lower():
        from langchain_google_genai import ChatGoogleGenAI
        return ChatGoogleGenAI(model=model_name)
    elif "gpt" in model_name.lower():
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=model_name)
    elif "claude" in model_name.lower():
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model=model_name)
    elif "llama" in model_name.lower():
        from langchain_openai import ChatOpenAI
        # Using NVIDIA NIM for Llama models
        api_key = os.environ.get("NVIDIA_API_KEY")
        return ChatOpenAI(
            model=model_name,
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key
        )
    else:
        raise ValueError(f"Unsupported model: {model_name}")
