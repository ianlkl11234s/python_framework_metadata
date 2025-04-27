---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/concepts/architecture/widget-behavior
date: 2025-04-27 12:48:03
---

# Understanding widget behavior

Widgets (likest.button,st.selectbox, andst.text_input) are at the heart of Streamlit apps. They are the interactive elements of Streamlit that pass information from your users into your Python code. Widgets are magical and often work how you want, but they can have surprising behavior in some situations. Understanding the different parts of a widget and the precise order in which events occur helps you achieve your desired results.

`st.button`

`st.selectbox`

`st.text_input`

This guide covers advanced concepts about widgets. Generally, it begins with simpler concepts and increases in complexity. For most beginning users, these details won't be important to know right away. When you want to dynamically change widgets or preserve widget information between pages, these concepts will be important to understand. We recommend having a basic understanding ofSession Statebefore reading this guide.

- The actions of one user do not affect the widgets of any other user.
- A widget function call returns the widget's current value, which is a simple Python type. (e.g.st.buttonreturns a boolean value.)
- Widgets return their default values on their first call before a user interacts with them.
- A widget's identity depends on the arguments passed to the widget function. Changing a widget's label, min or max value, default value, placeholder text, help text, or key will cause it to reset.
- If you don't call a widget function in a script run, Streamlit will delete the widget's information—including its key-value pair in Session State. If you call the same widget function later, Streamlit treats it as a new widget.
`st.button`

The last two points (widget identity and widget deletion) are the most relevant when dynamically changing widgets or working with multi-page applications. This is covered in detail later in this guide:Statefulness of widgetsandWidget life cycle.

## Anatomy of a widget

There are four parts to keep in mind when using widgets:

- The frontend component as seen by the user.
- The backend value or value as seen throughst.session_state.
- The key of the widget used to access its value viast.session_state.
- The return value given by the widget's function.
`st.session_state`

`st.session_state`

### Widgets are session dependent

Widget states are dependent on a particular session (browser connection). The actions of one user do not affect the widgets of any other user. Furthermore, if a user opens up multiple tabs to access an app, each tab will be a unique session. Changing a widget in one tab will not affect the same widget in another tab.

### Widgets return simple Python data types

The value of a widget as seen throughst.session_stateand returned by the widget function are of simple Python types. For example,st.buttonreturns a boolean value and will have the same boolean value saved inst.session_stateif using a key. The first time a widget function is called (before a user interacts with it), it will return its default value. (e.g.st.selectboxreturns the first option by default.) Default values are configurable for all widgets with a few special exceptions likest.buttonandst.file_uploader.

`st.session_state`

`st.button`

`st.session_state`

`st.selectbox`

`st.button`

`st.file_uploader`

### Keys help distinguish widgets and access their values

Widget keys serve two purposes:

- Distinguishing two otherwise identical widgets.
- Creating a means to access and manipulate the widget's value throughst.session_state.
`st.session_state`

Whenever possible, Streamlit updates widgets incrementally on the frontend instead of rebuilding them with each rerun. This means Streamlit assigns an ID to each widget from the arguments passed to the widget function. A widget's ID is based on parameters such as label, min or max value, default value, placeholder text, help text, and key. The page where the widget appears also factors into a widget's ID. If you have two widgets of the same type with the same arguments on the same page, you will get aDuplicateWidgetIDerror. In this case, assign unique keys to the two widgets.

`DuplicateWidgetID`

#### Streamlit can't understand two identical widgets on the same page

`# This will cause a DuplicateWidgetID error.
st.button("OK")
st.button("OK")`

#### Use keys to distinguish otherwise identical widgets

`st.button("OK", key="privacy")
st.button("OK", key="terms")`

## Order of operations

When a user interacts with a widget, the order of logic is:

- Its value inst.session_stateis updated.
- The callback function (if any) is executed.
- The page reruns with the widget function returning its new value.
`st.session_state`

If the callback function writes anything to the screen, that content will appear above the rest of the page. A callback function runs as aprefixto the script rerunning. Consequently, that means anything written via a callback function will disappear as soon as the user performs their next action. Other widgets should generally not be created within a callback function.

#### Note

If a callback function is passed any args or kwargs, those arguments will be established when the widget is rendered. In particular, if you want to use a widget's new value in its own callback function, you cannot pass that value to the callback function via theargsparameter; you will have to assign a key to the widget and look up its new value using a call tost.session_statewithin the callback function.

`args`

`st.session_state`

### Using callback functions with forms

Using a callback function with a form requires consideration of this order of operations.

`import streamlit as st

if "attendance" not in st.session_state:
    st.session_state.attendance = set()


def take_attendance():
    if st.session_state.name in st.session_state.attendance:
        st.info(f"{st.session_state.name} has already been counted.")
    else:
        st.session_state.attendance.add(st.session_state.name)


with st.form(key="my_form"):
    st.text_input("Name", key="name")
    st.form_submit_button("I'm here!", on_click=take_attendance)`

## Statefulness of widgets

As long as the defining parameters of a widget remain the same and that widget is continuously rendered on the frontend, then it will be stateful and remember user input.

### Changing parameters of a widget will reset it

If any of the defining parameters of a widget change, Streamlit will see it as a new widget and it will reset. The use of manually assigned keys and default values is particularly important in this case.Note that callback functions, callback args and kwargs, label visibility, and disabling a widget do not affect a widget's identity.

In this example, we have a slider whose min and max values are changed. Try interacting with each slider to change its value then change the min or max setting to see what happens.

`import streamlit as st

cols = st.columns([2, 1, 2])
minimum = cols[0].number_input("Minimum", 1, 5)
maximum = cols[2].number_input("Maximum", 6, 10, 10)

st.slider("No default, no key", minimum, maximum)
st.slider("No default, with key", minimum, maximum, key="a")
st.slider("With default, no key", minimum, maximum, value=5)
st.slider("With default, with key", minimum, maximum, value=5, key="b")`

#### Updating a slider with no default value

For the first two sliders above, as soon as the min or max value is changed, the sliders reset to the min value. The changing of the min or max value makes them "new" widgets from Streamlit's perspective and so they are recreated from scratch when the app reruns with the changed parameters. Since no default value is defined, each widget will reset to its min value. This is the same with or without a key since it's seen as a new widget either way. There is a subtle point to understand about pre-existing keys connecting to widgets. This will be explained further down inWidget life cycle.

#### Updating a slider with a default value

For the last two sliders above, a change to the min or max value will result in the widgets being seen as "new" and thus recreated like before. Since a default value of 5 is defined, each widget will reset to 5 whenever the min or max is changed. This is again the same (with or without a key).

A solution toRetain statefulness when changing a widget's parametersis provided further on.

### Widgets do not persist when not continually rendered

If a widget's function is not called during a script run, then none of its parts will be retained, including its value inst.session_state. If a widget has a key and you navigate away from that widget, its key and associated value inst.session_statewill be deleted. Even temporarily hiding a widget will cause it to reset when it reappears; Streamlit will treat it like a new widget. You can either interrupt theWidget clean-up process(described at the end of this page) or save the value to another key.

`st.session_state`

`st.session_state`

#### Save widget values in Session State to preserve them between pages

If you want to navigate away from a widget and return to it while keeping its value, use a separate key inst.session_stateto save the information independently from the widget. In this example, a temporary key is used with a widget. The temporary key uses an underscore prefix. Hence,"_my_key"is used as the widget key, but the data is copied to"my_key"to preserve it between pages.

`st.session_state`

`"_my_key"`

`"my_key"`

`import streamlit as st

def store_value():
    # Copy the value to the permanent key
    st.session_state["my_key"] = st.session_state["_my_key"]

# Copy the saved value to the temporary key
st.session_state["_my_key"] = st.session_state["my_key"]
st.number_input("Number of filters", key="_my_key", on_change=store_value)`

If this is functionalized to work with multiple widgets, it could look something like this:

`import streamlit as st

def store_value(key):
    st.session_state[key] = st.session_state["_"+key]
def load_value(key):
    st.session_state["_"+key] = st.session_state[key]

load_value("my_key")
st.number_input("Number of filters", key="_my_key", on_change=store_value, args=["my_key"])`

## Widget life cycle

When a widget function is called, Streamlit will check if it already has a widget with the same parameters. Streamlit will reconnect if it thinks the widget already exists. Otherwise, it will make a new one.

As mentioned earlier, Streamlit determines a widget's ID based on parameters such as label, min or max value, default value, placeholder text, help text, and key. The page name also factors into a widget's ID. On the other hand, callback functions, callback args and kwargs, label visibility, and disabling a widget do not affect a widget's identity.

### Calling a widget function when the widget doesn't already exist

If your script rerun calls a widget function with changed parameters or calls a widget function that wasn't used on the last script run:

- Streamlit will build the frontend and backend parts of the widget, using its default value.
- If the widget has been assigned a key, Streamlit will check if that key already exists in Session State.a. If it exists and is not currently associated with another widget, Streamlit will assign that key's value to the widget.
b. Otherwise, it will assign the default value to the key inst.session_state(creating a new key-value pair or overwriting an existing one).
- If there are args or kwargs for a callback function, they are computed and saved at this point in time.
- The widget value is then returned by the function.
`st.session_state`

Step 2 can be tricky. If you have a widget:

`st.number_input("Alpha",key="A")`

and you change it on a page rerun to:

`st.number_input("Beta",key="A")`

Streamlit will see that as a new widget because of the label change. The key"A"will be considered part of the widget labeled"Alpha"and will not be attached as-is to the new widget labeled"Beta". Streamlit will destroyst.session_state.Aand recreate it with the default value.

`"A"`

`"Alpha"`

`"Beta"`

`st.session_state.A`

If a widget attaches to a pre-existing key when created and is also manually assigned a default value, you will get a warning if there is a disparity. If you want to control a widget's value throughst.session_state, initialize the widget's value throughst.session_stateand avoid the default value argument to prevent conflict.

`st.session_state`

`st.session_state`

### Calling a widget function when the widget already exists

When rerunning a script without changing a widget's parameters:

- Streamlit will connect to the existing frontend and backend parts.
- If the widget has a key that was deleted fromst.session_state, then Streamlit will recreate the key using the current frontend value. (e.g Deleting a key will not revert the widget to a default value.)
- It will return the current value of the widget.
`st.session_state`

### Widget clean-up process

When Streamlit gets to the end of a script run, it will delete the data for any widgets it has in memory that were not rendered on the screen. Most importantly, that means Streamlit will delete all key-value pairs inst.session_stateassociated with a widget not currently on screen.

`st.session_state`

## Additional examples

As promised, let's address how to retain the statefulness of widgets when changing pages or modifying their parameters. There are two ways to do this.

- Use dummy keys to duplicate widget values inst.session_stateand protect the data from being deleted along with the widget.
- Interrupt the widget clean-up process.
`st.session_state`

The first method was shown above inSave widget values in Session State to preserve them between pages

### Interrupting the widget clean-up process

To retain information for a widget withkey="my_key", just add this to the top of every page:

`key="my_key"`

`st.session_state.my_key = st.session_state.my_key`

When you manually save data to a key inst.session_state, it will become detached from any widget as far as the clean-up process is concerned. If you navigate away from a widget with some key"my_key"and save data tost.session_state.my_keyon the new page, you will interrupt the widget clean-up process and prevent the key-value pair from being deleted or overwritten if another widget with the same key exists.

`st.session_state`

`"my_key"`

`st.session_state.my_key`

### Retain statefulness when changing a widget's parameters

Here is a solution to our earlier example of changing a slider's min and max values. This solution interrupts the clean-up process as described above.

`import streamlit as st

# Set default value
if "a" not in st.session_state:
    st.session_state.a = 5

cols = st.columns(2)
minimum = cols[0].number_input("Min", 1, 5, key="min")
maximum = cols[1].number_input("Max", 6, 10, 10, key="max")


def update_value():
    # Helper function to ensure consistency between widget parameters and value
    st.session_state.a = min(st.session_state.a, maximum)
    st.session_state.a = max(st.session_state.a, minimum)


# Validate the slider value before rendering
update_value()
st.slider("A", minimum, maximum, key="a")`

Theupdate_value()helper function is actually doing two things. On the surface, it's making sure there are no inconsistent changes to the parameters values as described. Importantly, it's also interrupting the widget clean-up process. When the min or max value of the widget changes, Streamlit sees it as a new widget on rerun. Without saving a value tost.session_state.a, the value would be thrown out and replaced by the "new" widget's default value.

`update_value()`

`st.session_state.a`

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
