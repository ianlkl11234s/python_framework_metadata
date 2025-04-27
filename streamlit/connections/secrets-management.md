---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/concepts/connections/secrets-management
date: 2025-04-27 12:48:31
---

# Secrets management

Storing unencrypted secrets in a git repository is a bad practice. For applications that require access to sensitive credentials, the recommended solution is to store those credentials outside the repository - such as using a credentials file not committed to the repository or passing them as environment variables.

Streamlit provides native file-based secrets management to easily store and securely access your secrets in your Streamlit app.

#### Note

Existing secrets management tools, such asdotenv files,AWS credentials files,Google Cloud Secret Manager, orHashicorp Vault, will work fine in Streamlit. We just add native secrets management for times when it's useful.

## How to use secrets management

### Develop locally and set up secrets

Streamlit provides two ways to set up secrets locally usingTOMLformat:

- In aglobal secrets fileat~/.streamlit/secrets.tomlfor macOS/Linux or%userprofile%/.streamlit/secrets.tomlfor Windows:# Everything in this section will be available as an environment variable
db_username = "Jane"
db_password = "mypassword"

# You can also add other sections if you like.
# The contents of sections as shown below will not become environment variables,
# but they'll be easily accessible from within Streamlit anyway as we show
# later in this doc.
[my_other_secrets]
things_i_like = ["Streamlit", "Python"]If you use the global secrets file, you don't have to duplicate secrets across several project-level files if multiple Streamlit apps share the same secrets.
- In aper-project secrets fileat$CWD/.streamlit/secrets.toml, where$CWDis the folder you're running Streamlit from. If both a global secrets file and a per-project secrets file exist,secrets in the per-project file overwrite those defined in the global file.
In aglobal secrets fileat~/.streamlit/secrets.tomlfor macOS/Linux or%userprofile%/.streamlit/secrets.tomlfor Windows:

`~/.streamlit/secrets.toml`

`%userprofile%/.streamlit/secrets.toml`

`# Everything in this section will be available as an environment variable
db_username = "Jane"
db_password = "mypassword"

# You can also add other sections if you like.
# The contents of sections as shown below will not become environment variables,
# but they'll be easily accessible from within Streamlit anyway as we show
# later in this doc.
[my_other_secrets]
things_i_like = ["Streamlit", "Python"]`

If you use the global secrets file, you don't have to duplicate secrets across several project-level files if multiple Streamlit apps share the same secrets.

In aper-project secrets fileat$CWD/.streamlit/secrets.toml, where$CWDis the folder you're running Streamlit from. If both a global secrets file and a per-project secrets file exist,secrets in the per-project file overwrite those defined in the global file.

`$CWD/.streamlit/secrets.toml`

`$CWD`

#### Important

Add this file to your.gitignoreso you don't commit your secrets!

`.gitignore`

### Use secrets in your app

Access your secrets by querying thest.secretsdict, or as environment variables. For example, if you enter the secrets from the section above, the code below shows you how to access them within your Streamlit app.

`st.secrets`

`import streamlit as st

# Everything is accessible via the st.secrets dict:

st.write("DB username:", st.secrets["db_username"])
st.write("DB password:", st.secrets["db_password"])

# And the root-level secrets are also accessible as environment variables:

import os

st.write(
    "Has environment variables been set:",
    os.environ["db_username"] == st.secrets["db_username"],
)`

#### Tip

You can accessst.secretsvia attribute notation (e.g.st.secrets.key), in addition to key notation (e.g.st.secrets["key"]) — likest.session_state.

`st.secrets`

`st.secrets.key`

`st.secrets["key"]`

You can even compactly use TOML sections to pass multiple secrets as a single attribute. Consider the following secrets:

`[db_credentials]
username = "my_username"
password = "my_password"`

Rather than passing each secret as attributes in a function, you can more compactly pass the section to achieve the same result. See the notional code below, which uses the secrets above:

`# Verbose version
my_db.connect(username=st.secrets.db_credentials.username, password=st.secrets.db_credentials.password)

# Far more compact version!
my_db.connect(**st.secrets.db_credentials)`

### Error handling

Here are some common errors you might encounter when using secrets management.

- If a.streamlit/secrets.tomlis createdwhilethe app is running, the server needs to be restarted for changes to be reflected in the app.
- If you try accessing a secret, but nosecrets.tomlfile exists, Streamlit will raise aFileNotFoundErrorexception:
- If you try accessing a secret that doesn't exist, Streamlit will raise aKeyErrorexception:import streamlit as st

st.write(st.secrets["nonexistent_key"])
If a.streamlit/secrets.tomlis createdwhilethe app is running, the server needs to be restarted for changes to be reflected in the app.

`.streamlit/secrets.toml`

If you try accessing a secret, but nosecrets.tomlfile exists, Streamlit will raise aFileNotFoundErrorexception:

`secrets.toml`

`FileNotFoundError`

If you try accessing a secret that doesn't exist, Streamlit will raise aKeyErrorexception:

`KeyError`

`import streamlit as st

st.write(st.secrets["nonexistent_key"])`

### Use secrets on Streamlit Community Cloud

When you deploy your app toStreamlit Community Cloud, you can use the same secrets management workflow as you would locally. However, you'll need to also set up your secrets in the Community Cloud Secrets Management console. Learn how to do so via the Cloud-specificSecrets managementdocumentation.

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
