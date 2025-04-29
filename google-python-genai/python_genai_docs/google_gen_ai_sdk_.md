# Google Gen AI SDK¶


# Google Gen AI SDK[¶](#google-gen-ai-sdk "Link to this heading")

[![pypi](https://img.shields.io/pypi/v/google-genai.svg)](https://pypi.org/project/google-genai/)

<https://github.com/googleapis/python-genai>

**google-genai** is an initial Python client library for interacting with
Google’s Generative AI APIs.

Google Gen AI Python SDK provides an interface for developers to integrate Google’s generative models into their Python applications. It supports the [Gemini Developer API](https://ai.google.dev/gemini-api/docs) and [Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/overview) APIs.

## Installation[¶](#installation "Link to this heading")

```
pip install google-genai

```



## Imports[¶](#imports "Link to this heading")

```
from google import genai
from google.genai import types

```



## Create a client[¶](#create-a-client "Link to this heading")

Please run one of the following code blocks to create a client for
different services ([Gemini Developer API](https://ai.google.dev/gemini-api/docs) or [Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/overview)). Feel free to switch the client and
run all the examples to see how it behaves under different APIs.

```
# Only run this block for Gemini Developer API
client = genai.Client(api_key='GEMINI_API_KEY')

```


```
# Only run this block for Vertex AI API
client = genai.Client(
    vertexai=True, project='your-project-id', location='us-central1'
)

```

**(Optional) Using environment variables:**

You can create a client by configuring the necessary environment variables.
Configuration setup instructions depends on whether you’re using the Gemini
Developer API or the Gemini API in Vertex AI.

**Gemini Developer API:** Set GOOGLE\_API\_KEY as shown below:

```
export GOOGLE_API_KEY='your-api-key'

```

**Gemini API in Vertex AI:** Set GOOGLE\_GENAI\_USE\_VERTEXAI, GOOGLE\_CLOUD\_PROJECT
and GOOGLE\_CLOUD\_LOCATION, as shown below:

```
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT='your-project-id'
export GOOGLE_CLOUD_LOCATION='us-central1'

```


```
client = genai.Client()

```


### API Selection[¶](#api-selection "Link to this heading")

By default, the SDK uses the beta API endpoints provided by Google to support preview features in the APIs. The stable API endpoints can be selected by setting the API version to v1.

To set the API version use `http_options`. For example, to set the API version to `v1` for Vertex AI:

```
client = genai.Client(
    vertexai=True,
    project='your-project-id',
    location='us-central1',
    http_options=types.HttpOptions(api_version='v1')
)

```

To set the API version to v1alpha for the Gemini Developer API:

```
# Only run this block for Gemini Developer API
client = genai.Client(
    api_key='GEMINI_API_KEY',
    http_options=types.HttpOptions(api_version='v1alpha')
)

```




## Types[¶](#types "Link to this heading")

Parameter types can be specified as either dictionaries(`TypedDict`) or [Pydantic Models](https://pydantic.readthedocs.io/en/stable/model.html).
Pydantic model types are available in the `types` module.



# Models[¶](#models "Link to this heading")

The `client.models` modules exposes model inferencing and model
getters.

## Generate Content[¶](#generate-content "Link to this heading")

### with text content[¶](#with-text-content "Link to this heading")

```
response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents='Why is the sky blue?'
)
print(response.text)

```



### with uploaded file (Gemini Developer API only)[¶](#with-uploaded-file-gemini-developer-api-only "Link to this heading")

download the file in console.

```
!wget -q https://storage.googleapis.com/generativeai-downloads/data/a11.txt

```

python code.

```
file = client.files.upload(file='a11.txt')
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=['Could you summarize this file?', file]
)
print(response.text)

```



### How to structure contents argument for generate\_content[¶](#how-to-structure-contents-argument-for-generate-content "Link to this heading")

The SDK always converts the inputs to the contents argument into
list[types.Content].
The following shows some common ways to provide your inputs.

#### Provide a list[types.Content][¶](#provide-a-list-types-content "Link to this heading")

This is the canonical way to provide contents, SDK will not do any conversion.


#### Provide a types.Content instance[¶](#provide-a-types-content-instance "Link to this heading")

```
contents = types.Content(
role='user',
parts=[types.Part.from_text(text='Why is the sky blue?')]
)

```

SDK converts this to

```
[
types.Content(
    role='user',
    parts=[types.Part.from_text(text='Why is the sky blue?')]
)
]

```



#### Provide a string[¶](#provide-a-string "Link to this heading")

```
contents='Why is the sky blue?'

```

The SDK will assume this is a text part, and it converts this into the following:

```
[
types.UserContent(
    parts=[
    types.Part.from_text(text='Why is the sky blue?')
    ]
)
]

```

Where a types.UserContent is a subclass of types.Content, it sets the
role field to be user.


#### Provide a list of string[¶](#provide-a-list-of-string "Link to this heading")

The SDK assumes these are 2 text parts, it converts this into a single content,
like the following:

```
[
types.UserContent(
    parts=[
    types.Part.from_text(text='Why is the sky blue?'),
    types.Part.from_text(text='Why is the cloud white?'),
    ]
)
]

```

Where a types.UserContent is a subclass of types.Content, the
role field in types.UserContent is fixed to be user.


#### Provide a function call part[¶](#provide-a-function-call-part "Link to this heading")

```
contents = types.Part.from_function_call(
name='get_weather_by_location',
args={'location': 'Boston'}
)

```

The SDK converts a function call part to a content with a model role:

```
[
types.ModelContent(
    parts=[
    types.Part.from_function_call(
        name='get_weather_by_location',
        args={'location': 'Boston'}
    )
    ]
)
]

```

Where a types.ModelContent is a subclass of types.Content, the
role field in types.ModelContent is fixed to be model.


#### Provide a list of function call parts[¶](#provide-a-list-of-function-call-parts "Link to this heading")

```
contents = [
types.Part.from_function_call(
    name='get_weather_by_location',
    args={'location': 'Boston'}
),
types.Part.from_function_call(
    name='get_weather_by_location',
    args={'location': 'New York'}
),
]

```

The SDK converts a list of function call parts to the a content with a model role:

```
[
types.ModelContent(
    parts=[
    types.Part.from_function_call(
        name='get_weather_by_location',
        args={'location': 'Boston'}
    ),
    types.Part.from_function_call(
        name='get_weather_by_location',
        args={'location': 'New York'}
    )
    ]
)
]

```

Where a types.ModelContent is a subclass of types.Content, the
role field in types.ModelContent is fixed to be model.


#### Provide a non function call part[¶](#provide-a-non-function-call-part "Link to this heading")

```
contents = types.Part.from_uri(
file_uri: 'gs://generativeai-downloads/images/scones.jpg',
mime_type: 'image/jpeg',
)

```

The SDK converts all non function call parts into a content with a user role.

```
[
types.UserContent(parts=[
    types.Part.from_uri(
    file_uri: 'gs://generativeai-downloads/images/scones.jpg',
    mime_type: 'image/jpeg',
    )
])
]

```



#### Provide a list of non function call parts[¶](#provide-a-list-of-non-function-call-parts "Link to this heading")

```
contents = [
types.Part.from_text('What is this image about?'),
types.Part.from_uri(
    file_uri: 'gs://generativeai-downloads/images/scones.jpg',
    mime_type: 'image/jpeg',
)
]

```

The SDK will convert the list of parts into a content with a user role

```
[
types.UserContent(
    parts=[
    types.Part.from_text('What is this image about?'),
    types.Part.from_uri(
        file_uri: 'gs://generativeai-downloads/images/scones.jpg',
        mime_type: 'image/jpeg',
    )
    ]
)
]

```



#### Mix types in contents[¶](#mix-types-in-contents "Link to this heading")

You can also provide a list of types.ContentUnion. The SDK leaves items of
types.Content as is, it groups consecutive non function call parts into a
single types.UserContent, and it groups consecutive function call parts into
a single types.ModelContent.

If you put a list within a list, the inner list can only contain
types.PartUnion items. The SDK will convert the inner list into a single
types.UserContent.




## System Instructions and Other Configs[¶](#system-instructions-and-other-configs "Link to this heading")

The output of the model can be influenced by several optional settings
available in generate\_content’s config parameter. For example, the
variability and length of the output can be influenced by the temperature
and max\_output\_tokens respectively.

```
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='high',
    config=types.GenerateContentConfig(
        system_instruction='I say high, you say low',
        max_output_tokens=3,
        temperature=0.3,
    ),
)
print(response.text)

```



## Typed Config[¶](#typed-config "Link to this heading")

All API methods support Pydantic types for parameters as well as
dictionaries. You can get the type from `google.genai.types`.

```
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=types.Part.from_text(text='Why is the sky blue?'),
    config=types.GenerateContentConfig(
        temperature=0,
        top_p=0.95,
        top_k=20,
        candidate_count=1,
        seed=5,
        max_output_tokens=100,
        stop_sequences=['STOP!'],
        presence_penalty=0.0,
        frequency_penalty=0.0,
    ),
)

print(response.text)

```



## List Base Models[¶](#list-base-models "Link to this heading")

To retrieve tuned models, see: List Tuned Models

```
for model in client.models.list():
    print(model)

```


```
pager = client.models.list(config={'page_size': 10})
print(pager.page_size)
print(pager[0])
pager.next_page()
print(pager[0])

```


```
async for job in await client.aio.models.list():
    print(job)

```


```
async_pager = await client.aio.models.list(config={'page_size': 10})
print(async_pager.page_size)
print(async_pager[0])
await async_pager.next_page()
print(async_pager[0])

```



## Safety Settings[¶](#safety-settings "Link to this heading")

```
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='Say something bad.',
    config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category='HARM_CATEGORY_HATE_SPEECH',
                threshold='BLOCK_ONLY_HIGH',
            )
        ]
    ),
)
print(response.text)

```



## Function Calling[¶](#function-calling "Link to this heading")

You can pass a Python function directly and it will be automatically
called and responded.

```
def get_current_weather(location: str) -> str:
    """Returns the current weather.

    Args:
      location: The city and state, e.g. San Francisco, CA
    """
    return 'sunny'


response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='What is the weather like in Boston?',
    config=types.GenerateContentConfig(
        tools=[get_current_weather],
    ),
)

print(response.text)

```

If you pass in a python function as a tool directly, and do not want
automatic function calling, you can disable automatic function calling
as follows:

With automatic function calling disabled, you will get a list of function call
parts in the response:

If you don’t want to use the automatic function support, you can manually
declare the function and invoke it.

The following example shows how to declare a function and pass it as a tool.
Then you will receive a function call part in the response.

```
function = types.FunctionDeclaration(
    name='get_current_weather',
    description='Get the current weather in a given location',
    parameters=types.Schema(
        type='OBJECT',
        properties={
            'location': types.Schema(
                type='STRING',
                description='The city and state, e.g. San Francisco, CA',
            ),
        },
        required=['location'],
    ),
)

tool = types.Tool(function_declarations=[function])

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='What is the weather like in Boston?',
    config=types.GenerateContentConfig(
        tools=[tool],
    ),
)
print(response.function_calls[0])

```

After you receive the function call part from the model, you can invoke the function
and get the function response. And then you can pass the function response to
the model.
The following example shows how to do it for a simple function invocation.

```
user_prompt_content = types.Content(
    role='user',
    parts=[types.Part.from_text(text='What is the weather like in Boston?')],
)
function_call_part = response.function_calls[0]
function_call_content = response.candidates[0].content


try:
    function_result = get_current_weather(
        **function_call_part.function_call.args
    )
    function_response = {'result': function_result}
except (
    Exception
) as e:  # instead of raising the exception, you can let the model handle it
    function_response = {'error': str(e)}


function_response_part = types.Part.from_function_response(
    name=function_call_part.name,
    response=function_response,
)
function_response_content = types.Content(
    role='tool', parts=[function_response_part]
)

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=[
        user_prompt_content,
        function_call_content,
        function_response_content,
    ],
    config=types.GenerateContentConfig(
        tools=[tool],
    ),
)

print(response.text)

```

If you configure function calling mode to be ANY, then the model will always
return function call parts. If you also pass a python function as a tool, by
default the SDK will perform automatic function calling until the remote calls
exceed the maximum remote call for automatic function calling (default to 10 times).

If you’d like to disable automatic function calling in ANY mode:

```
def get_current_weather(location: str) -> str:
    """Returns the current weather.

    Args:
        location: The city and state, e.g. San Francisco, CA
    """
    return "sunny"

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents="What is the weather like in Boston?",
    config=types.GenerateContentConfig(
        tools=[get_current_weather],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),
        tool_config=types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(mode='ANY')
        ),
    ),
)

```

If you’d like to set `x` number of automatic function call turns, you can
configure the maximum remote calls to be `x + 1`.
Assuming you prefer `1` turn for automatic function calling:

```
def get_current_weather(location: str) -> str:
    """Returns the current weather.

    Args:
        location: The city and state, e.g. San Francisco, CA
    """
    return "sunny"

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents="What is the weather like in Boston?",
    config=types.GenerateContentConfig(
        tools=[get_current_weather],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            maximum_remote_calls=2
        ),
        tool_config=types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(mode='ANY')
        ),
    ),
)

```



## JSON Response Schema[¶](#json-response-schema "Link to this heading")

Schemas can be provided as Pydantic Models.

```
from pydantic import BaseModel


class CountryInfo(BaseModel):
    name: str
    population: int
    capital: str
    continent: str
    gdp: int
    official_language: str
    total_area_sq_mi: int


response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='Give me information for the United States.',
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema=CountryInfo,
    ),
)
print(response.text)

```


```
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='Give me information for the United States.',
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema={
            'required': [
                'name',
                'population',
                'capital',
                'continent',
                'gdp',
                'official_language',
                'total_area_sq_mi',
            ],
            'properties': {
                'name': {'type': 'STRING'},
                'population': {'type': 'INTEGER'},
                'capital': {'type': 'STRING'},
                'continent': {'type': 'STRING'},
                'gdp': {'type': 'INTEGER'},
                'official_language': {'type': 'STRING'},
                'total_area_sq_mi': {'type': 'INTEGER'},
            },
            'type': 'OBJECT',
        },
    ),
)
print(response.text)

```



## Enum Response Schema[¶](#enum-response-schema "Link to this heading")

You can set response\_mime\_type to ‘text/x.enum’ to return one of those enum
values as the response.

```
from enum import Enum

class InstrumentEnum(Enum):
    PERCUSSION = 'Percussion'
    STRING = 'String'
    WOODWIND = 'Woodwind'
    BRASS = 'Brass'
    KEYBOARD = 'Keyboard'

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='What instrument plays multiple notes at once?',
    config={
        'response_mime_type': 'text/x.enum',
        'response_schema': InstrumentEnum,
    },
)
print(response.text)

```

You can also set response\_mime\_type to ‘application/json’, the response will be
identical but in quotes.

```
class InstrumentEnum(Enum):
    PERCUSSION = 'Percussion'
    STRING = 'String'
    WOODWIND = 'Woodwind'
    BRASS = 'Brass'
    KEYBOARD = 'Keyboard'

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='What instrument plays multiple notes at once?',
    config={
        'response_mime_type': 'application/json',
        'response_schema': InstrumentEnum,
    },
)
print(response.text)

```



## Streaming[¶](#streaming "Link to this heading")

```
for chunk in client.models.generate_content_stream(
    model='gemini-2.0-flash-001', contents='Tell me a story in 300 words.'
):
    print(chunk.text, end='')

```

If your image is stored in [Google Cloud Storage](https://cloud.google.com/storage), you can use the from\_uri class method to create a Part object.

```
for chunk in client.models.generate_content_stream(
    model='gemini-2.0-flash-001',
    contents=[
        'What is this image about?',
        types.Part.from_uri(
            file_uri='gs://generativeai-downloads/images/scones.jpg',
            mime_type='image/jpeg',
        ),
    ],
):
    print(chunk.text, end='')

```

If your image is stored in your local file system, you can read it in as bytes
data and use the `from_bytes` class method to create a `Part` object.

```
YOUR_IMAGE_PATH = 'your_image_path'
YOUR_IMAGE_MIME_TYPE = 'your_image_mime_type'
with open(YOUR_IMAGE_PATH, 'rb') as f:
    image_bytes = f.read()

for chunk in client.models.generate_content_stream(
    model='gemini-2.0-flash-001',
    contents=[
        'What is this image about?',
        types.Part.from_bytes(data=image_bytes, mime_type=YOUR_IMAGE_MIME_TYPE),
    ],
):
    print(chunk.text, end='')

```



## Async[¶](#async "Link to this heading")

`client.aio` exposes all the analogous [async methods](https://docs.python.org/3/library/asyncio.html) that are available on `client`

For example, `client.aio.models.generate_content` is the `async` version of `client.models.generate_content`

```
response = await client.aio.models.generate_content(
    model='gemini-2.0-flash-001', contents='Tell me a story in 300 words.'
)

print(response.text)

```



## Streaming[¶](#id3 "Link to this heading")

```
async for chunk in await client.aio.models.generate_content_stream(
    model='gemini-2.0-flash-001', contents='Tell me a story in 300 words.'
):
    print(chunk.text, end='')

```



## Count Tokens and Compute Tokens[¶](#count-tokens-and-compute-tokens "Link to this heading")

```
response = client.models.count_tokens(
    model='gemini-2.0-flash-001',
    contents='why is the sky blue?',
)
print(response)

```

Compute tokens is only supported in Vertex AI.

```
response = client.models.compute_tokens(
    model='gemini-2.0-flash-001',
    contents='why is the sky blue?',
)
print(response)

```


### Async[¶](#id4 "Link to this heading")

```
response = await client.aio.models.count_tokens(
    model='gemini-2.0-flash-001',
    contents='why is the sky blue?',
)
print(response)

```




## Embed Content[¶](#embed-content "Link to this heading")

```
response = client.models.embed_content(
    model='text-embedding-004',
    contents='why is the sky blue?',
)
print(response)

```


```
# multiple contents with config
response = client.models.embed_content(
    model='text-embedding-004',
    contents=['why is the sky blue?', 'What is your age?'],
    config=types.EmbedContentConfig(output_dimensionality=10),
)

print(response)

```



## Imagen[¶](#imagen "Link to this heading")

Support for generate image in Gemini Developer API is behind an allowlist

```
# Generate Image
response1 = client.models.generate_images(
    model='imagen-3.0-generate-002',
    prompt='An umbrella in the foreground, and a rainy night sky in the background',
    config=types.GenerateImagesConfig(
        number_of_images=1,
        include_rai_reason=True,
        output_mime_type='image/jpeg',
    ),
)
response1.generated_images[0].image.show()

```

Upscale image is only supported in Vertex AI.

```
# Upscale the generated image from above
response2 = client.models.upscale_image(
    model='imagen-3.0-generate-002',
    image=response1.generated_images[0].image,
    upscale_factor='x2',
    config=types.UpscaleImageConfig(
        include_rai_reason=True,
        output_mime_type='image/jpeg',
    ),
)
response2.generated_images[0].image.show()

```

Edit image uses a separate model from generate and upscale.

Edit image is only supported in Vertex AI.

```
# Edit the generated image from above
from google.genai.types import RawReferenceImage, MaskReferenceImage

raw_ref_image = RawReferenceImage(
    reference_id=1,
    reference_image=response1.generated_images[0].image,
)

# Model computes a mask of the background
mask_ref_image = MaskReferenceImage(
    reference_id=2,
    config=types.MaskReferenceConfig(
        mask_mode='MASK_MODE_BACKGROUND',
        mask_dilation=0,
    ),
)

response3 = client.models.edit_image(
    model='imagen-3.0-capability-001',
    prompt='Sunlight and clear sky',
    reference_images=[raw_ref_image, mask_ref_image],
    config=types.EditImageConfig(
        edit_mode='EDIT_MODE_INPAINT_INSERTION',
        number_of_images=1,
        include_rai_reason=True,
        output_mime_type='image/jpeg',
    ),
)
response3.generated_images[0].image.show()

```



## Veo[¶](#veo "Link to this heading")

Support for generate videos in Vertex and Gemini Developer API is behind an allowlist

```
# Create operation
operation = client.models.generate_videos(
    model='veo-2.0-generate-001',
    prompt='A neon hologram of a cat driving at top speed',
    config=types.GenerateVideosConfig(
        number_of_videos=1,
        fps=24,
        duration_seconds=5,
        enhance_prompt=True,
    ),
)

# Poll operation
while not operation.done:
    time.sleep(20)
    operation = client.operations.get(operation)

video = operation.result.generated_videos[0].video
video.show()

```




# Chats[¶](#chats "Link to this heading")

Create a chat session to start a multi-turn conversations with the model.

## Send Message[¶](#send-message "Link to this heading")

```
chat = client.chats.create(model='gemini-2.0-flash-001')
response = chat.send_message('tell me a story')
print(response.text)

```



## Streaming[¶](#id5 "Link to this heading")

```
chat = client.chats.create(model='gemini-2.0-flash-001')
for chunk in chat.send_message_stream('tell me a story'):
    print(chunk.text, end='')

```



## Async[¶](#id6 "Link to this heading")

```
chat = client.aio.chats.create(model='gemini-2.0-flash-001')
response = await chat.send_message('tell me a story')
print(response.text)

```



## Async Streaming[¶](#async-streaming "Link to this heading")

```
chat = client.aio.chats.create(model='gemini-2.0-flash-001')
async for chunk in await chat.send_message_stream('tell me a story'):
    print(chunk.text, end='')

```




# Files[¶](#files "Link to this heading")

Files are only supported in Gemini Developer API.

```
gsutil cp gs://cloud-samples-data/generative-ai/pdf/2312.11805v3.pdf .
gsutil cp gs://cloud-samples-data/generative-ai/pdf/2403.05530.pdf .

```


## Upload[¶](#upload "Link to this heading")

```
file1 = client.files.upload(file='2312.11805v3.pdf')
file2 = client.files.upload(file='2403.05530.pdf')

print(file1)
print(file2)

```



## Get[¶](#get "Link to this heading")

```
file1 = client.files.upload(file='2312.11805v3.pdf')
file_info = client.files.get(name=file1.name)

```



## Delete[¶](#delete "Link to this heading")

```
file3 = client.files.upload(file='2312.11805v3.pdf')

client.files.delete(name=file3.name)

```




# Caches[¶](#caches "Link to this heading")

`client.caches` contains the control plane APIs for cached content

## Create[¶](#create "Link to this heading")

```
if client.vertexai:
    file_uris = [
        'gs://cloud-samples-data/generative-ai/pdf/2312.11805v3.pdf',
        'gs://cloud-samples-data/generative-ai/pdf/2403.05530.pdf',
    ]
else:
    file_uris = [file1.uri, file2.uri]

cached_content = client.caches.create(
    model='gemini-1.5-pro-002',
    config=types.CreateCachedContentConfig(
        contents=[
            types.Content(
                role='user',
                parts=[
                    types.Part.from_uri(
                        file_uri=file_uris[0], mime_type='application/pdf'
                    ),
                    types.Part.from_uri(
                        file_uri=file_uris[1],
                        mime_type='application/pdf',
                    ),
                ],
            )
        ],
        system_instruction='What is the sum of the two pdfs?',
        display_name='test cache',
        ttl='3600s',
    ),
)

```



## Get[¶](#id7 "Link to this heading")

```
cached_content = client.caches.get(name=cached_content.name)

```



## Generate Content[¶](#id8 "Link to this heading")

```
response = client.models.generate_content(
    model='gemini-1.5-pro-002',
    contents='Summarize the pdfs',
    config=types.GenerateContentConfig(
        cached_content=cached_content.name,
    ),
)
print(response.text)

```




# Tunings[¶](#tunings "Link to this heading")

`client.tunings` contains tuning job APIs and supports supervised fine
tuning through `tune`.

## Tune[¶](#tune "Link to this heading")

* Vertex AI supports tuning from GCS source
* Gemini Developer API supports tuning from inline examples

```
if client.vertexai:
    model = 'gemini-1.5-pro-002'
    training_dataset = types.TuningDataset(
        gcs_uri='gs://cloud-samples-data/ai-platform/generative_ai/gemini-1_5/text/sft_train_data.jsonl',
    )
else:
    model = 'models/gemini-1.0-pro-001'
    training_dataset = types.TuningDataset(
        examples=[
            types.TuningExample(
                text_input=f'Input text {i}',
                output=f'Output text {i}',
            )
            for i in range(5)
        ],
    )

```


```
tuning_job = client.tunings.tune(
    base_model=model,
    training_dataset=training_dataset,
    config=types.CreateTuningJobConfig(
        epoch_count=1, tuned_model_display_name='test_dataset_examples model'
    ),
)
print(tuning_job)

```



## Get Tuning Job[¶](#get-tuning-job "Link to this heading")

```
tuning_job = client.tunings.get(name=tuning_job.name)
print(tuning_job)

```


```
import time

running_states = set(
    [
        'JOB_STATE_PENDING',
        'JOB_STATE_RUNNING',
    ]
)

while tuning_job.state in running_states:
    print(tuning_job.state)
    tuning_job = client.tunings.get(name=tuning_job.name)
    time.sleep(10)

```


```
response = client.models.generate_content(
    model=tuning_job.tuned_model.endpoint,
    contents='why is the sky blue?',
)

print(response.text)

```



## Get Tuned Model[¶](#get-tuned-model "Link to this heading")

```
tuned_model = client.models.get(model=tuning_job.tuned_model.model)
print(tuned_model)

```



## List Tuned Models[¶](#list-tuned-models "Link to this heading")

To retrieve base models, see: List Base Models

```
for model in client.models.list(config={'page_size': 10, 'query_base': False}}):
    print(model)

```


```
pager = client.models.list(config={'page_size': 10, 'query_base': False}})
print(pager.page_size)
print(pager[0])
pager.next_page()
print(pager[0])

```


```
async for job in await client.aio.models.list(config={'page_size': 10, 'query_base': False}}):
    print(job)

```


```
async_pager = await client.aio.models.list(config={'page_size': 10, 'query_base': False}})
print(async_pager.page_size)
print(async_pager[0])
await async_pager.next_page()
print(async_pager[0])

```



## Update Tuned Model[¶](#update-tuned-model "Link to this heading")

```
model = pager[0]

model = client.models.update(
    model=model.name,
    config=types.UpdateModelConfig(
        display_name='my tuned model', description='my tuned model description'
    ),
)

print(model)

```



## List Tuning Jobs[¶](#list-tuning-jobs "Link to this heading")

```
for job in client.tunings.list(config={'page_size': 10}):
    print(job)

```


```
pager = client.tunings.list(config={'page_size': 10})
print(pager.page_size)
print(pager[0])
pager.next_page()
print(pager[0])

```


```
async for job in await client.aio.tunings.list(config={'page_size': 10}):
    print(job)

```


```
async_pager = await client.aio.tunings.list(config={'page_size': 10})
print(async_pager.page_size)
print(async_pager[0])
await async_pager.next_page()
print(async_pager[0])

```




# Batch Prediction[¶](#batch-prediction "Link to this heading")

Only supported in Vertex AI.

## Create[¶](#id9 "Link to this heading")

```
# Specify model and source file only, destination and job display name will be auto-populated
job = client.batches.create(
    model='gemini-1.5-flash-002',
    src='bq://my-project.my-dataset.my-table',
)

job

```


```
# Get a job by name
job = client.batches.get(name=job.name)

job.state

```


```
completed_states = set(
    [
        'JOB_STATE_SUCCEEDED',
        'JOB_STATE_FAILED',
        'JOB_STATE_CANCELLED',
        'JOB_STATE_PAUSED',
    ]
)

while job.state not in completed_states:
    print(job.state)
    job = client.batches.get(name=job.name)
    time.sleep(30)

job

```



## List[¶](#list "Link to this heading")

```
for job in client.batches.list(config=types.ListBatchJobsConfig(page_size=10)):
    print(job)

```


```
pager = client.batches.list(config=types.ListBatchJobsConfig(page_size=10))
print(pager.page_size)
print(pager[0])
pager.next_page()
print(pager[0])

```


```
async for job in await client.aio.batches.list(
    config=types.ListBatchJobsConfig(page_size=10)
):
    print(job)

```


```
async_pager = await client.aio.batches.list(
    config=types.ListBatchJobsConfig(page_size=10)
)
print(async_pager.page_size)
print(async_pager[0])
await async_pager.next_page()
print(async_pager[0])

```



## Delete[¶](#id10 "Link to this heading")

```
# Delete the job resource
delete_job = client.batches.delete(name=job.name)

delete_job

```




# Error Handling[¶](#error-handling "Link to this heading")

To handle errors raised by the model, the SDK provides this [APIError](<https://github.com/googleapis/python-genai/blob/main/google/genai/errors.py>) class.

```
try:
    client.models.generate_content(
        model="invalid-model-name",
        contents="What is your name?",
    )
except errors.APIError as e:
    print(e.code) # 404
    print(e.message)

```



# Reference[¶](#reference "Link to this heading")

* [Submodules](genai.html)
* [genai.client module](genai.html#module-genai.client)
  + [`AsyncClient`](genai.html#genai.client.AsyncClient)
    - [`AsyncClient.batches`](genai.html#genai.client.AsyncClient.batches)
    - [`AsyncClient.caches`](genai.html#genai.client.AsyncClient.caches)
    - [`AsyncClient.chats`](genai.html#genai.client.AsyncClient.chats)
    - [`AsyncClient.files`](genai.html#genai.client.AsyncClient.files)
    - [`AsyncClient.live`](genai.html#genai.client.AsyncClient.live)
    - [`AsyncClient.models`](genai.html#genai.client.AsyncClient.models)
    - [`AsyncClient.operations`](genai.html#genai.client.AsyncClient.operations)
    - [`AsyncClient.tunings`](genai.html#genai.client.AsyncClient.tunings)
  + [`Client`](genai.html#genai.client.Client)
    - [`Client.api_key`](genai.html#genai.client.Client.api_key)
    - [`Client.vertexai`](genai.html#genai.client.Client.vertexai)
    - [`Client.credentials`](genai.html#genai.client.Client.credentials)
    - [`Client.project`](genai.html#genai.client.Client.project)
    - [`Client.location`](genai.html#genai.client.Client.location)
    - [`Client.debug_config`](genai.html#genai.client.Client.debug_config)
    - [`Client.http_options`](genai.html#genai.client.Client.http_options)
    - [`Client.aio`](genai.html#genai.client.Client.aio)
    - [`Client.batches`](genai.html#genai.client.Client.batches)
    - [`Client.caches`](genai.html#genai.client.Client.caches)
    - [`Client.chats`](genai.html#genai.client.Client.chats)
    - [`Client.files`](genai.html#genai.client.Client.files)
    - [`Client.models`](genai.html#genai.client.Client.models)
    - [`Client.operations`](genai.html#genai.client.Client.operations)
    - [`Client.tunings`](genai.html#genai.client.Client.tunings)
    - [`Client.vertexai`](genai.html#id0)
  + [`DebugConfig`](genai.html#genai.client.DebugConfig)
    - [`DebugConfig.client_mode`](genai.html#genai.client.DebugConfig.client_mode)
    - [`DebugConfig.replay_id`](genai.html#genai.client.DebugConfig.replay_id)
    - [`DebugConfig.replays_directory`](genai.html#genai.client.DebugConfig.replays_directory)
* [genai.batches module](genai.html#module-genai.batches)
  + [`AsyncBatches`](genai.html#genai.batches.AsyncBatches)
    - [`AsyncBatches.cancel()`](genai.html#genai.batches.AsyncBatches.cancel)
    - [`AsyncBatches.create()`](genai.html#genai.batches.AsyncBatches.create)
    - [`AsyncBatches.delete()`](genai.html#genai.batches.AsyncBatches.delete)
    - [`AsyncBatches.get()`](genai.html#genai.batches.AsyncBatches.get)
    - [`AsyncBatches.list()`](genai.html#genai.batches.AsyncBatches.list)
  + [`Batches`](genai.html#genai.batches.Batches)
    - [`Batches.cancel()`](genai.html#genai.batches.Batches.cancel)
    - [`Batches.create()`](genai.html#genai.batches.Batches.create)
    - [`Batches.delete()`](genai.html#genai.batches.Batches.delete)
    - [`Batches.get()`](genai.html#genai.batches.Batches.get)
    - [`Batches.list()`](genai.html#genai.batches.Batches.list)
* [genai.caches module](genai.html#module-genai.caches)
  + [`AsyncCaches`](genai.html#genai.caches.AsyncCaches)
    - [`AsyncCaches.create()`](genai.html#genai.caches.AsyncCaches.create)
    - [`AsyncCaches.delete()`](genai.html#genai.caches.AsyncCaches.delete)
    - [`AsyncCaches.get()`](genai.html#genai.caches.AsyncCaches.get)
    - [`AsyncCaches.list()`](genai.html#genai.caches.AsyncCaches.list)
    - [`AsyncCaches.update()`](genai.html#genai.caches.AsyncCaches.update)
  + [`Caches`](genai.html#genai.caches.Caches)
    - [`Caches.create()`](genai.html#genai.caches.Caches.create)
    - [`Caches.delete()`](genai.html#genai.caches.Caches.delete)
    - [`Caches.get()`](genai.html#genai.caches.Caches.get)
    - [`Caches.list()`](genai.html#genai.caches.Caches.list)
    - [`Caches.update()`](genai.html#genai.caches.Caches.update)
* [genai.chats module](genai.html#module-genai.chats)
  + [`AsyncChat`](genai.html#genai.chats.AsyncChat)
    - [`AsyncChat.send_message()`](genai.html#genai.chats.AsyncChat.send_message)
    - [`AsyncChat.send_message_stream()`](genai.html#genai.chats.AsyncChat.send_message_stream)
  + [`AsyncChats`](genai.html#genai.chats.AsyncChats)
    - [`AsyncChats.create()`](genai.html#genai.chats.AsyncChats.create)
  + [`Chat`](genai.html#genai.chats.Chat)
    - [`Chat.send_message()`](genai.html#genai.chats.Chat.send_message)
    - [`Chat.send_message_stream()`](genai.html#genai.chats.Chat.send_message_stream)
  + [`Chats`](genai.html#genai.chats.Chats)
    - [`Chats.create()`](genai.html#genai.chats.Chats.create)
* [genai.files module](genai.html#module-genai.files)
  + [`AsyncFiles`](genai.html#genai.files.AsyncFiles)
    - [`AsyncFiles.delete()`](genai.html#genai.files.AsyncFiles.delete)
    - [`AsyncFiles.download()`](genai.html#genai.files.AsyncFiles.download)
    - [`AsyncFiles.get()`](genai.html#genai.files.AsyncFiles.get)
    - [`AsyncFiles.list()`](genai.html#genai.files.AsyncFiles.list)
    - [`AsyncFiles.upload()`](genai.html#genai.files.AsyncFiles.upload)
  + [`Files`](genai.html#genai.files.Files)
    - [`Files.delete()`](genai.html#genai.files.Files.delete)
    - [`Files.download()`](genai.html#genai.files.Files.download)
    - [`Files.get()`](genai.html#genai.files.Files.get)
    - [`Files.list()`](genai.html#genai.files.Files.list)
    - [`Files.upload()`](genai.html#genai.files.Files.upload)
* [genai.live module](genai.html#module-genai.live)
  + [`AsyncLive`](genai.html#genai.live.AsyncLive)
    - [`AsyncLive.connect()`](genai.html#genai.live.AsyncLive.connect)
  + [`AsyncSession`](genai.html#genai.live.AsyncSession)
    - [`AsyncSession.close()`](genai.html#genai.live.AsyncSession.close)
    - [`AsyncSession.receive()`](genai.html#genai.live.AsyncSession.receive)
    - [`AsyncSession.send()`](genai.html#genai.live.AsyncSession.send)
    - [`AsyncSession.send_client_content()`](genai.html#genai.live.AsyncSession.send_client_content)
    - [`AsyncSession.send_realtime_input()`](genai.html#genai.live.AsyncSession.send_realtime_input)
    - [`AsyncSession.send_tool_response()`](genai.html#genai.live.AsyncSession.send_tool_response)
    - [`AsyncSession.start_stream()`](genai.html#genai.live.AsyncSession.start_stream)
* [genai.models module](genai.html#module-genai.models)
  + [`AsyncModels`](genai.html#genai.models.AsyncModels)
    - [`AsyncModels.compute_tokens()`](genai.html#genai.models.AsyncModels.compute_tokens)
    - [`AsyncModels.count_tokens()`](genai.html#genai.models.AsyncModels.count_tokens)
    - [`AsyncModels.delete()`](genai.html#genai.models.AsyncModels.delete)
    - [`AsyncModels.edit_image()`](genai.html#genai.models.AsyncModels.edit_image)
    - [`AsyncModels.embed_content()`](genai.html#genai.models.AsyncModels.embed_content)
    - [`AsyncModels.generate_content()`](genai.html#genai.models.AsyncModels.generate_content)
    - [`AsyncModels.generate_content_stream()`](genai.html#genai.models.AsyncModels.generate_content_stream)
    - [`AsyncModels.generate_images()`](genai.html#genai.models.AsyncModels.generate_images)
    - [`AsyncModels.generate_videos()`](genai.html#genai.models.AsyncModels.generate_videos)
    - [`AsyncModels.get()`](genai.html#genai.models.AsyncModels.get)
    - [`AsyncModels.list()`](genai.html#genai.models.AsyncModels.list)
    - [`AsyncModels.update()`](genai.html#genai.models.AsyncModels.update)
    - [`AsyncModels.upscale_image()`](genai.html#genai.models.AsyncModels.upscale_image)
  + [`Models`](genai.html#genai.models.Models)
    - [`Models.compute_tokens()`](genai.html#genai.models.Models.compute_tokens)
    - [`Models.count_tokens()`](genai.html#genai.models.Models.count_tokens)
    - [`Models.delete()`](genai.html#genai.models.Models.delete)
    - [`Models.edit_image()`](genai.html#genai.models.Models.edit_image)
    - [`Models.embed_content()`](genai.html#genai.models.Models.embed_content)
    - [`Models.generate_content()`](genai.html#genai.models.Models.generate_content)
    - [`Models.generate_content_stream()`](genai.html#genai.models.Models.generate_content_stream)
    - [`Models.generate_images()`](genai.html#genai.models.Models.generate_images)
    - [`Models.generate_videos()`](genai.html#genai.models.Models.generate_videos)
    - [`Models.get()`](genai.html#genai.models.Models.get)
    - [`Models.list()`](genai.html#genai.models.Models.list)
    - [`Models.update()`](genai.html#genai.models.Models.update)
    - [`Models.upscale_image()`](genai.html#genai.models.Models.upscale_image)
* [genai.tunings module](genai.html#module-genai.tunings)
  + [`AsyncTunings`](genai.html#genai.tunings.AsyncTunings)
    - [`AsyncTunings.get()`](genai.html#genai.tunings.AsyncTunings.get)
    - [`AsyncTunings.list()`](genai.html#genai.tunings.AsyncTunings.list)
    - [`AsyncTunings.tune()`](genai.html#genai.tunings.AsyncTunings.tune)
  + [`Tunings`](genai.html#genai.tunings.Tunings)
    - [`Tunings.get()`](genai.html#genai.tunings.Tunings.get)
    - [`Tunings.list()`](genai.html#genai.tunings.Tunings.list)
    - [`Tunings.tune()`](genai.html#genai.tunings.Tunings.tune)
* [genai.types module](genai.html#module-genai.types)
  + [`ActivityEnd`](genai.html#genai.types.ActivityEnd)
  + [`ActivityEndDict`](genai.html#genai.types.ActivityEndDict)
  + [`ActivityHandling`](genai.html#genai.types.ActivityHandling)
    - [`ActivityHandling.ACTIVITY_HANDLING_UNSPECIFIED`](genai.html#genai.types.ActivityHandling.ACTIVITY_HANDLING_UNSPECIFIED)
    - [`ActivityHandling.NO_INTERRUPTION`](genai.html#genai.types.ActivityHandling.NO_INTERRUPTION)
    - [`ActivityHandling.START_OF_ACTIVITY_INTERRUPTS`](genai.html#genai.types.ActivityHandling.START_OF_ACTIVITY_INTERRUPTS)
  + [`ActivityStart`](genai.html#genai.types.ActivityStart)
  + [`ActivityStartDict`](genai.html#genai.types.ActivityStartDict)
  + [`AdapterSize`](genai.html#genai.types.AdapterSize)
    - [`AdapterSize.ADAPTER_SIZE_EIGHT`](genai.html#genai.types.AdapterSize.ADAPTER_SIZE_EIGHT)
    - [`AdapterSize.ADAPTER_SIZE_FOUR`](genai.html#genai.types.AdapterSize.ADAPTER_SIZE_FOUR)
    - [`AdapterSize.ADAPTER_SIZE_ONE`](genai.html#genai.types.AdapterSize.ADAPTER_SIZE_ONE)
    - [`AdapterSize.ADAPTER_SIZE_SIXTEEN`](genai.html#genai.types.AdapterSize.ADAPTER_SIZE_SIXTEEN)
    - [`AdapterSize.ADAPTER_SIZE_THIRTY_TWO`](genai.html#genai.types.AdapterSize.ADAPTER_SIZE_THIRTY_TWO)
    - [`AdapterSize.ADAPTER_SIZE_TWO`](genai.html#genai.types.AdapterSize.ADAPTER_SIZE_TWO)
    - [`AdapterSize.ADAPTER_SIZE_UNSPECIFIED`](genai.html#genai.types.AdapterSize.ADAPTER_SIZE_UNSPECIFIED)
  + [`AudioTranscriptionConfig`](genai.html#genai.types.AudioTranscriptionConfig)
  + [`AudioTranscriptionConfigDict`](genai.html#genai.types.AudioTranscriptionConfigDict)
  + [`AutomaticActivityDetection`](genai.html#genai.types.AutomaticActivityDetection)
    - [`AutomaticActivityDetection.disabled`](genai.html#genai.types.AutomaticActivityDetection.disabled)
    - [`AutomaticActivityDetection.end_of_speech_sensitivity`](genai.html#genai.types.AutomaticActivityDetection.end_of_speech_sensitivity)
    - [`AutomaticActivityDetection.prefix_padding_ms`](genai.html#genai.types.AutomaticActivityDetection.prefix_padding_ms)
    - [`AutomaticActivityDetection.silence_duration_ms`](genai.html#genai.types.AutomaticActivityDetection.silence_duration_ms)
    - [`AutomaticActivityDetection.start_of_speech_sensitivity`](genai.html#genai.types.AutomaticActivityDetection.start_of_speech_sensitivity)
  + [`AutomaticActivityDetectionDict`](genai.html#genai.types.AutomaticActivityDetectionDict)
    - [`AutomaticActivityDetectionDict.disabled`](genai.html#genai.types.AutomaticActivityDetectionDict.disabled)
    - [`AutomaticActivityDetectionDict.end_of_speech_sensitivity`](genai.html#genai.types.AutomaticActivityDetectionDict.end_of_speech_sensitivity)
    - [`AutomaticActivityDetectionDict.prefix_padding_ms`](genai.html#genai.types.AutomaticActivityDetectionDict.prefix_padding_ms)
    - [`AutomaticActivityDetectionDict.silence_duration_ms`](genai.html#genai.types.AutomaticActivityDetectionDict.silence_duration_ms)
    - [`AutomaticActivityDetectionDict.start_of_speech_sensitivity`](genai.html#genai.types.AutomaticActivityDetectionDict.start_of_speech_sensitivity)
  + [`AutomaticFunctionCallingConfig`](genai.html#genai.types.AutomaticFunctionCallingConfig)
    - [`AutomaticFunctionCallingConfig.disable`](genai.html#genai.types.AutomaticFunctionCallingConfig.disable)
    - [`AutomaticFunctionCallingConfig.ignore_call_history`](genai.html#genai.types.AutomaticFunctionCallingConfig.ignore_call_history)
    - [`AutomaticFunctionCallingConfig.maximum_remote_calls`](genai.html#genai.types.AutomaticFunctionCallingConfig.maximum_remote_calls)
  + [`AutomaticFunctionCallingConfigDict`](genai.html#genai.types.AutomaticFunctionCallingConfigDict)
    - [`AutomaticFunctionCallingConfigDict.disable`](genai.html#genai.types.AutomaticFunctionCallingConfigDict.disable)
    - [`AutomaticFunctionCallingConfigDict.ignore_call_history`](genai.html#genai.types.AutomaticFunctionCallingConfigDict.ignore_call_history)
    - [`AutomaticFunctionCallingConfigDict.maximum_remote_calls`](genai.html#genai.types.AutomaticFunctionCallingConfigDict.maximum_remote_calls)
  + [`BatchJob`](genai.html#genai.types.BatchJob)
    - [`BatchJob.create_time`](genai.html#genai.types.BatchJob.create_time)
    - [`BatchJob.dest`](genai.html#genai.types.BatchJob.dest)
    - [`BatchJob.display_name`](genai.html#genai.types.BatchJob.display_name)
    - [`BatchJob.end_time`](genai.html#genai.types.BatchJob.end_time)
    - [`BatchJob.error`](genai.html#genai.types.BatchJob.error)
    - [`BatchJob.model`](genai.html#genai.types.BatchJob.model)
    - [`BatchJob.name`](genai.html#genai.types.BatchJob.name)
    - [`BatchJob.src`](genai.html#genai.types.BatchJob.src)
    - [`BatchJob.start_time`](genai.html#genai.types.BatchJob.start_time)
    - [`BatchJob.state`](genai.html#genai.types.BatchJob.state)
    - [`BatchJob.update_time`](genai.html#genai.types.BatchJob.update_time)
  + [`BatchJobDestination`](genai.html#genai.types.BatchJobDestination)
    - [`BatchJobDestination.bigquery_uri`](genai.html#genai.types.BatchJobDestination.bigquery_uri)
    - [`BatchJobDestination.format`](genai.html#genai.types.BatchJobDestination.format)
    - [`BatchJobDestination.gcs_uri`](genai.html#genai.types.BatchJobDestination.gcs_uri)
  + [`BatchJobDestinationDict`](genai.html#genai.types.BatchJobDestinationDict)
    - [`BatchJobDestinationDict.bigquery_uri`](genai.html#genai.types.BatchJobDestinationDict.bigquery_uri)
    - [`BatchJobDestinationDict.format`](genai.html#genai.types.BatchJobDestinationDict.format)
    - [`BatchJobDestinationDict.gcs_uri`](genai.html#genai.types.BatchJobDestinationDict.gcs_uri)
  + [`BatchJobDict`](genai.html#genai.types.BatchJobDict)
    - [`BatchJobDict.create_time`](genai.html#genai.types.BatchJobDict.create_time)
    - [`BatchJobDict.dest`](genai.html#genai.types.BatchJobDict.dest)
    - [`BatchJobDict.display_name`](genai.html#genai.types.BatchJobDict.display_name)
    - [`BatchJobDict.end_time`](genai.html#genai.types.BatchJobDict.end_time)
    - [`BatchJobDict.error`](genai.html#genai.types.BatchJobDict.error)
    - [`BatchJobDict.model`](genai.html#genai.types.BatchJobDict.model)
    - [`BatchJobDict.name`](genai.html#genai.types.BatchJobDict.name)
    - [`BatchJobDict.src`](genai.html#genai.types.BatchJobDict.src)
    - [`BatchJobDict.start_time`](genai.html#genai.types.BatchJobDict.start_time)
    - [`BatchJobDict.state`](genai.html#genai.types.BatchJobDict.state)
    - [`BatchJobDict.update_time`](genai.html#genai.types.BatchJobDict.update_time)
  + [`BatchJobSource`](genai.html#genai.types.BatchJobSource)
    - [`BatchJobSource.bigquery_uri`](genai.html#genai.types.BatchJobSource.bigquery_uri)
    - [`BatchJobSource.format`](genai.html#genai.types.BatchJobSource.format)
    - [`BatchJobSource.gcs_uri`](genai.html#genai.types.BatchJobSource.gcs_uri)
  + [`BatchJobSourceDict`](genai.html#genai.types.BatchJobSourceDict)
    - [`BatchJobSourceDict.bigquery_uri`](genai.html#genai.types.BatchJobSourceDict.bigquery_uri)
    - [`BatchJobSourceDict.format`](genai.html#genai.types.BatchJobSourceDict.format)
    - [`BatchJobSourceDict.gcs_uri`](genai.html#genai.types.BatchJobSourceDict.gcs_uri)
  + [`Blob`](genai.html#genai.types.Blob)
    - [`Blob.data`](genai.html#genai.types.Blob.data)
    - [`Blob.mime_type`](genai.html#genai.types.Blob.mime_type)
  + [`BlobDict`](genai.html#genai.types.BlobDict)
    - [`BlobDict.data`](genai.html#genai.types.BlobDict.data)
    - [`BlobDict.mime_type`](genai.html#genai.types.BlobDict.mime_type)
  + [`BlockedReason`](genai.html#genai.types.BlockedReason)
    - [`BlockedReason.BLOCKED_REASON_UNSPECIFIED`](genai.html#genai.types.BlockedReason.BLOCKED_REASON_UNSPECIFIED)
    - [`BlockedReason.BLOCKLIST`](genai.html#genai.types.BlockedReason.BLOCKLIST)
    - [`BlockedReason.OTHER`](genai.html#genai.types.BlockedReason.OTHER)
    - [`BlockedReason.PROHIBITED_CONTENT`](genai.html#genai.types.BlockedReason.PROHIBITED_CONTENT)
    - [`BlockedReason.SAFETY`](genai.html#genai.types.BlockedReason.SAFETY)
  + [`CachedContent`](genai.html#genai.types.CachedContent)
    - [`CachedContent.create_time`](genai.html#genai.types.CachedContent.create_time)
    - [`CachedContent.display_name`](genai.html#genai.types.CachedContent.display_name)
    - [`CachedContent.expire_time`](genai.html#genai.types.CachedContent.expire_time)
    - [`CachedContent.model`](genai.html#genai.types.CachedContent.model)
    - [`CachedContent.name`](genai.html#genai.types.CachedContent.name)
    - [`CachedContent.update_time`](genai.html#genai.types.CachedContent.update_time)
    - [`CachedContent.usage_metadata`](genai.html#genai.types.CachedContent.usage_metadata)
  + [`CachedContentDict`](genai.html#genai.types.CachedContentDict)
    - [`CachedContentDict.create_time`](genai.html#genai.types.CachedContentDict.create_time)
    - [`CachedContentDict.display_name`](genai.html#genai.types.CachedContentDict.display_name)
    - [`CachedContentDict.expire_time`](genai.html#genai.types.CachedContentDict.expire_time)
    - [`CachedContentDict.model`](genai.html#genai.types.CachedContentDict.model)
    - [`CachedContentDict.name`](genai.html#genai.types.CachedContentDict.name)
    - [`CachedContentDict.update_time`](genai.html#genai.types.CachedContentDict.update_time)
    - [`CachedContentDict.usage_metadata`](genai.html#genai.types.CachedContentDict.usage_metadata)
  + [`CachedContentUsageMetadata`](genai.html#genai.types.CachedContentUsageMetadata)
    - [`CachedContentUsageMetadata.audio_duration_seconds`](genai.html#genai.types.CachedContentUsageMetadata.audio_duration_seconds)
    - [`CachedContentUsageMetadata.image_count`](genai.html#genai.types.CachedContentUsageMetadata.image_count)
    - [`CachedContentUsageMetadata.text_count`](genai.html#genai.types.CachedContentUsageMetadata.text_count)
    - [`CachedContentUsageMetadata.total_token_count`](genai.html#genai.types.CachedContentUsageMetadata.total_token_count)
    - [`CachedContentUsageMetadata.video_duration_seconds`](genai.html#genai.types.CachedContentUsageMetadata.video_duration_seconds)
  + [`CachedContentUsageMetadataDict`](genai.html#genai.types.CachedContentUsageMetadataDict)
    - [`CachedContentUsageMetadataDict.audio_duration_seconds`](genai.html#genai.types.CachedContentUsageMetadataDict.audio_duration_seconds)
    - [`CachedContentUsageMetadataDict.image_count`](genai.html#genai.types.CachedContentUsageMetadataDict.image_count)
    - [`CachedContentUsageMetadataDict.text_count`](genai.html#genai.types.CachedContentUsageMetadataDict.text_count)
    - [`CachedContentUsageMetadataDict.total_token_count`](genai.html#genai.types.CachedContentUsageMetadataDict.total_token_count)
    - [`CachedContentUsageMetadataDict.video_duration_seconds`](genai.html#genai.types.CachedContentUsageMetadataDict.video_duration_seconds)
  + [`CancelBatchJobConfig`](genai.html#genai.types.CancelBatchJobConfig)
    - [`CancelBatchJobConfig.http_options`](genai.html#genai.types.CancelBatchJobConfig.http_options)
  + [`CancelBatchJobConfigDict`](genai.html#genai.types.CancelBatchJobConfigDict)
    - [`CancelBatchJobConfigDict.http_options`](genai.html#genai.types.CancelBatchJobConfigDict.http_options)
  + [`Candidate`](genai.html#genai.types.Candidate)
    - [`Candidate.avg_logprobs`](genai.html#genai.types.Candidate.avg_logprobs)
    - [`Candidate.citation_metadata`](genai.html#genai.types.Candidate.citation_metadata)
    - [`Candidate.content`](genai.html#genai.types.Candidate.content)
    - [`Candidate.finish_message`](genai.html#genai.types.Candidate.finish_message)
    - [`Candidate.finish_reason`](genai.html#genai.types.Candidate.finish_reason)
    - [`Candidate.grounding_metadata`](genai.html#genai.types.Candidate.grounding_metadata)
    - [`Candidate.index`](genai.html#genai.types.Candidate.index)
    - [`Candidate.logprobs_result`](genai.html#genai.types.Candidate.logprobs_result)
    - [`Candidate.safety_ratings`](genai.html#genai.types.Candidate.safety_ratings)
    - [`Candidate.token_count`](genai.html#genai.types.Candidate.token_count)
  + [`CandidateDict`](genai.html#genai.types.CandidateDict)
    - [`CandidateDict.avg_logprobs`](genai.html#genai.types.CandidateDict.avg_logprobs)
    - [`CandidateDict.citation_metadata`](genai.html#genai.types.CandidateDict.citation_metadata)
    - [`CandidateDict.content`](genai.html#genai.types.CandidateDict.content)
    - [`CandidateDict.finish_message`](genai.html#genai.types.CandidateDict.finish_message)
    - [`CandidateDict.finish_reason`](genai.html#genai.types.CandidateDict.finish_reason)
    - [`CandidateDict.grounding_metadata`](genai.html#genai.types.CandidateDict.grounding_metadata)
    - [`CandidateDict.index`](genai.html#genai.types.CandidateDict.index)
    - [`CandidateDict.logprobs_result`](genai.html#genai.types.CandidateDict.logprobs_result)
    - [`CandidateDict.safety_ratings`](genai.html#genai.types.CandidateDict.safety_ratings)
    - [`CandidateDict.token_count`](genai.html#genai.types.CandidateDict.token_count)
  + [`Citation`](genai.html#genai.types.Citation)
    - [`Citation.end_index`](genai.html#genai.types.Citation.end_index)
    - [`Citation.license`](genai.html#genai.types.Citation.license)
    - [`Citation.publication_date`](genai.html#genai.types.Citation.publication_date)
    - [`Citation.start_index`](genai.html#genai.types.Citation.start_index)
    - [`Citation.title`](genai.html#genai.types.Citation.title)
    - [`Citation.uri`](genai.html#genai.types.Citation.uri)
  + [`CitationDict`](genai.html#genai.types.CitationDict)
    - [`CitationDict.end_index`](genai.html#genai.types.CitationDict.end_index)
    - [`CitationDict.license`](genai.html#genai.types.CitationDict.license)
    - [`CitationDict.publication_date`](genai.html#genai.types.CitationDict.publication_date)
    - [`CitationDict.start_index`](genai.html#genai.types.CitationDict.start_index)
    - [`CitationDict.title`](genai.html#genai.types.CitationDict.title)
    - [`CitationDict.uri`](genai.html#genai.types.CitationDict.uri)
  + [`CitationMetadata`](genai.html#genai.types.CitationMetadata)
    - [`CitationMetadata.citations`](genai.html#genai.types.CitationMetadata.citations)
  + [`CitationMetadataDict`](genai.html#genai.types.CitationMetadataDict)
    - [`CitationMetadataDict.citations`](genai.html#genai.types.CitationMetadataDict.citations)
  + [`CodeExecutionResult`](genai.html#genai.types.CodeExecutionResult)
    - [`CodeExecutionResult.outcome`](genai.html#genai.types.CodeExecutionResult.outcome)
    - [`CodeExecutionResult.output`](genai.html#genai.types.CodeExecutionResult.output)
  + [`CodeExecutionResultDict`](genai.html#genai.types.CodeExecutionResultDict)
    - [`CodeExecutionResultDict.outcome`](genai.html#genai.types.CodeExecutionResultDict.outcome)
    - [`CodeExecutionResultDict.output`](genai.html#genai.types.CodeExecutionResultDict.output)
  + [`ComputeTokensConfig`](genai.html#genai.types.ComputeTokensConfig)
    - [`ComputeTokensConfig.http_options`](genai.html#genai.types.ComputeTokensConfig.http_options)
  + [`ComputeTokensConfigDict`](genai.html#genai.types.ComputeTokensConfigDict)
    - [`ComputeTokensConfigDict.http_options`](genai.html#genai.types.ComputeTokensConfigDict.http_options)
  + [`ComputeTokensResponse`](genai.html#genai.types.ComputeTokensResponse)
    - [`ComputeTokensResponse.tokens_info`](genai.html#genai.types.ComputeTokensResponse.tokens_info)
  + [`ComputeTokensResponseDict`](genai.html#genai.types.ComputeTokensResponseDict)
    - [`ComputeTokensResponseDict.tokens_info`](genai.html#genai.types.ComputeTokensResponseDict.tokens_info)
  + [`Content`](genai.html#genai.types.Content)
    - [`Content.parts`](genai.html#genai.types.Content.parts)
    - [`Content.role`](genai.html#genai.types.Content.role)
  + [`ContentDict`](genai.html#genai.types.ContentDict)
    - [`ContentDict.parts`](genai.html#genai.types.ContentDict.parts)
    - [`ContentDict.role`](genai.html#genai.types.ContentDict.role)
  + [`ContentEmbedding`](genai.html#genai.types.ContentEmbedding)
    - [`ContentEmbedding.statistics`](genai.html#genai.types.ContentEmbedding.statistics)
    - [`ContentEmbedding.values`](genai.html#genai.types.ContentEmbedding.values)
  + [`ContentEmbeddingDict`](genai.html#genai.types.ContentEmbeddingDict)
    - [`ContentEmbeddingDict.statistics`](genai.html#genai.types.ContentEmbeddingDict.statistics)
  + [`ContentEmbeddingStatistics`](genai.html#genai.types.ContentEmbeddingStatistics)
    - [`ContentEmbeddingStatistics.token_count`](genai.html#genai.types.ContentEmbeddingStatistics.token_count)
    - [`ContentEmbeddingStatistics.truncated`](genai.html#genai.types.ContentEmbeddingStatistics.truncated)
  + [`ContentEmbeddingStatisticsDict`](genai.html#genai.types.ContentEmbeddingStatisticsDict)
    - [`ContentEmbeddingStatisticsDict.token_count`](genai.html#genai.types.ContentEmbeddingStatisticsDict.token_count)
    - [`ContentEmbeddingStatisticsDict.truncated`](genai.html#genai.types.ContentEmbeddingStatisticsDict.truncated)
  + [`ContextWindowCompressionConfig`](genai.html#genai.types.ContextWindowCompressionConfig)
    - [`ContextWindowCompressionConfig.sliding_window`](genai.html#genai.types.ContextWindowCompressionConfig.sliding_window)
    - [`ContextWindowCompressionConfig.trigger_tokens`](genai.html#genai.types.ContextWindowCompressionConfig.trigger_tokens)
  + [`ContextWindowCompressionConfigDict`](genai.html#genai.types.ContextWindowCompressionConfigDict)
    - [`ContextWindowCompressionConfigDict.sliding_window`](genai.html#genai.types.ContextWindowCompressionConfigDict.sliding_window)
    - [`ContextWindowCompressionConfigDict.trigger_tokens`](genai.html#genai.types.ContextWindowCompressionConfigDict.trigger_tokens)
  + [`ControlReferenceConfig`](genai.html#genai.types.ControlReferenceConfig)
    - [`ControlReferenceConfig.control_type`](genai.html#genai.types.ControlReferenceConfig.control_type)
    - [`ControlReferenceConfig.enable_control_image_computation`](genai.html#genai.types.ControlReferenceConfig.enable_control_image_computation)
  + [`ControlReferenceConfigDict`](genai.html#genai.types.ControlReferenceConfigDict)
    - [`ControlReferenceConfigDict.control_type`](genai.html#genai.types.ControlReferenceConfigDict.control_type)
    - [`ControlReferenceConfigDict.enable_control_image_computation`](genai.html#genai.types.ControlReferenceConfigDict.enable_control_image_computation)
  + [`ControlReferenceImage`](genai.html#genai.types.ControlReferenceImage)
    - [`ControlReferenceImage.config`](genai.html#genai.types.ControlReferenceImage.config)
    - [`ControlReferenceImage.control_image_config`](genai.html#genai.types.ControlReferenceImage.control_image_config)
    - [`ControlReferenceImage.reference_id`](genai.html#genai.types.ControlReferenceImage.reference_id)
    - [`ControlReferenceImage.reference_image`](genai.html#genai.types.ControlReferenceImage.reference_image)
    - [`ControlReferenceImage.reference_type`](genai.html#genai.types.ControlReferenceImage.reference_type)
  + [`ControlReferenceImageDict`](genai.html#genai.types.ControlReferenceImageDict)
    - [`ControlReferenceImageDict.config`](genai.html#genai.types.ControlReferenceImageDict.config)
    - [`ControlReferenceImageDict.reference_id`](genai.html#genai.types.ControlReferenceImageDict.reference_id)
    - [`ControlReferenceImageDict.reference_image`](genai.html#genai.types.ControlReferenceImageDict.reference_image)
    - [`ControlReferenceImageDict.reference_type`](genai.html#genai.types.ControlReferenceImageDict.reference_type)
  + [`ControlReferenceType`](genai.html#genai.types.ControlReferenceType)
    - [`ControlReferenceType.CONTROL_TYPE_CANNY`](genai.html#genai.types.ControlReferenceType.CONTROL_TYPE_CANNY)
    - [`ControlReferenceType.CONTROL_TYPE_DEFAULT`](genai.html#genai.types.ControlReferenceType.CONTROL_TYPE_DEFAULT)
    - [`ControlReferenceType.CONTROL_TYPE_FACE_MESH`](genai.html#genai.types.ControlReferenceType.CONTROL_TYPE_FACE_MESH)
    - [`ControlReferenceType.CONTROL_TYPE_SCRIBBLE`](genai.html#genai.types.ControlReferenceType.CONTROL_TYPE_SCRIBBLE)
  + [`CountTokensConfig`](genai.html#genai.types.CountTokensConfig)
    - [`CountTokensConfig.generation_config`](genai.html#genai.types.CountTokensConfig.generation_config)
    - [`CountTokensConfig.http_options`](genai.html#genai.types.CountTokensConfig.http_options)
    - [`CountTokensConfig.system_instruction`](genai.html#genai.types.CountTokensConfig.system_instruction)
    - [`CountTokensConfig.tools`](genai.html#genai.types.CountTokensConfig.tools)
  + [`CountTokensConfigDict`](genai.html#genai.types.CountTokensConfigDict)
    - [`CountTokensConfigDict.generation_config`](genai.html#genai.types.CountTokensConfigDict.generation_config)
    - [`CountTokensConfigDict.http_options`](genai.html#genai.types.CountTokensConfigDict.http_options)
    - [`CountTokensConfigDict.system_instruction`](genai.html#genai.types.CountTokensConfigDict.system_instruction)
    - [`CountTokensConfigDict.tools`](genai.html#genai.types.CountTokensConfigDict.tools)
  + [`CountTokensResponse`](genai.html#genai.types.CountTokensResponse)
    - [`CountTokensResponse.cached_content_token_count`](genai.html#genai.types.CountTokensResponse.cached_content_token_count)
    - [`CountTokensResponse.total_tokens`](genai.html#genai.types.CountTokensResponse.total_tokens)
  + [`CountTokensResponseDict`](genai.html#genai.types.CountTokensResponseDict)
    - [`CountTokensResponseDict.cached_content_token_count`](genai.html#genai.types.CountTokensResponseDict.cached_content_token_count)
    - [`CountTokensResponseDict.total_tokens`](genai.html#genai.types.CountTokensResponseDict.total_tokens)
  + [`CreateBatchJobConfig`](genai.html#genai.types.CreateBatchJobConfig)
    - [`CreateBatchJobConfig.dest`](genai.html#genai.types.CreateBatchJobConfig.dest)
    - [`CreateBatchJobConfig.display_name`](genai.html#genai.types.CreateBatchJobConfig.display_name)
    - [`CreateBatchJobConfig.http_options`](genai.html#genai.types.CreateBatchJobConfig.http_options)
  + [`CreateBatchJobConfigDict`](genai.html#genai.types.CreateBatchJobConfigDict)
    - [`CreateBatchJobConfigDict.dest`](genai.html#genai.types.CreateBatchJobConfigDict.dest)
    - [`CreateBatchJobConfigDict.display_name`](genai.html#genai.types.CreateBatchJobConfigDict.display_name)
    - [`CreateBatchJobConfigDict.http_options`](genai.html#genai.types.CreateBatchJobConfigDict.http_options)
  + [`CreateCachedContentConfig`](genai.html#genai.types.CreateCachedContentConfig)
    - [`CreateCachedContentConfig.contents`](genai.html#genai.types.CreateCachedContentConfig.contents)
    - [`CreateCachedContentConfig.display_name`](genai.html#genai.types.CreateCachedContentConfig.display_name)
    - [`CreateCachedContentConfig.expire_time`](genai.html#genai.types.CreateCachedContentConfig.expire_time)
    - [`CreateCachedContentConfig.http_options`](genai.html#genai.types.CreateCachedContentConfig.http_options)
    - [`CreateCachedContentConfig.system_instruction`](genai.html#genai.types.CreateCachedContentConfig.system_instruction)
    - [`CreateCachedContentConfig.tool_config`](genai.html#genai.types.CreateCachedContentConfig.tool_config)
    - [`CreateCachedContentConfig.tools`](genai.html#genai.types.CreateCachedContentConfig.tools)
    - [`CreateCachedContentConfig.ttl`](genai.html#genai.types.CreateCachedContentConfig.ttl)
  + [`CreateCachedContentConfigDict`](genai.html#genai.types.CreateCachedContentConfigDict)
    - [`CreateCachedContentConfigDict.contents`](genai.html#genai.types.CreateCachedContentConfigDict.contents)
    - [`CreateCachedContentConfigDict.display_name`](genai.html#genai.types.CreateCachedContentConfigDict.display_name)
    - [`CreateCachedContentConfigDict.expire_time`](genai.html#genai.types.CreateCachedContentConfigDict.expire_time)
    - [`CreateCachedContentConfigDict.http_options`](genai.html#genai.types.CreateCachedContentConfigDict.http_options)
    - [`CreateCachedContentConfigDict.system_instruction`](genai.html#genai.types.CreateCachedContentConfigDict.system_instruction)
    - [`CreateCachedContentConfigDict.tool_config`](genai.html#genai.types.CreateCachedContentConfigDict.tool_config)
    - [`CreateCachedContentConfigDict.tools`](genai.html#genai.types.CreateCachedContentConfigDict.tools)
    - [`CreateCachedContentConfigDict.ttl`](genai.html#genai.types.CreateCachedContentConfigDict.ttl)
  + [`CreateFileConfig`](genai.html#genai.types.CreateFileConfig)
    - [`CreateFileConfig.http_options`](genai.html#genai.types.CreateFileConfig.http_options)
  + [`CreateFileConfigDict`](genai.html#genai.types.CreateFileConfigDict)
    - [`CreateFileConfigDict.http_options`](genai.html#genai.types.CreateFileConfigDict.http_options)
  + [`CreateFileResponse`](genai.html#genai.types.CreateFileResponse)
    - [`CreateFileResponse.http_headers`](genai.html#genai.types.CreateFileResponse.http_headers)
  + [`CreateFileResponseDict`](genai.html#genai.types.CreateFileResponseDict)
    - [`CreateFileResponseDict.http_headers`](genai.html#genai.types.CreateFileResponseDict.http_headers)
  + [`CreateTuningJobConfig`](genai.html#genai.types.CreateTuningJobConfig)
    - [`CreateTuningJobConfig.adapter_size`](genai.html#genai.types.CreateTuningJobConfig.adapter_size)
    - [`CreateTuningJobConfig.batch_size`](genai.html#genai.types.CreateTuningJobConfig.batch_size)
    - [`CreateTuningJobConfig.description`](genai.html#genai.types.CreateTuningJobConfig.description)
    - [`CreateTuningJobConfig.epoch_count`](genai.html#genai.types.CreateTuningJobConfig.epoch_count)
    - [`CreateTuningJobConfig.http_options`](genai.html#genai.types.CreateTuningJobConfig.http_options)
    - [`CreateTuningJobConfig.learning_rate`](genai.html#genai.types.CreateTuningJobConfig.learning_rate)
    - [`CreateTuningJobConfig.learning_rate_multiplier`](genai.html#genai.types.CreateTuningJobConfig.learning_rate_multiplier)
    - [`CreateTuningJobConfig.tuned_model_display_name`](genai.html#genai.types.CreateTuningJobConfig.tuned_model_display_name)
    - [`CreateTuningJobConfig.validation_dataset`](genai.html#genai.types.CreateTuningJobConfig.validation_dataset)
  + [`CreateTuningJobConfigDict`](genai.html#genai.types.CreateTuningJobConfigDict)
    - [`CreateTuningJobConfigDict.adapter_size`](genai.html#genai.types.CreateTuningJobConfigDict.adapter_size)
    - [`CreateTuningJobConfigDict.batch_size`](genai.html#genai.types.CreateTuningJobConfigDict.batch_size)
    - [`CreateTuningJobConfigDict.description`](genai.html#genai.types.CreateTuningJobConfigDict.description)
    - [`CreateTuningJobConfigDict.epoch_count`](genai.html#genai.types.CreateTuningJobConfigDict.epoch_count)
    - [`CreateTuningJobConfigDict.http_options`](genai.html#genai.types.CreateTuningJobConfigDict.http_options)
    - [`CreateTuningJobConfigDict.learning_rate`](genai.html#genai.types.CreateTuningJobConfigDict.learning_rate)
    - [`CreateTuningJobConfigDict.learning_rate_multiplier`](genai.html#genai.types.CreateTuningJobConfigDict.learning_rate_multiplier)
    - [`CreateTuningJobConfigDict.tuned_model_display_name`](genai.html#genai.types.CreateTuningJobConfigDict.tuned_model_display_name)
    - [`CreateTuningJobConfigDict.validation_dataset`](genai.html#genai.types.CreateTuningJobConfigDict.validation_dataset)
  + [`DatasetDistribution`](genai.html#genai.types.DatasetDistribution)
    - [`DatasetDistribution.buckets`](genai.html#genai.types.DatasetDistribution.buckets)
    - [`DatasetDistribution.max`](genai.html#genai.types.DatasetDistribution.max)
    - [`DatasetDistribution.mean`](genai.html#genai.types.DatasetDistribution.mean)
    - [`DatasetDistribution.median`](genai.html#genai.types.DatasetDistribution.median)
    - [`DatasetDistribution.min`](genai.html#genai.types.DatasetDistribution.min)
    - [`DatasetDistribution.p5`](genai.html#genai.types.DatasetDistribution.p5)
    - [`DatasetDistribution.p95`](genai.html#genai.types.DatasetDistribution.p95)
    - [`DatasetDistribution.sum`](genai.html#genai.types.DatasetDistribution.sum)
  + [`DatasetDistributionDict`](genai.html#genai.types.DatasetDistributionDict)
    - [`DatasetDistributionDict.buckets`](genai.html#genai.types.DatasetDistributionDict.buckets)
    - [`DatasetDistributionDict.max`](genai.html#genai.types.DatasetDistributionDict.max)
    - [`DatasetDistributionDict.mean`](genai.html#genai.types.DatasetDistributionDict.mean)
    - [`DatasetDistributionDict.median`](genai.html#genai.types.DatasetDistributionDict.median)
    - [`DatasetDistributionDict.min`](genai.html#genai.types.DatasetDistributionDict.min)
    - [`DatasetDistributionDict.p5`](genai.html#genai.types.DatasetDistributionDict.p5)
    - [`DatasetDistributionDict.p95`](genai.html#genai.types.DatasetDistributionDict.p95)
    - [`DatasetDistributionDict.sum`](genai.html#genai.types.DatasetDistributionDict.sum)
  + [`DatasetDistributionDistributionBucket`](genai.html#genai.types.DatasetDistributionDistributionBucket)
    - [`DatasetDistributionDistributionBucket.count`](genai.html#genai.types.DatasetDistributionDistributionBucket.count)
    - [`DatasetDistributionDistributionBucket.left`](genai.html#genai.types.DatasetDistributionDistributionBucket.left)
    - [`DatasetDistributionDistributionBucket.right`](genai.html#genai.types.DatasetDistributionDistributionBucket.right)
  + [`DatasetDistributionDistributionBucketDict`](genai.html#genai.types.DatasetDistributionDistributionBucketDict)
    - [`DatasetDistributionDistributionBucketDict.count`](genai.html#genai.types.DatasetDistributionDistributionBucketDict.count)
    - [`DatasetDistributionDistributionBucketDict.left`](genai.html#genai.types.DatasetDistributionDistributionBucketDict.left)
    - [`DatasetDistributionDistributionBucketDict.right`](genai.html#genai.types.DatasetDistributionDistributionBucketDict.right)
  + [`DatasetStats`](genai.html#genai.types.DatasetStats)
    - [`DatasetStats.total_billable_character_count`](genai.html#genai.types.DatasetStats.total_billable_character_count)
    - [`DatasetStats.total_tuning_character_count`](genai.html#genai.types.DatasetStats.total_tuning_character_count)
    - [`DatasetStats.tuning_dataset_example_count`](genai.html#genai.types.DatasetStats.tuning_dataset_example_count)
    - [`DatasetStats.tuning_step_count`](genai.html#genai.types.DatasetStats.tuning_step_count)
    - [`DatasetStats.user_dataset_examples`](genai.html#genai.types.DatasetStats.user_dataset_examples)
    - [`DatasetStats.user_input_token_distribution`](genai.html#genai.types.DatasetStats.user_input_token_distribution)
    - [`DatasetStats.user_message_per_example_distribution`](genai.html#genai.types.DatasetStats.user_message_per_example_distribution)
    - [`DatasetStats.user_output_token_distribution`](genai.html#genai.types.DatasetStats.user_output_token_distribution)
  + [`DatasetStatsDict`](genai.html#genai.types.DatasetStatsDict)
    - [`DatasetStatsDict.total_billable_character_count`](genai.html#genai.types.DatasetStatsDict.total_billable_character_count)
    - [`DatasetStatsDict.total_tuning_character_count`](genai.html#genai.types.DatasetStatsDict.total_tuning_character_count)
    - [`DatasetStatsDict.tuning_dataset_example_count`](genai.html#genai.types.DatasetStatsDict.tuning_dataset_example_count)
    - [`DatasetStatsDict.tuning_step_count`](genai.html#genai.types.DatasetStatsDict.tuning_step_count)
    - [`DatasetStatsDict.user_dataset_examples`](genai.html#genai.types.DatasetStatsDict.user_dataset_examples)
    - [`DatasetStatsDict.user_input_token_distribution`](genai.html#genai.types.DatasetStatsDict.user_input_token_distribution)
    - [`DatasetStatsDict.user_message_per_example_distribution`](genai.html#genai.types.DatasetStatsDict.user_message_per_example_distribution)
    - [`DatasetStatsDict.user_output_token_distribution`](genai.html#genai.types.DatasetStatsDict.user_output_token_distribution)
  + [`DeleteBatchJobConfig`](genai.html#genai.types.DeleteBatchJobConfig)
    - [`DeleteBatchJobConfig.http_options`](genai.html#genai.types.DeleteBatchJobConfig.http_options)
  + [`DeleteBatchJobConfigDict`](genai.html#genai.types.DeleteBatchJobConfigDict)
    - [`DeleteBatchJobConfigDict.http_options`](genai.html#genai.types.DeleteBatchJobConfigDict.http_options)
  + [`DeleteCachedContentConfig`](genai.html#genai.types.DeleteCachedContentConfig)
    - [`DeleteCachedContentConfig.http_options`](genai.html#genai.types.DeleteCachedContentConfig.http_options)
  + [`DeleteCachedContentConfigDict`](genai.html#genai.types.DeleteCachedContentConfigDict)
    - [`DeleteCachedContentConfigDict.http_options`](genai.html#genai.types.DeleteCachedContentConfigDict.http_options)
  + [`DeleteCachedContentResponse`](genai.html#genai.types.DeleteCachedContentResponse)
  + [`DeleteCachedContentResponseDict`](genai.html#genai.types.DeleteCachedContentResponseDict)
  + [`DeleteFileConfig`](genai.html#genai.types.DeleteFileConfig)
    - [`DeleteFileConfig.http_options`](genai.html#genai.types.DeleteFileConfig.http_options)
  + [`DeleteFileConfigDict`](genai.html#genai.types.DeleteFileConfigDict)
    - [`DeleteFileConfigDict.http_options`](genai.html#genai.types.DeleteFileConfigDict.http_options)
  + [`DeleteFileResponse`](genai.html#genai.types.DeleteFileResponse)
  + [`DeleteFileResponseDict`](genai.html#genai.types.DeleteFileResponseDict)
  + [`DeleteModelConfig`](genai.html#genai.types.DeleteModelConfig)
    - [`DeleteModelConfig.http_options`](genai.html#genai.types.DeleteModelConfig.http_options)
  + [`DeleteModelConfigDict`](genai.html#genai.types.DeleteModelConfigDict)
    - [`DeleteModelConfigDict.http_options`](genai.html#genai.types.DeleteModelConfigDict.http_options)
  + [`DeleteModelResponse`](genai.html#genai.types.DeleteModelResponse)
  + [`DeleteModelResponseDict`](genai.html#genai.types.DeleteModelResponseDict)
  + [`DeleteResourceJob`](genai.html#genai.types.DeleteResourceJob)
    - [`DeleteResourceJob.done`](genai.html#genai.types.DeleteResourceJob.done)
    - [`DeleteResourceJob.error`](genai.html#genai.types.DeleteResourceJob.error)
    - [`DeleteResourceJob.name`](genai.html#genai.types.DeleteResourceJob.name)
  + [`DeleteResourceJobDict`](genai.html#genai.types.DeleteResourceJobDict)
    - [`DeleteResourceJobDict.done`](genai.html#genai.types.DeleteResourceJobDict.done)
    - [`DeleteResourceJobDict.error`](genai.html#genai.types.DeleteResourceJobDict.error)
    - [`DeleteResourceJobDict.name`](genai.html#genai.types.DeleteResourceJobDict.name)
  + [`DistillationDataStats`](genai.html#genai.types.DistillationDataStats)
    - [`DistillationDataStats.training_dataset_stats`](genai.html#genai.types.DistillationDataStats.training_dataset_stats)
  + [`DistillationDataStatsDict`](genai.html#genai.types.DistillationDataStatsDict)
    - [`DistillationDataStatsDict.training_dataset_stats`](genai.html#genai.types.DistillationDataStatsDict.training_dataset_stats)
  + [`DistillationHyperParameters`](genai.html#genai.types.DistillationHyperParameters)
    - [`DistillationHyperParameters.adapter_size`](genai.html#genai.types.DistillationHyperParameters.adapter_size)
    - [`DistillationHyperParameters.epoch_count`](genai.html#genai.types.DistillationHyperParameters.epoch_count)
    - [`DistillationHyperParameters.learning_rate_multiplier`](genai.html#genai.types.DistillationHyperParameters.learning_rate_multiplier)
  + [`DistillationHyperParametersDict`](genai.html#genai.types.DistillationHyperParametersDict)
    - [`DistillationHyperParametersDict.adapter_size`](genai.html#genai.types.DistillationHyperParametersDict.adapter_size)
    - [`DistillationHyperParametersDict.epoch_count`](genai.html#genai.types.DistillationHyperParametersDict.epoch_count)
    - [`DistillationHyperParametersDict.learning_rate_multiplier`](genai.html#genai.types.DistillationHyperParametersDict.learning_rate_multiplier)
  + [`DistillationSpec`](genai.html#genai.types.DistillationSpec)
    - [`DistillationSpec.base_teacher_model`](genai.html#genai.types.DistillationSpec.base_teacher_model)
    - [`DistillationSpec.hyper_parameters`](genai.html#genai.types.DistillationSpec.hyper_parameters)
    - [`DistillationSpec.pipeline_root_directory`](genai.html#genai.types.DistillationSpec.pipeline_root_directory)
    - [`DistillationSpec.student_model`](genai.html#genai.types.DistillationSpec.student_model)
    - [`DistillationSpec.training_dataset_uri`](genai.html#genai.types.DistillationSpec.training_dataset_uri)
    - [`DistillationSpec.tuned_teacher_model_source`](genai.html#genai.types.DistillationSpec.tuned_teacher_model_source)
    - [`DistillationSpec.validation_dataset_uri`](genai.html#genai.types.DistillationSpec.validation_dataset_uri)
  + [`DistillationSpecDict`](genai.html#genai.types.DistillationSpecDict)
    - [`DistillationSpecDict.base_teacher_model`](genai.html#genai.types.DistillationSpecDict.base_teacher_model)
    - [`DistillationSpecDict.hyper_parameters`](genai.html#genai.types.DistillationSpecDict.hyper_parameters)
    - [`DistillationSpecDict.pipeline_root_directory`](genai.html#genai.types.DistillationSpecDict.pipeline_root_directory)
    - [`DistillationSpecDict.student_model`](genai.html#genai.types.DistillationSpecDict.student_model)
    - [`DistillationSpecDict.training_dataset_uri`](genai.html#genai.types.DistillationSpecDict.training_dataset_uri)
    - [`DistillationSpecDict.tuned_teacher_model_source`](genai.html#genai.types.DistillationSpecDict.tuned_teacher_model_source)
    - [`DistillationSpecDict.validation_dataset_uri`](genai.html#genai.types.DistillationSpecDict.validation_dataset_uri)
  + [`DownloadFileConfig`](genai.html#genai.types.DownloadFileConfig)
    - [`DownloadFileConfig.http_options`](genai.html#genai.types.DownloadFileConfig.http_options)
  + [`DownloadFileConfigDict`](genai.html#genai.types.DownloadFileConfigDict)
    - [`DownloadFileConfigDict.http_options`](genai.html#genai.types.DownloadFileConfigDict.http_options)
  + [`DynamicRetrievalConfig`](genai.html#genai.types.DynamicRetrievalConfig)
    - [`DynamicRetrievalConfig.dynamic_threshold`](genai.html#genai.types.DynamicRetrievalConfig.dynamic_threshold)
    - [`DynamicRetrievalConfig.mode`](genai.html#genai.types.DynamicRetrievalConfig.mode)
  + [`DynamicRetrievalConfigDict`](genai.html#genai.types.DynamicRetrievalConfigDict)
    - [`DynamicRetrievalConfigDict.dynamic_threshold`](genai.html#genai.types.DynamicRetrievalConfigDict.dynamic_threshold)
    - [`DynamicRetrievalConfigDict.mode`](genai.html#genai.types.DynamicRetrievalConfigDict.mode)
  + [`DynamicRetrievalConfigMode`](genai.html#genai.types.DynamicRetrievalConfigMode)
    - [`DynamicRetrievalConfigMode.MODE_DYNAMIC`](genai.html#genai.types.DynamicRetrievalConfigMode.MODE_DYNAMIC)
    - [`DynamicRetrievalConfigMode.MODE_UNSPECIFIED`](genai.html#genai.types.DynamicRetrievalConfigMode.MODE_UNSPECIFIED)
  + [`EditImageConfig`](genai.html#genai.types.EditImageConfig)
    - [`EditImageConfig.aspect_ratio`](genai.html#genai.types.EditImageConfig.aspect_ratio)
    - [`EditImageConfig.base_steps`](genai.html#genai.types.EditImageConfig.base_steps)
    - [`EditImageConfig.edit_mode`](genai.html#genai.types.EditImageConfig.edit_mode)
    - [`EditImageConfig.guidance_scale`](genai.html#genai.types.EditImageConfig.guidance_scale)
    - [`EditImageConfig.http_options`](genai.html#genai.types.EditImageConfig.http_options)
    - [`EditImageConfig.include_rai_reason`](genai.html#genai.types.EditImageConfig.include_rai_reason)
    - [`EditImageConfig.include_safety_attributes`](genai.html#genai.types.EditImageConfig.include_safety_attributes)
    - [`EditImageConfig.language`](genai.html#genai.types.EditImageConfig.language)
    - [`EditImageConfig.negative_prompt`](genai.html#genai.types.EditImageConfig.negative_prompt)
    - [`EditImageConfig.number_of_images`](genai.html#genai.types.EditImageConfig.number_of_images)
    - [`EditImageConfig.output_compression_quality`](genai.html#genai.types.EditImageConfig.output_compression_quality)
    - [`EditImageConfig.output_gcs_uri`](genai.html#genai.types.EditImageConfig.output_gcs_uri)
    - [`EditImageConfig.output_mime_type`](genai.html#genai.types.EditImageConfig.output_mime_type)
    - [`EditImageConfig.person_generation`](genai.html#genai.types.EditImageConfig.person_generation)
    - [`EditImageConfig.safety_filter_level`](genai.html#genai.types.EditImageConfig.safety_filter_level)
    - [`EditImageConfig.seed`](genai.html#genai.types.EditImageConfig.seed)
  + [`EditImageConfigDict`](genai.html#genai.types.EditImageConfigDict)
    - [`EditImageConfigDict.aspect_ratio`](genai.html#genai.types.EditImageConfigDict.aspect_ratio)
    - [`EditImageConfigDict.base_steps`](genai.html#genai.types.EditImageConfigDict.base_steps)
    - [`EditImageConfigDict.edit_mode`](genai.html#genai.types.EditImageConfigDict.edit_mode)
    - [`EditImageConfigDict.guidance_scale`](genai.html#genai.types.EditImageConfigDict.guidance_scale)
    - [`EditImageConfigDict.http_options`](genai.html#genai.types.EditImageConfigDict.http_options)
    - [`EditImageConfigDict.include_rai_reason`](genai.html#genai.types.EditImageConfigDict.include_rai_reason)
    - [`EditImageConfigDict.include_safety_attributes`](genai.html#genai.types.EditImageConfigDict.include_safety_attributes)
    - [`EditImageConfigDict.language`](genai.html#genai.types.EditImageConfigDict.language)
    - [`EditImageConfigDict.negative_prompt`](genai.html#genai.types.EditImageConfigDict.negative_prompt)
    - [`EditImageConfigDict.number_of_images`](genai.html#genai.types.EditImageConfigDict.number_of_images)
    - [`EditImageConfigDict.output_compression_quality`](genai.html#genai.types.EditImageConfigDict.output_compression_quality)
    - [`EditImageConfigDict.output_gcs_uri`](genai.html#genai.types.EditImageConfigDict.output_gcs_uri)
    - [`EditImageConfigDict.output_mime_type`](genai.html#genai.types.EditImageConfigDict.output_mime_type)
    - [`EditImageConfigDict.person_generation`](genai.html#genai.types.EditImageConfigDict.person_generation)
    - [`EditImageConfigDict.safety_filter_level`](genai.html#genai.types.EditImageConfigDict.safety_filter_level)
    - [`EditImageConfigDict.seed`](genai.html#genai.types.EditImageConfigDict.seed)
  + [`EditImageResponse`](genai.html#genai.types.EditImageResponse)
    - [`EditImageResponse.generated_images`](genai.html#genai.types.EditImageResponse.generated_images)
  + [`EditImageResponseDict`](genai.html#genai.types.EditImageResponseDict)
    - [`EditImageResponseDict.generated_images`](genai.html#genai.types.EditImageResponseDict.generated_images)
  + [`EditMode`](genai.html#genai.types.EditMode)
    - [`EditMode.EDIT_MODE_BGSWAP`](genai.html#genai.types.EditMode.EDIT_MODE_BGSWAP)
    - [`EditMode.EDIT_MODE_CONTROLLED_EDITING`](genai.html#genai.types.EditMode.EDIT_MODE_CONTROLLED_EDITING)
    - [`EditMode.EDIT_MODE_DEFAULT`](genai.html#genai.types.EditMode.EDIT_MODE_DEFAULT)
    - [`EditMode.EDIT_MODE_INPAINT_INSERTION`](genai.html#genai.types.EditMode.EDIT_MODE_INPAINT_INSERTION)
    - [`EditMode.EDIT_MODE_INPAINT_REMOVAL`](genai.html#genai.types.EditMode.EDIT_MODE_INPAINT_REMOVAL)
    - [`EditMode.EDIT_MODE_OUTPAINT`](genai.html#genai.types.EditMode.EDIT_MODE_OUTPAINT)
    - [`EditMode.EDIT_MODE_PRODUCT_IMAGE`](genai.html#genai.types.EditMode.EDIT_MODE_PRODUCT_IMAGE)
    - [`EditMode.EDIT_MODE_STYLE`](genai.html#genai.types.EditMode.EDIT_MODE_STYLE)
  + [`EmbedContentConfig`](genai.html#genai.types.EmbedContentConfig)
    - [`EmbedContentConfig.auto_truncate`](genai.html#genai.types.EmbedContentConfig.auto_truncate)
    - [`EmbedContentConfig.http_options`](genai.html#genai.types.EmbedContentConfig.http_options)
    - [`EmbedContentConfig.mime_type`](genai.html#genai.types.EmbedContentConfig.mime_type)
    - [`EmbedContentConfig.output_dimensionality`](genai.html#genai.types.EmbedContentConfig.output_dimensionality)
    - [`EmbedContentConfig.task_type`](genai.html#genai.types.EmbedContentConfig.task_type)
    - [`EmbedContentConfig.title`](genai.html#genai.types.EmbedContentConfig.title)
  + [`EmbedContentConfigDict`](genai.html#genai.types.EmbedContentConfigDict)
    - [`EmbedContentConfigDict.auto_truncate`](genai.html#genai.types.EmbedContentConfigDict.auto_truncate)
    - [`EmbedContentConfigDict.http_options`](genai.html#genai.types.EmbedContentConfigDict.http_options)
    - [`EmbedContentConfigDict.mime_type`](genai.html#genai.types.EmbedContentConfigDict.mime_type)
    - [`EmbedContentConfigDict.output_dimensionality`](genai.html#genai.types.EmbedContentConfigDict.output_dimensionality)
    - [`EmbedContentConfigDict.task_type`](genai.html#genai.types.EmbedContentConfigDict.task_type)
    - [`EmbedContentConfigDict.title`](genai.html#genai.types.EmbedContentConfigDict.title)
  + [`EmbedContentMetadata`](genai.html#genai.types.EmbedContentMetadata)
    - [`EmbedContentMetadata.billable_character_count`](genai.html#genai.types.EmbedContentMetadata.billable_character_count)
  + [`EmbedContentMetadataDict`](genai.html#genai.types.EmbedContentMetadataDict)
    - [`EmbedContentMetadataDict.billable_character_count`](genai.html#genai.types.EmbedContentMetadataDict.billable_character_count)
  + [`EmbedContentResponse`](genai.html#genai.types.EmbedContentResponse)
    - [`EmbedContentResponse.embeddings`](genai.html#genai.types.EmbedContentResponse.embeddings)
    - [`EmbedContentResponse.metadata`](genai.html#genai.types.EmbedContentResponse.metadata)
  + [`EmbedContentResponseDict`](genai.html#genai.types.EmbedContentResponseDict)
    - [`EmbedContentResponseDict.embeddings`](genai.html#genai.types.EmbedContentResponseDict.embeddings)
    - [`EmbedContentResponseDict.metadata`](genai.html#genai.types.EmbedContentResponseDict.metadata)
  + [`EncryptionSpec`](genai.html#genai.types.EncryptionSpec)
    - [`EncryptionSpec.kms_key_name`](genai.html#genai.types.EncryptionSpec.kms_key_name)
  + [`EncryptionSpecDict`](genai.html#genai.types.EncryptionSpecDict)
    - [`EncryptionSpecDict.kms_key_name`](genai.html#genai.types.EncryptionSpecDict.kms_key_name)
  + [`EndSensitivity`](genai.html#genai.types.EndSensitivity)
    - [`EndSensitivity.END_SENSITIVITY_HIGH`](genai.html#genai.types.EndSensitivity.END_SENSITIVITY_HIGH)
    - [`EndSensitivity.END_SENSITIVITY_LOW`](genai.html#genai.types.EndSensitivity.END_SENSITIVITY_LOW)
    - [`EndSensitivity.END_SENSITIVITY_UNSPECIFIED`](genai.html#genai.types.EndSensitivity.END_SENSITIVITY_UNSPECIFIED)
  + [`Endpoint`](genai.html#genai.types.Endpoint)
    - [`Endpoint.deployed_model_id`](genai.html#genai.types.Endpoint.deployed_model_id)
    - [`Endpoint.name`](genai.html#genai.types.Endpoint.name)
  + [`EndpointDict`](genai.html#genai.types.EndpointDict)
    - [`EndpointDict.deployed_model_id`](genai.html#genai.types.EndpointDict.deployed_model_id)
    - [`EndpointDict.name`](genai.html#genai.types.EndpointDict.name)
  + [`ExecutableCode`](genai.html#genai.types.ExecutableCode)
    - [`ExecutableCode.code`](genai.html#genai.types.ExecutableCode.code)
    - [`ExecutableCode.language`](genai.html#genai.types.ExecutableCode.language)
  + [`ExecutableCodeDict`](genai.html#genai.types.ExecutableCodeDict)
    - [`ExecutableCodeDict.code`](genai.html#genai.types.ExecutableCodeDict.code)
    - [`ExecutableCodeDict.language`](genai.html#genai.types.ExecutableCodeDict.language)
  + [`FeatureSelectionPreference`](genai.html#genai.types.FeatureSelectionPreference)
    - [`FeatureSelectionPreference.BALANCED`](genai.html#genai.types.FeatureSelectionPreference.BALANCED)
    - [`FeatureSelectionPreference.FEATURE_SELECTION_PREFERENCE_UNSPECIFIED`](genai.html#genai.types.FeatureSelectionPreference.FEATURE_SELECTION_PREFERENCE_UNSPECIFIED)
    - [`FeatureSelectionPreference.PRIORITIZE_COST`](genai.html#genai.types.FeatureSelectionPreference.PRIORITIZE_COST)
    - [`FeatureSelectionPreference.PRIORITIZE_QUALITY`](genai.html#genai.types.FeatureSelectionPreference.PRIORITIZE_QUALITY)
  + [`FetchPredictOperationConfig`](genai.html#genai.types.FetchPredictOperationConfig)
    - [`FetchPredictOperationConfig.http_options`](genai.html#genai.types.FetchPredictOperationConfig.http_options)
  + [`FetchPredictOperationConfigDict`](genai.html#genai.types.FetchPredictOperationConfigDict)
    - [`FetchPredictOperationConfigDict.http_options`](genai.html#genai.types.FetchPredictOperationConfigDict.http_options)
  + [`File`](genai.html#genai.types.File)
    - [`File.create_time`](genai.html#genai.types.File.create_time)
    - [`File.display_name`](genai.html#genai.types.File.display_name)
    - [`File.download_uri`](genai.html#genai.types.File.download_uri)
    - [`File.error`](genai.html#genai.types.File.error)
    - [`File.expiration_time`](genai.html#genai.types.File.expiration_time)
    - [`File.mime_type`](genai.html#genai.types.File.mime_type)
    - [`File.name`](genai.html#genai.types.File.name)
    - [`File.sha256_hash`](genai.html#genai.types.File.sha256_hash)
    - [`File.size_bytes`](genai.html#genai.types.File.size_bytes)
    - [`File.source`](genai.html#genai.types.File.source)
    - [`File.state`](genai.html#genai.types.File.state)
    - [`File.update_time`](genai.html#genai.types.File.update_time)
    - [`File.uri`](genai.html#genai.types.File.uri)
    - [`File.video_metadata`](genai.html#genai.types.File.video_metadata)
  + [`FileData`](genai.html#genai.types.FileData)
    - [`FileData.file_uri`](genai.html#genai.types.FileData.file_uri)
    - [`FileData.mime_type`](genai.html#genai.types.FileData.mime_type)
  + [`FileDataDict`](genai.html#genai.types.FileDataDict)
    - [`FileDataDict.file_uri`](genai.html#genai.types.FileDataDict.file_uri)
    - [`FileDataDict.mime_type`](genai.html#genai.types.FileDataDict.mime_type)
  + [`FileDict`](genai.html#genai.types.FileDict)
    - [`FileDict.create_time`](genai.html#genai.types.FileDict.create_time)
    - [`FileDict.display_name`](genai.html#genai.types.FileDict.display_name)
    - [`FileDict.download_uri`](genai.html#genai.types.FileDict.download_uri)
    - [`FileDict.error`](genai.html#genai.types.FileDict.error)
    - [`FileDict.expiration_time`](genai.html#genai.types.FileDict.expiration_time)
    - [`FileDict.mime_type`](genai.html#genai.types.FileDict.mime_type)
    - [`FileDict.name`](genai.html#genai.types.FileDict.name)
    - [`FileDict.sha256_hash`](genai.html#genai.types.FileDict.sha256_hash)
    - [`FileDict.size_bytes`](genai.html#genai.types.FileDict.size_bytes)
    - [`FileDict.source`](genai.html#genai.types.FileDict.source)
    - [`FileDict.state`](genai.html#genai.types.FileDict.state)
    - [`FileDict.update_time`](genai.html#genai.types.FileDict.update_time)
    - [`FileDict.uri`](genai.html#genai.types.FileDict.uri)
    - [`FileDict.video_metadata`](genai.html#genai.types.FileDict.video_metadata)
  + [`FileSource`](genai.html#genai.types.FileSource)
    - [`FileSource.GENERATED`](genai.html#genai.types.FileSource.GENERATED)
    - [`FileSource.SOURCE_UNSPECIFIED`](genai.html#genai.types.FileSource.SOURCE_UNSPECIFIED)
    - [`FileSource.UPLOADED`](genai.html#genai.types.FileSource.UPLOADED)
  + [`FileState`](genai.html#genai.types.FileState)
    - [`FileState.ACTIVE`](genai.html#genai.types.FileState.ACTIVE)
    - [`FileState.FAILED`](genai.html#genai.types.FileState.FAILED)
    - [`FileState.PROCESSING`](genai.html#genai.types.FileState.PROCESSING)
    - [`FileState.STATE_UNSPECIFIED`](genai.html#genai.types.FileState.STATE_UNSPECIFIED)
  + [`FileStatus`](genai.html#genai.types.FileStatus)
    - [`FileStatus.code`](genai.html#genai.types.FileStatus.code)
    - [`FileStatus.details`](genai.html#genai.types.FileStatus.details)
    - [`FileStatus.message`](genai.html#genai.types.FileStatus.message)
  + [`FileStatusDict`](genai.html#genai.types.FileStatusDict)
    - [`FileStatusDict.code`](genai.html#genai.types.FileStatusDict.code)
    - [`FileStatusDict.details`](genai.html#genai.types.FileStatusDict.details)
    - [`FileStatusDict.message`](genai.html#genai.types.FileStatusDict.message)
  + [`FinishReason`](genai.html#genai.types.FinishReason)
    - [`FinishReason.BLOCKLIST`](genai.html#genai.types.FinishReason.BLOCKLIST)
    - [`FinishReason.FINISH_REASON_UNSPECIFIED`](genai.html#genai.types.FinishReason.FINISH_REASON_UNSPECIFIED)
    - [`FinishReason.IMAGE_SAFETY`](genai.html#genai.types.FinishReason.IMAGE_SAFETY)
    - [`FinishReason.LANGUAGE`](genai.html#genai.types.FinishReason.LANGUAGE)
    - [`FinishReason.MALFORMED_FUNCTION_CALL`](genai.html#genai.types.FinishReason.MALFORMED_FUNCTION_CALL)
    - [`FinishReason.MAX_TOKENS`](genai.html#genai.types.FinishReason.MAX_TOKENS)
    - [`FinishReason.OTHER`](genai.html#genai.types.FinishReason.OTHER)
    - [`FinishReason.PROHIBITED_CONTENT`](genai.html#genai.types.FinishReason.PROHIBITED_CONTENT)
    - [`FinishReason.RECITATION`](genai.html#genai.types.FinishReason.RECITATION)
    - [`FinishReason.SAFETY`](genai.html#genai.types.FinishReason.SAFETY)
    - [`FinishReason.SPII`](genai.html#genai.types.FinishReason.SPII)
    - [`FinishReason.STOP`](genai.html#genai.types.FinishReason.STOP)
  + [`FunctionCall`](genai.html#genai.types.FunctionCall)
    - [`FunctionCall.args`](genai.html#genai.types.FunctionCall.args)
    - [`FunctionCall.id`](genai.html#genai.types.FunctionCall.id)
    - [`FunctionCall.name`](genai.html#genai.types.FunctionCall.name)
  + [`FunctionCallDict`](genai.html#genai.types.FunctionCallDict)
    - [`FunctionCallDict.args`](genai.html#genai.types.FunctionCallDict.args)
    - [`FunctionCallDict.id`](genai.html#genai.types.FunctionCallDict.id)
    - [`FunctionCallDict.name`](genai.html#genai.types.FunctionCallDict.name)
  + [`FunctionCallingConfig`](genai.html#genai.types.FunctionCallingConfig)
    - [`FunctionCallingConfig.allowed_function_names`](genai.html#genai.types.FunctionCallingConfig.allowed_function_names)
    - [`FunctionCallingConfig.mode`](genai.html#genai.types.FunctionCallingConfig.mode)
  + [`FunctionCallingConfigDict`](genai.html#genai.types.FunctionCallingConfigDict)
    - [`FunctionCallingConfigDict.allowed_function_names`](genai.html#genai.types.FunctionCallingConfigDict.allowed_function_names)
    - [`FunctionCallingConfigDict.mode`](genai.html#genai.types.FunctionCallingConfigDict.mode)
  + [`FunctionCallingConfigMode`](genai.html#genai.types.FunctionCallingConfigMode)
    - [`FunctionCallingConfigMode.ANY`](genai.html#genai.types.FunctionCallingConfigMode.ANY)
    - [`FunctionCallingConfigMode.AUTO`](genai.html#genai.types.FunctionCallingConfigMode.AUTO)
    - [`FunctionCallingConfigMode.MODE_UNSPECIFIED`](genai.html#genai.types.FunctionCallingConfigMode.MODE_UNSPECIFIED)
    - [`FunctionCallingConfigMode.NONE`](genai.html#genai.types.FunctionCallingConfigMode.NONE)
  + [`FunctionDeclaration`](genai.html#genai.types.FunctionDeclaration)
    - [`FunctionDeclaration.description`](genai.html#genai.types.FunctionDeclaration.description)
    - [`FunctionDeclaration.name`](genai.html#genai.types.FunctionDeclaration.name)
    - [`FunctionDeclaration.parameters`](genai.html#genai.types.FunctionDeclaration.parameters)
    - [`FunctionDeclaration.response`](genai.html#genai.types.FunctionDeclaration.response)
    - [`FunctionDeclaration.from_callable()`](genai.html#genai.types.FunctionDeclaration.from_callable)
    - [`FunctionDeclaration.from_callable_with_api_option()`](genai.html#genai.types.FunctionDeclaration.from_callable_with_api_option)
  + [`FunctionDeclarationDict`](genai.html#genai.types.FunctionDeclarationDict)
    - [`FunctionDeclarationDict.description`](genai.html#genai.types.FunctionDeclarationDict.description)
    - [`FunctionDeclarationDict.name`](genai.html#genai.types.FunctionDeclarationDict.name)
    - [`FunctionDeclarationDict.parameters`](genai.html#genai.types.FunctionDeclarationDict.parameters)
    - [`FunctionDeclarationDict.response`](genai.html#genai.types.FunctionDeclarationDict.response)
  + [`FunctionResponse`](genai.html#genai.types.FunctionResponse)
    - [`FunctionResponse.id`](genai.html#genai.types.FunctionResponse.id)
    - [`FunctionResponse.name`](genai.html#genai.types.FunctionResponse.name)
    - [`FunctionResponse.response`](genai.html#genai.types.FunctionResponse.response)
  + [`FunctionResponseDict`](genai.html#genai.types.FunctionResponseDict)
    - [`FunctionResponseDict.id`](genai.html#genai.types.FunctionResponseDict.id)
    - [`FunctionResponseDict.name`](genai.html#genai.types.FunctionResponseDict.name)
    - [`FunctionResponseDict.response`](genai.html#genai.types.FunctionResponseDict.response)
  + [`GenerateContentConfig`](genai.html#genai.types.GenerateContentConfig)
    - [`GenerateContentConfig.audio_timestamp`](genai.html#genai.types.GenerateContentConfig.audio_timestamp)
    - [`GenerateContentConfig.automatic_function_calling`](genai.html#genai.types.GenerateContentConfig.automatic_function_calling)
    - [`GenerateContentConfig.cached_content`](genai.html#genai.types.GenerateContentConfig.cached_content)
    - [`GenerateContentConfig.candidate_count`](genai.html#genai.types.GenerateContentConfig.candidate_count)
    - [`GenerateContentConfig.frequency_penalty`](genai.html#genai.types.GenerateContentConfig.frequency_penalty)
    - [`GenerateContentConfig.http_options`](genai.html#genai.types.GenerateContentConfig.http_options)
    - [`GenerateContentConfig.labels`](genai.html#genai.types.GenerateContentConfig.labels)
    - [`GenerateContentConfig.logprobs`](genai.html#genai.types.GenerateContentConfig.logprobs)
    - [`GenerateContentConfig.max_output_tokens`](genai.html#genai.types.GenerateContentConfig.max_output_tokens)
    - [`GenerateContentConfig.media_resolution`](genai.html#genai.types.GenerateContentConfig.media_resolution)
    - [`GenerateContentConfig.model_selection_config`](genai.html#genai.types.GenerateContentConfig.model_selection_config)
    - [`GenerateContentConfig.presence_penalty`](genai.html#genai.types.GenerateContentConfig.presence_penalty)
    - [`GenerateContentConfig.response_logprobs`](genai.html#genai.types.GenerateContentConfig.response_logprobs)
    - [`GenerateContentConfig.response_mime_type`](genai.html#genai.types.GenerateContentConfig.response_mime_type)
    - [`GenerateContentConfig.response_modalities`](genai.html#genai.types.GenerateContentConfig.response_modalities)
    - [`GenerateContentConfig.response_schema`](genai.html#genai.types.GenerateContentConfig.response_schema)
    - [`GenerateContentConfig.routing_config`](genai.html#genai.types.GenerateContentConfig.routing_config)
    - [`GenerateContentConfig.safety_settings`](genai.html#genai.types.GenerateContentConfig.safety_settings)
    - [`GenerateContentConfig.seed`](genai.html#genai.types.GenerateContentConfig.seed)
    - [`GenerateContentConfig.speech_config`](genai.html#genai.types.GenerateContentConfig.speech_config)
    - [`GenerateContentConfig.stop_sequences`](genai.html#genai.types.GenerateContentConfig.stop_sequences)
    - [`GenerateContentConfig.system_instruction`](genai.html#genai.types.GenerateContentConfig.system_instruction)
    - [`GenerateContentConfig.temperature`](genai.html#genai.types.GenerateContentConfig.temperature)
    - [`GenerateContentConfig.thinking_config`](genai.html#genai.types.GenerateContentConfig.thinking_config)
    - [`GenerateContentConfig.tool_config`](genai.html#genai.types.GenerateContentConfig.tool_config)
    - [`GenerateContentConfig.tools`](genai.html#genai.types.GenerateContentConfig.tools)
    - [`GenerateContentConfig.top_k`](genai.html#genai.types.GenerateContentConfig.top_k)
    - [`GenerateContentConfig.top_p`](genai.html#genai.types.GenerateContentConfig.top_p)
  + [`GenerateContentConfigDict`](genai.html#genai.types.GenerateContentConfigDict)
    - [`GenerateContentConfigDict.audio_timestamp`](genai.html#genai.types.GenerateContentConfigDict.audio_timestamp)
    - [`GenerateContentConfigDict.automatic_function_calling`](genai.html#genai.types.GenerateContentConfigDict.automatic_function_calling)
    - [`GenerateContentConfigDict.cached_content`](genai.html#genai.types.GenerateContentConfigDict.cached_content)
    - [`GenerateContentConfigDict.candidate_count`](genai.html#genai.types.GenerateContentConfigDict.candidate_count)
    - [`GenerateContentConfigDict.frequency_penalty`](genai.html#genai.types.GenerateContentConfigDict.frequency_penalty)
    - [`GenerateContentConfigDict.http_options`](genai.html#genai.types.GenerateContentConfigDict.http_options)
    - [`GenerateContentConfigDict.labels`](genai.html#genai.types.GenerateContentConfigDict.labels)
    - [`GenerateContentConfigDict.logprobs`](genai.html#genai.types.GenerateContentConfigDict.logprobs)
    - [`GenerateContentConfigDict.max_output_tokens`](genai.html#genai.types.GenerateContentConfigDict.max_output_tokens)
    - [`GenerateContentConfigDict.media_resolution`](genai.html#genai.types.GenerateContentConfigDict.media_resolution)
    - [`GenerateContentConfigDict.model_selection_config`](genai.html#genai.types.GenerateContentConfigDict.model_selection_config)
    - [`GenerateContentConfigDict.presence_penalty`](genai.html#genai.types.GenerateContentConfigDict.presence_penalty)
    - [`GenerateContentConfigDict.response_logprobs`](genai.html#genai.types.GenerateContentConfigDict.response_logprobs)
    - [`GenerateContentConfigDict.response_mime_type`](genai.html#genai.types.GenerateContentConfigDict.response_mime_type)
    - [`GenerateContentConfigDict.response_modalities`](genai.html#genai.types.GenerateContentConfigDict.response_modalities)
    - [`GenerateContentConfigDict.response_schema`](genai.html#genai.types.GenerateContentConfigDict.response_schema)
    - [`GenerateContentConfigDict.routing_config`](genai.html#genai.types.GenerateContentConfigDict.routing_config)
    - [`GenerateContentConfigDict.safety_settings`](genai.html#genai.types.GenerateContentConfigDict.safety_settings)
    - [`GenerateContentConfigDict.seed`](genai.html#genai.types.GenerateContentConfigDict.seed)
    - [`GenerateContentConfigDict.speech_config`](genai.html#genai.types.GenerateContentConfigDict.speech_config)
    - [`GenerateContentConfigDict.stop_sequences`](genai.html#genai.types.GenerateContentConfigDict.stop_sequences)
    - [`GenerateContentConfigDict.system_instruction`](genai.html#genai.types.GenerateContentConfigDict.system_instruction)
    - [`GenerateContentConfigDict.temperature`](genai.html#genai.types.GenerateContentConfigDict.temperature)
    - [`GenerateContentConfigDict.thinking_config`](genai.html#genai.types.GenerateContentConfigDict.thinking_config)
    - [`GenerateContentConfigDict.tool_config`](genai.html#genai.types.GenerateContentConfigDict.tool_config)
    - [`GenerateContentConfigDict.tools`](genai.html#genai.types.GenerateContentConfigDict.tools)
    - [`GenerateContentConfigDict.top_k`](genai.html#genai.types.GenerateContentConfigDict.top_k)
    - [`GenerateContentConfigDict.top_p`](genai.html#genai.types.GenerateContentConfigDict.top_p)
  + [`GenerateContentResponse`](genai.html#genai.types.GenerateContentResponse)
    - [`GenerateContentResponse.automatic_function_calling_history`](genai.html#genai.types.GenerateContentResponse.automatic_function_calling_history)
    - [`GenerateContentResponse.candidates`](genai.html#genai.types.GenerateContentResponse.candidates)
    - [`GenerateContentResponse.create_time`](genai.html#genai.types.GenerateContentResponse.create_time)
    - [`GenerateContentResponse.model_version`](genai.html#genai.types.GenerateContentResponse.model_version)
    - [`GenerateContentResponse.parsed`](genai.html#genai.types.GenerateContentResponse.parsed)
    - [`GenerateContentResponse.prompt_feedback`](genai.html#genai.types.GenerateContentResponse.prompt_feedback)
    - [`GenerateContentResponse.response_id`](genai.html#genai.types.GenerateContentResponse.response_id)
    - [`GenerateContentResponse.usage_metadata`](genai.html#genai.types.GenerateContentResponse.usage_metadata)
    - [`GenerateContentResponse.code_execution_result`](genai.html#genai.types.GenerateContentResponse.code_execution_result)
    - [`GenerateContentResponse.executable_code`](genai.html#genai.types.GenerateContentResponse.executable_code)
    - [`GenerateContentResponse.function_calls`](genai.html#genai.types.GenerateContentResponse.function_calls)
    - [`GenerateContentResponse.text`](genai.html#genai.types.GenerateContentResponse.text)
  + [`GenerateContentResponseDict`](genai.html#genai.types.GenerateContentResponseDict)
    - [`GenerateContentResponseDict.candidates`](genai.html#genai.types.GenerateContentResponseDict.candidates)
    - [`GenerateContentResponseDict.create_time`](genai.html#genai.types.GenerateContentResponseDict.create_time)
    - [`GenerateContentResponseDict.model_version`](genai.html#genai.types.GenerateContentResponseDict.model_version)
    - [`GenerateContentResponseDict.prompt_feedback`](genai.html#genai.types.GenerateContentResponseDict.prompt_feedback)
    - [`GenerateContentResponseDict.response_id`](genai.html#genai.types.GenerateContentResponseDict.response_id)
    - [`GenerateContentResponseDict.usage_metadata`](genai.html#genai.types.GenerateContentResponseDict.usage_metadata)
  + [`GenerateContentResponsePromptFeedback`](genai.html#genai.types.GenerateContentResponsePromptFeedback)
    - [`GenerateContentResponsePromptFeedback.block_reason`](genai.html#genai.types.GenerateContentResponsePromptFeedback.block_reason)
    - [`GenerateContentResponsePromptFeedback.block_reason_message`](genai.html#genai.types.GenerateContentResponsePromptFeedback.block_reason_message)
    - [`GenerateContentResponsePromptFeedback.safety_ratings`](genai.html#genai.types.GenerateContentResponsePromptFeedback.safety_ratings)
  + [`GenerateContentResponsePromptFeedbackDict`](genai.html#genai.types.GenerateContentResponsePromptFeedbackDict)
    - [`GenerateContentResponsePromptFeedbackDict.block_reason`](genai.html#genai.types.GenerateContentResponsePromptFeedbackDict.block_reason)
    - [`GenerateContentResponsePromptFeedbackDict.block_reason_message`](genai.html#genai.types.GenerateContentResponsePromptFeedbackDict.block_reason_message)
    - [`GenerateContentResponsePromptFeedbackDict.safety_ratings`](genai.html#genai.types.GenerateContentResponsePromptFeedbackDict.safety_ratings)
  + [`GenerateContentResponseUsageMetadata`](genai.html#genai.types.GenerateContentResponseUsageMetadata)
    - [`GenerateContentResponseUsageMetadata.cache_tokens_details`](genai.html#genai.types.GenerateContentResponseUsageMetadata.cache_tokens_details)
    - [`GenerateContentResponseUsageMetadata.cached_content_token_count`](genai.html#genai.types.GenerateContentResponseUsageMetadata.cached_content_token_count)
    - [`GenerateContentResponseUsageMetadata.candidates_token_count`](genai.html#genai.types.GenerateContentResponseUsageMetadata.candidates_token_count)
    - [`GenerateContentResponseUsageMetadata.candidates_tokens_details`](genai.html#genai.types.GenerateContentResponseUsageMetadata.candidates_tokens_details)
    - [`GenerateContentResponseUsageMetadata.prompt_token_count`](genai.html#genai.types.GenerateContentResponseUsageMetadata.prompt_token_count)
    - [`GenerateContentResponseUsageMetadata.prompt_tokens_details`](genai.html#genai.types.GenerateContentResponseUsageMetadata.prompt_tokens_details)
    - [`GenerateContentResponseUsageMetadata.thoughts_token_count`](genai.html#genai.types.GenerateContentResponseUsageMetadata.thoughts_token_count)
    - [`GenerateContentResponseUsageMetadata.tool_use_prompt_token_count`](genai.html#genai.types.GenerateContentResponseUsageMetadata.tool_use_prompt_token_count)
    - [`GenerateContentResponseUsageMetadata.tool_use_prompt_tokens_details`](genai.html#genai.types.GenerateContentResponseUsageMetadata.tool_use_prompt_tokens_details)
    - [`GenerateContentResponseUsageMetadata.total_token_count`](genai.html#genai.types.GenerateContentResponseUsageMetadata.total_token_count)
    - [`GenerateContentResponseUsageMetadata.traffic_type`](genai.html#genai.types.GenerateContentResponseUsageMetadata.traffic_type)
  + [`GenerateContentResponseUsageMetadataDict`](genai.html#genai.types.GenerateContentResponseUsageMetadataDict)
    - [`GenerateContentResponseUsageMetadataDict.cache_tokens_details`](genai.html#genai.types.GenerateContentResponseUsageMetadataDict.cache_tokens_details)
    - [`GenerateContentResponseUsageMetadataDict.cached_content_token_count`](genai.html#genai.types.GenerateContentResponseUsageMetadataDict.cached_content_token_count)
    - [`GenerateContentResponseUsageMetadataDict.candidates_token_count`](genai.html#genai.types.GenerateContentResponseUsageMetadataDict.candidates_token_count)
    - [`GenerateContentResponseUsageMetadataDict.candidates_tokens_details`](genai.html#genai.types.GenerateContentResponseUsageMetadataDict.candidates_tokens_details)
    - [`GenerateContentResponseUsageMetadataDict.prompt_token_count`](genai.html#genai.types.GenerateContentResponseUsageMetadataDict.prompt_token_count)
    - [`GenerateContentResponseUsageMetadataDict.prompt_tokens_details`](genai.html#genai.types.GenerateContentResponseUsageMetadataDict.prompt_tokens_details)
    - [`GenerateContentResponseUsageMetadataDict.thoughts_token_count`](genai.html#genai.types.GenerateContentResponseUsageMetadataDict.thoughts_token_count)
    - [`GenerateContentResponseUsageMetadataDict.tool_use_prompt_token_count`](genai.html#genai.types.GenerateContentResponseUsageMetadataDict.tool_use_prompt_token_count)
    - [`GenerateContentResponseUsageMetadataDict.tool_use_prompt_tokens_details`](genai.html#genai.types.GenerateContentResponseUsageMetadataDict.tool_use_prompt_tokens_details)
    - [`GenerateContentResponseUsageMetadataDict.total_token_count`](genai.html#genai.types.GenerateContentResponseUsageMetadataDict.total_token_count)
    - [`GenerateContentResponseUsageMetadataDict.traffic_type`](genai.html#genai.types.GenerateContentResponseUsageMetadataDict.traffic_type)
  + [`GenerateImagesConfig`](genai.html#genai.types.GenerateImagesConfig)
    - [`GenerateImagesConfig.add_watermark`](genai.html#genai.types.GenerateImagesConfig.add_watermark)
    - [`GenerateImagesConfig.aspect_ratio`](genai.html#genai.types.GenerateImagesConfig.aspect_ratio)
    - [`GenerateImagesConfig.enhance_prompt`](genai.html#genai.types.GenerateImagesConfig.enhance_prompt)
    - [`GenerateImagesConfig.guidance_scale`](genai.html#genai.types.GenerateImagesConfig.guidance_scale)
    - [`GenerateImagesConfig.http_options`](genai.html#genai.types.GenerateImagesConfig.http_options)
    - [`GenerateImagesConfig.include_rai_reason`](genai.html#genai.types.GenerateImagesConfig.include_rai_reason)
    - [`GenerateImagesConfig.include_safety_attributes`](genai.html#genai.types.GenerateImagesConfig.include_safety_attributes)
    - [`GenerateImagesConfig.language`](genai.html#genai.types.GenerateImagesConfig.language)
    - [`GenerateImagesConfig.negative_prompt`](genai.html#genai.types.GenerateImagesConfig.negative_prompt)
    - [`GenerateImagesConfig.number_of_images`](genai.html#genai.types.GenerateImagesConfig.number_of_images)
    - [`GenerateImagesConfig.output_compression_quality`](genai.html#genai.types.GenerateImagesConfig.output_compression_quality)
    - [`GenerateImagesConfig.output_gcs_uri`](genai.html#genai.types.GenerateImagesConfig.output_gcs_uri)
    - [`GenerateImagesConfig.output_mime_type`](genai.html#genai.types.GenerateImagesConfig.output_mime_type)
    - [`GenerateImagesConfig.person_generation`](genai.html#genai.types.GenerateImagesConfig.person_generation)
    - [`GenerateImagesConfig.safety_filter_level`](genai.html#genai.types.GenerateImagesConfig.safety_filter_level)
    - [`GenerateImagesConfig.seed`](genai.html#genai.types.GenerateImagesConfig.seed)
  + [`GenerateImagesConfigDict`](genai.html#genai.types.GenerateImagesConfigDict)
    - [`GenerateImagesConfigDict.add_watermark`](genai.html#genai.types.GenerateImagesConfigDict.add_watermark)
    - [`GenerateImagesConfigDict.aspect_ratio`](genai.html#genai.types.GenerateImagesConfigDict.aspect_ratio)
    - [`GenerateImagesConfigDict.enhance_prompt`](genai.html#genai.types.GenerateImagesConfigDict.enhance_prompt)
    - [`GenerateImagesConfigDict.guidance_scale`](genai.html#genai.types.GenerateImagesConfigDict.guidance_scale)
    - [`GenerateImagesConfigDict.http_options`](genai.html#genai.types.GenerateImagesConfigDict.http_options)
    - [`GenerateImagesConfigDict.include_rai_reason`](genai.html#genai.types.GenerateImagesConfigDict.include_rai_reason)
    - [`GenerateImagesConfigDict.include_safety_attributes`](genai.html#genai.types.GenerateImagesConfigDict.include_safety_attributes)
    - [`GenerateImagesConfigDict.language`](genai.html#genai.types.GenerateImagesConfigDict.language)
    - [`GenerateImagesConfigDict.negative_prompt`](genai.html#genai.types.GenerateImagesConfigDict.negative_prompt)
    - [`GenerateImagesConfigDict.number_of_images`](genai.html#genai.types.GenerateImagesConfigDict.number_of_images)
    - [`GenerateImagesConfigDict.output_compression_quality`](genai.html#genai.types.GenerateImagesConfigDict.output_compression_quality)
    - [`GenerateImagesConfigDict.output_gcs_uri`](genai.html#genai.types.GenerateImagesConfigDict.output_gcs_uri)
    - [`GenerateImagesConfigDict.output_mime_type`](genai.html#genai.types.GenerateImagesConfigDict.output_mime_type)
    - [`GenerateImagesConfigDict.person_generation`](genai.html#genai.types.GenerateImagesConfigDict.person_generation)
    - [`GenerateImagesConfigDict.safety_filter_level`](genai.html#genai.types.GenerateImagesConfigDict.safety_filter_level)
    - [`GenerateImagesConfigDict.seed`](genai.html#genai.types.GenerateImagesConfigDict.seed)
  + [`GenerateImagesResponse`](genai.html#genai.types.GenerateImagesResponse)
    - [`GenerateImagesResponse.generated_images`](genai.html#genai.types.GenerateImagesResponse.generated_images)
    - [`GenerateImagesResponse.positive_prompt_safety_attributes`](genai.html#genai.types.GenerateImagesResponse.positive_prompt_safety_attributes)
  + [`GenerateImagesResponseDict`](genai.html#genai.types.GenerateImagesResponseDict)
    - [`GenerateImagesResponseDict.generated_images`](genai.html#genai.types.GenerateImagesResponseDict.generated_images)
    - [`GenerateImagesResponseDict.positive_prompt_safety_attributes`](genai.html#genai.types.GenerateImagesResponseDict.positive_prompt_safety_attributes)
  + [`GenerateVideosConfig`](genai.html#genai.types.GenerateVideosConfig)
    - [`GenerateVideosConfig.aspect_ratio`](genai.html#genai.types.GenerateVideosConfig.aspect_ratio)
    - [`GenerateVideosConfig.duration_seconds`](genai.html#genai.types.GenerateVideosConfig.duration_seconds)
    - [`GenerateVideosConfig.enhance_prompt`](genai.html#genai.types.GenerateVideosConfig.enhance_prompt)
    - [`GenerateVideosConfig.fps`](genai.html#genai.types.GenerateVideosConfig.fps)
    - [`GenerateVideosConfig.http_options`](genai.html#genai.types.GenerateVideosConfig.http_options)
    - [`GenerateVideosConfig.negative_prompt`](genai.html#genai.types.GenerateVideosConfig.negative_prompt)
    - [`GenerateVideosConfig.number_of_videos`](genai.html#genai.types.GenerateVideosConfig.number_of_videos)
    - [`GenerateVideosConfig.output_gcs_uri`](genai.html#genai.types.GenerateVideosConfig.output_gcs_uri)
    - [`GenerateVideosConfig.person_generation`](genai.html#genai.types.GenerateVideosConfig.person_generation)
    - [`GenerateVideosConfig.pubsub_topic`](genai.html#genai.types.GenerateVideosConfig.pubsub_topic)
    - [`GenerateVideosConfig.resolution`](genai.html#genai.types.GenerateVideosConfig.resolution)
    - [`GenerateVideosConfig.seed`](genai.html#genai.types.GenerateVideosConfig.seed)
  + [`GenerateVideosConfigDict`](genai.html#genai.types.GenerateVideosConfigDict)
    - [`GenerateVideosConfigDict.aspect_ratio`](genai.html#genai.types.GenerateVideosConfigDict.aspect_ratio)
    - [`GenerateVideosConfigDict.duration_seconds`](genai.html#genai.types.GenerateVideosConfigDict.duration_seconds)
    - [`GenerateVideosConfigDict.enhance_prompt`](genai.html#genai.types.GenerateVideosConfigDict.enhance_prompt)
    - [`GenerateVideosConfigDict.fps`](genai.html#genai.types.GenerateVideosConfigDict.fps)
    - [`GenerateVideosConfigDict.http_options`](genai.html#genai.types.GenerateVideosConfigDict.http_options)
    - [`GenerateVideosConfigDict.negative_prompt`](genai.html#genai.types.GenerateVideosConfigDict.negative_prompt)
    - [`GenerateVideosConfigDict.number_of_videos`](genai.html#genai.types.GenerateVideosConfigDict.number_of_videos)
    - [`GenerateVideosConfigDict.output_gcs_uri`](genai.html#genai.types.GenerateVideosConfigDict.output_gcs_uri)
    - [`GenerateVideosConfigDict.person_generation`](genai.html#genai.types.GenerateVideosConfigDict.person_generation)
    - [`GenerateVideosConfigDict.pubsub_topic`](genai.html#genai.types.GenerateVideosConfigDict.pubsub_topic)
    - [`GenerateVideosConfigDict.resolution`](genai.html#genai.types.GenerateVideosConfigDict.resolution)
    - [`GenerateVideosConfigDict.seed`](genai.html#genai.types.GenerateVideosConfigDict.seed)
  + [`GenerateVideosOperation`](genai.html#genai.types.GenerateVideosOperation)
    - [`GenerateVideosOperation.done`](genai.html#genai.types.GenerateVideosOperation.done)
    - [`GenerateVideosOperation.error`](genai.html#genai.types.GenerateVideosOperation.error)
    - [`GenerateVideosOperation.metadata`](genai.html#genai.types.GenerateVideosOperation.metadata)
    - [`GenerateVideosOperation.name`](genai.html#genai.types.GenerateVideosOperation.name)
    - [`GenerateVideosOperation.response`](genai.html#genai.types.GenerateVideosOperation.response)
    - [`GenerateVideosOperation.result`](genai.html#genai.types.GenerateVideosOperation.result)
  + [`GenerateVideosOperationDict`](genai.html#genai.types.GenerateVideosOperationDict)
    - [`GenerateVideosOperationDict.done`](genai.html#genai.types.GenerateVideosOperationDict.done)
    - [`GenerateVideosOperationDict.error`](genai.html#genai.types.GenerateVideosOperationDict.error)
    - [`GenerateVideosOperationDict.metadata`](genai.html#genai.types.GenerateVideosOperationDict.metadata)
    - [`GenerateVideosOperationDict.name`](genai.html#genai.types.GenerateVideosOperationDict.name)
    - [`GenerateVideosOperationDict.response`](genai.html#genai.types.GenerateVideosOperationDict.response)
    - [`GenerateVideosOperationDict.result`](genai.html#genai.types.GenerateVideosOperationDict.result)
  + [`GenerateVideosResponse`](genai.html#genai.types.GenerateVideosResponse)
    - [`GenerateVideosResponse.generated_videos`](genai.html#genai.types.GenerateVideosResponse.generated_videos)
    - [`GenerateVideosResponse.rai_media_filtered_count`](genai.html#genai.types.GenerateVideosResponse.rai_media_filtered_count)
    - [`GenerateVideosResponse.rai_media_filtered_reasons`](genai.html#genai.types.GenerateVideosResponse.rai_media_filtered_reasons)
  + [`GenerateVideosResponseDict`](genai.html#genai.types.GenerateVideosResponseDict)
    - [`GenerateVideosResponseDict.generated_videos`](genai.html#genai.types.GenerateVideosResponseDict.generated_videos)
    - [`GenerateVideosResponseDict.rai_media_filtered_count`](genai.html#genai.types.GenerateVideosResponseDict.rai_media_filtered_count)
    - [`GenerateVideosResponseDict.rai_media_filtered_reasons`](genai.html#genai.types.GenerateVideosResponseDict.rai_media_filtered_reasons)
  + [`GeneratedImage`](genai.html#genai.types.GeneratedImage)
    - [`GeneratedImage.enhanced_prompt`](genai.html#genai.types.GeneratedImage.enhanced_prompt)
    - [`GeneratedImage.image`](genai.html#genai.types.GeneratedImage.image)
    - [`GeneratedImage.rai_filtered_reason`](genai.html#genai.types.GeneratedImage.rai_filtered_reason)
    - [`GeneratedImage.safety_attributes`](genai.html#genai.types.GeneratedImage.safety_attributes)
  + [`GeneratedImageDict`](genai.html#genai.types.GeneratedImageDict)
    - [`GeneratedImageDict.enhanced_prompt`](genai.html#genai.types.GeneratedImageDict.enhanced_prompt)
    - [`GeneratedImageDict.image`](genai.html#genai.types.GeneratedImageDict.image)
    - [`GeneratedImageDict.rai_filtered_reason`](genai.html#genai.types.GeneratedImageDict.rai_filtered_reason)
    - [`GeneratedImageDict.safety_attributes`](genai.html#genai.types.GeneratedImageDict.safety_attributes)
  + [`GeneratedVideo`](genai.html#genai.types.GeneratedVideo)
    - [`GeneratedVideo.video`](genai.html#genai.types.GeneratedVideo.video)
  + [`GeneratedVideoDict`](genai.html#genai.types.GeneratedVideoDict)
    - [`GeneratedVideoDict.video`](genai.html#genai.types.GeneratedVideoDict.video)
  + [`GenerationConfig`](genai.html#genai.types.GenerationConfig)
    - [`GenerationConfig.audio_timestamp`](genai.html#genai.types.GenerationConfig.audio_timestamp)
    - [`GenerationConfig.candidate_count`](genai.html#genai.types.GenerationConfig.candidate_count)
    - [`GenerationConfig.frequency_penalty`](genai.html#genai.types.GenerationConfig.frequency_penalty)
    - [`GenerationConfig.logprobs`](genai.html#genai.types.GenerationConfig.logprobs)
    - [`GenerationConfig.max_output_tokens`](genai.html#genai.types.GenerationConfig.max_output_tokens)
    - [`GenerationConfig.media_resolution`](genai.html#genai.types.GenerationConfig.media_resolution)
    - [`GenerationConfig.presence_penalty`](genai.html#genai.types.GenerationConfig.presence_penalty)
    - [`GenerationConfig.response_logprobs`](genai.html#genai.types.GenerationConfig.response_logprobs)
    - [`GenerationConfig.response_mime_type`](genai.html#genai.types.GenerationConfig.response_mime_type)
    - [`GenerationConfig.response_schema`](genai.html#genai.types.GenerationConfig.response_schema)
    - [`GenerationConfig.routing_config`](genai.html#genai.types.GenerationConfig.routing_config)
    - [`GenerationConfig.seed`](genai.html#genai.types.GenerationConfig.seed)
    - [`GenerationConfig.stop_sequences`](genai.html#genai.types.GenerationConfig.stop_sequences)
    - [`GenerationConfig.temperature`](genai.html#genai.types.GenerationConfig.temperature)
    - [`GenerationConfig.top_k`](genai.html#genai.types.GenerationConfig.top_k)
    - [`GenerationConfig.top_p`](genai.html#genai.types.GenerationConfig.top_p)
  + [`GenerationConfigDict`](genai.html#genai.types.GenerationConfigDict)
    - [`GenerationConfigDict.audio_timestamp`](genai.html#genai.types.GenerationConfigDict.audio_timestamp)
    - [`GenerationConfigDict.candidate_count`](genai.html#genai.types.GenerationConfigDict.candidate_count)
    - [`GenerationConfigDict.frequency_penalty`](genai.html#genai.types.GenerationConfigDict.frequency_penalty)
    - [`GenerationConfigDict.logprobs`](genai.html#genai.types.GenerationConfigDict.logprobs)
    - [`GenerationConfigDict.max_output_tokens`](genai.html#genai.types.GenerationConfigDict.max_output_tokens)
    - [`GenerationConfigDict.media_resolution`](genai.html#genai.types.GenerationConfigDict.media_resolution)
    - [`GenerationConfigDict.presence_penalty`](genai.html#genai.types.GenerationConfigDict.presence_penalty)
    - [`GenerationConfigDict.response_logprobs`](genai.html#genai.types.GenerationConfigDict.response_logprobs)
    - [`GenerationConfigDict.response_mime_type`](genai.html#genai.types.GenerationConfigDict.response_mime_type)
    - [`GenerationConfigDict.response_schema`](genai.html#genai.types.GenerationConfigDict.response_schema)
    - [`GenerationConfigDict.routing_config`](genai.html#genai.types.GenerationConfigDict.routing_config)
    - [`GenerationConfigDict.seed`](genai.html#genai.types.GenerationConfigDict.seed)
    - [`GenerationConfigDict.stop_sequences`](genai.html#genai.types.GenerationConfigDict.stop_sequences)
    - [`GenerationConfigDict.temperature`](genai.html#genai.types.GenerationConfigDict.temperature)
    - [`GenerationConfigDict.top_k`](genai.html#genai.types.GenerationConfigDict.top_k)
    - [`GenerationConfigDict.top_p`](genai.html#genai.types.GenerationConfigDict.top_p)
  + [`GenerationConfigRoutingConfig`](genai.html#genai.types.GenerationConfigRoutingConfig)
    - [`GenerationConfigRoutingConfig.auto_mode`](genai.html#genai.types.GenerationConfigRoutingConfig.auto_mode)
    - [`GenerationConfigRoutingConfig.manual_mode`](genai.html#genai.types.GenerationConfigRoutingConfig.manual_mode)
  + [`GenerationConfigRoutingConfigAutoRoutingMode`](genai.html#genai.types.GenerationConfigRoutingConfigAutoRoutingMode)
    - [`GenerationConfigRoutingConfigAutoRoutingMode.model_routing_preference`](genai.html#genai.types.GenerationConfigRoutingConfigAutoRoutingMode.model_routing_preference)
  + [`GenerationConfigRoutingConfigAutoRoutingModeDict`](genai.html#genai.types.GenerationConfigRoutingConfigAutoRoutingModeDict)
    - [`GenerationConfigRoutingConfigAutoRoutingModeDict.model_routing_preference`](genai.html#genai.types.GenerationConfigRoutingConfigAutoRoutingModeDict.model_routing_preference)
  + [`GenerationConfigRoutingConfigDict`](genai.html#genai.types.GenerationConfigRoutingConfigDict)
    - [`GenerationConfigRoutingConfigDict.auto_mode`](genai.html#genai.types.GenerationConfigRoutingConfigDict.auto_mode)
    - [`GenerationConfigRoutingConfigDict.manual_mode`](genai.html#genai.types.GenerationConfigRoutingConfigDict.manual_mode)
  + [`GenerationConfigRoutingConfigManualRoutingMode`](genai.html#genai.types.GenerationConfigRoutingConfigManualRoutingMode)
    - [`GenerationConfigRoutingConfigManualRoutingMode.model_name`](genai.html#genai.types.GenerationConfigRoutingConfigManualRoutingMode.model_name)
  + [`GenerationConfigRoutingConfigManualRoutingModeDict`](genai.html#genai.types.GenerationConfigRoutingConfigManualRoutingModeDict)
    - [`GenerationConfigRoutingConfigManualRoutingModeDict.model_name`](genai.html#genai.types.GenerationConfigRoutingConfigManualRoutingModeDict.model_name)
  + [`GetBatchJobConfig`](genai.html#genai.types.GetBatchJobConfig)
    - [`GetBatchJobConfig.http_options`](genai.html#genai.types.GetBatchJobConfig.http_options)
  + [`GetBatchJobConfigDict`](genai.html#genai.types.GetBatchJobConfigDict)
    - [`GetBatchJobConfigDict.http_options`](genai.html#genai.types.GetBatchJobConfigDict.http_options)
  + [`GetCachedContentConfig`](genai.html#genai.types.GetCachedContentConfig)
    - [`GetCachedContentConfig.http_options`](genai.html#genai.types.GetCachedContentConfig.http_options)
  + [`GetCachedContentConfigDict`](genai.html#genai.types.GetCachedContentConfigDict)
    - [`GetCachedContentConfigDict.http_options`](genai.html#genai.types.GetCachedContentConfigDict.http_options)
  + [`GetFileConfig`](genai.html#genai.types.GetFileConfig)
    - [`GetFileConfig.http_options`](genai.html#genai.types.GetFileConfig.http_options)
  + [`GetFileConfigDict`](genai.html#genai.types.GetFileConfigDict)
    - [`GetFileConfigDict.http_options`](genai.html#genai.types.GetFileConfigDict.http_options)
  + [`GetModelConfig`](genai.html#genai.types.GetModelConfig)
    - [`GetModelConfig.http_options`](genai.html#genai.types.GetModelConfig.http_options)
  + [`GetModelConfigDict`](genai.html#genai.types.GetModelConfigDict)
    - [`GetModelConfigDict.http_options`](genai.html#genai.types.GetModelConfigDict.http_options)
  + [`GetOperationConfig`](genai.html#genai.types.GetOperationConfig)
    - [`GetOperationConfig.http_options`](genai.html#genai.types.GetOperationConfig.http_options)
  + [`GetOperationConfigDict`](genai.html#genai.types.GetOperationConfigDict)
    - [`GetOperationConfigDict.http_options`](genai.html#genai.types.GetOperationConfigDict.http_options)
  + [`GetTuningJobConfig`](genai.html#genai.types.GetTuningJobConfig)
    - [`GetTuningJobConfig.http_options`](genai.html#genai.types.GetTuningJobConfig.http_options)
  + [`GetTuningJobConfigDict`](genai.html#genai.types.GetTuningJobConfigDict)
    - [`GetTuningJobConfigDict.http_options`](genai.html#genai.types.GetTuningJobConfigDict.http_options)
  + [`GoogleRpcStatus`](genai.html#genai.types.GoogleRpcStatus)
    - [`GoogleRpcStatus.code`](genai.html#genai.types.GoogleRpcStatus.code)
    - [`GoogleRpcStatus.details`](genai.html#genai.types.GoogleRpcStatus.details)
    - [`GoogleRpcStatus.message`](genai.html#genai.types.GoogleRpcStatus.message)
  + [`GoogleRpcStatusDict`](genai.html#genai.types.GoogleRpcStatusDict)
    - [`GoogleRpcStatusDict.code`](genai.html#genai.types.GoogleRpcStatusDict.code)
    - [`GoogleRpcStatusDict.details`](genai.html#genai.types.GoogleRpcStatusDict.details)
    - [`GoogleRpcStatusDict.message`](genai.html#genai.types.GoogleRpcStatusDict.message)
  + [`GoogleSearch`](genai.html#genai.types.GoogleSearch)
  + [`GoogleSearchDict`](genai.html#genai.types.GoogleSearchDict)
  + [`GoogleSearchRetrieval`](genai.html#genai.types.GoogleSearchRetrieval)
    - [`GoogleSearchRetrieval.dynamic_retrieval_config`](genai.html#genai.types.GoogleSearchRetrieval.dynamic_retrieval_config)
  + [`GoogleSearchRetrievalDict`](genai.html#genai.types.GoogleSearchRetrievalDict)
    - [`GoogleSearchRetrievalDict.dynamic_retrieval_config`](genai.html#genai.types.GoogleSearchRetrievalDict.dynamic_retrieval_config)
  + [`GoogleTypeDate`](genai.html#genai.types.GoogleTypeDate)
    - [`GoogleTypeDate.day`](genai.html#genai.types.GoogleTypeDate.day)
    - [`GoogleTypeDate.month`](genai.html#genai.types.GoogleTypeDate.month)
    - [`GoogleTypeDate.year`](genai.html#genai.types.GoogleTypeDate.year)
  + [`GoogleTypeDateDict`](genai.html#genai.types.GoogleTypeDateDict)
    - [`GoogleTypeDateDict.day`](genai.html#genai.types.GoogleTypeDateDict.day)
    - [`GoogleTypeDateDict.month`](genai.html#genai.types.GoogleTypeDateDict.month)
    - [`GoogleTypeDateDict.year`](genai.html#genai.types.GoogleTypeDateDict.year)
  + [`GroundingChunk`](genai.html#genai.types.GroundingChunk)
    - [`GroundingChunk.retrieved_context`](genai.html#genai.types.GroundingChunk.retrieved_context)
    - [`GroundingChunk.web`](genai.html#genai.types.GroundingChunk.web)
  + [`GroundingChunkDict`](genai.html#genai.types.GroundingChunkDict)
    - [`GroundingChunkDict.retrieved_context`](genai.html#genai.types.GroundingChunkDict.retrieved_context)
    - [`GroundingChunkDict.web`](genai.html#genai.types.GroundingChunkDict.web)
  + [`GroundingChunkRetrievedContext`](genai.html#genai.types.GroundingChunkRetrievedContext)
    - [`GroundingChunkRetrievedContext.text`](genai.html#genai.types.GroundingChunkRetrievedContext.text)
    - [`GroundingChunkRetrievedContext.title`](genai.html#genai.types.GroundingChunkRetrievedContext.title)
    - [`GroundingChunkRetrievedContext.uri`](genai.html#genai.types.GroundingChunkRetrievedContext.uri)
  + [`GroundingChunkRetrievedContextDict`](genai.html#genai.types.GroundingChunkRetrievedContextDict)
    - [`GroundingChunkRetrievedContextDict.text`](genai.html#genai.types.GroundingChunkRetrievedContextDict.text)
    - [`GroundingChunkRetrievedContextDict.title`](genai.html#genai.types.GroundingChunkRetrievedContextDict.title)
    - [`GroundingChunkRetrievedContextDict.uri`](genai.html#genai.types.GroundingChunkRetrievedContextDict.uri)
  + [`GroundingChunkWeb`](genai.html#genai.types.GroundingChunkWeb)
    - [`GroundingChunkWeb.domain`](genai.html#genai.types.GroundingChunkWeb.domain)
    - [`GroundingChunkWeb.title`](genai.html#genai.types.GroundingChunkWeb.title)
    - [`GroundingChunkWeb.uri`](genai.html#genai.types.GroundingChunkWeb.uri)
  + [`GroundingChunkWebDict`](genai.html#genai.types.GroundingChunkWebDict)
    - [`GroundingChunkWebDict.domain`](genai.html#genai.types.GroundingChunkWebDict.domain)
    - [`GroundingChunkWebDict.title`](genai.html#genai.types.GroundingChunkWebDict.title)
    - [`GroundingChunkWebDict.uri`](genai.html#genai.types.GroundingChunkWebDict.uri)
  + [`GroundingMetadata`](genai.html#genai.types.GroundingMetadata)
    - [`GroundingMetadata.grounding_chunks`](genai.html#genai.types.GroundingMetadata.grounding_chunks)
    - [`GroundingMetadata.grounding_supports`](genai.html#genai.types.GroundingMetadata.grounding_supports)
    - [`GroundingMetadata.retrieval_metadata`](genai.html#genai.types.GroundingMetadata.retrieval_metadata)
    - [`GroundingMetadata.retrieval_queries`](genai.html#genai.types.GroundingMetadata.retrieval_queries)
    - [`GroundingMetadata.search_entry_point`](genai.html#genai.types.GroundingMetadata.search_entry_point)
    - [`GroundingMetadata.web_search_queries`](genai.html#genai.types.GroundingMetadata.web_search_queries)
  + [`GroundingMetadataDict`](genai.html#genai.types.GroundingMetadataDict)
    - [`GroundingMetadataDict.grounding_chunks`](genai.html#genai.types.GroundingMetadataDict.grounding_chunks)
    - [`GroundingMetadataDict.grounding_supports`](genai.html#genai.types.GroundingMetadataDict.grounding_supports)
    - [`GroundingMetadataDict.retrieval_metadata`](genai.html#genai.types.GroundingMetadataDict.retrieval_metadata)
    - [`GroundingMetadataDict.retrieval_queries`](genai.html#genai.types.GroundingMetadataDict.retrieval_queries)
    - [`GroundingMetadataDict.search_entry_point`](genai.html#genai.types.GroundingMetadataDict.search_entry_point)
    - [`GroundingMetadataDict.web_search_queries`](genai.html#genai.types.GroundingMetadataDict.web_search_queries)
  + [`GroundingSupport`](genai.html#genai.types.GroundingSupport)
    - [`GroundingSupport.confidence_scores`](genai.html#genai.types.GroundingSupport.confidence_scores)
    - [`GroundingSupport.grounding_chunk_indices`](genai.html#genai.types.GroundingSupport.grounding_chunk_indices)
    - [`GroundingSupport.segment`](genai.html#genai.types.GroundingSupport.segment)
  + [`GroundingSupportDict`](genai.html#genai.types.GroundingSupportDict)
    - [`GroundingSupportDict.confidence_scores`](genai.html#genai.types.GroundingSupportDict.confidence_scores)
    - [`GroundingSupportDict.grounding_chunk_indices`](genai.html#genai.types.GroundingSupportDict.grounding_chunk_indices)
    - [`GroundingSupportDict.segment`](genai.html#genai.types.GroundingSupportDict.segment)
  + [`HarmBlockMethod`](genai.html#genai.types.HarmBlockMethod)
    - [`HarmBlockMethod.HARM_BLOCK_METHOD_UNSPECIFIED`](genai.html#genai.types.HarmBlockMethod.HARM_BLOCK_METHOD_UNSPECIFIED)
    - [`HarmBlockMethod.PROBABILITY`](genai.html#genai.types.HarmBlockMethod.PROBABILITY)
    - [`HarmBlockMethod.SEVERITY`](genai.html#genai.types.HarmBlockMethod.SEVERITY)
  + [`HarmBlockThreshold`](genai.html#genai.types.HarmBlockThreshold)
    - [`HarmBlockThreshold.BLOCK_LOW_AND_ABOVE`](genai.html#genai.types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE)
    - [`HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE`](genai.html#genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE)
    - [`HarmBlockThreshold.BLOCK_NONE`](genai.html#genai.types.HarmBlockThreshold.BLOCK_NONE)
    - [`HarmBlockThreshold.BLOCK_ONLY_HIGH`](genai.html#genai.types.HarmBlockThreshold.BLOCK_ONLY_HIGH)
    - [`HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED`](genai.html#genai.types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED)
    - [`HarmBlockThreshold.OFF`](genai.html#genai.types.HarmBlockThreshold.OFF)
  + [`HarmCategory`](genai.html#genai.types.HarmCategory)
    - [`HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY`](genai.html#genai.types.HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY)
    - [`HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT`](genai.html#genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT)
    - [`HarmCategory.HARM_CATEGORY_HARASSMENT`](genai.html#genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT)
    - [`HarmCategory.HARM_CATEGORY_HATE_SPEECH`](genai.html#genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH)
    - [`HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT`](genai.html#genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT)
    - [`HarmCategory.HARM_CATEGORY_UNSPECIFIED`](genai.html#genai.types.HarmCategory.HARM_CATEGORY_UNSPECIFIED)
  + [`HarmProbability`](genai.html#genai.types.HarmProbability)
    - [`HarmProbability.HARM_PROBABILITY_UNSPECIFIED`](genai.html#genai.types.HarmProbability.HARM_PROBABILITY_UNSPECIFIED)
    - [`HarmProbability.HIGH`](genai.html#genai.types.HarmProbability.HIGH)
    - [`HarmProbability.LOW`](genai.html#genai.types.HarmProbability.LOW)
    - [`HarmProbability.MEDIUM`](genai.html#genai.types.HarmProbability.MEDIUM)
    - [`HarmProbability.NEGLIGIBLE`](genai.html#genai.types.HarmProbability.NEGLIGIBLE)
  + [`HarmSeverity`](genai.html#genai.types.HarmSeverity)
    - [`HarmSeverity.HARM_SEVERITY_HIGH`](genai.html#genai.types.HarmSeverity.HARM_SEVERITY_HIGH)
    - [`HarmSeverity.HARM_SEVERITY_LOW`](genai.html#genai.types.HarmSeverity.HARM_SEVERITY_LOW)
    - [`HarmSeverity.HARM_SEVERITY_MEDIUM`](genai.html#genai.types.HarmSeverity.HARM_SEVERITY_MEDIUM)
    - [`HarmSeverity.HARM_SEVERITY_NEGLIGIBLE`](genai.html#genai.types.HarmSeverity.HARM_SEVERITY_NEGLIGIBLE)
    - [`HarmSeverity.HARM_SEVERITY_UNSPECIFIED`](genai.html#genai.types.HarmSeverity.HARM_SEVERITY_UNSPECIFIED)
  + [`HttpOptions`](genai.html#genai.types.HttpOptions)
    - [`HttpOptions.api_version`](genai.html#genai.types.HttpOptions.api_version)
    - [`HttpOptions.async_client_args`](genai.html#genai.types.HttpOptions.async_client_args)
    - [`HttpOptions.base_url`](genai.html#genai.types.HttpOptions.base_url)
    - [`HttpOptions.client_args`](genai.html#genai.types.HttpOptions.client_args)
    - [`HttpOptions.headers`](genai.html#genai.types.HttpOptions.headers)
    - [`HttpOptions.timeout`](genai.html#genai.types.HttpOptions.timeout)
  + [`HttpOptionsDict`](genai.html#genai.types.HttpOptionsDict)
    - [`HttpOptionsDict.api_version`](genai.html#genai.types.HttpOptionsDict.api_version)
    - [`HttpOptionsDict.async_client_args`](genai.html#genai.types.HttpOptionsDict.async_client_args)
    - [`HttpOptionsDict.base_url`](genai.html#genai.types.HttpOptionsDict.base_url)
    - [`HttpOptionsDict.client_args`](genai.html#genai.types.HttpOptionsDict.client_args)
    - [`HttpOptionsDict.headers`](genai.html#genai.types.HttpOptionsDict.headers)
    - [`HttpOptionsDict.timeout`](genai.html#genai.types.HttpOptionsDict.timeout)
  + [`Image`](genai.html#genai.types.Image)
    - [`Image.gcs_uri`](genai.html#genai.types.Image.gcs_uri)
    - [`Image.image_bytes`](genai.html#genai.types.Image.image_bytes)
    - [`Image.mime_type`](genai.html#genai.types.Image.mime_type)
    - [`Image.from_file()`](genai.html#genai.types.Image.from_file)
    - [`Image.model_post_init()`](genai.html#genai.types.Image.model_post_init)
    - [`Image.save()`](genai.html#genai.types.Image.save)
    - [`Image.show()`](genai.html#genai.types.Image.show)
  + [`ImageDict`](genai.html#genai.types.ImageDict)
    - [`ImageDict.gcs_uri`](genai.html#genai.types.ImageDict.gcs_uri)
    - [`ImageDict.image_bytes`](genai.html#genai.types.ImageDict.image_bytes)
    - [`ImageDict.mime_type`](genai.html#genai.types.ImageDict.mime_type)
  + [`ImagePromptLanguage`](genai.html#genai.types.ImagePromptLanguage)
    - [`ImagePromptLanguage.auto`](genai.html#genai.types.ImagePromptLanguage.auto)
    - [`ImagePromptLanguage.en`](genai.html#genai.types.ImagePromptLanguage.en)
    - [`ImagePromptLanguage.hi`](genai.html#genai.types.ImagePromptLanguage.hi)
    - [`ImagePromptLanguage.ja`](genai.html#genai.types.ImagePromptLanguage.ja)
    - [`ImagePromptLanguage.ko`](genai.html#genai.types.ImagePromptLanguage.ko)
  + [`JSONSchema`](genai.html#genai.types.JSONSchema)
    - [`JSONSchema.any_of`](genai.html#genai.types.JSONSchema.any_of)
    - [`JSONSchema.default`](genai.html#genai.types.JSONSchema.default)
    - [`JSONSchema.description`](genai.html#genai.types.JSONSchema.description)
    - [`JSONSchema.enum`](genai.html#genai.types.JSONSchema.enum)
    - [`JSONSchema.format`](genai.html#genai.types.JSONSchema.format)
    - [`JSONSchema.items`](genai.html#genai.types.JSONSchema.items)
    - [`JSONSchema.max_items`](genai.html#genai.types.JSONSchema.max_items)
    - [`JSONSchema.max_length`](genai.html#genai.types.JSONSchema.max_length)
    - [`JSONSchema.max_properties`](genai.html#genai.types.JSONSchema.max_properties)
    - [`JSONSchema.maximum`](genai.html#genai.types.JSONSchema.maximum)
    - [`JSONSchema.min_items`](genai.html#genai.types.JSONSchema.min_items)
    - [`JSONSchema.min_length`](genai.html#genai.types.JSONSchema.min_length)
    - [`JSONSchema.min_properties`](genai.html#genai.types.JSONSchema.min_properties)
    - [`JSONSchema.minimum`](genai.html#genai.types.JSONSchema.minimum)
    - [`JSONSchema.pattern`](genai.html#genai.types.JSONSchema.pattern)
    - [`JSONSchema.properties`](genai.html#genai.types.JSONSchema.properties)
    - [`JSONSchema.required`](genai.html#genai.types.JSONSchema.required)
    - [`JSONSchema.title`](genai.html#genai.types.JSONSchema.title)
    - [`JSONSchema.type`](genai.html#genai.types.JSONSchema.type)
  + [`JSONSchemaType`](genai.html#genai.types.JSONSchemaType)
    - [`JSONSchemaType.ARRAY`](genai.html#genai.types.JSONSchemaType.ARRAY)
    - [`JSONSchemaType.BOOLEAN`](genai.html#genai.types.JSONSchemaType.BOOLEAN)
    - [`JSONSchemaType.INTEGER`](genai.html#genai.types.JSONSchemaType.INTEGER)
    - [`JSONSchemaType.NULL`](genai.html#genai.types.JSONSchemaType.NULL)
    - [`JSONSchemaType.NUMBER`](genai.html#genai.types.JSONSchemaType.NUMBER)
    - [`JSONSchemaType.OBJECT`](genai.html#genai.types.JSONSchemaType.OBJECT)
    - [`JSONSchemaType.STRING`](genai.html#genai.types.JSONSchemaType.STRING)
  + [`JobError`](genai.html#genai.types.JobError)
    - [`JobError.code`](genai.html#genai.types.JobError.code)
    - [`JobError.details`](genai.html#genai.types.JobError.details)
    - [`JobError.message`](genai.html#genai.types.JobError.message)
  + [`JobErrorDict`](genai.html#genai.types.JobErrorDict)
    - [`JobErrorDict.code`](genai.html#genai.types.JobErrorDict.code)
    - [`JobErrorDict.details`](genai.html#genai.types.JobErrorDict.details)
    - [`JobErrorDict.message`](genai.html#genai.types.JobErrorDict.message)
  + [`JobState`](genai.html#genai.types.JobState)
    - [`JobState.JOB_STATE_CANCELLED`](genai.html#genai.types.JobState.JOB_STATE_CANCELLED)
    - [`JobState.JOB_STATE_CANCELLING`](genai.html#genai.types.JobState.JOB_STATE_CANCELLING)
    - [`JobState.JOB_STATE_EXPIRED`](genai.html#genai.types.JobState.JOB_STATE_EXPIRED)
    - [`JobState.JOB_STATE_FAILED`](genai.html#genai.types.JobState.JOB_STATE_FAILED)
    - [`JobState.JOB_STATE_PARTIALLY_SUCCEEDED`](genai.html#genai.types.JobState.JOB_STATE_PARTIALLY_SUCCEEDED)
    - [`JobState.JOB_STATE_PAUSED`](genai.html#genai.types.JobState.JOB_STATE_PAUSED)
    - [`JobState.JOB_STATE_PENDING`](genai.html#genai.types.JobState.JOB_STATE_PENDING)
    - [`JobState.JOB_STATE_QUEUED`](genai.html#genai.types.JobState.JOB_STATE_QUEUED)
    - [`JobState.JOB_STATE_RUNNING`](genai.html#genai.types.JobState.JOB_STATE_RUNNING)
    - [`JobState.JOB_STATE_SUCCEEDED`](genai.html#genai.types.JobState.JOB_STATE_SUCCEEDED)
    - [`JobState.JOB_STATE_UNSPECIFIED`](genai.html#genai.types.JobState.JOB_STATE_UNSPECIFIED)
    - [`JobState.JOB_STATE_UPDATING`](genai.html#genai.types.JobState.JOB_STATE_UPDATING)
  + [`Language`](genai.html#genai.types.Language)
    - [`Language.LANGUAGE_UNSPECIFIED`](genai.html#genai.types.Language.LANGUAGE_UNSPECIFIED)
    - [`Language.PYTHON`](genai.html#genai.types.Language.PYTHON)
  + [`ListBatchJobsConfig`](genai.html#genai.types.ListBatchJobsConfig)
    - [`ListBatchJobsConfig.filter`](genai.html#genai.types.ListBatchJobsConfig.filter)
    - [`ListBatchJobsConfig.http_options`](genai.html#genai.types.ListBatchJobsConfig.http_options)
    - [`ListBatchJobsConfig.page_size`](genai.html#genai.types.ListBatchJobsConfig.page_size)
    - [`ListBatchJobsConfig.page_token`](genai.html#genai.types.ListBatchJobsConfig.page_token)
  + [`ListBatchJobsConfigDict`](genai.html#genai.types.ListBatchJobsConfigDict)
    - [`ListBatchJobsConfigDict.filter`](genai.html#genai.types.ListBatchJobsConfigDict.filter)
    - [`ListBatchJobsConfigDict.http_options`](genai.html#genai.types.ListBatchJobsConfigDict.http_options)
    - [`ListBatchJobsConfigDict.page_size`](genai.html#genai.types.ListBatchJobsConfigDict.page_size)
    - [`ListBatchJobsConfigDict.page_token`](genai.html#genai.types.ListBatchJobsConfigDict.page_token)
  + [`ListBatchJobsResponse`](genai.html#genai.types.ListBatchJobsResponse)
    - [`ListBatchJobsResponse.batch_jobs`](genai.html#genai.types.ListBatchJobsResponse.batch_jobs)
    - [`ListBatchJobsResponse.next_page_token`](genai.html#genai.types.ListBatchJobsResponse.next_page_token)
  + [`ListBatchJobsResponseDict`](genai.html#genai.types.ListBatchJobsResponseDict)
    - [`ListBatchJobsResponseDict.batch_jobs`](genai.html#genai.types.ListBatchJobsResponseDict.batch_jobs)
    - [`ListBatchJobsResponseDict.next_page_token`](genai.html#genai.types.ListBatchJobsResponseDict.next_page_token)
  + [`ListCachedContentsConfig`](genai.html#genai.types.ListCachedContentsConfig)
    - [`ListCachedContentsConfig.http_options`](genai.html#genai.types.ListCachedContentsConfig.http_options)
    - [`ListCachedContentsConfig.page_size`](genai.html#genai.types.ListCachedContentsConfig.page_size)
    - [`ListCachedContentsConfig.page_token`](genai.html#genai.types.ListCachedContentsConfig.page_token)
  + [`ListCachedContentsConfigDict`](genai.html#genai.types.ListCachedContentsConfigDict)
    - [`ListCachedContentsConfigDict.http_options`](genai.html#genai.types.ListCachedContentsConfigDict.http_options)
    - [`ListCachedContentsConfigDict.page_size`](genai.html#genai.types.ListCachedContentsConfigDict.page_size)
    - [`ListCachedContentsConfigDict.page_token`](genai.html#genai.types.ListCachedContentsConfigDict.page_token)
  + [`ListCachedContentsResponse`](genai.html#genai.types.ListCachedContentsResponse)
    - [`ListCachedContentsResponse.cached_contents`](genai.html#genai.types.ListCachedContentsResponse.cached_contents)
    - [`ListCachedContentsResponse.next_page_token`](genai.html#genai.types.ListCachedContentsResponse.next_page_token)
  + [`ListCachedContentsResponseDict`](genai.html#genai.types.ListCachedContentsResponseDict)
    - [`ListCachedContentsResponseDict.cached_contents`](genai.html#genai.types.ListCachedContentsResponseDict.cached_contents)
    - [`ListCachedContentsResponseDict.next_page_token`](genai.html#genai.types.ListCachedContentsResponseDict.next_page_token)
  + [`ListFilesConfig`](genai.html#genai.types.ListFilesConfig)
    - [`ListFilesConfig.http_options`](genai.html#genai.types.ListFilesConfig.http_options)
    - [`ListFilesConfig.page_size`](genai.html#genai.types.ListFilesConfig.page_size)
    - [`ListFilesConfig.page_token`](genai.html#genai.types.ListFilesConfig.page_token)
  + [`ListFilesConfigDict`](genai.html#genai.types.ListFilesConfigDict)
    - [`ListFilesConfigDict.http_options`](genai.html#genai.types.ListFilesConfigDict.http_options)
    - [`ListFilesConfigDict.page_size`](genai.html#genai.types.ListFilesConfigDict.page_size)
    - [`ListFilesConfigDict.page_token`](genai.html#genai.types.ListFilesConfigDict.page_token)
  + [`ListFilesResponse`](genai.html#genai.types.ListFilesResponse)
    - [`ListFilesResponse.files`](genai.html#genai.types.ListFilesResponse.files)
    - [`ListFilesResponse.next_page_token`](genai.html#genai.types.ListFilesResponse.next_page_token)
  + [`ListFilesResponseDict`](genai.html#genai.types.ListFilesResponseDict)
    - [`ListFilesResponseDict.files`](genai.html#genai.types.ListFilesResponseDict.files)
    - [`ListFilesResponseDict.next_page_token`](genai.html#genai.types.ListFilesResponseDict.next_page_token)
  + [`ListModelsConfig`](genai.html#genai.types.ListModelsConfig)
    - [`ListModelsConfig.filter`](genai.html#genai.types.ListModelsConfig.filter)
    - [`ListModelsConfig.http_options`](genai.html#genai.types.ListModelsConfig.http_options)
    - [`ListModelsConfig.page_size`](genai.html#genai.types.ListModelsConfig.page_size)
    - [`ListModelsConfig.page_token`](genai.html#genai.types.ListModelsConfig.page_token)
    - [`ListModelsConfig.query_base`](genai.html#genai.types.ListModelsConfig.query_base)
  + [`ListModelsConfigDict`](genai.html#genai.types.ListModelsConfigDict)
    - [`ListModelsConfigDict.filter`](genai.html#genai.types.ListModelsConfigDict.filter)
    - [`ListModelsConfigDict.http_options`](genai.html#genai.types.ListModelsConfigDict.http_options)
    - [`ListModelsConfigDict.page_size`](genai.html#genai.types.ListModelsConfigDict.page_size)
    - [`ListModelsConfigDict.page_token`](genai.html#genai.types.ListModelsConfigDict.page_token)
    - [`ListModelsConfigDict.query_base`](genai.html#genai.types.ListModelsConfigDict.query_base)
  + [`ListModelsResponse`](genai.html#genai.types.ListModelsResponse)
    - [`ListModelsResponse.models`](genai.html#genai.types.ListModelsResponse.models)
    - [`ListModelsResponse.next_page_token`](genai.html#genai.types.ListModelsResponse.next_page_token)
  + [`ListModelsResponseDict`](genai.html#genai.types.ListModelsResponseDict)
    - [`ListModelsResponseDict.models`](genai.html#genai.types.ListModelsResponseDict.models)
    - [`ListModelsResponseDict.next_page_token`](genai.html#genai.types.ListModelsResponseDict.next_page_token)
  + [`ListTuningJobsConfig`](genai.html#genai.types.ListTuningJobsConfig)
    - [`ListTuningJobsConfig.filter`](genai.html#genai.types.ListTuningJobsConfig.filter)
    - [`ListTuningJobsConfig.http_options`](genai.html#genai.types.ListTuningJobsConfig.http_options)
    - [`ListTuningJobsConfig.page_size`](genai.html#genai.types.ListTuningJobsConfig.page_size)
    - [`ListTuningJobsConfig.page_token`](genai.html#genai.types.ListTuningJobsConfig.page_token)
  + [`ListTuningJobsConfigDict`](genai.html#genai.types.ListTuningJobsConfigDict)
    - [`ListTuningJobsConfigDict.filter`](genai.html#genai.types.ListTuningJobsConfigDict.filter)
    - [`ListTuningJobsConfigDict.http_options`](genai.html#genai.types.ListTuningJobsConfigDict.http_options)
    - [`ListTuningJobsConfigDict.page_size`](genai.html#genai.types.ListTuningJobsConfigDict.page_size)
    - [`ListTuningJobsConfigDict.page_token`](genai.html#genai.types.ListTuningJobsConfigDict.page_token)
  + [`ListTuningJobsResponse`](genai.html#genai.types.ListTuningJobsResponse)
    - [`ListTuningJobsResponse.next_page_token`](genai.html#genai.types.ListTuningJobsResponse.next_page_token)
    - [`ListTuningJobsResponse.tuning_jobs`](genai.html#genai.types.ListTuningJobsResponse.tuning_jobs)
  + [`ListTuningJobsResponseDict`](genai.html#genai.types.ListTuningJobsResponseDict)
    - [`ListTuningJobsResponseDict.next_page_token`](genai.html#genai.types.ListTuningJobsResponseDict.next_page_token)
    - [`ListTuningJobsResponseDict.tuning_jobs`](genai.html#genai.types.ListTuningJobsResponseDict.tuning_jobs)
  + [`LiveClientContent`](genai.html#genai.types.LiveClientContent)
    - [`LiveClientContent.turn_complete`](genai.html#genai.types.LiveClientContent.turn_complete)
    - [`LiveClientContent.turns`](genai.html#genai.types.LiveClientContent.turns)
  + [`LiveClientContentDict`](genai.html#genai.types.LiveClientContentDict)
    - [`LiveClientContentDict.turn_complete`](genai.html#genai.types.LiveClientContentDict.turn_complete)
    - [`LiveClientContentDict.turns`](genai.html#genai.types.LiveClientContentDict.turns)
  + [`LiveClientMessage`](genai.html#genai.types.LiveClientMessage)
    - [`LiveClientMessage.client_content`](genai.html#genai.types.LiveClientMessage.client_content)
    - [`LiveClientMessage.realtime_input`](genai.html#genai.types.LiveClientMessage.realtime_input)
    - [`LiveClientMessage.setup`](genai.html#genai.types.LiveClientMessage.setup)
    - [`LiveClientMessage.tool_response`](genai.html#genai.types.LiveClientMessage.tool_response)
  + [`LiveClientMessageDict`](genai.html#genai.types.LiveClientMessageDict)
    - [`LiveClientMessageDict.client_content`](genai.html#genai.types.LiveClientMessageDict.client_content)
    - [`LiveClientMessageDict.realtime_input`](genai.html#genai.types.LiveClientMessageDict.realtime_input)
    - [`LiveClientMessageDict.setup`](genai.html#genai.types.LiveClientMessageDict.setup)
    - [`LiveClientMessageDict.tool_response`](genai.html#genai.types.LiveClientMessageDict.tool_response)
  + [`LiveClientRealtimeInput`](genai.html#genai.types.LiveClientRealtimeInput)
    - [`LiveClientRealtimeInput.activity_end`](genai.html#genai.types.LiveClientRealtimeInput.activity_end)
    - [`LiveClientRealtimeInput.activity_start`](genai.html#genai.types.LiveClientRealtimeInput.activity_start)
    - [`LiveClientRealtimeInput.audio`](genai.html#genai.types.LiveClientRealtimeInput.audio)
    - [`LiveClientRealtimeInput.audio_stream_end`](genai.html#genai.types.LiveClientRealtimeInput.audio_stream_end)
    - [`LiveClientRealtimeInput.media_chunks`](genai.html#genai.types.LiveClientRealtimeInput.media_chunks)
    - [`LiveClientRealtimeInput.text`](genai.html#genai.types.LiveClientRealtimeInput.text)
    - [`LiveClientRealtimeInput.video`](genai.html#genai.types.LiveClientRealtimeInput.video)
  + [`LiveClientRealtimeInputDict`](genai.html#genai.types.LiveClientRealtimeInputDict)
    - [`LiveClientRealtimeInputDict.activity_end`](genai.html#genai.types.LiveClientRealtimeInputDict.activity_end)
    - [`LiveClientRealtimeInputDict.activity_start`](genai.html#genai.types.LiveClientRealtimeInputDict.activity_start)
    - [`LiveClientRealtimeInputDict.audio`](genai.html#genai.types.LiveClientRealtimeInputDict.audio)
    - [`LiveClientRealtimeInputDict.audio_stream_end`](genai.html#genai.types.LiveClientRealtimeInputDict.audio_stream_end)
    - [`LiveClientRealtimeInputDict.media_chunks`](genai.html#genai.types.LiveClientRealtimeInputDict.media_chunks)
    - [`LiveClientRealtimeInputDict.text`](genai.html#genai.types.LiveClientRealtimeInputDict.text)
    - [`LiveClientRealtimeInputDict.video`](genai.html#genai.types.LiveClientRealtimeInputDict.video)
  + [`LiveClientSetup`](genai.html#genai.types.LiveClientSetup)
    - [`LiveClientSetup.context_window_compression`](genai.html#genai.types.LiveClientSetup.context_window_compression)
    - [`LiveClientSetup.generation_config`](genai.html#genai.types.LiveClientSetup.generation_config)
    - [`LiveClientSetup.model`](genai.html#genai.types.LiveClientSetup.model)
    - [`LiveClientSetup.session_resumption`](genai.html#genai.types.LiveClientSetup.session_resumption)
    - [`LiveClientSetup.system_instruction`](genai.html#genai.types.LiveClientSetup.system_instruction)
    - [`LiveClientSetup.tools`](genai.html#genai.types.LiveClientSetup.tools)
  + [`LiveClientSetupDict`](genai.html#genai.types.LiveClientSetupDict)
    - [`LiveClientSetupDict.context_window_compression`](genai.html#genai.types.LiveClientSetupDict.context_window_compression)
    - [`LiveClientSetupDict.generation_config`](genai.html#genai.types.LiveClientSetupDict.generation_config)
    - [`LiveClientSetupDict.model`](genai.html#genai.types.LiveClientSetupDict.model)
    - [`LiveClientSetupDict.session_resumption`](genai.html#genai.types.LiveClientSetupDict.session_resumption)
    - [`LiveClientSetupDict.system_instruction`](genai.html#genai.types.LiveClientSetupDict.system_instruction)
    - [`LiveClientSetupDict.tools`](genai.html#genai.types.LiveClientSetupDict.tools)
  + [`LiveClientToolResponse`](genai.html#genai.types.LiveClientToolResponse)
    - [`LiveClientToolResponse.function_responses`](genai.html#genai.types.LiveClientToolResponse.function_responses)
  + [`LiveClientToolResponseDict`](genai.html#genai.types.LiveClientToolResponseDict)
    - [`LiveClientToolResponseDict.function_responses`](genai.html#genai.types.LiveClientToolResponseDict.function_responses)
  + [`LiveConnectConfig`](genai.html#genai.types.LiveConnectConfig)
    - [`LiveConnectConfig.context_window_compression`](genai.html#genai.types.LiveConnectConfig.context_window_compression)
    - [`LiveConnectConfig.generation_config`](genai.html#genai.types.LiveConnectConfig.generation_config)
    - [`LiveConnectConfig.input_audio_transcription`](genai.html#genai.types.LiveConnectConfig.input_audio_transcription)
    - [`LiveConnectConfig.max_output_tokens`](genai.html#genai.types.LiveConnectConfig.max_output_tokens)
    - [`LiveConnectConfig.media_resolution`](genai.html#genai.types.LiveConnectConfig.media_resolution)
    - [`LiveConnectConfig.output_audio_transcription`](genai.html#genai.types.LiveConnectConfig.output_audio_transcription)
    - [`LiveConnectConfig.realtime_input_config`](genai.html#genai.types.LiveConnectConfig.realtime_input_config)
    - [`LiveConnectConfig.response_modalities`](genai.html#genai.types.LiveConnectConfig.response_modalities)
    - [`LiveConnectConfig.seed`](genai.html#genai.types.LiveConnectConfig.seed)
    - [`LiveConnectConfig.session_resumption`](genai.html#genai.types.LiveConnectConfig.session_resumption)
    - [`LiveConnectConfig.speech_config`](genai.html#genai.types.LiveConnectConfig.speech_config)
    - [`LiveConnectConfig.system_instruction`](genai.html#genai.types.LiveConnectConfig.system_instruction)
    - [`LiveConnectConfig.temperature`](genai.html#genai.types.LiveConnectConfig.temperature)
    - [`LiveConnectConfig.tools`](genai.html#genai.types.LiveConnectConfig.tools)
    - [`LiveConnectConfig.top_k`](genai.html#genai.types.LiveConnectConfig.top_k)
    - [`LiveConnectConfig.top_p`](genai.html#genai.types.LiveConnectConfig.top_p)
  + [`LiveConnectConfigDict`](genai.html#genai.types.LiveConnectConfigDict)
    - [`LiveConnectConfigDict.context_window_compression`](genai.html#genai.types.LiveConnectConfigDict.context_window_compression)
    - [`LiveConnectConfigDict.generation_config`](genai.html#genai.types.LiveConnectConfigDict.generation_config)
    - [`LiveConnectConfigDict.input_audio_transcription`](genai.html#genai.types.LiveConnectConfigDict.input_audio_transcription)
    - [`LiveConnectConfigDict.max_output_tokens`](genai.html#genai.types.LiveConnectConfigDict.max_output_tokens)
    - [`LiveConnectConfigDict.media_resolution`](genai.html#genai.types.LiveConnectConfigDict.media_resolution)
    - [`LiveConnectConfigDict.output_audio_transcription`](genai.html#genai.types.LiveConnectConfigDict.output_audio_transcription)
    - [`LiveConnectConfigDict.realtime_input_config`](genai.html#genai.types.LiveConnectConfigDict.realtime_input_config)
    - [`LiveConnectConfigDict.response_modalities`](genai.html#genai.types.LiveConnectConfigDict.response_modalities)
    - [`LiveConnectConfigDict.seed`](genai.html#genai.types.LiveConnectConfigDict.seed)
    - [`LiveConnectConfigDict.session_resumption`](genai.html#genai.types.LiveConnectConfigDict.session_resumption)
    - [`LiveConnectConfigDict.speech_config`](genai.html#genai.types.LiveConnectConfigDict.speech_config)
    - [`LiveConnectConfigDict.system_instruction`](genai.html#genai.types.LiveConnectConfigDict.system_instruction)
    - [`LiveConnectConfigDict.temperature`](genai.html#genai.types.LiveConnectConfigDict.temperature)
    - [`LiveConnectConfigDict.tools`](genai.html#genai.types.LiveConnectConfigDict.tools)
    - [`LiveConnectConfigDict.top_k`](genai.html#genai.types.LiveConnectConfigDict.top_k)
    - [`LiveConnectConfigDict.top_p`](genai.html#genai.types.LiveConnectConfigDict.top_p)
  + [`LiveConnectParameters`](genai.html#genai.types.LiveConnectParameters)
    - [`LiveConnectParameters.config`](genai.html#genai.types.LiveConnectParameters.config)
    - [`LiveConnectParameters.model`](genai.html#genai.types.LiveConnectParameters.model)
  + [`LiveConnectParametersDict`](genai.html#genai.types.LiveConnectParametersDict)
    - [`LiveConnectParametersDict.config`](genai.html#genai.types.LiveConnectParametersDict.config)
    - [`LiveConnectParametersDict.model`](genai.html#genai.types.LiveConnectParametersDict.model)
  + [`LiveSendRealtimeInputParameters`](genai.html#genai.types.LiveSendRealtimeInputParameters)
    - [`LiveSendRealtimeInputParameters.activity_end`](genai.html#genai.types.LiveSendRealtimeInputParameters.activity_end)
    - [`LiveSendRealtimeInputParameters.activity_start`](genai.html#genai.types.LiveSendRealtimeInputParameters.activity_start)
    - [`LiveSendRealtimeInputParameters.audio`](genai.html#genai.types.LiveSendRealtimeInputParameters.audio)
    - [`LiveSendRealtimeInputParameters.audio_stream_end`](genai.html#genai.types.LiveSendRealtimeInputParameters.audio_stream_end)
    - [`LiveSendRealtimeInputParameters.media`](genai.html#genai.types.LiveSendRealtimeInputParameters.media)
    - [`LiveSendRealtimeInputParameters.text`](genai.html#genai.types.LiveSendRealtimeInputParameters.text)
    - [`LiveSendRealtimeInputParameters.video`](genai.html#genai.types.LiveSendRealtimeInputParameters.video)
  + [`LiveSendRealtimeInputParametersDict`](genai.html#genai.types.LiveSendRealtimeInputParametersDict)
    - [`LiveSendRealtimeInputParametersDict.activity_end`](genai.html#genai.types.LiveSendRealtimeInputParametersDict.activity_end)
    - [`LiveSendRealtimeInputParametersDict.activity_start`](genai.html#genai.types.LiveSendRealtimeInputParametersDict.activity_start)
    - [`LiveSendRealtimeInputParametersDict.audio`](genai.html#genai.types.LiveSendRealtimeInputParametersDict.audio)
    - [`LiveSendRealtimeInputParametersDict.audio_stream_end`](genai.html#genai.types.LiveSendRealtimeInputParametersDict.audio_stream_end)
    - [`LiveSendRealtimeInputParametersDict.media`](genai.html#genai.types.LiveSendRealtimeInputParametersDict.media)
    - [`LiveSendRealtimeInputParametersDict.text`](genai.html#genai.types.LiveSendRealtimeInputParametersDict.text)
    - [`LiveSendRealtimeInputParametersDict.video`](genai.html#genai.types.LiveSendRealtimeInputParametersDict.video)
  + [`LiveServerContent`](genai.html#genai.types.LiveServerContent)
    - [`LiveServerContent.generation_complete`](genai.html#genai.types.LiveServerContent.generation_complete)
    - [`LiveServerContent.input_transcription`](genai.html#genai.types.LiveServerContent.input_transcription)
    - [`LiveServerContent.interrupted`](genai.html#genai.types.LiveServerContent.interrupted)
    - [`LiveServerContent.model_turn`](genai.html#genai.types.LiveServerContent.model_turn)
    - [`LiveServerContent.output_transcription`](genai.html#genai.types.LiveServerContent.output_transcription)
    - [`LiveServerContent.turn_complete`](genai.html#genai.types.LiveServerContent.turn_complete)
  + [`LiveServerContentDict`](genai.html#genai.types.LiveServerContentDict)
    - [`LiveServerContentDict.generation_complete`](genai.html#genai.types.LiveServerContentDict.generation_complete)
    - [`LiveServerContentDict.input_transcription`](genai.html#genai.types.LiveServerContentDict.input_transcription)
    - [`LiveServerContentDict.interrupted`](genai.html#genai.types.LiveServerContentDict.interrupted)
    - [`LiveServerContentDict.model_turn`](genai.html#genai.types.LiveServerContentDict.model_turn)
    - [`LiveServerContentDict.output_transcription`](genai.html#genai.types.LiveServerContentDict.output_transcription)
    - [`LiveServerContentDict.turn_complete`](genai.html#genai.types.LiveServerContentDict.turn_complete)
  + [`LiveServerGoAway`](genai.html#genai.types.LiveServerGoAway)
    - [`LiveServerGoAway.time_left`](genai.html#genai.types.LiveServerGoAway.time_left)
  + [`LiveServerGoAwayDict`](genai.html#genai.types.LiveServerGoAwayDict)
    - [`LiveServerGoAwayDict.time_left`](genai.html#genai.types.LiveServerGoAwayDict.time_left)
  + [`LiveServerMessage`](genai.html#genai.types.LiveServerMessage)
    - [`LiveServerMessage.go_away`](genai.html#genai.types.LiveServerMessage.go_away)
    - [`LiveServerMessage.server_content`](genai.html#genai.types.LiveServerMessage.server_content)
    - [`LiveServerMessage.session_resumption_update`](genai.html#genai.types.LiveServerMessage.session_resumption_update)
    - [`LiveServerMessage.setup_complete`](genai.html#genai.types.LiveServerMessage.setup_complete)
    - [`LiveServerMessage.tool_call`](genai.html#genai.types.LiveServerMessage.tool_call)
    - [`LiveServerMessage.tool_call_cancellation`](genai.html#genai.types.LiveServerMessage.tool_call_cancellation)
    - [`LiveServerMessage.usage_metadata`](genai.html#genai.types.LiveServerMessage.usage_metadata)
    - [`LiveServerMessage.data`](genai.html#genai.types.LiveServerMessage.data)
    - [`LiveServerMessage.text`](genai.html#genai.types.LiveServerMessage.text)
  + [`LiveServerMessageDict`](genai.html#genai.types.LiveServerMessageDict)
    - [`LiveServerMessageDict.go_away`](genai.html#genai.types.LiveServerMessageDict.go_away)
    - [`LiveServerMessageDict.server_content`](genai.html#genai.types.LiveServerMessageDict.server_content)
    - [`LiveServerMessageDict.session_resumption_update`](genai.html#genai.types.LiveServerMessageDict.session_resumption_update)
    - [`LiveServerMessageDict.setup_complete`](genai.html#genai.types.LiveServerMessageDict.setup_complete)
    - [`LiveServerMessageDict.tool_call`](genai.html#genai.types.LiveServerMessageDict.tool_call)
    - [`LiveServerMessageDict.tool_call_cancellation`](genai.html#genai.types.LiveServerMessageDict.tool_call_cancellation)
    - [`LiveServerMessageDict.usage_metadata`](genai.html#genai.types.LiveServerMessageDict.usage_metadata)
  + [`LiveServerSessionResumptionUpdate`](genai.html#genai.types.LiveServerSessionResumptionUpdate)
    - [`LiveServerSessionResumptionUpdate.last_consumed_client_message_index`](genai.html#genai.types.LiveServerSessionResumptionUpdate.last_consumed_client_message_index)
    - [`LiveServerSessionResumptionUpdate.new_handle`](genai.html#genai.types.LiveServerSessionResumptionUpdate.new_handle)
    - [`LiveServerSessionResumptionUpdate.resumable`](genai.html#genai.types.LiveServerSessionResumptionUpdate.resumable)
  + [`LiveServerSessionResumptionUpdateDict`](genai.html#genai.types.LiveServerSessionResumptionUpdateDict)
    - [`LiveServerSessionResumptionUpdateDict.last_consumed_client_message_index`](genai.html#genai.types.LiveServerSessionResumptionUpdateDict.last_consumed_client_message_index)
    - [`LiveServerSessionResumptionUpdateDict.new_handle`](genai.html#genai.types.LiveServerSessionResumptionUpdateDict.new_handle)
    - [`LiveServerSessionResumptionUpdateDict.resumable`](genai.html#genai.types.LiveServerSessionResumptionUpdateDict.resumable)
  + [`LiveServerSetupComplete`](genai.html#genai.types.LiveServerSetupComplete)
  + [`LiveServerSetupCompleteDict`](genai.html#genai.types.LiveServerSetupCompleteDict)
  + [`LiveServerToolCall`](genai.html#genai.types.LiveServerToolCall)
    - [`LiveServerToolCall.function_calls`](genai.html#genai.types.LiveServerToolCall.function_calls)
  + [`LiveServerToolCallCancellation`](genai.html#genai.types.LiveServerToolCallCancellation)
    - [`LiveServerToolCallCancellation.ids`](genai.html#genai.types.LiveServerToolCallCancellation.ids)
  + [`LiveServerToolCallCancellationDict`](genai.html#genai.types.LiveServerToolCallCancellationDict)
    - [`LiveServerToolCallCancellationDict.ids`](genai.html#genai.types.LiveServerToolCallCancellationDict.ids)
  + [`LiveServerToolCallDict`](genai.html#genai.types.LiveServerToolCallDict)
    - [`LiveServerToolCallDict.function_calls`](genai.html#genai.types.LiveServerToolCallDict.function_calls)
  + [`LogprobsResult`](genai.html#genai.types.LogprobsResult)
    - [`LogprobsResult.chosen_candidates`](genai.html#genai.types.LogprobsResult.chosen_candidates)
    - [`LogprobsResult.top_candidates`](genai.html#genai.types.LogprobsResult.top_candidates)
  + [`LogprobsResultCandidate`](genai.html#genai.types.LogprobsResultCandidate)
    - [`LogprobsResultCandidate.log_probability`](genai.html#genai.types.LogprobsResultCandidate.log_probability)
    - [`LogprobsResultCandidate.token`](genai.html#genai.types.LogprobsResultCandidate.token)
    - [`LogprobsResultCandidate.token_id`](genai.html#genai.types.LogprobsResultCandidate.token_id)
  + [`LogprobsResultCandidateDict`](genai.html#genai.types.LogprobsResultCandidateDict)
    - [`LogprobsResultCandidateDict.log_probability`](genai.html#genai.types.LogprobsResultCandidateDict.log_probability)
    - [`LogprobsResultCandidateDict.token`](genai.html#genai.types.LogprobsResultCandidateDict.token)
    - [`LogprobsResultCandidateDict.token_id`](genai.html#genai.types.LogprobsResultCandidateDict.token_id)
  + [`LogprobsResultDict`](genai.html#genai.types.LogprobsResultDict)
    - [`LogprobsResultDict.chosen_candidates`](genai.html#genai.types.LogprobsResultDict.chosen_candidates)
    - [`LogprobsResultDict.top_candidates`](genai.html#genai.types.LogprobsResultDict.top_candidates)
  + [`LogprobsResultTopCandidates`](genai.html#genai.types.LogprobsResultTopCandidates)
    - [`LogprobsResultTopCandidates.candidates`](genai.html#genai.types.LogprobsResultTopCandidates.candidates)
  + [`LogprobsResultTopCandidatesDict`](genai.html#genai.types.LogprobsResultTopCandidatesDict)
    - [`LogprobsResultTopCandidatesDict.candidates`](genai.html#genai.types.LogprobsResultTopCandidatesDict.candidates)
  + [`MaskReferenceConfig`](genai.html#genai.types.MaskReferenceConfig)
    - [`MaskReferenceConfig.mask_dilation`](genai.html#genai.types.MaskReferenceConfig.mask_dilation)
    - [`MaskReferenceConfig.mask_mode`](genai.html#genai.types.MaskReferenceConfig.mask_mode)
    - [`MaskReferenceConfig.segmentation_classes`](genai.html#genai.types.MaskReferenceConfig.segmentation_classes)
  + [`MaskReferenceConfigDict`](genai.html#genai.types.MaskReferenceConfigDict)
    - [`MaskReferenceConfigDict.mask_dilation`](genai.html#genai.types.MaskReferenceConfigDict.mask_dilation)
    - [`MaskReferenceConfigDict.mask_mode`](genai.html#genai.types.MaskReferenceConfigDict.mask_mode)
    - [`MaskReferenceConfigDict.segmentation_classes`](genai.html#genai.types.MaskReferenceConfigDict.segmentation_classes)
  + [`MaskReferenceImage`](genai.html#genai.types.MaskReferenceImage)
    - [`MaskReferenceImage.config`](genai.html#genai.types.MaskReferenceImage.config)
    - [`MaskReferenceImage.mask_image_config`](genai.html#genai.types.MaskReferenceImage.mask_image_config)
    - [`MaskReferenceImage.reference_id`](genai.html#genai.types.MaskReferenceImage.reference_id)
    - [`MaskReferenceImage.reference_image`](genai.html#genai.types.MaskReferenceImage.reference_image)
    - [`MaskReferenceImage.reference_type`](genai.html#genai.types.MaskReferenceImage.reference_type)
  + [`MaskReferenceImageDict`](genai.html#genai.types.MaskReferenceImageDict)
    - [`MaskReferenceImageDict.config`](genai.html#genai.types.MaskReferenceImageDict.config)
    - [`MaskReferenceImageDict.reference_id`](genai.html#genai.types.MaskReferenceImageDict.reference_id)
    - [`MaskReferenceImageDict.reference_image`](genai.html#genai.types.MaskReferenceImageDict.reference_image)
    - [`MaskReferenceImageDict.reference_type`](genai.html#genai.types.MaskReferenceImageDict.reference_type)
  + [`MaskReferenceMode`](genai.html#genai.types.MaskReferenceMode)
    - [`MaskReferenceMode.MASK_MODE_BACKGROUND`](genai.html#genai.types.MaskReferenceMode.MASK_MODE_BACKGROUND)
    - [`MaskReferenceMode.MASK_MODE_DEFAULT`](genai.html#genai.types.MaskReferenceMode.MASK_MODE_DEFAULT)
    - [`MaskReferenceMode.MASK_MODE_FOREGROUND`](genai.html#genai.types.MaskReferenceMode.MASK_MODE_FOREGROUND)
    - [`MaskReferenceMode.MASK_MODE_SEMANTIC`](genai.html#genai.types.MaskReferenceMode.MASK_MODE_SEMANTIC)
    - [`MaskReferenceMode.MASK_MODE_USER_PROVIDED`](genai.html#genai.types.MaskReferenceMode.MASK_MODE_USER_PROVIDED)
  + [`MediaModality`](genai.html#genai.types.MediaModality)
    - [`MediaModality.AUDIO`](genai.html#genai.types.MediaModality.AUDIO)
    - [`MediaModality.DOCUMENT`](genai.html#genai.types.MediaModality.DOCUMENT)
    - [`MediaModality.IMAGE`](genai.html#genai.types.MediaModality.IMAGE)
    - [`MediaModality.MODALITY_UNSPECIFIED`](genai.html#genai.types.MediaModality.MODALITY_UNSPECIFIED)
    - [`MediaModality.TEXT`](genai.html#genai.types.MediaModality.TEXT)
    - [`MediaModality.VIDEO`](genai.html#genai.types.MediaModality.VIDEO)
  + [`MediaResolution`](genai.html#genai.types.MediaResolution)
    - [`MediaResolution.MEDIA_RESOLUTION_HIGH`](genai.html#genai.types.MediaResolution.MEDIA_RESOLUTION_HIGH)
    - [`MediaResolution.MEDIA_RESOLUTION_LOW`](genai.html#genai.types.MediaResolution.MEDIA_RESOLUTION_LOW)
    - [`MediaResolution.MEDIA_RESOLUTION_MEDIUM`](genai.html#genai.types.MediaResolution.MEDIA_RESOLUTION_MEDIUM)
    - [`MediaResolution.MEDIA_RESOLUTION_UNSPECIFIED`](genai.html#genai.types.MediaResolution.MEDIA_RESOLUTION_UNSPECIFIED)
  + [`Modality`](genai.html#genai.types.Modality)
    - [`Modality.AUDIO`](genai.html#genai.types.Modality.AUDIO)
    - [`Modality.IMAGE`](genai.html#genai.types.Modality.IMAGE)
    - [`Modality.MODALITY_UNSPECIFIED`](genai.html#genai.types.Modality.MODALITY_UNSPECIFIED)
    - [`Modality.TEXT`](genai.html#genai.types.Modality.TEXT)
  + [`ModalityTokenCount`](genai.html#genai.types.ModalityTokenCount)
    - [`ModalityTokenCount.modality`](genai.html#genai.types.ModalityTokenCount.modality)
    - [`ModalityTokenCount.token_count`](genai.html#genai.types.ModalityTokenCount.token_count)
  + [`ModalityTokenCountDict`](genai.html#genai.types.ModalityTokenCountDict)
    - [`ModalityTokenCountDict.modality`](genai.html#genai.types.ModalityTokenCountDict.modality)
    - [`ModalityTokenCountDict.token_count`](genai.html#genai.types.ModalityTokenCountDict.token_count)
  + [`Mode`](genai.html#genai.types.Mode)
    - [`Mode.MODE_DYNAMIC`](genai.html#genai.types.Mode.MODE_DYNAMIC)
    - [`Mode.MODE_UNSPECIFIED`](genai.html#genai.types.Mode.MODE_UNSPECIFIED)
  + [`Model`](genai.html#genai.types.Model)
    - [`Model.description`](genai.html#genai.types.Model.description)
    - [`Model.display_name`](genai.html#genai.types.Model.display_name)
    - [`Model.endpoints`](genai.html#genai.types.Model.endpoints)
    - [`Model.input_token_limit`](genai.html#genai.types.Model.input_token_limit)
    - [`Model.labels`](genai.html#genai.types.Model.labels)
    - [`Model.name`](genai.html#genai.types.Model.name)
    - [`Model.output_token_limit`](genai.html#genai.types.Model.output_token_limit)
    - [`Model.supported_actions`](genai.html#genai.types.Model.supported_actions)
    - [`Model.tuned_model_info`](genai.html#genai.types.Model.tuned_model_info)
    - [`Model.version`](genai.html#genai.types.Model.version)
  + [`ModelContent`](genai.html#genai.types.ModelContent)
    - [`ModelContent.parts`](genai.html#genai.types.ModelContent.parts)
    - [`ModelContent.role`](genai.html#genai.types.ModelContent.role)
  + [`ModelDict`](genai.html#genai.types.ModelDict)
    - [`ModelDict.description`](genai.html#genai.types.ModelDict.description)
    - [`ModelDict.display_name`](genai.html#genai.types.ModelDict.display_name)
    - [`ModelDict.endpoints`](genai.html#genai.types.ModelDict.endpoints)
    - [`ModelDict.input_token_limit`](genai.html#genai.types.ModelDict.input_token_limit)
    - [`ModelDict.labels`](genai.html#genai.types.ModelDict.labels)
    - [`ModelDict.name`](genai.html#genai.types.ModelDict.name)
    - [`ModelDict.output_token_limit`](genai.html#genai.types.ModelDict.output_token_limit)
    - [`ModelDict.supported_actions`](genai.html#genai.types.ModelDict.supported_actions)
    - [`ModelDict.tuned_model_info`](genai.html#genai.types.ModelDict.tuned_model_info)
    - [`ModelDict.version`](genai.html#genai.types.ModelDict.version)
  + [`ModelSelectionConfig`](genai.html#genai.types.ModelSelectionConfig)
    - [`ModelSelectionConfig.feature_selection_preference`](genai.html#genai.types.ModelSelectionConfig.feature_selection_preference)
  + [`ModelSelectionConfigDict`](genai.html#genai.types.ModelSelectionConfigDict)
    - [`ModelSelectionConfigDict.feature_selection_preference`](genai.html#genai.types.ModelSelectionConfigDict.feature_selection_preference)
  + [`Operation`](genai.html#genai.types.Operation)
    - [`Operation.done`](genai.html#genai.types.Operation.done)
    - [`Operation.error`](genai.html#genai.types.Operation.error)
    - [`Operation.metadata`](genai.html#genai.types.Operation.metadata)
    - [`Operation.name`](genai.html#genai.types.Operation.name)
  + [`OperationDict`](genai.html#genai.types.OperationDict)
    - [`OperationDict.done`](genai.html#genai.types.OperationDict.done)
    - [`OperationDict.error`](genai.html#genai.types.OperationDict.error)
    - [`OperationDict.metadata`](genai.html#genai.types.OperationDict.metadata)
    - [`OperationDict.name`](genai.html#genai.types.OperationDict.name)
  + [`Outcome`](genai.html#genai.types.Outcome)
    - [`Outcome.OUTCOME_DEADLINE_EXCEEDED`](genai.html#genai.types.Outcome.OUTCOME_DEADLINE_EXCEEDED)
    - [`Outcome.OUTCOME_FAILED`](genai.html#genai.types.Outcome.OUTCOME_FAILED)
    - [`Outcome.OUTCOME_OK`](genai.html#genai.types.Outcome.OUTCOME_OK)
    - [`Outcome.OUTCOME_UNSPECIFIED`](genai.html#genai.types.Outcome.OUTCOME_UNSPECIFIED)
  + [`Part`](genai.html#genai.types.Part)
    - [`Part.code_execution_result`](genai.html#genai.types.Part.code_execution_result)
    - [`Part.executable_code`](genai.html#genai.types.Part.executable_code)
    - [`Part.file_data`](genai.html#genai.types.Part.file_data)
    - [`Part.function_call`](genai.html#genai.types.Part.function_call)
    - [`Part.function_response`](genai.html#genai.types.Part.function_response)
    - [`Part.inline_data`](genai.html#genai.types.Part.inline_data)
    - [`Part.text`](genai.html#genai.types.Part.text)
    - [`Part.thought`](genai.html#genai.types.Part.thought)
    - [`Part.video_metadata`](genai.html#genai.types.Part.video_metadata)
    - [`Part.from_bytes()`](genai.html#genai.types.Part.from_bytes)
    - [`Part.from_code_execution_result()`](genai.html#genai.types.Part.from_code_execution_result)
    - [`Part.from_executable_code()`](genai.html#genai.types.Part.from_executable_code)
    - [`Part.from_function_call()`](genai.html#genai.types.Part.from_function_call)
    - [`Part.from_function_response()`](genai.html#genai.types.Part.from_function_response)
    - [`Part.from_text()`](genai.html#genai.types.Part.from_text)
    - [`Part.from_uri()`](genai.html#genai.types.Part.from_uri)
  + [`PartDict`](genai.html#genai.types.PartDict)
    - [`PartDict.code_execution_result`](genai.html#genai.types.PartDict.code_execution_result)
    - [`PartDict.executable_code`](genai.html#genai.types.PartDict.executable_code)
    - [`PartDict.file_data`](genai.html#genai.types.PartDict.file_data)
    - [`PartDict.function_call`](genai.html#genai.types.PartDict.function_call)
    - [`PartDict.function_response`](genai.html#genai.types.PartDict.function_response)
    - [`PartDict.inline_data`](genai.html#genai.types.PartDict.inline_data)
    - [`PartDict.text`](genai.html#genai.types.PartDict.text)
    - [`PartDict.thought`](genai.html#genai.types.PartDict.thought)
    - [`PartDict.video_metadata`](genai.html#genai.types.PartDict.video_metadata)
  + [`PartnerModelTuningSpec`](genai.html#genai.types.PartnerModelTuningSpec)
    - [`PartnerModelTuningSpec.hyper_parameters`](genai.html#genai.types.PartnerModelTuningSpec.hyper_parameters)
    - [`PartnerModelTuningSpec.training_dataset_uri`](genai.html#genai.types.PartnerModelTuningSpec.training_dataset_uri)
    - [`PartnerModelTuningSpec.validation_dataset_uri`](genai.html#genai.types.PartnerModelTuningSpec.validation_dataset_uri)
  + [`PartnerModelTuningSpecDict`](genai.html#genai.types.PartnerModelTuningSpecDict)
    - [`PartnerModelTuningSpecDict.hyper_parameters`](genai.html#genai.types.PartnerModelTuningSpecDict.hyper_parameters)
    - [`PartnerModelTuningSpecDict.training_dataset_uri`](genai.html#genai.types.PartnerModelTuningSpecDict.training_dataset_uri)
    - [`PartnerModelTuningSpecDict.validation_dataset_uri`](genai.html#genai.types.PartnerModelTuningSpecDict.validation_dataset_uri)
  + [`PersonGeneration`](genai.html#genai.types.PersonGeneration)
    - [`PersonGeneration.ALLOW_ADULT`](genai.html#genai.types.PersonGeneration.ALLOW_ADULT)
    - [`PersonGeneration.ALLOW_ALL`](genai.html#genai.types.PersonGeneration.ALLOW_ALL)
    - [`PersonGeneration.DONT_ALLOW`](genai.html#genai.types.PersonGeneration.DONT_ALLOW)
  + [`PrebuiltVoiceConfig`](genai.html#genai.types.PrebuiltVoiceConfig)
    - [`PrebuiltVoiceConfig.voice_name`](genai.html#genai.types.PrebuiltVoiceConfig.voice_name)
  + [`PrebuiltVoiceConfigDict`](genai.html#genai.types.PrebuiltVoiceConfigDict)
    - [`PrebuiltVoiceConfigDict.voice_name`](genai.html#genai.types.PrebuiltVoiceConfigDict.voice_name)
  + [`RagRetrievalConfig`](genai.html#genai.types.RagRetrievalConfig)
    - [`RagRetrievalConfig.filter`](genai.html#genai.types.RagRetrievalConfig.filter)
    - [`RagRetrievalConfig.hybrid_search`](genai.html#genai.types.RagRetrievalConfig.hybrid_search)
    - [`RagRetrievalConfig.ranking`](genai.html#genai.types.RagRetrievalConfig.ranking)
    - [`RagRetrievalConfig.top_k`](genai.html#genai.types.RagRetrievalConfig.top_k)
  + [`RagRetrievalConfigDict`](genai.html#genai.types.RagRetrievalConfigDict)
    - [`RagRetrievalConfigDict.filter`](genai.html#genai.types.RagRetrievalConfigDict.filter)
    - [`RagRetrievalConfigDict.hybrid_search`](genai.html#genai.types.RagRetrievalConfigDict.hybrid_search)
    - [`RagRetrievalConfigDict.ranking`](genai.html#genai.types.RagRetrievalConfigDict.ranking)
    - [`RagRetrievalConfigDict.top_k`](genai.html#genai.types.RagRetrievalConfigDict.top_k)
  + [`RagRetrievalConfigFilter`](genai.html#genai.types.RagRetrievalConfigFilter)
    - [`RagRetrievalConfigFilter.metadata_filter`](genai.html#genai.types.RagRetrievalConfigFilter.metadata_filter)
    - [`RagRetrievalConfigFilter.vector_distance_threshold`](genai.html#genai.types.RagRetrievalConfigFilter.vector_distance_threshold)
    - [`RagRetrievalConfigFilter.vector_similarity_threshold`](genai.html#genai.types.RagRetrievalConfigFilter.vector_similarity_threshold)
  + [`RagRetrievalConfigFilterDict`](genai.html#genai.types.RagRetrievalConfigFilterDict)
    - [`RagRetrievalConfigFilterDict.metadata_filter`](genai.html#genai.types.RagRetrievalConfigFilterDict.metadata_filter)
    - [`RagRetrievalConfigFilterDict.vector_distance_threshold`](genai.html#genai.types.RagRetrievalConfigFilterDict.vector_distance_threshold)
    - [`RagRetrievalConfigFilterDict.vector_similarity_threshold`](genai.html#genai.types.RagRetrievalConfigFilterDict.vector_similarity_threshold)
  + [`RagRetrievalConfigHybridSearch`](genai.html#genai.types.RagRetrievalConfigHybridSearch)
    - [`RagRetrievalConfigHybridSearch.alpha`](genai.html#genai.types.RagRetrievalConfigHybridSearch.alpha)
  + [`RagRetrievalConfigHybridSearchDict`](genai.html#genai.types.RagRetrievalConfigHybridSearchDict)
    - [`RagRetrievalConfigHybridSearchDict.alpha`](genai.html#genai.types.RagRetrievalConfigHybridSearchDict.alpha)
  + [`RagRetrievalConfigRanking`](genai.html#genai.types.RagRetrievalConfigRanking)
    - [`RagRetrievalConfigRanking.llm_ranker`](genai.html#genai.types.RagRetrievalConfigRanking.llm_ranker)
    - [`RagRetrievalConfigRanking.rank_service`](genai.html#genai.types.RagRetrievalConfigRanking.rank_service)
  + [`RagRetrievalConfigRankingDict`](genai.html#genai.types.RagRetrievalConfigRankingDict)
    - [`RagRetrievalConfigRankingDict.llm_ranker`](genai.html#genai.types.RagRetrievalConfigRankingDict.llm_ranker)
    - [`RagRetrievalConfigRankingDict.rank_service`](genai.html#genai.types.RagRetrievalConfigRankingDict.rank_service)
  + [`RagRetrievalConfigRankingLlmRanker`](genai.html#genai.types.RagRetrievalConfigRankingLlmRanker)
    - [`RagRetrievalConfigRankingLlmRanker.model_name`](genai.html#genai.types.RagRetrievalConfigRankingLlmRanker.model_name)
  + [`RagRetrievalConfigRankingLlmRankerDict`](genai.html#genai.types.RagRetrievalConfigRankingLlmRankerDict)
    - [`RagRetrievalConfigRankingLlmRankerDict.model_name`](genai.html#genai.types.RagRetrievalConfigRankingLlmRankerDict.model_name)
  + [`RagRetrievalConfigRankingRankService`](genai.html#genai.types.RagRetrievalConfigRankingRankService)
    - [`RagRetrievalConfigRankingRankService.model_name`](genai.html#genai.types.RagRetrievalConfigRankingRankService.model_name)
  + [`RagRetrievalConfigRankingRankServiceDict`](genai.html#genai.types.RagRetrievalConfigRankingRankServiceDict)
    - [`RagRetrievalConfigRankingRankServiceDict.model_name`](genai.html#genai.types.RagRetrievalConfigRankingRankServiceDict.model_name)
  + [`RawReferenceImage`](genai.html#genai.types.RawReferenceImage)
    - [`RawReferenceImage.reference_id`](genai.html#genai.types.RawReferenceImage.reference_id)
    - [`RawReferenceImage.reference_image`](genai.html#genai.types.RawReferenceImage.reference_image)
    - [`RawReferenceImage.reference_type`](genai.html#genai.types.RawReferenceImage.reference_type)
  + [`RawReferenceImageDict`](genai.html#genai.types.RawReferenceImageDict)
    - [`RawReferenceImageDict.reference_id`](genai.html#genai.types.RawReferenceImageDict.reference_id)
    - [`RawReferenceImageDict.reference_image`](genai.html#genai.types.RawReferenceImageDict.reference_image)
    - [`RawReferenceImageDict.reference_type`](genai.html#genai.types.RawReferenceImageDict.reference_type)
  + [`RealtimeInputConfig`](genai.html#genai.types.RealtimeInputConfig)
    - [`RealtimeInputConfig.activity_handling`](genai.html#genai.types.RealtimeInputConfig.activity_handling)
    - [`RealtimeInputConfig.automatic_activity_detection`](genai.html#genai.types.RealtimeInputConfig.automatic_activity_detection)
    - [`RealtimeInputConfig.turn_coverage`](genai.html#genai.types.RealtimeInputConfig.turn_coverage)
  + [`RealtimeInputConfigDict`](genai.html#genai.types.RealtimeInputConfigDict)
    - [`RealtimeInputConfigDict.activity_handling`](genai.html#genai.types.RealtimeInputConfigDict.activity_handling)
    - [`RealtimeInputConfigDict.automatic_activity_detection`](genai.html#genai.types.RealtimeInputConfigDict.automatic_activity_detection)
    - [`RealtimeInputConfigDict.turn_coverage`](genai.html#genai.types.RealtimeInputConfigDict.turn_coverage)
  + [`ReplayFile`](genai.html#genai.types.ReplayFile)
    - [`ReplayFile.interactions`](genai.html#genai.types.ReplayFile.interactions)
    - [`ReplayFile.replay_id`](genai.html#genai.types.ReplayFile.replay_id)
  + [`ReplayFileDict`](genai.html#genai.types.ReplayFileDict)
    - [`ReplayFileDict.interactions`](genai.html#genai.types.ReplayFileDict.interactions)
    - [`ReplayFileDict.replay_id`](genai.html#genai.types.ReplayFileDict.replay_id)
  + [`ReplayInteraction`](genai.html#genai.types.ReplayInteraction)
    - [`ReplayInteraction.request`](genai.html#genai.types.ReplayInteraction.request)
    - [`ReplayInteraction.response`](genai.html#genai.types.ReplayInteraction.response)
  + [`ReplayInteractionDict`](genai.html#genai.types.ReplayInteractionDict)
    - [`ReplayInteractionDict.request`](genai.html#genai.types.ReplayInteractionDict.request)
    - [`ReplayInteractionDict.response`](genai.html#genai.types.ReplayInteractionDict.response)
  + [`ReplayRequest`](genai.html#genai.types.ReplayRequest)
    - [`ReplayRequest.body_segments`](genai.html#genai.types.ReplayRequest.body_segments)
    - [`ReplayRequest.headers`](genai.html#genai.types.ReplayRequest.headers)
    - [`ReplayRequest.method`](genai.html#genai.types.ReplayRequest.method)
    - [`ReplayRequest.url`](genai.html#genai.types.ReplayRequest.url)
  + [`ReplayRequestDict`](genai.html#genai.types.ReplayRequestDict)
    - [`ReplayRequestDict.body_segments`](genai.html#genai.types.ReplayRequestDict.body_segments)
    - [`ReplayRequestDict.headers`](genai.html#genai.types.ReplayRequestDict.headers)
    - [`ReplayRequestDict.method`](genai.html#genai.types.ReplayRequestDict.method)
    - [`ReplayRequestDict.url`](genai.html#genai.types.ReplayRequestDict.url)
  + [`ReplayResponse`](genai.html#genai.types.ReplayResponse)
    - [`ReplayResponse.body_segments`](genai.html#genai.types.ReplayResponse.body_segments)
    - [`ReplayResponse.headers`](genai.html#genai.types.ReplayResponse.headers)
    - [`ReplayResponse.sdk_response_segments`](genai.html#genai.types.ReplayResponse.sdk_response_segments)
    - [`ReplayResponse.status_code`](genai.html#genai.types.ReplayResponse.status_code)
  + [`ReplayResponseDict`](genai.html#genai.types.ReplayResponseDict)
    - [`ReplayResponseDict.body_segments`](genai.html#genai.types.ReplayResponseDict.body_segments)
    - [`ReplayResponseDict.headers`](genai.html#genai.types.ReplayResponseDict.headers)
    - [`ReplayResponseDict.sdk_response_segments`](genai.html#genai.types.ReplayResponseDict.sdk_response_segments)
    - [`ReplayResponseDict.status_code`](genai.html#genai.types.ReplayResponseDict.status_code)
  + [`Retrieval`](genai.html#genai.types.Retrieval)
    - [`Retrieval.disable_attribution`](genai.html#genai.types.Retrieval.disable_attribution)
    - [`Retrieval.vertex_ai_search`](genai.html#genai.types.Retrieval.vertex_ai_search)
    - [`Retrieval.vertex_rag_store`](genai.html#genai.types.Retrieval.vertex_rag_store)
  + [`RetrievalDict`](genai.html#genai.types.RetrievalDict)
    - [`RetrievalDict.disable_attribution`](genai.html#genai.types.RetrievalDict.disable_attribution)
    - [`RetrievalDict.vertex_ai_search`](genai.html#genai.types.RetrievalDict.vertex_ai_search)
    - [`RetrievalDict.vertex_rag_store`](genai.html#genai.types.RetrievalDict.vertex_rag_store)
  + [`RetrievalMetadata`](genai.html#genai.types.RetrievalMetadata)
    - [`RetrievalMetadata.google_search_dynamic_retrieval_score`](genai.html#genai.types.RetrievalMetadata.google_search_dynamic_retrieval_score)
  + [`RetrievalMetadataDict`](genai.html#genai.types.RetrievalMetadataDict)
    - [`RetrievalMetadataDict.google_search_dynamic_retrieval_score`](genai.html#genai.types.RetrievalMetadataDict.google_search_dynamic_retrieval_score)
  + [`SafetyAttributes`](genai.html#genai.types.SafetyAttributes)
    - [`SafetyAttributes.categories`](genai.html#genai.types.SafetyAttributes.categories)
    - [`SafetyAttributes.content_type`](genai.html#genai.types.SafetyAttributes.content_type)
    - [`SafetyAttributes.scores`](genai.html#genai.types.SafetyAttributes.scores)
  + [`SafetyAttributesDict`](genai.html#genai.types.SafetyAttributesDict)
    - [`SafetyAttributesDict.categories`](genai.html#genai.types.SafetyAttributesDict.categories)
    - [`SafetyAttributesDict.content_type`](genai.html#genai.types.SafetyAttributesDict.content_type)
    - [`SafetyAttributesDict.scores`](genai.html#genai.types.SafetyAttributesDict.scores)
  + [`SafetyFilterLevel`](genai.html#genai.types.SafetyFilterLevel)
    - [`SafetyFilterLevel.BLOCK_LOW_AND_ABOVE`](genai.html#genai.types.SafetyFilterLevel.BLOCK_LOW_AND_ABOVE)
    - [`SafetyFilterLevel.BLOCK_MEDIUM_AND_ABOVE`](genai.html#genai.types.SafetyFilterLevel.BLOCK_MEDIUM_AND_ABOVE)
    - [`SafetyFilterLevel.BLOCK_NONE`](genai.html#genai.types.SafetyFilterLevel.BLOCK_NONE)
    - [`SafetyFilterLevel.BLOCK_ONLY_HIGH`](genai.html#genai.types.SafetyFilterLevel.BLOCK_ONLY_HIGH)
  + [`SafetyRating`](genai.html#genai.types.SafetyRating)
    - [`SafetyRating.blocked`](genai.html#genai.types.SafetyRating.blocked)
    - [`SafetyRating.category`](genai.html#genai.types.SafetyRating.category)
    - [`SafetyRating.probability`](genai.html#genai.types.SafetyRating.probability)
    - [`SafetyRating.probability_score`](genai.html#genai.types.SafetyRating.probability_score)
    - [`SafetyRating.severity`](genai.html#genai.types.SafetyRating.severity)
    - [`SafetyRating.severity_score`](genai.html#genai.types.SafetyRating.severity_score)
  + [`SafetyRatingDict`](genai.html#genai.types.SafetyRatingDict)
    - [`SafetyRatingDict.blocked`](genai.html#genai.types.SafetyRatingDict.blocked)
    - [`SafetyRatingDict.category`](genai.html#genai.types.SafetyRatingDict.category)
    - [`SafetyRatingDict.probability`](genai.html#genai.types.SafetyRatingDict.probability)
    - [`SafetyRatingDict.probability_score`](genai.html#genai.types.SafetyRatingDict.probability_score)
    - [`SafetyRatingDict.severity`](genai.html#genai.types.SafetyRatingDict.severity)
    - [`SafetyRatingDict.severity_score`](genai.html#genai.types.SafetyRatingDict.severity_score)
  + [`SafetySetting`](genai.html#genai.types.SafetySetting)
    - [`SafetySetting.category`](genai.html#genai.types.SafetySetting.category)
    - [`SafetySetting.method`](genai.html#genai.types.SafetySetting.method)
    - [`SafetySetting.threshold`](genai.html#genai.types.SafetySetting.threshold)
  + [`SafetySettingDict`](genai.html#genai.types.SafetySettingDict)
    - [`SafetySettingDict.category`](genai.html#genai.types.SafetySettingDict.category)
    - [`SafetySettingDict.method`](genai.html#genai.types.SafetySettingDict.method)
    - [`SafetySettingDict.threshold`](genai.html#genai.types.SafetySettingDict.threshold)
  + [`Schema`](genai.html#genai.types.Schema)
    - [`Schema.any_of`](genai.html#genai.types.Schema.any_of)
    - [`Schema.default`](genai.html#genai.types.Schema.default)
    - [`Schema.description`](genai.html#genai.types.Schema.description)
    - [`Schema.enum`](genai.html#genai.types.Schema.enum)
    - [`Schema.example`](genai.html#genai.types.Schema.example)
    - [`Schema.format`](genai.html#genai.types.Schema.format)
    - [`Schema.items`](genai.html#genai.types.Schema.items)
    - [`Schema.max_items`](genai.html#genai.types.Schema.max_items)
    - [`Schema.max_length`](genai.html#genai.types.Schema.max_length)
    - [`Schema.max_properties`](genai.html#genai.types.Schema.max_properties)
    - [`Schema.maximum`](genai.html#genai.types.Schema.maximum)
    - [`Schema.min_items`](genai.html#genai.types.Schema.min_items)
    - [`Schema.min_length`](genai.html#genai.types.Schema.min_length)
    - [`Schema.min_properties`](genai.html#genai.types.Schema.min_properties)
    - [`Schema.minimum`](genai.html#genai.types.Schema.minimum)
    - [`Schema.nullable`](genai.html#genai.types.Schema.nullable)
    - [`Schema.pattern`](genai.html#genai.types.Schema.pattern)
    - [`Schema.properties`](genai.html#genai.types.Schema.properties)
    - [`Schema.property_ordering`](genai.html#genai.types.Schema.property_ordering)
    - [`Schema.required`](genai.html#genai.types.Schema.required)
    - [`Schema.title`](genai.html#genai.types.Schema.title)
    - [`Schema.type`](genai.html#genai.types.Schema.type)
    - [`Schema.from_json_schema()`](genai.html#genai.types.Schema.from_json_schema)
    - [`Schema.json_schema`](genai.html#genai.types.Schema.json_schema)
  + [`SchemaDict`](genai.html#genai.types.SchemaDict)
    - [`SchemaDict.any_of`](genai.html#genai.types.SchemaDict.any_of)
    - [`SchemaDict.default`](genai.html#genai.types.SchemaDict.default)
    - [`SchemaDict.description`](genai.html#genai.types.SchemaDict.description)
    - [`SchemaDict.enum`](genai.html#genai.types.SchemaDict.enum)
    - [`SchemaDict.example`](genai.html#genai.types.SchemaDict.example)
    - [`SchemaDict.format`](genai.html#genai.types.SchemaDict.format)
    - [`SchemaDict.max_items`](genai.html#genai.types.SchemaDict.max_items)
    - [`SchemaDict.max_length`](genai.html#genai.types.SchemaDict.max_length)
    - [`SchemaDict.max_properties`](genai.html#genai.types.SchemaDict.max_properties)
    - [`SchemaDict.maximum`](genai.html#genai.types.SchemaDict.maximum)
    - [`SchemaDict.min_items`](genai.html#genai.types.SchemaDict.min_items)
    - [`SchemaDict.min_length`](genai.html#genai.types.SchemaDict.min_length)
    - [`SchemaDict.min_properties`](genai.html#genai.types.SchemaDict.min_properties)
    - [`SchemaDict.minimum`](genai.html#genai.types.SchemaDict.minimum)
    - [`SchemaDict.nullable`](genai.html#genai.types.SchemaDict.nullable)
    - [`SchemaDict.pattern`](genai.html#genai.types.SchemaDict.pattern)
    - [`SchemaDict.properties`](genai.html#genai.types.SchemaDict.properties)
    - [`SchemaDict.property_ordering`](genai.html#genai.types.SchemaDict.property_ordering)
    - [`SchemaDict.required`](genai.html#genai.types.SchemaDict.required)
    - [`SchemaDict.title`](genai.html#genai.types.SchemaDict.title)
    - [`SchemaDict.type`](genai.html#genai.types.SchemaDict.type)
  + [`SearchEntryPoint`](genai.html#genai.types.SearchEntryPoint)
    - [`SearchEntryPoint.rendered_content`](genai.html#genai.types.SearchEntryPoint.rendered_content)
    - [`SearchEntryPoint.sdk_blob`](genai.html#genai.types.SearchEntryPoint.sdk_blob)
  + [`SearchEntryPointDict`](genai.html#genai.types.SearchEntryPointDict)
    - [`SearchEntryPointDict.rendered_content`](genai.html#genai.types.SearchEntryPointDict.rendered_content)
    - [`SearchEntryPointDict.sdk_blob`](genai.html#genai.types.SearchEntryPointDict.sdk_blob)
  + [`Segment`](genai.html#genai.types.Segment)
    - [`Segment.end_index`](genai.html#genai.types.Segment.end_index)
    - [`Segment.part_index`](genai.html#genai.types.Segment.part_index)
    - [`Segment.start_index`](genai.html#genai.types.Segment.start_index)
    - [`Segment.text`](genai.html#genai.types.Segment.text)
  + [`SegmentDict`](genai.html#genai.types.SegmentDict)
    - [`SegmentDict.end_index`](genai.html#genai.types.SegmentDict.end_index)
    - [`SegmentDict.part_index`](genai.html#genai.types.SegmentDict.part_index)
    - [`SegmentDict.start_index`](genai.html#genai.types.SegmentDict.start_index)
    - [`SegmentDict.text`](genai.html#genai.types.SegmentDict.text)
  + [`SessionResumptionConfig`](genai.html#genai.types.SessionResumptionConfig)
    - [`SessionResumptionConfig.handle`](genai.html#genai.types.SessionResumptionConfig.handle)
    - [`SessionResumptionConfig.transparent`](genai.html#genai.types.SessionResumptionConfig.transparent)
  + [`SessionResumptionConfigDict`](genai.html#genai.types.SessionResumptionConfigDict)
    - [`SessionResumptionConfigDict.handle`](genai.html#genai.types.SessionResumptionConfigDict.handle)
    - [`SessionResumptionConfigDict.transparent`](genai.html#genai.types.SessionResumptionConfigDict.transparent)
  + [`SlidingWindow`](genai.html#genai.types.SlidingWindow)
    - [`SlidingWindow.target_tokens`](genai.html#genai.types.SlidingWindow.target_tokens)
  + [`SlidingWindowDict`](genai.html#genai.types.SlidingWindowDict)
    - [`SlidingWindowDict.target_tokens`](genai.html#genai.types.SlidingWindowDict.target_tokens)
  + [`SpeechConfig`](genai.html#genai.types.SpeechConfig)
    - [`SpeechConfig.language_code`](genai.html#genai.types.SpeechConfig.language_code)
    - [`SpeechConfig.voice_config`](genai.html#genai.types.SpeechConfig.voice_config)
  + [`SpeechConfigDict`](genai.html#genai.types.SpeechConfigDict)
    - [`SpeechConfigDict.language_code`](genai.html#genai.types.SpeechConfigDict.language_code)
    - [`SpeechConfigDict.voice_config`](genai.html#genai.types.SpeechConfigDict.voice_config)
  + [`StartSensitivity`](genai.html#genai.types.StartSensitivity)
    - [`StartSensitivity.START_SENSITIVITY_HIGH`](genai.html#genai.types.StartSensitivity.START_SENSITIVITY_HIGH)
    - [`StartSensitivity.START_SENSITIVITY_LOW`](genai.html#genai.types.StartSensitivity.START_SENSITIVITY_LOW)
    - [`StartSensitivity.START_SENSITIVITY_UNSPECIFIED`](genai.html#genai.types.StartSensitivity.START_SENSITIVITY_UNSPECIFIED)
  + [`StyleReferenceConfig`](genai.html#genai.types.StyleReferenceConfig)
    - [`StyleReferenceConfig.style_description`](genai.html#genai.types.StyleReferenceConfig.style_description)
  + [`StyleReferenceConfigDict`](genai.html#genai.types.StyleReferenceConfigDict)
    - [`StyleReferenceConfigDict.style_description`](genai.html#genai.types.StyleReferenceConfigDict.style_description)
  + [`StyleReferenceImage`](genai.html#genai.types.StyleReferenceImage)
    - [`StyleReferenceImage.config`](genai.html#genai.types.StyleReferenceImage.config)
    - [`StyleReferenceImage.reference_id`](genai.html#genai.types.StyleReferenceImage.reference_id)
    - [`StyleReferenceImage.reference_image`](genai.html#genai.types.StyleReferenceImage.reference_image)
    - [`StyleReferenceImage.reference_type`](genai.html#genai.types.StyleReferenceImage.reference_type)
    - [`StyleReferenceImage.style_image_config`](genai.html#genai.types.StyleReferenceImage.style_image_config)
  + [`StyleReferenceImageDict`](genai.html#genai.types.StyleReferenceImageDict)
    - [`StyleReferenceImageDict.config`](genai.html#genai.types.StyleReferenceImageDict.config)
    - [`StyleReferenceImageDict.reference_id`](genai.html#genai.types.StyleReferenceImageDict.reference_id)
    - [`StyleReferenceImageDict.reference_image`](genai.html#genai.types.StyleReferenceImageDict.reference_image)
    - [`StyleReferenceImageDict.reference_type`](genai.html#genai.types.StyleReferenceImageDict.reference_type)
  + [`SubjectReferenceConfig`](genai.html#genai.types.SubjectReferenceConfig)
    - [`SubjectReferenceConfig.subject_description`](genai.html#genai.types.SubjectReferenceConfig.subject_description)
    - [`SubjectReferenceConfig.subject_type`](genai.html#genai.types.SubjectReferenceConfig.subject_type)
  + [`SubjectReferenceConfigDict`](genai.html#genai.types.SubjectReferenceConfigDict)
    - [`SubjectReferenceConfigDict.subject_description`](genai.html#genai.types.SubjectReferenceConfigDict.subject_description)
    - [`SubjectReferenceConfigDict.subject_type`](genai.html#genai.types.SubjectReferenceConfigDict.subject_type)
  + [`SubjectReferenceImage`](genai.html#genai.types.SubjectReferenceImage)
    - [`SubjectReferenceImage.config`](genai.html#genai.types.SubjectReferenceImage.config)
    - [`SubjectReferenceImage.reference_id`](genai.html#genai.types.SubjectReferenceImage.reference_id)
    - [`SubjectReferenceImage.reference_image`](genai.html#genai.types.SubjectReferenceImage.reference_image)
    - [`SubjectReferenceImage.reference_type`](genai.html#genai.types.SubjectReferenceImage.reference_type)
    - [`SubjectReferenceImage.subject_image_config`](genai.html#genai.types.SubjectReferenceImage.subject_image_config)
  + [`SubjectReferenceImageDict`](genai.html#genai.types.SubjectReferenceImageDict)
    - [`SubjectReferenceImageDict.config`](genai.html#genai.types.SubjectReferenceImageDict.config)
    - [`SubjectReferenceImageDict.reference_id`](genai.html#genai.types.SubjectReferenceImageDict.reference_id)
    - [`SubjectReferenceImageDict.reference_image`](genai.html#genai.types.SubjectReferenceImageDict.reference_image)
    - [`SubjectReferenceImageDict.reference_type`](genai.html#genai.types.SubjectReferenceImageDict.reference_type)
  + [`SubjectReferenceType`](genai.html#genai.types.SubjectReferenceType)
    - [`SubjectReferenceType.SUBJECT_TYPE_ANIMAL`](genai.html#genai.types.SubjectReferenceType.SUBJECT_TYPE_ANIMAL)
    - [`SubjectReferenceType.SUBJECT_TYPE_DEFAULT`](genai.html#genai.types.SubjectReferenceType.SUBJECT_TYPE_DEFAULT)
    - [`SubjectReferenceType.SUBJECT_TYPE_PERSON`](genai.html#genai.types.SubjectReferenceType.SUBJECT_TYPE_PERSON)
    - [`SubjectReferenceType.SUBJECT_TYPE_PRODUCT`](genai.html#genai.types.SubjectReferenceType.SUBJECT_TYPE_PRODUCT)
  + [`SupervisedHyperParameters`](genai.html#genai.types.SupervisedHyperParameters)
    - [`SupervisedHyperParameters.adapter_size`](genai.html#genai.types.SupervisedHyperParameters.adapter_size)
    - [`SupervisedHyperParameters.epoch_count`](genai.html#genai.types.SupervisedHyperParameters.epoch_count)
    - [`SupervisedHyperParameters.learning_rate_multiplier`](genai.html#genai.types.SupervisedHyperParameters.learning_rate_multiplier)
  + [`SupervisedHyperParametersDict`](genai.html#genai.types.SupervisedHyperParametersDict)
    - [`SupervisedHyperParametersDict.adapter_size`](genai.html#genai.types.SupervisedHyperParametersDict.adapter_size)
    - [`SupervisedHyperParametersDict.epoch_count`](genai.html#genai.types.SupervisedHyperParametersDict.epoch_count)
    - [`SupervisedHyperParametersDict.learning_rate_multiplier`](genai.html#genai.types.SupervisedHyperParametersDict.learning_rate_multiplier)
  + [`SupervisedTuningDataStats`](genai.html#genai.types.SupervisedTuningDataStats)
    - [`SupervisedTuningDataStats.total_billable_character_count`](genai.html#genai.types.SupervisedTuningDataStats.total_billable_character_count)
    - [`SupervisedTuningDataStats.total_billable_token_count`](genai.html#genai.types.SupervisedTuningDataStats.total_billable_token_count)
    - [`SupervisedTuningDataStats.total_truncated_example_count`](genai.html#genai.types.SupervisedTuningDataStats.total_truncated_example_count)
    - [`SupervisedTuningDataStats.total_tuning_character_count`](genai.html#genai.types.SupervisedTuningDataStats.total_tuning_character_count)
    - [`SupervisedTuningDataStats.truncated_example_indices`](genai.html#genai.types.SupervisedTuningDataStats.truncated_example_indices)
    - [`SupervisedTuningDataStats.tuning_dataset_example_count`](genai.html#genai.types.SupervisedTuningDataStats.tuning_dataset_example_count)
    - [`SupervisedTuningDataStats.tuning_step_count`](genai.html#genai.types.SupervisedTuningDataStats.tuning_step_count)
    - [`SupervisedTuningDataStats.user_dataset_examples`](genai.html#genai.types.SupervisedTuningDataStats.user_dataset_examples)
    - [`SupervisedTuningDataStats.user_input_token_distribution`](genai.html#genai.types.SupervisedTuningDataStats.user_input_token_distribution)
    - [`SupervisedTuningDataStats.user_message_per_example_distribution`](genai.html#genai.types.SupervisedTuningDataStats.user_message_per_example_distribution)
    - [`SupervisedTuningDataStats.user_output_token_distribution`](genai.html#genai.types.SupervisedTuningDataStats.user_output_token_distribution)
  + [`SupervisedTuningDataStatsDict`](genai.html#genai.types.SupervisedTuningDataStatsDict)
    - [`SupervisedTuningDataStatsDict.total_billable_character_count`](genai.html#genai.types.SupervisedTuningDataStatsDict.total_billable_character_count)
    - [`SupervisedTuningDataStatsDict.total_billable_token_count`](genai.html#genai.types.SupervisedTuningDataStatsDict.total_billable_token_count)
    - [`SupervisedTuningDataStatsDict.total_truncated_example_count`](genai.html#genai.types.SupervisedTuningDataStatsDict.total_truncated_example_count)
    - [`SupervisedTuningDataStatsDict.total_tuning_character_count`](genai.html#genai.types.SupervisedTuningDataStatsDict.total_tuning_character_count)
    - [`SupervisedTuningDataStatsDict.truncated_example_indices`](genai.html#genai.types.SupervisedTuningDataStatsDict.truncated_example_indices)
    - [`SupervisedTuningDataStatsDict.tuning_dataset_example_count`](genai.html#genai.types.SupervisedTuningDataStatsDict.tuning_dataset_example_count)
    - [`SupervisedTuningDataStatsDict.tuning_step_count`](genai.html#genai.types.SupervisedTuningDataStatsDict.tuning_step_count)
    - [`SupervisedTuningDataStatsDict.user_dataset_examples`](genai.html#genai.types.SupervisedTuningDataStatsDict.user_dataset_examples)
    - [`SupervisedTuningDataStatsDict.user_input_token_distribution`](genai.html#genai.types.SupervisedTuningDataStatsDict.user_input_token_distribution)
    - [`SupervisedTuningDataStatsDict.user_message_per_example_distribution`](genai.html#genai.types.SupervisedTuningDataStatsDict.user_message_per_example_distribution)
    - [`SupervisedTuningDataStatsDict.user_output_token_distribution`](genai.html#genai.types.SupervisedTuningDataStatsDict.user_output_token_distribution)
  + [`SupervisedTuningDatasetDistribution`](genai.html#genai.types.SupervisedTuningDatasetDistribution)
    - [`SupervisedTuningDatasetDistribution.billable_sum`](genai.html#genai.types.SupervisedTuningDatasetDistribution.billable_sum)
    - [`SupervisedTuningDatasetDistribution.buckets`](genai.html#genai.types.SupervisedTuningDatasetDistribution.buckets)
    - [`SupervisedTuningDatasetDistribution.max`](genai.html#genai.types.SupervisedTuningDatasetDistribution.max)
    - [`SupervisedTuningDatasetDistribution.mean`](genai.html#genai.types.SupervisedTuningDatasetDistribution.mean)
    - [`SupervisedTuningDatasetDistribution.median`](genai.html#genai.types.SupervisedTuningDatasetDistribution.median)
    - [`SupervisedTuningDatasetDistribution.min`](genai.html#genai.types.SupervisedTuningDatasetDistribution.min)
    - [`SupervisedTuningDatasetDistribution.p5`](genai.html#genai.types.SupervisedTuningDatasetDistribution.p5)
    - [`SupervisedTuningDatasetDistribution.p95`](genai.html#genai.types.SupervisedTuningDatasetDistribution.p95)
    - [`SupervisedTuningDatasetDistribution.sum`](genai.html#genai.types.SupervisedTuningDatasetDistribution.sum)
  + [`SupervisedTuningDatasetDistributionDatasetBucket`](genai.html#genai.types.SupervisedTuningDatasetDistributionDatasetBucket)
    - [`SupervisedTuningDatasetDistributionDatasetBucket.count`](genai.html#genai.types.SupervisedTuningDatasetDistributionDatasetBucket.count)
    - [`SupervisedTuningDatasetDistributionDatasetBucket.left`](genai.html#genai.types.SupervisedTuningDatasetDistributionDatasetBucket.left)
    - [`SupervisedTuningDatasetDistributionDatasetBucket.right`](genai.html#genai.types.SupervisedTuningDatasetDistributionDatasetBucket.right)
  + [`SupervisedTuningDatasetDistributionDatasetBucketDict`](genai.html#genai.types.SupervisedTuningDatasetDistributionDatasetBucketDict)
    - [`SupervisedTuningDatasetDistributionDatasetBucketDict.count`](genai.html#genai.types.SupervisedTuningDatasetDistributionDatasetBucketDict.count)
    - [`SupervisedTuningDatasetDistributionDatasetBucketDict.left`](genai.html#genai.types.SupervisedTuningDatasetDistributionDatasetBucketDict.left)
    - [`SupervisedTuningDatasetDistributionDatasetBucketDict.right`](genai.html#genai.types.SupervisedTuningDatasetDistributionDatasetBucketDict.right)
  + [`SupervisedTuningDatasetDistributionDict`](genai.html#genai.types.SupervisedTuningDatasetDistributionDict)
    - [`SupervisedTuningDatasetDistributionDict.billable_sum`](genai.html#genai.types.SupervisedTuningDatasetDistributionDict.billable_sum)
    - [`SupervisedTuningDatasetDistributionDict.buckets`](genai.html#genai.types.SupervisedTuningDatasetDistributionDict.buckets)
    - [`SupervisedTuningDatasetDistributionDict.max`](genai.html#genai.types.SupervisedTuningDatasetDistributionDict.max)
    - [`SupervisedTuningDatasetDistributionDict.mean`](genai.html#genai.types.SupervisedTuningDatasetDistributionDict.mean)
    - [`SupervisedTuningDatasetDistributionDict.median`](genai.html#genai.types.SupervisedTuningDatasetDistributionDict.median)
    - [`SupervisedTuningDatasetDistributionDict.min`](genai.html#genai.types.SupervisedTuningDatasetDistributionDict.min)
    - [`SupervisedTuningDatasetDistributionDict.p5`](genai.html#genai.types.SupervisedTuningDatasetDistributionDict.p5)
    - [`SupervisedTuningDatasetDistributionDict.p95`](genai.html#genai.types.SupervisedTuningDatasetDistributionDict.p95)
    - [`SupervisedTuningDatasetDistributionDict.sum`](genai.html#genai.types.SupervisedTuningDatasetDistributionDict.sum)
  + [`SupervisedTuningSpec`](genai.html#genai.types.SupervisedTuningSpec)
    - [`SupervisedTuningSpec.hyper_parameters`](genai.html#genai.types.SupervisedTuningSpec.hyper_parameters)
    - [`SupervisedTuningSpec.training_dataset_uri`](genai.html#genai.types.SupervisedTuningSpec.training_dataset_uri)
    - [`SupervisedTuningSpec.validation_dataset_uri`](genai.html#genai.types.SupervisedTuningSpec.validation_dataset_uri)
  + [`SupervisedTuningSpecDict`](genai.html#genai.types.SupervisedTuningSpecDict)
    - [`SupervisedTuningSpecDict.hyper_parameters`](genai.html#genai.types.SupervisedTuningSpecDict.hyper_parameters)
    - [`SupervisedTuningSpecDict.training_dataset_uri`](genai.html#genai.types.SupervisedTuningSpecDict.training_dataset_uri)
    - [`SupervisedTuningSpecDict.validation_dataset_uri`](genai.html#genai.types.SupervisedTuningSpecDict.validation_dataset_uri)
  + [`TestTableFile`](genai.html#genai.types.TestTableFile)
    - [`TestTableFile.comment`](genai.html#genai.types.TestTableFile.comment)
    - [`TestTableFile.parameter_names`](genai.html#genai.types.TestTableFile.parameter_names)
    - [`TestTableFile.test_method`](genai.html#genai.types.TestTableFile.test_method)
    - [`TestTableFile.test_table`](genai.html#genai.types.TestTableFile.test_table)
  + [`TestTableFileDict`](genai.html#genai.types.TestTableFileDict)
    - [`TestTableFileDict.comment`](genai.html#genai.types.TestTableFileDict.comment)
    - [`TestTableFileDict.parameter_names`](genai.html#genai.types.TestTableFileDict.parameter_names)
    - [`TestTableFileDict.test_method`](genai.html#genai.types.TestTableFileDict.test_method)
    - [`TestTableFileDict.test_table`](genai.html#genai.types.TestTableFileDict.test_table)
  + [`TestTableItem`](genai.html#genai.types.TestTableItem)
    - [`TestTableItem.exception_if_mldev`](genai.html#genai.types.TestTableItem.exception_if_mldev)
    - [`TestTableItem.exception_if_vertex`](genai.html#genai.types.TestTableItem.exception_if_vertex)
    - [`TestTableItem.has_union`](genai.html#genai.types.TestTableItem.has_union)
    - [`TestTableItem.ignore_keys`](genai.html#genai.types.TestTableItem.ignore_keys)
    - [`TestTableItem.name`](genai.html#genai.types.TestTableItem.name)
    - [`TestTableItem.override_replay_id`](genai.html#genai.types.TestTableItem.override_replay_id)
    - [`TestTableItem.parameters`](genai.html#genai.types.TestTableItem.parameters)
    - [`TestTableItem.skip_in_api_mode`](genai.html#genai.types.TestTableItem.skip_in_api_mode)
  + [`TestTableItemDict`](genai.html#genai.types.TestTableItemDict)
    - [`TestTableItemDict.exception_if_mldev`](genai.html#genai.types.TestTableItemDict.exception_if_mldev)
    - [`TestTableItemDict.exception_if_vertex`](genai.html#genai.types.TestTableItemDict.exception_if_vertex)
    - [`TestTableItemDict.has_union`](genai.html#genai.types.TestTableItemDict.has_union)
    - [`TestTableItemDict.ignore_keys`](genai.html#genai.types.TestTableItemDict.ignore_keys)
    - [`TestTableItemDict.name`](genai.html#genai.types.TestTableItemDict.name)
    - [`TestTableItemDict.override_replay_id`](genai.html#genai.types.TestTableItemDict.override_replay_id)
    - [`TestTableItemDict.parameters`](genai.html#genai.types.TestTableItemDict.parameters)
    - [`TestTableItemDict.skip_in_api_mode`](genai.html#genai.types.TestTableItemDict.skip_in_api_mode)
  + [`ThinkingConfig`](genai.html#genai.types.ThinkingConfig)
    - [`ThinkingConfig.include_thoughts`](genai.html#genai.types.ThinkingConfig.include_thoughts)
    - [`ThinkingConfig.thinking_budget`](genai.html#genai.types.ThinkingConfig.thinking_budget)
  + [`ThinkingConfigDict`](genai.html#genai.types.ThinkingConfigDict)
    - [`ThinkingConfigDict.include_thoughts`](genai.html#genai.types.ThinkingConfigDict.include_thoughts)
    - [`ThinkingConfigDict.thinking_budget`](genai.html#genai.types.ThinkingConfigDict.thinking_budget)
  + [`TokensInfo`](genai.html#genai.types.TokensInfo)
    - [`TokensInfo.role`](genai.html#genai.types.TokensInfo.role)
    - [`TokensInfo.token_ids`](genai.html#genai.types.TokensInfo.token_ids)
    - [`TokensInfo.tokens`](genai.html#genai.types.TokensInfo.tokens)
  + [`TokensInfoDict`](genai.html#genai.types.TokensInfoDict)
    - [`TokensInfoDict.role`](genai.html#genai.types.TokensInfoDict.role)
    - [`TokensInfoDict.token_ids`](genai.html#genai.types.TokensInfoDict.token_ids)
    - [`TokensInfoDict.tokens`](genai.html#genai.types.TokensInfoDict.tokens)
  + [`Tool`](genai.html#genai.types.Tool)
    - [`Tool.code_execution`](genai.html#genai.types.Tool.code_execution)
    - [`Tool.function_declarations`](genai.html#genai.types.Tool.function_declarations)
    - [`Tool.google_search`](genai.html#genai.types.Tool.google_search)
    - [`Tool.google_search_retrieval`](genai.html#genai.types.Tool.google_search_retrieval)
    - [`Tool.retrieval`](genai.html#genai.types.Tool.retrieval)
  + [`ToolCodeExecution`](genai.html#genai.types.ToolCodeExecution)
  + [`ToolCodeExecutionDict`](genai.html#genai.types.ToolCodeExecutionDict)
  + [`ToolConfig`](genai.html#genai.types.ToolConfig)
    - [`ToolConfig.function_calling_config`](genai.html#genai.types.ToolConfig.function_calling_config)
  + [`ToolConfigDict`](genai.html#genai.types.ToolConfigDict)
    - [`ToolConfigDict.function_calling_config`](genai.html#genai.types.ToolConfigDict.function_calling_config)
  + [`ToolDict`](genai.html#genai.types.ToolDict)
    - [`ToolDict.code_execution`](genai.html#genai.types.ToolDict.code_execution)
    - [`ToolDict.function_declarations`](genai.html#genai.types.ToolDict.function_declarations)
    - [`ToolDict.google_search`](genai.html#genai.types.ToolDict.google_search)
    - [`ToolDict.google_search_retrieval`](genai.html#genai.types.ToolDict.google_search_retrieval)
    - [`ToolDict.retrieval`](genai.html#genai.types.ToolDict.retrieval)
  + [`TrafficType`](genai.html#genai.types.TrafficType)
    - [`TrafficType.ON_DEMAND`](genai.html#genai.types.TrafficType.ON_DEMAND)
    - [`TrafficType.PROVISIONED_THROUGHPUT`](genai.html#genai.types.TrafficType.PROVISIONED_THROUGHPUT)
    - [`TrafficType.TRAFFIC_TYPE_UNSPECIFIED`](genai.html#genai.types.TrafficType.TRAFFIC_TYPE_UNSPECIFIED)
  + [`Transcription`](genai.html#genai.types.Transcription)
    - [`Transcription.finished`](genai.html#genai.types.Transcription.finished)
    - [`Transcription.text`](genai.html#genai.types.Transcription.text)
  + [`TranscriptionDict`](genai.html#genai.types.TranscriptionDict)
    - [`TranscriptionDict.finished`](genai.html#genai.types.TranscriptionDict.finished)
    - [`TranscriptionDict.text`](genai.html#genai.types.TranscriptionDict.text)
  + [`TunedModel`](genai.html#genai.types.TunedModel)
    - [`TunedModel.endpoint`](genai.html#genai.types.TunedModel.endpoint)
    - [`TunedModel.model`](genai.html#genai.types.TunedModel.model)
  + [`TunedModelDict`](genai.html#genai.types.TunedModelDict)
    - [`TunedModelDict.endpoint`](genai.html#genai.types.TunedModelDict.endpoint)
    - [`TunedModelDict.model`](genai.html#genai.types.TunedModelDict.model)
  + [`TunedModelInfo`](genai.html#genai.types.TunedModelInfo)
    - [`TunedModelInfo.base_model`](genai.html#genai.types.TunedModelInfo.base_model)
    - [`TunedModelInfo.create_time`](genai.html#genai.types.TunedModelInfo.create_time)
    - [`TunedModelInfo.update_time`](genai.html#genai.types.TunedModelInfo.update_time)
  + [`TunedModelInfoDict`](genai.html#genai.types.TunedModelInfoDict)
    - [`TunedModelInfoDict.base_model`](genai.html#genai.types.TunedModelInfoDict.base_model)
    - [`TunedModelInfoDict.create_time`](genai.html#genai.types.TunedModelInfoDict.create_time)
    - [`TunedModelInfoDict.update_time`](genai.html#genai.types.TunedModelInfoDict.update_time)
  + [`TuningDataStats`](genai.html#genai.types.TuningDataStats)
    - [`TuningDataStats.distillation_data_stats`](genai.html#genai.types.TuningDataStats.distillation_data_stats)
    - [`TuningDataStats.supervised_tuning_data_stats`](genai.html#genai.types.TuningDataStats.supervised_tuning_data_stats)
  + [`TuningDataStatsDict`](genai.html#genai.types.TuningDataStatsDict)
    - [`TuningDataStatsDict.distillation_data_stats`](genai.html#genai.types.TuningDataStatsDict.distillation_data_stats)
    - [`TuningDataStatsDict.supervised_tuning_data_stats`](genai.html#genai.types.TuningDataStatsDict.supervised_tuning_data_stats)
  + [`TuningDataset`](genai.html#genai.types.TuningDataset)
    - [`TuningDataset.examples`](genai.html#genai.types.TuningDataset.examples)
    - [`TuningDataset.gcs_uri`](genai.html#genai.types.TuningDataset.gcs_uri)
  + [`TuningDatasetDict`](genai.html#genai.types.TuningDatasetDict)
    - [`TuningDatasetDict.examples`](genai.html#genai.types.TuningDatasetDict.examples)
    - [`TuningDatasetDict.gcs_uri`](genai.html#genai.types.TuningDatasetDict.gcs_uri)
  + [`TuningExample`](genai.html#genai.types.TuningExample)
    - [`TuningExample.output`](genai.html#genai.types.TuningExample.output)
    - [`TuningExample.text_input`](genai.html#genai.types.TuningExample.text_input)
  + [`TuningExampleDict`](genai.html#genai.types.TuningExampleDict)
    - [`TuningExampleDict.output`](genai.html#genai.types.TuningExampleDict.output)
    - [`TuningExampleDict.text_input`](genai.html#genai.types.TuningExampleDict.text_input)
  + [`TuningJob`](genai.html#genai.types.TuningJob)
    - [`TuningJob.base_model`](genai.html#genai.types.TuningJob.base_model)
    - [`TuningJob.create_time`](genai.html#genai.types.TuningJob.create_time)
    - [`TuningJob.description`](genai.html#genai.types.TuningJob.description)
    - [`TuningJob.distillation_spec`](genai.html#genai.types.TuningJob.distillation_spec)
    - [`TuningJob.encryption_spec`](genai.html#genai.types.TuningJob.encryption_spec)
    - [`TuningJob.end_time`](genai.html#genai.types.TuningJob.end_time)
    - [`TuningJob.error`](genai.html#genai.types.TuningJob.error)
    - [`TuningJob.experiment`](genai.html#genai.types.TuningJob.experiment)
    - [`TuningJob.labels`](genai.html#genai.types.TuningJob.labels)
    - [`TuningJob.name`](genai.html#genai.types.TuningJob.name)
    - [`TuningJob.partner_model_tuning_spec`](genai.html#genai.types.TuningJob.partner_model_tuning_spec)
    - [`TuningJob.pipeline_job`](genai.html#genai.types.TuningJob.pipeline_job)
    - [`TuningJob.start_time`](genai.html#genai.types.TuningJob.start_time)
    - [`TuningJob.state`](genai.html#genai.types.TuningJob.state)
    - [`TuningJob.supervised_tuning_spec`](genai.html#genai.types.TuningJob.supervised_tuning_spec)
    - [`TuningJob.tuned_model`](genai.html#genai.types.TuningJob.tuned_model)
    - [`TuningJob.tuned_model_display_name`](genai.html#genai.types.TuningJob.tuned_model_display_name)
    - [`TuningJob.tuning_data_stats`](genai.html#genai.types.TuningJob.tuning_data_stats)
    - [`TuningJob.update_time`](genai.html#genai.types.TuningJob.update_time)
    - [`TuningJob.has_ended`](genai.html#genai.types.TuningJob.has_ended)
    - [`TuningJob.has_succeeded`](genai.html#genai.types.TuningJob.has_succeeded)
  + [`TuningJobDict`](genai.html#genai.types.TuningJobDict)
    - [`TuningJobDict.base_model`](genai.html#genai.types.TuningJobDict.base_model)
    - [`TuningJobDict.create_time`](genai.html#genai.types.TuningJobDict.create_time)
    - [`TuningJobDict.description`](genai.html#genai.types.TuningJobDict.description)
    - [`TuningJobDict.distillation_spec`](genai.html#genai.types.TuningJobDict.distillation_spec)
    - [`TuningJobDict.encryption_spec`](genai.html#genai.types.TuningJobDict.encryption_spec)
    - [`TuningJobDict.end_time`](genai.html#genai.types.TuningJobDict.end_time)
    - [`TuningJobDict.error`](genai.html#genai.types.TuningJobDict.error)
    - [`TuningJobDict.experiment`](genai.html#genai.types.TuningJobDict.experiment)
    - [`TuningJobDict.labels`](genai.html#genai.types.TuningJobDict.labels)
    - [`TuningJobDict.name`](genai.html#genai.types.TuningJobDict.name)
    - [`TuningJobDict.partner_model_tuning_spec`](genai.html#genai.types.TuningJobDict.partner_model_tuning_spec)
    - [`TuningJobDict.pipeline_job`](genai.html#genai.types.TuningJobDict.pipeline_job)
    - [`TuningJobDict.start_time`](genai.html#genai.types.TuningJobDict.start_time)
    - [`TuningJobDict.state`](genai.html#genai.types.TuningJobDict.state)
    - [`TuningJobDict.supervised_tuning_spec`](genai.html#genai.types.TuningJobDict.supervised_tuning_spec)
    - [`TuningJobDict.tuned_model`](genai.html#genai.types.TuningJobDict.tuned_model)
    - [`TuningJobDict.tuned_model_display_name`](genai.html#genai.types.TuningJobDict.tuned_model_display_name)
    - [`TuningJobDict.tuning_data_stats`](genai.html#genai.types.TuningJobDict.tuning_data_stats)
    - [`TuningJobDict.update_time`](genai.html#genai.types.TuningJobDict.update_time)
  + [`TuningValidationDataset`](genai.html#genai.types.TuningValidationDataset)
    - [`TuningValidationDataset.gcs_uri`](genai.html#genai.types.TuningValidationDataset.gcs_uri)
  + [`TuningValidationDatasetDict`](genai.html#genai.types.TuningValidationDatasetDict)
    - [`TuningValidationDatasetDict.gcs_uri`](genai.html#genai.types.TuningValidationDatasetDict.gcs_uri)
  + [`TurnCoverage`](genai.html#genai.types.TurnCoverage)
    - [`TurnCoverage.TURN_COVERAGE_UNSPECIFIED`](genai.html#genai.types.TurnCoverage.TURN_COVERAGE_UNSPECIFIED)
    - [`TurnCoverage.TURN_INCLUDES_ALL_INPUT`](genai.html#genai.types.TurnCoverage.TURN_INCLUDES_ALL_INPUT)
    - [`TurnCoverage.TURN_INCLUDES_ONLY_ACTIVITY`](genai.html#genai.types.TurnCoverage.TURN_INCLUDES_ONLY_ACTIVITY)
  + [`Type`](genai.html#genai.types.Type)
    - [`Type.ARRAY`](genai.html#genai.types.Type.ARRAY)
    - [`Type.BOOLEAN`](genai.html#genai.types.Type.BOOLEAN)
    - [`Type.INTEGER`](genai.html#genai.types.Type.INTEGER)
    - [`Type.NUMBER`](genai.html#genai.types.Type.NUMBER)
    - [`Type.OBJECT`](genai.html#genai.types.Type.OBJECT)
    - [`Type.STRING`](genai.html#genai.types.Type.STRING)
    - [`Type.TYPE_UNSPECIFIED`](genai.html#genai.types.Type.TYPE_UNSPECIFIED)
  + [`UpdateCachedContentConfig`](genai.html#genai.types.UpdateCachedContentConfig)
    - [`UpdateCachedContentConfig.expire_time`](genai.html#genai.types.UpdateCachedContentConfig.expire_time)
    - [`UpdateCachedContentConfig.http_options`](genai.html#genai.types.UpdateCachedContentConfig.http_options)
    - [`UpdateCachedContentConfig.ttl`](genai.html#genai.types.UpdateCachedContentConfig.ttl)
  + [`UpdateCachedContentConfigDict`](genai.html#genai.types.UpdateCachedContentConfigDict)
    - [`UpdateCachedContentConfigDict.expire_time`](genai.html#genai.types.UpdateCachedContentConfigDict.expire_time)
    - [`UpdateCachedContentConfigDict.http_options`](genai.html#genai.types.UpdateCachedContentConfigDict.http_options)
    - [`UpdateCachedContentConfigDict.ttl`](genai.html#genai.types.UpdateCachedContentConfigDict.ttl)
  + [`UpdateModelConfig`](genai.html#genai.types.UpdateModelConfig)
    - [`UpdateModelConfig.description`](genai.html#genai.types.UpdateModelConfig.description)
    - [`UpdateModelConfig.display_name`](genai.html#genai.types.UpdateModelConfig.display_name)
    - [`UpdateModelConfig.http_options`](genai.html#genai.types.UpdateModelConfig.http_options)
  + [`UpdateModelConfigDict`](genai.html#genai.types.UpdateModelConfigDict)
    - [`UpdateModelConfigDict.description`](genai.html#genai.types.UpdateModelConfigDict.description)
    - [`UpdateModelConfigDict.display_name`](genai.html#genai.types.UpdateModelConfigDict.display_name)
    - [`UpdateModelConfigDict.http_options`](genai.html#genai.types.UpdateModelConfigDict.http_options)
  + [`UploadFileConfig`](genai.html#genai.types.UploadFileConfig)
    - [`UploadFileConfig.display_name`](genai.html#genai.types.UploadFileConfig.display_name)
    - [`UploadFileConfig.http_options`](genai.html#genai.types.UploadFileConfig.http_options)
    - [`UploadFileConfig.mime_type`](genai.html#genai.types.UploadFileConfig.mime_type)
    - [`UploadFileConfig.name`](genai.html#genai.types.UploadFileConfig.name)
  + [`UploadFileConfigDict`](genai.html#genai.types.UploadFileConfigDict)
    - [`UploadFileConfigDict.display_name`](genai.html#genai.types.UploadFileConfigDict.display_name)
    - [`UploadFileConfigDict.http_options`](genai.html#genai.types.UploadFileConfigDict.http_options)
    - [`UploadFileConfigDict.mime_type`](genai.html#genai.types.UploadFileConfigDict.mime_type)
    - [`UploadFileConfigDict.name`](genai.html#genai.types.UploadFileConfigDict.name)
  + [`UpscaleImageConfig`](genai.html#genai.types.UpscaleImageConfig)
    - [`UpscaleImageConfig.http_options`](genai.html#genai.types.UpscaleImageConfig.http_options)
    - [`UpscaleImageConfig.include_rai_reason`](genai.html#genai.types.UpscaleImageConfig.include_rai_reason)
    - [`UpscaleImageConfig.output_compression_quality`](genai.html#genai.types.UpscaleImageConfig.output_compression_quality)
    - [`UpscaleImageConfig.output_mime_type`](genai.html#genai.types.UpscaleImageConfig.output_mime_type)
  + [`UpscaleImageConfigDict`](genai.html#genai.types.UpscaleImageConfigDict)
    - [`UpscaleImageConfigDict.http_options`](genai.html#genai.types.UpscaleImageConfigDict.http_options)
    - [`UpscaleImageConfigDict.include_rai_reason`](genai.html#genai.types.UpscaleImageConfigDict.include_rai_reason)
    - [`UpscaleImageConfigDict.output_compression_quality`](genai.html#genai.types.UpscaleImageConfigDict.output_compression_quality)
    - [`UpscaleImageConfigDict.output_mime_type`](genai.html#genai.types.UpscaleImageConfigDict.output_mime_type)
  + [`UpscaleImageParameters`](genai.html#genai.types.UpscaleImageParameters)
    - [`UpscaleImageParameters.config`](genai.html#genai.types.UpscaleImageParameters.config)
    - [`UpscaleImageParameters.image`](genai.html#genai.types.UpscaleImageParameters.image)
    - [`UpscaleImageParameters.model`](genai.html#genai.types.UpscaleImageParameters.model)
    - [`UpscaleImageParameters.upscale_factor`](genai.html#genai.types.UpscaleImageParameters.upscale_factor)
  + [`UpscaleImageParametersDict`](genai.html#genai.types.UpscaleImageParametersDict)
    - [`UpscaleImageParametersDict.config`](genai.html#genai.types.UpscaleImageParametersDict.config)
    - [`UpscaleImageParametersDict.image`](genai.html#genai.types.UpscaleImageParametersDict.image)
    - [`UpscaleImageParametersDict.model`](genai.html#genai.types.UpscaleImageParametersDict.model)
    - [`UpscaleImageParametersDict.upscale_factor`](genai.html#genai.types.UpscaleImageParametersDict.upscale_factor)
  + [`UpscaleImageResponse`](genai.html#genai.types.UpscaleImageResponse)
    - [`UpscaleImageResponse.generated_images`](genai.html#genai.types.UpscaleImageResponse.generated_images)
  + [`UpscaleImageResponseDict`](genai.html#genai.types.UpscaleImageResponseDict)
    - [`UpscaleImageResponseDict.generated_images`](genai.html#genai.types.UpscaleImageResponseDict.generated_images)
  + [`UsageMetadata`](genai.html#genai.types.UsageMetadata)
    - [`UsageMetadata.cache_tokens_details`](genai.html#genai.types.UsageMetadata.cache_tokens_details)
    - [`UsageMetadata.cached_content_token_count`](genai.html#genai.types.UsageMetadata.cached_content_token_count)
    - [`UsageMetadata.prompt_token_count`](genai.html#genai.types.UsageMetadata.prompt_token_count)
    - [`UsageMetadata.prompt_tokens_details`](genai.html#genai.types.UsageMetadata.prompt_tokens_details)
    - [`UsageMetadata.response_token_count`](genai.html#genai.types.UsageMetadata.response_token_count)
    - [`UsageMetadata.response_tokens_details`](genai.html#genai.types.UsageMetadata.response_tokens_details)
    - [`UsageMetadata.thoughts_token_count`](genai.html#genai.types.UsageMetadata.thoughts_token_count)
    - [`UsageMetadata.tool_use_prompt_token_count`](genai.html#genai.types.UsageMetadata.tool_use_prompt_token_count)
    - [`UsageMetadata.tool_use_prompt_tokens_details`](genai.html#genai.types.UsageMetadata.tool_use_prompt_tokens_details)
    - [`UsageMetadata.total_token_count`](genai.html#genai.types.UsageMetadata.total_token_count)
    - [`UsageMetadata.traffic_type`](genai.html#genai.types.UsageMetadata.traffic_type)
  + [`UsageMetadataDict`](genai.html#genai.types.UsageMetadataDict)
    - [`UsageMetadataDict.cache_tokens_details`](genai.html#genai.types.UsageMetadataDict.cache_tokens_details)
    - [`UsageMetadataDict.cached_content_token_count`](genai.html#genai.types.UsageMetadataDict.cached_content_token_count)
    - [`UsageMetadataDict.prompt_token_count`](genai.html#genai.types.UsageMetadataDict.prompt_token_count)
    - [`UsageMetadataDict.prompt_tokens_details`](genai.html#genai.types.UsageMetadataDict.prompt_tokens_details)
    - [`UsageMetadataDict.response_token_count`](genai.html#genai.types.UsageMetadataDict.response_token_count)
    - [`UsageMetadataDict.response_tokens_details`](genai.html#genai.types.UsageMetadataDict.response_tokens_details)
    - [`UsageMetadataDict.thoughts_token_count`](genai.html#genai.types.UsageMetadataDict.thoughts_token_count)
    - [`UsageMetadataDict.tool_use_prompt_token_count`](genai.html#genai.types.UsageMetadataDict.tool_use_prompt_token_count)
    - [`UsageMetadataDict.tool_use_prompt_tokens_details`](genai.html#genai.types.UsageMetadataDict.tool_use_prompt_tokens_details)
    - [`UsageMetadataDict.total_token_count`](genai.html#genai.types.UsageMetadataDict.total_token_count)
    - [`UsageMetadataDict.traffic_type`](genai.html#genai.types.UsageMetadataDict.traffic_type)
  + [`UserContent`](genai.html#genai.types.UserContent)
    - [`UserContent.parts`](genai.html#genai.types.UserContent.parts)
    - [`UserContent.role`](genai.html#genai.types.UserContent.role)
  + [`VertexAISearch`](genai.html#genai.types.VertexAISearch)
    - [`VertexAISearch.datastore`](genai.html#genai.types.VertexAISearch.datastore)
    - [`VertexAISearch.engine`](genai.html#genai.types.VertexAISearch.engine)
  + [`VertexAISearchDict`](genai.html#genai.types.VertexAISearchDict)
    - [`VertexAISearchDict.datastore`](genai.html#genai.types.VertexAISearchDict.datastore)
    - [`VertexAISearchDict.engine`](genai.html#genai.types.VertexAISearchDict.engine)
  + [`VertexRagStore`](genai.html#genai.types.VertexRagStore)
    - [`VertexRagStore.rag_corpora`](genai.html#genai.types.VertexRagStore.rag_corpora)
    - [`VertexRagStore.rag_resources`](genai.html#genai.types.VertexRagStore.rag_resources)
    - [`VertexRagStore.rag_retrieval_config`](genai.html#genai.types.VertexRagStore.rag_retrieval_config)
    - [`VertexRagStore.similarity_top_k`](genai.html#genai.types.VertexRagStore.similarity_top_k)
    - [`VertexRagStore.vector_distance_threshold`](genai.html#genai.types.VertexRagStore.vector_distance_threshold)
  + [`VertexRagStoreDict`](genai.html#genai.types.VertexRagStoreDict)
    - [`VertexRagStoreDict.rag_corpora`](genai.html#genai.types.VertexRagStoreDict.rag_corpora)
    - [`VertexRagStoreDict.rag_resources`](genai.html#genai.types.VertexRagStoreDict.rag_resources)
    - [`VertexRagStoreDict.rag_retrieval_config`](genai.html#genai.types.VertexRagStoreDict.rag_retrieval_config)
    - [`VertexRagStoreDict.similarity_top_k`](genai.html#genai.types.VertexRagStoreDict.similarity_top_k)
    - [`VertexRagStoreDict.vector_distance_threshold`](genai.html#genai.types.VertexRagStoreDict.vector_distance_threshold)
  + [`VertexRagStoreRagResource`](genai.html#genai.types.VertexRagStoreRagResource)
    - [`VertexRagStoreRagResource.rag_corpus`](genai.html#genai.types.VertexRagStoreRagResource.rag_corpus)
    - [`VertexRagStoreRagResource.rag_file_ids`](genai.html#genai.types.VertexRagStoreRagResource.rag_file_ids)
  + [`VertexRagStoreRagResourceDict`](genai.html#genai.types.VertexRagStoreRagResourceDict)
    - [`VertexRagStoreRagResourceDict.rag_corpus`](genai.html#genai.types.VertexRagStoreRagResourceDict.rag_corpus)
    - [`VertexRagStoreRagResourceDict.rag_file_ids`](genai.html#genai.types.VertexRagStoreRagResourceDict.rag_file_ids)
  + [`Video`](genai.html#genai.types.Video)
    - [`Video.mime_type`](genai.html#genai.types.Video.mime_type)
    - [`Video.uri`](genai.html#genai.types.Video.uri)
    - [`Video.video_bytes`](genai.html#genai.types.Video.video_bytes)
    - [`Video.save()`](genai.html#genai.types.Video.save)
    - [`Video.show()`](genai.html#genai.types.Video.show)
  + [`VideoDict`](genai.html#genai.types.VideoDict)
    - [`VideoDict.mime_type`](genai.html#genai.types.VideoDict.mime_type)
    - [`VideoDict.uri`](genai.html#genai.types.VideoDict.uri)
    - [`VideoDict.video_bytes`](genai.html#genai.types.VideoDict.video_bytes)
  + [`VideoMetadata`](genai.html#genai.types.VideoMetadata)
    - [`VideoMetadata.end_offset`](genai.html#genai.types.VideoMetadata.end_offset)
    - [`VideoMetadata.start_offset`](genai.html#genai.types.VideoMetadata.start_offset)
  + [`VideoMetadataDict`](genai.html#genai.types.VideoMetadataDict)
    - [`VideoMetadataDict.end_offset`](genai.html#genai.types.VideoMetadataDict.end_offset)
    - [`VideoMetadataDict.start_offset`](genai.html#genai.types.VideoMetadataDict.start_offset)
  + [`VoiceConfig`](genai.html#genai.types.VoiceConfig)
    - [`VoiceConfig.prebuilt_voice_config`](genai.html#genai.types.VoiceConfig.prebuilt_voice_config)
  + [`VoiceConfigDict`](genai.html#genai.types.VoiceConfigDict)
    - [`VoiceConfigDict.prebuilt_voice_config`](genai.html#genai.types.VoiceConfigDict.prebuilt_voice_config)


