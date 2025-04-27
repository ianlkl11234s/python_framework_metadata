---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/write-magic/st.write_stream
date: 2025-04-27 12:48:49
---

## st.write_stream

Stream a generator, iterable, or stream-like sequence to the app.

st.write_streamiterates through the given sequences and writes all
chunks to the app. String chunks will be written using a typewriter effect.
Other data types will be written usingst.write.

st.write_stream(stream)

stream(Callable, Generator, Iterable, OpenAI Stream, or LangChain Stream)

The generator or iterable to stream.

If you pass an async generator, Streamlit will internally convert
it to a sync generator.

Note

To use additional LLM libraries, you can create a wrapper to
manually define a generator function and include custom output
parsing.

(str or list)

The full response. If the streamed output only contains text, this
is a string. Otherwise, this is a list of all the streamed objects.
The return value is fully compatible as input forst.write.

#### Example

You can pass an OpenAI stream as shown in our tutorial,Build a         basic LLM chat app. Alternatively,
you can pass a generic generator function as input:

```python

import time
import numpy as np
import pandas as pd
import streamlit as st

_LOREM_IPSUM = """
Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
"""


def stream_data():
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)

    yield pd.DataFrame(
        np.random.randn(5, 10),
        columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    )

    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)


if st.button("Stream data"):
    st.write_stream(stream_data)

```

#### Tip

If your stream object is not compatible withst.write_stream, define a wrapper around your stream object to create a compatible generator function.

`st.write_stream`

`for chunk in unsupported_stream:
    yield preprocess(chunk)`

For an example, see how we useReplicatewithSnowflake Arcticinthis code.

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
