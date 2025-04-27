---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/layout/st.columns
date: 2025-04-27 12:50:19
---

## st.columns

Insert containers laid out as side-by-side columns.

Inserts a number of multi-element containers laid out side-by-side and
returns a list of container objects.

To add elements to the returned containers, you can use thewithnotation
(preferred) or just call methods directly on the returned object. See
examples below.

Columns can only be placed inside other columns up to one level of nesting.

Warning

Columns cannot be placed inside other columns in the sidebar. This
is only possible in the main area of the app.

st.columns(spec, *, gap="small", vertical_alignment="top", border=False)

spec(int or Iterable of numbers)

Controls the number and width of columns to insert. Can be one of:

- An integer that specifies the number of columns. All columns have equal
width in this case.
- An Iterable of numbers (int or float) that specify the relative width of
each column. E.g.[0.7, 0.3]creates two columns where the first
one takes up 70% of the available with and the second one takes up 30%.
Or[1, 2, 3]creates three columns where the second one is two times
the width of the first one, and the third one is three times that width.
gap("small", "medium", or "large")

The size of the gap between the columns. The default is"small".

vertical_alignment("top", "center", or "bottom")

The vertical alignment of the content inside the columns. The
default is"top".

border(bool)

Whether to show a border around the column containers. If this isFalse(default), no border is shown. If this isTrue, a
border is shown around each column.

(list of containers)

A list of container objects.

#### Examples

Example 1: Use context management

You can use thewithstatement to insert any element into a column:

```python

import streamlit as st

col1, col2, col3 = st.columns(3)

with col1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg")

```

Example 2: Use commands as container methods

You can just call methods directly on the returned objects:

```python

import streamlit as st
import numpy as np

col1, col2 = st.columns([3, 1])
data = np.random.randn(10, 1)

col1.subheader("A wide column with a chart")
col1.line_chart(data)

col2.subheader("A narrow column with the data")
col2.write(data)

```

Example 3: Align widgets

Usevertical_alignment="bottom"to align widgets.

```python

import streamlit as st

left, middle, right = st.columns(3, vertical_alignment="bottom")

left.text_input("Write something")
middle.button("Click me", use_container_width=True)
right.checkbox("Check me")

```

Example 4: Use vertical alignment to create grids

Adjust vertical alignment to customize your grid layouts.

```python

import streamlit as st
import numpy as np

vertical_alignment = st.selectbox(
    "Vertical alignment", ["top", "center", "bottom"], index=2
)

left, middle, right = st.columns(3, vertical_alignment=vertical_alignment)
left.image("https://static.streamlit.io/examples/cat.jpg")
middle.image("https://static.streamlit.io/examples/dog.jpg")
right.image("https://static.streamlit.io/examples/owl.jpg")

```

Example 5: Add borders

Add borders to your columns instead of nested containers for consistent
heights.

```python

import streamlit as st

left, middle, right = st.columns(3, border=True)

left.markdown("Lorem ipsum " * 10)
middle.markdown("Lorem ipsum " * 5)
right.markdown("Lorem ipsum ")

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
