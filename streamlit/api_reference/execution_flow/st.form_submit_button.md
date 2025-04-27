---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/execution-flow/st.form_submit_button
date: 2025-04-27 12:50:28
---

## st.form_submit_button

Display a form submit button.

When this button is clicked, all widget values inside the form will be
sent from the user's browser to your Streamlit server in a batch.

Every form must have at least onest.form_submit_button. Anst.form_submit_buttoncannot exist outside of a form.

For more information about forms, check out ourdocs.

st.form_submit_button(label="Submit", help=None, on_click=None, args=None, kwargs=None, *, type="secondary", icon=None, disabled=False, use_container_width=False)

label(str)

A short label explaining to the user what this button is for. This
defaults to"Submit". The label can optionally contain
GitHub-flavored Markdown of the following types: Bold, Italics,
Strikethroughs, Inline Code, Links, and Images. Images display like
icons, with a max height equal to the font height.

Unsupported Markdown elements are unwrapped so only their children
(text contents) render. Display unsupported elements as literal
characters by backslash-escaping them. E.g.,"1\. Not an ordered list".

See thebodyparameter ofst.markdownfor additional,
supported Markdown directives.

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

Whether to disable the button. If this isFalse(default), the
user can interact with the button. If this isTrue, the button
is grayed-out and can't be clicked.

If the firstst.form_submit_buttonin the form is disabled,
the form will override submission behavior withenter_to_submit=False.

use_container_width(bool)

Whether to expand the button's width to fill its parent container.
Ifuse_container_widthisFalse(default), Streamlit sizes
the button to fit its contents. Ifuse_container_widthisTrue, the width of the button matches its parent container.

In both cases, if the contents of the button are wider than the
parent container, the contents will line wrap.

(bool)

True if the button was clicked.

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
