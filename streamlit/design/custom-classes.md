---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/concepts/design/custom-classes
date: 2025-04-27 12:48:24
---

# Using custom Python classes in your Streamlit app

If you are building a complex Streamlit app or working with existing code, you may have custom Python classes defined in your script. Common examples include the following:

- Defining a@dataclassto store related data within your app.
- Defining anEnumclass to represent a fixed set of options or values.
- Defining custom interfaces to external services or databases not covered byst.connection.
`@dataclass`

`Enum`

`st.connection`

Because Streamlit reruns your script after every user interaction, custom classes may be redefined multiple times within the same Streamlit session. This may result in unwanted effects, especially with class and instance comparisons. Read on to understand this common pitfall and how to avoid it.

We begin by covering some general-purpose patterns you can use for different types of custom classes, and follow with a few more technical details explaining why this matters. Finally, we go into more detail aboutUsingEnumclassesspecifically, and describe a configuration option which can make them more convenient.

`Enum`

## Patterns to define your custom classes

### Pattern 1: Define your class in a separate module

This is the recommended, general solution. If possible, move class definitions into their own module file and import them into your app script. As long as you are not editing the files that define your app, Streamlit will not re-import those classes with each rerun. Therefore, if a class is defined in an external file and imported into your script, the class will not be redefined during the session, unless you are actively editing your app.

#### Example: Move your class definition

Try running the following Streamlit app whereMyClassis defined within the page's script.isinstance()will returnTrueon the first script run then returnFalseon each rerun thereafter.

`MyClass`

`isinstance()`

`True`

`False`

`# app.py
import streamlit as st

# MyClass gets redefined every time app.py reruns
class MyClass:
    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2

if "my_instance" not in st.session_state:
  st.session_state.my_instance = MyClass("foo", "bar")

# Displays True on the first run then False on every rerun
st.write(isinstance(st.session_state.my_instance, MyClass))

st.button("Rerun")`

If you move the class definition out ofapp.pyinto another file, you can makeisinstance()consistently returnTrue. Consider the following file structure:

`app.py`

`isinstance()`

`True`

`myproject/
├── my_class.py
└── app.py`

`# my_class.py
class MyClass:
    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2`

`# app.py
import streamlit as st
from my_class import MyClass # MyClass doesn't get redefined with each rerun

if "my_instance" not in st.session_state:
  st.session_state.my_instance = MyClass("foo", "bar")

# Displays True on every rerun
st.write(isinstance(st.session_state.my_instance, MyClass))

st.button("Rerun")`

Streamlit only reloads code in imported modules when it detects the code has changed. Thus, if you are actively editing your app code, you may need to start a new session or restart your Streamlit server to avoid an undesirable class redefinition.

### Pattern 2: Force your class to compare internal values

For classes that store data (likedataclasses), you may be more interested in comparing the internally stored values rather than the class itself. If you define a custom__eq__method, you can force comparisons to be made on the internally stored values.

`__eq__`

#### Example: Define__eq__

`__eq__`

Try running the following Streamlit app and observe how the comparison isTrueon the first run thenFalseon every rerun thereafter.

`True`

`False`

`import streamlit as st
from dataclasses import dataclass

@dataclass
class MyDataclass:
    var1: int
    var2: float

if "my_dataclass" not in st.session_state:
    st.session_state.my_dataclass = MyDataclass(1, 5.5)

# Displays True on the first run the False on every rerun
st.session_state.my_dataclass == MyDataclass(1, 5.5)

st.button("Rerun")`

SinceMyDataclassgets redefined with each rerun, the instance stored in Session State will not be equal to any instance defined in a later script run. You can fix this by forcing a comparison of internal values as follows:

`MyDataclass`

`import streamlit as st
from dataclasses import dataclass

@dataclass
class MyDataclass:
    var1: int
    var2: float

    def __eq__(self, other):
        # An instance of MyDataclass is equal to another object if the object
        # contains the same fields with the same values
        return (self.var1, self.var2) == (other.var1, other.var2)

if "my_dataclass" not in st.session_state:
    st.session_state.my_dataclass = MyDataclass(1, 5.5)

# Displays True on every rerun
st.session_state.my_dataclass == MyDataclass(1, 5.5)

st.button("Rerun")`

The default Python__eq__implementation for a regular class or@dataclassdepends on the in-memory ID of the class or class instance. To avoid problems in Streamlit, your custom__eq__method should not depend thetype()ofselfandother.

`__eq__`

`@dataclass`

`__eq__`

`type()`

`self`

`other`

### Pattern 3: Store your class as serialized data

Another option for classes that store data is to define serialization and deserialization methods liketo_strandfrom_strfor your class. You can use these to store class instance data inst.session_staterather than storing the class instance itself. Similar to pattern 2, this is a way to force comparison of the internal data and bypass the changing in-memory IDs.

`to_str`

`from_str`

`st.session_state`

#### Example: Save your class instance as a string

Using the same example from pattern 2, this can be done as follows:

`import streamlit as st
from dataclasses import dataclass

@dataclass
class MyDataclass:
    var1: int
    var2: float

    def to_str(self):
        return f"{self.var1},{self.var2}"

    @classmethod
    def from_str(cls, serial_str):
        values = serial_str.split(",")
        var1 = int(values[0])
        var2 = float(values[1])
        return cls(var1, var2)

if "my_dataclass" not in st.session_state:
    st.session_state.my_dataclass = MyDataclass(1, 5.5).to_str()

# Displays True on every rerun
MyDataclass.from_str(st.session_state.my_dataclass) == MyDataclass(1, 5.5)

st.button("Rerun")`

### Pattern 4: Use caching to preserve your class

For classes that are used as resources (database connections, state managers, APIs), consider using the cached singleton pattern. Use@st.cache_resourceto decorate a@staticmethodof your class to generate a single, cached instance of the class. For example:

`@st.cache_resource`

`@staticmethod`

`import streamlit as st

class MyResource:
    def __init__(self, api_url: str):
        self._url = api_url

    @st.cache_resource(ttl=300)
    @staticmethod
    def get_resource_manager(api_url: str):
        return MyResource(api_url)

# This is cached until Session State is cleared or 5 minutes has elapsed.
resource_manager = MyResource.get_resource_manager("http://example.com/api/")`

When you use one of Streamlit's caching decorators on a function, Streamlit doesn't use the function object to look up cached values. Instead, Streamlit's caching decorators index return values using the function's qualified name and module. So, even though Streamlit redefinesMyResourcewith each script run,st.cache_resourceis unaffected by this.get_resource_manager()will return its cached value with each rerun, until the value expires.

`MyResource`

`st.cache_resource`

`get_resource_manager()`

## Understanding how Python defines and compares classes

So what's really happening here? We'll consider a simple example to illustrate why this is a pitfall. Feel free to skip this section if you don't want to deal more details. You can jump ahead to learn aboutUsingEnumclasses.

`Enum`

### Example: What happens when you define the same class twice?

Set aside Streamlit for a moment and think about this simple Python script:

`from dataclasses import dataclass

@dataclass
class Student:
    student_id: int
    name: str

Marshall_A = Student(1, "Marshall")
Marshall_B = Student(1, "Marshall")

# This is True (because a dataclass will compare two of its instances by value)
Marshall_A == Marshall_B

# Redefine the class
@dataclass
class Student:
    student_id: int
    name: str

Marshall_C = Student(1, "Marshall")

# This is False
Marshall_A == Marshall_C`

In this example, the dataclassStudentis defined twice. All three Marshalls have the same internal values. If you compareMarshall_AandMarshall_Bthey will be equal because they were both created from the first definition ofStudent. However, if you compareMarshall_AandMarshall_Cthey will not be equal becauseMarshall_Cwas created from theseconddefinition ofStudent. Even though bothStudentdataclasses are defined exactly the same, they have different in-memory IDs and are therefore different.

`Student`

`Marshall_A`

`Marshall_B`

`Student`

`Marshall_A`

`Marshall_C`

`Marshall_C`

`Student`

`Student`

### What's happening in Streamlit?

In Streamlit, you probably don't have the same class written twice in your page script. However, the rerun logic of Streamlit creates the same effect. Let's use the above example for an analogy. If you define a class in one script run and save an instance in Session State, then a later rerun will redefine the class and you may end up comparing aMashall_Cin your rerun to aMarshall_Ain Session State. Since widgets rely on Session State under the hood, this is where things can get confusing.

`Mashall_C`

`Marshall_A`

## How Streamlit widgets store options

Several Streamlit UI elements, such asst.selectboxorst.radio, accept multiple-choice options via anoptionsargument. The user of your application can typically select one or more of these options. The selected value is returned by the widget function. For example:

`st.selectbox`

`st.radio`

`options`

`number = st.selectbox("Pick a number, any number", options=[1, 2, 3])
# number == whatever value the user has selected from the UI.`

When you call a function likest.selectboxand pass anIterabletooptions, theIterableand current selection are saved into a hidden portion ofSession Statecalled the Widget Metadata.

`st.selectbox`

`Iterable`

`options`

`Iterable`

When the user of your application interacts with thest.selectboxwidget, the broswer sends the index of their selection to your Streamlit server. This index is used to determine which values from the originaloptionslist,saved in the Widget Metadata from the previous page execution, are returned to your application.

`st.selectbox`

`options`

The key detail is that the value returned byst.selectbox(or similar widget function) is from anIterablesaved in Session State during apreviousexecution of the page, NOT the values passed tooptionson thecurrentexecution. There are a number of architectural reasons why Streamlit is designed this way, which we won't go into here. However,thisis how we end up comparing instances of different classes when we think we are comparing instances of the same class.

`st.selectbox`

`Iterable`

`options`

### A pathological example

The above explanation might be a bit confusing, so here's a pathological example to illustrate the idea.

`import streamlit as st
from dataclasses import dataclass

@dataclass
class Student:
    student_id: int
    name: str

Marshall_A = Student(1, "Marshall")
if "B" not in st.session_state:
    st.session_state.B = Student(1, "Marshall")
Marshall_B = st.session_state.B

options = [Marshall_A,Marshall_B]
selected = st.selectbox("Pick", options)

# This comparison does not return expected results:
selected == Marshall_A
# This comparison evaluates as expected:
selected == Marshall_B`

As a final note, we used@dataclassin the example for this section to illustrate a point, but in fact it is possible to encounter these same problems with classes, in general. Any class which checks class identity inside of a comparison operator—such as__eq__or__gt__—can exhibit these issues.

`@dataclass`

`__eq__`

`__gt__`

## UsingEnumclasses in Streamlit

`Enum`

TheEnumclass from the Python standard library is a powerful way to define custom symbolic names that can be used as options forst.multiselectorst.selectboxin place ofstrvalues.

`Enum`

`st.multiselect`

`st.selectbox`

`str`

For example, you might add the following to your streamlit page:

`from enum import Enum
import streamlit as st

# class syntax
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

selected_colors = set(st.multiselect("Pick colors", options=Color))

if selected_colors == {Color.RED, Color.GREEN}:
    st.write("Hooray, you found the color YELLOW!")`

If you're using the latest version of Streamlit, this Streamlit page will work as it appears it should. When a user picks bothColor.REDandColor.GREEN, they are shown the special message.

`Color.RED`

`Color.GREEN`

However, if you've read the rest of this page you might notice something tricky going on. Specifically, theEnumclassColorgets redefined every time this script is run. In Python, if you define twoEnumclasses with the same class name, members, and values, the classes and their members are still considered unique from each other. Thisshouldcause the aboveifcondition to always evaluate toFalse. In any script rerun, theColorvalues returned byst.multiselectwould be of a different class than theColordefined in that script run.

`Enum`

`Color`

`Enum`

`if`

`False`

`Color`

`st.multiselect`

`Color`

If you run the snippet above with Streamlit version 1.28.0 or less, you will not be able see the special message. Thankfully, as of version 1.29.0, Streamlit introduced a configuration option to greatly simplify the problem. That's where the enabled-by-defaultenumCoercionconfiguration option comes in.

`enumCoercion`

### Understanding theenumCoercionconfiguration option

`enumCoercion`

WhenenumCoercionis enabled, Streamlit tries to recognize when you are using an element likest.multiselectorst.selectboxwith a set ofEnummembers as options.

`enumCoercion`

`st.multiselect`

`st.selectbox`

`Enum`

If Streamlit detects this, it will convert the widget's returned values to members of theEnumclass defined in the latest script run. This is something we call automaticEnumcoercion.

`Enum`

`Enum`

This behavior isconfigurablevia theenumCoercionsetting in your Streamlitconfig.tomlfile. It is enabled by default, and may be disabled or set to a stricter set of matching criteria.

`enumCoercion`

`config.toml`

If you find that you still encounter issues withenumCoercionenabled, consider using thecustom class patternsdescribed above, such as moving yourEnumclass definition to a separate module file.

`enumCoercion`

`Enum`

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
