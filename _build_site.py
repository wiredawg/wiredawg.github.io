#!/usr/bin/env python
import os
import sys
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import markdown2

def build_blog():
    # Load the main template
    tenv = Environment(loader=FileSystemLoader('_templates'))

    # Parse all the posts
    post_files = []
    for path, dir, files in os.walk('./_posts'):
        for f in files:
            post_files.append(os.path.join(path, f))
    
    posts = []
    pages = []
    for pf in post_files:
        with open(pf) as fp: tobj = markdown2.markdown(fp.read(), extras=['metadata', 'fenced-code-blocks'])
        p = {}
        for k,v in tobj.metadata.items():
            if k == "date":
                p["timestamp"] = datetime.strptime(v, "%Y-%m-%d %H:%M")
                p["date"] = p["timestamp"].strftime("%A, %h. %d %Y at %I:%M %p")
            else:
                p[k] = v
        p["filename"] = pf
        p["content"] = tobj
        # Decide if this is going to the posts or as a page itself
        if "template" in p: pages.append(p)
        else: posts.append(p)

    # Render any pages
    for p in pages:
        ofile = os.path.basename(p["filename"]).replace(".md", ".html")
        try: os.mkdir("pages")
        except: pass
        ofile = os.path.join("pages", ofile)
        p["link"] = "/" + ofile
        tmpl = tenv.get_template(p["template"]+".j2")
        r = tmpl.render({"page":p, "pages": pages, "posts": posts})
        with open(ofile, 'w') as fp: fp.write(r)

    # Render the posts
    posts.sort(key= lambda x: x["timestamp"], reverse=True)
    tmpl = tenv.get_template("posts.j2")
    r = tmpl.render({"posts": posts, "pages": pages})
    with open("index.html", 'w') as fp: fp.write(r)

    return 0

if __name__ == "__main__": sys.exit(build_blog())

