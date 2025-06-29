# nih script untuk doxing sudah jadi, nanti kalau ada yang error bisa langsung chat gw aja, +6289519450908
# SUMBER: https://whatsapp.com/channel/0029VagB9OYJJhzZIjgXGd11

#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import csv
import random
import platform
import getpass
import requests
from googlesearch import search
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from datetime import datetime
import json
import webbrowser
from urllib.parse import urlparse
import whois
import socket
import ssl

MAX_RESULTS = 500
SAVE_DIR = "result"
PROXY_FILE = "/sdcard/proxy.txt"
PROXY_DOWNLOAD_URL = "https://raw.githubusercontent.com/Hosting-git/all_tools/refs/heads/main/proxy.txt"

def install_module(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for modul, pip_name in [("googlesearch", "googlesearch-python"),
                        ("rich", "rich"),
                        ("requests", "requests"),
                        ("whois", "python-whois"),
                        ("bs4", "beautifulsoup4")]:
    try:
        __import__(modul)
    except ModuleNotFoundError:
        install_module(pip_name)

console = Console()
os.makedirs(SAVE_DIR, exist_ok=True)

def download_proxy_file():
    proxy_dir = os.path.dirname(PROXY_FILE)
    if not os.path.exists(proxy_dir):
        os.makedirs(proxy_dir, exist_ok=True)
    try:
        r = requests.get(PROXY_DOWNLOAD_URL, timeout=10)
        r.raise_for_status()
        with open(PROXY_FILE, "w") as f:
            f.write(r.text)
        console.print(f"[green]Proxy file berhasil diunduh ke {PROXY_FILE}[/green]")
    except Exception as e:
        console.print(f"[red]Gagal mengunduh proxy file: {e}[/red]")

if not os.path.exists(PROXY_FILE):
    download_proxy_file()

def load_proxies(filename=PROXY_FILE):
    proxies = []
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if not (line.startswith("http://") or line.startswith("https://")):
                    proxy_url = f"http://{line}"
                else:
                    proxy_url = line
                proxies.append({"http": proxy_url, "https": proxy_url})
    except Exception as e:
        console.print(f"[red]Gagal memuat proxy: {e}[/red]")
    return proxies

proxies_list = load_proxies()
def get_random_proxy():
    return random.choice(proxies_list) if proxies_list else None

def get_random_user_agent():
    uas = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1"
    ]
    return random.choice(uas)

msg = {
    "sistem_terdeteksi": "Sistem Terdeteksi:",
    "masukkan_dork": "Masukkan dork:",
    "filter_domain": "Filter domain (misalnya .com, .gov):",
    "jumlah_hasil": "Jumlah hasil (1-100):",
    "delay_permintaan": "Delay antar permintaan (detik):",
    "hasil_disimpan": "Berhasil menyimpan {n} hasil ke {file}",
    "tidak_ada_hasil": "Tidak ada hasil ditemukan.",
    "tekan_enter": "Tekan Enter untuk melanjutkan...",
    "opsi_tidak_valid": "Opsi tidak valid! Silakan coba lagi.",
    "keluar": "Keluar...",
    "pilih_opsi": "Pilih opsi:",
    "menu_utama": "Menu Utama",
    "info_lanjutan": "Pengumpulan Informasi Website Lanjutan",
    "doxing": "Doxing",
    "masukkan_target": "Masukkan target doxing (misalnya email atau nama):",
    "masukkan_jumlah": "Masukkan jumlah hasil doxing (1-50):",
    "hasil_doxing": "Hasil Doxing:",
    "tentang_alat": "Tentang Alat Ini",
    "hapus_hasil": "Hapus Semua Hasil",
    "lihat_riwayat": "Lihat Riwayat Penelitian"
}

def detect_terminal():
    if os.environ.get("TERMUX_VERSION"):
        return "Termux"
    s = platform.system()
    if s == "Linux":
        try:
            with open("/etc/os-release") as f:
                for baris in f:
                    if baris.startswith("PRETTY_NAME="):
                        return baris.split('=')[1].strip().strip('"')
        except Exception:
            return "Linux"
    elif s == "Windows":
        return "Windows"
    elif s == "Darwin":
        return "macOS"
    return s

sistem_terdeteksi = detect_terminal()
console.print(f"[bold cyan]{msg['sistem_terdeteksi']}[/bold cyan] {sistem_terdeteksi}\n")

def generate_filename():
    files = os.listdir(SAVE_DIR)
    nums = []
    for f in files:
        if f.startswith("hasil-") and f.endswith(".txt"):
            try:
                nums.append(int(f[len("hasil-"):-len(".txt")]))
            except:
                continue
    next_num = max(nums) + 1 if nums else 1
    return os.path.join(SAVE_DIR, f"hasil-{next_num}.txt")

banner_text = r"""
  ____  _____ ____  _   _ _____ _____ ____  
 |  _ \| ____|  _ \| | | | ____|_   _/ ___| 
 | |_) |  _| | |_) | |_| |  _|   | | \___ \ 
 |  _ <| |___|  __/|  _  | |___  | |  ___) |
 |_| \_\_____|_|   |_| |_|_____| |_| |____/ 
"""

def display_banner():
    panel = Panel.fit(banner_text, title="[bold cyan]Security Research Tool[/bold cyan]",
                      subtitle="[bold magenta]Untuk pengujian yang diotorisasi saja[/bold magenta]", style="blue")
    console.print(panel)

def loading_animation(message="Memuat", duration=2):
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                  TimeElapsedColumn(), transient=True) as progress:
        task = progress.add_task(f"{message}...", total=duration)
        start = time.time()
        while time.time() - start < duration:
            progress.update(task, completed=time.time() - start)
            time.sleep(0.1)

def get_system_info():
    try:
        ip = requests.get("https://api.ipify.org", timeout=5).text
    except:
        ip = "Tidak Diketahui"
    return {"username": getpass.getuser(), "sistem": platform.system(),
            "rilis": platform.release(), "public_ip": ip,
            "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

def print_menu():
    table = Table(title=f"[bold yellow]{msg['menu_utama']}[/bold yellow]", show_header=False, header_style="bold magenta")
    table.add_row("[green]1[/green]", "Mulai Pencarian Google Dork")
    table.add_row("[green]2[/green]", "Lihat Hasil Terakhir")
    table.add_row("[green]3[/green]", "Generate Random Dorks")
    table.add_row("[green]4[/green]", "Ekspor Hasil ke CSV")
    table.add_row("[green]5[/green]", msg["info_lanjutan"])
    table.add_row("[green]6[/green]", msg["lihat_riwayat"])
    table.add_row("[green]7[/green]", msg["hapus_hasil"])
    table.add_row("[green]8[/green]", msg["tentang_alat"])
    table.add_row("[green]9[/green]", msg["doxing"])
    table.add_row("[green]0[/green]", "Keluar")
    console.print(table)

# Menu 1: Pencarian Google Dork dengan retry eksponensial yang lebih kuat
def perform_search():
    try:
        query = console.input(f"[bold red]{msg['masukkan_dork']}[/bold red] ").strip()
        domain = console.input(f"[bold red]{msg['filter_domain']}[/bold red] ").strip()
        if domain:
            query += f" site:{domain}"
        pages = int(console.input(f"[bold red]{msg['jumlah_hasil']}[/bold red] "))
        if pages < 1 or pages > 100:
            console.print("[red]Jumlah hasil harus antara 1 sampai 100.[/red]")
            return
        delay = int(console.input(f"[bold red]{msg['delay_permintaan']}[/bold red] "))
        if delay < 1:
            console.print("[red]Delay minimal 1 detik.[/red]")
            return
        filename = generate_filename()
        console.print(f"\n[bold]Hasil akan disimpan ke:[/bold] [green]{filename}[/green]\n")
        loading_animation("Mencari", duration=2)
        results = []

        # Fungsi search dengan retry eksponensial berulang tanpa henti (hingga sukses)
        def search_with_retry(query, num_results, base_delay=5):
            attempt = 0
            while True:
                try:
                    return list(search(query, num_results=num_results))
                except requests.exceptions.HTTPError as err:
                    if err.response.status_code == 429:
                        delay_retry = base_delay * (2 ** attempt)
                        console.print(f"[yellow]Error 429. Mencoba ulang dalam {delay_retry} detik (Attempt {attempt+1})[/yellow]")
                        time.sleep(delay_retry)
                        attempt += 1
                    else:
                        raise err

        try:
            original_get = requests.get
            def patched_get(*args, **kwargs):
                headers = kwargs.get('headers', {})
                headers['User-Agent'] = get_random_user_agent()
                kwargs['headers'] = headers
                proxy = get_random_proxy()
                if proxy:
                    kwargs['proxies'] = proxy
                return original_get(*args, **kwargs)
            requests.get = patched_get

            results = search_with_retry(query, num_results=pages)
            for url in results:
                console.print(f"[white]{len(results)}. [green]{url}[/green]")
                time.sleep(delay)
                if len(results) >= MAX_RESULTS:
                    console.print("[yellow]Jumlah hasil maksimum tercapai. Berhenti...[/yellow]")
                    break
            requests.get = original_get
        except Exception as e:
            console.print(f"[red]Error pencarian: {e}[/red]")
        if results:
            with open(filename, 'w') as f:
                f.write("\n".join(results))
            console.print(f"\n[green]{msg['hasil_disimpan'].format(n=len(results), file=filename)}[/green]\n")
        else:
            console.print(f"\n[yellow]{msg['tidak_ada_hasil']}[/yellow]\n")
    except ValueError:
        console.print("[red]Input tidak valid! Harap masukkan angka di tempat yang diperlukan.[/red]")
    except KeyboardInterrupt:
        console.print("\n[red]Pencarian dibatalkan oleh pengguna.[/red]")

def view_results():
    files = [f for f in os.listdir(SAVE_DIR) if f.startswith("hasil-") and f.endswith(".txt")]
    if not files:
        console.print("\n[yellow]Tidak ada file hasil yang ditemukan.[/yellow]\n")
        return
    files.sort(key=lambda x: int(x[len("hasil-"):-len(".txt")]) if x[len("hasil-"):-len(".txt")].isdigit() else 0, reverse=True)
    latest_file = os.path.join(SAVE_DIR, files[0])
    try:
        with open(latest_file, 'r') as f:
            content = f.read().splitlines()
        table = Table(title=f"[bold green]Hasil dari {latest_file}[/bold green]")
        table.add_column("No", justify="right")
        table.add_column("URL", style="cyan")
        for idx, url in enumerate(content[:20], 1):
            table.add_row(str(idx), url)
        console.print(table)
        console.print(f"\n[dim]Menampilkan 20 dari {len(content)} hasil. Lihat file lengkap untuk daftar selengkapnya.[/dim]\n")
    except Exception as e:
        console.print(f"[red]Error membaca file: {e}[/red]")

def generate_random_dorks():
    dork_categories = {
        "Files": [
            "intitle:index.of inurl:ktp (ext:pdf OR ext:xls OR ext:doc OR ext:zip)",
            "intitle:index.of inurl:kk (ext:pdf OR ext:xls OR ext:doc OR ext:zip)",
            "intitle:index.of inurl:sim (ext:pdf OR ext:xls OR ext:doc OR ext:zip)",
            "intitle:index.of inurl:data pegawai (ext:pdf OR ext:xls OR ext:doc)",
            "intitle:index.of inurl:anggaran dpr (ext:pdf OR ext:xls OR ext:doc)",
            "index of/ ktp",
            "index of/ kk",
            "index of/ dokumen database",
            "index of/ data pegawai",
            "directory: file penting",
            "file: ktp AND kk AND sim",
            "file: laporan dpr AND anggaran",
            "intext:KTP filetype:pdf",
            "intext:KK filetype:doc",
            "intext:DPR filetype:xls",
            "intext:SENSITIF AND DPR filetype:zip",
            "intext:PRIVATE OR confidential ext:pdf",
            "intitle:index.of inurl:biodata (ext:pdf OR ext:xls OR ext:doc OR ext:zip)",
            "intitle:index.of inurl:cv (ext:pdf OR ext:xls OR ext:doc OR ext:zip)",
            "intitle:index.of inurl:resumé (ext:pdf OR ext:xls OR ext:doc OR ext:zip)",
            "filetype:pdf biodata OR cv OR resumé",
            "filetype:xls biodata OR cv OR resumé",
            "intitle:index.of inurl:profile (ext:pdf OR ext:xls OR ext:doc)",
            "intitle:index.of inurl:personal information (ext:pdf OR ext:xls OR ext:doc)",
            "intext:biodata AND filetype:pdf",
            "intext:cv AND filetype:doc",
            "intext:resumé AND filetype:xls",
            "intext:personal details AND ext:pdf",
            "directory: dokumen kominfo filetype:pdf",
            "directory: laporan kominfo filetype:pdf",
            "directory: data pegawai kominfo filetype:pdf",
            "intitle:index.of inurl:kominfo ext:pdf",
            "filetype:pdf site:kominfo.go.id biodata",
            "filetype:pdf site:kominfo.go.id profile",
            "filetype:pdf site:kominfo.go.id data pegawai",
            "filetype:pdf inurl:ktp biodata",
            "filetype:pdf inurl:kk biodata",
            "filetype:pdf inurl:sim biodata",
            "intitle:index.of intext:ktp ext:pdf",
            "intitle:index.of intext:kk ext:pdf",
            "intitle:index.of intext:sim ext:pdf",
            "intitle:index.of inurl:data ext:pdf AND biodata",
            "intext:Kartu Tanda Penduduk AND filetype:pdf",
            "intext:Kartu Keluarga AND filetype:pdf",
            "intext:Sistem Informasi Manajemen Kependudukan filetype:pdf",
            "intitle:index.of AND filetype:pdf AND ktp OR kk OR sim",
            "filetype:pdf biodata pegawai",
            "filetype:pdf biodata aparatur sipil negara",
            "filetype:pdf daftar nama pegawai kominfo",
            "filetype:pdf profil pegawai site:kominfo.go.id",
            "filetype:pdf site:kominfo.go.id daftar pegawai biodata",
            "intitle:index.of AND filetype:pdf biodata AND inurl:pegawai",
            "biodata AND filetype:pdf site:kominfo.go.id"
        ],
        "Admin Pages": [
            "intitle:admin", "inurl:admin", "inurl:login", "intitle:login", "intext:administrator",
            "inurl:dashboard", "inurl:adminpanel", "inurl:cpanel", "intitle:\"control panel\"", "inurl:manage"
        ],
        "Sensitive Info": [
            "intitle:index.of", "intext:password", "intext:username", "intext:credentials", "intext:secret",
            "intext:confidential", "intext:private", "intext:backup", "intext:\"database dump\"", "intext:\"sql dump\""
        ],
        "Vulnerabilities": [
            "inurl:wp-config.php", "inurl:config.php", "inurl:phpinfo.php", "inurl:shell.php", "inurl:adminer.php",
            "inurl:login.php", "inurl:upload.php", "inurl:exec.php", "inurl:cmd.php", "inurl:debug"
        ],
        "Databases": [
            "filetype:sql", "intext:\"DB_PASSWORD\"", "intext:\"DB_USER\"", "intext:\"DB_HOST\"", "intext:\"mysql_fetch_array\"",
            "intext:\"SQL syntax\"", "intext:\"Warning: mysql_connect()\"", "intext:\"phpMyAdmin\"", "inurl:phpmyadmin", "intext:\"database error\""
        ]
    }
    random.shuffle(dork_categories["Files"])
    for kategori, dorks in dork_categories.items():
        selected = random.choice(dorks)
        console.print(f"[bold]{kategori}:[/bold] [green]{selected}[/green]")
    console.print("\n[dim]Gabungkan dengan site:contoh.com untuk target spesifik.[/dim]\n")

def export_to_csv():
    files = [f for f in os.listdir(SAVE_DIR) if f.startswith("hasil-") and f.endswith(".txt")]
    if not files:
        console.print("\n[yellow]Tidak ada file hasil yang ditemukan untuk diekspor.[/yellow]\n")
        return
    files.sort(key=lambda x: int(x[len("hasil-"):-len(".txt")]) if x[len("hasil-"):-len(".txt")].isdigit() else 0, reverse=True)
    latest_file = os.path.join(SAVE_DIR, files[0])
    csv_file = latest_file.replace(".txt", ".csv")
    try:
        with open(latest_file, 'r') as infile:
            urls = [baris.strip() for baris in infile if baris.strip()]
        if not urls:
            console.print("\n[yellow]Tidak ada URL yang ditemukan dalam file tersebut.[/yellow]\n")
            return
        with open(csv_file, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["ID", "URL", "Domain"])
            for idx, url in enumerate(urls, 1):
                domain = urlparse(url).netloc
                writer.writerow([idx, url, domain])
        console.print(f"\n[green]{msg['hasil_disimpan'].format(n=len(urls), file=csv_file)}[/green]\n")
    except Exception as e:
        console.print(f"[red]Ekspor gagal: {e}[/red]")

def website_info_gathering():
    url = console.input("\n[bold]Masukkan URL yang akan dianalisis (misalnya: contoh.com):[/bold] ").strip()
    if not url:
        console.print("[red]URL tidak boleh kosong![/red]")
        return
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    try:
        console.print("\n[bold cyan]Mengumpulkan informasi lanjutan...[/bold cyan]\n")
        start_time = time.time()
        response = requests.get(url, timeout=10)
        elapsed = time.time() - start_time
        console.print(f"[bold green]Status HTTP:[/bold green] {response.status_code}")
        console.print(f"[bold green]Waktu Respons:[/bold green] {elapsed:.2f} detik")
        final_url = response.url
        console.print(f"[bold green]URL Akhir:[/bold green] {final_url}")
        if response.history:
            chain = " -> ".join(r.url for r in response.history) + " -> " + response.url
            console.print(f"[bold green]Redirect Chain:[/bold green] {chain}")
        html = response.text
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string.strip() if soup.title else "Judul tidak ditemukan"
        meta_desc = ""
        meta_keywords = ""
        generator = ""
        h1_tags = [h1.get_text(strip=True) for h1 in soup.find_all("h1")]
        for meta in soup.find_all("meta"):
            nama = meta.get("name", "").lower()
            if nama == "description":
                meta_desc = meta.get("content", "").strip()
            if nama == "keywords":
                meta_keywords = meta.get("content", "").strip()
            if nama == "generator":
                generator = meta.get("content", "").strip()
        console.print(f"[bold green]Judul Halaman:[/bold green] {title}")
        console.print(f"[bold green]Meta Deskripsi:[/bold green] {meta_desc if meta_desc else 'Tidak Tersedia'}")
        console.print(f"[bold green]Meta Keywords:[/bold green] {meta_keywords if meta_keywords else 'Tidak Tersedia'}")
        console.print(f"[bold green]CMS/Generator:[/bold green] {generator if generator else 'Tidak Terdeteksi'}")
        if h1_tags:
            console.print(f"[bold green]Tag H1:[/bold green] {', '.join(h1_tags)}")
        else:
            console.print(f"[bold green]Tag H1:[/bold green] Tidak ditemukan")
        domain = urlparse(url).netloc
        try:
            ip_address = socket.gethostbyname(domain)
            console.print(f"[bold green]IP Terdeteksi:[/bold green] {ip_address}")
        except Exception as dns_err:
            console.print(f"[red]DNS lookup gagal: {dns_err}[/red]")
        loading_animation("Melakukan WHOIS lookup", duration=2)
        try:
            domain_info = whois.whois(domain)
            console.print("\n[bold green]Informasi WHOIS:[/bold green]")
            console.print(json.dumps(domain_info, indent=2, default=str))
        except Exception as e:
            console.print(f"[red]WHOIS lookup gagal: {e}[/red]")
        loading_animation("Mengambil HTTP headers", duration=2)
        console.print("\n[bold green]HTTP Headers:[/bold green]")
        security_headers = ["Content-Security-Policy", "X-Frame-Options", "X-XSS-Protection", "Strict-Transport-Security"]
        for header, value in response.headers.items():
            marker = "[*]" if header in security_headers else ""
            console.print(f"[cyan]{header}:[/cyan] {value} {marker}")
        if response.cookies.get_dict():
            console.print(f"[bold green]Cookies:[/bold green] {response.cookies.get_dict()}")
        if url.startswith("https://"):
            try:
                ctx = ssl.create_default_context()
                with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
                    s.settimeout(5.0)
                    s.connect((domain, 443))
                    cert_bin = s.getpeercert(binary_form=True)
                cert_pem = ssl.DER_cert_to_PEM_cert(cert_bin)
                temp_cert = "temp_cert.pem"
                with open(temp_cert, "w") as f:
                    f.write(cert_pem)
                cert_details = ssl._ssl._test_decode_cert(temp_cert)
                os.remove(temp_cert)
                console.print("\n[bold green]Info Sertifikat SSL:[/bold green]")
                console.print(json.dumps(cert_details, indent=2))
            except Exception as e:
                console.print(f"[red]Gagal mengambil sertifikat SSL: {e}[/red]")
        common_ports = {80: "HTTP", 443: "HTTPS", 22: "SSH", 21: "FTP"}
        console.print("\n[bold green]Pemeriksaan Port (port umum):[/bold green]")
        for port, service in common_ports.items():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((domain, port))
            status = "Terbuka" if result == 0 else "Tertutup"
            console.print(f"Port {port} ({service}): {status}")
            sock.close()
        loading_animation("Mendeteksi teknologi", duration=2)
        tech_url = f"https://builtwith.com/{domain}"
        console.print(f"\n[bold green]Deteksi Teknologi:[/bold green]")
        console.print(f"Kunjungi [blue]{tech_url}[/blue] untuk profil teknologi secara detail")
        webbrowser.open(tech_url)
    except Exception as e:
        console.print(f"\n[red]Error saat analisis lanjutan: {e}[/red]\n")

def doxing_info():
    target = console.input(f"\n[bold red]{msg['masukkan_target']}[/bold red] ").strip()
    if not target:
        console.print("[red]Target tidak boleh kosong![/red]")
        return
    try:
        jumlah = int(console.input(f"[bold red]{msg['masukkan_jumlah']}[/bold red] "))
        if jumlah < 1 or jumlah > 50:
            console.print("[red]Jumlah hasil harus antara 1 sampai 50.[/red]")
            return
    except ValueError:
        console.print("[red]Input jumlah tidak valid![/red]")
        return

    query_list = [
        f'"{target}"',
        f'"{target}" site:linkedin.com',
        f'"{target}" site:facebook.com',
        f'"{target}" site:twitter.com',
        f'"{target}" site:instagram.com',
        f'"{target}" site:reddit.com',
        f'"{target}" site:youtube.com',
        f'"{target}" site:github.com',
        f'"{target}" site:medium.com',
        f'"{target}" site:quora.com',
        f'"{target}" site:blogspot.com',
        f'"{target}" site:wordpress.com'
    ]
    random.shuffle(query_list)
    hasil_set = set()
    console.print(f"\n[bold cyan]{msg['hasil_doxing']}[/bold cyan]")
    original_get = requests.get
    def patched_get(*args, **kwargs):
        headers = kwargs.get('headers', {})
        headers['User-Agent'] = get_random_user_agent()
        kwargs['headers'] = headers
        proxy = get_random_proxy()
        if proxy:
            kwargs['proxies'] = proxy
        return original_get(*args, **kwargs)
    requests.get = patched_get

    # Fungsi search dengan retry eksponensial berulang hingga sukses (maksimal 10 kali)
    def search_with_retry(query, num_results, max_retries=10, base_delay=5):
        attempt = 0
        while attempt < max_retries:
            try:
                return list(search(query, num_results=num_results))
            except requests.exceptions.HTTPError as err:
                if err.response.status_code == 429:
                    delay_retry = base_delay * (2 ** attempt)
                    console.print(f"[yellow]Error 429. Mencoba ulang dalam {delay_retry} detik (Attempt {attempt+1}/{max_retries})[/yellow]")
                    time.sleep(delay_retry)
                    attempt += 1
                else:
                    raise err
        return []

    try:
        for q in query_list:
            results = search_with_retry(q, num_results=jumlah)
            for url in results:
                hasil_set.add(url)
                if len(hasil_set) >= jumlah:
                    break
            if len(hasil_set) >= jumlah:
                break
            time.sleep(random.uniform(1, 3))
        if hasil_set:
            for idx, url in enumerate(hasil_set, 1):
                if idx > jumlah:
                    break
                console.print(f"[green]{idx}. {url}[/green]")
        else:
            console.print("[yellow]Tidak ada informasi publik ditemukan.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error saat doxing: {e}[/red]")
    requests.get = original_get

def view_history():
    files = [f for f in os.listdir(SAVE_DIR) if f.startswith("hasil-")]
    if not files:
        console.print("\n[yellow]Tidak ada file penelitian yang ditemukan.[/yellow]\n")
        return
    files.sort(key=lambda x: int(x[len("hasil-"):-len(".txt")]) if x[len("hasil-"):-len(".txt")].isdigit() else 0, reverse=True)
    table = Table(title="[bold green]Riwayat Penelitian[/bold green]")
    table.add_column("Tanggal", justify="left")
    table.add_column("Nama File", style="cyan")
    table.add_column("Tipe", justify="center")
    for file in files[:10]:
        file_date = datetime.fromtimestamp(os.path.getmtime(os.path.join(SAVE_DIR, file))).strftime("%Y-%m-%d %H:%M")
        file_type = "Dork"
        table.add_row(file_date, file, file_type)
    console.print(table)
    console.print(f"\n[dim]Menampilkan {min(10, len(files))} dari {len(files)} file[/dim]\n")

def clear_results():
    confirm = console.input(f"\n[bold red]Yakin ingin menghapus SEMUA file penelitian? (y/n):[/bold red] ").lower()
    if confirm == 'y':
        try:
            loading_animation("Menghapus hasil", duration=2)
            for file in os.listdir(SAVE_DIR):
                os.remove(os.path.join(SAVE_DIR, file))
            console.print("\n[green]Semua file penelitian telah dihapus.[/green]\n")
        except Exception as e:
            console.print(f"\n[red]Error menghapus file: {e}[/red]\n")
    else:
        console.print("\n[cyan]Operasi dibatalkan.[/cyan]\n")

def about_tool():
    info = f"""
[bold cyan]Security Research Tool[/bold cyan]

[bold]Versi:[/bold] 2.0
[bold]Pengembang:[/bold] Ethical Security Researcher

[bold]Fitur:[/bold]
- Pencarian Google Dork dengan filter
- Organisasi dan ekspor hasil
- Pengumpulan Informasi Website Lanjutan yang sangat lengkap dan detail,
  termasuk redirect chain, cookies, header, dan info sertifikat SSL secara mendalam
- Fitur Doxing (gunakan etis!)
- Riwayat Penelitian

[bold]Penting:[/bold]
Alat ini hanya untuk [red]pengujian keamanan yang diotorisasi[/red].
Penggunaan tanpa izin dapat melanggar hukum.

[bold]Disclaimer:[/bold]
Pengembang tidak bertanggung jawab atas penyalahgunaan alat ini.
Selalu dapatkan izin sebelum menguji sistem apa pun.
"""
    console.print(Panel.fit(info, title=f"[bold cyan]{msg['tentang_alat']}[/bold cyan]", style="blue"))

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    display_banner()
    while True:
        print_menu()
        choice = console.input(f"\n[bold yellow]{msg['pilih_opsi']}[/bold yellow] ").strip()
        if choice == "1":
            perform_search()
        elif choice == "2":
            view_results()
        elif choice == "3":
            generate_random_dorks()
        elif choice == "4":
            export_to_csv()
        elif choice == "5":
            website_info_gathering()
        elif choice == "6":
            view_history()
        elif choice == "7":
            clear_results()
        elif choice == "8":
            about_tool()
        elif choice == "9":
            doxing_info()
        elif choice == "0":
            loading_animation("Keluar", duration=1)
            console.print(f"\n[cyan]{msg['keluar']}[/cyan]\n")
            break
        else:
            console.print(f"[red]{msg['opsi_tidak_valid']}[/red]")
        console.input(f"\n[cyan]{msg['tekan_enter']}[/cyan]")
        os.system('cls' if os.name == 'nt' else 'clear')
        display_banner()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Program dihentikan oleh pengguna.[/red]\n")
    except Exception as e:
        console.print(f"\n[red]Critical error: {e}[/red]\n")
