---
title: "お手製CMS markdownのFront Matter定義"
date: 2022-04-02T13:22:00+09:00
draft: true
private: true
image: https://i.imgur.com/dSD7sBI.png
toc: false
tags:
  - draft
  - 日記
  - 開発
  - python
  - disk
---

CMSがお手製ならFront Matter変数もお手製。
一応互換性は考慮しているけども。

### title

ページタイトル。
`og:title`にもなる。

### date

日付。
用途は未定、なくすかも。

### draft

trueならdraftモードの時のみhtml生成される。

### private

trueならprivateモードの時のみ生成される。

### image

サムネイル画像のurl。
`og:image`にも使う。

### toc

trueならページ先頭に目次を生成する。
実装するかどうかは保留。

### tags

タグの指定。
階層構造については検討中。


[Imgur](https://imgur.com/dSD7sBI)
