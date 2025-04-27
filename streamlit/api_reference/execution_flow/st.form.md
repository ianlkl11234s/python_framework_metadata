---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/execution-flow/st.form
date: 2025-04-27 12:50:25
---

## st.form

Create a form that batches elements together with a "Submit" button.

A form is a container that visually groups other elements and
widgets together, and contains a Submit button. When the form's
Submit button is pressed, all widget values inside the form will be
sent to Streamlit in a batch.

To add elements to a form object, you can usewithnotation
(preferred) or just call methods directly on the form. See
examples below.

Forms have a few constraints:

- Every form must contain ast.form_submit_button.
- st.buttonandst.download_buttoncannot be added to a form.
- Forms can appear anywhere in your app (sidebar, columns, etc),
but they cannot be embedded inside other forms.
- Within a form, the only widget that can have a callback function isst.form_submit_button.
st.form(key, clear_on_submit=False, *, enter_to_submit=True, border=True)

key(str)

A string that identifies the form. Each form must have its own
key. (This key is not displayed to the user in the interface.)

clear_on_submit(bool)

If True, all widgets inside the form will be reset to their default
values after the user presses the Submit button. Defaults to False.
(Note that Custom Components are unaffected by this flag, and
will not be reset to their defaults on form submission.)

enter_to_submit(bool)

Whether to submit the form when a user presses Enter while
interacting with a widget inside the form.

If this isTrue(default), pressing Enter while interacting
with a form widget is equivalent to clicking the firstst.form_submit_buttonin the form.

If this isFalse, the user must click anst.form_submit_buttonto submit the form.

If the firstst.form_submit_buttonin the form is disabled,
the form will override submission behavior withenter_to_submit=False.

border(bool)

Whether to show a border around the form. Defaults to True.

Note

Not showing a border can be confusing to viewers since interacting with a
widget in the form will do nothing. You should only remove the border if
there's another border (e.g. because of an expander) or the form is small
(e.g. just a text input and a submit button).

#### Examples

Inserting elements usingwithnotation:

```python

import streamlit as st

with st.form("my_form"):
    st.write("Inside the form")
    slider_val = st.slider("Form slider")
    checkbox_val = st.checkbox("Form checkbox")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider_val, "checkbox", checkbox_val)
st.write("Outside the form")

```

Inserting elements out of order:

```python

import streamlit as st

form = st.form("my_form")
form.slider("Inside the form")
st.slider("Outside the form")

# Now add a submit button to the form:
form.form_submit_button("Submit")

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
