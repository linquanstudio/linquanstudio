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
import mytool as mt

usage = F"""
{mt.N_PYTHON} {mt.N_ME} private:true|false src:path dest:path baseurl:url

private:true|false -> trueならprivateの記事も変換
src:変換元ディレクトリのパス
dest:出力先ディレクトリのパス
baseurl:公開サイトのbaseurl

markdownのポイント
* コードはcodeでなく<pre></pre>を使う →```を<pre></pre>に変換?

"""

p_dict = {
    'private': 'true',
    'src': '',
    'dest': '',
    'verbose': 'true',
    'baseurl': 'http://localhost:8000',
}

#-----------------------------------------------------------------------------------------------
# markdownをhtmlに変換する
#-----------------------------------------------------------------------------------------------
def md2html(src, dest, depth, private, url):
    ym, md = read_yaml_and_markdown(src)
    # private指定に合致しないものはskip(指定がpublicで文書がprivate)
    if not private and ym['private']:
        mt.xprint(F"[md2html] {src} private mode is different, skip.")
        return
    ym['dest'] = dest
    ym['url'] = url
    #pprint.pprint(ym)
    # html部分をnode tree化
    soup = BeautifulSoup(markdown.markdown(md), 'html.parser')
    tag_a(soup)
    tag_h2(soup)
    tag_img(soup)
    # 出力
    mt.xprint(F"[render] {src} --> {dest}")
    with open(dest, 'w') as f:
        f.write(to_html(soup.prettify(), depth, ym))

#-----------------------------------------------------------------------------------------------
# aタグの処理
#  1. target="_blank"を追加
#  2. hrefが".md"だったら.htmlに変更
#-----------------------------------------------------------------------------------------------
def tag_a(soup):
    for a in soup.find_all('a'):
        a['target'] = '_blank'
        href = os.path.splitext(a.get('href'))
        if href[1] in [ '.md' ]:
            a['href'] = F"{href[0]}.html"

#-----------------------------------------------------------------------------------------------
# h2タグの処理
# 1. ページ内で通番をつける
#-----------------------------------------------------------------------------------------------
def tag_h2(soup):
    for i, h2 in enumerate(soup('h2')):
        h2.insert(0, F"{i+1}. ")
            
#-----------------------------------------------------------------------------------------------
# imgタグの処理
#-----------------------------------------------------------------------------------------------
def tag_img(soup):
    # imgサイズを調整する (外部サイトにある場合も含めて調整に拡張)
    # ローカルの格納場所 md段階ではどこでも、htmlでは/image/下にランダム名でコピー
    # リンクのURLも調整する
    # または最初から/imageに置くか？
    for t in soup('img'):
    #    ext = os.path.splitext(t['src'])[1]
    #    img_path = F"{ls['root']}{os.sep}{t['src']}"
        width = int(t['width']) if t.has_attr('width') else None
    #    if ext.lower() in [ '.png', '.jpg', '.jpeg' ]:
    #        with Image.open(img_path) as img:
    #            width = img.width
    #    #print(img_path, ext, width)
        if width is None or width > 340:
            width = 340
        t['width'] = str(width)
        #t['style'] = 'display:block; margin:auto;'
        #t['style'] = 'display:block;margin:0;'
    
#-----------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------
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
    return (ym, '\n'.join(lines))
            
#-----------------------------------------------------------------------------------------------
# 整形後の<body></body>内のhtmlをwrapして返す
#-----------------------------------------------------------------------------------------------
def to_html(body, depth, ym):
    pprint.pprint(ym)
    return F"""<!doctype html>
<html lang="ja">
<head
prefix="og: https://ogp.me/ns# fb: https://ogp.me/ns/fb# article: https://ogp.me/ns/article#">
<meta charset="utf-8">
<meta property="og:url" content="{ym['url']}" />
<meta name="twitter:card" content="summary">
<meta name="twitter:site" content="@hayashiisme">
<meta name="twitter:creator" content="@hayashiisme">
<meta name="twitter:image"
content="{ym['twitter-image']}" />
<meta property="og:type" content="article" />
<meta property="og:title" content="{ym['title']}" />
<meta property="og:description" content="
{ym['description']}
" />
<meta property="og:site_name" content="林泉商店" />
<meta property="og:image" content="{ym['image']}" />
<meta property="og:locale" content="ja_JP" />
<meta charset="utf-8">
<title>{ym['title']} - {ym['date']}</title>
<meta name="description" content="{ym['description']}">
<!-- <meta name="viewport" content="width=device-width, initial-scale=1"> -->
<link rel="stylesheet" href="{'../' * depth}css/style.css">
</head>
<body>
<h1>{ym['title']}</h1>
{body}
<hr>
<div class="footer">
{ym['date']}
</div>
</body>
</html>"""

#-----------------------------------------------------------------------------------------------
# srcディレクトリを再帰的に辿って一ファイルずつ処理
#-----------------------------------------------------------------------------------------------
def doit(src, dest, private, verbose, baseurl):
    # srcの全リスト
    lsr = []
    if os.path.isdir(src):
        dirlist(lsr, src, '', 0)
    else:
        root, name = os.path.split(src)
        pair = os.path.splitext(name)
        lsr.append({'root': root, 'subdir': '', 'base': pair[0], 'ext': pair[1], 'is_dir': False,
                    'depth': 0 })
    # 全リストを一つずつ処理
    for l in lsr:
        if l['ext'] != '.md':
            # markdownではない
            if l['is_dir']:
                # directryなら同じものをdestに作る
                d = F"{dest}{l['subdir']}"
                os.makedirs(d, exist_ok=True)
                mt.xprint(F"[make dir] {d}")
            else:
                # directoryでなければコピーする
                s = F"{l['root']}{l['subdir']}{os.sep}{l['base']}{l['ext']}"
                d = F"{dest}{l['subdir']}{os.sep}{l['base']}{l['ext']}"
                mt.xprint(F"[copy] {s} -> {d}")
                shutil.copy2(s, d)
        else:
            # markdown
            s = F"{l['root']}{l['subdir']}{os.sep}{l['base']}.md"
            d = F"{dest}{l['subdir']}{os.sep}{l['base']}.html"
            url = F"{baseurl}{l['subdir']}{os.sep}{l['base']}.html"
            md2html(s, d, l['depth'], private, url)

#-----------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------
def dirlist(a, root, subdir, depth):
    fulldir = F"{root}{os.sep}{subdir}{os.sep}*" if subdir != '' else F"{root}{os.sep}*"
    for g in sorted(glob.glob(fulldir)):
        if os.path.isdir(g):
            newsubdir = F"{subdir}{os.sep}{os.path.basename(g)}"
            a.append({ 'root': root, 'subdir': newsubdir, 'base': '', 'ext': '', 'is_dir': True,
                       'depth': depth })
            dirlist(a, root, newsubdir, depth + 1)
        else:
            pair = os.path.splitext(os.path.basename(g))
            a.append({ 'root': root, 'subdir': subdir, 'base': pair[0], 'ext': pair[1],
                       'is_dir': False, 'depth': depth })

#-----------------------------------------------------------------------------------------------
# コマンドラインパラメータの取り込み
#-----------------------------------------------------------------------------------------------
def coax_params(pdict):
    src = os.path.expanduser(pdict['src']) if pdict['src'] != '' else None
    dest = os.path.expanduser(pdict['dest']) if pdict['dest'] != '' else None
    private = mt.t_or_f(pdict['private'])
    verbose = mt.t_or_f(pdict['verbose'])
    baseurl = pdict['baseurl']
    return [ src, dest, private, verbose, baseurl ]

#-----------------------------------------------------------------------------------------------
# verbose=Trueの時の実行設定表示
#-----------------------------------------------------------------------------------------------
def banner(src, dest, private, verbose, baseurl):
    if verbose:
        mt.xbanner([
            F"SCRIPT DIR : {mt.D_ME} (PID:{mt.P_ME})",
            F"SRC        : {src}",
            F"DEST       : {dest}",
            F"PRIVATE    : {private}",
            F"BASE URL   : {baseurl}",
        ])

#-----------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    if not mt.getintodict(sys.argv, usage, p_dict): mt.exit_with_elapsed_code(1)
    src, dest, private, verbose, baseurl = coax_params(p_dict)
    if src is None: mt.exit_with_elapsed_code(1, s='srcの指定がない')
    if dest is None: mt.exit_with_elapsed_code(1, s='destの指定がない')
    banner(src, dest, private, verbose, baseurl)
    doit(src, dest, private, verbose, baseurl)
    
    
