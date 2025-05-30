---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/text/st.divider
date: 2025-04-27 12:48:58
---

## st.divider

Display a horizontal rule.

Note

You can achieve the same effect with st.write("---") or
even just "---" in your script (via magic).

st.divider()

#### Example

```python

import streamlit as st

st.divider()

```

Here's what it looks like in action when you have multiple elements in the app:

`import streamlit as st

st.write("This is some text.")

st.slider("This is a slider", 0, 100, (25, 75))

st.divider()  # 👈 Draws a horizontal rule

st.write("This text is between the horizontal rules.")

st.divider()  # 👈 Another horizontal rule`

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
