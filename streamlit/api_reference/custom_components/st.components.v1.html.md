---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/custom-components/st.components.v1.html
date: 2025-04-27 12:50:52
---

## st.components.v1.html

Display an HTML string in an iframe.

To use this function, import it from thestreamlit.components.v1module.

If you want to insert HTML text into your app without an iframe, tryst.htmlinstead.

Warning

Usingst.components.v1.htmldirectly (instead of importing
its module) is deprecated and will be disallowed in a later version.

st.components.v1.html(html, width=None, height=None, scrolling=False)

html(str)

The HTML string to embed in the iframe.

width(int)

The width of the iframe in CSS pixels. By default, this is the
app's default element width.

height(int)

The height of the frame in CSS pixels. By default, this is150.

scrolling(bool)

Whether to allow scrolling in the iframe. If thisFalse(default), Streamlit crops any content larger than the iframe and
does not show a scrollbar. If this isTrue, Streamlit shows a
scrollbar when the content is larger than the iframe.

#### Example

```python

import streamlit.components.v1 as components

components.html(
    "<p><span style='text-decoration: line-through double red;'>Oops</span>!</p>"
)

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
