#!/usr/bin/env python3
_d='proxies'
_c='User-Agent'
_b='Keluar'
_a='lihat_riwayat'
_Z='hapus_hasil'
_Y='hasil_doxing'
_X='masukkan_jumlah'
_W='masukkan_target'
_V='doxing'
_U='info_lanjutan'
_T='menu_utama'
_S='pilih_opsi'
_R='keluar'
_Q='opsi_tidak_valid'
_P='tekan_enter'
_O='tidak_ada_hasil'
_N='delay_permintaan'
_M='jumlah_hasil'
_L='filter_domain'
_K='masukkan_dork'
_J='sistem_terdeteksi'
_I='requests'
_H='tentang_alat'
_G='hasil_disimpan'
_F='https://'
_E='http://'
_D='headers'
_C=True
_B='.txt'
_A='hasil-'
import os,sys,subprocess,time,csv,random,platform,getpass,requests
from googlesearch import search
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress,SpinnerColumn,TextColumn,TimeElapsedColumn
from datetime import datetime
import json,webbrowser
from urllib.parse import urlparse
import whois,socket,ssl
MAX_RESULTS=500
SAVE_DIR='result'
PROXY_FILE='/sdcard/cp/proxy.txt'
PROXY_DOWNLOAD_URL='https://raw.githubusercontent.com/Hosting-git/all_tools/refs/heads/main/proxy.txt'
def install_module(package):subprocess.check_call([sys.executable,'-m','pip','install',package])
for(modul,pip_name)in[('googlesearch','googlesearch-python'),('rich','rich'),(_I,_I),('whois','python-whois'),('bs4','beautifulsoup4')]:
	try:__import__(modul)
	except ModuleNotFoundError:install_module(pip_name)
console=Console()
os.makedirs(SAVE_DIR,exist_ok=_C)
def download_proxy_file():
	A=os.path.dirname(PROXY_FILE)
	if not os.path.exists(A):os.makedirs(A,exist_ok=_C)
	try:
		B=requests.get(PROXY_DOWNLOAD_URL,timeout=10);B.raise_for_status()
		with open(PROXY_FILE,'w')as C:C.write(B.text)
		console.print(f"[green]Proxy file berhasil diunduh ke {PROXY_FILE}[/green]")
	except Exception as D:console.print(f"[red]Gagal mengunduh proxy file: {D}[/red]")
if not os.path.exists(PROXY_FILE):download_proxy_file()
def load_proxies(filename=PROXY_FILE):
	C=[]
	try:
		with open(filename,'r')as D:
			for A in D:
				A=A.strip()
				if not A:continue
				if not(A.startswith(_E)or A.startswith(_F)):B=f"http://{A}"
				else:B=A
				C.append({'http':B,'https':B})
	except Exception as E:console.print(f"[red]Gagal memuat proxy: {E}[/red]")
	return C
proxies_list=load_proxies()
def get_random_proxy():return random.choice(proxies_list)if proxies_list else None
def get_random_user_agent():A=['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/92.0.4515.131 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/91.0.4472.114 Safari/537.36','Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1','Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1'];return random.choice(A)
msg={_J:'Sistem Terdeteksi:',_K:'Masukkan dork:',_L:'Filter domain (misalnya .com, .gov):',_M:'Jumlah hasil (1-100):',_N:'Delay antar permintaan (detik):',_G:'Berhasil menyimpan {n} hasil ke {file}',_O:'Tidak ada hasil ditemukan.',_P:'Tekan Enter untuk melanjutkan...',_Q:'Opsi tidak valid! Silakan coba lagi.',_R:'Keluar...',_S:'Pilih opsi:',_T:'Menu Utama',_U:'Pengumpulan Informasi Website Lanjutan',_V:'Doxing',_W:'Masukkan target doxing (misalnya email atau nama):',_X:'Masukkan jumlah hasil doxing (1-50):',_Y:'Hasil Doxing:',_H:'Tentang Alat Ini',_Z:'Hapus Semua Hasil',_a:'Lihat Riwayat Penelitian'}
def detect_terminal():
	D='Windows';C='Linux'
	if os.environ.get('TERMUX_VERSION'):return'Termux'
	A=platform.system()
	if A==C:
		try:
			with open('/etc/os-release')as E:
				for B in E:
					if B.startswith('PRETTY_NAME='):return B.split('=')[1].strip().strip('"')
		except Exception:return C
	elif A==D:return D
	elif A=='Darwin':return'macOS'
	return A
sistem_terdeteksi=detect_terminal()
console.print(f"[bold cyan]{msg[_J]}[/bold cyan] {sistem_terdeteksi}\n")
def generate_filename():
	C=os.listdir(SAVE_DIR);A=[]
	for B in C:
		if B.startswith(_A)and B.endswith(_B):
			try:A.append(int(B[len(_A):-len(_B)]))
			except:continue
	D=max(A)+1 if A else 1;return os.path.join(SAVE_DIR,f"hasil-{D}.txt")
banner_text='\n____      ____  _____  _  _ \n(  _ \\ ___(  _ \\(  _  )( \\/ )\n )   /(___))(_) ))(_)(  )  ( \n(_)\\_)    (____/(_____)(_/\\_)\n\nScript By ~ RenXploit | github.com/THEOYS123\n'
def display_banner():A=Panel.fit(banner_text,title='[bold cyan]R-Dox v 2.0.1 [/bold cyan]',subtitle='[bold magenta]~~~R-Dox~~~[/bold magenta]',style='blue');console.print(A)
def loading_animation(message='Memuat',duration=2):
	A=duration
	with Progress(SpinnerColumn(),TextColumn('[progress.description]{task.description}'),TimeElapsedColumn(),transient=_C)as B:
		D=B.add_task(f"{message}...",total=A);C=time.time()
		while time.time()-C<A:B.update(D,completed=time.time()-C);time.sleep(.1)
def get_system_info():
	try:A=requests.get('https://api.ipify.org',timeout=5).text
	except:A='Tidak Diketahui'
	return{'username':getpass.getuser(),'sistem':platform.system(),'rilis':platform.release(),'public_ip':A,'waktu':datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
def print_menu():A=Table(title=f"[bold yellow]{msg[_T]}[/bold yellow]",show_header=False,header_style='bold magenta');A.add_row('[green]1[/green]','Mulai Pencarian Google Dork');A.add_row('[green]2[/green]','Lihat Hasil Terakhir');A.add_row('[green]3[/green]','Create Random Dorks');A.add_row('[green]4[/green]','Ekspor Hasil ke CSV');A.add_row('[green]5[/green]',msg[_U]);A.add_row('[green]6[/green]',msg[_a]);A.add_row('[green]7[/green]',msg[_Z]);A.add_row('[green]8[/green]',msg[_H]);A.add_row('[green]9[/green]',msg[_V]);A.add_row('[green]0[/green]',_b);console.print(A)
def perform_search():
	try:
		D=console.input(f"[bold red]{msg[_K]}[/bold red] ").strip();E=console.input(f"[bold red]{msg[_L]}[/bold red] ").strip()
		if E:D+=f" site:{E}"
		B=int(console.input(f"[bold red]{msg[_M]}[/bold red] "))
		if B<1 or B>100:console.print('[red]Jumlah hasil harus antara 1 sampai 100.[/red]');return
		F=int(console.input(f"[bold red]{msg[_N]}[/bold red] "))
		if F<1:console.print('[red]Delay minimal 1 detik.[/red]');return
		C=generate_filename();console.print(f"\n[bold]Hasil akan disimpan ke:[/bold] [green]{C}[/green]\n");loading_animation('Mencari',duration=2);A=[]
		try:
			G=requests.get
			def I(*D,**A):
				B=A.get(_D,{});B[_c]=get_random_user_agent();A[_D]=B;C=get_random_proxy()
				if C:A[_d]=C
				return G(*D,**A)
			requests.get=I
			for H in search(D,num_results=B):
				A.append(H);console.print(f"[white]{len(A)}. [green]{H}[/green]");time.sleep(F)
				if len(A)>=MAX_RESULTS:console.print('[yellow]Jumlah hasil maksimum tercapai. Berhenti...[/yellow]');break
			requests.get=G
		except Exception as J:console.print(f"[red]Error pencarian: {J}[/red]")
		if A:
			with open(C,'w')as K:K.write('\n'.join(A))
			console.print(f"\n[green]{msg[_G].format(n=len(A),file=C)}[/green]\n")
		else:console.print(f"\n[yellow]{msg[_O]}[/yellow]\n")
	except ValueError:console.print('[red]Input tidak valid! Harap masukkan angka di tempat yang diperlukan.[/red]')
	except KeyboardInterrupt:console.print('\n[red]Pencarian dibatalkan oleh pengguna.[/red]')
def view_results():
	B=[A for A in os.listdir(SAVE_DIR)if A.startswith(_A)and A.endswith(_B)]
	if not B:console.print('\n[yellow]Tidak ada file hasil yang ditemukan.[/yellow]\n');return
	B.sort(key=lambda x:int(x[len(_A):-len(_B)])if x[len(_A):-len(_B)].isdigit()else 0,reverse=_C);C=os.path.join(SAVE_DIR,B[0])
	try:
		with open(C,'r')as E:D=E.read().splitlines()
		A=Table(title=f"[bold green]Hasil dari {C}[/bold green]");A.add_column('No',justify='right');A.add_column('URL',style='cyan')
		for(F,G)in enumerate(D[:20],1):A.add_row(str(F),G)
		console.print(A);console.print(f"\n[dim]Menampilkan 20 dari {len(D)} hasil. Lihat file lengkap untuk daftar selengkapnya.[/dim]\n")
	except Exception as H:console.print(f"[red]Error membaca file: {H}[/red]")
def generate_random_dorks():
	B='Files';A={B:['intitle:index.of inurl:ktp (ext:pdf OR ext:xls OR ext:doc OR ext:zip)','intitle:index.of inurl:kk (ext:pdf OR ext:xls OR ext:doc OR ext:zip)','intitle:index.of inurl:sim (ext:pdf OR ext:xls OR ext:doc OR ext:zip)','intitle:index.of inurl:data pegawai (ext:pdf OR ext:xls OR ext:doc)','intitle:index.of inurl:anggaran dpr (ext:pdf OR ext:xls OR ext:doc)','index of/ ktp','index of/ kk','index of/ dokumen database','index of/ data pegawai','directory: file penting','file: ktp AND kk AND sim','file: laporan dpr AND anggaran','intext:KTP filetype:pdf','intext:KK filetype:doc','intext:DPR filetype:xls','intext:SENSITIF AND DPR filetype:zip','intext:PRIVATE OR confidential ext:pdf','intitle:index.of inurl:biodata (ext:pdf OR ext:xls OR ext:doc OR ext:zip)','intitle:index.of inurl:cv (ext:pdf OR ext:xls OR ext:doc OR ext:zip)','intitle:index.of inurl:resumé (ext:pdf OR ext:xls OR ext:doc OR ext:zip)','filetype:pdf biodata OR cv OR resumé','filetype:xls biodata OR cv OR resumé','intitle:index.of inurl:profile (ext:pdf OR ext:xls OR ext:doc)','intitle:index.of inurl:personal information (ext:pdf OR ext:xls OR ext:doc)','intext:biodata AND filetype:pdf','intext:cv AND filetype:doc','intext:resumé AND filetype:xls','intext:personal details AND ext:pdf','directory: dokumen kominfo filetype:pdf','directory: laporan kominfo filetype:pdf','directory: data pegawai kominfo filetype:pdf','intitle:index.of inurl:kominfo ext:pdf','filetype:pdf site:kominfo.go.id biodata','filetype:pdf site:kominfo.go.id profile','filetype:pdf site:kominfo.go.id data pegawai','filetype:pdf inurl:ktp biodata','filetype:pdf inurl:kk biodata','filetype:pdf inurl:sim biodata','intitle:index.of intext:ktp ext:pdf','intitle:index.of intext:kk ext:pdf','intitle:index.of intext:sim ext:pdf','intitle:index.of inurl:data ext:pdf AND biodata','intext:Kartu Tanda Penduduk AND filetype:pdf','intext:Kartu Keluarga AND filetype:pdf','intext:Sistem Informasi Manajemen Kependudukan filetype:pdf','intitle:index.of AND filetype:pdf AND ktp OR kk OR sim','filetype:pdf biodata pegawai','filetype:pdf biodata aparatur sipil negara','filetype:pdf daftar nama pegawai kominfo','filetype:pdf profil pegawai site:kominfo.go.id','filetype:pdf site:kominfo.go.id daftar pegawai biodata','intitle:index.of AND filetype:pdf biodata AND inurl:pegawai','biodata AND filetype:pdf site:kominfo.go.id'],'Admin Pages':['intitle:admin','inurl:admin','inurl:login','intitle:login','intext:administrator','inurl:dashboard','inurl:adminpanel','inurl:cpanel','intitle:"control panel"','inurl:manage'],'Sensitive Info':['intitle:index.of','intext:password','intext:username','intext:credentials','intext:secret','intext:confidential','intext:private','intext:backup','intext:"database dump"','intext:"sql dump"'],'Vulnerabilities':['inurl:wp-config.php','inurl:config.php','inurl:phpinfo.php','inurl:shell.php','inurl:adminer.php','inurl:login.php','inurl:upload.php','inurl:exec.php','inurl:cmd.php','inurl:debug'],'Databases':['filetype:sql','intext:"DB_PASSWORD"','intext:"DB_USER"','intext:"DB_HOST"','intext:"mysql_fetch_array"','intext:"SQL syntax"','intext:"Warning: mysql_connect()"','intext:"phpMyAdmin"','inurl:phpmyadmin','intext:"database error"']};random.shuffle(A[B])
	for(C,D)in A.items():E=random.choice(D);console.print(f"[bold]{C}:[/bold] [green]{E}[/green]")
	console.print('\n[dim]Gabungkan dengan site:contoh.com untuk target spesifik.[/dim]\n')
def export_to_csv():
	A=[A for A in os.listdir(SAVE_DIR)if A.startswith(_A)and A.endswith(_B)]
	if not A:console.print('\n[yellow]Tidak ada file hasil yang ditemukan untuk diekspor.[/yellow]\n');return
	A.sort(key=lambda x:int(x[len(_A):-len(_B)])if x[len(_A):-len(_B)].isdigit()else 0,reverse=_C);C=os.path.join(SAVE_DIR,A[0]);D=C.replace(_B,'.csv')
	try:
		with open(C,'r')as G:B=[A.strip()for A in G if A.strip()]
		if not B:console.print('\n[yellow]Tidak ada URL yang ditemukan dalam file tersebut.[/yellow]\n');return
		with open(D,'w',newline='')as H:
			E=csv.writer(H);E.writerow(['ID','URL','Domain'])
			for(I,F)in enumerate(B,1):J=urlparse(F).netloc;E.writerow([I,F,J])
		console.print(f"\n[green]{msg[_G].format(n=len(B),file=D)}[/green]\n")
	except Exception as K:console.print(f"[red]Ekspor gagal: {K}[/red]")
def website_info_gathering():
	T='Tidak Tersedia';S=' -> ';N='content';B=console.input('\n[bold]Masukkan URL yang akan dianalisis (misalnya: contoh.com):[/bold] ').strip()
	if not B:console.print('[red]URL tidak boleh kosong![/red]');return
	if not B.startswith((_E,_F)):B=_E+B
	try:
		console.print('\n[bold cyan]Mengumpulkan informasi lanjutan...[/bold cyan]\n');U=time.time();A=requests.get(B,timeout=10);V=time.time()-U;console.print(f"[bold green]Status HTTP:[/bold green] {A.status_code}");console.print(f"[bold green]Waktu Respons:[/bold green] {V:.2f} detik");W=A.url;console.print(f"[bold green]URL Akhir:[/bold green] {W}")
		if A.history:X=S.join(A.url for A in A.history)+S+A.url;console.print(f"[bold green]Redirect Chain:[/bold green] {X}")
		Y=A.text;from bs4 import BeautifulSoup as Z;E=Z(Y,'html.parser');a=E.title.string.strip()if E.title else'Judul tidak ditemukan';G='';H='';I='';O=[A.get_text(strip=_C)for A in E.find_all('h1')]
		for F in E.find_all('meta'):
			J=F.get('name','').lower()
			if J=='description':G=F.get(N,'').strip()
			if J=='keywords':H=F.get(N,'').strip()
			if J=='generator':I=F.get(N,'').strip()
		console.print(f"[bold green]Judul Halaman:[/bold green] {a}");console.print(f"[bold green]Meta Deskripsi:[/bold green] {G if G else T}");console.print(f"[bold green]Meta Keywords:[/bold green] {H if H else T}");console.print(f"[bold green]CMS/Generator:[/bold green] {I if I else'Tidak Terdeteksi'}")
		if O:console.print(f"[bold green]Tag H1:[/bold green] {', '.join(O)}")
		else:console.print(f"[bold green]Tag H1:[/bold green] Tidak ditemukan")
		C=urlparse(B).netloc
		try:b=socket.gethostbyname(C);console.print(f"[bold green]IP Terdeteksi:[/bold green] {b}")
		except Exception as c:console.print(f"[red]DNS lookup gagal: {c}[/red]")
		loading_animation('Melakukan WHOIS lookup',duration=2)
		try:d=whois.whois(C);console.print('\n[bold green]Informasi WHOIS:[/bold green]');console.print(json.dumps(d,indent=2,default=str))
		except Exception as D:console.print(f"[red]WHOIS lookup gagal: {D}[/red]")
		loading_animation('Mengambil HTTP headers',duration=2);console.print('\n[bold green]HTTP Headers:[/bold green]');e=['Content-Security-Policy','X-Frame-Options','X-XSS-Protection','Strict-Transport-Security']
		for(P,f)in A.headers.items():g='[*]'if P in e else'';console.print(f"[cyan]{P}:[/cyan] {f} {g}")
		if A.cookies.get_dict():console.print(f"[bold green]Cookies:[/bold green] {A.cookies.get_dict()}")
		if B.startswith(_F):
			try:
				h=ssl.create_default_context()
				with h.wrap_socket(socket.socket(),server_hostname=C)as K:K.settimeout(5.);K.connect((C,443));i=K.getpeercert(binary_form=_C)
				j=ssl.DER_cert_to_PEM_cert(i);L='temp_cert.pem'
				with open(L,'w')as k:k.write(j)
				l=ssl._ssl._test_decode_cert(L);os.remove(L);console.print('\n[bold green]Info Sertifikat SSL:[/bold green]');console.print(json.dumps(l,indent=2))
			except Exception as D:console.print(f"[red]Gagal mengambil sertifikat SSL: {D}[/red]")
		m={80:'HTTP',443:'HTTPS',22:'SSH',21:'FTP'};console.print('\n[bold green]Pemeriksaan Port (port umum):[/bold green]')
		for(Q,n)in m.items():M=socket.socket(socket.AF_INET,socket.SOCK_STREAM);M.settimeout(2);o=M.connect_ex((C,Q));p='Terbuka'if o==0 else'Tertutup';console.print(f"Port {Q} ({n}): {p}");M.close()
		loading_animation('Mendeteksi teknologi',duration=2);R=f"https://builtwith.com/{C}";console.print(f"\n[bold green]Deteksi Teknologi:[/bold green]");console.print(f"Kunjungi [blue]{R}[/blue] untuk profil teknologi secara detail");webbrowser.open(R)
	except Exception as D:console.print(f"\n[red]Error saat analisis lanjutan: {D}[/red]\n")
def doxing_info():
	A=console.input(f"\n[bold red]{msg[_W]}[/bold red] ").strip()
	if not A:console.print('[red]Target tidak boleh kosong![/red]');return
	try:
		B=int(console.input(f"[bold red]{msg[_X]}[/bold red] "))
		if B<1 or B>50:console.print('[red]Jumlah hasil harus antara 1 sampai 50.[/red]');return
	except ValueError:console.print('[red]Input jumlah tidak valid![/red]');return
	E=[f'"{A}"',f'"{A}" site:linkedin.com',f'"{A}" site:facebook.com',f'"{A}" site:twitter.com',f'"{A}" site:instagram.com',f'"{A}" site:reddit.com',f'"{A}" site:youtube.com',f'"{A}" site:github.com',f'"{A}" site:medium.com',f'"{A}" site:quora.com',f'"{A}" site:blogspot.com',f'"{A}" site:wordpress.com'];random.shuffle(E);C=set();console.print(f"\n[bold cyan]{msg[_Y]}[/bold cyan]");F=requests.get
	def H(*D,**A):
		B=A.get(_D,{});B[_c]=get_random_user_agent();A[_D]=B;C=get_random_proxy()
		if C:A[_d]=C
		return F(*D,**A)
	requests.get=H
	def I(query,num_results,retries=3,delay_retry=5):
		B=delay_retry;A=retries
		for D in range(A):
			try:return list(search(query,num_results=num_results))
			except requests.exceptions.HTTPError as C:
				if C.response.status_code==429:console.print(f"[yellow]Error 429. Mencoba ulang dalam {B} detik... (Attempt {D+1}/{A})[/yellow]");time.sleep(B)
				else:raise C
		return[]
	try:
		for J in E:
			K=I(J,num_results=B)
			for D in K:
				C.add(D)
				if len(C)>=B:break
			if len(C)>=B:break
			time.sleep(random.uniform(1,3))
		if C:
			for(G,D)in enumerate(C,1):
				if G>B:break
				console.print(f"[green]{G}. {D}[/green]")
		else:console.print('[yellow]Tidak ada informasi publik ditemukan.[/yellow]')
	except Exception as L:console.print(f"[red]Error saat doxing: {L}[/red]")
	requests.get=F
def view_history():
	A=[A for A in os.listdir(SAVE_DIR)if A.startswith(_A)]
	if not A:console.print('\n[yellow]Tidak ada file penelitian yang ditemukan.[/yellow]\n');return
	A.sort(key=lambda x:int(x[len(_A):-len(_B)])if x[len(_A):-len(_B)].isdigit()else 0,reverse=_C);B=Table(title='[bold green]Riwayat Penelitian[/bold green]');B.add_column('Tanggal',justify='left');B.add_column('Nama File',style='cyan');B.add_column('Tipe',justify='center')
	for C in A[:10]:D=datetime.fromtimestamp(os.path.getmtime(os.path.join(SAVE_DIR,C))).strftime('%Y-%m-%d %H:%M');E='Dork';B.add_row(D,C,E)
	console.print(B);console.print(f"\n[dim]Menampilkan {min(10,len(A))} dari {len(A)} file[/dim]\n")
def clear_results():
	A=console.input(f"\n[bold red]Yakin ingin menghapus SEMUA file penelitian? (y/n):[/bold red] ").lower()
	if A=='y':
		try:
			loading_animation('Menghapus hasil',duration=2)
			for B in os.listdir(SAVE_DIR):os.remove(os.path.join(SAVE_DIR,B))
			console.print('\n[green]Semua file penelitian telah dihapus.[/green]\n')
		except Exception as C:console.print(f"\n[red]Error menghapus file: {C}[/red]\n")
	else:console.print('\n[cyan]Operasi dibatalkan.[/cyan]\n')
def about_tool():A=f"""
[bold cyan]Security Research Tool[/bold cyan]

[bold]Versi:[/bold] 2.0
[bold]Pengembang:[/bold] Ethical Security Researcher

[bold]Fitur:[/bold]
- Pencarian Google Dork dengan filter
- Organisasi dan ekspor hasil
- Pengumpulan Informasi Website Lanjutan yang sangat lengkap
- Fitur Doxing (gunakan etis!)
- Riwayat Penelitian

[bold]Penting:[/bold]
Alat ini hanya untuk [red]pengujian keamanan yang diotorisasi[/red].
Penggunaan tanpa izin dapat melanggar hukum.

[bold]Disclaimer:[/bold]
Pengembang tidak bertanggung jawab atas penyalahgunaan alat ini.
Selalu dapatkan izin sebelum menguji sistem apa pun.
""";console.print(Panel.fit(A,title=f"[bold cyan]{msg[_H]}[/bold cyan]",style='blue'))
def main():
	C='clear';B='cls';os.system(B if os.name=='nt'else C);display_banner()
	while _C:
		print_menu();A=console.input(f"\n[bold yellow]{msg[_S]}[/bold yellow] ").strip()
		if A=='1':perform_search()
		elif A=='2':view_results()
		elif A=='3':generate_random_dorks()
		elif A=='4':export_to_csv()
		elif A=='5':website_info_gathering()
		elif A=='6':view_history()
		elif A=='7':clear_results()
		elif A=='8':about_tool()
		elif A=='9':doxing_info()
		elif A=='0':loading_animation(_b,duration=1);console.print(f"\n[cyan]{msg[_R]}[/cyan]\n");break
		else:console.print(f"[red]{msg[_Q]}[/red]")
		console.input(f"\n[cyan]{msg[_P]}[/cyan]");os.system(B if os.name=='nt'else C);display_banner()
if __name__=='__main__':
	try:main()
	except KeyboardInterrupt:console.print('\n[red]Program dihentikan oleh pengguna.[/red]\n')
	except Exception as e:console.print(f"\n[red]Critical error: {e}[/red]\n")
