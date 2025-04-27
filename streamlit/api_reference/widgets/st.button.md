---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/widgets/st.button
date: 2025-04-27 12:49:57
---

## st.button

Display a button widget.

st.button(label, key=None, help=None, on_click=None, args=None, kwargs=None, *, type="secondary", icon=None, disabled=False, use_container_width=False)

label(str)

A short label explaining to the user what this button is for.
The label can optionally contain GitHub-flavored Markdown of the
following types: Bold, Italics, Strikethroughs, Inline Code, Links,
and Images. Images display like icons, with a max height equal to
the font height.

Unsupported Markdown elements are unwrapped so only their children
(text contents) render. Display unsupported elements as literal
characters by backslash-escaping them. E.g.,"1\. Not an ordered list".

See thebodyparameter ofst.markdownfor additional,
supported Markdown directives.

key(str or int)

An optional string or integer to use as the unique key for the widget.
If this is omitted, a key will be generated for the widget
based on its content. No two widgets may have the same key.

help(str or None)

A tooltip that gets displayed when the button is hovered over. If
this isNone(default), no tooltip is displayed.

The tooltip can optionally contain GitHub-flavored Markdown,
including the Markdown directives described in thebodyparameter ofst.markdown.

on_click(callable)

An optional callback invoked when this button is clicked.

args(tuple)

An optional tuple of args to pass to the callback.

kwargs(dict)

An optional dict of kwargs to pass to the callback.

type("primary", "secondary", or "tertiary")

An optional string that specifies the button type. This can be one
of the following:

- "primary": The button's background is the app's primary color
for additional emphasis.
- "secondary"(default): The button's background coordinates
with the app's background color for normal emphasis.
- "tertiary": The button is plain text without a border or
background for subtly.
icon(str or None)

An optional emoji or icon to display next to the button label. IficonisNone(default), no icon is displayed. Ificonis a
string, the following options are valid:

- A single-character emoji. For example, you can seticon="🚨"oricon="🔥". Emoji short codes are not supported.
- An icon from the Material Symbols library (rounded style) in the
format":material/icon_name:"where "icon_name" is the name
of the icon in snake case.For example,icon=":material/thumb_up:"will display the
Thumb Up icon. Find additional icons in theMaterial Symbolsfont library.
A single-character emoji. For example, you can seticon="🚨"oricon="🔥". Emoji short codes are not supported.

An icon from the Material Symbols library (rounded style) in the
format":material/icon_name:"where "icon_name" is the name
of the icon in snake case.

For example,icon=":material/thumb_up:"will display the
Thumb Up icon. Find additional icons in theMaterial Symbolsfont library.

disabled(bool)

An optional boolean that disables the button if set toTrue.
The default isFalse.

use_container_width(bool)

Whether to expand the button's width to fill its parent container.
Ifuse_container_widthisFalse(default), Streamlit sizes
the button to fit its contents. Ifuse_container_widthisTrue, the width of the button matches its parent container.

In both cases, if the contents of the button are wider than the
parent container, the contents will line wrap.

(bool)

True if the button was clicked on the last run of the app,
False otherwise.

#### Examples

Example 1: Customize your button type

```python

import streamlit as st

st.button("Reset", type="primary")
if st.button("Say hello"):
    st.write("Why hello there")
else:
    st.write("Goodbye")

if st.button("Aloha", type="tertiary"):
    st.write("Ciao")

```

Example 2: Add icons to your button

Although you can add icons to your buttons through Markdown, theiconparameter is a convenient and consistent alternative.

```python

import streamlit as st

left, middle, right = st.columns(3)
if left.button("Plain button", use_container_width=True):
    left.markdown("You clicked the plain button.")
if middle.button("Emoji button", icon="😃", use_container_width=True):
    middle.markdown("You clicked the emoji button.")
if right.button("Material button", icon=":material/mood:", use_container_width=True):
    right.markdown("You clicked the Material button.")

```

### Advanced functionality

Although a button is the simplest of input widgets, it's very common for buttons to be deeply tied to the use ofst.session_state. Check out our advanced guide onButton behavior and examples.

`st.session_state`

### Featured videos

Check out our video on how to use one of Streamlit's core functions, the button!

In the video below, we'll take it a step further and learn how to combine abutton,checkboxandradio button!

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
