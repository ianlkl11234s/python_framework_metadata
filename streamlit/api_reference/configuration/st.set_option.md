---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/configuration/st.set_option
date: 2025-04-27 12:51:04
---

## st.set_option

Set a configuration option.

Currently, onlyclientconfiguration options can be set within the
script itself:

- client.showErrorDetails
- client.showSidebarNavigation
- client.toolbarMode
Callingst.set_optionwith any other option will raise aStreamlitAPIException. When changing a configuration option in a
running app, you may need to trigger a rerun after changing the option to
see the effects.

Runstreamlit config showin a terminal to see all available options.

st.set_option(key, value)

key(str)

The config option key of the form "section.optionName". To see all
available options, runstreamlit config showin a terminal.

value(null)

The new value to assign to this config option.

#### Example

```python

import streamlit as st

st.set_option("client.showErrorDetails", True)

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
