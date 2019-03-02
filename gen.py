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
shutil.copyfile('theme/_htaccess', 'html/.htaccess')

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
        date = ""
        if re.match("^\d{6}-.+?\.html$", f):
            y, m, d = '20'+f[0:2], f[2:4], f[4:6]
            d1 = "%s-%s-%s" % (y, m, d)
            d2 = "%s.%s.%s" % (y, m, d)
            date = '<time datetime="%s">%s</time>' % (d1, d2)
        h1 = frag.split('\n', 1)[0]
        post = post.replace('<title></title>', "<title>%s | YOUR TITLE</title>" % ext(h1))
        post = post.replace('<nav></nav>', "<nav><h4>What to Read Next...</h4>%s</nav>" % ul)
        post = base.replace('<article></article>', "<article>%s%s</article>" % (frag, date))
        post = post.replace('<header></header>', "<header>%s</header>" % header)
        post = post.replace('<aside></aside>', "<aside>%s</aside>" % aside)
        post = post.replace('<footer></footer>', "<footer>%s</footer>" % footer)        
        open('html/'+f, 'w').write(post)

shutil.rmtree('html/tmp')
