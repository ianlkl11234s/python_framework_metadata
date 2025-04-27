---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/caching-and-state/st.context
date: 2025-04-27 12:50:41
---

## st.context

An interface to access user session context.

st.contextprovides a read-only interface to access headers and cookies
for the current user session.

Each property (st.context.headersandst.context.cookies) returns
a dictionary of named values.

st.context()

cookies

A read-only, dict-like object containing cookies sent in the initial request.

headers

A read-only, dict-like object containing headers sent in the initial request.

locale

The read-only locale of the user's browser.

timezone

The read-only timezone of the user's browser.

timezone_offset

The read-only timezone offset of the user's browser.

## context.cookies

A read-only, dict-like object containing cookies sent in the initial request.

context.cookies

#### Examples

Example 1: Access all available cookies

Show a dictionary of cookies:

```python

import streamlit as st

st.context.cookies

```

Example 2: Access a specific cookie

Show the value of a specific cookie:

```python

import streamlit as st

st.context.cookies["_ga"]

```

## context.headers

A read-only, dict-like object containing headers sent in the initial request.

Keys are case-insensitive and may be repeated. When keys are repeated,
dict-like methods will only return the last instance of each key. Use.get_all(key="your_repeated_key")to see all values if the same
header is set multiple times.

context.headers

#### Examples

Example 1: Access all available headers

Show a dictionary of headers (with only the last instance of any
repeated key):

```python

import streamlit as st

st.context.headers

```

Example 2: Access a specific header

Show the value of a specific header (or the last instance if it's
repeated):

```python

import streamlit as st

st.context.headers["host"]

```

Show of list of all headers for a given key:

```python

import streamlit as st

st.context.headers.get_all("pragma")

```

## context.locale

The read-only locale of the user's browser.

st.context.localereturns the value ofnavigator.languagefrom
the user's DOM. This is a string representing the user's preferred
language (e.g. "en-US").

context.locale

#### Example

Access the user's locale to display locally:

```python

import streamlit as st

if st.context.locale == "fr-FR":
    st.write("Bonjour!")
else:
    st.write("Hello!")

```

## context.timezone

The read-only timezone of the user's browser.

context.timezone

#### Example

Access the user's timezone, and format a datetime to display locally:

```python

import streamlit as st
from datetime import datetime, timezone
import pytz

tz = st.context.timezone
tz_obj = pytz.timezone(tz)

now = datetime.now(timezone.utc)

f"The user's timezone is {tz}."
f"The UTC time is {now}."
f"The user's local time is {now.astimezone(tz_obj)}"

```

## context.timezone_offset

The read-only timezone offset of the user's browser.

context.timezone_offset

#### Example

Access the user's timezone offset, and format a datetime to display locally:

```python

import streamlit as st
from datetime import datetime, timezone, timedelta

tzoff = st.context.timezone_offset
tz_obj = timezone(-timedelta(minutes=tzoff))

now = datetime.now(timezone.utc)

f"The user's timezone is {tz}."
f"The UTC time is {now}."
f"The user's local time is {now.astimezone(tz_obj)}"

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
