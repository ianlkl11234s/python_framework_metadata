---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/execution-flow/st.rerun
date: 2025-04-27 12:50:32
---

## st.rerun

Rerun the script immediately.

Whenst.rerun()is called, Streamlit halts the current script run and
executes no further statements. Streamlit immediately queues the script to
rerun.

When usingst.rerunin a fragment, you can scope the rerun to the
fragment. However, if a fragment is running as part of a full-app rerun,
a fragment-scoped rerun is not allowed.

st.rerun(*, scope="app")

scope("app" or "fragment")

Specifies what part of the app should rerun. Ifscopeis"app"(default), the full app reruns. Ifscopeis"fragment",
Streamlit only reruns the fragment from which this command is called.

Settingscope="fragment"is only valid inside a fragment during a
fragment rerun. Ifst.rerun(scope="fragment")is called during a
full-app rerun or outside of a fragment, Streamlit will raise aStreamlitAPIException.

### Caveats forst.rerun

`st.rerun`

st.rerunis one of the tools to control the logic of your app. While it is great for prototyping, there can be adverse side effects:

`st.rerun`

- Additional script runs may be inefficient and slower.
- Excessive reruns may complicate your app's logic and be harder to follow.
- If misused, infinite looping may crash your app.
In many cases wherest.rerunworks,callbacksmay be a cleaner alternative.Containersmay also be helpful.

`st.rerun`

### A simple example in three variations

###### Usingst.rerunto update an earlier header

`st.rerun`

`import streamlit as st

if "value" not in st.session_state:
    st.session_state.value = "Title"

##### Option using st.rerun #####
st.header(st.session_state.value)

if st.button("Foo"):
    st.session_state.value = "Foo"
    st.rerun()`

###### Using a callback to update an earlier header

`##### Option using a callback #####
st.header(st.session_state.value)

def update_value():
    st.session_state.value = "Bar"

st.button("Bar", on_click=update_value)`

###### Using containers to update an earlier header

`##### Option using a container #####
container = st.container()

if st.button("Baz"):
    st.session_state.value = "Baz"

container.header(st.session_state.value)`

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
