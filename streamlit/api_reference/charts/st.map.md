---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/charts/st.map
date: 2025-04-27 12:49:35
---

## st.map

Display a map with a scatterplot overlaid onto it.

This is a wrapper aroundst.pydeck_chartto quickly create
scatterplot charts on top of a map, with auto-centering and auto-zoom.

When using this command, Mapbox provides the map tiles to render map
content. Note that Mapbox is a third-party product and Streamlit accepts
no responsibility or liability of any kind for Mapbox or for any content
or information made available by Mapbox.

Mapbox requires users to register and provide a token before users can
request map tiles. Currently, Streamlit provides this token for you, but
this could change at any time. We strongly recommend all users create and
use their own personal Mapbox token to avoid any disruptions to their
experience. You can do this with themapbox.tokenconfig option. The
use of Mapbox is governed by Mapbox's Terms of Use.

To get a token for yourself, create an account athttps://mapbox.com.
For more info on how to set config options, seehttps://docs.streamlit.io/develop/api-reference/configuration/config.toml.

st.map(data=None, *, latitude=None, longitude=None, color=None, size=None, zoom=None, use_container_width=True, width=None, height=None)

data(Anything supported by st.dataframe)

The data to be plotted.

latitude(str or None)

The name of the column containing the latitude coordinates of
the datapoints in the chart.

If None, the latitude data will come from any column named 'lat',
'latitude', 'LAT', or 'LATITUDE'.

longitude(str or None)

The name of the column containing the longitude coordinates of
the datapoints in the chart.

If None, the longitude data will come from any column named 'lon',
'longitude', 'LON', or 'LONGITUDE'.

color(str or tuple or None)

The color of the circles representing each datapoint.

Can be:

- None, to use the default color.
- A hex string like "#ffaa00" or "#ffaa0088".
- An RGB or RGBA tuple with the red, green, blue, and alpha
components specified as ints from 0 to 255 or floats from 0.0 to
1.0.
- The name of the column to use for the color. Cells in this column
should contain colors represented as a hex string or color tuple,
as described above.
size(str or float or None)

The size of the circles representing each point, in meters.

This can be:

- None, to use the default size.
- A number like 100, to specify a single size to use for all
datapoints.
- The name of the column to use for the size. This allows each
datapoint to be represented by a circle of a different size.
zoom(int)

Zoom level as specified inhttps://wiki.openstreetmap.org/wiki/Zoom_levels.

use_container_width(bool)

Whether to override the map's native width with the width of
the parent container. Ifuse_container_widthisTrue(default), Streamlit sets the width of the map to match the width
of the parent container. Ifuse_container_widthisFalse,
Streamlit sets the width of the chart to fit its contents according
to the plotting library, up to the width of the parent container.

width(int or None)

Desired width of the chart expressed in pixels. IfwidthisNone(default), Streamlit sets the width of the chart to fit
its contents according to the plotting library, up to the width of
the parent container. Ifwidthis greater than the width of the
parent container, Streamlit sets the chart width to match the width
of the parent container.

To usewidth, you must setuse_container_width=False.

height(int or None)

Desired height of the chart expressed in pixels. IfheightisNone(default), Streamlit sets the height of the chart to fit
its contents according to the plotting library.

#### Examples

```python

import streamlit as st
import pandas as pd
import numpy as np

df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=["lat", "lon"],
)
st.map(df)

```

You can also customize the size and color of the datapoints:

```python

st.map(df, size=20, color="#0044ff")

```

And finally, you can choose different columns to use for the latitude
and longitude components, as well as set size and color of each
datapoint dynamically based on other columns:

```python

import streamlit as st
import pandas as pd
import numpy as np

df = pd.DataFrame(
    {
        "col1": np.random.randn(1000) / 50 + 37.76,
        "col2": np.random.randn(1000) / 50 + -122.4,
        "col3": np.random.randn(1000) * 100,
        "col4": np.random.rand(1000, 4).tolist(),
    }
)

st.map(df, latitude="col1", longitude="col2", size="col3", color="col4")

```

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

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
