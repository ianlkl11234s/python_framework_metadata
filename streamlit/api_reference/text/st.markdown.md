---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/text/st.markdown
date: 2025-04-27 12:48:51
---

## st.markdown

Display string formatted as Markdown.

st.markdown(body, unsafe_allow_html=False, *, help=None)

body(any)

The text to display as GitHub-flavored Markdown. Syntax
information can be found at:https://github.github.com/gfm.
If anything other than a string is passed, it will be converted
into a string behind the scenes usingstr(body).

This also supports:

- Emoji shortcodes, such as:+1:and:sunglasses:.
For a list of all supported codes,
seehttps://share.streamlit.io/streamlit/emoji-shortcodes.
- Streamlit logo shortcode. Use:streamlit:to add a little
Streamlit flair to your text.
- A limited set of typographical symbols."<--><->-->= <= ~="becomes "← → ↔ — ≥ ≤ ≈" when parsed as Markdown.
- Google Material Symbols (rounded style), using the syntax:material/icon_name:, where "icon_name" is the name of the
icon in snake case. For a complete list of icons, see Google'sMaterial Symbolsfont library.
- LaTeX expressions, by wrapping them in "$" or "$$" (the "$$"
must be on their own lines). Supported LaTeX functions are listed
athttps://katex.org/docs/supported.html.
- Colored text and background colors for text, using the syntax:color[text to be colored]and:color-background[textto be colored],
respectively.colormust be replaced with any of the following
supported colors: blue, green, orange, red, violet, gray/grey,
rainbow, or primary. For example, you can use:orange[your text here]or:blue-background[yourtext here].
If you use "primary" for color, Streamlit will use the default
primary accent color unless you set thetheme.primaryColorconfiguration option.
- Colored badges, using the syntax:color-badge[textin the badge].colormust be replaced with any of the following supported
colors: blue, green, orange, red, violet, gray/grey, or primary.
For example, you can use:orange-badge[yourtext here]or:blue-badge[yourtext here].
- Small text, using the syntax:small[text to show small].
unsafe_allow_html(bool)

Whether to render HTML withinbody. If this isFalse(default), any HTML tags found inbodywill be escaped and
therefore treated as raw text. If this isTrue, any HTML
expressions withinbodywill be rendered.

Adding custom HTML to your app impacts safety, styling, and
maintainability.

Note

If you only want to insert HTML or CSS without Markdown text,
we recommend usingst.htmlinstead.

help(str or None)

A tooltip that gets displayed next to the Markdown. If this isNone(default), no tooltip is displayed.

The tooltip can optionally contain GitHub-flavored Markdown,
including the Markdown directives described in thebodyparameter ofst.markdown.

#### Examples

```python

import streamlit as st

st.markdown("*Streamlit* is **really** ***cool***.")
st.markdown('''
    :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
    :gray[pretty] :rainbow[colors] and :blue-background[highlight] text.''')
st.markdown("Here's a bouquet &mdash;\
            :tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:")

multi = '''If you end a line with two spaces,
a soft return is used for the next line.

Two (or more) newline characters in a row will result in a hard return.
'''
st.markdown(multi)

```

`import streamlit as st

md = st.text_area('Type in your markdown string (without outer quotes)',
                  "Happy Streamlit-ing! :balloon:")

st.code(f"""
import streamlit as st

st.markdown('''{md}''')
""")

st.markdown(md)`

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
