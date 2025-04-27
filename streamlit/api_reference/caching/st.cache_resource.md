---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache_resource
date: 2025-04-27 12:50:39
---

## st.cache_resource

Decorator to cache functions that return global resources (e.g. database connections, ML models).

Cached objects are shared across all users, sessions, and reruns. They
must be thread-safe because they can be accessed from multiple threads
concurrently. If thread safety is an issue, consider usingst.session_stateto store resources per session instead.

You can clear a function's cache withfunc.clear()or clear the entire
cache withst.cache_resource.clear().

A function's arguments must be hashable to cache it. If you have an
unhashable argument (like a database connection) or an argument you
want to exclude from caching, use an underscore prefix in the argument
name. In this case, Streamlit will return a cached value when all other
arguments match a previous function call. Alternatively, you can
declare custom hashing functions withhash_funcs.

To cache data, usest.cache_datainstead. Learn more about caching athttps://docs.streamlit.io/develop/concepts/architecture/caching.

st.cache_resource(func, *, ttl, max_entries, show_spinner, validate, experimental_allow_widgets, hash_funcs=None)

func(callable)

The function that creates the cached resource. Streamlit hashes the
function's source code.

ttl(float, timedelta, str, or None)

The maximum time to keep an entry in the cache. Can be one of:

- Noneif cache entries should never expire (default).
- A number specifying the time in seconds.
- A string specifying the time in a format supported byPandas's
Timedelta constructor,
e.g."1d","1.5 days", or"1h23s".
- Atimedeltaobject fromPython's built-in datetime library,
e.g.timedelta(days=1).
max_entries(int or None)

The maximum number of entries to keep in the cache, or None
for an unbounded cache. When a new entry is added to a full cache,
the oldest cached entry will be removed. Defaults to None.

show_spinner(bool or str)

Enable the spinner. Default is True to show a spinner when there is
a "cache miss" and the cached resource is being created. If string,
value of show_spinner param will be used for spinner text.

validate(callable or None)

An optional validation function for cached data.validateis called
each time the cached value is accessed. It receives the cached value as
its only parameter and it must return a boolean. Ifvalidatereturns
False, the current cached value is discarded, and the decorated function
is called to compute a new value. This is useful e.g. to check the
health of database connections.

experimental_allow_widgets(bool)

The cached widget replay functionality was removed in 1.38. Please
remove theexperimental_allow_widgetsparameter from your
caching decorators. This parameter will be removed in a future
version.

Allow widgets to be used in the cached function. Defaults to False.

hash_funcs(dict or None)

Mapping of types or fully qualified names to hash functions.
This is used to override the behavior of the hasher inside Streamlit's
caching mechanism: when the hasher encounters an object, it will first
check to see if its type matches a key in this dict and, if so, will use
the provided function to generate a hash for it. See below for an example
of how this can be used.

#### Example

```python

import streamlit as st

@st.cache_resource
def get_database_session(url):
    # Create a database session object that points to the URL.
    return session

s1 = get_database_session(SESSION_URL_1)
# Actually executes the function, since this is the first time it was
# encountered.

s2 = get_database_session(SESSION_URL_1)
# Does not execute the function. Instead, returns its previously computed
# value. This means that now the connection object in s1 is the same as in s2.

s3 = get_database_session(SESSION_URL_2)
# This is a different URL, so the function executes.

```

By default, all parameters to a cache_resource function must be hashable.
Any parameter whose name begins with_will not be hashed. You can use
this as an "escape hatch" for parameters that are not hashable:

```python

import streamlit as st

@st.cache_resource
def get_database_session(_sessionmaker, url):
    # Create a database connection object that points to the URL.
    return connection

s1 = get_database_session(create_sessionmaker(), DATA_URL_1)
# Actually executes the function, since this is the first time it was
# encountered.

s2 = get_database_session(create_sessionmaker(), DATA_URL_1)
# Does not execute the function. Instead, returns its previously computed
# value - even though the _sessionmaker parameter was different
# in both calls.

```

A cache_resource function's cache can be procedurally cleared:

```python

import streamlit as st

@st.cache_resource
def get_database_session(_sessionmaker, url):
    # Create a database connection object that points to the URL.
    return connection

fetch_and_clean_data.clear(_sessionmaker, "https://streamlit.io/")
# Clear the cached entry for the arguments provided.

get_database_session.clear()
# Clear all cached entries for this function.

```

To override the default hashing behavior, pass a custom hash function.
You can do that by mapping a type (e.g.Person) to a hash
function (str) like this:

```python

import streamlit as st
from pydantic import BaseModel

class Person(BaseModel):
    name: str

@st.cache_resource(hash_funcs={Person: str})
def get_person_name(person: Person):
    return person.name

```

Alternatively, you can map the type's fully-qualified name
(e.g."__main__.Person") to the hash function instead:

```python

import streamlit as st
from pydantic import BaseModel

class Person(BaseModel):
    name: str

@st.cache_resource(hash_funcs={"__main__.Person": str})
def get_person_name(person: Person):
    return person.name

```

## st.cache_resource.clear

Clear all cache_resource caches.

st.cache_resource.clear()

#### Example

In the example below, pressing the "Clear All" button will clearallcache_resource caches. i.e. Clears cached global resources from all functions decorated with@st.cache_resource.

`@st.cache_resource`

`import streamlit as st
from transformers import BertModel

@st.cache_resource
 def get_database_session(url):
     # Create a database session object that points to the URL.
     return session

@st.cache_resource
def get_model(model_type):
    # Create a model of the specified type.
    return BertModel.from_pretrained(model_type)

if st.button("Clear All"):
    # Clears all st.cache_resource caches:
    st.cache_resource.clear()`

## CachedFunc.clear

Clear the cached function's associated cache.

If no arguments are passed, Streamlit will clear all values cached for
the function. If arguments are passed, Streamlit will clear the cached
value for these arguments only.

CachedFunc.clear(*args, **kwargs)

*args(Any)

Arguments of the cached functions.

**kwargs(Any)

Keyword arguments of the cached function.

#### Example

```python

import streamlit as st
import time

@st.cache_data
def foo(bar):
    time.sleep(2)
    st.write(f"Executed foo({bar}).")
    return bar

if st.button("Clear all cached values for `foo`", on_click=foo.clear):
    foo.clear()

if st.button("Clear the cached value of `foo(1)`"):
    foo.clear(1)

foo(1)
foo(2)

```

## Using Streamlit commands in cached functions

### Static elements

Since version 1.16.0, cached functions can contain Streamlit commands! For example, you can do this:

`from transformers import pipeline

@st.cache_resource
def load_model():
    model = pipeline("sentiment-analysis")
    st.success("Loaded NLP model from Hugging Face!")  # 👈 Show a success message
    return model`

As we know, Streamlit only runs this function if it hasn’t been cached before. On this first run, thest.successmessage will appear in the app. But what happens on subsequent runs? It still shows up! Streamlit realizes that there is anst.command inside the cached function, saves it during the first run, and replays it on subsequent runs. Replaying static elements works for both caching decorators.

`st.success`

`st.`

You can also use this functionality to cache entire parts of your UI:

`@st.cache_resource
def load_model():
    st.header("Data analysis")
    model = torchvision.models.resnet50(weights=ResNet50_Weights.DEFAULT)
    st.success("Loaded model!")
    st.write("Turning on evaluation mode...")
    model.eval()
    st.write("Here's the model:")
    return model`

### Input widgets

You can also useinteractive input widgetslikest.sliderorst.text_inputin cached functions. Widget replay is an experimental feature at the moment. To enable it, you need to set theexperimental_allow_widgetsparameter:

`st.slider`

`st.text_input`

`experimental_allow_widgets`

`@st.cache_resource(experimental_allow_widgets=True)  # 👈 Set the parameter
def load_model():
    pretrained = st.checkbox("Use pre-trained model:")  # 👈 Add a checkbox
    model = torchvision.models.resnet50(weights=ResNet50_Weights.DEFAULT, pretrained=pretrained)
    return model`

Streamlit treats the checkbox like an additional input parameter to the cached function. If you uncheck it, Streamlit will see if it has already cached the function for this checkbox state. If yes, it will return the cached value. If not, it will rerun the function using the new slider value.

Using widgets in cached functions is extremely powerful because it lets you cache entire parts of your app. But it can be dangerous! Since Streamlit treats the widget value as an additional input parameter, it can easily lead to excessive memory usage. Imagine your cached function has five sliders and returns a 100 MB DataFrame. Then we’ll add 100 MB to the cache forevery permutationof these five slider values – even if the sliders do not influence the returned data! These additions can make your cache explode very quickly. Please be aware of this limitation if you use widgets in cached functions. We recommend using this feature only for isolated parts of your UI where the widgets directly influence the cached return value.

#### Warning

Support for widgets in cached functions is currently experimental. We may change or remove it anytime without warning. Please use it with care!

#### Note

Two widgets are currently not supported in cached functions:st.file_uploaderandst.camera_input. We may support them in the future. Feel free toopen a GitHub issueif you need them!

`st.file_uploader`

`st.camera_input`

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
