---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/data/st.metric
date: 2025-04-27 12:49:10
---

## st.metric

Display a metric in big bold font, with an optional indicator of how the metric changed.

Tip: If you want to display a large number, it may be a good idea to
shorten it using packages likemillifyornumerize. E.g.1234can be
displayed as1.2kusingst.metric("Shortnumber", millify(1234)).

st.metric(label, value, delta=None, delta_color="normal", help=None, label_visibility="visible", border=False)

label(str)

The header or title for the metric. The label can optionally
contain GitHub-flavored Markdown of the following types: Bold, Italics,
Strikethroughs, Inline Code, Links, and Images. Images display like
icons, with a max height equal to the font height.

Unsupported Markdown elements are unwrapped so only their children
(text contents) render. Display unsupported elements as literal
characters by backslash-escaping them. E.g.,"1\. Not an ordered list".

See thebodyparameter ofst.markdownfor additional,
supported Markdown directives.

value(int, float, str, or None)

Value of the metric. None is rendered as a long dash.

delta(int, float, str, or None)

Indicator of how the metric changed, rendered with an arrow below
the metric. If delta is negative (int/float) or starts with a minus
sign (str), the arrow points down and the text is red; else the
arrow points up and the text is green. If None (default), no delta
indicator is shown.

delta_color("normal", "inverse", or "off")

If "normal" (default), the delta indicator is shown as described
above. If "inverse", it is red when positive and green when
negative. This is useful when a negative change is considered
good, e.g. if cost decreased. If "off", delta is  shown in gray
regardless of its value.

help(str or None)

A tooltip that gets displayed next to the metric label. Streamlit
only displays the tooltip whenlabel_visibility="visible". If
this isNone(default), no tooltip is displayed.

The tooltip can optionally contain GitHub-flavored Markdown,
including the Markdown directives described in thebodyparameter ofst.markdown.

label_visibility("visible", "hidden", or "collapsed")

The visibility of the label. The default is"visible". If this
is"hidden", Streamlit displays an empty spacer instead of the
label, which can help keep the widget alligned with other widgets.
If this is"collapsed", Streamlit displays no label or spacer.

border(bool)

Whether to show a border around the metric container. If this isFalse(default), no border is shown. If this isTrue, a
border is shown.

#### Examples

Example 1: Show a metric

```python

import streamlit as st

st.metric(label="Temperature", value="70 °F", delta="1.2 °F")

```

Example 2: Create a row of metrics

st.metriclooks especially nice in combination withst.columns.

```python

import streamlit as st

col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

```

Example 3: Modify the delta indicator

The delta indicator color can also be inverted or turned off.

```python

import streamlit as st

st.metric(label="Gas price", value=4, delta=-0.5, delta_color="inverse")

st.metric(
    label="Active developers", value=123, delta=123, delta_color="off"
)

```

Example 4: Create a grid of metric cards

Add borders to your metrics to create a dashboard look.

```python

import streamlit as st

a, b = st.columns(2)
c, d = st.columns(2)

a.metric("Temperature", "30°F", "-9°F", border=True)
b.metric("Wind", "4 mph", "2 mph", border=True)

c.metric("Humidity", "77%", "5%", border=True)
d.metric("Pressure", "30.34 inHg", "-2 inHg", border=True)

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
