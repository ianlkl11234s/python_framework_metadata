---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/configuration/st.get_option
date: 2025-04-27 12:50:59
---

## st.get_option

Return the current value of a given Streamlit configuration option.

Runstreamlit config showin a terminal to see all available options.

st.get_option(key)

key(str)

The config option key of the form "section.optionName". To see all
available options, runstreamlit config showin a terminal.

#### Example

```python

import streamlit as st

color = st.get_option("theme.primaryColor")

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
