---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/text/st.code
date: 2025-04-27 12:48:56
---

## st.code

Display a code block with optional syntax highlighting.

st.code(body, language="python", *, line_numbers=False, wrap_lines=False, height=None)

body(str)

The string to display as code or monospace text.

language(str or None)

The language that the code is written in, for syntax highlighting.
This defaults to"python". If this isNone, the code will
be plain, monospace text.

For a list of availablelanguagevalues, seereact-syntax-highlighteron GitHub.

line_numbers(bool)

An optional boolean indicating whether to show line numbers to the
left of the code block. This defaults toFalse.

wrap_lines(bool)

An optional boolean indicating whether to wrap lines. This defaults
toFalse.

height(int or None)

Desired height of the code block expressed in pixels. IfheightisNone(default), Streamlit sets the element's height to fit
its content. Vertical scrolling within the element is enabled when
the height does not accomodate all lines.

#### Examples

```python

import streamlit as st

code = '''def hello():
    print("Hello, Streamlit!")'''
st.code(code, language="python")

```

```python

import streamlit as st
code = '''Is it a crown or boat?
                        ii
                      iiiiii
WWw                 .iiiiiiii.                ...:
 WWWWWWw          .iiiiiiiiiiii.         ........
  WWWWWWWWWWw    iiiiiiiiiiiiiiii    ...........
   WWWWWWWWWWWWWWwiiiiiiiiiiiiiiiii............
    WWWWWWWWWWWWWWWWWWwiiiiiiiiiiiiii.........
     WWWWWWWWWWWWWWWWWWWWWWwiiiiiiiiii.......
      WWWWWWWWWWWWWWWWWWWWWWWWWWwiiiiiii....
       WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWwiiii.
          -MMMWWWWWWWWWWWWWWWWWWWWWWMMM-
'''
st.code(code, language=None)

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
