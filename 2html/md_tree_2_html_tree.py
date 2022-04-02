# -*- coding: utf-8 -*-
import os
import sys
import glob
import shutil
import markdown
from bs4 import BeautifulSoup
from PIL import Image
import pprint

def dirlist(a, root, depth):
    for g in sorted(glob.glob(F"{root}/*")):
        b = os.path.basename(g)
        d = os.path.isdir(g)
        a.append({'root': root, 'name': b, 'is_directory': d, 'depth': depth })
        if d: dirlist(a, g, depth + 1)

def doit(src, dest):
    #print(src)
    # srcの全リスト
    lsr = []
    # srcがディレクトリだったらdestもディレクトリ
    if os.path.isdir(src):
        os.makedirs(dest, exist_ok=True)
        dirlist(lsr, src, 0)
    else:
        sp = os.path.split(src)
        lsr.append({'root': src, 'name': sp[1], 'is_directory': False, 'depth':0 })
    for ls in lsr:
        src_root = ls['root'].split(src)[0]
        src_relative = F"{src_root}{os.sep}{ls['name']}" if src_root != '' else ls['name']
        src_path= F"{src_root}{os.sep}{ls['name']}"
        dest_path = F"{dest}{os.sep}{src_relative}"
        if ls['is_directory']:
            os.makedirs(dest_path, exist_ok=True)
        else:
            base_ext = os.path.splitext(dest_path)
            #print(src_path, dest_path, base_ext)
            if not base_ext[1] in [ '.md' ]:
                #shutil.copy2(src_path, dest_path)
                print(F"[copy] {src_relative} --> {dest_path}")
                shutil.copy2(src_relative, dest_path)
            else:
                # markdownをhtmlに変換
                #with open(src_path, 'r', encoding='utf-8') as f:
                with open(src_relative, 'r', encoding='utf-8') as f:
                    md = f.read()
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
                # imgサイズを調整する
                for t in soup('img'):
                    ext = os.path.splitext(t['src'])[1]
                    img_path = F"{ls['root']}{os.sep}{t['src']}"
                    width = int(t['width']) if t.has_attr('width') else None
                    if ext.lower() in [ '.png', '.jpg', '.jpeg' ]:
                        with Image.open(img_path) as img:
                            width = img.width
                    #print(img_path, ext, width)
                    if width is None or width > 720:
                        width = 780
                    t['width'] = str(width)
                    t['style'] = 'display:block; margin:auto;'
                # 出力
                dest_path = F"{base_ext[0]}.html"
                #print(dest_path)
                print(F"[render] {src_relative} --> {dest_path}")
                with open(dest_path, 'w') as f:
                    f.write(to_html(soup.prettify(), ls['depth']))
                

def to_html(body, depth):
    return F"""<!doctype html>
<html lang="ja">
<head
  prefix="og: https://ogp.me/ns# fb: https://ogp.me/ns/fb# article: https://ogp.me/ns/article#">
  <meta charset="utf-8">
  <!-- <meta property="og:url" content="" /> -->
  <meta property="og:type" content="" />
  <meta property="og:title" content="" />
  <meta property="og:description" content="
[商店主の仕込み]
満を持して自家製CMSシステム開発開始。
自家消費目的。
" />
  <meta property="og:site_name" content="林泉商店" />
  <meta property="og:image" content="https://i.imgur.com/dSD7sBI.png" />  
  <meta charset="utf-8">
  <title></title>
  <meta name="description" content="">
  <!-- <meta name="viewport" content="width=device-width, initial-scale=1"> -->
  <link rel="stylesheet" href="{'../' * depth}css/style.css">
</head>
<body>
{body}
</body>
</html>
    """

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('$ python md_tree_2_html_tree.py src dest')
        sys.exit(1)
    src = sys.argv[1]
    dest = sys.argv[2]
    doit(src, dest)
    
    
