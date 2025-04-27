---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/concepts/architecture/fragments
date: 2025-04-27 12:48:01
---

# Working with fragments

Reruns are a central part of every Streamlit app. When users interact with widgets, your script reruns from top to bottom, and your app's frontend is updated. Streamlit provides several features to help you develop your app within this execution model. Streamlit version 1.37.0 introduced fragments to allow rerunning a portion of your code instead of your full script. As your app grows larger and more complex, these fragment reruns help your app be efficient and performant. Fragments give you finer, easy-to-understand control over your app's execution flow.

Before you read about fragments, we recommend having a basic understanding ofcaching,Session State, andforms.

## Use cases for fragments

Fragments are versatile and applicable to a wide variety of circumstances. Here are just a few, common scenarios where fragments are useful:

- Your app has multiple visualizations and each one takes time to load, but you have a filter input that only updates one of them.
- You have a dynamic form that doesn't need to update the rest of your app (until the form is complete).
- You want to automatically update a single component or group of components to stream data.
## Defining and calling a fragment

Streamlit provides a decorator (st.fragment) to turn any function into a fragment function. When you call a fragment function that contains a widget function, a user triggers afragment reruninstead of a full rerun when they interact with that fragment's widget. During a fragment rerun, only your fragment function is re-executed. Anything within the main body of your fragment is updated on the frontend, while the rest of your app remains the same. We'll describe fragments written across multiple containers later on.

`st.fragment`

Here is a basic example of defining and calling a fragment function. Just like with caching, remember to call your function after defining it.

`import streamlit as st

@st.fragment
def fragment_function():
    if st.button("Hi!"):
        st.write("Hi back!")

fragment_function()`

If you want the main body of your fragment to appear in the sidebar or another container, call your fragment function inside a context manager.

`with st.sidebar:
    fragment_function()`

### Fragment execution flow

Consider the following code with the explanation and diagram below.

`import streamlit as st

st.title("My Awesome App")

@st.fragment()
def toggle_and_text():
    cols = st.columns(2)
    cols[0].toggle("Toggle")
    cols[1].text_area("Enter text")

@st.fragment()
def filter_and_file():
    cols = st.columns(2)
    cols[0].checkbox("Filter")
    cols[1].file_uploader("Upload image")

toggle_and_text()
cols = st.columns(2)
cols[0].selectbox("Select", [1,2,3], None)
cols[1].button("Update")
filter_and_file()`

When a user interacts with an input widget inside a fragment, only the fragment reruns instead of the full script. When a user interacts with an input widget outside a fragment, the full script reruns as usual.

If you run the code above, the full script will run top to bottom on your app's initial load. If you flip the toggle button in your running app, the first fragment (toggle_and_text()) will rerun, redrawing the toggle and text area while leaving everything else unchanged. If you click the checkbox, the second fragment (filter_and_file()) will rerun and consequently redraw the checkbox and file uploader. Everything else remains unchanged. Finally, if you click the update button, the full script will rerun, and Streamlit will redraw everything.

`toggle_and_text()`

`filter_and_file()`

## Fragment return values and interacting with the rest of your app

Streamlit ignores fragment return values during fragment reruns, so defining return values for your fragment functions is not recommended. Instead, if your fragment needs to share data with the rest of your app, use Session State. Fragments are just functions in your script, so they can access Session State, imported modules, and other Streamlit elements like containers. If your fragment writes to any container created outside of itself, note the following difference in behavior:

- Elements drawn in the main body of your fragment are cleared and redrawn in place during a fragment rerun. Repeated fragment reruns will not cause additional elements to appear.
- Elements drawn to containers outside the main body of fragment will not be cleared with each fragment rerun. Instead, Streamlit will draw them additively and these elements will accumulate until the next full-script rerun.
- A fragment can't draw widgets in containers outside of the main body of the fragment. Widgets can only go in the main body of a fragment.
To prevent elements from accumulating in outside containers, usest.emptycontainers. For a related tutorial, seeCreate a fragment across multiple containers.

`st.empty`

If you need to trigger a full-script rerun from inside a fragment, callst.rerun. For a related tutorial, seeTrigger a full-script rerun from inside a fragment.

`st.rerun`

## Automate fragment reruns

st.fragmentincludes a convenientrun_everyparameter that causes the fragment to rerun automatically at the specified time interval. These reruns are in addition to any reruns (fragment or full-script) triggered by your user. The automatic fragment reruns will continue even if your user is not interacting with your app. This is a great way to show a live data stream or status on a running background job, efficiently updating your rendered data andonlyyour rendered data.

`st.fragment`

`run_every`

`@st.fragment(run_every="10s")
def auto_function():
		# This will update every 10 seconds!
		df = get_latest_updates()
		st.line_chart(df)

auto_function()`

For a related tutorial, seeStart and stop a streaming fragment.

## Compare fragments to other Streamlit features

### Fragments vs forms

Here is a comparison between fragments and forms:

- Formsallow users to interact with widgets without rerunning your app. Streamlit does not send user actions within a form to your app's Python backend until the form is submitted. Widgets within a form can not dynamically update other widgets (in or out of the form) in real-time.
- Fragmentsrun independently from the rest of your code. As your users interact with fragment widgets, their actions are immediately processed by your app's Python backend and your fragment code is rerun. Widgets within a fragment can dynamically update other widgets within the same fragment in real-time.
A form batches user input without interaction between any widgets. A fragment immediately processes user input but limits the scope of the rerun.

### Fragments vs callbacks

Here is a comparison between fragments and callbacks:

- Callbacksallow you to execute a function at the beginning of a script rerun. A callback is asingle prefixto your script rerun.
- Fragmentsallow you to rerun a portion of your script. A fragment is arepeatable postfixto your script, running each time a user interacts with a fragment widget, or automatically in sequence whenrun_everyis set.
`run_every`

When callbacks render elements to your page, they are rendered before the rest of your page elements. When fragments render elements to your page, they are updated with each fragment rerun (unless they are written to containers outside of the fragment, in which case they accumulate there).

### Fragments vs custom components

Here is a comparison between fragments and custom components:

- Componentsare custom frontend code that can interact with the Python code, native elements, and widgets in your Streamlit app. Custom components extend what’s possible with Streamlit. They follow the normal Streamlit execution flow.
- Fragmentsare parts of your app that can rerun independently of the full app. Fragments can be composed of multiple Streamlit elements, widgets, or any Python code.
A fragment can include one or more custom components. A custom component could not easily include a fragment!

### Fragments vs caching

Here is a comparison between fragments and caching:

- Caching:allows you to skip over a function and return a previously computed value. When you use caching, you execute everything except the cached function (if you've already run it before).
- Fragments:allow you to freeze most of your app and just execute the fragment. When you use fragments, you execute only the fragment (when triggering a fragment rerun).
Caching saves you from unnecessarily running a piece of your app while the rest runs. Fragments save you from running your full app when you only want to run one piece.

## Limitations and unsupported behavior

- Fragments can't detect a change in input values. It is best to use Session State for dynamic input and output for fragment functions.
- Using caching and fragments on the same function is unsupported.
- Fragments can't render widgets in externally-created containers; widgets can only be in the main body of a fragment.
### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
