---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/widgets/st.date_input
date: 2025-04-27 12:50:09
---

## st.date_input

Display a date input widget.

The first day of the week is determined from the user's locale in their
browser.

st.date_input(label, value="today", min_value=None, max_value=None, key=None, help=None, on_change=None, args=None, kwargs=None, *, format="YYYY/MM/DD", disabled=False, label_visibility="visible")

label(str)

A short label explaining to the user what this date input is for.
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

value("today", datetime.date, datetime.datetime, str, list/tuple of these, or None)

The value of this widget when it first renders. This can be one of
the following:

- "today"(default): The widget initializes with the current date.
- Adatetime.dateordatetime.datetimeobject: The widget
initializes with the given date, ignoring any time if included.
- An ISO-formatted date ("YYYY-MM-DD") or datetime
("YYYY-MM-DD hh:mm:ss") string: The widget initializes with the
given date, ignoring any time if included.
- A list or tuple with up to two of the above: The widget will
initialize with the given date interval and return a tuple of the
selected interval. You can pass an empty list to initialize the
widget with an empty interval or a list with one value to
initialize only the beginning date of the iterval.
- None: The widget initializes with no date and returnsNoneuntil the user selects a date.
min_value("today", datetime.date, datetime.datetime, str, or None)

The minimum selectable date. This can be any of the date types
accepted byvalue, except list or tuple.

If this isNone(default), the minimum selectable date is ten
years before the initial value. If the initial value is an
interval, the minimum selectable date is ten years before the start
date of the interval. If no initial value is set, the minimum
selectable date is ten years before today.

max_value("today", datetime.date, datetime.datetime, str, or None)

The maximum selectable date. This can be any of the date types
accepted byvalue, except list or tuple.

If this isNone(default), the maximum selectable date is ten
years after the initial value. If the initial value is an interval,
the maximum selectable date is ten years after the end date of the
interval. If no initial value is set, the maximum selectable date
is ten years after today.

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

An optional callback invoked when this date_input's value changes.

args(tuple)

An optional tuple of args to pass to the callback.

kwargs(dict)

An optional dict of kwargs to pass to the callback.

format(str)

A format string controlling how the interface should display dates.
Supports "YYYY/MM/DD" (default), "DD/MM/YYYY", or "MM/DD/YYYY".
You may also use a period (.) or hyphen (-) as separators.

disabled(bool)

An optional boolean that disables the date input if set toTrue. The default isFalse.

label_visibility("visible", "hidden", or "collapsed")

The visibility of the label. The default is"visible". If this
is"hidden", Streamlit displays an empty spacer instead of the
label, which can help keep the widget alligned with other widgets.
If this is"collapsed", Streamlit displays no label or spacer.

(datetime.date or a tuple with 0-2 dates or None)

The current value of the date input widget orNoneif no date has been
selected.

#### Examples

```python

import datetime
import streamlit as st

d = st.date_input("When's your birthday", datetime.date(2019, 7, 6))
st.write("Your birthday is:", d)

```

```python

import datetime
import streamlit as st

today = datetime.datetime.now()
next_year = today.year + 1
jan_1 = datetime.date(next_year, 1, 1)
dec_31 = datetime.date(next_year, 12, 31)

d = st.date_input(
    "Select your vacation for next year",
    (jan_1, datetime.date(next_year, 1, 7)),
    jan_1,
    dec_31,
    format="MM.DD.YYYY",
)
d

```

To initialize an empty date input, useNoneas the value:

```python

import datetime
import streamlit as st

d = st.date_input("When's your birthday", value=None)
st.write("Your birthday is:", d)

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
