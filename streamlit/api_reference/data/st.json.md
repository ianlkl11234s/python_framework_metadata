---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/data/st.json
date: 2025-04-27 12:49:12
---

## st.json

Display an object or string as a pretty-printed, interactive JSON string.

st.json(body, *, expanded=True)

body(object or str)

The object to print as JSON. All referenced objects should be
serializable to JSON as well. If object is a string, we assume it
contains serialized JSON.

expanded(bool or int)

The initial expansion state of the JSON element. This can be one
of the following:

- True(default): The element is fully expanded.
- False: The element is fully collapsed.
- An integer: The element is expanded to the depth specified. The
integer must be non-negative.expanded=0is equivalent toexpanded=False.
Regardless of the initial expansion state, users can collapse or
expand any key-value pair to show or hide any part of the object.

#### Example

```python

import streamlit as st

st.json(
    {
        "foo": "bar",
        "stuff": [
            "stuff 1",
            "stuff 2",
            "stuff 3",
        ],
        "level1": {"level2": {"level3": {"a": "b"}}},
    },
    expanded=2,
)

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
