# -*- coding: utf-8 -*-
import sys
import os
import psutil
import time
import datetime
import platform
import subprocess
import pickle

# 実行Platformの名称 'Windows', 'Darwin', 'Linux'
N_SYSTEM = platform.system()
# PYTHONの名前。現在は単にスクリプトがPython3用であることを示す程度の意味しかない
N_PYTHON = 'python' if os.name == 'nt' else 'python3'
# pythonのバージョン文字列
V_PYTHON = sys.version
# 実行プロセスのスクリプト名
N_ME = os.path.basename(sys.argv[0])
# N_MEが存在するパス。子プロセス実行の際の起点のパスとなる
D_ME = None
for p in sys.path:
    d = p + '/' + N_ME
    if os.path.exists(d): D_ME = os.path.dirname(d)
# このProcessのpid
P_ME = psutil.Process().pid
# 開始時間とする
T_ME = time.time()
# lap time用
T_LA = time.time()

# いちおう表示しておく
print("[executed] {} {}({}) path:{} time:{} {}".format(N_PYTHON, N_ME, P_ME, D_ME, time.strftime("%y-%m-%d %H:%M:%S", time.localtime(T_ME)), T_LA), file=sys.stderr)

# --------------------------------------------------
# option指定のみで構成されるコマンドライン引数をdictionaryにして返す
# 'd:dbs'という引数が
# dct['d'] = 'dbs'となる
# ※default指定はあらかじめdctに入れておく
# --------------------------------------------------
def getintodict(xargv, usage, dct):
    argv = xargv[1:]
    if len(argv) <= 0:
        print(usage)
        return False
    for i in range(len(argv)):
        kv = argv[i].replace('\\', '/').split(':')
        if len(kv) > 2:
            v = ':'.join(kv[1:len(kv)])
        else: v = kv[1]
        dct[kv[0]] = v
    return True

# ------------------------------------------------------------------------------
# 'True|False'等の文字列から真偽値を返す
# 'True', 'true', 'T', 't', '1' 以外は全てFalseを返す
# ------------------------------------------------------------------------------
def t_or_f(s):
    ss = s.lower()
    if ss == 't': return True
    elif ss == 'true': return True
    elif ss == '1': return True
    else: return False

# --------------------------------------------------
# tag付きprint
# --------------------------------------------------
def xprint(s, out=sys.stderr):
    print(F"{datetime.datetime.now().strftime('%H:%M:%S')} {N_ME:21} {s}", file=out)

# --------------------------------------------------
# tag付きprintでスクリプトバナー
# --------------------------------------------------
def xbanner(sa):
    for s in sa: xprint(s)

# --------------------------------------------------
# 
# --------------------------------------------------
def xsys_exit(s, code):
    xprint(s)
    sys.exit(code)

# --------------------------------------------------
# 
# --------------------------------------------------
def exit_with_elapsed_code(code, s=None):

    xsys_exit("{} = {}{}".format(
        F"[complete {code}] total elapsed time (min.)",
        F"{((time.time() - T_ME) / 60.0):.4f}",
        F"\n{s}" if s is not None else '',
    ), code)
    
# --------------------------------------------------
# ラップタイム表示用 実行すると開始時刻が更新される
# --------------------------------------------------
def elapsed():
    global T_LA
    t = time.time()
    print("{} = {}".format(
        F"[lap] {N_PYTHON} {N_ME}({P_ME}) total elapsed time (min.)",
        F"{((t - T_LA) / 60.0):.4f}"
    ))
    T_LA = t

# --------------------------------------------------
# tag付きprintでスクリプトバナー
# --------------------------------------------------
def xbanner(sa):
    for s in sa: xprint(s)
    
# --------------------------------------------------
# 終了したsubprocessをチェックして取り除きsubprocessが追加可能か否かを返す
# sp:subprocess array, msp:max subprocess array length
# --------------------------------------------------
def cleaning_subprocesses(spa, mspal):
    print(F"### - {len(spa)} ------------------------------")
    for i in reversed(range(len(spa))):
        pid = spa[i]['proc'].pid
        if psutil.pid_exists(pid):
            print(F"{pid} {psutil.Process(pid).status()}")
            if psutil.Process(pid).status() not in [
                    'running', 'sleeping', 'disk-sleep' ]:
                print("pop spa.")
                spa.pop(i)
        else:
            print(F"{pid} process has exit.")
            spa.pop(i)
    print("### ---------------------------------")
    return len(spa) < mspal

# --------------------------------------------------
# 実行中subprocessの表示
# --------------------------------------------------
def display_subprocesses(spa):
    print(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    s = '> {}, elapsed(min.): {}, pid: {}'
    for sp in spa:
        print(s.format(sp['title'], int((time.time() - sp['start_time']) / 60.0), sp['proc'].pid))

# --------------------------------------------------
# subprocessを一つ追加
# --------------------------------------------------
def append_subprocess(d, a, title, spa, verbose):
    po = xPopen(a, d, verbose)
    spa.append({'title':title, 'start_time':time.time(), 'proc':po})

# --------------------------------------------------
# subprocess 同期実行
# subprocessがエラーになったら終了
# 正常終了ならTrue/エラーならFalseを返す
# --------------------------------------------------
def xrun(ca, cwd, verbose):
    if verbose: spcp = subprocess.run(ca, cwd=cwd)
    else: spcp = subprocess.run(ca, cwd=cwd, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
    return spcp.returncode == 0
    
# --------------------------------------------------
# subprocess 非同期実行
# Popenのオブジェクトを返す
# --------------------------------------------------
def xPopen(ca, cwd, verbose):
    if verbose:
        spcp = subprocess.Popen(ca, cwd=cwd)
    else:
        spcp = subprocess.Popen(ca, cwd=cwd,
                                stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
    return spcp

