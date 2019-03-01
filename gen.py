#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, sys, shutil
from distutils.spawn import find_executable

# if find_executable('pandoc') is None:
if find_executable('hoedown') is None:
    # print("Please, install 'pandoc'. https://pandoc.org/installing.html")
    print("Please, install 'hoedown'. https://github.com/hoedown/hoedown")
    sys.exit()

if os.path.exists('html'):
    shutil.rmtree('html')

os.mkdir('html')
os.mkdir('html/tmp')

shutil.copytree('md/img', 'html/img')
# shutil.copytree('theme/imgbase', 'html/imgbase')
shutil.copytree('theme/css', 'html/css')

# os.system('cd md && find . -iname "*.md" -type f -exec sh -c \'pandoc "${0}" -o "../html/tmp/${0%.md}.html"\' {} \;')
os.system('cd md && find . -iname "*.md" -type f -exec sh -c \'hoedown --tables "${0}" > "../html/tmp/${0%.md}.html"\' {} \;')

ext = lambda s: re.sub('<[^<>]+>', '', s)

ul = "<ul>"
for f in sorted(os.listdir('html/tmp'), reverse=True):
    if f not in ['index.html', '_header.html', '_aside.html', '_footer.html']:
        h1 = open('html/tmp/'+f, 'r').readline().strip()
        ul += "<li><a href='%s'>%s</a></li>" % (f, ext(h1))
ul += "</ul>"

base = open('theme/base.html', 'r').read()
header = open('html/tmp/_header.html', 'r').read()
aside = open('html/tmp/_aside.html', 'r').read()
footer = open('html/tmp/_footer.html', 'r').read()

for f in os.listdir('html/tmp'):
    if f not in ['_header.html', '_aside.html', '_footer.html']:
        frag = open('html/tmp/'+f, 'r').read()
        h1 = frag.split('\n', 1)[0]
        post = base.replace('<article></article>', "<article>%s</article>" % frag)
        post = post.replace('<header></header>', "<header>%s</header>" % header)
        post = post.replace('<aside></aside>', "<aside>%s</aside>" % aside)
        post = post.replace('<footer></footer>', "<footer>%s</footer>" % footer)
        
        post = post.replace('<nav></nav>', "<nav><h3>What to Read Next...</h3>%s</nav>" % ul)
        post = post.replace('<title></title>', "<title>%s | YOUR TITLE</title>" % ext(h1))
        
        open('html/'+f, 'w').write(post)

shutil.rmtree('html/tmp')
