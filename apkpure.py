#!/usr/bin/python3
# ApkPure Downloader
# Coded by FR13NDS
# Source: github.com/FR13NDS666

try: import bs4
except ImportError: os.system('python3 -m pip install bs4')
try: import requests
except ImportError: os.system('python3 -m pip install requests')
try: from tqdm import tqdm
except ImportError: os.system('python2 -m pip install tqdm')

import os
from bs4 import BeautifulSoup as sabuncantik

logo = '         ╔═╗╔═╗╦╔═   ╔═╗╦ ╦╦═╗╔═╗\n         ╠═╣╠═╝╠╩╗───╠═╝║ ║╠╦╝║╣\n         ╩ ╩╩  ╩ ╩   ╩  ╚═╝╩╚═╚═╝\n     +-------------------------------+\n       Author : FR13NDS\n       Github : github.com/FR13NDS666\n     +-------------------------------+'
headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532G Build/MMB29T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36'}

def download(url, out):
	r = requests.get(url, headers=headers, stream=True)
	total_size = int(r.headers.get('content-length', 0))
	print ('[*] Sedang Mendownload .....')
	block_size = 1024
	t = tqdm(total=total_size, unit='iB', unit_scale=True)
	with open(out, 'wb') as f:
		for data in r.iter_content(chunk_size=block_size):
			if data: t.update(len(data)); f.write(data)
	t.close()
	print ('[*] Download Selesai'); print (f'[*] Apk Disimpan: {out}')

def main_main():
	os.system('clear')
	print (logo); print ()
	nama = str(input('[#] Masukan Nama Apk: '))
	link, nomor, garis = ([], 0, '-'*45)

	try:
		req = requests.get(f'https://m.apkpure.com/id/search?q={nama.replace(" ", "+")}', headers=headers).content
	except requests.ConnectionError:
		exit('[!] Tidak Tersambung Ke Internet')

	req = sabuncantik(req, 'html.parser')
	print (); print (garis)
	for a in req.find_all('a', attrs={'class':'dd'}):
		ling = a.get('href')
		link.append(ling)

	for div in req.find_all('div', attrs={'class':'r'}):
		nomor += 1
		nama_apk = div.find('p', attrs={'class':'p1'}).text
		developer = div.find('p', attrs={'class':'p2'}).text
		nama_apk = nama_apk[:20]
		print (f'[ {str(nomor)} ]  Aplikasi: {nama_apk}...')
		print ('-'*len(f'[ {str(nomor)} ]')+f' Developer: {developer}')
		print (garis)

	try:
		pilih = int(input('[#] Pilih Apk: '))
		if pilih in ['', ' ']: exit('[!] Pilihan Tidak Ada')
	except ValueError:
		exit('[!] Pilihan Harus Angka')

	pilih = (pilih)-1

	try:
		url = f'https://m.apkpure.com{str(link[pilih])}/download?from=details'
		run = requests.get(url, headers=headers).content
	except IndexError: exit('[!] Pilihan Tidak Ada')
	except requests.ConnectionError:
		exit('[!] Koneksi Internet Buruk')


	ok = sabuncantik(run, 'html.parser')
	_find_1 = ok.find('div', attrs={'class':'fast-download-box'})
	_find_2 = _find_1.find('a', attrs={'class':'ga'})
	_find_3 = _find_1.find('span', attrs={'class':'fsize'})
	apksize = _find_3.text

	print (f'[!] Size Aplikasi: {str(apksize.replace("(", "").replace(")", ""))}')
	tanya = str(input('[!] Yakin Untuk Mendownload?\n[!] [Y: IYA, T: TIDAK] Jawab: '))
	if tanya in list('yY'):
		output = str(input('[#] Output: '))+'.apk'
		file = _find_2.get('href')
		try: download(file, output)
		except Exception as exceptions: exit(exceptions)
	elif tanya in list('tT'):
		exit('[!] Program Diberhentikan')
	else:
		exit('[!] Jawaban Tidak Ada')


if __name__ == '__main__':
	main_main()
