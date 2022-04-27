import hashlib
import re

def query_hash(query:str)->str:
    return hashlib.md5(query.encode("utf-8")).hexdigest()

def clean_filename(filename:str)->str:
    return re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", "", filename)

def clean_query(query:str)->str:
    return re.sub(r"\W", "", query).lower()