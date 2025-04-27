---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/concepts/design/timezone-handling
date: 2025-04-27 12:48:26
---

# Working with timezones

In general, working with timezones can be tricky. Your Streamlit app users are not necessarily in the same timezone as the server running your app. It is especially true of public apps, where anyone in the world (in any timezone) can access your app. As such, it is crucial to understand how Streamlit handles timezones, so you can avoid unexpected behavior when displayingdatetimeinformation.

`datetime`

## How Streamlit handles timezones

Streamlit always showsdatetimeinformation on the frontend with the same information as its correspondingdatetimeinstance in the backend. I.e., date or time information does not automatically adjust to the users' timezone. We distinguish between the following two cases:

`datetime`

`datetime`

### datetimeinstance without a timezone (naive)

`datetime`

When you provide adatetimeinstancewithout specifying a timezone, the frontend shows thedatetimeinstance without timezone information. For example (this also applies to other widgets likest.dataframe):

`datetime`

`datetime`

`st.dataframe`

`import streamlit as st
from datetime import datetime

st.write(datetime(2020, 1, 10, 10, 30))
# Outputs: 2020-01-10 10:30:00`

Users of the above app always see the output as2020-01-10 10:30:00.

`2020-01-10 10:30:00`

### datetimeinstance with a timezone

`datetime`

When you provide adatetimeinstanceand specify a timezone, the frontend shows thedatetimeinstance in that same timezone. For example (this also applies to other widgets likest.dataframe):

`datetime`

`datetime`

`st.dataframe`

`import streamlit as st
from datetime import datetime
import pytz

st.write(datetime(2020, 1, 10, 10, 30, tzinfo=pytz.timezone("EST")))
# Outputs: 2020-01-10 10:30:00-05:00`

Users of the above app always see the output as2020-01-10 10:30:00-05:00.

`2020-01-10 10:30:00-05:00`

In both cases, neither the date nor time information automatically adjusts to the users' timezone on the frontend. What users see is identical to the correspondingdatetimeinstance in the backend. It is currently not possible to automatically adjust the date or time information to the timezone of the users viewing the app.

`datetime`

#### Note

The legacy version of thest.dataframehas issues with timezones. We do not plan to roll out additional fixes or enhancements for the legacy dataframe. If you need stable timezone support, please consider switching to the arrow serialization by changing theconfig setting,config.dataFrameSerialization = "arrow".

`st.dataframe`

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
