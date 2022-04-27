import os
import warnings
from numpy import require

import openai
import pandas as pd

openai.api_key = os.getenv("OPENAI_API_KEY")

def require_api_key(func):
    def wrapper(*args, **kwargs):
        if (not openai.api_key):
            raise RuntimeError("No api key set for OpenAI. Export key to OPENAI_API_KEY environment variable.")
        else:
            return func(*args, **kwargs)
    
    return wrapper

@require_api_key
def get_engine_list():
    return openai.Engine.list()["data"]

@require_api_key
def get_engine_index():
    _engine_df = pd.DataFrame.from_records(get_engine_list())
    _engine_df.set_index("id", inplace=True)

    return _engine_df.to_dict(
        orient="index",
    )

@require_api_key
def print_engine_list():
    print (pd.DataFrame.from_records(get_engine_list()))

@require_api_key
def online():
    try:
        return bool(get_engine_list)
    except Exception as e:
        return False

@require_api_key
def is_ready(engine_id:str):
    _engine_index = get_engine_index()

    _engine_info = _engine_index.get(engine_id, {})
    
    return _engine_info.get("ready", False)

def get_endpoint(endpoint:str):
    """
    Get the actual class which relates to the endpoint.
    """

    # Additional mapping where errors are common
    _map = {
        "Completions":"Completion",
    }

    endpoint = _map.get(
        endpoint.title(),
        endpoint.title(),
    )
    
    _cls = getattr(openai, endpoint, None)

    # Verify its the right type of stuff
    if (isinstance(_cls, type)):
        if (issubclass(_cls, openai.api_resources.abstract.engine_api_resource.EngineAPIResource)):
            return _cls
        
    return None