---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/charts/st.altair_chart
date: 2025-04-27 12:49:41
---

## st.altair_chart

Display a chart using the Vega-Altair library.

Vega-Altairis a declarative
statistical visualization library for Python, based on Vega and
Vega-Lite.

st.altair_chart(altair_chart, *, use_container_width=None, theme="streamlit", key=None, on_select="ignore", selection_mode=None)

altair_chart(altair.Chart)

The Altair chart object to display. Seehttps://altair-viz.github.io/gallery/for examples of graph
descriptions.

use_container_width(bool or None)

Whether to override the chart's native width with the width of
the parent container. This can be one of the following:

- None(default): Streamlit will use the parent container's
width for all charts except those with known incompatibility
(altair.Facet,altair.HConcatChart, andaltair.RepeatChart).
- True: Streamlit sets the width of the chart to match the
width of the parent container.
- False: Streamlit sets the width of the chart to fit its
contents according to the plotting library, up to the width of
the parent container.
theme("streamlit" or None)

The theme of the chart. Ifthemeis"streamlit"(default),
Streamlit uses its own design default. IfthemeisNone,
Streamlit falls back to the default behavior of the library.

key(str)

An optional string to use for giving this element a stable
identity. IfkeyisNone(default), this element's identity
will be determined based on the values of the other parameters.

Additionally, if selections are activated andkeyis provided,
Streamlit will register the key in Session State to store the
selection state. The selection state is read-only.

on_select("ignore", "rerun", or callable)

How the figure should respond to user selection events. This
controls whether or not the figure behaves like an input widget.on_selectcan be one of the following:

- "ignore"(default): Streamlit will not react to any selection
events in the chart. The figure will not behave like an input
widget.
- "rerun": Streamlit will rerun the app when the user selects
data in the chart. In this case,st.altair_chartwill return
the selection data as a dictionary.
- Acallable: Streamlit will rerun the app and execute thecallableas a callback function before the rest of the app.
In this case,st.altair_chartwill return the selection data
as a dictionary.
To use selection events, the object passed toaltair_chartmust
include selection paramters. To learn about defining interactions
in Altair and how to declare selection-type parameters, seeInteractive Chartsin Altair's documentation.

selection_mode(str or Iterable of str)

The selection parameters Streamlit should use. Ifselection_modeisNone(default), Streamlit will use all
selection parameters defined in the chart's Altair spec.

When Streamlit uses a selection parameter, selections from that
parameter will trigger a rerun and be included in the selection
state. When Streamlit does not use a selection parameter,
selections from that parameter will not trigger a rerun and not be
included in the selection state.

Selection parameters are identified by theirnameproperty.

(element or dict)

Ifon_selectis"ignore"(default), this command returns an
internal placeholder for the chart element that can be used with
the.add_rows()method. Otherwise, this command returns a
dictionary-like object that supports both key and attribute
notation. The attributes are described by theVegaLiteStatedictionary schema.

#### Example

```python

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

c = (
   alt.Chart(chart_data)
   .mark_circle()
   .encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])
)

st.altair_chart(c)

```

## Chart selections

### VegaLiteState

The schema for the Vega-Lite event state.

The event state is stored in a dictionary-like object that supports both
key and attribute notation. Event states cannot be programmatically
changed or set through Session State.

Only selection events are supported at this time.

selection(dict)

The state of theon_selectevent. This attribute returns a
dictionary-like object that supports both key and attribute notation.
The name of each Vega-Lite selection parameter becomes an attribute in
theselectiondictionary. The format of the data within each
attribute is determined by the selection parameter definition within
Vega-Lite.

#### Examples

The following two examples have equivalent definitions. Each one has a
point and interval selection parameter include in the chart definition.
The point selection parameter is named"point_selection". The interval
or box selection parameter is named"interval_selection".

The follow example usesst.altair_chart:

```python

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        np.random.randn(20, 3), columns=["a", "b", "c"]
    )
df = st.session_state.data

point_selector = alt.selection_point("point_selection")
interval_selector = alt.selection_interval("interval_selection")
chart = (
    alt.Chart(df)
    .mark_circle()
    .encode(
        x="a",
        y="b",
        size="c",
        color="c",
        tooltip=["a", "b", "c"],
        fillOpacity=alt.condition(point_selector, alt.value(1), alt.value(0.3)),
    )
    .add_params(point_selector, interval_selector)
)

event = st.altair_chart(chart, key="alt_chart", on_select="rerun")

event

```

The following example usesst.vega_lite_chart:

```python

import streamlit as st
import pandas as pd
import numpy as np

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        np.random.randn(20, 3), columns=["a", "b", "c"]
    )

spec = {
    "mark": {"type": "circle", "tooltip": True},
    "params": [
        {"name": "interval_selection", "select": "interval"},
        {"name": "point_selection", "select": "point"},
    ],
    "encoding": {
        "x": {"field": "a", "type": "quantitative"},
        "y": {"field": "b", "type": "quantitative"},
        "size": {"field": "c", "type": "quantitative"},
        "color": {"field": "c", "type": "quantitative"},
        "fillOpacity": {
            "condition": {"param": "point_selection", "value": 1},
            "value": 0.3,
        },
    },
}

event = st.vega_lite_chart(
    st.session_state.data, spec, key="vega_chart", on_select="rerun"
)

event

```

Try selecting points in this interactive example. When you click a point,
the selection will appear under the attribute,"point_selection", which
is the name given to the point selection parameter. Similarly, when you
make an interval selection, it will appear under the attribute"interval_selection". You can give your selection parameters other
names if desired.

If you holdShiftwhile selecting points, existing point selections
will be preserved. Interval selections are not preserved when making
additional selections.

## element.add_rows

Concatenate a dataframe to the bottom of the current one.

element.add_rows(data=None, **kwargs)

data(pandas.DataFrame, pandas.Styler, pyarrow.Table, numpy.ndarray, pyspark.sql.DataFrame, snowflake.snowpark.dataframe.DataFrame, Iterable, dict, or None)

Table to concat. Optional.

**kwargs(pandas.DataFrame, numpy.ndarray, Iterable, dict, or None)

The named dataset to concat. Optional. You can only pass in 1
dataset (including the one in the data parameter).

#### Example

```python

import streamlit as st
import pandas as pd
import numpy as np

df1 = pd.DataFrame(
    np.random.randn(50, 20), columns=("col %d" % i for i in range(20))
)

my_table = st.table(df1)

df2 = pd.DataFrame(
    np.random.randn(50, 20), columns=("col %d" % i for i in range(20))
)

my_table.add_rows(df2)
# Now the table shown in the Streamlit app contains the data for
# df1 followed by the data for df2.

```

You can do the same thing with plots. For example, if you want to add
more data to a line chart:

```python

# Assuming df1 and df2 from the example above still exist...
my_chart = st.line_chart(df1)
my_chart.add_rows(df2)
# Now the chart shown in the Streamlit app contains the data for
# df1 followed by the data for df2.

```

And for plots whose datasets are named, you can pass the data with a
keyword argument where the key is the name:

```python

my_chart = st.vega_lite_chart(
    {
        "mark": "line",
        "encoding": {"x": "a", "y": "b"},
        "datasets": {
            "some_fancy_name": df1,  # <-- named dataset
        },
        "data": {"name": "some_fancy_name"},
    }
)
my_chart.add_rows(some_fancy_name=df2)  # <-- name used as keyword

```

## Theming

Altair charts are displayed using the Streamlit theme by default. This theme is sleek, user-friendly, and incorporates Streamlit's color palette. The added benefit is that your charts better integrate with the rest of your app's design.

The Streamlit theme is available from Streamlit 1.16.0 through thetheme="streamlit"keyword argument. To disable it, and use Altair's native theme, usetheme=Noneinstead.

`theme="streamlit"`

`theme=None`

Let's look at an example of charts with the Streamlit theme and the native Altair theme:

`import altair as alt
from vega_datasets import data

source = data.cars()

chart = alt.Chart(source).mark_circle().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
).interactive()

tab1, tab2 = st.tabs(["Streamlit theme (default)", "Altair native theme"])

with tab1:
    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.altair_chart(chart, theme="streamlit", use_container_width=True)
with tab2:
    # Use the native Altair theme.
    st.altair_chart(chart, theme=None, use_container_width=True)`

Click the tabs in the interactive app below to see the charts with the Streamlit theme enabled and disabled.

If you're wondering if your own customizations will still be taken into account, don't worry! You can still make changes to your chart configurations. In other words, although we now enable the Streamlit theme by default, you can overwrite it with custom colors or fonts. For example, if you want a chart line to be green instead of the default red, you can do it!

Here's an example of an Altair chart where manual color passing is done and reflected:

`import altair as alt
import streamlit as st
from vega_datasets import data

source = data.seattle_weather()

scale = alt.Scale(
    domain=["sun", "fog", "drizzle", "rain", "snow"],
    range=["#e7ba52", "#a7a7a7", "#aec7e8", "#1f77b4", "#9467bd"],
)
color = alt.Color("weather:N", scale=scale)

# We create two selections:
# - a brush that is active on the top panel
# - a multi-click that is active on the bottom panel
brush = alt.selection_interval(encodings=["x"])
click = alt.selection_multi(encodings=["color"])

# Top panel is scatter plot of temperature vs time
points = (
    alt.Chart()
    .mark_point()
    .encode(
        alt.X("monthdate(date):T", title="Date"),
        alt.Y(
            "temp_max:Q",
            title="Maximum Daily Temperature (C)",
            scale=alt.Scale(domain=[-5, 40]),
        ),
        color=alt.condition(brush, color, alt.value("lightgray")),
        size=alt.Size("precipitation:Q", scale=alt.Scale(range=[5, 200])),
    )
    .properties(width=550, height=300)
    .add_selection(brush)
    .transform_filter(click)
)

# Bottom panel is a bar chart of weather type
bars = (
    alt.Chart()
    .mark_bar()
    .encode(
        x="count()",
        y="weather:N",
        color=alt.condition(click, color, alt.value("lightgray")),
    )
    .transform_filter(brush)
    .properties(
        width=550,
    )
    .add_selection(click)
)

chart = alt.vconcat(points, bars, data=source, title="Seattle Weather: 2012-2015")

tab1, tab2 = st.tabs(["Streamlit theme (default)", "Altair native theme"])

with tab1:
    st.altair_chart(chart, theme="streamlit", use_container_width=True)
with tab2:
    st.altair_chart(chart, theme=None, use_container_width=True)`

Notice how the custom colors are still reflected in the chart, even when the Streamlit theme is enabled 👇

For many more examples of Altair charts with and without the Streamlit theme, check out thealtair.streamlit.app.

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
