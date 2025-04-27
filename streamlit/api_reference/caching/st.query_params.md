---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/caching-and-state/st.query_params
date: 2025-04-27 12:50:44
---

## st.query_params

st.query_paramsprovides a dictionary-like interface to access query parameters in your app's URL and is available as of Streamlit 1.30.0. It behaves similarly tost.session_statewith the notable exception that keys may be repeated in an app's URL. Handling of repeated keys requires special consideration as explained below.

`st.query_params`

`st.session_state`

st.query_paramscan be used with both key and attribute notation. For example,st.query_params.my_keyandst.query_params["my_key"]. All keys and values will be set and returned as strings. When you write tost.query_params, key-value pair prefixed with?is added to the end of your app's URL. Each additional pair is prefixed with&instead of?. Query parameters are cleared when navigating between pages in a multipage app.

`st.query_params`

`st.query_params.my_key`

`st.query_params["my_key"]`

`st.query_params`

`?`

`&`

`?`

For example, consider the following URL:

`https://your_app.streamlit.app/?first_key=1&second_key=two&third_key=true`

The parameters in the URL above will be accessible inst.query_paramsas:

`st.query_params`

`{
    "first_key" : "1",
    "second_key" : "two",
    "third_key" : "true"
}`

This means you can use those parameters in your app like this:

`# You can read query params using key notation
if st.query_params["first_key"] == "1":
    do_something()

# ...or using attribute notation
if st.query_params.second_key == "two":
    do_something_else()

# And you can change a param by just writing to it
st.query_params.first_key = 2  # This gets converted to str automatically`

### Repeated keys

When a key is repeated in your app's URL (?a=1&a=2&a=3), dict-like methods will return only the last value. In this example,st.query_params["a"]returns"3". To get all keys as a list, use the.get_all()method shown below. To set the value of a repeated key, assign the values as a list. For example,st.query_params.a = ["1", "2", "3"]produces the repeated key given at the beginning of this paragraph.

`?a=1&a=2&a=3`

`st.query_params["a"]`

`"3"`

`.get_all()`

`st.query_params.a = ["1", "2", "3"]`

### Limitation

st.query_paramscan't get or set embedding settings as described inEmbed your app.st.query_params.embedandst.query_params.embed_optionswill raise anAttributeErrororStreamlitAPIExceptionwhen trying to get or set their values, respectively.

`st.query_params`

`st.query_params.embed`

`st.query_params.embed_options`

`AttributeError`

`StreamlitAPIException`

## st.query_params.clear

Clear all query parameters from the URL of the app.

st.query_params.clear()

(None)

No description

## st.query_params.from_dict

Set all of the query parameters from a dictionary or dictionary-like object.

This method primarily exists for advanced users who want to control
multiple query parameters in a single update. To set individual query
parameters, use key or attribute notation instead.

This method inherits limitations fromst.query_paramsand can't be
used to set embedding options as described inEmbed your app.

To handle repeated keys, the value in a key-value pair should be a list.

Note

.from_dict()is not a direct inverse of.to_dict()if
you are working with repeated keys. A true inverse operation is{key: st.query_params.get_all(key) for key in st.query_params}.

st.query_params.from_dict(params)

params(dict)

A dictionary used to replace the current query parameters.

#### Example

```python

import streamlit as st

st.query_params.from_dict({"foo": "bar", "baz": [1, "two"]})

```

## st.query_params.get_all

Get a list of all query parameter values associated to a given key.

When a key is repeated as a query parameter within the URL, this method
allows all values to be obtained. In contrast, dict-like methods only
retrieve the last value when a key is repeated in the URL.

st.query_params.get_all(key)

key(str)

The label of the query parameter in the URL.

(List[str])

A list of values associated to the given key. May return zero, one,
or multiple values.

## st.query_params.to_dict

Get all query parameters as a dictionary.

This method primarily exists for internal use and is not needed for
most cases.st.query_paramsreturns an object that inherits fromdictby default.

When a key is repeated as a query parameter within the URL, this method
will return only the last value of each unique key.

st.query_params.to_dict()

(Dict[str,str])

A dictionary of the current query paramters in the app's URL.

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
