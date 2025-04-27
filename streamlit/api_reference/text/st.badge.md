---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/text/st.badge
date: 2025-04-27 12:48:53
---

## st.badge

Display a colored badge with an icon and label.

This is a thin wrapper around the color-badge Markdown directive.
The following are equivalent:

- st.markdown(":blue-badge[Home]")
- st.badge("Home",color="blue")
Note

You can insert badges everywhere Streamlit supports Markdown by
using the color-badge Markdown directive. Seest.markdownfor
more information.

st.badge(label, *, icon=None, color="blue")

label(str)

The label to display in the badge. The label can optionally contain
GitHub-flavored Markdown of the following types: Bold, Italics,
Strikethroughs, Inline Code.

See thebodyparameter ofst.markdownfor additional,
supported Markdown directives. Because this command escapes square
brackets ([ ]) in this parameter, any directive requiring
square brackets is not supported.

icon(str or None)

An optional emoji or icon to display next to the badge label. IficonisNone(default), no icon is displayed. Ificonis a string, the following options are valid:

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

color(str)

The color to use for the badge. This defaults to"blue".

This can be one of the following supported colors: blue, green,
orange, red, violet, gray/grey, or primary. If you use"primary", Streamlit will use the default primary accent color
unless you set thetheme.primaryColorconfiguration option.

#### Examples

Create standalone badges withst.badge(with or without icons). If
you want to have multiple, side-by-side badges, you can use the
Markdown directive inst.markdown.

```python

import streamlit as st

st.badge("New")
st.badge("Success", icon=":material/check:", color="green")

st.markdown(
    ":violet-badge[:material/star: Favorite] :orange-badge[⚠️ Needs review] :gray-badge[Deprecated]"
)

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
