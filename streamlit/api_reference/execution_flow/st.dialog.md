---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/execution-flow/st.dialog
date: 2025-04-27 12:50:23
---

## st.dialog

Function decorator to create a modal dialog.

A function decorated with@st.dialogbecomes a dialog
function. When you call a dialog function, Streamlit inserts a modal dialog
into your app. Streamlit element commands called within the dialog function
render inside the modal dialog.

The dialog function can accept arguments that can be passed when it is
called. Any values from the dialog that need to be accessed from the wider
app should generally be stored in Session State.

A user can dismiss a modal dialog by clicking outside of it, clicking the
"X" in its upper-right corner, or pressingESCon their keyboard.
Dismissing a modal dialog does not trigger an app rerun. To close the modal
dialog programmatically, callst.rerun()explicitly inside of the
dialog function.

st.dialoginherits behavior fromst.fragment.
When a user interacts with an input widget created inside a dialog function,
Streamlit only reruns the dialog function instead of the full script.

Callingst.sidebarin a dialog function is not supported.

Dialog code can interact with Session State, imported modules, and other
Streamlit elements created outside the dialog. Note that these interactions
are additive across multiple dialog reruns. You are responsible for
handling any side effects of that behavior.

Warning

Only one dialog function may be called in a script run, which means
that only one dialog can be open at any given time.

st.dialog(title, *, width="small")

title(str)

The title to display at the top of the modal dialog. It cannot be empty.

width("small", "large")

The width of the modal dialog. Ifwidthis"small(default), the
modal dialog will be 500 pixels wide. Ifwidthis"large", the
modal dialog will be about 750 pixels wide.

#### Examples

The following example demonstrates the basic usage of@st.dialog.
In this app, clicking "A" or "B" will open a modal dialog and prompt you
to enter a reason for your vote. In the modal dialog, click "Submit" to record
your vote into Session State and rerun the app. This will close the modal dialog
since the dialog function is not called during the full-script rerun.

```python

import streamlit as st

@st.dialog("Cast your vote")
def vote(item):
    st.write(f"Why is {item} your favorite?")
    reason = st.text_input("Because...")
    if st.button("Submit"):
        st.session_state.vote = {"item": item, "reason": reason}
        st.rerun()

if "vote" not in st.session_state:
    st.write("Vote for your favorite")
    if st.button("A"):
        vote("A")
    if st.button("B"):
        vote("B")
else:
    f"You voted for {st.session_state.vote['item']} because {st.session_state.vote['reason']}"

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
