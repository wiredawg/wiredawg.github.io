#!/usr/bin/env python
import os
import sys
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import markdown2

def build_blog():
    # Load the main template
    tenv = Environment(loader=FileSystemLoader('.'))
    tmpl = tenv.get_template("_base_template.j2")

    # Parse all the posts
    post_files = []
    for path, dir, files in os.walk('./_posts'):
        for f in files:
            post_files.append(os.path.join(path, f))
    
    posts = []
    for pf in post_files:
        with open(pf) as fp: raw_html = markdown2.markdown(fp.read(), extras=['metadata'])
        p = {}
        p["date"] = datetime.strptime(raw_html.metadata["date"], "%Y-%m-%d %H:%M").strftime("%A, %h. %d %Y at %I:%M %p")
        p["title"] = raw_html.metadata["title"]
        p["content"] = raw_html
        posts.append(p)

    r = tmpl.render({"posts": posts})

    with open("index.html", 'w') as fp: fp.write(r)

    return 0

if __name__ == "__main__": sys.exit(build_blog())

