---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/widgets/st.time_input
date: 2025-04-27 12:50:12
---

## st.time_input

Display a time input widget.

st.time_input(label, value="now", key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False, label_visibility="visible", step=0:15:00)

label(str)

A short label explaining to the user what this time input is for.
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

value("now", datetime.time, datetime.datetime, str, or None)

The value of this widget when it first renders. This can be one of
the following:

- "now"(default): The widget initializes with the current time.
- Adatetime.timeordatetime.datetimeobject: The widget
initializes with the given time, ignoring any date if included.
- An ISO-formatted time ("hh:mm", "hh:mm:ss", or "hh:mm:ss.sss") or
datetime ("YYYY-MM-DD hh:mm:ss") string: The widget initializes
with the given time, ignoring any date if included.
- None: The widget initializes with no time and returnsNoneuntil the user selects a time.
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

An optional callback invoked when this time_input's value changes.

args(tuple)

An optional tuple of args to pass to the callback.

kwargs(dict)

An optional dict of kwargs to pass to the callback.

disabled(bool)

An optional boolean that disables the time input if set toTrue. The default isFalse.

label_visibility("visible", "hidden", or "collapsed")

The visibility of the label. The default is"visible". If this
is"hidden", Streamlit displays an empty spacer instead of the
label, which can help keep the widget alligned with other widgets.
If this is"collapsed", Streamlit displays no label or spacer.

step(int or timedelta)

The stepping interval in seconds. Defaults to 900, i.e. 15 minutes.
You can also pass a datetime.timedelta object.

(datetime.time or None)

The current value of the time input widget orNoneif no time has been
selected.

#### Example

```python

import datetime
import streamlit as st

t = st.time_input("Set an alarm for", datetime.time(8, 45))
st.write("Alarm is set for", t)

```

To initialize an empty time input, useNoneas the value:

```python

import datetime
import streamlit as st

t = st.time_input("Set an alarm for", value=None)
st.write("Alarm is set for", t)

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
