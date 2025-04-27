---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/concepts/architecture/caching
date: 2025-04-27 12:47:54
---

# Caching overview

Streamlit runs your script from top to bottom at every user interaction or code change. This execution model makes development super easy. But it comes with two major challenges:

- Long-running functions run again and again, which slows down your app.
- Objects get recreated again and again, which makes it hard to persist them across reruns or sessions.
But don't worry! Streamlit lets you tackle both issues with its built-in caching mechanism. Caching stores the results of slow function calls, so they only need to run once. This makes your app much faster and helps with persisting objects across reruns. Cached values are available to all users of your app. If you need to save results that should only be accessible within a session, useSession Stateinstead.

- Minimal example
- Basic usage
- Advanced usage
- Migrating from st.cache
## Minimal example

To cache a function in Streamlit, you must decorate it with one of two decorators (st.cache_dataorst.cache_resource):

`st.cache_data`

`st.cache_resource`

`@st.cache_data
def long_running_function(param1, param2):
    return …`

In this example, decoratinglong_running_functionwith@st.cache_datatells Streamlit that whenever the function is called, it checks two things:

`long_running_function`

`@st.cache_data`

- The values of the input parameters (in this case,param1andparam2).
- The code inside the function.
`param1`

`param2`

If this is the first time Streamlit sees these parameter values and function code, it runs the function and stores the return value in a cache. The next time the function is called with the same parameters and code (e.g., when a user interacts with the app), Streamlit will skip executing the function altogether and return the cached value instead. During development, the cache updates automatically as the function code changes, ensuring that the latest changes are reflected in the cache.

As mentioned, there are two caching decorators:

- st.cache_datais the recommended way to cache computations that return data: loading a DataFrame from CSV, transforming a NumPy array, querying an API, or any other function that returns a serializable data object (str, int, float, DataFrame, array, list, …). It creates a new copy of the data at each function call, making it safe againstmutations and race conditions. The behavior ofst.cache_datais what you want in most cases – so if you're unsure, start withst.cache_dataand see if it works!
- st.cache_resourceis the recommended way to cache global resources like ML models or database connections – unserializable objects that you don't want to load multiple times. Using it, you can share these resources across all reruns and sessions of an app without copying or duplication. Note that any mutations to the cached return value directly mutate the object in the cache (more details below).
`st.cache_data`

`st.cache_data`

`st.cache_data`

`st.cache_resource`

Streamlit's two caching decorators and their use cases.

## Basic usage

### st.cache_data

st.cache_datais your go-to command for all functions that return data – whether DataFrames, NumPy arrays, str, int, float, or other serializable types. It's the right command for almost all use cases! Within each user session, an@st.cache_data-decorated function returns acopyof the cached return value (if the value is already cached).

`st.cache_data`

`@st.cache_data`

#### Usage

Let's look at an example of usingst.cache_data. Suppose your app loads theUber ride-sharing dataset– a CSV file of 50 MB – from the internet into a DataFrame:

`st.cache_data`

`def load_data(url):
    df = pd.read_csv(url)  # 👈 Download the data
    return df

df = load_data("https://github.com/plotly/datasets/raw/master/uber-rides-data1.csv")
st.dataframe(df)

st.button("Rerun")`

Running theload_datafunction takes 2 to 30 seconds, depending on your internet connection. (Tip: if you are on a slow connection, usethis 5 MB dataset instead). Without caching, the download is rerun each time the app is loaded or with user interaction. Try it yourself by clicking the button we added! Not a great experience… 😕

`load_data`

Now let's add the@st.cache_datadecorator onload_data:

`@st.cache_data`

`load_data`

`@st.cache_data  # 👈 Add the caching decorator
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data("https://github.com/plotly/datasets/raw/master/uber-rides-data1.csv")
st.dataframe(df)

st.button("Rerun")`

Run the app again. You'll notice that the slow download only happens on the first run. Every subsequent rerun should be almost instant! 💨

#### Behavior

How does this work? Let's go through the behavior ofst.cache_datastep by step:

`st.cache_data`

- On the first run, Streamlit recognizes that it has never called theload_datafunction with the specified parameter value (the URL of the CSV file) So it runs the function and downloads the data.
- Now our caching mechanism becomes active: the returned DataFrame is serialized (converted to bytes) viapickleand stored in the cache (together with the value of theurlparameter).
- On the next run, Streamlit checks the cache for an entry ofload_datawith the specificurl. There is one! So it retrieves the cached object, deserializes it to a DataFrame, and returns it instead of re-running the function and downloading the data again.
`load_data`

`url`

`load_data`

`url`

This process of serializing and deserializing the cached object creates a copy of our original DataFrame. While this copying behavior may seem unnecessary, it's what we want when caching data objects since it effectively prevents mutation and concurrency issues. Read the section “Mutation and concurrency issues" below to understand this in more detail.

#### Warning

st.cache_dataimplicitly uses thepicklemodule, which is known to be insecure. Anything your cached function returns is pickled and stored, then unpickled on retrieval. Ensure your cached functions return trusted values because it is possible to construct malicious pickle data that will execute arbitrary code during unpickling. Never load data that could have come from an untrusted source in an unsafe mode or that could have been tampered with.Only load data you trust.

`st.cache_data`

`pickle`

#### Examples

DataFrame transformations

In the example above, we already showed how to cache loading a DataFrame. It can also be useful to cache DataFrame transformations such asdf.filter,df.apply, ordf.sort_values. Especially with large DataFrames, these operations can be slow.

`df.filter`

`df.apply`

`df.sort_values`

`@st.cache_data
def transform(df):
    df = df.filter(items=['one', 'three'])
    df = df.apply(np.sum, axis=0)
	return df`

Array computations

Similarly, it can make sense to cache computations on NumPy arrays:

`@st.cache_data
def add(arr1, arr2):
	return arr1 + arr2`

Database queries

You usually make SQL queries to load data into your app when working with databases. Repeatedly running these queries can be slow, cost money, and degrade the performance of your database. We strongly recommend caching any database queries in your app. See alsoour guides on connecting Streamlit to different databasesfor in-depth examples.

`connection = database.connect()

@st.cache_data
def query():
    return pd.read_sql_query("SELECT * from table", connection)`

#### Tip

You should set attl(time to live) to get new results from your database. If you setst.cache_data(ttl=3600), Streamlit invalidates any cached values after 1 hour (3600 seconds) and runs the cached function again. See details inControlling cache size and duration.

`ttl`

`st.cache_data(ttl=3600)`

API calls

Similarly, it makes sense to cache API calls. Doing so also avoids rate limits.

`@st.cache_data
def api_call():
    response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
    return response.json()`

Running ML models (inference)

Running complex machine learning models can use significant time and memory. To avoid rerunning the same computations over and over, use caching.

`@st.cache_data
def run_model(inputs):
    return model(inputs)`

### st.cache_resource

st.cache_resourceis the right command to cache “resources" that should be available globally across all users, sessions, and reruns. It has more limited use cases thanst.cache_data, especially for caching database connections and ML models. Within each user session, an@st.cache_resource-decorated function returns the cached instance of the return value (if the value is already cached). Therefore, objects cached byst.cache_resourceact like singletons and can mutate.

`st.cache_resource`

`st.cache_data`

`@st.cache_resource`

`st.cache_resource`

#### Usage

As an example forst.cache_resource, let's look at a typical machine learning app. As a first step, we need to load an ML model. We do this withHugging Face's transformers library:

`st.cache_resource`

`from transformers import pipeline
model = pipeline("sentiment-analysis")  # 👈 Load the model`

If we put this code into a Streamlit app directly, the app will load the model at each rerun or user interaction. Repeatedly loading the model poses two problems:

- Loading the model takes time and slows down the app.
- Each session loads the model from scratch, which takes up a huge amount of memory.
Instead, it would make much more sense to load the model once and use that same object across all users and sessions. That's exactly the use case forst.cache_resource! Let's add it to our app and process some text the user entered:

`st.cache_resource`

`from transformers import pipeline

@st.cache_resource  # 👈 Add the caching decorator
def load_model():
    return pipeline("sentiment-analysis")

model = load_model()

query = st.text_input("Your query", value="I love Streamlit! 🎈")
if query:
    result = model(query)[0]  # 👈 Classify the query text
    st.write(result)`

If you run this app, you'll see that the app callsload_modelonly once – right when the app starts. Subsequent runs will reuse that same model stored in the cache, saving time and memory!

`load_model`

#### Behavior

Usingst.cache_resourceis very similar to usingst.cache_data. But there are a few important differences in behavior:

`st.cache_resource`

`st.cache_data`

- st.cache_resourcedoesnotcreate a copy of the cached return value but instead stores the object itself in the cache. All mutations on the function's return value directly affect the object in the cache, so you must ensure that mutations from multiple sessions do not cause problems. In short, the return value must be thread-safe.priority_highWarningUsingst.cache_resourceon objects that are not thread-safe might lead to crashes or corrupted data. Learn more below underMutation and concurrency issues.
- Not creating a copy means there's just one global instance of the cached return object, which saves memory, e.g. when using a large ML model. In computer science terms, we create asingleton.
- Return values of functions do not need to be serializable. This behavior is great for types not serializable by nature, e.g., database connections, file handles, or threads. Caching these objects withst.cache_datais not possible.
st.cache_resourcedoesnotcreate a copy of the cached return value but instead stores the object itself in the cache. All mutations on the function's return value directly affect the object in the cache, so you must ensure that mutations from multiple sessions do not cause problems. In short, the return value must be thread-safe.

`st.cache_resource`

#### Warning

Usingst.cache_resourceon objects that are not thread-safe might lead to crashes or corrupted data. Learn more below underMutation and concurrency issues.

`st.cache_resource`

Not creating a copy means there's just one global instance of the cached return object, which saves memory, e.g. when using a large ML model. In computer science terms, we create asingleton.

Return values of functions do not need to be serializable. This behavior is great for types not serializable by nature, e.g., database connections, file handles, or threads. Caching these objects withst.cache_datais not possible.

`st.cache_data`

#### Examples

Database connections

st.cache_resourceis useful for connecting to databases. Usually, you're creating a connection object that you want to reuse globally for every query. Creating a new connection object at each run would be inefficient and might lead to connection errors. That's exactly whatst.cache_resourcecan do, e.g., for a Postgres database:

`st.cache_resource`

`st.cache_resource`

`@st.cache_resource
def init_connection():
    host = "hh-pgsql-public.ebi.ac.uk"
    database = "pfmegrnargs"
    user = "reader"
    password = "NWDMCE5xdipIjRrp"
    return psycopg2.connect(host=host, database=database, user=user, password=password)

conn = init_connection()`

Of course, you can do the same for any other database. Have a look atour guides on how to connect Streamlit to databasesfor in-depth examples.

Loading ML models

Your app should always cache ML models, so they are not loaded into memory again for every new session. See theexampleabove for how this works with 🤗 Hugging Face models. You can do the same thing for PyTorch, TensorFlow, etc. Here's an example for PyTorch:

`@st.cache_resource
def load_model():
    model = torchvision.models.resnet50(weights=ResNet50_Weights.DEFAULT)
    model.eval()
    return model

model = load_model()`

### Deciding which caching decorator to use

The sections above showed many common examples for each caching decorator. But there are edge cases for which it's less trivial to decide which caching decorator to use. Eventually, it all comes down to the difference between “data" and “resource":

- Data are serializable objects (objects that can be converted to bytes viapickle) that you could easily save to disk. Imagine all the types you would usually store in a database or on a file system – basic types like str, int, and float, but also arrays, DataFrames, images, or combinations of these types (lists, tuples, dicts, and so on).
- Resources are unserializable objects that you usually would not save to disk or a database. They are often more complex, non-permanent objects like database connections, ML models, file handles, threads, etc.
From the types listed above, it should be obvious that most objects in Python are “data." That's also whyst.cache_datais the correct command for almost all use cases.st.cache_resourceis a more exotic command that you should only use in specific situations.

`st.cache_data`

`st.cache_resource`

Or if you're lazy and don't want to think too much, look up your use case or return type in the table below 😉:

## Advanced usage

### Controlling cache size and duration

If your app runs for a long time and constantly caches functions, you might run into two problems:

- The app runs out of memory because the cache is too large.
- Objects in the cache become stale, e.g. because you cached old data from a database.
You can combat these problems with thettlandmax_entriesparameters, which are available for both caching decorators.

`ttl`

`max_entries`

Thettl(time-to-live) parameter

`ttl`

ttlsets a time to live on a cached function. If that time is up and you call the function again, the app will discard any old, cached values, and the function will be rerun. The newly computed value will then be stored in the cache. This behavior is useful for preventing stale data (problem 2) and the cache from growing too large (problem 1). Especially when pulling data from a database or API, you should always set attlso you are not using old data. Here's an example:

`ttl`

`ttl`

`@st.cache_data(ttl=3600)  # 👈 Cache data for 1 hour (=3600 seconds)
def get_api_data():
    data = api.get(...)
    return data`

#### Tip

You can also setttlvalues usingtimedelta, e.g.,ttl=datetime.timedelta(hours=1).

`ttl`

`timedelta`

`ttl=datetime.timedelta(hours=1)`

Themax_entriesparameter

`max_entries`

max_entriessets the maximum number of entries in the cache. An upper bound on the number of cache entries is useful for limiting memory (problem 1), especially when caching large objects. The oldest entry will be removed when a new entry is added to a full cache. Here's an example:

`max_entries`

`@st.cache_data(max_entries=1000)  # 👈 Maximum 1000 entries in the cache
def get_large_array(seed):
    np.random.seed(seed)
    arr = np.random.rand(100000)
    return arr`

### Customizing the spinner

By default, Streamlit shows a small loading spinner in the app when a cached function is running. You can modify it easily with theshow_spinnerparameter, which is available for both caching decorators:

`show_spinner`

`@st.cache_data(show_spinner=False)  # 👈 Disable the spinner
def get_api_data():
    data = api.get(...)
    return data

@st.cache_data(show_spinner="Fetching data from API...")  # 👈 Use custom text for spinner
def get_api_data():
    data = api.get(...)
    return data`

### Excluding input parameters

In a cached function, all input parameters must be hashable. Let's quickly explain why and what it means. When the function is called, Streamlit looks at its parameter values to determine if it was cached before. Therefore, it needs a reliable way to compare the parameter values across function calls. Trivial for a string or int – but complex for arbitrary objects! Streamlit useshashingto solve that. It converts the parameter to a stable key and stores that key. At the next function call, it hashes the parameter again and compares it with the stored hash key.

Unfortunately, not all parameters are hashable! E.g., you might pass an unhashable database connection or ML model to your cached function. In this case, you can exclude input parameters from caching. Simply prepend the parameter name with an underscore (e.g.,_param1), and it will not be used for caching. Even if it changes, Streamlit will return a cached result if all the other parameters match up.

`_param1`

Here's an example:

`@st.cache_data
def fetch_data(_db_connection, num_rows):  # 👈 Don't hash _db_connection
    data = _db_connection.fetch(num_rows)
    return data

connection = init_connection()
fetch_data(connection, 10)`

But what if you want to cache a function that takes an unhashable parameter? For example, you might want to cache a function that takes an ML model as input and returns the layer names of that model. Since the model is the only input parameter, you cannot exclude it from caching. In this case you can use thehash_funcsparameter to specify a custom hashing function for the model.

`hash_funcs`

### Thehash_funcsparameter

`hash_funcs`

As described above, Streamlit's caching decorators hash the input parameters and cached function's signature to determine whether the function has been run before and has a return value stored ("cache hit") or needs to be run ("cache miss"). Input parameters that are not hashable by Streamlit's hashing implementation can be ignored by prepending an underscore to their name. But there two rare cases where this is undesirable. i.e. where you want to hash the parameter that Streamlit is unable to hash:

- When Streamlit's hashing mechanism fails to hash a parameter, resulting in aUnhashableParamErrorbeing raised.
- When you want to override Streamlit's default hashing mechanism for a parameter.
`UnhashableParamError`

Let's discuss each of these cases in turn with examples.

#### Example 1: Hashing a custom class

Streamlit does not know how to hash custom classes. If you pass a custom class to a cached function, Streamlit will raise aUnhashableParamError. For example, let's define a custom classMyCustomClassthat accepts an initial integer score. Let's also define a cached functionmultiply_scorethat multiplies the score by a multiplier:

`UnhashableParamError`

`MyCustomClass`

`multiply_score`

`import streamlit as st

class MyCustomClass:
    def __init__(self, initial_score: int):
        self.my_score = initial_score

@st.cache_data
def multiply_score(obj: MyCustomClass, multiplier: int) -> int:
    return obj.my_score * multiplier

initial_score = st.number_input("Enter initial score", value=15)

score = MyCustomClass(initial_score)
multiplier = 2

st.write(multiply_score(score, multiplier))`

If you run this app, you'll see that Streamlit raises aUnhashableParamErrorsince it does not know how to hashMyCustomClass:

`UnhashableParamError`

`MyCustomClass`

`UnhashableParamError: Cannot hash argument 'obj' (of type __main__.MyCustomClass) in 'multiply_score'.`

To fix this, we can use thehash_funcsparameter to tell Streamlit how to hashMyCustomClass. We do this by passing a dictionary tohash_funcsthat maps the name of the parameter to a hash function. The choice of hash function is up to the developer. In this case, let's define a custom hash functionhash_functhat takes the custom class as input and returns the score. We want the score to be the unique identifier of the object, so we can use it to deterministically hash the object:

`hash_funcs`

`MyCustomClass`

`hash_funcs`

`hash_func`

`import streamlit as st

class MyCustomClass:
    def __init__(self, initial_score: int):
        self.my_score = initial_score

def hash_func(obj: MyCustomClass) -> int:
    return obj.my_score  # or any other value that uniquely identifies the object

@st.cache_data(hash_funcs={MyCustomClass: hash_func})
def multiply_score(obj: MyCustomClass, multiplier: int) -> int:
    return obj.my_score * multiplier

initial_score = st.number_input("Enter initial score", value=15)

score = MyCustomClass(initial_score)
multiplier = 2

st.write(multiply_score(score, multiplier))`

Now if you run the app, you'll see that Streamlit no longer raises aUnhashableParamErrorand the app runs as expected.

`UnhashableParamError`

Let's now consider the case wheremultiply_scoreis an attribute ofMyCustomClassand we want to hash the entire object:

`multiply_score`

`MyCustomClass`

`import streamlit as st

class MyCustomClass:
    def __init__(self, initial_score: int):
        self.my_score = initial_score

    @st.cache_data
    def multiply_score(self, multiplier: int) -> int:
        return self.my_score * multiplier

initial_score = st.number_input("Enter initial score", value=15)

score = MyCustomClass(initial_score)
multiplier = 2

st.write(score.multiply_score(multiplier))`

If you run this app, you'll see that Streamlit raises aUnhashableParamErrorsince it cannot hash the argument'self' (of type __main__.MyCustomClass) in 'multiply_score'. A simple fix here could be to use Python'shash()function to hash the object:

`UnhashableParamError`

`'self' (of type __main__.MyCustomClass) in 'multiply_score'`

`hash()`

`import streamlit as st

class MyCustomClass:
    def __init__(self, initial_score: int):
        self.my_score = initial_score

    @st.cache_data(hash_funcs={"__main__.MyCustomClass": lambda x: hash(x.my_score)})
    def multiply_score(self, multiplier: int) -> int:
        return self.my_score * multiplier

initial_score = st.number_input("Enter initial score", value=15)

score = MyCustomClass(initial_score)
multiplier = 2

st.write(score.multiply_score(multiplier))`

Above, the hash function is defined aslambda x: hash(x.my_score). This creates a hash based on themy_scoreattribute of theMyCustomClassinstance. As long asmy_scoreremains the same, the hash remains the same. Thus, the result ofmultiply_scorecan be retrieved from the cache without recomputation.

`lambda x: hash(x.my_score)`

`my_score`

`MyCustomClass`

`my_score`

`multiply_score`

As an astute Pythonista, you may have been tempted to use Python'sid()function to hash the object like so:

`id()`

`import streamlit as st

class MyCustomClass:
    def __init__(self, initial_score: int):
        self.my_score = initial_score

    @st.cache_data(hash_funcs={"__main__.MyCustomClass": id})
    def multiply_score(self, multiplier: int) -> int:
        return self.my_score * multiplier

initial_score = st.number_input("Enter initial score", value=15)

score = MyCustomClass(initial_score)
multiplier = 2

st.write(score.multiply_score(multiplier))`

If you run the app, you'll notice that Streamlit recomputesmultiply_scoreeach time even ifmy_scorehasn't changed! Puzzled? In Python,id()returns the identity of an object, which is unique and constant for the object during its lifetime. This means that even if themy_scorevalue is the same between two instances ofMyCustomClass,id()will return different values for these two instances, leading to different hash values. As a result, Streamlit considers these two different instances as needing separate cached values, thus it recomputes themultiply_scoreeach time even ifmy_scorehasn't changed.

`multiply_score`

`my_score`

`id()`

`my_score`

`MyCustomClass`

`id()`

`multiply_score`

`my_score`

This is why we discourage using it as hash func, and instead encourage functions that return deterministic, true hash values. That said, if you know what you're doing, you can useid()as a hash function. Just be aware of the consequences. For example,idis often thecorrecthash func when you're passing the result of an@st.cache_resourcefunction as the input param to another cached function. There's a whole class of object types that aren’t otherwise hashable.

`id()`

`id`

`@st.cache_resource`

#### Example 2: Hashing a Pydantic model

Let's consider another example where we want to hash a Pydantic model:

`import streamlit as st
from pydantic import BaseModel

class Person(BaseModel):
    name: str

@st.cache_data
def identity(person: Person):
    return person

person = identity(Person(name="Lee"))
st.write(f"The person is {person.name}")`

Above, we define a custom classPersonusing Pydantic'sBaseModelwith a single attribute name. We also define anidentityfunction which accepts an instance ofPersonas an arg and returns it without modification. This function is intended to cache the result, therefore, if called multiple times with the samePersoninstance, it won't recompute but return the cached instance.

`Person`

`BaseModel`

`identity`

`Person`

`Person`

If you run the app, however, you'll run into aUnhashableParamError: Cannot hash argument 'person' (of type __main__.Person) in 'identity'.error. This is because Streamlit does not know how to hash thePersonclass. To fix this, we can use thehash_funcskwarg to tell Streamlit how to hashPerson.

`UnhashableParamError: Cannot hash argument 'person' (of type __main__.Person) in 'identity'.`

`Person`

`hash_funcs`

`Person`

In the version below, we define a custom hash functionhash_functhat takes thePersoninstance as input and returns the name attribute. We want the name to be the unique identifier of the object, so we can use it to deterministically hash the object:

`hash_func`

`Person`

`import streamlit as st
from pydantic import BaseModel

class Person(BaseModel):
    name: str

@st.cache_data(hash_funcs={Person: lambda p: p.name})
def identity(person: Person):
    return person

person = identity(Person(name="Lee"))
st.write(f"The person is {person.name}")`

#### Example 3: Hashing a ML model

There may be cases where you want to pass your favorite machine learning model to a cached function. For example, let's say you want to pass a TensorFlow model to a cached function, based on what model the user selects in the app. You might try something like this:

`import streamlit as st
import tensorflow as tf

@st.cache_resource
def load_base_model(option):
    if option == 1:
        return tf.keras.applications.ResNet50(include_top=False, weights="imagenet")
    else:
        return tf.keras.applications.MobileNetV2(include_top=False, weights="imagenet")

@st.cache_resource
def load_layers(base_model):
    return [layer.name for layer in base_model.layers]

option = st.radio("Model 1 or 2", [1, 2])

base_model = load_base_model(option)

layers = load_layers(base_model)

st.write(layers)`

In the above app, the user can select one of two models. Based on the selection, the app loads the corresponding model and passes it toload_layers. This function then returns the names of the layers in the model. If you run the app, you'll see that Streamlit raises aUnhashableParamErrorsince it cannot hash the argument'base_model' (of type keras.engine.functional.Functional) in 'load_layers'.

`load_layers`

`UnhashableParamError`

`'base_model' (of type keras.engine.functional.Functional) in 'load_layers'`

If you disable hashing forbase_modelby prepending an underscore to its name, you'll observe that regardless of which base model is chosen, the layers displayed are same. This subtle bug is due to the fact that theload_layersfunction is not re-run when the base model changes. This is because Streamlit does not hash thebase_modelargument, so it does not know that the function needs to be re-run when the base model changes.

`base_model`

`load_layers`

`base_model`

To fix this, we can use thehash_funcskwarg to tell Streamlit how to hash thebase_modelargument. In the version below, we define a custom hash functionhash_func:Functional: lambda x: x.name. Our choice of hash func is informed by our knowledge that thenameattribute of aFunctionalobject or model uniquely identifies it. As long as thenameattribute remains the same, the hash remains the same. Thus, the result ofload_layerscan be retrieved from the cache without recomputation.

`hash_funcs`

`base_model`

`hash_func`

`Functional: lambda x: x.name`

`name`

`Functional`

`name`

`load_layers`

`import streamlit as st
import tensorflow as tf
from keras.engine.functional import Functional

@st.cache_resource
def load_base_model(option):
    if option == 1:
        return tf.keras.applications.ResNet50(include_top=False, weights="imagenet")
    else:
        return tf.keras.applications.MobileNetV2(include_top=False, weights="imagenet")

@st.cache_resource(hash_funcs={Functional: lambda x: x.name})
def load_layers(base_model):
    return [layer.name for layer in base_model.layers]

option = st.radio("Model 1 or 2", [1, 2])

base_model = load_base_model(option)

layers = load_layers(base_model)

st.write(layers)`

In the above case, we could also have usedhash_funcs={Functional: id}as the hash function. This is becauseidis often thecorrecthash func when you're passing the result of an@st.cache_resourcefunction as the input param to another cached function.

`hash_funcs={Functional: id}`

`id`

`@st.cache_resource`

#### Example 4: Overriding Streamlit's default hashing mechanism

Let's consider another example where we want to override Streamlit's default hashing mechanism for a pytz-localized datetime object:

`from datetime import datetime
import pytz
import streamlit as st

tz = pytz.timezone("Europe/Berlin")

@st.cache_data
def load_data(dt):
    return dt

now = datetime.now()
st.text(load_data(dt=now))

now_tz = tz.localize(datetime.now())
st.text(load_data(dt=now_tz))`

It may be surprising to see that althoughnowandnow_tzare of the same<class 'datetime.datetime'>type, Streamlit does not how to hashnow_tzand raises aUnhashableParamError. In this case, we can override Streamlit's default hashing mechanism fordatetimeobjects by passing a custom hash function to thehash_funcskwarg:

`now`

`now_tz`

`<class 'datetime.datetime'>`

`now_tz`

`UnhashableParamError`

`datetime`

`hash_funcs`

`from datetime import datetime

import pytz
import streamlit as st

tz = pytz.timezone("Europe/Berlin")

@st.cache_data(hash_funcs={datetime: lambda x: x.strftime("%a %d %b %Y, %I:%M%p")})
def load_data(dt):
    return dt

now = datetime.now()
st.text(load_data(dt=now))

now_tz = tz.localize(datetime.now())
st.text(load_data(dt=now_tz))`

Let's now consider a case where we want to override Streamlit's default hashing mechanism for NumPy arrays. While Streamlit natively hashes Pandas and NumPy objects, there may be cases where you want to override Streamlit's default hashing mechanism for these objects.

For example, let's say we create a cache-decoratedshow_datafunction that accepts a NumPy array and returns it without modification. In the bellow app,data = df["str"].unique()(which is a NumPy array) is passed to theshow_datafunction.

`show_data`

`data = df["str"].unique()`

`show_data`

`import time
import numpy as np
import pandas as pd
import streamlit as st

@st.cache_data
def get_data():
    df = pd.DataFrame({"num": [112, 112, 2, 3], "str": ["be", "a", "be", "c"]})
    return df

@st.cache_data
def show_data(data):
    time.sleep(2)  # This makes the function take 2s to run
    return data

df = get_data()
data = df["str"].unique()

st.dataframe(show_data(data))
st.button("Re-run")`

Sincedatais always the same, we expect theshow_datafunction to return the cached value. However, if you run the app, and click theRe-runbutton, you'll notice that theshow_datafunction is re-run each time. We can assume this behavior is a consequence of Streamlit's default hashing mechanism for NumPy arrays.

`data`

`show_data`

`Re-run`

`show_data`

To work around this, let's define a custom hash functionhash_functhat takes a NumPy array as input and returns a string representation of the array:

`hash_func`

`import time
import numpy as np
import pandas as pd
import streamlit as st

@st.cache_data
def get_data():
    df = pd.DataFrame({"num": [112, 112, 2, 3], "str": ["be", "a", "be", "c"]})
    return df

@st.cache_data(hash_funcs={np.ndarray: str})
def show_data(data):
    time.sleep(2)  # This makes the function take 2s to run
    return data

df = get_data()
data = df["str"].unique()

st.dataframe(show_data(data))
st.button("Re-run")`

Now if you run the app, and click theRe-runbutton, you'll notice that theshow_datafunction is no longer re-run each time. It's important to note here that our choice of hash function was very naive and not necessarily the best choice. For example, if the NumPy array is large, converting it to a string representation may be expensive. In such cases, it is up to you as the developer to define what a good hash function is for your use case.

`Re-run`

`show_data`

#### Static elements

Since version 1.16.0, cached functions can contain Streamlit commands! For example, you can do this:

`@st.cache_data
def get_api_data():
    data = api.get(...)
    st.success("Fetched data from API!")  # 👈 Show a success message
    return data`

As we know, Streamlit only runs this function if it hasn't been cached before. On this first run, thest.successmessage will appear in the app. But what happens on subsequent runs? It still shows up! Streamlit realizes that there is anst.command inside the cached function, saves it during the first run, and replays it on subsequent runs. Replaying static elements works for both caching decorators.

`st.success`

`st.`

You can also use this functionality to cache entire parts of your UI:

`@st.cache_data
def show_data():
    st.header("Data analysis")
    data = api.get(...)
    st.success("Fetched data from API!")
    st.write("Here is a plot of the data:")
    st.line_chart(data)
    st.write("And here is the raw data:")
    st.dataframe(data)`

#### Input widgets

You can also useinteractive input widgetslikest.sliderorst.text_inputin cached functions. Widget replay is an experimental feature at the moment. To enable it, you need to set theexperimental_allow_widgetsparameter:

`st.slider`

`st.text_input`

`experimental_allow_widgets`

`@st.cache_data(experimental_allow_widgets=True)  # 👈 Set the parameter
def get_data():
    num_rows = st.slider("Number of rows to get")  # 👈 Add a slider
    data = api.get(..., num_rows)
    return data`

Streamlit treats the slider like an additional input parameter to the cached function. If you change the slider position, Streamlit will see if it has already cached the function for this slider value. If yes, it will return the cached value. If not, it will rerun the function using the new slider value.

Using widgets in cached functions is extremely powerful because it lets you cache entire parts of your app. But it can be dangerous! Since Streamlit treats the widget value as an additional input parameter, it can easily lead to excessive memory usage. Imagine your cached function has five sliders and returns a 100 MB DataFrame. Then we'll add 100 MB to the cache forevery permutationof these five slider values – even if the sliders do not influence the returned data! These additions can make your cache explode very quickly. Please be aware of this limitation if you use widgets in cached functions. We recommend using this feature only for isolated parts of your UI where the widgets directly influence the cached return value.

#### Warning

Support for widgets in cached functions is experimental. We may change or remove it anytime without warning. Please use it with care!

#### Note

Two widgets are currently not supported in cached functions:st.file_uploaderandst.camera_input. We may support them in the future. Feel free toopen a GitHub issueif you need them!

`st.file_uploader`

`st.camera_input`

### Dealing with large data

As we explained, you should cache data objects withst.cache_data. But this can be slow for extremely large data, e.g., DataFrames or arrays with >100 million rows. That's because of thecopying behaviorofst.cache_data: on the first run, it serializes the return value to bytes and deserializes it on subsequent runs. Both operations take time.

`st.cache_data`

`st.cache_data`

If you're dealing with extremely large data, it can make sense to usest.cache_resourceinstead. It does not create a copy of the return value via serialization/deserialization and is almost instant. But watch out: any mutation to the function's return value (such as dropping a column from a DataFrame or setting a value in an array) directly manipulates the object in the cache. You must ensure this doesn't corrupt your data or lead to crashes. See the section onMutation and concurrency issuesbelow.

`st.cache_resource`

When benchmarkingst.cache_dataon pandas DataFrames with four columns, we found that it becomes slow when going beyond 100 million rows. The table shows runtimes for both caching decorators at different numbers of rows (all with four columns):

`st.cache_data`

### Mutation and concurrency issues

In the sections above, we talked a lot about issues when mutating return objects of cached functions. This topic is complicated! But it's central to understanding the behavior differences betweenst.cache_dataandst.cache_resource. So let's dive in a bit deeper.

`st.cache_data`

`st.cache_resource`

First, we should clearly define what we mean by mutations and concurrency:

- Bymutations, we mean any changes made to a cached function's return valueafterthat function has been called. I.e. something like this:@st.cache_data
def create_list():
    l = [1, 2, 3]

l = create_list()  # 👈 Call the function
l[0] = 2  # 👈 Mutate its return value
- Byconcurrency, we mean that multiple sessions can cause these mutations at the same time. Streamlit is a web framework that needs to handle many users and sessions connecting to an app. If two people view an app at the same time, they will both cause the Python script to rerun, which may manipulate cached return objects at the same time – concurrently.
Bymutations, we mean any changes made to a cached function's return valueafterthat function has been called. I.e. something like this:

`@st.cache_data
def create_list():
    l = [1, 2, 3]

l = create_list()  # 👈 Call the function
l[0] = 2  # 👈 Mutate its return value`

Byconcurrency, we mean that multiple sessions can cause these mutations at the same time. Streamlit is a web framework that needs to handle many users and sessions connecting to an app. If two people view an app at the same time, they will both cause the Python script to rerun, which may manipulate cached return objects at the same time – concurrently.

Mutating cached return objects can be dangerous. It can lead to exceptions in your app and even corrupt your data (which can be worse than a crashed app!). Below, we'll first explain the copying behavior ofst.cache_dataand show how it can avoid mutation issues. Then, we'll show how concurrent mutations can lead to data corruption and how to prevent it.

`st.cache_data`

#### Copying behavior

st.cache_datacreates a copy of the cached return value each time the function is called. This avoids most mutations and concurrency issues. To understand it in detail, let's go back to theUber ridesharing examplefrom the section onst.cache_dataabove. We are making two modifications to it:

`st.cache_data`

`st.cache_data`

- We are usingst.cache_resourceinstead ofst.cache_data.st.cache_resourcedoesnotcreate a copy of the cached object, so we can see what happens without the copying behavior.
- After loading the data, we manipulate the returned DataFrame (in place!) by dropping the column"Lat".
`st.cache_resource`

`st.cache_data`

`st.cache_resource`

`"Lat"`

Here's the code:

`@st.cache_resource   # 👈 Turn off copying behavior
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data("https://raw.githubusercontent.com/plotly/datasets/master/uber-rides-data1.csv")
st.dataframe(df)

df.drop(columns=['Lat'], inplace=True)  # 👈 Mutate the dataframe inplace

st.button("Rerun")`

Let's run it and see what happens! The first run should work fine. But in the second run, you see an exception:KeyError: "['Lat'] not found in axis". Why is that happening? Let's go step by step:

`KeyError: "['Lat'] not found in axis"`

- On the first run, Streamlit runsload_dataand stores the resulting DataFrame in the cache. Since we're usingst.cache_resource, it doesnotcreate a copy but stores the original DataFrame.
- Then we drop the column"Lat"from the DataFrame. Note that this is dropping the column from theoriginalDataFrame stored in the cache. We are manipulating it!
- On the second run, Streamlit returns that exact same manipulated DataFrame from the cache. It does not have the column"Lat"anymore! So our call todf.dropresults in an exception. Pandas cannot drop a column that doesn't exist.
`load_data`

`st.cache_resource`

`"Lat"`

`"Lat"`

`df.drop`

The copying behavior ofst.cache_dataprevents this kind of mutation error. Mutations can only affect a specific copy and not the underlying object in the cache. The next rerun will get its own, unmutated copy of the DataFrame. You can try it yourself, just replacest.cache_resourcewithst.cache_dataabove, and you'll see that everything works.

`st.cache_data`

`st.cache_resource`

`st.cache_data`

Because of this copying behavior,st.cache_datais the recommended way to cache data transforms and computations – anything that returns a serializable object.

`st.cache_data`

#### Concurrency issues

Now let's look at what can happen when multiple users concurrently mutate an object in the cache. Let's say you have a function that returns a list. Again, we are usingst.cache_resourceto cache it so that we are not creating a copy:

`st.cache_resource`

`@st.cache_resource
def create_list():
    l = [1, 2, 3]
    return l

l = create_list()
first_list_value = l[0]
l[0] = first_list_value + 1

st.write("l[0] is:", l[0])`

Let's say user A runs the app. They will see the following output:

`l[0] is: 2`

Let's say another user, B, visits the app right after. In contrast to user A, they will see the following output:

`l[0] is: 3`

Now, user A reruns the app immediately after user B. They will see the following output:

`l[0] is: 4`

What is happening here? Why are all outputs different?

- When user A visits the app,create_list()is called, and the list[1, 2, 3]is stored in the cache. This list is then returned to user A. The first value of the list,1, is assigned tofirst_list_value, andl[0]is changed to2.
- When user B visits the app,create_list()returns the mutated list from the cache:[2, 2, 3]. The first value of the list,2, is assigned tofirst_list_valueandl[0]is changed to3.
- When user A reruns the app,create_list()returns the mutated list again:[3, 2, 3]. The first value of the list,3, is assigned tofirst_list_value,andl[0]is changed to 4.
`create_list()`

`[1, 2, 3]`

`1`

`first_list_value`

`l[0]`

`2`

`create_list()`

`[2, 2, 3]`

`2`

`first_list_value`

`l[0]`

`3`

`create_list()`

`[3, 2, 3]`

`3`

`first_list_value,`

`l[0]`

If you think about it, this makes sense. Users A and B use the same list object (the one stored in the cache). And since the list object is mutated, user A's change to the list object is also reflected in user B's app.

This is why you must be careful about mutating objects cached withst.cache_resource, especially when multiple users access the app concurrently. If we had usedst.cache_datainstead ofst.cache_resource, the app would have copied the list object for each user, and the above example would have worked as expected – users A and B would have both seen:

`st.cache_resource`

`st.cache_data`

`st.cache_resource`

`l[0] is: 2`

#### Note

This toy example might seem benign. But data corruption can be extremely dangerous! Imagine we had worked with the financial records of a large bank here. You surely don't want to wake up with less money on your account just because someone used the wrong caching decorator 😉

## Migrating from st.cache

We introduced the caching commands described above in Streamlit 1.18.0. Before that, we had one catch-all commandst.cache. Using it was often confusing, resulted in weird exceptions, and was slow. That's why we replacedst.cachewith the new commands in 1.18.0 (read more in thisblog post). The new commands provide a more intuitive and efficient way to cache your data and resources and are intended to replacest.cachein all new development.

`st.cache`

`st.cache`

`st.cache`

If your app is still usingst.cache, don't despair! Here are a few notes on migrating:

`st.cache`

- Streamlit will show a deprecation warning if your app usesst.cache.
- We will not removest.cachesoon, so you don't need to worry about your 2-year-old app breaking. But we encourage you to try the new commands going forward – they will be way less annoying!
- Switching code to the new commands should be easy in most cases. To decide whether to usest.cache_dataorst.cache_resource, readDeciding which caching decorator to use. Streamlit will also recognize common use cases and show hints right in the deprecation warnings.
- Most parameters fromst.cacheare also present in the new commands, with a few exceptions:allow_output_mutationdoes not exist anymore. You can safely delete it. Just make sure you use the right caching command for your use case.suppress_st_warningdoes not exist anymore. You can safely delete it. Cached functions can now contain Streamlit commands and will replay them. If you want to use widgets inside cached functions, setexperimental_allow_widgets=True. SeeInput widgetsfor an example.
- allow_output_mutationdoes not exist anymore. You can safely delete it. Just make sure you use the right caching command for your use case.
- suppress_st_warningdoes not exist anymore. You can safely delete it. Cached functions can now contain Streamlit commands and will replay them. If you want to use widgets inside cached functions, setexperimental_allow_widgets=True. SeeInput widgetsfor an example.
`st.cache`

`st.cache`

`st.cache_data`

`st.cache_resource`

`st.cache`

- allow_output_mutationdoes not exist anymore. You can safely delete it. Just make sure you use the right caching command for your use case.
- suppress_st_warningdoes not exist anymore. You can safely delete it. Cached functions can now contain Streamlit commands and will replay them. If you want to use widgets inside cached functions, setexperimental_allow_widgets=True. SeeInput widgetsfor an example.
`allow_output_mutation`

`suppress_st_warning`

`experimental_allow_widgets=True`

If you have any questions or issues during the migration process, please contact us on theforum, and we will be happy to assist you. 🎈

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
