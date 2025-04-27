---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/concepts/custom-components/create
date: 2025-04-27 12:48:40
---

# Create a Component

#### Note

If you are only interested inusing Streamlit Components, then you can skip this section and
head over to theStreamlit Components Galleryto find and install
components created by the community!

Developers can write JavaScript and HTML "components" that can be rendered in Streamlit apps. Streamlit Components can receive data from, and also send data to, Streamlit Python scripts.

Streamlit Components let you expand the functionality provided in the base Streamlit package. Use Streamlit Components to create the needed functionality for your use-case, then wrap it up in a Python package and share with the broader Streamlit community!

Types of Streamlit Components you could create include:

- Custom versions of existing Streamlit elements and widgets, such asst.sliderorst.file_uploader.
- Completely new Streamlit elements and widgets by wrapping existing React.js, Vue.js, or other JavaScript widget toolkits.
- Rendering Python objects having methods that output HTML, such as IPython__repr_html__.
- Convenience functions for commonly-used web features likeGitHub gists and Pastebin.
`st.slider`

`st.file_uploader`

`__repr_html__`

Check out these Streamlit Components tutorial videos by Streamlit engineer Tim Conkling to get started:

## Part 1: Setup and Architecture

## Part 2: Make a Slider Widget

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
