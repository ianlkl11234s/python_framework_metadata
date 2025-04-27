---
title: Streamlit Documentation Capture
url: https://docs.streamlit.io/develop/concepts/custom-components/publish
date: 2025-04-27 12:48:42
---

# Publish a Component

## Publish to PyPI

Publishing your Streamlit Component toPyPImakes it easily accessible to Python users around the world. This step is completely optional, so if you won’t be releasing your component publicly, you can skip this section!

#### Note

Forstatic Streamlit Components, publishing a Python package to PyPI follows the same steps as thecore PyPI packaging instructions. A static Component likely contains only Python code, so once you have yoursetup.pyfile correct andgenerate your distribution files, you're ready toupload to PyPI.

Bi-directional Streamlit Componentsat minimum include both Python and JavaScript code, and as such, need a bit more preparation before they can be published on PyPI. The remainder of this page focuses on the bi-directional Component preparation process.

### Prepare your Component

A bi-directional Streamlit Component varies slightly from a pure Python library in that it must contain pre-compiled frontend code. This is how base Streamlit works as well; when youpip install streamlit, you are getting a Python library where the HTML and frontend code contained within it have been compiled into static assets.

`pip install streamlit`

Thecomponent-templateGitHub repo provides the folder structure necessary for PyPI publishing. But before you can publish, you'll need to do a bit of housekeeping:

- Give your Component a name, if you haven't alreadyRename thetemplate/my_component/folder totemplate/<component name>/Pass your component's name as the the first argument todeclare_component()
- Rename thetemplate/my_component/folder totemplate/<component name>/
- Pass your component's name as the the first argument todeclare_component()
- EditMANIFEST.in, change the path for recursive-include frompackage/frontend/build *to<component name>/frontend/build *
- Editsetup.py, adding your component's name and other relevant info
- Create a release build of your frontend code. This will add a new directory,frontend/build/, with your compiled frontend in it:cd frontend
npm run build
- Pass the build folder's path as thepathparameter todeclare_component. (If you're using the template Python file, you can set_RELEASE = Trueat the top of the file):import streamlit.components.v1 as components

   # Change this:
   # component = components.declare_component("my_component", url="http://localhost:3001")

   # To this:
   parent_dir = os.path.dirname(os.path.abspath(__file__))
   build_dir = os.path.join(parent_dir, "frontend/build")
   component = components.declare_component("new_component_name", path=build_dir)
Give your Component a name, if you haven't already

- Rename thetemplate/my_component/folder totemplate/<component name>/
- Pass your component's name as the the first argument todeclare_component()
`template/my_component/`

`template/<component name>/`

`declare_component()`

EditMANIFEST.in, change the path for recursive-include frompackage/frontend/build *to<component name>/frontend/build *

`MANIFEST.in`

`package/frontend/build *`

`<component name>/frontend/build *`

Editsetup.py, adding your component's name and other relevant info

`setup.py`

Create a release build of your frontend code. This will add a new directory,frontend/build/, with your compiled frontend in it:

`frontend/build/`

`cd frontend
npm run build`

Pass the build folder's path as thepathparameter todeclare_component. (If you're using the template Python file, you can set_RELEASE = Trueat the top of the file):

`path`

`declare_component`

`_RELEASE = True`

`import streamlit.components.v1 as components

   # Change this:
   # component = components.declare_component("my_component", url="http://localhost:3001")

   # To this:
   parent_dir = os.path.dirname(os.path.abspath(__file__))
   build_dir = os.path.join(parent_dir, "frontend/build")
   component = components.declare_component("new_component_name", path=build_dir)`

### Build a Python wheel

Once you've changed the defaultmy_componentreferences, compiled the HTML and JavaScript code and set your new component name incomponents.declare_component(), you're ready to build a Python wheel:

`my_component`

`components.declare_component()`

- Make sure you have the latest versions of setuptools, wheel, and twine
- Create a wheel from the source code:# Run this from your component's top-level directory; that is,
 # the directory that contains `setup.py`
 python setup.py sdist bdist_wheel
Make sure you have the latest versions of setuptools, wheel, and twine

Create a wheel from the source code:

`# Run this from your component's top-level directory; that is,
 # the directory that contains `setup.py`
 python setup.py sdist bdist_wheel`

### Upload your wheel to PyPI

With your wheel created, the final step is to upload to PyPI. The instructions here highlight how to upload toTest PyPI, so that you can learn the mechanics of the process without worrying about messing anything up. Uploading to PyPI follows the same basic procedure.

- Create an account onTest PyPIif you don't already have oneVisithttps://test.pypi.org/account/register/and complete the stepsVisithttps://test.pypi.org/manage/account/#api-tokensand create a new API token. Don’t limit the token scope to a particular project, since you are creating a new project. Copy your token before closing the page, as you won’t be able to retrieve it again.
- Visithttps://test.pypi.org/account/register/and complete the steps
- Visithttps://test.pypi.org/manage/account/#api-tokensand create a new API token. Don’t limit the token scope to a particular project, since you are creating a new project. Copy your token before closing the page, as you won’t be able to retrieve it again.
- Upload your wheel to Test PyPI.twinewill prompt you for a username and password. For the username, use__token__. For the password, use your token value from the previous step, including thepypi-prefix:python -m twine upload --repository testpypi dist/*
- Install your newly-uploaded package in a new Python project to make sure it works:python -m pip install --index-url https://test.pypi.org/simple/ --no-deps example-pkg-YOUR-USERNAME-HERE
Create an account onTest PyPIif you don't already have one

- Visithttps://test.pypi.org/account/register/and complete the steps
- Visithttps://test.pypi.org/manage/account/#api-tokensand create a new API token. Don’t limit the token scope to a particular project, since you are creating a new project. Copy your token before closing the page, as you won’t be able to retrieve it again.
Visithttps://test.pypi.org/account/register/and complete the steps

Visithttps://test.pypi.org/manage/account/#api-tokensand create a new API token. Don’t limit the token scope to a particular project, since you are creating a new project. Copy your token before closing the page, as you won’t be able to retrieve it again.

Upload your wheel to Test PyPI.twinewill prompt you for a username and password. For the username, use__token__. For the password, use your token value from the previous step, including thepypi-prefix:

`twine`

`pypi-`

`python -m twine upload --repository testpypi dist/*`

Install your newly-uploaded package in a new Python project to make sure it works:

`python -m pip install --index-url https://test.pypi.org/simple/ --no-deps example-pkg-YOUR-USERNAME-HERE`

If all goes well, you're ready to upload your library to PyPI by following the instructions athttps://packaging.python.org/tutorials/packaging-projects/#next-steps.

Congratulations, you've created a publicly-available Streamlit Component!

## Promote your Component!

We'd love to help you share your Component with the Streamlit Community! To share it:

- If you host your code on GitHub, add the tagstreamlit-component, so that it's listed in theGitHubstreamlit-componenttopic:Add the streamlit-component tag to your GitHub repo
- Post on the Streamlit Forum inShow the Community!. Use a post title similar to "New Component:<your component name>, a new way to do X".
- Add your component to theCommunity Component Tracker.
- Tweet us at@streamlitso that we can retweet your announcement for you.
If you host your code on GitHub, add the tagstreamlit-component, so that it's listed in theGitHubstreamlit-componenttopic:

`streamlit-component`

Add the streamlit-component tag to your GitHub repo

Post on the Streamlit Forum inShow the Community!. Use a post title similar to "New Component:<your component name>, a new way to do X".

`<your component name>`

Add your component to theCommunity Component Tracker.

Tweet us at@streamlitso that we can retweet your announcement for you.

OurComponents Galleryis updated approximately every month. Follow the above recommendations to maximize the liklihood of your component landing in our Components Gallery. Community Components featured in our docs are hand-curated on a less-regular basis. Popular components with many stars and good documentation are more likely to be selected.

### Still have questions?

Ourforumsare full of helpful information and Streamlit experts.
