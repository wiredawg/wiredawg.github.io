#!/usr/bin/env python
import os
import sys
import shutil
import json
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import markdown2

DEFAULT_POST_TEMPLATE = "post.j2"
DEFAULT_PAGE_TEMPLATE = "page.j2"
DEFAULT_TEMPLATE_MAP  = { "page": DEFAULT_PAGE_TEMPLATE, "post": DEFAULT_POST_TEMPLATE }

def make_pages_dir():
    try: shutil.rmtree("pages")
    except FileNotFoundError: pass
    try: os.mkdir("pages")
    except: pass

def build_blog():
    # Load the main template
    tenv = Environment(loader=FileSystemLoader('_templates'))

    # Parse all the posts
    post_files = []
    for path, dir, files in os.walk('./_posts'):
        for f in files:
            if f.startswith("."): continue # ignore hidden files
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

        # Allow Posts to be unpublished or in draft mode:
        # ... basically skip it in the render
        if "draft" in p and p["draft"].lower() == "true": continue

        if "category" not in p: p["category"] = "post"
        if "template" not in p: p["template"] = DEFAULT_TEMPLATE_MAP.get("category", DEFAULT_PAGE_TEMPLATE)
        p["filename"] = pf
        p["content"] = tobj

        # There are different categories of articles that can be published:
        #   1. Posts: Blog posts that are published to the main index page. These are usually short articles that
        #             the blog owner wants highlighted on their blog
        #   2. Pages: These are usually articles that are longer and will not appear by default on the post timeline
        #             but instead are available only through the nav bar.
        if p["category"] == "page":
            # Setup links to these articles
            ofile = os.path.basename(p["filename"]).replace(".md", ".html")
            ofile = os.path.join("pages", ofile)
            p["filename_html"] = ofile
            p["link"] = "/" + ofile
            pages.append(p)
        elif p["category"] == "post":
            # Setup links to these articles
            p["filename_html"] = "/"
            p["link"] = "/#" + p["title"].lower().replace(" ", "_")
            posts.append(p)
        else: raise KeyError("Unrecognized category '{}' in post '{}'".format(p["category"], pf))

    # Render any pages
    make_pages_dir()
    pages.sort(key=lambda x: x["title"])
#    print(json.dumps([{y:x[y] for y in x.keys() if y != "content"} for x in pages], default=lambda x: str(x), indent=4))
    for p in pages:
        tmpl = tenv.get_template(p["template"].replace(".j2", "")+".j2")
        r = tmpl.render({"page":p, "pages": pages, "posts": posts})
        with open(p["filename_html"], 'w') as fp: fp.write(r)

    # Render the posts
    posts.sort(key=lambda x: x["timestamp"], reverse=True)
    tmpl = tenv.get_template(DEFAULT_POST_TEMPLATE)
    r = tmpl.render({"posts": posts, "pages": pages})
    with open("index.html", 'w') as fp: fp.write(r)

    return 0

if __name__ == "__main__": sys.exit(build_blog())

