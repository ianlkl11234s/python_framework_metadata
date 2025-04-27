---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/data/st.column_config/st.column_config.selectboxcolumn
date: 2025-04-27 12:49:16
---

## st.column_config.SelectboxColumn

Configure a selectbox column inst.dataframeorst.data_editor.

This is the default column type for Pandas categorical values. This command needs to
be used in thecolumn_configparameter ofst.dataframeorst.data_editor.
When used withst.data_editor, editing will be enabled with a selectbox widget.

st.column_config.SelectboxColumn(label=None, *, width=None, help=None, disabled=None, required=None, pinned=None, default=None, options=None)

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

disabled(bool or None)

Whether editing should be disabled for this column. If this isNone(default), Streamlit will decide: indices are disabled and data columns
are not.

If a column has mixed types, it may become uneditable regardless ofdisabled.

required(bool or None)

Whether edited cells in the column need to have a value. If this isFalse(default), the user can submit empty values for this column.
If this isTrue, an edited cell in this column can only be
submitted if its value is notNone, and a new row will only be
submitted after the user fills in this column.

pinned(bool or None)

Whether the column is pinned. A pinned column will stay visible on the
left side no matter where the user scrolls. If this isNone(default), Streamlit will decide: index columns are pinned, and data
columns are not pinned.

default(str, int, float, bool, or None)

Specifies the default value in this column when a new row is added by
the user. This defaults toNone.

options(Iterable of str or None)

The options that can be selected during editing. If this isNone(default), the options will be inferred from the underlying dataframe
column if its dtype is "category". For more information, seePandas docs).

#### Examples

```python

import pandas as pd
import streamlit as st

data_df = pd.DataFrame(
    {
        "category": [
            "📊 Data Exploration",
            "📈 Data Visualization",
            "🤖 LLM",
            "📊 Data Exploration",
        ],
    }
)

st.data_editor(
    data_df,
    column_config={
        "category": st.column_config.SelectboxColumn(
            "App Category",
            help="The category of the app",
            width="medium",
            options=[
                "📊 Data Exploration",
                "📈 Data Visualization",
                "🤖 LLM",
            ],
            required=True,
        )
    },
    hide_index=True,
)

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
