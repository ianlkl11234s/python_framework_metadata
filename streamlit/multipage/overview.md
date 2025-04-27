---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/concepts/multipage-apps/overview
date: 2025-04-27 12:48:05
---

# Overview of multipage apps

Streamlit provides two built-in mechanisms for creating multipage apps. The simplest method is to use apages/directory. However, the preferred and more customizable method is to usest.navigation.

`pages/`

`st.navigation`

## st.Pageandst.navigation

`st.Page`

`st.navigation`

If you want maximum flexibility in defining your multipage app, we recommend usingst.Pageandst.navigation. Withst.Pageyou can declare any Python file orCallableas a page in your app. Furthermore, you can define common elements for your pages in your entrypoint file (the file you pass tostreamlit run). With these methods, your entrypoint file becomes like a picture frame shared by all your pages.

`st.Page`

`st.navigation`

`st.Page`

`Callable`

`streamlit run`

You must includest.navigationin your entrypoint file to configure your app's navigation menu. This is also how your entrypoint file serves as the router between your pages.

`st.navigation`

## pages/directory

`pages/`

If you're looking for a quick and simple solution, just place apages/directory next to your entrypoint file. For every Python file in yourpages/directory, Streamlit will create an additional page for your app. Streamlit determines the page labels and URLs from the file name and automatically populates a navigation menu at the top of your app's sidebar.

`pages/`

`pages/`

`your_working_directory/
├── pages/
│   ├── a_page.py
│   └── another_page.py
└── your_homepage.py`

Streamlit determines the page order in navigation from the filenames. You can use numerical prefixes in the filenames to adjust page order. For more information, seeHow pages are sorted in the sidebar. If you want to customize your navigation menu with this option, you can deactivate the default navigation throughconfiguration(client.showSidebarNavigation = false). Then, you can usest.page_linkto manually contruct a custom navigation menu. Withst.page_link, you can change the page label and icon in your navigation menu, but you can't change the URLs of your pages.

`client.showSidebarNavigation = false`

`st.page_link`

`st.page_link`

## Page terminology

A page has four identifying pieces as follows:

- Page source: This is a Python file or callable function with the page's source code.
- Page label: This is how the page is identified within the navigation menu. Seelooks_one.
- Page title: This is the content of the HTML<title>element and how the page is identified within a browser tab. Seelooks_two.
- Page URL pathname: This is the relative path of the page from the root URL of the app. Seelooks_3.
`<title>`

Additionly, a page can have two icons as follows:

- Page favicon: This is the icon next to your page title within a browser tab. Seelooks_4.
- Page icon: This is the icon next to your page label in the navigation menu. Seelooks_5.
Typically, the page icon and favicon are the same, but it's possible make them different.

1. Page label, 2.Page titles, 3. Page URL pathname, 4.Page favicon, 5. Page icon

## Automatic page labels and URLs

If you usest.Pagewithout declaring the page title or URL pathname, Streamlit falls back on automatically determining the page label, title, and URL pathname in the same manner as when you use apages/directory with the default navigation menu. This section describes this naming convention which is shared between the two approaches to multipage apps.

`st.Page`

`pages/`

### Parts of filenames and callables

Filenames are composed of four different parts as follows (in order):

- number: A non-negative integer.
- separator: Any combination of underscore ("_"), dash ("-"), and space (" ").
- identifier: Everything up to, but not including,".py".
- ".py"
`number`

`separator`

`"_"`

`"-"`

`" "`

`identifier`

`".py"`

`".py"`

For callables, the function name is theidentifier, including any leading or trailing underscores.

`identifier`

### How Streamlit converts filenames into labels and titles

Within the navigation menu, Streamlit displays page labels and titles as follows:

- If your page has anidentifier, Streamlit displays theidentifier. Any underscores within the page'sidentifierare treated as spaces. Therefore, leading and trailing underscores are not shown. Sequential underscores appear as a single space.
- Otherwise, if your page has anumberbut does not have anidentifier, Streamlit displays thenumber, unmodified. Leading zeros are included, if present.
- Otherwise, if your page only has aseparatorwith nonumberand noidentifier, Streamlit will not display the page in the sidebar navigation.
`identifier`

`identifier`

`identifier`

`number`

`identifier`

`number`

`separator`

`number`

`identifier`

The following filenames and callables would all display as "Awesome page" in the sidebar navigation.

- "Awesome page.py"
- "Awesome_page.py"
- "02Awesome_page.py"
- "--Awesome_page.py"
- "1_Awesome_page.py"
- "33 - Awesome page.py"
- Awesome_page()
- _Awesome_page()
- __Awesome_page__()
`"Awesome page.py"`

`"Awesome_page.py"`

`"02Awesome_page.py"`

`"--Awesome_page.py"`

`"1_Awesome_page.py"`

`"33 - Awesome page.py"`

`Awesome_page()`

`_Awesome_page()`

`__Awesome_page__()`

### How Streamlit converts filenames into URL pathnames

Your app's homepage is associated to the root URL of app. For all other pages, theiridentifierornumberbecomes their URL pathname as follows:

`identifier`

`number`

- If your page has anidentifierthat came from a filename, Streamlit uses theidentifierwith one modification. Streamlit condenses each consecutive grouping of spaces (" ") and underscores ("_") to a single underscore.
- Otherwise, if your page has anidentifierthat came from the name of a callable, Streamlit uses theidentifierunmodified.
- Otherwise, if your page has anumberbut does not have anidentifier, Streamlit uses thenumber. Leading zeros are included, if present.
`identifier`

`identifier`

`" "`

`"_"`

`identifier`

`identifier`

`number`

`identifier`

`number`

For each filename in the list above, the URL pathname would be "Awesome_page" relative to the root URL of the app. For example, if your app was running onlocalhostport8501, the full URL would belocalhost:8501/awesome_page. For the last two callables, however, the pathname would include the leading and trailing underscores to match the callable name exactly.

`localhost`

`8501`

`localhost:8501/awesome_page`

## Navigating between pages

The primary way users navigate between pages is through the navigation widget. Both methods for defining multipage apps include a default navigation menu that appears in the sidebar. When a user clicks this navigation widget, the app reruns and loads the selected page. Optionally, you can hide the default navigation UI and build your own withst.page_link. For more information, seeBuild a custom navigation menu withst.page_link.

`st.page_link`

`st.page_link`

If you need to programmatically switch pages, usest.switch_page.

`st.switch_page`

Users can also navigate between pages using URLs as noted above. When multiple files have the same URL pathname, Streamlit picks the first one (based on the ordering in the navigation menu. Users can view a specific page by visiting the page's URL.

#### Important

Navigating between pages by URL creates a new browser session. In particular, clicking markdown links to other pages resetsst.session_state. In order to retain values inst.session_state, handle page switching through Streamlit navigation commands and widgets, likest.navigation,st.switch_page,st.page_link, and the built-in navigation menu.

`st.session_state`

`st.session_state`

`st.navigation`

`st.switch_page`

`st.page_link`

If a user tries to access a URL for a page that does not exist, they will see a modal like the one below, saying "Page not found."

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
