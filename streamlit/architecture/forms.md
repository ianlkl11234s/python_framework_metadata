---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/concepts/architecture/forms
date: 2025-04-27 12:47:59
---

# Using forms

When you don't want to rerun your script with each input made by a user,st.formis here to help! Forms make it easy to batch user input into a single rerun. This guide to using forms provides examples and explains how users interact with forms.

`st.form`

## Example

In the following example, a user can set multiple parameters to update the map. As the user changes the parameters, the script will not rerun and the map will not update. When the user submits the form with the button labeled "Update map", the script reruns and the map updates.

If at any time the user clicks "Generate new points" which is outside of the form, the script will rerun. If the user has any unsubmitted changes within the form, these willnotbe sent with the rerun. All changes made to a form will only be sent to the Python backend when the form itself is submitted.

`import streamlit as st
import pandas as pd
import numpy as np

def get_data():
    df = pd.DataFrame({
        "lat": np.random.randn(200) / 50 + 37.76,
        "lon": np.random.randn(200) / 50 + -122.4,
        "team": ['A','B']*100
    })
    return df

if st.button('Generate new points'):
    st.session_state.df = get_data()
if 'df' not in st.session_state:
    st.session_state.df = get_data()
df = st.session_state.df

with st.form("my_form"):
    header = st.columns([1,2,2])
    header[0].subheader('Color')
    header[1].subheader('Opacity')
    header[2].subheader('Size')

    row1 = st.columns([1,2,2])
    colorA = row1[0].color_picker('Team A', '#0000FF')
    opacityA = row1[1].slider('A opacity', 20, 100, 50, label_visibility='hidden')
    sizeA = row1[2].slider('A size', 50, 200, 100, step=10, label_visibility='hidden')

    row2 = st.columns([1,2,2])
    colorB = row2[0].color_picker('Team B', '#FF0000')
    opacityB = row2[1].slider('B opacity', 20, 100, 50, label_visibility='hidden')
    sizeB = row2[2].slider('B size', 50, 200, 100, step=10, label_visibility='hidden')

    st.form_submit_button('Update map')

alphaA = int(opacityA*255/100)
alphaB = int(opacityB*255/100)

df['color'] = np.where(df.team=='A',colorA+f'{alphaA:02x}',colorB+f'{alphaB:02x}')
df['size'] = np.where(df.team=='A',sizeA, sizeB)

st.map(df, size='size', color='color')`

## User interaction

If a widget is not in a form, that widget will trigger a script rerun whenever a user changes its value. For widgets with keyed input (st.number_input,st.text_input,st.text_area), a new value triggers a rerun when the user clicks or tabs out of the widget. A user can also submit a change by pressingEnterwhile their cursor is active in the widget.

`st.number_input`

`st.text_input`

`st.text_area`

`Enter`

On the other hand if a widget is inside of a form, the script will not rerun when a user clicks or tabs out of that widget. For widgets inside a form, the script will rerun when the form is submitted and all widgets within the form will send their updated values to the Python backend.

A user can submit a form usingEnteron their keyboard if their cursor active in a widget that accepts keyed input. Withinst.number_inputandst.text_inputa user pressesEnterto submit the form. Withinst.text_areaa user pressesCtrl+Enter/⌘+Enterto submit the form.

`st.number_input`

`st.text_input`

`st.text_area`

## Widget values

Before a form is submitted, all widgets within that form will have default values, just like widgets outside of a form have default values.

`import streamlit as st

with st.form("my_form"):
   st.write("Inside the form")
   my_number = st.slider('Pick a number', 1, 10)
   my_color = st.selectbox('Pick a color', ['red','orange','green','blue','violet'])
   st.form_submit_button('Submit my picks')

# This is outside the form
st.write(my_number)
st.write(my_color)`

## Forms are containers

Whenst.formis called, a container is created on the frontend. You can write to that container like you do with othercontainer elements. That is, you can use Python'swithstatement as shown in the example above, or you can assign the form container to a variable and call methods on it directly. Additionally, you can placest.form_submit_buttonanywhere in the form container.

`st.form`

`with`

`st.form_submit_button`

`import streamlit as st

animal = st.form('my_animal')

# This is writing directly to the main body. Since the form container is
# defined above, this will appear below everything written in the form.
sound = st.selectbox('Sounds like', ['meow','woof','squeak','tweet'])

# These methods called on the form container, so they appear inside the form.
submit = animal.form_submit_button(f'Say it with {sound}!')
sentence = animal.text_input('Your sentence:', 'Where\'s the tuna?')
say_it = sentence.rstrip('.,!?') + f', {sound}!'
if submit:
    animal.subheader(say_it)
else:
    animal.subheader('&nbsp;')`

## Processing form submissions

The purpose of a form is to override the default behavior of Streamlit which reruns a script as soon as the user makes a change. For widgets outside of a form, the logical flow is:

- The user changes a widget's value on the frontend.
- The widget's value inst.session_stateand in the Python backend (server) is updated.
- The script rerun begins.
- If the widget has a callback, it is executed as a prefix to the page rerun.
- When the updated widget's function is executed during the rerun, it outputs the new value.
`st.session_state`

For widgets inside a form, any changes made by a user (step 1) do not get passed to the Python backend (step 2) until the form is submitted. Furthermore, the only widget inside a form that can have a callback function is thest.form_submit_button. If you need to execute a process using newly submitted values, you have three major patterns for doing so.

`st.form_submit_button`

### Execute the process after the form

If you need to execute a one-time process as a result of a form submission, you can condition that process on thest.form_submit_buttonand execute it after the form. If you need results from your process to display above the form, you can use containers to control where the form displays relative to your output.

`st.form_submit_button`

`import streamlit as st

col1,col2 = st.columns([1,2])
col1.title('Sum:')

with st.form('addition'):
    a = st.number_input('a')
    b = st.number_input('b')
    submit = st.form_submit_button('add')

if submit:
    col2.title(f'{a+b:.2f}')`

### Use a callback with session state

You can use a callback to execute a process as a prefix to the script rerunning.

#### Important

When processing newly updated values within a callback, do not pass those values to the callback directly through theargsorkwargsparameters. You need to assign a key to any widget whose value you use within the callback. If you look up the value of that widget fromst.session_statewithin the body of the callback, you will be able to access the newly submitted value. See the example below.

`args`

`kwargs`

`st.session_state`

`import streamlit as st

if 'sum' not in st.session_state:
    st.session_state.sum = ''

def sum():
    result = st.session_state.a + st.session_state.b
    st.session_state.sum = result

col1,col2 = st.columns(2)
col1.title('Sum:')
if isinstance(st.session_state.sum, float):
    col2.title(f'{st.session_state.sum:.2f}')

with st.form('addition'):
    st.number_input('a', key = 'a')
    st.number_input('b', key = 'b')
    st.form_submit_button('add', on_click=sum)`

### Usest.rerun

`st.rerun`

If your process affects content above your form, another alternative is using an extra rerun. This can be less resource-efficient though, and may be less desirable that the above options.

`import streamlit as st

if 'sum' not in st.session_state:
    st.session_state.sum = ''

col1,col2 = st.columns(2)
col1.title('Sum:')
if isinstance(st.session_state.sum, float):
    col2.title(f'{st.session_state.sum:.2f}')

with st.form('addition'):
    a = st.number_input('a')
    b = st.number_input('b')
    submit = st.form_submit_button('add')

# The value of st.session_state.sum is updated at the end of the script rerun,
# so the displayed value at the top in col2 does not show the new sum. Trigger
# a second rerun when the form is submitted to update the value above.
st.session_state.sum = a + b
if submit:
    st.rerun()`

## Limitations

- Every form must contain ast.form_submit_button.
- st.buttonandst.download_buttoncannot be added to a form.
- st.formcannot be embedded inside anotherst.form.
- Callback functions can only be assigned tost.form_submit_buttonwithin a form; no other widgets in a form can have a callback.
- Interdependent widgets within a form are unlikely to be particularly useful. If you passwidget1's value intowidget2when they are both inside a form, thenwidget2will only update when the form is submitted.
`st.form_submit_button`

`st.button`

`st.download_button`

`st.form`

`st.form`

`st.form_submit_button`

`widget1`

`widget2`

`widget2`

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
