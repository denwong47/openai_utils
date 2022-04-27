import os

OPENAI_API_ENGINE = "https://api.openai.com/v1/engines/{engine_id}/{endpoint}"

LOG_DEFAULT_PATH = os.getenv("OPENAI_LOG_PATH", None)
LOG_FILENAME_FORMAT = "openai-{category}-{engine}-{query_head}...{query_tail}-{query_hash_short}-{timestamp}.json"