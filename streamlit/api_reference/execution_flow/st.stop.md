---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/execution-flow/st.stop
date: 2025-04-27 12:50:34
---

## st.stop

Stops execution immediately.

Streamlit will not run any statements afterst.stop().
We recommend rendering a message to explain why the script has stopped.

st.stop()

#### Example

```python

import streamlit as st

name = st.text_input("Name")
if not name:
  st.warning('Please input a name.')
  st.stop()
st.success("Thank you for inputting a name.")

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
