# openai_utils
 Simple functions for sending queries to OpenAI, and log the result as JSON files.


# Environment Variables

`OPENAI_API_KEY` - your OpenAI API key, as per OpenAI documentation.\
`OPENAI_LOG_PATH` - where the logs are to be saved on your local system.



# Methods

## openai_utils.send_query
 ```
 def send_query(
    query:str,
    category:str = "generic_test",
    log_filename_format:str = LOG_FILENAME_FORMAT,
    log_path:Union[str, None] = LOG_DEFAULT_PATH,
    engine_id:str = "text-davinci-002",
    endpoint:str = "completions",
    max_tokens:int = 512,
    **kwargs,
 ):
 ```

 Sends a query to OpenAI. \
 \
 `query` - Prompt to be sent. \
 `category` - Used for logging only - can be used in file name via `{category}`\
 `log_filename_format` - Format of log json file name. See separate section below.
 `log_path` - Path of log json files. Default to environmental variable `OPENAI_LOG_PATH` if `None`.\
 `engine_id` - Valid engine name for OpenAI. Use `openai_utils.status.print_engine_list()` to see all available engines.\
 `endpoint` - name for endpoint for OpenAI. Expects `completion`, `edits`, `classification`, etc. Not case-sensitive.\
 `max_tokens` - maximum tokens allowed.\
 `**kwargs` - any other keyworded arguments as per OpenAI API Documentation.\

# Misc Settings

### Log File Format Strings
 Supported keywords:

 - `{category}` - parameter of `send_query`.
 - `{endpoint}` - endpoint name.
 - `{engine}` - engine name.
 - `{prompt}` - the full string prompt sent. This should NOT be used in the file name.
 - `{max_tokens}` - max tokens specified.
 - `{timestamp}` - timestamp as returned in the OpenAI response.
 - `{query_hash}` - MD5 hash of the prompt.
 - `{query_hash_short}` - the first 8 characters of the MD5 hash of the prompt.
 - `{query_head}` - First 20 characters of the prompt, with all non-alphanumeric characters removed.
 - `{query_tail}` - Last 20 characters of the prompt, with all non-alphanumeric characters removed.
 