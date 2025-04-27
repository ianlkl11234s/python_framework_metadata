---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/widgets/st.feedback
date: 2025-04-27 12:49:56
---

## st.feedback

Display a feedback widget.

A feedback widget is an icon-based button group available in three
styles, as described inoptions. It is commonly used in chat and AI
apps to allow users to rate responses.

st.feedback(options="thumbs", *, key=None, disabled=False, on_change=None, args=None, kwargs=None)

options("thumbs", "faces", or "stars")

The feedback options displayed to the user.optionscan be one
of the following:

- "thumbs"(default): Streamlit displays a thumb-up and
thumb-down button group.
- "faces": Streamlit displays a row of five buttons with
facial expressions depicting increasing satisfaction from left to
right.
- "stars": Streamlit displays a row of star icons, allowing the
user to select a rating from one to five stars.
key(str or int)

An optional string or integer to use as the unique key for the widget.
If this is omitted, a key will be generated for the widget
based on its content. No two widgets may have the same key.

disabled(bool)

An optional boolean that disables the feedback widget if set
toTrue. The default isFalse.

on_change(callable)

An optional callback invoked when this feedback widget's value
changes.

args(tuple)

An optional tuple of args to pass to the callback.

kwargs(dict)

An optional dict of kwargs to pass to the callback.

(int or None)

An integer indicating the user's selection, where0is the
lowest feedback. Higher values indicate more positive feedback.
If no option was selected, the widget returnsNone.

- Foroptions="thumbs", a return value of0indicates
thumbs-down, and1indicates thumbs-up.
- Foroptions="faces"andoptions="stars", return values
range from0(least satisfied) to4(most satisfied).
#### Examples

Display a feedback widget with stars, and show the selected sentiment:

```python

import streamlit as st

sentiment_mapping = ["one", "two", "three", "four", "five"]
selected = st.feedback("stars")
if selected is not None:
    st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")

```

Display a feedback widget with thumbs, and show the selected sentiment:

```python

import streamlit as st

sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]
selected = st.feedback("thumbs")
if selected is not None:
    st.markdown(f"You selected: {sentiment_mapping[selected]}")

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
