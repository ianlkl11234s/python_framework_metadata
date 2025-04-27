---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/widgets/st.text_area
date: 2025-04-27 12:50:14
---

## st.text_area

Display a multi-line text input widget.

st.text_area(label, value="", height=None, max_chars=None, key=None, help=None, on_change=None, args=None, kwargs=None, *, placeholder=None, disabled=False, label_visibility="visible")

label(str)

A short label explaining to the user what this input is for.
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

value(object or None)

The text value of this widget when it first renders. This will be
cast to str internally. IfNone, will initialize empty and
returnNoneuntil the user provides input. Defaults to empty string.

height(int or None)

Desired height of the UI element expressed in pixels. If this isNone(default), the widget's initial height fits three lines.
The height must be at least 68 pixels, which fits two lines.

max_chars(int or None)

Maximum number of characters allowed in text area.

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

An optional callback invoked when this text_area's value changes.

args(tuple)

An optional tuple of args to pass to the callback.

kwargs(dict)

An optional dict of kwargs to pass to the callback.

placeholder(str or None)

An optional string displayed when the text area is empty. If None,
no text is displayed.

disabled(bool)

An optional boolean that disables the text area if set toTrue.
The default isFalse.

label_visibility("visible", "hidden", or "collapsed")

The visibility of the label. The default is"visible". If this
is"hidden", Streamlit displays an empty spacer instead of the
label, which can help keep the widget alligned with other widgets.
If this is"collapsed", Streamlit displays no label or spacer.

(str or None)

The current value of the text area widget orNoneif no value has been
provided by the user.

#### Example

```python

import streamlit as st

txt = st.text_area(
    "Text to analyze",
    "It was the best of times, it was the worst of times, it was the age of "
    "wisdom, it was the age of foolishness, it was the epoch of belief, it "
    "was the epoch of incredulity, it was the season of Light, it was the "
    "season of Darkness, it was the spring of hope, it was the winter of "
    "despair, (...)",
)

st.write(f"You wrote {len(txt)} characters.")

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
