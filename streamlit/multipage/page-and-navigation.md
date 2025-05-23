---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/concepts/multipage-apps/page-and-navigation
date: 2025-04-27 12:48:07
---

# Define multipage apps withst.Pageandst.navigation

`st.Page`

`st.navigation`

st.Pageandst.navigationare the preferred commands for defining multipage apps. With these commands, you have flexibility to organize your project files and customize your navigation menu. Simply initializeStreamlitPageobjects withst.Page, then pass thoseStreamlitPageobjects tost.navigationin your entrypoint file (i.e. the file you pass tostreamlit run).

`st.Page`

`st.navigation`

`StreamlitPage`

`st.Page`

`StreamlitPage`

`st.navigation`

`streamlit run`

This page assumes you understand thePage terminologypresented in the overview.

## App structure

When usingst.navigation, your entrypoint file acts like a page router. Each page is a script executed from your entrypoint file. You can define a page from a Python file or function. If you include elements or widgets in your entrypoint file, they become common elements between your pages. In this case, you can think of your entrypoint file like a picture frame around each of your pages.

`st.navigation`

You can only callst.navigationonce per app run and you must call it from your entrypoint file. When a user selects a page in navigation (or is routed through a command likest.switch_page),st.navigationreturns the selected page. You must manually execute that page with the.run()method. The following example is a two-page app where each page is defined by a Python file.

`st.navigation`

`st.switch_page`

`st.navigation`

`.run()`

Directory structure:

`your-repository/
├── page_1.py
├── page_2.py
└── streamlit_app.py`

streamlit_app.py:

`streamlit_app.py`

`import streamlit as st

pg = st.navigation([st.Page("page_1.py"), st.Page("page_2.py")])
pg.run()`

## Defining pages

st.Pagelets you define a page. The first and only required argument defines your page source, which can be a Python file or function. When using Python files, your pages may be in a subdirectory (or superdirectory). The path to your page file must always be relative to the entrypoint file. Once you create your page objects, pass them tost.navigationto register them as pages in your app.

`st.Page`

`st.navigation`

If you don't define your page title or URL pathname, Streamlit will infer them from the file or function name as described in the multipage appsOverview. However,st.Pagelets you configure them manually. Withinst.Page, Streamlit usestitleto set the page label and title. Additionaly, Streamlit usesiconto set the page icon and favicon. If you want to have a different page title and label, or different page icon and favicon, you can usest.set_page_configto change the page title and/or favicon. Just callst.set_page_configafterst.navigation, either in your entrypoint file or in your page source.

`st.Page`

`st.Page`

`title`

`icon`

`st.set_page_config`

`st.set_page_config`

`st.navigation`

The following example usesst.set_page_configto set a page title and favicon consistently across pages. Each page will have its own label and icon in the navigation menu, but the browser tab will show a consistent title and favicon on all pages.

`st.set_page_config`

Directory structure:

`your-repository/
├── create.py
├── delete.py
└── streamlit_app.py`

streamlit_app.py:

`streamlit_app.py`

`import streamlit as st

create_page = st.Page("create.py", title="Create entry", icon=":material/add_circle:")
delete_page = st.Page("delete.py", title="Delete entry", icon=":material/delete:")

pg = st.navigation([create_page, delete_page])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()`

## Customizing navigation

If you want to group your pages into sections,st.navigationlets you insert headers within your navigation. Alternatively, you can disable the default navigation widget and build a custom navigation menu withst.page_link.

`st.navigation`

`st.page_link`

Additionally, you can dynamically change which pages you pass tost.navigation. However, only the page returned byst.navigationaccepts the.run()method. If a user enters a URL with a pathname, and that pathname is not associated to a page inst.navigation(on first run), Streamlit will throw a "Page not found" error and redirect them to the default page.

`st.navigation`

`st.navigation`

`.run()`

`st.navigation`

### Adding section headers

As long as you don't want to hide a valid, accessible page in the navigation menu, the simplest way to customize your navigation menu is to organize the pages withinst.navigation. You can sort or group pages, as well as remove any pages you don't want the user to access. This is a convenient way to handle user permissions.

`st.navigation`

The following example creates two menu states. When a user starts a new session, they are not logged in. In this case, the only available page is the login page. If a user tries to access another page by URL, it will create a new session and Streamlit will not recognize the page. The user will be diverted to the login page. However, after a user logs in, they will see a navigation menu with three sections and be directed to the dashboard as the app's default page (i.e. homepage).

Directory structure:

`your-repository/
├── reports
│   ├── alerts.py
│   ├── bugs.py
│   └── dashboard.py
├── tools
│   ├── history.py
│   └── search.py
└── streamlit_app.py`

streamlit_app.py:

`streamlit_app.py`

`import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

dashboard = st.Page(
    "reports/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True
)
bugs = st.Page("reports/bugs.py", title="Bug reports", icon=":material/bug_report:")
alerts = st.Page(
    "reports/alerts.py", title="System alerts", icon=":material/notification_important:"
)

search = st.Page("tools/search.py", title="Search", icon=":material/search:")
history = st.Page("tools/history.py", title="History", icon=":material/history:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Reports": [dashboard, bugs, alerts],
            "Tools": [search, history],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()`

### Dynamically changing the available pages

You can change what pages are available to a user by updating the list of pages inst.navigation. This is a convenient way to handle role-based or user-based access to certain pages. For more information, check out our tutorial,Create a dynamic navigation menu.

`st.navigation`

### Building a custom navigation menu

If you want more control over your navigation menu, you can hide the default navigation and build your own. You can hide the default navigation by includingposition="hidden"in yourst.navigationcommand. If you want a page to be available to a user without showing it in the navigation menu, you must use this method. A user can't be routed to a page if the page isn't included inst.navigation. This applies to navigation by URL as well as commands likest.switch_pageandst.page_link.

`position="hidden"`

`st.navigation`

`st.navigation`

`st.switch_page`

`st.page_link`

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
