---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/concepts/architecture/run-your-app
date: 2025-04-27 12:47:48
---

# Run your Streamlit app

Working with Streamlit is simple. First you sprinkle a few Streamlit commands into a normal Python script, and then you run it. We list few ways to run your script, depending on your use case.

## Use streamlit run

Once you've created your script, sayyour_script.py, the easiest way to run it is withstreamlit run:

`your_script.py`

`streamlit run`

`streamlit run your_script.py`

As soon as you run the script as shown above, a local Streamlit server will spin up and your app will open in a new tab in your default web browser.

### Pass arguments to your script

When passing your script some custom arguments, they must be passed after two dashes. Otherwise the arguments get interpreted as arguments to Streamlit itself:

`streamlit run your_script.py [-- script args]`

### Pass a URL to streamlit run

You can also pass a URL tostreamlit run! This is great when your script is hosted remotely, such as a GitHub Gist. For example:

`streamlit run`

`streamlit run https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/streamlit_app.py`

## Run Streamlit as a Python module

Another way of running Streamlit is to run it as a Python module. This is useful when configuring an IDE like PyCharm to work with Streamlit:

`# Running
python -m streamlit run your_script.py`

`# is equivalent to:
streamlit run your_script.py`

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
