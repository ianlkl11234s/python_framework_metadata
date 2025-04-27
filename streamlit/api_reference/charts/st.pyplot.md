---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/charts/st.pyplot
date: 2025-04-27 12:49:52
---

## st.pyplot

Display a matplotlib.pyplot figure.

Important

You must installmatplotlibto use this command.

st.pyplot(fig=None, clear_figure=None, use_container_width=True, **kwargs)

fig(Matplotlib Figure)

The MatplotlibFigureobject to render. Seehttps://matplotlib.org/stable/gallery/index.htmlfor examples.

Note

When this argument isn't specified, this function will render the global
Matplotlib figure object. However, this feature is deprecated and
will be removed in a later version.

clear_figure(bool)

If True, the figure will be cleared after being rendered.
If False, the figure will not be cleared after being rendered.
If left unspecified, we pick a default based on the value offig.

- Iffigis set, defaults toFalse.
- Iffigis not set, defaults toTrue. This simulates Jupyter's
approach to matplotlib rendering.
use_container_width(bool)

Whether to override the figure's native width with the width of
the parent container. Ifuse_container_widthisTrue(default), Streamlit sets the width of the figure to match the
width of the parent container. Ifuse_container_widthisFalse, Streamlit sets the width of the chart to fit its
contents according to the plotting library, up to the width of the
parent container.

**kwargs(any)

Arguments to pass to Matplotlib's savefig function.

#### Example

```python

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.pyplot(fig)

```

Matplotlib supports several types of "backends". If you're getting an
error using Matplotlib with Streamlit, try setting your backend to "TkAgg":

```python

echo "backend: TkAgg" >> ~/.matplotlib/matplotlibrc

```

For more information, seehttps://matplotlib.org/faq/usage_faq.html.

#### Warning

Matplotlibdoesn't work well with threads. So if you're using Matplotlib you should wrap your code with locks. This Matplotlib bug is more prominent when you deploy and share your apps because you're more likely to get concurrent users then. The following example usesRlockfrom thethreadingmodule.

`Rlock`

`threading`

`import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from threading import RLock

_lock = RLock()

x = np.random.normal(1, 1, 100)
y = np.random.normal(1, 1, 100)

with _lock:
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    st.pyplot(fig)`

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
