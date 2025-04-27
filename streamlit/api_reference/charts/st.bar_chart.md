---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/charts/st.bar_chart
date: 2025-04-27 12:49:30
---

## st.bar_chart

Display a bar chart.

This is syntax-sugar aroundst.altair_chart. The main difference
is this command uses the data's own column and indices to figure out
the chart's Altair spec. As a result this is easier to use for many
"just plot this" scenarios, while being less customizable.

Ifst.bar_chartdoes not guess the data specification
correctly, try specifying your desired chart usingst.altair_chart.

st.bar_chart(data=None, *, x=None, y=None, x_label=None, y_label=None, color=None, horizontal=False, stack=None, width=None, height=None, use_container_width=True)

data(Anything supported by st.dataframe)

Data to be plotted.

x(str or None)

Column name or key associated to the x-axis data. IfxisNone(default), Streamlit uses the data index for the x-axis
values.

y(str, Sequence of str, or None)

Column name(s) or key(s) associated to the y-axis data. If this isNone(default), Streamlit draws the data of all remaining
columns as data series. If this is aSequenceof strings,
Streamlit draws several series on the same chart by melting your
wide-format table into a long-format table behind the scenes.

x_label(str or None)

The label for the x-axis. If this isNone(default), Streamlit
will use the column name specified inxif available, or else
no label will be displayed.

y_label(str or None)

The label for the y-axis. If this isNone(default), Streamlit
will use the column name(s) specified inyif available, or
else no label will be displayed.

color(str, tuple, Sequence of str, Sequence of tuple, or None)

The color to use for different series in this chart.

For a bar chart with just one series, this can be:

- None, to use the default color.
- A hex string like "#ffaa00" or "#ffaa0088".
- An RGB or RGBA tuple with the red, green, blue, and alpha
components specified as ints from 0 to 255 or floats from 0.0 to
1.0.
For a bar chart with multiple series, where the dataframe is in
long format (that is, y is None or just one column), this can be:

- None, to use the default colors.
- The name of a column in the dataset. Data points will be grouped
into series of the same color based on the value of this column.
In addition, if the values in this column match one of the color
formats above (hex string or color tuple), then that color will
be used.For example: if the dataset has 1000 rows, but this column only
contains the values "adult", "child", and "baby", then those 1000
datapoints will be grouped into three series whose colors will be
automatically selected from the default palette.But, if for the same 1000-row dataset, this column contained
the values "#ffaa00", "#f0f", "#0000ff", then then those 1000
datapoints would still be grouped into 3 series, but their
colors would be "#ffaa00", "#f0f", "#0000ff" this time around.
None, to use the default colors.

The name of a column in the dataset. Data points will be grouped
into series of the same color based on the value of this column.
In addition, if the values in this column match one of the color
formats above (hex string or color tuple), then that color will
be used.

For example: if the dataset has 1000 rows, but this column only
contains the values "adult", "child", and "baby", then those 1000
datapoints will be grouped into three series whose colors will be
automatically selected from the default palette.

But, if for the same 1000-row dataset, this column contained
the values "#ffaa00", "#f0f", "#0000ff", then then those 1000
datapoints would still be grouped into 3 series, but their
colors would be "#ffaa00", "#f0f", "#0000ff" this time around.

For a bar chart with multiple series, where the dataframe is in
wide format (that is, y is a Sequence of columns), this can be:

- None, to use the default colors.
- A list of string colors or color tuples to be used for each of
the series in the chart. This list should have the same length
as the number of y values (e.g.color=["#fd0","#f0f", "#04f"]for three lines).
horizontal(bool)

Whether to make the bars horizontal. If this isFalse(default), the bars display vertically. If this isTrue,
Streamlit swaps the x-axis and y-axis and the bars display
horizontally.

stack(bool, "normalize", "center", "layered", or None)

Whether to stack the bars. If this isNone(default),
Streamlit uses Vega's default. Other values can be as follows:

- True: The bars form a non-overlapping, additive stack within
the chart.
- False: The bars display side by side.
- "layered": The bars overlap each other without stacking.
- "normalize": The bars are stacked and the total height is
normalized to 100% of the height of the chart.
- "center": The bars are stacked and shifted to center the
total height around an axis.
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

use_container_width(bool)

Whether to overridewidthwith the width of the parent
container. Ifuse_container_widthisTrue(default),
Streamlit sets the width of the chart to match the width of the
parent container. Ifuse_container_widthisFalse,
Streamlit sets the chart's width according towidth.

#### Examples

```python

import streamlit as st
import pandas as pd
import numpy as np

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.bar_chart(chart_data)

```

You can also choose different columns to use for x and y, as well as set
the color dynamically based on a 3rd column (assuming your dataframe is in
long format):

```python

import streamlit as st
import pandas as pd
import numpy as np

chart_data = pd.DataFrame(
    {
        "col1": list(range(20)) * 3,
        "col2": np.random.randn(60),
        "col3": ["A"] * 20 + ["B"] * 20 + ["C"] * 20,
    }
)

st.bar_chart(chart_data, x="col1", y="col2", color="col3")

```

If your dataframe is in wide format, you can group multiple
columns under the y argument to show multiple series with different
colors:

```python

import streamlit as st
import pandas as pd
import numpy as np

chart_data = pd.DataFrame(
    {
        "col1": list(range(20)),
        "col2": np.random.randn(20),
        "col3": np.random.randn(20),
    }
)

st.bar_chart(
    chart_data,
    x="col1",
    y=["col2", "col3"],
    color=["#FF0000", "#0000FF"],  # Optional
)

```

You can rotate your bar charts to display horizontally.

```python

import streamlit as st
from vega_datasets import data

source = data.barley()

st.bar_chart(source, x="variety", y="yield", color="site", horizontal=True)

```

You can unstack your bar charts.

```python

import streamlit as st
from vega_datasets import data

source = data.barley()

st.bar_chart(source, x="year", y="yield", color="site", stack=False)

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
