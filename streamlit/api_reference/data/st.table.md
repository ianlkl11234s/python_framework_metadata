---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/data/st.table
date: 2025-04-27 12:49:08
---

## st.table

Display a static table.

Whilest.dataframeis geared towards large datasets and interactive
data exploration,st.tableis useful for displaying small, styled
tables without sorting or scrolling. For example,st.tablemay be
the preferred way to display a confusion matrix or leaderboard.
Additionally,st.tablesupports Markdown.

st.table(data=None)

data(Anything supported by st.dataframe)

The table data.

All cells including the index and column headers can optionally
contain GitHub-flavored Markdown. Syntax information can be found
at:https://github.github.com/gfm.

See thebodyparameter ofst.markdownfor additional,
supported Markdown directives.

#### Examples

Example 1: Display a simple dataframe as a static table

```python

import streamlit as st
import pandas as pd
import numpy as np

df = pd.DataFrame(
    np.random.randn(10, 5), columns=("col %d" % i for i in range(5))
)

st.table(df)

```

Example 2: Display a table of Markdown strings

```python

import streamlit as st
import pandas as pd

df = pd.DataFrame(
    {
        "Command": ["**st.table**", "*st.dataframe*"],
        "Type": ["`static`", "`interactive`"],
        "Docs": [
            "[:rainbow[docs]](https://docs.streamlit.io/develop/api-reference/data/st.dataframe)",
            "[:book:](https://docs.streamlit.io/develop/api-reference/data/st.table)",
        ],
    }
)
st.table(df)

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
