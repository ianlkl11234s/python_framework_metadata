---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/widgets/st.toggle
date: 2025-04-27 12:50:07
---

## st.toggle

Display a toggle widget.

st.toggle(label, value=False, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False, label_visibility="visible")

label(str)

A short label explaining to the user what this toggle is for.
The label can optionally contain GitHub-flavored Markdown of the
following types: Bold, Italics, Strikethroughs, Inline Code, Links,
and Images. Images display like icons, with a max height equal to
the font height.

Unsupported Markdown elements are unwrapped so only their children
(text contents) render. Display unsupported elements as literal
characters by backslash-escaping them. E.g.,"1\. Not an ordered list".

See thebodyparameter ofst.markdownfor additional,
supported Markdown directives.

For accessibility reasons, you should never set an empty label, but
you can hide it withlabel_visibilityif needed. In the future,
we may disallow empty labels by raising an exception.

value(bool)

Preselect the toggle when it first renders. This will be
cast to bool internally.

key(str or int)

An optional string or integer to use as the unique key for the widget.
If this is omitted, a key will be generated for the widget
based on its content. No two widgets may have the same key.

help(str or None)

A tooltip that gets displayed next to the widget label. Streamlit
only displays the tooltip whenlabel_visibility="visible". If
this isNone(default), no tooltip is displayed.

The tooltip can optionally contain GitHub-flavored Markdown,
including the Markdown directives described in thebodyparameter ofst.markdown.

on_change(callable)

An optional callback invoked when this toggle's value changes.

args(tuple)

An optional tuple of args to pass to the callback.

kwargs(dict)

An optional dict of kwargs to pass to the callback.

disabled(bool)

An optional boolean that disables the toggle if set toTrue.
The default isFalse.

label_visibility("visible", "hidden", or "collapsed")

The visibility of the label. The default is"visible". If this
is"hidden", Streamlit displays an empty spacer instead of the
label, which can help keep the widget alligned with other widgets.
If this is"collapsed", Streamlit displays no label or spacer.

(bool)

Whether or not the toggle is checked.

#### Example

```python

import streamlit as st

on = st.toggle("Activate feature")

if on:
    st.write("Feature activated!")

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
