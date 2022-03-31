# -*- coding: utf-8 -*-
import sys
import os
import markdown
from bs4 import BeautifulSoup

if __name__ == '__main__':
    print(F"[START] {sys.argv.pop(0)}")
    for fp in sys.argv:
        src, dest = fp.split(':')
        src += '.md'
        dest += '.html'
        print(F"{src} -> {dest}")
        fpt = os.path.split(src)
        with open(src) as f: s = ''.join(f.readlines())
        soup = BeautifulSoup(markdown.markdown(s, output_format='html5'), 'html.parser')
        title = soup.find('h1').get_text()
        style = """
        article, aside, dialog, figure, footer, header,
        hgroup, menu, nav, section { display: block; }
        body { font-size: 0.9em; }
        h2 { font-size:1.3em; }
        h3 { margin: 0 0 0 2em; margin-top: 0.8em; }
        p { margin: 0 0 0 3em; }
        ul, ol { margin: 0.2em 0 0.2em 0; }
        li { margin: 0 0 0 1.5em; }
        """
        html = F"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8" />
        <title>{title}</title>
        <!--[if IE]>
        <script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
        <![endif]-->
        <style>
        {style}
        </style>
        </head>
        <body>
        {soup}
        </body>
        </html>
        """
        with open(dest, 'w') as f: f.write(html)
        
        
        
