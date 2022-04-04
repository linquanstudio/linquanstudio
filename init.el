;; パッケージのリポジトリを追加
;; M-x eval-buffer
  (package-initialize)

(setq package-archives
      '(("gnu" . "http://elpa.gnu.org/packages/")
        ("melpa" . "http://stable.melpa.org/packages/")))

(setq default-directory (concat (getenv "HOME") "~"))
;; 追加パッケージ保存path
(setq load-path (append '("~/.emacs.d/elpa") load-path))
;; バックアップファイルの保存先
(setq backup-directory-alist '(("" . "~/.emacs.d/backup")))
;; フォント
(set-face-attribute 'default nil :family "HackGenNerd" :height 140)
(set-fontset-font nil '(#x80 . #x10ffff) (font-spec :family "HackGenNerd"));; default-directory 
;;; 画面の設定
(progn
  ;;(set-default-font "Consolas 10")
  ;;(set-fontset-font (frame-parameter nil 'font) 'japanese-jisx0208
  ;;(font-spec :family "Meiryo" :size 10))
  (setq initial-frame-alist
	(append (list
		 '(width . 100)
		 '(height . 104)
		 '(top . 0)
		 '(left . 1200)
		 '(alpha . 85)
		 ;;'(font . "BIZ UDゴシック 10")
		 )))
  )
(setq default-frame-alist initial-frame-alist)

;; DDSKK ;; 新しいのだと動かない。;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; ccc-20151205.543/cdb-20151205.543/ddskk-20160130.2100の組み合せだと可
(global-set-key "\C-\\" 'skk-mode)
(setq skk-large-jisyo "~/skk-dic/SKK-JISYO.L")
(setq skk-jisyo "~/skk-dic/.skk-jisyo")
(setq skk-backup-jisyo "~/skk-dic/.skk-jisyo.BAK")
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(set-language-environment 'Japanese)
(set-terminal-coding-system 'utf-8)
(set-keyboard-coding-system 'utf-8)
(set-buffer-file-coding-system 'utf-8)
(setq default-buffer-file-coding-system 'utf-8)
(setq file-name-coding-system 'utf-8)
(set-default-coding-systems 'utf-8)

(setq-default tab-width 2)

(line-number-mode t)
(column-number-mode t)
(setq mouse-drag-copy-region t)
(setq-default indent-tabs-mode nil) ;;設定するとindentにSPACEを使う
(setq-default c-basic-offset 2)
(setq indent-line-function 'insert-tab)
;; メニューバーにファイルパスを表示
(setq frame-title-format(format "%%f - Emacs@%s" (system-name)))
;; Ctrl-c dで日付を挿入
(defun insert-current-time()
  (interactive)
  (insert (format-time-string "%Y-%m-%dT%H:%M:00%:z" (current-time))))
(define-key global-map "\C-cd" `insert-current-time)
;; Ctrl-c fでCMSのfront matterを挿入
(defun insert-front-matter()
  (interactive)
  (insert "---\n")
  (insert "title: \n")
  (insert "description: \n")
  (insert (format-time-string "date: %Y-%m-%dT%H:%M:00%:z\n" (current-time)))
  (insert "draft: false\n")
  (insert "private: true\n")
  (insert "twitter-image: https://i.imgur.com/dSD7sBI.png\n")
  (insert "image: https://i.imgur.com/dSD7sBI.png\n")
  (insert "toc: false\n")
  (insert "tags:\n")
  (insert "  - 日記\n")
  (insert "---\n"))
(define-key global-map "\C-cf" `insert-front-matter)
;; text-modeの設定と.kscrに対する割当
(add-hook 'text-mode-hook
          (function
           (lambda ()
             ;;(set-fill-column 78)
             ;;(turn-on-auto-fill)
             ;;(setq indent-tabs-mode nil)
             (setq tab-width 2)
             (define-key text-mode-map "\C-i" 'self-insert-command)
             )))

(require 'web-mode)
;;(add-to-list 'auto-mode-alist '("\\.phtml\\'" . web-mode))
;;(add-to-list 'auto-mode-alist '("\\.tpl\\.php\\'" . web-mode))
;;(add-to-list 'auto-mode-alist '("\\.[agj]sp\\'" . web-mode))
;;(add-to-list 'auto-mode-alist '("\\.as[cp]x\\'" . web-mode))
;;(add-to-list 'auto-mode-alist '("\\.erb\\'" . web-mode))
;;(add-to-list 'auto-mode-alist '("\\.mustache\\'" . web-mode))
;;(add-to-list 'auto-mode-alist '("\\.djhtml\\'" . web-mode))
(add-to-list 'auto-mode-alist '("\\.html?\\'" . web-mode))
(add-to-list 'auto-mode-alist '("\\.xml?\\'" . web-mode))
;;(add-to-list 'auto-mode-alist '("\\.sql?\\'" . web-mode))
;;(add-to-list 'auto-mode-alist '("\\.js?\\'" . web-mode))
(add-hook 'web-mode-hook
					'(lambda ()
						 ;; 要素のハイライト
						 (setq tab-width 2)
						 (setq indent-tabs-mode nil)
						 (setq web-mode-enable-current-element-highlight t)
						 (setq web-mode-enable-auto-pairing t)
						 (setq web-mode-enable-auto-closing t)						 
						 
						 (setq web-mode-markup-indent-offset 2)
						 (setq web-mode-attr-indent-offset nil)
						 (setq web-mode-markup-indent-offset 2)
						 (setq web-mode-css-indent-offset 2)
						 (setq web-mode-code-indent-offset 2)
						 (setq web-mode-sql-indent-offset 2)
						 (setq web-mode-comment-style 2)
						 (setq web-mode-script-padding 1)
						 (setq web-mode-block-padding 0)
						 ;; フォントの配色
						 ;;(set-face-attribute 'web-mode-doctype-face nil :foreground "Pink3")
						 ;;(set-face-attribute 'web-mode-html-tag-face nil :foreground "Green")
						 ;;(set-face-attribute 'web-mode-html-attr-value-face nil :foreground "Yellow")
						 ;;(set-face-attribute 'web-mode-html-attr-name-face nil :foreground "#0FF")
						 ;; タグを自動で閉じる
						 ))

;; ------------------ markdown-mode ------------------------------------------------------
(autoload 'markdown-mode "markdown-mode"
   "Major mode for editing Markdown files" t)
(add-to-list 'auto-mode-alist '("\\.markdown\\'" . markdown-mode))
(add-to-list 'auto-mode-alist '("\\.md\\'" . markdown-mode))

(autoload 'gfm-mode "markdown-mode"
   "Major mode for editing GitHub Flavored Markdown files" t)
(add-to-list 'auto-mode-alist '("README\\.md\\'" . gfm-mode))
;; --------------------------------------------------------------------------------------

(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(ansi-color-faces-vector
	 [default default default italic underline success warning error])
 '(column-number-mode t)
 '(custom-enabled-themes '(misterioso))
 '(package-selected-packages '(web-mode ddskk)))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )
