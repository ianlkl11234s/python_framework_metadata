---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/concepts/connections/authentication
date: 2025-04-27 12:48:33
---

# User authentication and information

Personalizing your app for your users is a great way to make your app more engaging.

User authentication and personalization unlocks a plethora of use cases for developers, including controls for admins, a personalized stock ticker, or a chatbot app with a saved history between sessions.

Before reading this guide, you should have a basic understanding ofsecrets management.

## OpenID Connect

Streamlit supports user authentication with OpenID Connect (OIDC), which is an authentication protocol built on top of OAuth 2.0. OIDC supports authentication, but not authorization: that is, OIDC connections tell youwhoa user is (authentication), but don't give you the authority toimpersonatethem (authorization). If you need to connect with a generic OAuth 2.0 provider or have your app to act on behalf of a user, consider using or creating a custom component.

Some popular OIDC providers are:

- Google Identity
- Microsoft Entra ID
- Okta
- Auth0
## st.login(),st.experimental_user, andst.logout()

`st.login()`

`st.experimental_user`

`st.logout()`

There are three commands involved with user authentication:

- st.login()redirects the user to your identity provider. After they log in, Streamlit stores an identity cookie and then redirects them to the homepage of your app in a new session.
- st.experimental_useris a dict-like object for accessing user information. It has a persistent attribute,.is_logged_in, which you can check for the user's login status. When they are logged in, other attributes are available per your identity provider's configuration.
- st.logout()removes the identity cookie from the user's browser and redirects them to the homepage of your app in a new session.
`st.login()`

`st.experimental_user`

`.is_logged_in`

`st.logout()`

## User cookies and logging out

Streamlit checks for the identity cookie at the beginning of each new session. If a user logs in to your app in one tab and then opens a new tab, they will automatically be logged in to your app in the new tab. When you callst.logout()in a user session, Streamlit removes the identity cookie and starts a new session. This logs the user out from the current session. However, if they were logged in to other sessions already, they will remain logged in within those sessions. The information inst.experimental_useris updated at the beginning of a session (which is whyst.login()andst.logout()both start new sessions after saving or deleting the identity cookie).

`st.logout()`

`st.experimental_user`

`st.login()`

`st.logout()`

If a user closes your app without logging out, the identity cookie will expire after 30 days. This expiration time is not configurable and is not tied to any expiration time that may be returned in your user's identity token. If you need to prevent persistent authentication in your app, check the expiration information returned by the identity provider inst.experimental_userand manually callst.logout()when needed.

`st.experimental_user`

`st.logout()`

Streamlit does not modify or delete any cookies saved directly by your identity provider. For example, if you use Google as your identity provider and a user logs in to your app with Google, they will remain logged in to their Google account after they log out of your app withst.logout().

`st.logout()`

## Setting up an identity provider

In order to use an identity provider, you must first configure your identity provider through an admin account. This typically involves setting up a client or application within the identity provider's system. Follow the documentation for your identity provider. As a general overview, an identity-provider client typically does the following:

- Manages the list of your users.
- Optional: Allows users to add themselves to your user list.
- Declares the set of attributes passed from each user account to the client (which is then passed to your Streamlit app).
- Only allows authentication requests to come from your Streamlit app.
- Redirects users back to your Streamlit app after they authenticate.
To configure your app, you'll need the following:

- Your app's URL
For example, usehttp://localhost:8501for most local development cases.
- A redirect URL, which is your app's URL with the pathnameoauth2callbackFor example,http://localhost:8501/oauth2callbackfor most local development cases.
- A cookie secret, which should be a strong, randomly generated string
`http://localhost:8501`

`oauth2callback`

`http://localhost:8501/oauth2callback`

After you use this information to configure your identity-provider client, you'll receive the following information from your identity provider:

- Client ID
- Client secret
- Server metadata URL
Examples for popular OIDC provider configurations are listed in the API reference forst.login().

`st.login()`

## Configure your OIDC connection in Streamlit

After you've configured your identity-provider client, you'll need to configure your Streamlit app, too.st.login()uses your app'ssecrets.tomlfile to configure your connection, similar to howst.connection()works.

`st.login()`

`secrets.toml`

`st.connection()`

Whether you have one OIDC provider or many, you'll need to have an[auth]dictionary insecrets.toml. You must declareredirect_uriandcookie_secretin the[auth]dictionary. These two values are shared between all OIDC providers in your app.

`[auth]`

`secrets.toml`

`redirect_uri`

`cookie_secret`

`[auth]`

If you are only using one OIDC provider, you can put the remaining three properties (client_id,client_secret, andserver_metadata_url) in[auth]. However, if you are using multiple providers, they should each have a unique name so you can declare their unique values in their own dictionaries. For example, if you name your connections"connection_1"and"connection_2", put their remaining properties in dictionaries named[auth.connection_1]and[auth.connection_2], respectively.

`client_id`

`client_secret`

`server_metadata_url`

`[auth]`

`"connection_1"`

`"connection_2"`

`[auth.connection_1]`

`[auth.connection_2]`

## A simple example

If you use Google Identity as your identity provider, a basic configuration for local development will look like the following TOML file:

.streamlit/secrets.toml:

`.streamlit/secrets.toml`

`[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "xxx"
client_id = "xxx"
client_secret = "xxx"
server_metadata_url = (
    "https://accounts.google.com/.well-known/openid-configuration"
)`

Make sure the port inredirect_urimatches the port you are using. Thecookie_secretshould be a strong, randomly generated secret. Both theredirect_uriandcookie_secretshould have been entered into your client configuration on Google Cloud. You must copy theclient_idandclient_secretfrom Google Cloud after you create your client. For some identity providers,server_metadata_urlmay be unique to your client. However, for Google Cloud, a single URL is shared for OIDC clients.

`redirect_uri`

`cookie_secret`

`redirect_uri`

`cookie_secret`

`client_id`

`client_secret`

`server_metadata_url`

In your app, create a simple login flow:

`import streamlit as st

if not st.experimental_user.is_logged_in:
    if st.button("Log in with Google"):
        st.login()
    st.stop()

if st.button("Log out"):
    st.logout()
st.markdown(f"Welcome! {st.experimental_user.name}")`

When you usest.stop(), your script run ends as soon as the login button is displayed. This lets you avoid nesting your entire page within a conditional block. Additionally, you can use callbacks to simplify the code further:

`st.stop()`

`import streamlit as st

if not st.experimental_user.is_logged_in:
    st.button("Log in with Google", on_click=st.login)
    st.stop()

st.button("Log out", on_click=st.logout)
st.markdown(f"Welcome! {st.experimental_user.name}")`

## Using multiple OIDC providers

If you use more than one OIDC provider, you'll need to declare a unique name for each. If you want to use Google Identity and Microsoft Entra ID as two providers for the same app, your configuration for local development will look like the following TOML file:

.streamlit/secrets.toml:

`.streamlit/secrets.toml`

`[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "xxx"

[auth.google]
client_id = "xxx"
client_secret = "xxx"
server_metadata_url = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

[auth.microsoft]
client_id = "xxx"
client_secret = "xxx"
server_metadata_url = (
    "https://login.microsoftonline.com/{tenant}/v2.0/.well-known/openid-configuration"
)`

Microsoft's server metadata URL varies slightly depending on how your client is scoped. Replace{tenant}with the appropriate value described in Microsoft's documentation forOpenID configuration.

`{tenant}`

Your app code:

`import streamlit as st

if not st.experimental_user.is_logged_in:
    if st.button("Log in with Google"):
        st.login("google")
    if st.button("Log in with Microsoft"):
        st.login("microsoft")
    st.stop()

if st.button("Log out"):
    st.logout()
st.markdown(f"Welcome! {st.experimental_user.name}")`

Using callbacks, this would look like:

`import streamlit as st

if not st.experimental_user.is_logged_in:
    st.button("Log in with Google", on_click=st.login, args=["google"])
    st.button("Log in with Microsoft", on_click=st.login, args=["microsoft"])
    st.stop()

st.button("Log out", on_click=st.logout)
st.markdown(f"Welcome! {st.experimental_user.name}")`

## Passing keywords to your identity provider

To customize the behavior of your identity provider, you may need to declare additional keywords. For a complete list of OIDC parameters, seeOpenID Connect Coreand your provider's documentation. By default, Streamlit setsscope="openid profile email"andprompt="select_account". You can change these and other OIDC parameters by passing a dictionary of settings toclient_kwargs.stateandnonce, which are used for security, are handled automatically and don't need to be specified.

`scope="openid profile email"`

`prompt="select_account"`

`client_kwargs`

`state`

`nonce`

For example,if you are using Auth0 and need to force users to log in every time, useprompt="login"as described in Auth0'sCustomize Signup and Login Prompts. Your configuration will look like this:

`prompt="login"`

`[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "xxx"

[auth.auth0]
client_id = "xxx"
client_secret = "xxx"
server_metadata_url = (
    "https://{account}.{region}.auth0.com/.well-known/openid-configuration"
)
client_kwargs = { "prompt" = "login" }`

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
