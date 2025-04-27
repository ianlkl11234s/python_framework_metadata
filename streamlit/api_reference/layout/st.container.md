---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/layout/st.container
date: 2025-04-27 12:50:21
---

## st.container

Insert a multi-element container.

Inserts an invisible container into your app that can be used to hold
multiple elements. This allows you to, for example, insert multiple
elements into your app out of order.

To add elements to the returned container, you can use thewithnotation
(preferred) or just call methods directly on the returned object. See
examples below.

st.container(*, height=None, border=None, key=None)

height(int or None)

Desired height of the container expressed in pixels. IfNone(default)
the container grows to fit its content. If a fixed height, scrolling is
enabled for large content and a grey border is shown around the container
to visually separate its scroll surface from the rest of the app.

Note

Use containers with scroll sparingly. If you do, try to keep
the height small (below 500 pixels). Otherwise, the scroll
surface of the container might cover the majority of the screen
on mobile devices, which makes it hard to scroll the rest of the app.

border(bool or None)

Whether to show a border around the container. IfNone(default), a
border is shown if the container is set to a fixed height and not
shown otherwise.

key(str or None)

An optional string to give this container a stable identity.

Additionally, ifkeyis provided, it will be used as CSS
class name prefixed withst-key-.

#### Examples

Inserting elements usingwithnotation:

```python

import streamlit as st

with st.container():
    st.write("This is inside the container")

    # You can call any Streamlit command, including custom components:
    st.bar_chart(np.random.randn(50, 3))

st.write("This is outside the container")

```

Inserting elements out of order:

```python

import streamlit as st

container = st.container(border=True)
container.write("This is inside the container")
st.write("This is outside the container")

# Now insert some more in the container
container.write("This is inside too")

```

Usingheightto make a grid:

```python

import streamlit as st

row1 = st.columns(3)
row2 = st.columns(3)

for col in row1 + row2:
    tile = col.container(height=120)
    tile.title(":balloon:")

```

Usingheightto create a scrolling container for long content:

```python

import streamlit as st

long_text = "Lorem ipsum. " * 1000

with st.container(height=300):
    st.markdown(long_text)

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
