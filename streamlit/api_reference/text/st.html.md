---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/text/st.html
date: 2025-04-27 12:49:01
---

## st.html

Insert HTML into your app.

Adding custom HTML to your app impacts safety, styling, and
maintainability. We sanitize HTML withDOMPurify, but inserting HTML remains a
developer risk. Passing untrusted code tost.htmlor dynamically
loading external code can increase the risk of vulnerabilities in your
app.

st.htmlcontent isnotiframed. Executing JavaScript is not
supported at this time.

st.html(body)

body(any)

The HTML code to insert. This can be one of the following:

- A string of HTML code.
- A path to a local file with HTML code. The path can be astrorPathobject. Paths can be absolute or relative to the
working directory (where you executestreamlit run).
- Any object. Ifbodyis not a string or path, Streamlit will
convert the object to a string.body._repr_html_()takes
precedence overstr(body)when available.
#### Example

```python

import streamlit as st

st.html(
    "<p><span style='text-decoration: line-through double red;'>Oops</span>!</p>"
)

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
