---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/write-magic/st.write
date: 2025-04-27 12:48:47
---

## st.write

Displays arguments in the app.

This is the Swiss Army knife of Streamlit commands: it does different
things depending on what you throw at it. Unlike other Streamlit
commands,st.write()has some unique properties:

- You can pass in multiple arguments, all of which will be displayed.
- Its behavior depends on the input type(s).
st.write(*args, unsafe_allow_html=False, **kwargs)

*args(any)

One or many objects to display in the app.

unsafe_allow_html(bool)

Whether to render HTML within*args. This only applies to
strings or objects falling back on_repr_html_(). If this isFalse(default), any HTML tags found inbodywill be
escaped and therefore treated as raw text. If this isTrue, any
HTML expressions withinbodywill be rendered.

Adding custom HTML to your app impacts safety, styling, and
maintainability.

Note

If you only want to insert HTML or CSS without Markdown text,
we recommend usingst.htmlinstead.

**kwargs(any)

**kwargsis deprecated and will be removed in a later version.
Use other, more specific Streamlit commands to pass additional
keyword arguments.

Keyword arguments. Not used.

(None)

No description

#### Examples

Its basic use case is to draw Markdown-formatted text, whenever the
input is a string:

```python

import streamlit as st

st.write("Hello, *World!* :sunglasses:")

```

As mentioned earlier,st.write()also accepts other data formats, such as
numbers, data frames, styled data frames, and assorted objects:

```python

import streamlit as st
import pandas as pd

st.write(1234)
st.write(
    pd.DataFrame(
        {
            "first column": [1, 2, 3, 4],
            "second column": [10, 20, 30, 40],
        }
    )
)

```

Finally, you can pass in multiple arguments to do things like:

```python

import streamlit as st

st.write("1 + 1 = ", 2)
st.write("Below is a DataFrame:", data_frame, "Above is a dataframe.")

```

Oh, one more thing:st.writeaccepts chart objects too! For example:

```python

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

df = pd.DataFrame(np.random.randn(200, 3), columns=["a", "b", "c"])
c = (
    alt.Chart(df)
    .mark_circle()
    .encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])
)

st.write(c)

```

### Featured video

Learn what thest.writeandmagiccommands are and how to use them.

`st.write`

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
