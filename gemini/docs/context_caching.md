# Context caching






Gemini 2.5 Pro Preview is now available for production use! [Learn more](https://blog.google/technology/google-deepmind/gemini-model-thinking-updates-march-2025/)



* [Home](https://ai.google.dev/)
* [Gemini API](https://ai.google.dev/gemini-api)
* [Models](https://ai.google.dev/gemini-api/docs)



Send feedback

# Context caching



Python
JavaScript
Go
REST


In a typical AI workflow, you might pass the same input tokens over and over to
a model. Using the Gemini API context caching feature, you can pass some content
to the model once, cache the input tokens, and then refer to the cached tokens
for subsequent requests. At certain volumes, using cached tokens is lower cost
than passing in the same corpus of tokens repeatedly.

When you cache a set of tokens, you can choose how long you want the cache to
exist before the tokens are automatically deleted. This caching duration is
called the *time to live* (TTL). If not set, the TTL defaults to 1 hour. The
cost for caching depends on the input token size and how long you want the
tokens to persist.

Context caching varies from [model to model](/gemini-api/docs/models).

## When to use context caching

Context caching is particularly well suited to scenarios where a substantial
initial context is referenced repeatedly by shorter requests. Consider using
context caching for use cases such as:

* Chatbots with extensive [system instructions](/gemini-api/docs/system-instructions)
* Repetitive analysis of lengthy video files
* Recurring queries against large document sets
* Frequent code repository analysis or bug fixing

## How to use context caching

This section assumes that you've installed a Gemini SDK (or have curl installed)
and that you've configured an API key, as shown in the
[quickstart](/gemini-api/docs/quickstart).

### Generate content using a cache

The following example shows how to generate content using a cached system
instruction and video file.

### Videos

```
import os
import pathlib
import requests
import time

from google import genai
from google.genai import types

client = genai.Client()

# Download video file
url = 'https://storage.googleapis.com/generativeai-downloads/data/SherlockJr._10min.mp4'
path_to_video_file = pathlib.Path('SherlockJr._10min.mp4')
if not path_to_video_file.exists():
  with path_to_video_file.open('wb') as wf:
    response = requests.get(url, stream=True)
    for chunk in response.iter_content(chunk_size=32768):
      wf.write(chunk)

# Upload the video using the Files API
video_file = client.files.upload(file=path_to_video_file)

# Wait for the file to finish processing
while video_file.state.name == 'PROCESSING':
  print('Waiting for video to be processed.')
  time.sleep(2)
  video_file = client.files.get(name=video_file.name)

print(f'Video processing complete: {video_file.uri}')

# You must use an explicit version suffix: "-flash-001", not just "-flash".
model='models/gemini-2.0-flash-001'

# Create a cache with a 5 minute TTL
cache = client.caches.create(
    model=model,
    config=types.CreateCachedContentConfig(
      display_name='sherlock jr movie', # used to identify the cache
      system_instruction=(
          'You are an expert video analyzer, and your job is to answer '
          'the user\'s query based on the video file you have access to.'
      ),
      contents=[video_file],
      ttl="300s",
  )
)

# Construct a GenerativeModel which uses the created cache.
response = client.models.generate_content(
  model = model,
  contents= (
    'Introduce different characters in the movie by describing '
    'their personality, looks, and names. Also list the timestamps '
    'they were introduced for the first time.'),
  config=types.GenerateContentConfig(cached_content=cache.name)
)

print(response.usage_metadata)

# The output should look something like this:
#
# prompt_token_count: 696219
# cached_content_token_count: 696190
# candidates_token_count: 214
# total_token_count: 696433

print(response.text)

```

### PDFs

```
from google import genai
from google.genai import types
import io
import httpx

client = genai.Client()

long_context_pdf_path = "https://www.nasa.gov/wp-content/uploads/static/history/alsj/a17/A17_FlightPlan.pdf"

# Retrieve and upload the PDF using the File API
doc_io = io.BytesIO(httpx.get(long_context_pdf_path).content)

document = client.files.upload(
  file=doc_io,
  config=dict(mime_type='application/pdf')
)

model_name = "gemini-2.0-flash-001"
system_instruction = "You are an expert analyzing transcripts."

# Create a cached content object
cache = client.caches.create(
    model=model_name,
    config=types.CreateCachedContentConfig(
      system_instruction=system_instruction,
      contents=[document],
    )
)

# Display the cache details
print(f'{cache=}')

# Generate content using the cached prompt and document
response = client.models.generate_content(
  model=model_name,
  contents="Please summarize this transcript",
  config=types.GenerateContentConfig(
    cached_content=cache.name
  ))

# (Optional) Print usage metadata for insights into the API call
print(f'{response.usage_metadata=}')

# Print the generated text
print('\n\n', response.text)

```

### List caches

It's not possible to retrieve or view cached content, but you can retrieve
cache metadata (`name`, `model`, `display_name`, `usage_metadata`,
`create_time`, `update_time`, and `expire_time`).

To list metadata for all uploaded caches, use `CachedContent.list()`:

```
for cache in client.caches.list():
  print(cache)

```

To fetch the metadata for one cache object, if you know its name, use `get`:

```
client.caches.get(name=name)

```
### Update a cache

You can set a new `ttl` or `expire_time` for a cache. Changing anything else
about the cache isn't supported.

The following example shows how to update the `ttl` of a cache using
`client.caches.update()`.

```
from google import genai
from google.genai import types

client.caches.update(
  name = cache.name,
  config  = types.UpdateCachedContentConfig(
      ttl='300s'
  )
)

```

To set the expiry time, it will accepts either a `datetime` object
or an ISO-formatted datetime string (`dt.isoformat()`, like
`2025-01-27T16:02:36.473528+00:00`). Your time must include a time zone
(`datetime.utcnow()` doesn't attach a time zone,
`datetime.now(datetime.timezone.utc)` does attach a time zone).

```
from google import genai
from google.genai import types
import datetime

# You must use a time zone-aware time.
in10min = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=10)

client.caches.update(
  name = cache.name,
  config  = types.UpdateCachedContentConfig(
      expire_time=in10min
  )
)

```
### Delete a cache

The caching service provides a delete operation for manually removing content
from the cache. The following example shows how to delete a cache:

```
client.caches.delete(cache.name)

```
## How caching reduces costs

Context caching is a paid feature designed to reduce overall operational costs.
Billing is based on the following factors:

1. **Cache token count:** The number of input tokens cached, billed at a
   reduced rate when included in subsequent prompts.
2. **Storage duration:** The amount of time cached tokens are stored (TTL),
   billed based on the TTL duration of cached token count. There are no minimum
   or maximum bounds on the TTL.
3. **Other factors:** Other charges apply, such as for non-cached input tokens
   and output tokens.

For up-to-date pricing details, refer to the Gemini API [pricing
page](/pricing). To learn how to count tokens, see the [Token
guide](/gemini-api/docs/tokens).

## Additional considerations

Keep the following considerations in mind when using context caching:

* The *minimum* input token count for context caching is 4,096, and the
  *maximum* is the same as the maximum for the given model. (For more on
  counting tokens, see the [Token guide](/gemini-api/docs/tokens)).
* The model doesn't make any distinction between cached tokens and regular
  input tokens. Cached content is a prefix to the prompt.
* There are no special rate or usage limits on context caching; the standard
  rate limits for `GenerateContent` apply, and token limits include cached
  tokens.
* The number of cached tokens is returned in the `usage_metadata` from the
  create, get, and list operations of the cache service, and also in
  `GenerateContent` when using the cache.




Send feedback




Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-04-24 UTC.



Need to tell us more?



[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-04-24 UTC."],[],[]]



