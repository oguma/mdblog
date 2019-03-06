#! /usr/bin/env python
import os, re, sys, shutil
from distutils.spawn import find_executable

if find_executable('hoedown') is None:
    print("Please, install 'hoedown'. https://github.com/hoedown/hoedown")
    sys.exit()

if os.path.exists('html'):
    shutil.rmtree('html')

os.mkdir('html')
os.mkdir('html/tmp')

shutil.copytree('md/img', 'html/img')
shutil.copytree('theme/css', 'html/css')
shutil.copyfile('theme/_htaccess', 'html/.htaccess')
# shutil.copyfile('theme/favicon.ico', 'html/favicon.ico')

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

subtitle = re.search('<title>(.*)</title>', base).group(1)

base = base.replace('<nav></nav>', "<nav>%s</nav>" % ul)
base = base.replace('<header></header>', "<header>%s</header>" % header)
base = base.replace('<aside></aside>', "<aside>%s</aside>" % aside)
base = base.replace('<footer></footer>', "<footer>%s</footer>" % footer)

for f in os.listdir('html/tmp'):
    if f not in ['_header.html', '_aside.html', '_footer.html']:
        frag = open('html/tmp/'+f, 'r').read()
        h1 = frag.split('\n', 1)[0]
        desc, DESC_NUM = '', 300
        for s in ext(frag).split('\n')[1:]:
            s = s.strip()
            if len(desc+s) > DESC_NUM:
                break
            desc += s
        date = ''
        if re.match("^\d{6}-.+?\.html$", f):
            y, m, d = '20'+f[0:2], f[2:4], f[4:6]
            date = '<time datetime="%s">%s</time>' % ('-'.join([y,m,d]), '.'.join([y,str(int(m)),str(int(d))]))
        post = base.replace('<title>%s</title>' % subtitle, "<title>%s | %s</title>" % (ext(h1), subtitle))
        post = post.replace('<meta name="description" content="">', '<meta name="description" content="%s">' % desc)
        post = post.replace('<article></article>', "<article>%s%s</article>" % (frag, date))
        open('html/'+f, 'w').write(post)

shutil.rmtree('html/tmp')
