from pprint import pprint

#XXXは各ユーザー名　読み込み場所は各環境に応じた調整が必要
path = r'C:\Users\XXX\Desktop\Policy\Policy.txt'

file1 =  open(path,'r',encoding='utf-8')
f1 = file1.readlines()
file1.close()

#開いたファイルを変換
#[式 for 要素 in リスト if 条件]
lines_strip = [line.strip() for line in f1]
#print(lines_strip)

#事前処理 quota_exceeded 自動学習モードで追加できなかったポリシーがある
#リストから直接削除する
tmp = []
while lines_strip:
	x = lines_strip.pop()
	if x != 'quota_exceeded':
		tmp.append(x)

#元のリストに戻す		
while tmp:
	lines_strip.append(tmp.pop())

#各工程の変数宣言
Alist,Nlist_index,Access_subject = [],[],[]
Plist = [[]]
ALead_No,index_No = 0,0

#行番号を付けて特定の場所を探索
for No,Pick_text in enumerate(lines_strip):
	if 'use_profile 1' in Pick_text: #プロファイル決め打ち
		#print('{0}:{1}'.format(No,Pick_text))
		ALead_No = No - 1 
		#print(ALead_No)
		Nlist_index.append(ALead_No) #各行番号を格納
		index_No += 1 #行番号の個数を記録

#print(Nlist_index) #行番号の確認

#該当の行番号ごとに格納
for Pick_No in range(index_No):
	Alist = lines_strip[Nlist_index[Pick_No]:] #リスト更新
	del Alist[1:4] #1行目から3行目を削除
	#print(Alist[0:3])
	
	#空白がある行を探索
	for i,j in enumerate(Alist):
		if len(j) <= 1: #リスト内リストの空白判定
			Ai = i
			break
			
	#特定の行以下をすべて削除
	Alist = Alist[:Ai]
	#print(Alist[0:3])
	#print(Alist[0])
	#リストの更新
	Plist.append(Alist)
	#アクセス主体を別の場所へ保存
	Access_subject.append(Alist[0])

#print(Plist)

#多次元配列を一次元配列に変換
one_dim = []
for column in range(len(Plist)):
	for row in range(len(Plist[column])):
		#print(Plist[column][0], end=' ')
		#print(Plist[column][row], end=' ')
		one_dim.append(str(Plist[column][0]) + ' ' + str(Plist[column][row]))
	#print( )
		
#print(one_dim)

#文字列.replace(置換前の文字列, 置換後の文字列, 最大回数)
#特定の空白置換
file_execute = [f.replace('file execute', 'file_execute') for f in one_dim]
file_read = [f.replace('file read', 'file_read') for f in file_execute]
file_write = [f.replace('file write', 'file_write') for f in file_read]
file_append = [f.replace('file append', 'file_append') for f in file_write]
file_getattr = [f.replace('file getattr', 'file_getattr') for f in file_append]
file_create = [f.replace('file create', 'file_create') for f in file_getattr]
file_unlink = [f.replace('file unlink', 'file_unlink') for f in file_create]
file_chown = [f.replace('file chown', 'file_chown') for f in file_unlink]
file_chgrp = [f.replace('file chgrp', 'file_chgrp') for f in file_chown]
file_chmod = [f.replace('file chmod', 'file_chmod') for f in file_chgrp]
file_mkdir = [f.replace('file mkdir', 'file_mkdir') for f in file_chmod]
file_rmdir = [f.replace('file rmdir', 'file_rmdir') for f in file_mkdir]
file_mkfifo = [f.replace('file mkfifo', 'file_mkfifo') for f in file_rmdir]
file_mksock = [f.replace('file mksock', 'file_mksock') for f in file_mkfifo]
file_mkblock = [f.replace('file mkblock', 'file_mkblock') for f in file_mksock]
file_mkchar = [f.replace('file mkchar', 'file_mkchar') for f in file_mkblock]
file_truncate = [f.replace('file truncate', 'file_truncate') for f in file_mkchar]
file_symlink = [f.replace('file symlink', 'file_symlink') for f in file_truncate]
file_link = [f.replace('file link', 'file_link') for f in file_symlink]
file_rename = [f.replace('file rename', 'file_rename') for f in file_link]
file_ioctl = [f.replace('file ioctl', 'file_ioctl') for f in file_rename]
file_mount = [f.replace('file mount', 'file_mount') for f in file_ioctl]
file_unmount = [f.replace('file unmount', 'file_unmount') for f in file_mount]
file_chroot = [f.replace('file chroot', 'file_chroot') for f in file_unmount]
file_pivot_root = [f.replace('file pivot_root', 'file_pivot_root') for f in file_chroot]
misc_env = [f.replace('misc env', 'misc_env') for f in file_pivot_root]
network_inet = [f.replace('network inet', 'network_inet') for f in misc_env]
network_unix = [f.replace('network unix', 'network_unix') for f in network_inet]

#networkまわり
network = [f.replace('dgram send ', 'dgram_send_') for f in network_unix]
network = [f.replace('stream connect ', 'stream_connect_') for f in network]
network = [f.replace('dgram bind ', 'dgram_bind_') for f in network]
network = [f.replace('dgram ', 'dgram_') for f in network]
network = [f.replace('listen ', 'listen_') for f in network]

#カーネルを置換
kernel = [f.replace('<kernel> ', '') for f in network]
#print(kernel)

#残り全ての空白を置換
all_blank = [f.replace(' ', '", "') for f in kernel]
#print(all_blank)

#prologで処理可能な形へ変換
list_p = ['policy("' +  row + '").' for row in all_blank]
#print(list_p)

#アクセス主体のカーネル文字列の処理
Access_subject_kd = [f.replace('<kernel> ', '') for f in Access_subject]
#空白をカンマで区切る
Ask = []
for i in range(len(Access_subject_kd)):
	Ask.append(Access_subject_kd[i].split(' '))
#print(Ask)

#多次元リストを平坦化
flatten = lambda x: [z for y in x for z in (flatten(y) if hasattr(y, '__iter__') and not isinstance(y, str) else (y,))]
f_Ask = (flatten(Ask))
#重複を除く set型 重複を持たないデータ型
list_unique = list(set(f_Ask))
#print(list_unique)

#退避用リスト
tmp = []

'''
下記は環境によって異なるため注意が必要
'''

#一般ユーザーが使用する基本コマンド
bc_list = []
for bc in list_unique:
	if bc.find('/usr/bin/') >= 0:
		tmp = "basiscmd(\"" + bc + "\")."
		bc_list.append(tmp)
#print(bc_list)

#共有ライブラリ
sl_list = []
for sl in list_unique:
	if sl.find('/usr/lib/') >= 0:
		tmp = "sharelib(\"" + sl + "\")."
		sl_list.append(tmp)
#print(sl_list)

#管理コマンド
ac_list = []
for ac in list_unique:
	if ac.find('/usr/sbin/') >= 0:
		tmp = "admincmd(\"" + ac + "\")."
		ac_list.append(tmp)
#print(ac_list)

#システム全体で使用するデータ
alls_list = []
for alls in list_unique:
	if alls.find('/etc/') >= 0:
		tmp = "allsys(\"" + alls + "\")."
		alls_list.append(tmp)
#print(alls_list)

#マニュアルやライセンスなどのドキュメント
docu_list = []
for docu in list_unique:
	if docu.find('/usr/share/') >= 0:
		tmp = "docu(\"" + docu + "\")."
		docu_list.append(tmp)
#print(docu_list)

#管理以外
disa_list = ['disaccord-admincmd(X) :- sharelib(X).',
	'disaccord-admincmd(X) :- basiscmd(X).',
	'disaccord-admincmd(X) :- allsys(X).',
	'disaccord-admincmd(X) :- docu(X).'
]
#print(disa_list)

#各リストの連結
result = list_p + bc_list + sl_list + ac_list + alls_list + docu_list + disa_list

#出力確認
#XXXは各ユーザー名　出力場所は各環境に応じた調整が必要
path_w = r'C:\Users\XXX\Desktop\Policy\Policy.pl'

with open(path_w, mode='w') as f:
	f.write('\n'.join(result))
f.close()
print('file write ok')
