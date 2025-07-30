import tiktoken
from tenacity import retry, wait_random_exponential, stop_after_attempt
from openai import OpenAI

# Initialize client (will be set from main app)
client = None
GPT_MODEL = None

def set_client_and_model(openai_client, model_name):
    """
    Set the OpenAI client and model for the chat utilities.
    
    Args:
        openai_client: The OpenAI client instance
        model_name (str): The GPT model name to use
    """
    global client, GPT_MODEL
    client = openai_client
    GPT_MODEL = model_name

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tool_choice, tools, model=None):
    """
    Make a chat completion request to OpenAI with retry logic.
    
    Args:
        messages (list): List of conversation messages
        tool_choice: Tool choice parameter for OpenAI API
        tools: Available tools for the agent
        model (str, optional): Model to use, defaults to global GPT_MODEL
    
    Returns:
        OpenAI response object or Exception if failed
    """
    if not client:
        raise ValueError("Client not initialized. Call set_client_and_model() first.")
    
    model_to_use = model or GPT_MODEL
    try:
        response = client.chat.completions.create(
            model=model_to_use,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

def memory_optimise(messages: list):
    """
    Optimize memory usage by summarizing old messages when conversation gets too long.
    
    Args:
        messages (list): List of conversation messages
    
    Returns:
        list: Optimized message list with summarized history if needed
    """
    if not client:
        raise ValueError("Client not initialized. Call set_client_and_model() first.")
    
    system_prompt = messages[0]["content"]
    
    # Token count using tiktoken
    encoding = tiktoken.encoding_for_model(GPT_MODEL)
    
    if len(messages) > 24 or len(encoding.encode(str(messages))) > 10000:
        latest_messages = messages[-12:]
        
        token_count_latest_messages = len(encoding.encode(str(latest_messages)))
        print(f"Token count of latest messages: {token_count_latest_messages}")
        
        index = messages.index(latest_messages[0])
        early_messages = messages[:index]
        
        prompt = f"""{early_messages}
        -----
        Above is the past history of conversation between user & AI,
        including actions AI already taken
        Please summarise the past actions taken so far,
        what key information learnt & tasks that already completed
        
        SUMMARY:
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
        )
        
        system_prompt = f"""{system_prompt}; Here is a summary of past actions taken so far: {response.choices[0].message.content}"""
        messages = [{"role": "system", "content": system_prompt}] + latest_messages
        
        return messages
    
    return messages 