---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/concepts/multipage-apps/pages-directory
date: 2025-04-27 12:48:10
---

# Creating multipage apps using thepages/directory

`pages/`

The most customizable method for declaring multipage apps is usingPage and navigation. However, Streamlit also provides a frictionless way to create multipage apps where pages are automatically recognized and shown in a navigation widget inside your app's sidebar. This method uses thepages/directory.

`pages/`

This page assumes you understand thePage terminologypresented in the overview.

## App structure

When you use thepages/directory, Streamlit identifies pages in your multipage app by directory structure and filenames. Your entrypoint file (the file you pass tostreamlit run), is your app's homepage. When you have apages/directory next to your entrypoint file, Streamlit will identify each Python file within it as a page. The following example has three pages.your_homepage.pyis the entrypoint file and homepage.

`pages/`

`streamlit run`

`pages/`

`your_homepage.py`

`your_working_directory/
├── pages/
│   ├── a_page.py
│   └── another_page.py
└── your_homepage.py`

Run your multipage app just like you would for a single-page app. Pass your entrypoint file tostreamlit run.

`streamlit run`

`streamlit run your_homepage.py`

Only.pyfiles in thepages/directory will be identified as pages. Streamlit ignores all other files in thepages/directory and its subdirectories. Streamlit also ignores Python files in subdirectories ofpages/.

`.py`

`pages/`

`pages/`

`pages/`

#### Important

If you callst.navigationin your app (in any session), Streamlit will switch to using the newer, Page-and-navigation multipage structure. In this case, thepages/directory will be ignored across all sessions. You will not be able to revert back to thepages/directory unless you restart you app.

`st.navigation`

`pages/`

`pages/`

### How pages are sorted in the sidebar

See the overview to understand how Streamlit assignsAutomatic page labels and URLsbased on thenumber,separator,identifier, and".py"extension that constitute a filename.

`number`

`separator`

`identifier`

`".py"`

The entrypoint file is always displayed first. The remaining pages are sorted as follows:

- Files that have anumberappear before files without anumber.
- Files are sorted based on thenumber(if any), followed by thelabel(if any).
- When files are sorted, Streamlit treats thenumberas an actual number rather than a string. So03is the same as3.
`number`

`number`

`number`

`label`

`number`

`03`

`3`

This table shows examples of filenames and their corresponding labels, sorted by the order in which they appear in the sidebar.

Examples:

`1 - first page.py`

`12 monkeys.py`

`123.py`

`123_hello_dear_world.py`

`_12 monkeys.py`

#### Tip

Emojis can be used to make your page names more fun! For example, a file named🏠_Home.pywill create a page titled "🏠 Home" in the sidebar. When adding emojis to filenames, it’s best practice to include a numbered prefix to make autocompletion in your terminal easier. Terminal-autocomplete can get confused by unicode (which is how emojis are represented).

`🏠_Home.py`

## Notes and limitations

- Pages support run-on-save.When you update a page while your app is running, this causes a rerun for users currently viewing that exact page.When you update a page while your app is running, the app will not automatically rerun for users currently viewing a different page.
- When you update a page while your app is running, this causes a rerun for users currently viewing that exact page.
- When you update a page while your app is running, the app will not automatically rerun for users currently viewing a different page.
- While your app is running, adding or deleting a page updates the sidebar navigation immediately.
- st.set_page_configworks at the page level.When you settitleorfaviconusingst.set_page_config, this applies to the current page only.When you setlayoutusingst.set_page_config, the setting will remain for the session until changed by another call tost.set_page_config. If you usest.set_page_configto setlayout, it's recommended to call it onallpages.
- When you settitleorfaviconusingst.set_page_config, this applies to the current page only.
- When you setlayoutusingst.set_page_config, the setting will remain for the session until changed by another call tost.set_page_config. If you usest.set_page_configto setlayout, it's recommended to call it onallpages.
- Pages share the same Python modules globally:# page1.py
import foo
foo.hello = 123

# page2.py
import foo
st.write(foo.hello)  # If page1 already executed, this writes 123
- Pages share the samest.session_state:# page1.py
import streamlit as st
if "shared" not in st.session_state:
   st.session_state["shared"] = True

# page2.py
import streamlit as st
st.write(st.session_state["shared"]) # If page1 already executed, this writes True
Pages support run-on-save.

- When you update a page while your app is running, this causes a rerun for users currently viewing that exact page.
- When you update a page while your app is running, the app will not automatically rerun for users currently viewing a different page.
While your app is running, adding or deleting a page updates the sidebar navigation immediately.

st.set_page_configworks at the page level.

`st.set_page_config`

- When you settitleorfaviconusingst.set_page_config, this applies to the current page only.
- When you setlayoutusingst.set_page_config, the setting will remain for the session until changed by another call tost.set_page_config. If you usest.set_page_configto setlayout, it's recommended to call it onallpages.
`title`

`favicon`

`st.set_page_config`

`layout`

`st.set_page_config`

`st.set_page_config`

`st.set_page_config`

`layout`

Pages share the same Python modules globally:

`# page1.py
import foo
foo.hello = 123

# page2.py
import foo
st.write(foo.hello)  # If page1 already executed, this writes 123`

Pages share the samest.session_state:

`# page1.py
import streamlit as st
if "shared" not in st.session_state:
   st.session_state["shared"] = True

# page2.py
import streamlit as st
st.write(st.session_state["shared"]) # If page1 already executed, this writes True`

You now have a solid understanding of multipage apps. You've learned how to structure apps, define pages, and navigate between pages in the user interface. It's time tocreate your first multipage app! 🥳

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
