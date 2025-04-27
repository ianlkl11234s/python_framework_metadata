---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config
date: 2025-04-27 12:51:02
---

## st.set_page_config

Configures the default settings of the page.

Note

This must be the first Streamlit command used on an app page, and must only
be set once per page.

st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

page_title(str or None)

The page title, shown in the browser tab. If None, defaults to the
filename of the script ("app.py" would show "app • Streamlit").

page_icon(Anything supported by st.image (except list), str, or None)

The page favicon. Ifpage_iconisNone(default), the favicon
will be a monochrome Streamlit logo.

In addition to the types supported byst.image(except list), the
following strings are valid:

- A single-character emoji. For example, you can setpage_icon="🦈".
- An emoji short code. For example, you can setpage_icon=":shark:".
For a list of all supported codes, seehttps://share.streamlit.io/streamlit/emoji-shortcodes.
- The string literal,"random". You can setpage_icon="random"to set a random emoji from the supported list above.
- An icon from the Material Symbols library (rounded style) in the
format":material/icon_name:"where "icon_name" is the name
of the icon in snake case.For example,page_icon=":material/thumb_up:"will display the
Thumb Up icon. Find additional icons in theMaterial Symbolsfont library.
A single-character emoji. For example, you can setpage_icon="🦈".

An emoji short code. For example, you can setpage_icon=":shark:".
For a list of all supported codes, seehttps://share.streamlit.io/streamlit/emoji-shortcodes.

The string literal,"random". You can setpage_icon="random"to set a random emoji from the supported list above.

An icon from the Material Symbols library (rounded style) in the
format":material/icon_name:"where "icon_name" is the name
of the icon in snake case.

For example,page_icon=":material/thumb_up:"will display the
Thumb Up icon. Find additional icons in theMaterial Symbolsfont library.

Note

Colors are not supported for Material icons. When you use a
Material icon for favicon, it will be black, regardless of browser
theme.

layout("centered" or "wide")

How the page content should be laid out. Defaults to "centered",
which constrains the elements into a centered column of fixed width;
"wide" uses the entire screen.

initial_sidebar_state("auto", "expanded", or "collapsed")

How the sidebar should start out. Defaults to "auto",
which hides the sidebar on small devices and shows it otherwise.
"expanded" shows the sidebar initially; "collapsed" hides it.
In most cases, you should just use "auto", otherwise the app will
look bad when embedded and viewed on mobile.

menu_items(dict)

Configure the menu that appears on the top-right side of this app.
The keys in this dict denote the menu item you'd like to configure:

- "Get help": str or NoneThe URL this menu item should point to.
If None, hides this menu item.
- "Report a Bug": str or NoneThe URL this menu item should point to.
If None, hides this menu item.
- "About": str or NoneA markdown string to show in the About dialog.
If None, only shows Streamlit's default About text.
The URL may also refer to an email address e.g.mailto:john@example.com.

#### Example

```python

import streamlit as st

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
