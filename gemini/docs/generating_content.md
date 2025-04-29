# Generating content






Gemini 2.5 Pro Preview is now available for production use! [Learn more](https://blog.google/technology/google-deepmind/gemini-model-thinking-updates-march-2025/)



* [Home](https://ai.google.dev/)
* [Gemini API](https://ai.google.dev/gemini-api)
* [Models](https://ai.google.dev/gemini-api/docs)
* [API Reference](https://ai.google.dev/api)



Send feedback

# Generating content



The Gemini API supports content generation with images, audio, code, tools, and more. For details on each of these features, read on and check out the task-focused sample code, or read the comprehensive guides.

* [Text generation](https://ai.google.dev/gemini-api/docs/text-generation)
* [Vision](https://ai.google.dev/gemini-api/docs/vision)
* [Audio](https://ai.google.dev/gemini-api/docs/audio)
* [Long context](https://ai.google.dev/gemini-api/docs/long-context)
* [Code execution](https://ai.google.dev/gemini-api/docs/code-execution)
* [JSON Mode](https://ai.google.dev/gemini-api/docs/json-mode)
* [Function calling](https://ai.google.dev/gemini-api/docs/function-calling)
* [System instructions](https://ai.google.dev/gemini-api/docs/system-instructions)

## Method: models.generateContent




* [Endpoint](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Request body](#body.request_body)
  + [JSON representation](#body.request_body.SCHEMA_REPRESENTATION)
* [Response body](#body.response_body)
* [Authorization scopes](#body.aspect)
* [Example request](#body.codeSnippets)
  + [Text](#body.codeSnippets.group)
  + [Image](#body.codeSnippets.group_1)
  + [Audio](#body.codeSnippets.group_2)
  + [Video](#body.codeSnippets.group_3)
  + [PDF](#body.codeSnippets.group_4)
  + [Chat](#body.codeSnippets.group_5)
  + [Cache](#body.codeSnippets.group_6)
  + [Tuned Model](#body.codeSnippets.group_7)
  + [JSON Mode](#body.codeSnippets.group_8)
  + [Code execution](#body.codeSnippets.group_9)
  + [Function Calling](#body.codeSnippets.group_10)
  + [Generation config](#body.codeSnippets.group_11)
  + [Safety Settings](#body.codeSnippets.group_12)
  + [System Instruction](#body.codeSnippets.group_13)


Generates a model response given an input `GenerateContentRequest`. Refer to the [text generation guide](https://ai.google.dev/gemini-api/docs/text-generation) for detailed usage information. Input capabilities differ between models, including tuned models. Refer to the [model guide](https://ai.google.dev/gemini-api/docs/models/gemini) and [tuning guide](https://ai.google.dev/gemini-api/docs/model-tuning) for details.


### Endpoint

post

`https://generativelanguage.googleapis.com/v1beta/{model=models/*}:generateContent`


  



### Path parameters

 `model` |
`string`


Required. The name of the `Model` to use for generating the completion.

Format: `models/{model}`. It takes the form `models/{model}`.





### Request body

The request body contains data with the following structure:

| Fields | |
| --- | --- |
 `contents[]` |
`object ([Content](/api/caching#Content))`


Required. The content of the current conversation with the model.

For single-turn queries, this is a single instance. For multi-turn queries like [chat](https://ai.google.dev/gemini-api/docs/text-generation#chat), this is a repeated field that contains the conversation history and the latest request.




 `tools[]` |
`object ([Tool](/api/caching#Tool))`


Optional. A list of `Tools` the `Model` may use to generate the next response.

A `Tool` is a piece of code that enables the system to interact with external systems to perform an action, or set of actions, outside of knowledge and scope of the `Model`. Supported `Tool`s are `Function` and `codeExecution`. Refer to the [Function calling](https://ai.google.dev/gemini-api/docs/function-calling) and the [Code execution](https://ai.google.dev/gemini-api/docs/code-execution) guides to learn more.




 `toolConfig` |
`object ([ToolConfig](/api/caching#ToolConfig))`


Optional. Tool configuration for any `Tool` specified in the request. Refer to the [Function calling guide](https://ai.google.dev/gemini-api/docs/function-calling#function_calling_mode) for a usage example.




 `safetySettings[]` |
`object ([SafetySetting](/api/generate-content#v1beta.SafetySetting))`


Optional. A list of unique `SafetySetting` instances for blocking unsafe content.

This will be enforced on the `GenerateContentRequest.contents` and `GenerateContentResponse.candidates`. There should not be more than one setting for each `SafetyCategory` type. The API will block any contents and responses that fail to meet the thresholds set by these settings. This list overrides the default settings for each `SafetyCategory` specified in the safetySettings. If there is no `SafetySetting` for a given `SafetyCategory` provided in the list, the API will use the default safety setting for that category. Harm categories HARM\_CATEGORY\_HATE\_SPEECH, HARM\_CATEGORY\_SEXUALLY\_EXPLICIT, HARM\_CATEGORY\_DANGEROUS\_CONTENT, HARM\_CATEGORY\_HARASSMENT, HARM\_CATEGORY\_CIVIC\_INTEGRITY are supported. Refer to the [guide](https://ai.google.dev/gemini-api/docs/safety-settings) for detailed information on available safety settings. Also refer to the [Safety guidance](https://ai.google.dev/gemini-api/docs/safety-guidance) to learn how to incorporate safety considerations in your AI applications.




 `systemInstruction` |
`object ([Content](/api/caching#Content))`


Optional. Developer set [system instruction(s)](https://ai.google.dev/gemini-api/docs/system-instructions). Currently, text only.




 `generationConfig` |
`object ([GenerationConfig](/api/generate-content#v1beta.GenerationConfig))`


Optional. Configuration options for model generation and outputs.




 `cachedContent` |
`string`


Optional. The name of the content [cached](https://ai.google.dev/gemini-api/docs/caching) to use as context to serve the prediction. Format: `cachedContents/{cachedContent}`







### Example request

### Text

### Python

```
from google import genai

client = genai.Client()
response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Write a story about a magic backpack."
)
print(response.text)[text_generation.py](https://github.com/google-gemini/api-examples/blob/16520aea9a9f109d1f616ba3400e87c1ece94cac/python/text_generation.py#L26-L32)
```



### Node.js

```
// Make sure to include the following import:
// import {GoogleGenAI} from '@google/genai';
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

const response = await ai.models.generateContent({
  model: "gemini-2.0-flash",
  contents: "Write a story about a magic backpack.",
});
console.log(response.text);[text_generation.js](https://github.com/google-gemini/api-examples/blob/16520aea9a9f109d1f616ba3400e87c1ece94cac/javascript/text_generation.js#L36-L44)
```



### Go

```
ctx := context.Background()
client, err := genai.NewClient(ctx, &genai.ClientConfig{
	APIKey:  os.Getenv("GEMINI_API_KEY"),
	Backend: genai.BackendGeminiAPI,
})
if err != nil {
	log.Fatal(err)
}
contents := []*genai.Content{
	genai.NewContentFromText("Write a story about a magic backpack.", "user"),
}
response, err := client.Models.GenerateContent(ctx, "gemini-2.0-flash", contents, nil)
if err != nil {
	log.Fatal(err)
}
printResponse(response)[text_generation.go](https://github.com/google-gemini/api-examples/blob/16520aea9a9f109d1f616ba3400e87c1ece94cac/go/text_generation.go#L16-L31)
```



### Shell

```
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts":[{"text": "Write a story about a magic backpack."}]
        }]
       }' 2> /dev/null[text_generation.sh](https://github.com/google-gemini/deprecated-generative-ai-python/blob/e179614c3144360e3fa2b34fba6eb13398ea98a7/samples/rest/text_generation.sh#L21-L29)
```



### Kotlin

```
val generativeModel =
    GenerativeModel(
        // Specify a Gemini model appropriate for your use case
        modelName = "gemini-1.5-flash",
        // Access your API key as a Build Configuration variable (see "Set up your API key" above)
        apiKey = BuildConfig.apiKey)

val prompt = "Write a story about a magic backpack."
val response = generativeModel.generateContent(prompt)
print(response.text)[text_generation.kt](https://github.com/google-gemini/generative-ai-android/blob/3596cab996d0e09bf05e460c8307233ca3c14e46/samples/src/main/java/com/google/ai/client/generative/samples/text_generation.kt#L35-L44)
```



### Swift

```
let generativeModel =
  GenerativeModel(
    // Specify a Gemini model appropriate for your use case
    name: "gemini-1.5-flash",
    // Access your API key from your on-demand resource .plist file (see "Set up your API key"
    // above)
    apiKey: APIKey.default
  )

let prompt = "Write a story about a magic backpack."
let response = try await generativeModel.generateContent(prompt)
if let text = response.text {
  print(text)
}[TextGeneration.swift](https://github.com/google-gemini/generative-ai-swift/blob/31d3eb8b399deb288373b99953a8dec5c11bcb57/samples/TextGeneration.swift#L36-L49)
```



### Dart

```
// Make sure to include this import:
// import 'package:google_generative_ai/google_generative_ai.dart';
final model = GenerativeModel(
  model: 'gemini-1.5-flash',
  apiKey: apiKey,
);
final prompt = 'Write a story about a magic backpack.';

final response = await model.generateContent([Content.text(prompt)]);
print(response.text);[text_generation.dart](https://github.com/google-gemini/generative-ai-dart/blob/76ae8f89eed4789af0be9e7876d0089909abc419/samples/dart/bin/text_generation.dart#L30-L39)
```



### Java

```
// Specify a Gemini model appropriate for your use case
GenerativeModel gm =
    new GenerativeModel(
        /* modelName */ "gemini-1.5-flash",
        // Access your API key as a Build Configuration variable (see "Set up your API key"
        // above)
        /* apiKey */ BuildConfig.apiKey);
GenerativeModelFutures model = GenerativeModelFutures.from(gm);

Content content =
    new Content.Builder().addText("Write a story about a magic backpack.").build();

// For illustrative purposes only. You should use an executor that fits your needs.
Executor executor = Executors.newSingleThreadExecutor();

ListenableFuture<GenerateContentResponse> response = model.generateContent(content);
Futures.addCallback(
    response,
    new FutureCallback<GenerateContentResponse>() {
      @Override
      public void onSuccess(GenerateContentResponse result) {
        String resultText = result.getText();
        System.out.println(resultText);
      }

      @Override
      public void onFailure(Throwable t) {
        t.printStackTrace();
      }
    },
    executor);[text_generation.java](https://github.com/google-gemini/generative-ai-android/blob/3596cab996d0e09bf05e460c8307233ca3c14e46/samples/src/main/java/com/google/ai/client/generative/samples/java/text_generation.java#L44-L74)
```





### Image

### Python

```
from google import genai
import PIL.Image

client = genai.Client()
organ = PIL.Image.open(media / "organ.jpg")
response = client.models.generate_content(
    model="gemini-2.0-flash", contents=["Tell me about this instrument", organ]
)
print(response.text)[text_generation.py](https://github.com/google-gemini/api-examples/blob/16520aea9a9f109d1f616ba3400e87c1ece94cac/python/text_generation.py#L50-L58)
```



### Node.js

```
// Make sure to include the following import:
// import {GoogleGenAI} from '@google/genai';
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

const organ = await ai.files.upload({
  file: path.join(media, "organ.jpg"),
});

const response = await ai.models.generateContent({
  model: "gemini-2.0-flash",
  contents: [
    createUserContent([
      "Tell me about this instrument", 
      createPartFromUri(organ.uri, organ.mimeType)
    ]),
  ],
});
console.log(response.text);[text_generation.js](https://github.com/google-gemini/api-examples/blob/16520aea9a9f109d1f616ba3400e87c1ece94cac/javascript/text_generation.js#L70-L87)
```



### Go

```
ctx := context.Background()
client, err := genai.NewClient(ctx, &genai.ClientConfig{
	APIKey:  os.Getenv("GEMINI_API_KEY"),
	Backend: genai.BackendGeminiAPI,
})
if err != nil {
	log.Fatal(err)
}

file, err := client.Files.UploadFromPath(
	ctx, 
	filepath.Join(getMedia(), "organ.jpg"), 
	&genai.UploadFileConfig{
		MIMEType : "image/jpeg",
	},
)
if err != nil {
	log.Fatal(err)
}
parts := []*genai.Part{
	genai.NewPartFromText("Tell me about this instrument"),
	genai.NewPartFromURI(file.URI, file.MIMEType),
}
contents := []*genai.Content{
	genai.NewContentFromParts(parts, "user"),
}

response, err := client.Models.GenerateContent(ctx, "gemini-2.0-flash", contents, nil)
if err != nil {
	log.Fatal(err)
}
printResponse(response)[text_generation.go](https://github.com/google-gemini/api-examples/blob/16520aea9a9f109d1f616ba3400e87c1ece94cac/go/text_generation.go#L66-L97)
```



### Shell

```
# Use a temporary file to hold the base64 encoded image data
TEMP_B64=$(mktemp)
trap 'rm -f "$TEMP_B64"' EXIT
base64 $B64FLAGS $IMG_PATH > "$TEMP_B64"

# Use a temporary file to hold the JSON payload
TEMP_JSON=$(mktemp)
trap 'rm -f "$TEMP_JSON"' EXIT

cat > "$TEMP_JSON" << EOF
{
  "contents": [{
    "parts":[
      {"text": "Tell me about this instrument"},
      {
        "inline_data": {
          "mime_type":"image/jpeg",
          "data": "$(cat "$TEMP_B64")"
        }
      }
    ]
  }]
}
EOF

curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d "@$TEMP_JSON" 2> /dev/null[text_generation.sh](https://github.com/google-gemini/deprecated-generative-ai-python/blob/e179614c3144360e3fa2b34fba6eb13398ea98a7/samples/rest/text_generation.sh#L41-L70)
```



### Kotlin

```
val generativeModel =
    GenerativeModel(
        // Specify a Gemini model appropriate for your use case
        modelName = "gemini-1.5-flash",
        // Access your API key as a Build Configuration variable (see "Set up your API key" above)
        apiKey = BuildConfig.apiKey)

val image: Bitmap = BitmapFactory.decodeResource(context.resources, R.drawable.image)
val inputContent = content {
  image(image)
  text("What's in this picture?")
}

val response = generativeModel.generateContent(inputContent)
print(response.text)[text_generation.kt](https://github.com/google-gemini/generative-ai-android/blob/3596cab996d0e09bf05e460c8307233ca3c14e46/samples/src/main/java/com/google/ai/client/generative/samples/text_generation.kt#L66-L80)
```



### Swift

```
let generativeModel =
  GenerativeModel(
    // Specify a Gemini model appropriate for your use case
    name: "gemini-1.5-flash",
    // Access your API key from your on-demand resource .plist file (see "Set up your API key"
    // above)
    apiKey: APIKey.default
  )

guard let image = UIImage(systemName: "cloud.sun") else { fatalError() }

let prompt = "What's in this picture?"

let response = try await generativeModel.generateContent(image, prompt)
if let text = response.text {
  print(text)
}[TextGeneration.swift](https://github.com/google-gemini/generative-ai-swift/blob/31d3eb8b399deb288373b99953a8dec5c11bcb57/samples/TextGeneration.swift#L76-L92)
```



### Dart

```
// Make sure to include this import:
// import 'package:google_generative_ai/google_generative_ai.dart';
final model = GenerativeModel(
  model: 'gemini-1.5-flash',
  apiKey: apiKey,
);

Future<DataPart> fileToPart(String mimeType, String path) async {
  return DataPart(mimeType, await File(path).readAsBytes());
}

final prompt = 'Describe how this product might be manufactured.';
final image = await fileToPart('image/jpeg', 'resources/jetpack.jpg');

final response = await model.generateContent([
  Content.multi([TextPart(prompt), image])
]);
print(response.text);[text_generation.dart](https://github.com/google-gemini/generative-ai-dart/blob/76ae8f89eed4789af0be9e7876d0089909abc419/samples/dart/bin/text_generation.dart#L62-L79)
```



### Java

```
// Specify a Gemini model appropriate for your use case
GenerativeModel gm =
    new GenerativeModel(
        /* modelName */ "gemini-1.5-flash",
        // Access your API key as a Build Configuration variable (see "Set up your API key"
        // above)
        /* apiKey */ BuildConfig.apiKey);
GenerativeModelFutures model = GenerativeModelFutures.from(gm);

Bitmap image = BitmapFactory.decodeResource(context.getResources(), R.drawable.image);

Content content =
    new Content.Builder()
        .addText("What's different between these pictures?")
        .addImage(image)
        .build();

// For illustrative purposes only. You should use an executor that fits your needs.
Executor executor = Executors.newSingleThreadExecutor();

ListenableFuture<GenerateContentResponse> response = model.generateContent(content);
Futures.addCallback(
    response,
    new FutureCallback<GenerateContentResponse>() {
      @Override
      public void onSuccess(GenerateContentResponse result) {
        String resultText = result.getText();
        System.out.println(resultText);
      }

      @Override
      public void onFailure(Throwable t) {
        t.printStackTrace();
      }
    },
    executor);[text_generation.java](https://github.com/google-gemini/generative-ai-android/blob/3596cab996d0e09bf05e460c8307233ca3c14e46/samples/src/main/java/com/google/ai/client/generative/samples/java/text_generation.java#L124-L159)
```





### Audio

### Python

```
from google import genai

client = genai.Client()
sample_audio = client.files.upload(file=media / "sample.mp3")
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["Give me a summary of this audio file.", sample_audio],
)
print(response.text)[text_generation.py](https://github.com/google-gemini/api-examples/blob/16520aea9a9f109d1f616ba3400e87c1ece94cac/python/text_generation.py#L118-L126)
```



### Node.js

```
// Make sure to include the following import:
// import {GoogleGenAI} from '@google/genai';
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

const audio = await ai.files.upload({
  file: path.join(media, "sample.mp3"),
});

const response = await ai.models.generateContent({
  model: "gemini-2.0-flash",
  contents: [
    createUserContent([
      "Give me a summary of this audio file.",
      createPartFromUri(audio.uri, audio.mimeType),
    ]),
  ],
});
console.log(response.text);[text_generation.js](https://github.com/google-gemini/api-examples/blob/16520aea9a9f109d1f616ba3400e87c1ece94cac/javascript/text_generation.js#L185-L202)
```



### Shell

```
# Use File API to upload audio data to API request.
MIME_TYPE=$(file -b --mime-type "${AUDIO_PATH}")
NUM_BYTES=$(wc -c < "${AUDIO_PATH}")
DISPLAY_NAME=AUDIO

tmp_header_file=upload-header.tmp

# Initial resumable request defining metadata.
# The upload url is in the response headers dump them to a file.
curl "${BASE_URL}/upload/v1beta/files?key=${GEMINI_API_KEY}" \
  -D upload-header.tmp \
  -H "X-Goog-Upload-Protocol: resumable" \
  -H "X-Goog-Upload-Command: start" \
  -H "X-Goog-Upload-Header-Content-Length: ${NUM_BYTES}" \
  -H "X-Goog-Upload-Header-Content-Type: ${MIME_TYPE}" \
  -H "Content-Type: application/json" \
  -d "{'file': {'display_name': '${DISPLAY_NAME}'}}" 2> /dev/null

upload_url=$(grep -i "x-goog-upload-url: " "${tmp_header_file}" | cut -d" " -f2 | tr -d "\r")
rm "${tmp_header_file}"

# Upload the actual bytes.
curl "${upload_url}" \
  -H "Content-Length: ${NUM_BYTES}" \
  -H "X-Goog-Upload-Offset: 0" \
  -H "X-Goog-Upload-Command: upload, finalize" \
  --data-binary "@${AUDIO_PATH}" 2> /dev/null > file_info.json

file_uri=$(jq ".file.uri" file_info.json)
echo file_uri=$file_uri

curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts":[
          {"text": "Please describe this file."},
          {"file_data":{"mime_type": "audio/mpeg", "file_uri": '$file_uri'}}]
        }]
       }' 2> /dev/null > response.json

cat response.json
echo

jq ".candidates[].content.parts[].text" response.json[text_generation.sh](https://github.com/google-gemini/deprecated-generative-ai-python/blob/e179614c3144360e3fa2b34fba6eb13398ea98a7/samples/rest/text_generation.sh#L174-L220)
```





### Video

### Python

```
from google import genai
import time

client = genai.Client()
# Video clip (CC BY 3.0) from https://peach.blender.org/download/
myfile = client.files.upload(file=media / "Big_Buck_Bunny.mp4")
print(f"{myfile=}")

# Poll until the video file is completely processed (state becomes ACTIVE).
while not myfile.state or myfile.state.name != "ACTIVE":
    print("Processing video...")
    print("File state:", myfile.state)
    time.sleep(5)
    myfile = client.files.get(name=myfile.name)

response = client.models.generate_content(
    model="gemini-2.0-flash", contents=[myfile, "Describe this video clip"]
)
print(f"{response.text=}")[text_generation.py](https://github.com/google-gemini/api-examples/blob/16520aea9a9f109d1f616ba3400e87c1ece94cac/python/text_generation.py#L146-L164)
```



### Node.js

```
// Make sure to include the following import:
// import {GoogleGenAI} from '@google/genai';
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

let video = await ai.files.upload({
  file: path.join(media, 'Big_Buck_Bunny.mp4'),
});

// Poll until the video file is completely processed (state becomes ACTIVE).
while (!video.state || video.state.toString() !== 'ACTIVE') {
  console.log('Processing video...');
  console.log('File state: ', video.state);
  await sleep(5000);
  video = await ai.files.get({name: video.name});
}

const response = await ai.models.generateContent({
  model: "gemini-2.0-flash",
  contents: [
    createUserContent([
      "Describe this video clip",
      createPartFromUri(video.uri, video.mimeType),
    ]),
  ],
});
console.log(response.text);[text_generation.js](https://github.com/google-gemini/api-examples/blob/16520aea9a9f109d1f616ba3400e87c1ece94cac/javascript/text_generation.js#L237-L262)
```



### Go

```
ctx := context.Background()
client, err := genai.NewClient(ctx, &genai.ClientConfig{
	APIKey:  os.Getenv("GEMINI_API_KEY"),
	Backend: genai.BackendGeminiAPI,
})
if err != nil {
	log.Fatal(err)
}

file, err := client.Files.UploadFromPath(
	ctx, 
	filepath.Join(getMedia(), "Big_Buck_Bunny.mp4"), 
	&genai.UploadFileConfig{
		MIMEType : "video/mp4",
	},
)
if err != nil {
	log.Fatal(err)
}

// Poll until the video file is completely processed (state becomes ACTIVE).
for file.State == genai.FileStateUnspecified || file.State != genai.FileStateActive {
	fmt.Println("Processing video...")
	fmt.Println("File state:", file.State)
	time.Sleep(5 * time.Second)

	file, err = client.Files.Get(ctx, file.Name, nil)
	if err != nil {
		log.Fatal(err)
	}
}

parts := []*genai.Part{
	genai.NewPartFromText("Describe this video clip"),
	genai.NewPartFromURI(file.URI, file.MIMEType),
}

contents := []*genai.Content{
	genai.NewContentFromParts(parts, "user"),
}

response, err := client.Models.GenerateContent(ctx, "gemini-2.0-flash", contents, nil)
if err != nil {
	log.Fatal(err)
}
printResponse(response)[text_generation.go](https://github.com/google-gemini/api-examples/blob/16520aea9a9f109d1f616ba3400e87c1ece94cac/go/text_generation.go#L342-L387)
```



### Shell

```
# Use File API to upload audio data to API request.
MIME_TYPE=$(file -b --mime-type "${VIDEO_PATH}")
NUM_BYTES=$(wc -c < "${VIDEO_PATH}")
DISPLAY_NAME=VIDEO

# Initial resumable request defining metadata.
# The upload url is in the response headers dump them to a file.
curl "${BASE_URL}/upload/v1beta/files?key=${GEMINI_API_KEY}" \
  -D "${tmp_header_file}" \
  -H "X-Goog-Upload-Protocol: resumable" \
  -H "X-Goog-Upload-Command: start" \
  -H "X-Goog-Upload-Header-Content-Length: ${NUM_BYTES}" \
  -H "X-Goog-Upload-Header-Content-Type: ${MIME_TYPE}" \
  -H "Content-Type: application/json" \
  -d "{'file': {'display_name': '${DISPLAY_NAME}'}}" 2> /dev/null

upload_url=$(grep -i "x-goog-upload-url: " "${tmp_header_file}" | cut -d" " -f2 | tr -d "\r")
rm "${tmp_header_file}"

# Upload the actual bytes.
curl "${upload_url}" \
  -H "Content-Length: ${NUM_BYTES}" \
  -H "X-Goog-Upload-Offset: 0" \
  -H "X-Goog-Upload-Command: upload, finalize" \
  --data-binary "@${VIDEO_PATH}" 2> /dev/null > file_info.json

file_uri=$(jq ".file.uri" file_info.json)
echo file_uri=$file_uri

state=$(jq ".file.state" file_info.json)
echo state=$state

name=$(jq ".file.name" file_info.json)
echo name=$name

while [[ "($state)" = *"PROCESSING"* ]];
do
  echo "Processing video..."
  sleep 5
  # Get the file of interest to check state
  curl https://generativelanguage.googleapis.com/v1beta/files/$name > file_info.json
  state=$(jq ".file.state" file_info.json)
done

curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts":[
          {"text": "Transcribe the audio from this video, giving timestamps for salient events in the video. Also provide visual descriptions."},
          {"file_data":{"mime_type": "video/mp4", "file_uri": '$file_uri'}}]
        }]
       }' 2> /dev/null > response.json

cat response.json
echo

jq ".candidates[].content.parts[].text" response.json[text_generation.sh](https://github.com/google-gemini/deprecated-generative-ai-python/blob/e179614c3144360e3fa2b34fba6eb13398ea98a7/samples/rest/text_generation.sh#L272-L331)
```





### PDF

### Python

```
from google import genai

client = genai.Client()
sample_pdf = client.files.upload(file=media / "test.pdf")
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["Give me a summary of this document:", sample_pdf],
)
print(f"{response.text=}")[text_generation.py](https://github.com/google-gemini/api-examples/blob/16520aea9a9f109d1f616ba3400e87c1ece94cac/python/text_generation.py#L194-L202)
```



### Shell

```
MIME_TYPE=$(file -b --mime-type "${PDF_PATH}")
NUM_BYTES=$(wc -c < "${PDF_PATH}")
DISPLAY_NAME=TEXT


echo $MIME_TYPE
tmp_header_file=upload-header.tmp

# Initial resumable request defining metadata.
# The upload url is in the response headers dump them to a file.
curl "${BASE_URL}/upload/v1beta/files?key=${GEMINI_API_KEY}" \
  -D upload-header.tmp \
  -H "X-Goog-Upload-Protocol: resumable" \
  -H "X-Goog-Upload-Command: start" \
  -H "X-Goog-Upload-Header-Content-Length: ${NUM_BYTES}" \
  -H "X-Goog-Upload-Header-Content-Type: ${MIME_TYPE}" \
  -H "Content-Type: application/json" \
  -d "{'file': {'display_name': '${DISPLAY_NAME}'}}" 2> /dev/null

upload_url=$(grep -i "x-goog-upload-url: " "${tmp_header_file}" | cut -d" " -f2 | tr -d "\r")
rm "${tmp_header_file}"

# Upload the actual bytes.
curl "${upload_url}" \
  -H "Content-Length: ${NUM_BYTES}" \
  -H "X-Goog-Upload-Offset: 0" \
  -H "X-Goog-Upload-Command: upload, finalize" \
  --data-binary "@${PDF_PATH}" 2> /dev/null > file_info.json

file_uri=$(jq ".file.uri" file_info.json)
echo file_uri=$file_uri

# Now generate content using that file
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts":[
          {"text": "Can you add a few more lines to this poem?"},
          {"file_data":{"mime_type": "application/pdf", "file_uri": '$file_uri'}}]
        }]
       }' 2> /dev/null > response.json

cat response.json
echo

jq ".candidates[].content.parts[].text" response.json[text_generation.sh](https://github.com/google-gemini/deprecated-generative-ai-python/blob/e179614c3144360e3fa2b34fba6eb13398ea98a7/samples/rest/text_generation.sh#L393-L441)
```





### Chat

### Python

```
from google import genai
from google.genai import types

client = genai.Client()
# Pass initial history using the "history" argument
chat = client.chats.create(
    model="gemini-2.0-flash",
    history=[
        types.Content(role="user", parts=[types.Part(text="Hello")]),
        types.Content(
            role="model",
            parts=[
                types.Part(
                    text="Great to meet you. What would you like to know?"
                )
            ],
        ),
    ],
)
response = chat.send_message(message="I have 2 dogs in my house.")
print(response.text)
response = chat.send_message(message="How many paws are in my house?")
print(response.text)[chat.py](https://github.com/google-gemini/api-examples/blob/16520aea9a9f109d1f616ba3400e87c1ece94cac/python/chat.py#L25-L47)
```



### Node.js

```
// Make sure to include the following import:
// import {GoogleGenAI} from '@google/genai';
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
const chat = ai.chats.create({
  model: "gemini-2.0-flash",
  history: [
    {
      role: "user",
      parts: [{ text: "Hello" }],
    },
    {
      role: "model",
      parts: [{ text: "Great to meet you. What would you like to know?" }],
    },
  ],
});

const response1 = await chat.sendMessage({
  message: "I have 2 dogs in my house.",
});
console.log("Chat response 1:", response1.text);

const response2 = await chat.sendMessage({
  message: "How many paws are in my house?",
});
console.log("Chat response 2:", response2.text);[chat.js](https://github.com/google-gemini/api-examples/blob/16520aea9a9f109d1f616ba3400e87c1ece94cac/javascript/chat.js#L33-L58)
```



### Go

```
ctx := context.Background()
client, err := genai.NewClient(ctx, &genai.ClientConfig{
	APIKey:  os.Getenv("GEMINI_API_KEY"),
	Backend: genai.BackendGeminiAPI,
})
if err != nil {
	log.Fatal(err)
}

// Pass initial history using the History field.
history := []*genai.Content{
	genai.NewContentFromText("Hello", "user"),
	genai.NewContentFromText("Great to meet you. What would you like to know?", "model"),
}

chat, err := client.Chats.Create(ctx, "gemini-2.0-flash", nil, history)
if err != nil {
	log.Fatal(err)
}

firstResp, err := chat.SendMessage(ctx, genai.Part{Text: "I have 2 dogs in my house."})
if err != nil {
	log.Fatal(err)
}
fmt.Println(firstResp.Text())

secondResp, err := chat.SendMessage(ctx, genai.Part{Text: "How many paws are in my house?"})
if err != nil {
	log.Fatal(err)
}
fmt.Println(secondResp.Text())[chat.go](https://github.com/google-gemini/api-examples/blob/16520aea9a9f109d1f616ba3400e87c1ece94cac/go/chat.go#L16-L46)
```



### Shell

```
curl https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [
        {"role":"user",
         "parts":[{
           "text": "Hello"}]},
        {"role": "model",
         "parts":[{
           "text": "Great to meet you. What would you like to know?"}]},
        {"role":"user",
         "parts":[{
           "text": "I have two dogs in my house. How many paws are in my house?"}]},
      ]
    }' 2> /dev/null | grep "text"[chat.sh](https://github.com/google-gemini/deprecated-generative-ai-python/blob/e179614c3144360e3fa2b34fba6eb13398ea98a7/samples/rest/chat.sh#L7-L23)
```



### Kotlin

```
val generativeModel =
    GenerativeModel(
        // Specify a Gemini model appropriate for your use case
        modelName = "gemini-1.5-flash",
        // Access your API key as a Build Configuration variable (see "Set up your API key" above)
        apiKey = BuildConfig.apiKey)

val chat =
    generativeModel.startChat(
        history =
            listOf(
                content(role = "user") { text("Hello, I have 2 dogs in my house.") },
                content(role = "model") {
                  text("Great to meet you. What would you like to know?")
                }))

val response = chat.sendMessage("How many paws are in my house?")
print(response.text)[chat.kt](https://github.com/google-gemini/generative-ai-android/blob/3596cab996d0e09bf05e460c8307233ca3c14e46/samples/src/main/java/com/google/ai/client/generative/samples/chat.kt#L35-L52)
```



### Swift

```
let generativeModel =
  GenerativeModel(
    // Specify a Gemini model appropriate for your use case
    name: "gemini-1.5-flash",
    // Access your API key from your on-demand resource .plist file (see "Set up your API key"
    // above)
    apiKey: APIKey.default
  )

// Optionally specify existing chat history
let history = [
  ModelContent(role: "user", parts: "Hello, I have 2 dogs in my house."),
  ModelContent(role: "model", parts: "Great to meet you. What would you like to know?"),
]

// Initialize the chat with optional chat history
let chat = generativeModel.startChat(history: history)

// To generate text output, call sendMessage and pass in the message
let response = try await chat.sendMessage("How many paws are in my house?")
if let text = response.text {
  print(text)
}[ChatSnippets.swift](https://github.com/google-gemini/generative-ai-swift/blob/31d3eb8b399deb288373b99953a8dec5c11bcb57/samples/ChatSnippets.swift#L35-L57)
```



### Dart

```
// Make sure to include this import:
// import 'package:google_generative_ai/google_generative_ai.dart';
final model = GenerativeModel(
  model: 'gemini-1.5-flash',
  apiKey: apiKey,
);
final chat = model.startChat(history: [
  Content.text('hello'),
  Content.model([TextPart('Great to meet you. What would you like to know?')])
]);
var response =
    await chat.sendMessage(Content.text('I have 2 dogs in my house.'));
print(response.text);
response =
    await chat.sendMessage(Content.text('How many paws are in my house?'));
print(response.text);[chat.dart](https://github.com/google-gemini/generative-ai-dart/blob/76ae8f89eed4789af0be9e7876d0089909abc419/samples/dart/bin/chat.dart#L30-L45)
```



### Java

```
// Specify a Gemini model appropriate for your use case
GenerativeModel gm =
    new GenerativeModel(
        /* modelName */ "gemini-1.5-flash",
        // Access your API key as a Build Configuration variable (see "Set up your API key"
        // above)
        /* apiKey */ BuildConfig.apiKey);
GenerativeModelFutures model = GenerativeModelFutures.from(gm);

// (optional) Create previous chat history for context
Content.Builder userContentBuilder = new Content.Builder();
userContentBuilder.setRole("user");
userContentBuilder.addText("Hello, I have 2 dogs in my house.");
Content userContent = userContentBuilder.build();

Content.Builder modelContentBuilder = new Content.Builder();
modelContentBuilder.setRole("model");
modelContentBuilder.addText("Great to meet you. What would you like to know?");
Content modelContent = userContentBuilder.build();

List<Content> history = Arrays.asList(userContent, modelContent);

// Initialize the chat
ChatFutures chat = model.startChat(history);

// Create a new user message
Content.Builder userMessageBuilder = new Content.Builder();
userMessageBuilder.setRole("user");
userMessageBuilder.addText("How many paws are in my house?");
Content userMessage = userMessageBuilder.build();

// For illustrative purposes only. You should use an executor that fits your needs.
Executor executor = Executors.newSingleThreadExecutor();

// Send the message
ListenableFuture<GenerateContentResponse> response = chat.sendMessage(userMessage);

Futures.addCallback(
    response,
    new FutureCallback<GenerateContentResponse>() {
      @Override
      public void onSuccess(GenerateContentResponse result) {
        String resultText = result.getText();
        System.out.println(resultText);
      }

      @Override
      public void onFailure(Throwable t) {
        t.printStackTrace();
      }
    },
    executor);[chat.java](https://github.com/google-gemini/generative-ai-android/blob/3596cab996d0e09bf05e460c8307233ca3c14e46/samples/src/main/java/com/google/ai/client/generative/samples/java/chat.java#L47-L98)
```





### Cache

### Python

```
from google import genai
from google.genai import types

client = genai.Client()
document = client.files.upload(file=media / "a11.txt")
model_name = "gemini-1.5-flash-001"

cache = client.caches.create(
    model=model_name,
    config=types.CreateCachedContentConfig(
        contents=[document],
        system_instruction="You are an expert analyzing transcripts.",
    ),
)
print(cache)

response = client.models.generate_content(
    model=model_name,
    contents="Please summarize this transcript",
    config=types.GenerateContentConfig(cached_content=cache.name),
)
print(response.text)[cache.py](https://github.com/google-gemini/api-examples/blob/16520aea9a9f109d1f616ba3400e87c1ece94cac/python/cache.py#L25-L46)
```



### Node.js

```
// Make sure to include the following import:
// import {GoogleGenAI} from '@google/genai';
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
const filePath = path.join(media, "a11.txt");
const document = await ai.files.upload({
  file: filePath,
  config: { mimeType: "text/plain" },
});
console.log("Uploaded file name:", document.name);
const modelName = "gemini-1.5-flash-001";

const contents = [
  createUserContent(createPartFromUri(document.uri, document.mimeType)),
];

const cache = await ai.caches.create({
  model: modelName,
  config: {
    contents: contents,
    systemInstruction: "You are an expert analyzing transcripts.",
  },
});
console.log("Cache created:", cache);

const response = await ai.models.generateContent({
  model: modelName,
  contents: "Please summarize this transcript",
  config: { cachedContent: cache.name },
});
console.log("Response text:", response.text);[cache.js](https://github.com/google-gemini/api-examples/blob/16520aea9a9f109d1f616ba3400e87c1ece94cac/javascript/cache.js#L33-L62)
```





### Tuned Model

### Python

```
# With Gemini 2 we're launching a new SDK. See the following doc for details.
# https://ai.google.dev/gemini-api/docs/migrate[README.md](https://github.com/google-gemini/deprecated-generative-ai-python/blob/e179614c3144360e3fa2b34fba6eb13398ea98a7/README.md#L13-L14)
```



