---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/charts/st.graphviz_chart
date: 2025-04-27 12:49:46
---

## st.graphviz_chart

Display a graph using the dagre-d3 library.

st.graphviz_chart(figure_or_dot, use_container_width=False)

figure_or_dot(graphviz.dot.Graph, graphviz.dot.Digraph, graphviz.sources.Source, str)

The Graphlib graph object or dot string to display

use_container_width(bool)

Whether to override the figure's native width with the width of
the parent container. Ifuse_container_widthisFalse(default), Streamlit sets the width of the chart to fit its contents
according to the plotting library, up to the width of the parent
container. Ifuse_container_widthisTrue, Streamlit sets
the width of the figure to match the width of the parent container.

#### Example

```python

import streamlit as st
import graphviz

# Create a graphlib graph object
graph = graphviz.Digraph()
graph.edge("run", "intr")
graph.edge("intr", "runbl")
graph.edge("runbl", "run")
graph.edge("run", "kernel")
graph.edge("kernel", "zombie")
graph.edge("kernel", "sleep")
graph.edge("kernel", "runmem")
graph.edge("sleep", "swap")
graph.edge("swap", "runswap")
graph.edge("runswap", "new")
graph.edge("runswap", "runmem")
graph.edge("new", "runmem")
graph.edge("sleep", "runmem")

st.graphviz_chart(graph)

```

Or you can render the chart from the graph using GraphViz's Dot
language:

```python

st.graphviz_chart('''
    digraph {
        run -> intr
        intr -> runbl
        runbl -> run
        run -> kernel
        kernel -> zombie
        kernel -> sleep
        kernel -> runmem
        sleep -> swap
        swap -> runswap
        runswap -> new
        runswap -> runmem
        new -> runmem
        sleep -> runmem
    }
''')

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
