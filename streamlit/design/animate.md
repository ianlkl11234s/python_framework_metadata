---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/concepts/design/animate
date: 2025-04-27 12:48:14
---

# Animate and update elements

Sometimes you display a chart or dataframe and want to modify it live as the app
runs (for example, in a loop). Some elements have built-in methods to allow you
to update them in-place without rerunning the app.

Updatable elements include the following:

- st.emptycontainers can be written to in sequence and will always show the last thing written. They can also be cleared with an
additional.empty()called like a method.
- st.dataframe,st.table, and many chart elements can be updated with the.add_rows()method which appends data.
- st.progresselements can be updated with additional.progress()calls. They can also be cleared with a.empty()method call.
- st.statuscontainers have an.update()method to change their labels, expanded state, and status.
- st.toastmessages can be updated in place with additional.toast()calls.
`st.empty`

`.empty()`

`st.dataframe`

`st.table`

`.add_rows()`

`st.progress`

`.progress()`

`.empty()`

`st.status`

`.update()`

`st.toast`

`.toast()`

## st.emptycontainers

`st.empty`

st.emptycan hold a single element. When you write any element to anst.emptycontainer, Streamlit discards its previous content
displays the new element. You can alsost.emptycontainers by calling.empty()as a method. If you want to update a set of elements, use
a plain container (st.container()) insidest.emptyand write contents to the plain container. Rewrite the plain container and its
contents as often as desired to update your app's display.

`st.empty`

`st.empty`

`st.empty`

`.empty()`

`st.container()`

`st.empty`

## The.add_rows()method

`.add_rows()`

st.dataframe,st.table, and all chart functions can be mutated using the.add_rows()method on their output. In the following example, we usemy_data_element = st.line_chart(df). You can try the example withst.table,st.dataframe, and most of the other simple charts by just swapping outst.line_chart. Note thatst.dataframeonly shows the first ten rows by default and enables scrolling for additional rows. This means adding rows is not as visually apparent as it is withst.tableor the chart elements.

`st.dataframe`

`st.table`

`.add_rows()`

`my_data_element = st.line_chart(df)`

`st.table`

`st.dataframe`

`st.line_chart`

`st.dataframe`

`st.table`

`import streamlit as st
import pandas as pd
import numpy as np
import time

df = pd.DataFrame(np.random.randn(15, 3), columns=(["A", "B", "C"]))
my_data_element = st.line_chart(df)

for tick in range(10):
    time.sleep(.5)
    add_df = pd.DataFrame(np.random.randn(1, 3), columns=(["A", "B", "C"]))
    my_data_element.add_rows(add_df)

st.button("Regenerate")`

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
