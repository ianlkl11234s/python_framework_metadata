---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/connections/st.connection
date: 2025-04-27 12:50:50
---

## st.connection

Create a new connection to a data store or API, or return an existing one.

Configuration options, credentials, and secrets for connections are
combined from the following sources:

- The keyword arguments passed to this command.
- The app'ssecrets.tomlfiles.
- Any connection-specific configuration files.
The connection returned fromst.connectionis internally cached withst.cache_resourceand is therefore shared between sessions.

st.connection(name, type=None, max_entries=None, ttl=None, **kwargs)

name(str)

The connection name used for secrets lookup insecrets.toml.
Streamlit uses secrets under[connections.<name>]for the
connection.typewill be inferred ifnameis one of the
following:"snowflake","snowpark", or"sql".

type(str, connection class, or None)

The type of connection to create. This can be one of the following:

- None(default): Streamlit will infer the connection type fromname. If the type is not inferrable fromname, the type must
be specified insecrets.tomlinstead.
- "snowflake": Streamlit will initialize a connection withSnowflakeConnection.
- "snowpark": Streamlit will initialize a connection withSnowparkConnection. This is deprecated.
- "sql": Streamlit will initialize a connection withSQLConnection.
- A string path to an importable class: This must be a dot-separated
module path ending in the importable class. Streamlit will import the
class and initialize a connection with it. The class must extendst.connections.BaseConnection.
- An imported class reference: Streamlit will initialize a connection
with the referenced class, which must extendst.connections.BaseConnection.
max_entries(int or None)

The maximum number of connections to keep in the cache.
If this isNone(default), the cache is unbounded. Otherwise, when
a new entry is added to a full cache, the oldest cached entry is
removed.

ttl(float, timedelta, or None)

The maximum number of seconds to keep results in the cache.
If this isNone(default), cached results do not expire with time.

**kwargs(any)

Connection-specific keyword arguments that are passed to the
connection's._connect()method.**kwargsare typically
combined with (and take precendence over) key-value pairs insecrets.toml. To learn more, see the specific connection's
documentation.

(Subclass of BaseConnection)

An initialized connection object of the specifiedtype.

#### Examples

Example 1: Inferred connection type

The easiest way to create a first-party (SQL, Snowflake, or Snowpark) connection is
to use their default names and define corresponding sections in yoursecrets.tomlfile. The following example creates a"sql"-type connection.

.streamlit/secrets.toml:

```python

[connections.sql]
dialect = "xxx"
host = "xxx"
username = "xxx"
password = "xxx"

```

Your app code:

```python

import streamlit as st
conn = st.connection("sql")

```

Example 2: Named connections

Creating a connection with a custom name requires you to explicitly
specify the type. Iftypeis not passed as a keyword argument, it must
be set in the appropriate section ofsecrets.toml. The following
example creates two"sql"-type connections, each with their own
custom name. The first definestypein thest.connectioncommand;
the second definestypeinsecrets.toml.

.streamlit/secrets.toml:

```python

[connections.first_connection]
dialect = "xxx"
host = "xxx"
username = "xxx"
password = "xxx"

[connections.second_connection]
type = "sql"
dialect = "yyy"
host = "yyy"
username = "yyy"
password = "yyy"

```

Your app code:

```python

import streamlit as st
conn1 = st.connection("first_connection", type="sql")
conn2 = st.connection("second_connection")

```

Example 3: Using a path to the connection class

Passing the full module path to the connection class can be useful,
especially when working with a custom connection. Although this is not the
typical way to create first party connections, the following example
creates the same type of connection as one withtype="sql". Note thattypeis a string path.

.streamlit/secrets.toml:

```python

[connections.my_sql_connection]
url = "xxx+xxx://xxx:xxx@xxx:xxx/xxx"

```

Your app code:

```python

import streamlit as st
conn = st.connection(
    "my_sql_connection", type="streamlit.connections.SQLConnection"
)

```

Example 4: Importing the connection class

You can pass the connection class directly to thest.connectioncommand. Doing so allows static type checking tools such asmypyto
infer the exact return type ofst.connection. The following example
creates the same connection as in Example 3.

.streamlit/secrets.toml:

```python

[connections.my_sql_connection]
url = "xxx+xxx://xxx:xxx@xxx:xxx/xxx"

```

Your app code:

```python

import streamlit as st
from streamlit.connections import SQLConnection
conn = st.connection("my_sql_connection", type=SQLConnection)

```

For a comprehensive overview of this feature, check out this video tutorial by Joshua Carroll, Streamlit's Product Manager for Developer Experience. You'll learn about the feature's utility in creating and managing data connections within your apps by using real-world examples.

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
