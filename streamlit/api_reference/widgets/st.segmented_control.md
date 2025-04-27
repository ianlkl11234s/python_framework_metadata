---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/widgets/st.segmented_control
date: 2025-04-27 12:50:04
---

## st.segmented_control

Display a segmented control widget.

A segmented control widget is a linear set of segments where each of
the passedoptionsfunctions like a toggle button.

st.segmented_control(label, options, *, selection_mode="single", default=None, format_func=None, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")

label(str)

A short label explaining to the user what this widget is for.
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

options(Iterable of V)

Labels for the select options in anIterable. This can be alist,set, or anything supported byst.dataframe. Ifoptionsis dataframe-like, the first column will be used. Each
label will be cast tostrinternally by default and can
optionally contain GitHub-flavored Markdown, including the Markdown
directives described in thebodyparameter ofst.markdown.

selection_mode("single" or "multi")

The selection mode for the widget. If this is"single"(default), only one option can be selected. If this is"multi",
multiple options can be selected.

default(Iterable of V, V, or None)

The value of the widget when it first renders. If theselection_modeismulti, this can be a list of values, a
single value, orNone. If theselection_modeis"single", this can be a single value orNone.

format_func(function)

Function to modify the display of the options. It receives
the raw option as an argument and should output the label to be
shown for that option. This has no impact on the return value of
the command. The output can optionally contain GitHub-flavored
Markdown, including the Markdown directives described in thebodyparameter ofst.markdown.

key(str or int)

An optional string or integer to use as the unique key for the widget.
If this is omitted, a key will be generated for the widget
based on its content. Multiple widgets of the same type may
not share the same key.

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

disabled(bool)

An optional boolean that disables the widget if set toTrue.
The default isFalse.

label_visibility("visible", "hidden", or "collapsed")

The visibility of the label. The default is"visible". If this
is"hidden", Streamlit displays an empty spacer instead of the
label, which can help keep the widget alligned with other widgets.
If this is"collapsed", Streamlit displays no label or spacer.

(list of V, V, or None)

If theselection_modeismulti, this is a list of selected
options or an empty list. If theselection_modeis"single", this is a selected option orNone.

#### Examples

Example 1: Multi-select segmented control

Display a multi-select segmented control widget, and show the
selection:

```python

import streamlit as st

options = ["North", "East", "South", "West"]
selection = st.segmented_control(
    "Directions", options, selection_mode="multi"
)
st.markdown(f"Your selected options: {selection}.")

```

Example 2: Single-select segmented control with icons

Display a single-select segmented control widget with icons:

```python

import streamlit as st

option_map = {
    0: ":material/add:",
    1: ":material/zoom_in:",
    2: ":material/zoom_out:",
    3: ":material/zoom_out_map:",
}
selection = st.segmented_control(
    "Tool",
    options=option_map.keys(),
    format_func=lambda option: option_map[option],
    selection_mode="single",
)
st.write(
    "Your selected option: "
    f"{None if selection is None else option_map[selection]}"
)

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
