# Models






Gemini 2.5 Pro Preview is now available for production use! [Learn more](https://blog.google/technology/google-deepmind/gemini-model-thinking-updates-march-2025/)



* [Home](https://ai.google.dev/)
* [Gemini API](https://ai.google.dev/gemini-api)
* [Models](https://ai.google.dev/gemini-api/docs)
* [API Reference](https://ai.google.dev/api)



Send feedback

# Models



The models endpoint provides a way for you to programmatically list the available models, and retrieve extended metadata such as supported functionality and context window sizing. Read more in [the Models guide](https://ai.google.dev/gemini-api/docs/models/gemini).

## Method: models.get




* [Endpoint](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Request body](#body.request_body)
* [Response body](#body.response_body)
* [Authorization scopes](#body.aspect)
* [Example request](#body.codeSnippets)
  + [Get](#body.codeSnippets.group)


Gets information about a specific `Model` such as its version number, token limits, [parameters](https://ai.google.dev/gemini-api/docs/models/generative-models#model-parameters) and other metadata. Refer to the [Gemini models guide](https://ai.google.dev/gemini-api/docs/models/gemini) for detailed model information.


### Endpoint

get

`https://generativelanguage.googleapis.com/v1beta/{name=models/*}`


  



### Path parameters

 `name` |
`string`


Required. The resource name of the model.

This name should match a model name returned by the `models.list` method.

Format: `models/{model}` It takes the form `models/{model}`.





### Request body

The request body must be empty.



### Example request

### Python

```
from google import genai

client = genai.Client()
model_info = client.models.get(model="gemini-2.0-flash")
print(model_info)[models.py](https://github.com/google-gemini/api-examples/blob/6779d2884a5e011173d827626a2c66d947c73cb9/python/models.py#L41-L45)
```



### Shell

```
curl https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash?key=$GEMINI_API_KEY[models](https://github.com/google-gemini/deprecated-generative-ai-python/blob/e179614c3144360e3fa2b34fba6eb13398ea98a7/samples/rest/models.sh#L9-L10).sh
```





### Response body

If successful, the response body contains an instance of `[Model](/api/models#Model)`.




