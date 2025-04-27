---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/charts/st.bokeh_chart
date: 2025-04-27 12:49:43
---

## st.bokeh_chart

Display an interactive Bokeh chart.

Bokeh is a charting library for Python. The arguments to this function
closely follow the ones for Bokeh'sshowfunction. You can find
more about Bokeh athttps://bokeh.pydata.org.

To show Bokeh charts in Streamlit, callst.bokeh_chartwherever you would call Bokeh'sshow.

Important

You must installbokeh==2.4.3andnumpy<2to use this
command.

If you need a newer version of Bokeh, use ourstreamlit-bokehcustom component instead.

st.bokeh_chart(figure, use_container_width=True)

figure(bokeh.plotting.figure.Figure)

A Bokeh figure to plot.

use_container_width(bool)

Whether to override the figure's native width with the width of
the parent container. Ifuse_container_widthisTrue(default),
Streamlit sets the width of the figure to match the width of the parent
container. Ifuse_container_widthisFalse, Streamlit sets the
width of the chart to fit its contents according to the plotting library,
up to the width of the parent container.

#### Example

```python

import streamlit as st
from bokeh.plotting import figure

x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]

p = figure(title="simple line example", x_axis_label="x", y_axis_label="y")
p.line(x, y, legend_label="Trend", line_width=2)

st.bokeh_chart(p)

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
