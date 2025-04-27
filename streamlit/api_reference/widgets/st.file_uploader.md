---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader
date: 2025-04-27 12:50:16
---

## st.file_uploader

Display a file uploader widget.

By default, uploaded files are limited to 200 MB each. You can
configure this using theserver.maxUploadSizeconfig option. For
more information on how to set config options, seeconfig.toml.

st.file_uploader(label, type=None, accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False, label_visibility="visible")

label(str)

A short label explaining to the user what this file uploader is for.
The label can optionally contain GitHub-flavored Markdown of the
following types: Bold, Italics, Strikethroughs, Inline Code, Links,
and Images. Images display like icons, with a max height equal to
the font height.

Unsupported Markdown elements are unwrapped so only their children
(text contents) render. Display unsupported elements as literal
characters by backslash-escaping them. E.g.,"1\. Not an ordered list".

See thebodyparameter ofst.markdownfor additional,
supported Markdown directives.

For accessibility reasons, you should never set an empty label, but
you can hide it withlabel_visibilityif needed. In the future,
we may disallow empty labels by raising an exception.

type(str or list of str or None)

The allowed file extension(s) for uploaded files. This can be one
of the following types:

- None(default): All file extensions are allowed.
- A string: A single file extension is allowed. For example, to
only accept CSV files, use"csv".
- A sequence of strings: Multiple file extensions are allowed. For
example, to only accept JPG/JPEG and PNG files, use["jpg", "jpeg", "png"].
accept_multiple_files(bool)

Whether to accept more than one file in a submission. If this isFalse(default), the user can only submit one file at a time.
If this isTrue, the user can upload multiple files at the same
time, in which case the return value will be a list of files.

key(str or int)

An optional string or integer to use as the unique key for the widget.
If this is omitted, a key will be generated for the widget
based on its content. No two widgets may have the same key.

help(str or None)

A tooltip that gets displayed next to the widget label. Streamlit
only displays the tooltip whenlabel_visibility="visible". If
this isNone(default), no tooltip is displayed.

The tooltip can optionally contain GitHub-flavored Markdown,
including the Markdown directives described in thebodyparameter ofst.markdown.

on_change(callable)

An optional callback invoked when this file_uploader's value
changes.

args(tuple)

An optional tuple of args to pass to the callback.

kwargs(dict)

An optional dict of kwargs to pass to the callback.

disabled(bool)

An optional boolean that disables the file uploader if set toTrue. The default isFalse.

label_visibility("visible", "hidden", or "collapsed")

The visibility of the label. The default is"visible". If this
is"hidden", Streamlit displays an empty spacer instead of the
label, which can help keep the widget alligned with other widgets.
If this is"collapsed", Streamlit displays no label or spacer.

(None, UploadedFile, or list of UploadedFile)

- If accept_multiple_files is False, returns either None or
an UploadedFile object.
- If accept_multiple_files is True, returns a list with the
uploaded files as UploadedFile objects. If no files were
uploaded, returns an empty list.
The UploadedFile class is a subclass of BytesIO, and therefore is
"file-like". This means you can pass an instance of it anywhere a
file is expected.

#### Examples

Insert a file uploader that accepts a single file at a time:

```python

import streamlit as st
import pandas as pd
from io import StringIO

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    st.write(stringio)

    # To read file as string:
    string_data = stringio.read()
    st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)

```

Insert a file uploader that accepts multiple files at a time:

```python

import streamlit as st

uploaded_files = st.file_uploader(
    "Choose a CSV file", accept_multiple_files=True
)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    st.write(bytes_data)

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
