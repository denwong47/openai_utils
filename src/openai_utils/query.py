import os, sys
import hashlib
import json
import time
from typing import Any, Dict, Union

import openai

import openai_utils.exceptions as exceptions
from openai_utils.bin import        query_hash,         \
                                    clean_query,        \
                                    clean_filename
from openai_utils.status import     require_api_key,    \
                                    get_endpoint

from openai_utils.settings import   OPENAI_API_ENGINE,  \
                                    LOG_DEFAULT_PATH,   \
                                    LOG_FILENAME_FORMAT

@require_api_key
def send(
    query:str,
    category:str = "generic_test",
    log_filename_format:str = LOG_FILENAME_FORMAT,
    log_path:Union[str, None] = LOG_DEFAULT_PATH,
    engine_id:str = "text-davinci-002",
    endpoint:str = "completions",
    max_tokens:int = 512,
    **kwargs,
):
    """
    Send a prompt to OpenAI; log the result if requested.
    """

    # check category
    if ((not category) or \
        (not isinstance(category, str))
        ):
        raise RuntimeError(f"category needs to be a non-empty string instead of {repr(category)}.")

    # check endpoint
    _apiclass = get_endpoint(endpoint=endpoint)
    if (not _apiclass):
        raise RuntimeError(f"endpoint '{endpoint}' not recognised.")

    # start query
    _query = {
        "engine":       engine_id,
        "prompt":       query,
        "max_tokens":   max_tokens,
        **kwargs,
    }

    try:
        _time_start = time.perf_counter()

        _response = _apiclass.create(
            **_query,
        )

        _process_duration = time.perf_counter() - _time_start
    except Exception as e:
        return exceptions.OpenAIRequestFailed(
                f"{type(e).__name__}: {str(e)}",
            )

    # log result
    if (log_path is not None):
        _clean_query = clean_query(query)

        _log_formatters = {
            **_query,
            "category":     category,
            "endpoint":     _apiclass.__name__.lower(),
            "timestamp":    _response.get("created", "NaT"),
            "query_hash":   query_hash(query),
            "query_hash_short":   query_hash(query)[:8],
            "query_head":   _clean_query[:20],
            "query_tail":   _clean_query[-20:],
        }

        _log_path = os.path.join(
            log_path,
            clean_filename(
                log_filename_format.format(
                    **_log_formatters,
                )
            )
        )

        # Embed the original query into the object
        _response["prompt"] = query
        _response["duration"] = _process_duration

        try:
            with open(_log_path, "w") as _f:
                json.dump(
                    _response,
                    _f,
                    indent=4,
                )

            return _response
        except (
            FileNotFoundError,
            OSError,
        ) as e:
            return exceptions.LocalFileSystemError(
                f"{type(e).__name__}: {str(e)}",
            )