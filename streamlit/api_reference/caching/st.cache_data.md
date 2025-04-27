---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache_data
date: 2025-04-27 12:50:36
---

## st.cache_data

Decorator to cache functions that return data (e.g. dataframe transforms, database queries, ML inference).

Cached objects are stored in "pickled" form, which means that the return
value of a cached function must be pickleable. Each caller of the cached
function gets its own copy of the cached data.

You can clear a function's cache withfunc.clear()or clear the entire
cache withst.cache_data.clear().

A function's arguments must be hashable to cache it. If you have an
unhashable argument (like a database connection) or an argument you
want to exclude from caching, use an underscore prefix in the argument
name. In this case, Streamlit will return a cached value when all other
arguments match a previous function call. Alternatively, you can
declare custom hashing functions withhash_funcs.

To cache global resources, usest.cache_resourceinstead. Learn more
about caching athttps://docs.streamlit.io/develop/concepts/architecture/caching.

st.cache_data(func=None, *, ttl, max_entries, show_spinner, persist, experimental_allow_widgets, hash_funcs=None)

func(callable)

The function to cache. Streamlit hashes the function's source code.

ttl(float, timedelta, str, or None)

The maximum time to keep an entry in the cache. Can be one of:

- Noneif cache entries should never expire (default).
- A number specifying the time in seconds.
- A string specifying the time in a format supported byPandas's
Timedelta constructor,
e.g."1d","1.5 days", or"1h23s".
- Atimedeltaobject fromPython's built-in datetime library,
e.g.timedelta(days=1).
Note thatttlwill be ignored ifpersist="disk"orpersist=True.

max_entries(int or None)

The maximum number of entries to keep in the cache, or None
for an unbounded cache. When a new entry is added to a full cache,
the oldest cached entry will be removed. Defaults to None.

show_spinner(bool or str)

Enable the spinner. Default is True to show a spinner when there is
a "cache miss" and the cached data is being created. If string,
value of show_spinner param will be used for spinner text.

persist("disk", bool, or None)

Optional location to persist cached data to. Passing "disk" (or True)
will persist the cached data to the local disk. None (or False) will disable
persistence. The default is None.

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

@st.cache_data
def fetch_and_clean_data(url):
    # Fetch data from URL here, and then clean it up.
    return data

d1 = fetch_and_clean_data(DATA_URL_1)
# Actually executes the function, since this is the first time it was
# encountered.

d2 = fetch_and_clean_data(DATA_URL_1)
# Does not execute the function. Instead, returns its previously computed
# value. This means that now the data in d1 is the same as in d2.

d3 = fetch_and_clean_data(DATA_URL_2)
# This is a different URL, so the function executes.

```

To set thepersistparameter, use this command as follows:

```python

import streamlit as st

@st.cache_data(persist="disk")
def fetch_and_clean_data(url):
    # Fetch data from URL here, and then clean it up.
    return data

```

By default, all parameters to a cached function must be hashable.
Any parameter whose name begins with_will not be hashed. You can use
this as an "escape hatch" for parameters that are not hashable:

```python

import streamlit as st

@st.cache_data
def fetch_and_clean_data(_db_connection, num_rows):
    # Fetch data from _db_connection here, and then clean it up.
    return data

connection = make_database_connection()
d1 = fetch_and_clean_data(connection, num_rows=10)
# Actually executes the function, since this is the first time it was
# encountered.

another_connection = make_database_connection()
d2 = fetch_and_clean_data(another_connection, num_rows=10)
# Does not execute the function. Instead, returns its previously computed
# value - even though the _database_connection parameter was different
# in both calls.

```

A cached function's cache can be procedurally cleared:

```python

import streamlit as st

@st.cache_data
def fetch_and_clean_data(_db_connection, num_rows):
    # Fetch data from _db_connection here, and then clean it up.
    return data

fetch_and_clean_data.clear(_db_connection, 50)
# Clear the cached entry for the arguments provided.

fetch_and_clean_data.clear()
# Clear all cached entries for this function.

```

To override the default hashing behavior, pass a custom hash function.
You can do that by mapping a type (e.g.datetime.datetime) to a hash
function (lambda dt: dt.isoformat()) like this:

```python

import streamlit as st
import datetime

@st.cache_data(hash_funcs={datetime.datetime: lambda dt: dt.isoformat()})
def convert_to_utc(dt: datetime.datetime):
    return dt.astimezone(datetime.timezone.utc)

```

Alternatively, you can map the type's fully-qualified name
(e.g."datetime.datetime") to the hash function instead:

```python

import streamlit as st
import datetime

@st.cache_data(hash_funcs={"datetime.datetime": lambda dt: dt.isoformat()})
def convert_to_utc(dt: datetime.datetime):
    return dt.astimezone(datetime.timezone.utc)

```

#### Warning

st.cache_dataimplicitly uses thepicklemodule, which is known to be insecure. Anything your cached function returns is pickled and stored, then unpickled on retrieval. Ensure your cached functions return trusted values because it is possible to construct malicious pickle data that will execute arbitrary code during unpickling. Never load data that could have come from an untrusted source in an unsafe mode or that could have been tampered with.Only load data you trust.

`st.cache_data`

`pickle`

## st.cache_data.clear

Clear all in-memory and on-disk data caches.

st.cache_data.clear()

#### Example

In the example below, pressing the "Clear All" button will clear memoized values from all functions decorated with@st.cache_data.

`@st.cache_data`

`import streamlit as st

@st.cache_data
def square(x):
    return x**2

@st.cache_data
def cube(x):
    return x**3

if st.button("Clear All"):
    # Clear values from *all* all in-memory and on-disk data caches:
    # i.e. clear values from both square and cube
    st.cache_data.clear()`

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

`@st.cache_data
def get_api_data():
    data = api.get(...)
    st.success("Fetched data from API!")  # 👈 Show a success message
    return data`

As we know, Streamlit only runs this function if it hasn’t been cached before. On this first run, thest.successmessage will appear in the app. But what happens on subsequent runs? It still shows up! Streamlit realizes that there is anst.command inside the cached function, saves it during the first run, and replays it on subsequent runs. Replaying static elements works for both caching decorators.

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

### Input widgets

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

Using widgets in cached functions is extremely powerful because it lets you cache entire parts of your app. But it can be dangerous! Since Streamlit treats the widget value as an additional input parameter, it can easily lead to excessive memory usage. Imagine your cached function has five sliders and returns a 100 MB DataFrame. Then we’ll add 100 MB to the cache forevery permutationof these five slider values – even if the sliders do not influence the returned data! These additions can make your cache explode very quickly. Please be aware of this limitation if you use widgets in cached functions. We recommend using this feature only for isolated parts of your UI where the widgets directly influence the cached return value.

#### Warning

Support for widgets in cached functions is currently experimental. We may change or remove it anytime without warning. Please use it with care!

#### Note

Two widgets are currently not supported in cached functions:st.file_uploaderandst.camera_input. We may support them in the future. Feel free toopen a GitHub issueif you need them!

`st.file_uploader`

`st.camera_input`

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
