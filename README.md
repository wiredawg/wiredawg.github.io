This is very simple static site where all of the posts in the `_posts` directory
are appended to a list of posts in the index.html file.

# Usage

1. Clone this repo: `git clone https://github.com/wiredawg/wiredawg.github.io`
2. Create a python virtual env: `python -m venv venv`
3. Activate the venv: `source venv/bin/activate`
4. Install the dependencies: `pip install -r _requirements.txt`
5. Add a post to `_posts/<name>.md`

The contents of the post must have the header metadata:

```
---
title: <YOUR TITLE>
date: YYYY-mm-dd HH:MM
---
<YOUR POST CONTENTS>
```

6. Build the site: `./_build_site.py`
7. Publish the site: `git push origin master`

