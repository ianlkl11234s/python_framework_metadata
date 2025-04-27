---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/data/st.column_config/st.column_config.linechartcolumn
date: 2025-04-27 12:49:21
---

## st.column_config.LineChartColumn

Configure a line chart column inst.dataframeorst.data_editor.

Cells need to contain a list of numbers. Chart columns are not editable
at the moment. This command needs to be used in thecolumn_configparameter
ofst.dataframeorst.data_editor.

st.column_config.LineChartColumn(label=None, *, width=None, help=None, pinned=None, y_min=None, y_max=None)

label(str or None)

The label shown at the top of the column. If this isNone(default), the column name is used.

width("small", "medium", "large", or None)

The display width of the column. If this isNone(default), the
column will be sized to fit the cell contents. Otherwise, this can be
one of the following:

- "small": 75px wide
- "medium": 200px wide
- "large": 400px wide
help(str or None)

A tooltip that gets displayed when hovering over the column label. If
this isNone(default), no tooltip is displayed.

The tooltip can optionally contain GitHub-flavored Markdown, including
the Markdown directives described in thebodyparameter ofst.markdown.

pinned(bool or None)

Whether the column is pinned. A pinned column will stay visible on the
left side no matter where the user scrolls. If this isNone(default), Streamlit will decide: index columns are pinned, and data
columns are not pinned.

y_min(int, float, or None)

The minimum value on the y-axis for all cells in the column. If this isNone(default), every cell will use the minimum of its data.

y_max(int, float, or None)

The maximum value on the y-axis for all cells in the column. If this isNone(default), every cell will use the maximum of its data.

#### Examples

```python

import pandas as pd
import streamlit as st

data_df = pd.DataFrame(
    {
        "sales": [
            [0, 4, 26, 80, 100, 40],
            [80, 20, 80, 35, 40, 100],
            [10, 20, 80, 80, 70, 0],
            [10, 100, 20, 100, 30, 100],
        ],
    }
)

st.data_editor(
    data_df,
    column_config={
        "sales": st.column_config.LineChartColumn(
            "Sales (last 6 months)",
            width="medium",
            help="The sales volume in the last 6 months",
            y_min=0,
            y_max=100,
         ),
    },
    hide_index=True,
)

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
