---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/concepts/connections/security-reminders
date: 2025-04-27 12:48:36
---

# Security reminders

## Protect your secrets

Never save usernames, passwords, or security keys directly in your code or commit them to your repository.

### Use environment variables

Avoid putting sensitve information in your code by using environment variables. Be sure to check outst.secrets. Research any platform you use to follow their security best practices. If you use Streamlit Community Cloud,Secrets managementallows you save environment variables and store secrets outside of your code.

`st.secrets`

### Keep.gitignoreupdated

`.gitignore`

If you use any sensitive or private information during development, make sure that information is saved in separate files from your code. Ensure.gitignoreis properly configured to prevent saving private information to your repository.

`.gitignore`

## Pickle warning

Streamlit'sst.cache_dataandst.session_stateimplicitly use thepicklemodule, which is known to be insecure. It is possible to construct malicious pickle data that will execute arbitrary code during unpickling. Never load data that could have come from an untrusted source in an unsafe mode or that could have been tampered with.Only load data you trust.

`st.cache_data`

`st.session_state`

`pickle`

- When usingst.cache_data, anything your function returns is pickled and stored, then unpickled on retrieval. Ensure your cached functions return trusted values. This warning also applies tost.cache(deprecated).
- When therunner.enforceSerializableSessionStateconfiguration optionis set totrue, ensure all data saved and retrieved from Session State is trusted.
`st.cache_data`

`st.cache`

`runner.enforceSerializableSessionState`

`true`

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
