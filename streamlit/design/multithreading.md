---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/concepts/design/multithreading
date: 2025-04-27 12:48:21
---

# Multithreading in Streamlit

Multithreading is a type of concurrency, which improves the efficiency of computer programs. It's a way for processors to multitask. Streamlit uses threads within its architecture, which can make it difficult for app developers to include their own multithreaded processes. Streamlit does not officially support multithreading in app code, but this guide provides information on how it can be accomplished.

## Prerequisites

- You should have a basic understanding of Streamlit'sarchitecture.
## When to use multithreading

Multithreading is just one type of concurrency. Multiprocessing and coroutines are other forms of concurrency. You need to understand how your code is bottlenecked to choose the correct kind of concurrency.

Multiprocessing is inherently parallel, meaning that resources are split and multiple tasks are performed simultaneously. Therefore, multiprocessing is helpful with compute-bound operations. In contrast, multithreading and coroutines are not inherently parallel and instead allow resource switching. This makes them good choices when your code is stuckwaitingfor something, like an IO operation. AsyncIO uses coroutines and may be preferable with very slow IO operations. Threading may be preferable with faster IO operations. For a helpful guide to using AsyncIO with Streamlit, see thisMedium article by Sehmi-Conscious Thoughts.

Don't forget that Streamlit hasfragmentsandcaching, too! Use caching to avoid unnecessarily repeating computations or IO operations. Use fragments to isolate a bit of code you want to update separately from the rest of the app. You can set fragments to rerun at a specified interval, so they can be used to stream updates to a chart or table.

## Threads created by Streamlit

Streamlit creates two types of threads in Python:

- Theserver threadruns the Tornado web (HTTP + WebSocket) server.
- Ascript threadruns page code — one thread for each script run in a session.
When a user connects to your app, this creates a new session and runs a script thread to initialize the app for that user. As the script thread runs, it renders elements in the user's browser tab and reports state back to the server. When the user interacts with the app, another script thread runs, re-rendering the elements in the browser tab and updating state on the server.

This is a simplifed illustration to show how Streamlit works:

## streamlit.errors.NoSessionContext

`streamlit.errors.NoSessionContext`

Many Streamlit commands, includingst.session_state, expect to be called from a script thread. When Streamlit is running as expected, such commands use theScriptRunContextattached to the script thread to ensure they work within the intended session and update the correct user's view. When those Streamlit commands can't find anyScriptRunContext, they raise astreamlit.errors.NoSessionContextexception. Depending on your logger settings, you may also see a console message identifying a thread by name and warning, "missing ScriptRunContext!"

`st.session_state`

`ScriptRunContext`

`ScriptRunContext`

`streamlit.errors.NoSessionContext`

## Creating custom threads

When you work with IO-heavy operations like remote query or data loading, you may need to mitigate delays. A general programming strategy is to create threads and let them work concurrently. However, if you do this in a Streamlit app, these custom threads may have difficulty interacting with your Streamlit server.

This section introduces two patterns to let you create custom threads in your Streamlit app. These are only patterns to provide a starting point rather than complete solutions.

### Option 1: Do not use Streamlit commands within a custom thread

If you don't call Streamlit commands from a custom thread, you can avoid the problem entirely. Luckily Python threading provides ways to start a thread and collect its result from another thread.

In the following example, five custom threads are created from the script thread. After the threads are finished running, their results are displayed in the app.

`import streamlit as st
import time
from threading import Thread


class WorkerThread(Thread):
    def __init__(self, delay):
        super().__init__()
        self.delay = delay
        self.return_value = None

    def run(self):
        start_time = time.time()
        time.sleep(self.delay)
        end_time = time.time()
        self.return_value = f"start: {start_time}, end: {end_time}"


delays = [5, 4, 3, 2, 1]
threads = [WorkerThread(delay) for delay in delays]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
for i, thread in enumerate(threads):
    st.header(f"Thread {i}")
    st.write(thread.return_value)

st.button("Rerun")`

If you want to display results in your app as various custom threads finish running, use containers. In the following example, five custom threads are created similarly to the previous example. However, five containers are initialized before running the custom threads and awhileloop is used to display results as they become available. Since the Streamlitwritecommand is called outside of the custom threads, this does not raise an exception.

`while`

`write`

`import streamlit as st
import time
from threading import Thread


class WorkerThread(Thread):
    def __init__(self, delay):
        super().__init__()
        self.delay = delay
        self.return_value = None

    def run(self):
        start_time = time.time()
        time.sleep(self.delay)
        end_time = time.time()
        self.return_value = f"start: {start_time}, end: {end_time}"


delays = [5, 4, 3, 2, 1]
result_containers = []
for i, delay in enumerate(delays):
    st.header(f"Thread {i}")
    result_containers.append(st.container())

threads = [WorkerThread(delay) for delay in delays]
for thread in threads:
    thread.start()
thread_lives = [True] * len(threads)

while any(thread_lives):
    for i, thread in enumerate(threads):
        if thread_lives[i] and not thread.is_alive():
            result_containers[i].write(thread.return_value)
            thread_lives[i] = False
    time.sleep(0.5)

for thread in threads:
    thread.join()

st.button("Rerun")`

### Option 2: ExposeScriptRunContextto the thread

`ScriptRunContext`

If you want to call Streamlit commands from within your custom threads, you must attach the correctScriptRunContextto the thread.

`ScriptRunContext`

#### Warning

- This is not officially supported and may change in a future version of Streamlit.
- This may not work with all Streamlit commands.
- Ensure custom threads do not outlive the script thread owning theScriptRunContext. Leaking ofScriptRunContextmay cause security vulnerabilities, fatal errors, or unexpected behavior.
`ScriptRunContext`

`ScriptRunContext`

In the following example, a custom thread withScriptRunContextattached can callst.writewithout a warning.

`ScriptRunContext`

`st.write`

`import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx
import time
from threading import Thread


class WorkerThread(Thread):
    def __init__(self, delay, target):
        super().__init__()
        self.delay = delay
        self.target = target

    def run(self):
        # runs in custom thread, but can call Streamlit APIs
        start_time = time.time()
        time.sleep(self.delay)
        end_time = time.time()
        self.target.write(f"start: {start_time}, end: {end_time}")


delays = [5, 4, 3, 2, 1]
result_containers = []
for i, delay in enumerate(delays):
    st.header(f"Thread {i}")
    result_containers.append(st.container())

threads = [
    WorkerThread(delay, container)
    for delay, container in zip(delays, result_containers)
]
for thread in threads:
    add_script_run_ctx(thread, get_script_run_ctx())
    thread.start()

for thread in threads:
    thread.join()

st.button("Rerun")`

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
