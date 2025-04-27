---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/api-reference/connections/st.connections.sqlconnection
date: 2025-04-27 12:50:47
---

## st.connections.SQLConnection

A connection to a SQL database using a SQLAlchemy Engine.

Initialize this connection object usingst.connection("sql")orst.connection("<name>",type="sql"). Connection parameters for a
SQLConnection can be specified usingsecrets.tomland/or**kwargs.
Possible connection parameters include:

- urlor keyword arguments forsqlalchemy.engine.URL.create(), exceptdrivername. Usedialectanddriverinstead ofdrivername.
- Keyword arguments forsqlalchemy.create_engine(), including customconnect()arguments used by your specificdialectordriver.
- autocommit. If this isFalse(default), the connection operates
in manual commit (transactional) mode. If this isTrue, the
connection operates in autocommit (non-transactional) mode.
Ifurlexists as a connection parameter, Streamlit will pass it tosqlalchemy.engine.make_url(). Otherwise, Streamlit requires (at a
minimum)dialect,username, andhost. Streamlit will usedialectanddriver(if defined) to derivedrivername, then pass
the relevant connection parameters tosqlalchemy.engine.URL.create().

In addition to the default keyword arguments forsqlalchemy.create_engine(),
your dialect may accept additional keyword arguments. For example, if you
usedialect="snowflake"withSnowflake SQLAlchemy,
you can pass a value forprivate_keyto use key-pair authentication. If
you usedialect="bigquery"withGoogle BigQuery,
you can pass a value forlocation.

SQLConnection provides the.query()convenience method, which can be
used to run simple, read-only queries with both caching and simple error
handling/retries. More complex database interactions can be performed by
using the.sessionproperty to receive a regular SQLAlchemy Session.

Important

SQLAlchemymust be installed
in your environment to use this connection. You must also install your
driver, such aspyodbcorpsycopg2.

st.connections.SQLConnection(connection_name, **kwargs)

connect()

Call.connect()on the underlying SQLAlchemy Engine, returning a new        connection object.

query(sql, *, show_spinner="Running `sql.query(...)`.", ttl=None, index_col=None, chunksize=None, params=None, **kwargs)

Run a read-only query.

reset()

Reset this connection so that it gets reinitialized the next time it's used.

driver

The name of the driver used by the underlying SQLAlchemy Engine.

engine

The underlying SQLAlchemy Engine.

session

Return a SQLAlchemy Session.

#### Examples

Example 1: Configuration with URL

You can configure your SQL connection using Streamlit'sSecrets management.
The following example specifies a SQL connection URL.

.streamlit/secrets.toml:

```python

[connections.sql]
url = "xxx+xxx://xxx:xxx@xxx:xxx/xxx"

```

Your app code:

```python

import streamlit as st

conn = st.connection("sql")
df = conn.query("SELECT * FROM pet_owners")
st.dataframe(df)

```

Example 2: Configuration with dialect, host, and username

If you do not specifyurl, you must at least specifydialect,host, andusernameinstead. The following example also includespassword.

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
df = conn.query("SELECT * FROM pet_owners")
st.dataframe(df)

```

Example 3: Configuration with keyword arguments

You can configure your SQL connection with keyword arguments (with or
withoutsecrets.toml). For example, if you use Microsoft Entra ID with
a Microsoft Azure SQL server, you can quickly set up a local connection for
development usinginteractive authentication.

This example requires theMicrosoft ODBC Driver for SQL ServerforWindowsin addition to thesqlalchemyandpyodbcpackages for
Python.

```python

import streamlit as st

conn = st.connection(
    "sql",
    dialect="mssql",
    driver="pyodbc",
    host="xxx.database.windows.net",
    database="xxx",
    username="xxx",
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "authentication": "ActiveDirectoryInteractive",
        "encrypt": "yes",
    },
)

df = conn.query("SELECT * FROM pet_owners")
st.dataframe(df)

```

## SQLConnection.connect

Call.connect()on the underlying SQLAlchemy Engine, returning a new        connection object.

Calling this method is equivalent to callingself._instance.connect().

NOTE: This method should not be confused with the internal_connectmethod used
to implement a Streamlit Connection.

SQLConnection.connect()

(sqlalchemy.engine.Connection)

A new SQLAlchemy connection object.

## SQLConnection.query

Run a read-only query.

This method implements query result caching and simple error
handling/retries. The caching behavior is identical to that of using@st.cache_data.

Note

Queries that are run without a specified ttl are cached indefinitely.

All keyword arguments passed to this function are passed down topandas.read_sql, exceptttl.

SQLConnection.query(sql, *, show_spinner="Running `sql.query(...)`.", ttl=None, index_col=None, chunksize=None, params=None, **kwargs)

sql(str)

The read-only SQL query to execute.

show_spinner(boolean or string)

Enable the spinner. The default is to show a spinner when there is a
"cache miss" and the cached resource is being created. If a string, the value
of the show_spinner param will be used for the spinner text.

ttl(float, int, timedelta or None)

The maximum number of seconds to keep results in the cache, or
None if cached results should not expire. The default is None.

index_col(str, list of str, or None)

Column(s) to set as index(MultiIndex). Default is None.

chunksize(int or None)

If specified, return an iterator where chunksize is the number of
rows to include in each chunk. Default is None.

params(list, tuple, dict or None)

List of parameters to pass to the execute method. The syntax used to pass
parameters is database driver dependent. Check your database driver
documentation for which of the five syntax styles, described inPEP 249
paramstyle, is supported.
Default is None.

**kwargs(dict)

Additional keyword arguments are passed topandas.read_sql.

(pandas.DataFrame)

The result of running the query, formatted as a pandas DataFrame.

#### Example

```python

import streamlit as st

conn = st.connection("sql")
df = conn.query(
    "SELECT * FROM pet_owners WHERE owner = :owner",
    ttl=3600,
    params={"owner": "barbara"},
)
st.dataframe(df)

```

## SQLConnection.reset

Reset this connection so that it gets reinitialized the next time it's used.

This method can be useful when a connection has become stale, an auth token has
expired, or in similar scenarios where a broken connection might be fixed by
reinitializing it. Note that some connection methods may already usereset()in their error handling code.

SQLConnection.reset()

(None)

No description

#### Example

```python

import streamlit as st

conn = st.connection("my_conn")

# Reset the connection before using it if it isn't healthy
# Note: is_healthy() isn't a real method and is just shown for example here.
if not conn.is_healthy():
    conn.reset()

# Do stuff with conn...

```

## SQLConnection.driver

The name of the driver used by the underlying SQLAlchemy Engine.

This is equivalent to accessingself._instance.driver.

SQLConnection.driver

(str)

The name of the driver. For example,"pyodbc"or"psycopg2".

## SQLConnection.engine

The underlying SQLAlchemy Engine.

This is equivalent to accessingself._instance.

SQLConnection.engine

(sqlalchemy.engine.base.Engine)

The underlying SQLAlchemy Engine.

## SQLConnection.session

Return a SQLAlchemy Session.

Users of this connection should use the contextmanager pattern for writes,
transactions, and anything more complex than simple read queries.

See the usage example below, which assumes we have a tablenumberswith a
single integer columnval. TheSQLAlchemydocs also contain
much more information on the usage of sessions.

SQLConnection.session

(sqlalchemy.orm.Session)

A SQLAlchemy Session.

#### Example

```python

import streamlit as st
conn = st.connection("sql")
n = st.slider("Pick a number")
if st.button("Add the number!"):
    with conn.session as session:
        session.execute("INSERT INTO numbers (val) VALUES (:n);", {"n": n})
        session.commit()

```

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
