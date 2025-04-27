---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/data/st.column_config/st.column_config.progresscolumn
date: 2025-04-27 12:49:25
---

## st.column_config.ProgressColumn

Configure a progress column inst.dataframeorst.data_editor.

Cells need to contain a number. Progress columns are not editable at the moment.
This command needs to be used in thecolumn_configparameter ofst.dataframeorst.data_editor.

st.column_config.ProgressColumn(label=None, *, width=None, help=None, pinned=None, format=None, min_value=None, max_value=None)

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

format(str, "plain", "localized", "percent", "dollar", "euro", "accounting", "compact", "scientific", "engineering", or None)

A format string controlling how the numbers are displayed.
This can be one of the following values:

- None(default): Streamlit infers the formatting from the data.
- "plain": Show the full number without any formatting (e.g. "1234.567").
- "localized": Show the number in the default locale format (e.g. "1,234.567").
- "percent": Show the number as a percentage (e.g. "123456.70%").
- "dollar": Show the number as a dollar amount (e.g. "$1,234.57").
- "euro": Show the number as a euro amount (e.g. "€1,234.57").
- "accounting": Show the number in an accounting format (e.g. "1,234.00").
- "compact": Show the number in a compact format (e.g. "1.2K").
- "scientific": Show the number in scientific notation (e.g. "1.235E3").
- "engineering": Show the number in engineering notation (e.g. "1.235E3").
- printf-style format string: Format the number with a printf
specifier, like"%d"to show a signed integer (e.g. "1234") or"%X"to show an unsigned hexidecimal integer (e.g. "4D2"). You
can also add prefixes and suffixes. To show British pounds, use"£ %.2f"(e.g. "£ 1234.57"). For more information, seesprint-js.
Number formatting fromcolumn_configalways takes precedence over
number formatting frompandas.Styler. The number formatting does
not impact the return value when used inst.data_editor.

pinned(bool or None)

Whether the column is pinned. A pinned column will stay visible on the
left side no matter where the user scrolls. If this isNone(default), Streamlit will decide: index columns are pinned, and data
columns are not pinned.

min_value(int, float, or None)

The minimum value of the progress bar. If this isNone(default),
the minimum will be 0.

max_value(int, float, or None)

The maximum value of the progress bar. If this isNone(default),
the maximum will be 100 for integer values and 1.0 for float values.

#### Examples

```python

import pandas as pd
import streamlit as st

data_df = pd.DataFrame(
    {
        "sales": [200, 550, 1000, 80],
    }
)

st.data_editor(
    data_df,
    column_config={
        "sales": st.column_config.ProgressColumn(
            "Sales volume",
            help="The sales volume in USD",
            format="$%f",
            min_value=0,
            max_value=1000,
        ),
    },
    hide_index=True,
)

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
