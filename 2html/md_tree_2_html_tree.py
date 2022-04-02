# -*- coding: utf-8 -*-
import os
import sys
import glob
import shutil
import markdown
from bs4 import BeautifulSoup
from PIL import Image
import yaml
import pprint

def dirlist(a, root, subdir, depth):
    fulldir = F"{root}{os.sep}{subdir}{os.sep}*" if subdir != '' else F"{root}{os.sep}*"
    #print(fulldir)
    for g in sorted(glob.glob(fulldir)):
        #print('g--------', g)
        if os.path.isdir(g):
            newsubdir = F"{subdir}{os.sep}{os.path.basename(g)}"
            a.append({ 'root': root, 'subdir': newsubdir, 'base': '', 'ext': '', 'is_dir': True,
                       'depth': depth })
            dirlist(a, root, newsubdir, depth + 1)
        else:
            pair = os.path.splitext(os.path.basename(g))
            a.append({ 'root': root, 'subdir': subdir, 'base': pair[0], 'ext': pair[1],
                       'is_dir': False, 'depth': depth })


def read_yaml_and_markdown(src):
    with open(src, 'r', encoding='utf-8') as f:
        lines = [ l.strip() for l in f.readlines() ]
    # yamlのブロックとmarkdownを分ける
    ym = []
    if lines[0] == '---':
        lines.pop(0)
        while lines[0] != '---':
            ym.append(lines.pop(0))
        lines.pop(0)
    ym = yaml.safe_load('\n'.join(ym))
    #print('[yaml]')
    #print(ym)
    #print('[markdown')
    #print(lines)
    return (ym, '\n'.join(lines))
            
def to_html(body, depth):
    return F"""<!doctype html>
<html lang="ja">
<head
prefix="og: https://ogp.me/ns# fb: https://ogp.me/ns/fb# article: https://ogp.me/ns/article#">
<meta charset="utf-8">
<meta property="og:url" content="https://linquanstudio.github.io/linquanstudio/test-index.html" />
<meta name="twitter:card" content="summary">
<meta name="twitter:site" content="@hayashiisme">
<meta name="twitter:creator" content="@hayashiisme">
<meta name="twitter:image"
content="https://linquanstudio.github.io/linquanstudio/image/studio_icon.png" />
<meta property="og:type" content="article" />
<meta property="og:title" content="商店主の仕込み" />
<meta property="og:description" content="
[商店主の仕込み]満を持して自家製CMSシステム開発開始。自家消費目的。永遠にβ版。
" />
<meta property="og:site_name" content="林泉商店" />
<meta property="og:image" content="https://i.imgur.com/dSD7sBI.png" />
<meta property="og:locale" content="ja_JP" />
<meta charset="utf-8">
<title></title>
<meta name="description" content="">
<!-- <meta name="viewport" content="width=device-width, initial-scale=1"> -->
<link rel="stylesheet" href="{'../' * depth}css/style.css">
</head>
<body>
{body}
</body>
</html>"""

def md2html(src, dest, depth):
    ym, md = read_yaml_and_markdown(src)
    #print(md)
    soup = BeautifulSoup(markdown.markdown(md), 'html.parser')
    # aタグをすべてチェック
    for a in soup.find_all('a'):
        a['target'] = '_blank'
        href = os.path.splitext(a.get('href'))
        #print(href)
        if href[1] in [ '.md' ]:
            a['href'] = F"{href[0]}.html"
    # h2に番号をつける
    for i, h2 in enumerate(soup('h2')):
        h2.insert(0, F"{i+1}. ")
    # codeをそれらしくする
    for t in soup('code'):
        t.parent['class'] = 'code'
    # imgサイズを調整する (外部サイトにある場合も含めて調整に拡張)
    #for t in soup('img'):
    #    ext = os.path.splitext(t['src'])[1]
    #    img_path = F"{ls['root']}{os.sep}{t['src']}"
    #    width = int(t['width']) if t.has_attr('width') else None
    #    if ext.lower() in [ '.png', '.jpg', '.jpeg' ]:
    #        with Image.open(img_path) as img:
    #            width = img.width
    #    #print(img_path, ext, width)
    #    if width is None or width > 720:
    #        width = 780
    #    t['width'] = str(width)
    #    t['style'] = 'display:block; margin:auto;'
    # 出力
    print(F"[render] {src} --> {dest}")
    with open(dest, 'w') as f:
        f.write(to_html(soup.prettify(), depth))

            
def doit(src, dest):
    # srcの全リスト
    lsr = []
    if os.path.isdir(src):
        dirlist(lsr, src, '', 0)
    else:
        root, name = os.path.split(src)
        pair = os.path.splitext(name)
        lsr.append({'root': root, 'subdir': '', 'base': pair[0], 'ext': pair[1], 'is_dir': False,
                    'depth': 0 })
    for l in lsr:
        #print(l)
        if l['ext'] != '.md':
            if l['is_dir']:
                #s = F"{l['root']}{l['subdir']}"
                d = F"{dest}{l['subdir']}"
                os.makedirs(d, exist_ok=True)
                print(F"[make dir] {d}")
            else:
                s = F"{l['root']}{l['subdir']}{os.sep}{l['base']}{l['ext']}"
                d = F"{dest}{l['subdir']}{os.sep}{l['base']}{l['ext']}"
                print(F"[copy] {s} -> {d}")
                shutil.copy2(s, d)
        else:
            s = F"{l['root']}{l['subdir']}{os.sep}{l['base']}.md"
            d = F"{dest}{l['subdir']}{os.sep}{l['base']}.html"
            print(F"[rendering] {l['base']}{l['ext']}")
            md2html(s, d, l['depth'])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('$ python md_tree_2_html_tree.py src dest')
        sys.exit(1)
    src = sys.argv[1]
    dest = sys.argv[2]
    doit(src, dest)
    
    
