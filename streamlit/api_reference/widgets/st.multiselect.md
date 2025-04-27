---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/widgets/st.multiselect
date: 2025-04-27 12:50:02
---

## st.multiselect

Display a multiselect widget.

The multiselect widget starts as empty.

st.multiselect(label, options, default=None, format_func=special_internal_function, key=None, help=None, on_change=None, args=None, kwargs=None, *, max_selections=None, placeholder="Choose an option", disabled=False, label_visibility="visible")

label(str)

A short label explaining to the user what this select widget is for.
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

options(Iterable)

Labels for the select options in anIterable. This can be alist,set, or anything supported byst.dataframe. Ifoptionsis dataframe-like, the first column will be used. Each
label will be cast tostrinternally by default.

default(Iterable of V, V, or None)

List of default values. Can also be a single value.

format_func(function)

Function to modify the display of the options. It receives
the raw option as an argument and should output the label to be
shown for that option. This has no impact on the return value of
the command.

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

An optional callback invoked when this widget's value changes.

args(tuple)

An optional tuple of args to pass to the callback.

kwargs(dict)

An optional dict of kwargs to pass to the callback.

max_selections(int)

The max selections that can be selected at a time.

placeholder(str)

A string to display when no options are selected.
Defaults to "Choose an option."

disabled(bool)

An optional boolean that disables the multiselect widget if set
toTrue. The default isFalse.

label_visibility("visible", "hidden", or "collapsed")

The visibility of the label. The default is"visible". If this
is"hidden", Streamlit displays an empty spacer instead of the
label, which can help keep the widget alligned with other widgets.
If this is"collapsed", Streamlit displays no label or spacer.

(list)

A list with the selected options

#### Example

```python

import streamlit as st

options = st.multiselect(
    "What are your favorite colors",
    ["Green", "Yellow", "Red", "Blue"],
    ["Yellow", "Red"],
)

st.write("You selected:", options)

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
