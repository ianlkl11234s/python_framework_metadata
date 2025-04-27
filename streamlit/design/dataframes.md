---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/concepts/design/dataframes
date: 2025-04-27 12:48:19
---

# Dataframes

Dataframes are a great way to display and edit data in a tabular format. Working with Pandas DataFrames and other tabular data structures is key to data science workflows. If developers and data scientists want to display this data in Streamlit, they have multiple options:st.dataframeandst.data_editor. If you want to solely display data in a table-like UI,st.dataframeis the way to go. If you want to interactively edit data, usest.data_editor. We explore the use cases and advantages of each option in the following sections.

`st.dataframe`

`st.data_editor`

## Display dataframes with st.dataframe

Streamlit can display dataframes in a table-like UI viast.dataframe:

`st.dataframe`

`import streamlit as st
import pandas as pd

df = pd.DataFrame(
    [
        {"command": "st.selectbox", "rating": 4, "is_widget": True},
        {"command": "st.balloons", "rating": 5, "is_widget": False},
        {"command": "st.time_input", "rating": 3, "is_widget": True},
    ]
)

st.dataframe(df, use_container_width=True)`

## st.dataframeUI features

`st.dataframe`

st.dataframeprovides additional functionality by usingglide-data-gridunder the hood:

`st.dataframe`

- Column sorting: To sort columns, select their headers, or select "Sort ascending" or "Sort descending" from the header menu (more_vert).
- Column resizing: To resize columns, drag and drop column header borders, or select "Autosize" from the header menu.
- Column hiding: To hide columns, select "Hide column" from the header menu.
- Reorder and pin columns: To reorder columns or pin them on the left, drag and drop column headers or select "Pin column" from the header menu, respectively.
- Format numbers, dates, and times: To change the format of numeric columns, select an option under "Format" in the header menu.
- Dataframe resizing: To resize dataframes, drag and drop the bottom right corner.
- Fullscreen view: To enlarge dataframes to fullscreen, select the fullscreen icon (fullscreen) in the toolbar.
- Search: To search through the data, select the search icon (search) in the toolbar or use hotkeys (⌘+ForCtrl+F).
- Download: To download the data as a CSV file, select the download icon (download) in the toolbar.
- Copy to clipboard: To copy the data to the clipboard, select one or multiple cells, use the hotkeys (⌘+CorCtrl+C), and paste them into your favorite spreadsheet software.
`⌘+F`

`Ctrl+F`

`⌘+C`

`Ctrl+C`

Try out all the UI features using the embedded app from the prior section.

In addition to Pandas DataFrames,st.dataframealso supports other common Python types, e.g., list, dict, or numpy array. It also supportsSnowparkandPySparkDataFrames, which allow you to lazily evaluate and pull data from databases. This can be useful for working with large datasets.

`st.dataframe`

## Edit data with st.data_editor

Streamlit supports editable dataframes via thest.data_editorcommand. Check out its API inst.data_editor. It shows the dataframe in a table, similar tost.dataframe. But in contrast tost.dataframe, this table isn't static! The user can click on cells and edit them. The edited data is then returned on the Python side. Here's an example:

`st.data_editor`

`st.dataframe`

`st.dataframe`

`df = pd.DataFrame(
    [
        {"command": "st.selectbox", "rating": 4, "is_widget": True},
        {"command": "st.balloons", "rating": 5, "is_widget": False},
        {"command": "st.time_input", "rating": 3, "is_widget": True},
    ]
)

edited_df = st.data_editor(df) # 👈 An editable dataframe

favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
st.markdown(f"Your favorite command is **{favorite_command}** 🎈")`

Try it out by double-clicking on any cell. You'll notice you can edit all cell values. Try editing the values in the rating column and observe how the text output at the bottom changes:

## st.data_editorUI features

`st.data_editor`

st.data_editoralso supports a few additional things:

`st.data_editor`

- Add and delete rows: You can do this by settingnum_rows= "dynamic"when callingst.data_editor. This will allow users to add and delete rows as needed.
- Copy and paste support: Copy and paste both betweenst.data_editorand spreadsheet software like Google Sheets and Excel.
- Access edited data: Access only the individual edits instead of the entire edited data structure via Session State.
- Bulk edits: Similar to Excel, just drag a handle to edit neighboring cells.
- Automatic input validation: Column Configuration provides strong data type support and other configurable options. For example, there's no way to enter letters into a number cell. Number cells can have a designated min and max.
- Edit common data structures:st.data_editorsupports lists, dicts, NumPy ndarray, and more!
`num_rows= "dynamic"`

`st.data_editor`

`st.data_editor`

`st.data_editor`

### Add and delete rows

Withst.data_editor, viewers can add or delete rows via the table UI. This mode can be activated by setting thenum_rowsparameter to"dynamic":

`st.data_editor`

`num_rows`

`"dynamic"`

`edited_df = st.data_editor(df, num_rows="dynamic")`

- To add new rows, click the plus icon (add) in the toolbar. Alternatively, click inside a shaded cell below the bottom row of the table.
- To delete rows, select one or more rows using the checkboxes on the left. Click the delete icon (delete) or press thedeletekey on your keyboard.
`delete`

### Copy and paste support

The data editor supports pasting in tabular data from Google Sheets, Excel, Notion, and many other similar tools. You can also copy-paste data betweenst.data_editorinstances. This functionality, powered by theClipboard API, can be a huge time saver for users who need to work with data across multiple platforms. To try it out:

`st.data_editor`

- Copy data fromthis Google Sheets documentto your clipboard.
- Single click any cell in thenamecolumn in the app above. Paste it in using hotkeys (⌘+VorCtrl+V).
`name`

`⌘+V`

`Ctrl+V`

#### Note

Every cell of the pasted data will be evaluated individually and inserted into the cells if the data is compatible with the column type. For example, pasting in non-numerical text data into a number column will be ignored.

#### Tip

If you embed your apps with iframes, you'll need to allow the iframe to access the clipboard if you want to use the copy-paste functionality. To do so, give the iframeclipboard-writeandclipboard-readpermissions. E.g.

`clipboard-write`

`clipboard-read`

`<iframe allow="clipboard-write;clipboard-read;" ... src="https://your-app-url"></iframe>`

As developers, ensure the app is served with a valid, trusted certificate when using TLS. If users encounter issues with copying and pasting data, direct them to check if their browser has activated clipboard access permissions for the Streamlit application, either when prompted or through the browser's site settings.

### Access edited data

Sometimes, it is more convenient to know which cells have been changed rather than getting the entire edited dataframe back. Streamlit makes this easy through the use ofSession State. If akeyparameter is set, Streamlit will store any changes made to the dataframe in Session State.

`key`

This snippet shows how you can access changed data using Session State:

`st.data_editor(df, key="my_key", num_rows="dynamic") # 👈 Set a key
st.write("Here's the value in Session State:")
st.write(st.session_state["my_key"]) # 👈 Show the value in Session State`

In this code snippet, thekeyparameter is set to"my_key". After the data editor is created, the value associated to"my_key"in Session State is displayed in the app usingst.write. This shows the additions, edits, and deletions that were made.

`key`

`"my_key"`

`"my_key"`

`st.write`

This can be useful when working with large dataframes and you only need to know which cells have changed, rather than access the entire edited dataframe.

Use all we've learned so far and apply them to the above embedded app. Try editing cells, adding new rows, and deleting rows.

Notice how edits to the table are reflected in Session State. When you make any edits, a rerun is triggered which sends the edits to the backend. The widget's state is a JSON object containing three properties:edited_rows,added_rows, anddeleted rows:.

#### Warning

When going fromst.experimental_data_editortost.data_editorin 1.23.0, the data editor's representation inst.session_statewas changed. Theedited_cellsdictionary is now callededited_rowsand uses a different format ({0: {"column name": "edited value"}}instead of{"0:1": "edited value"}). You may need to adjust your code if your app usesst.experimental_data_editorin combination withst.session_state."

`st.experimental_data_editor`

`st.data_editor`

`st.session_state`

`edited_cells`

`edited_rows`

`{0: {"column name": "edited value"}}`

`{"0:1": "edited value"}`

`st.experimental_data_editor`

`st.session_state`

- edited_rowsis a dictionary containing all edits. Keys are zero-based row indices and values are dictionaries that map column names to edits (e.g.{0: {"col1": ..., "col2": ...}}).
- added_rowsis a list of newly added rows. Each value is a dictionary with the same format as above (e.g.[{"col1": ..., "col2": ...}]).
- deleted_rowsis a list of row numbers that have been deleted from the table (e.g.[0, 2]).
`edited_rows`

`{0: {"col1": ..., "col2": ...}}`

`added_rows`

`[{"col1": ..., "col2": ...}]`

`deleted_rows`

`[0, 2]`

st.data_editordoes not support reordering rows, so added rows will always be appended to the end of the dataframe with any edits and deletions applicable to the original rows.

`st.data_editor`

### Bulk edits

The data editor includes a feature that allows for bulk editing of cells. Similar to Excel, you can drag a handle across a selection of cells to edit their values in bulk. You can even apply commonly usedkeyboard shortcutsin spreadsheet software. This is useful when you need to make the same change across multiple cells, rather than editing each cell individually.

### Edit common data structures

Editing doesn't just work for Pandas DataFrames! You can also edit lists, tuples, sets, dictionaries, NumPy arrays, or Snowpark & PySpark DataFrames. Most data types will be returned in their original format. But some types (e.g. Snowpark and PySpark) are converted to Pandas DataFrames. To learn about all the supported types, read thest.data_editorAPI.

For example, you can easily let the user add items to a list:

`edited_list = st.data_editor(["red", "green", "blue"], num_rows= "dynamic")
st.write("Here are all the colors you entered:")
st.write(edited_list)`

Or numpy arrays:

`import numpy as np

st.data_editor(np.array([
	["st.text_area", "widget", 4.92],
	["st.markdown", "element", 47.22]
]))`

Or lists of records:

`st.data_editor([
    {"name": "st.text_area", "type": "widget"},
    {"name": "st.markdown", "type": "element"},
])`

Or dictionaries and many more types!

`st.data_editor({
	"st.text_area": "widget",
	"st.markdown": "element"
})`

### Automatic input validation

The data editor includes automatic input validation to help prevent errors when editing cells. For example, if you have a column that contains numerical data, the input field will automatically restrict the user to only entering numerical data. This helps to prevent errors that could occur if the user were to accidentally enter a non-numerical value. Additional input validation can be configured through theColumn configuration API. Keep reading below for an overview of column configuration, including validation options.

## Configuring columns

You can configure the display and editing behavior of columns inst.dataframeandst.data_editorvia theColumn configuration API. We have developed the API to let you add images, charts, and clickable URLs in dataframe and data editor columns. Additionally, you can make individual columns editable, set columns as categorical and specify which options they can take, hide the index of the dataframe, and much more.

`st.dataframe`

`st.data_editor`

Column configuration includes the following column types: Text, Number, Checkbox, Selectbox, Date, Time, Datetime, List, Link, Image, Line chart, Bar chart, and Progress. There is also a generic Column option. See the embedded app below to view these different column types. Each column type is individually previewed in theColumn configuration APIdocumentation.

### Format values

Aformatparameter is available in column configuration forText,Date,Time, andDatetimecolumns. Chart-like columns can also be formatted.Line chartandBar chartcolumns have ay_minandy_maxparameters to set the vertical bounds. For aProgress column, you can declare the horizontal bounds withmin_valueandmax_value.

`format`

`y_min`

`y_max`

`min_value`

`max_value`

### Validate input

When specifying a column configuration, you can declare not only the data type of the column but also value restrictions. All column configuration elements allow you to make a column required with the keyword parameterrequired=True.

`required=True`

For Text and Link columns, you can specify the maximum number of characters withmax_charsor use regular expressions to validate entries throughvalidate. Numerical columns, including Number, Date, Time, and Datetime havemin_valueandmax_valueparameters. Selectbox columns have a configurable list ofoptions.

`max_chars`

`validate`

`min_value`

`max_value`

`options`

The data type for Number columns isfloatby default. Passing a value of typeintto any ofmin_value,max_value,step, ordefaultwill set the type for the column asint.

`float`

`int`

`min_value`

`max_value`

`step`

`default`

`int`

### Configure an empty dataframe

You can usest.data_editorto collect tabular input from a user. When starting from an empty dataframe, default column types are text. Use column configuration to specify the data types you want to collect from users.

`st.data_editor`

`import streamlit as st
import pandas as pd

df = pd.DataFrame(columns=['name','age','color'])
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
config = {
    'name' : st.column_config.TextColumn('Full Name (required)', width='large', required=True),
    'age' : st.column_config.NumberColumn('Age (years)', min_value=0, max_value=122),
    'color' : st.column_config.SelectboxColumn('Favorite Color', options=colors)
}

result = st.data_editor(df, column_config = config, num_rows='dynamic')

if st.button('Get results'):
    st.write(result)`

## Additional formatting options

In addition to column configuration,st.dataframeandst.data_editorhave a few more parameters to customize the display of your dataframe.

`st.dataframe`

`st.data_editor`

- hide_index: Set toTrueto hide the dataframe's index.
- column_order: Pass a list of column labels to specify the order of display.
- disabled: Pass a list of column labels to disable them from editing. This let's you avoid disabling them individually.
`hide_index`

`True`

`column_order`

`disabled`

## Handling large datasets

st.dataframeandst.data_editorhave been designed to theoretically handle tables with millions of rows thanks to their highly performant implementation using the glide-data-grid library and HTML canvas. However, the maximum amount of data that an app can realistically handle will depend on several other factors, including:

`st.dataframe`

`st.data_editor`

- The maximum size of WebSocket messages: Streamlit's WebSocket messages are configurable via theserver.maxMessageSizeconfig option, which limits the amount of data that can be transferred via the WebSocket connection at once.
- The server memory: The amount of data that your app can handle will also depend on the amount of memory available on your server. If the server's memory is exceeded, the app may become slow or unresponsive.
- The user's browser memory: Since all the data needs to be transferred to the user's browser for rendering, the amount of memory available on the user's device can also affect the app's performance. If the browser's memory is exceeded, it may crash or become unresponsive.
`server.maxMessageSize`

In addition to these factors, a slow network connection can also significantly slow down apps that handle large datasets.

When handling large datasets with more than 150,000 rows, Streamlit applies additional optimizations and disables column sorting. This can help to reduce the amount of data that needs to be processed at once and improve the app's performance.

## Limitations

- Streamlit casts all column names to strings internally, sost.data_editorwill return a DataFrame where all column names are strings.
- The dataframe toolbar is not currently configurable.
- While Streamlit's data editing capabilities offer a lot of functionality, editing is enabled for a limited set of column types (TextColumn,NumberColumn,LinkColumn,CheckboxColumn,SelectboxColumn,DateColumn,TimeColumn, andDatetimeColumn). We are actively working on supporting editing for other column types as well, such as images, lists, and charts.
- Almost all editable datatypes are supported for index editing. However,pandas.CategoricalIndexandpandas.MultiIndexare not supported for editing.
- Sorting is not supported forst.data_editorwhennum_rows="dynamic".
- Sorting is deactivated to optimize performance on large datasets with more than 150,000 rows.
`st.data_editor`

`pandas.CategoricalIndex`

`pandas.MultiIndex`

`st.data_editor`

`num_rows="dynamic"`

We are continually working to improve Streamlit's handling of DataFrame and add functionality to data editing, so keep an eye out for updates.

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
