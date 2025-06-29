#!/usr/bin/env python3
import os
import subprocess
import time
import csv
import random
import platform
import getpass
import re
import requests
from googlesearch import search
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn, BarColumn
from datetime import datetime
import json
import webbrowser
from urllib.parse import urlparse
import whois
import socket
import ssl
from http.client import RemoteDisconnected
import sys
from bs4 import BeautifulSoup
import threading
import math
import shutil
from rich.text import Text
from rich.live import Live
from rich.layout import Layout
from rich.columns import Columns
from rich.rule import Rule
from rich.color import Color
from rich.style import Style
from rich.markdown import Markdown
from rich.align import Align

# Konfigurasi dasar
MAX_RESULTS = 500
SAVE_DIR = "result"
PROXY_FILE = "/sdcard/proxy.txt"
PROXY_DOWNLOAD_URL = "https://raw.githubusercontent.com/Hosting-git/all_tools/refs/heads/main/proxy.txt"

# Fungsi untuk menginstall modul jika belum ada
def install_module(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for modul, pip_name in [
    ("googlesearch", "googlesearch-python"),
    ("rich", "rich"),
    ("requests", "requests"),
    ("whois", "python-whois"),
    ("bs4", "beautifulsoup4")
]:
    try:
        __import__(modul)
    except ModuleNotFoundError:
        install_module(pip_name)

console = Console()
os.makedirs(SAVE_DIR, exist_ok=True)

# Jika file proxy tidak ada, unduh secara otomatis
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
                # Jika tidak ada "http://" atau "https://" di awal, tambahkan "http://"
                proxy_url = line if (line.startswith("http://") or line.startswith("https://")) else f"http://{line}"
                proxies.append({"http": proxy_url, "https": proxy_url})
    except Exception as e:
        console.print(f"[red]Gagal memuat proxy: {e}[/red]")
    return proxies

proxies_list = load_proxies()
def get_random_proxy():
    return random.choice(proxies_list) if proxies_list else None

# Membuat pool 1000 User-Agent acak dengan variasi platform dan versi Chrome
def generate_user_agent_pool(n=1000):
    pool = []
    platforms = ["Windows NT 10.0; Win64; x64", "X11; Linux x86_64", "Macintosh; Intel Mac OS X 10_15_7"]
    browsers = ["Chrome", "Firefox", "Safari", "Edge"]
    for _ in range(n):
        plat = random.choice(platforms)
        browser = random.choice(browsers)
        if browser == "Chrome":
            version = random.randint(70, 100)
            build = random.randint(3000, 4000)
            patch = random.randint(100, 200)
            ua = f"Mozilla/5.0 ({plat}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.{build}.{patch} Safari/537.36"
        elif browser == "Firefox":
            version = random.randint(70, 100)
            patch = random.randint(0, 9)
            ua = f"Mozilla/5.0 ({plat}; rv:{version}.0) Gecko/20100101 Firefox/{version}.{patch}"
        elif browser == "Safari":
            version = random.randint(12, 15)
            patch = random.randint(0, 6)
            ua = f"Mozilla/5.0 ({plat}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{version}.{patch} Safari/605.1.15"
        else:  # Edge
            version = random.randint(80, 100)
            build = random.randint(1000, 2000)
            ua = f"Mozilla/5.0 ({plat}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.{build}.0 Safari/537.36 Edg/{version}.0.{build}.0"
        pool.append(ua)
    return pool

USER_AGENT_POOL = generate_user_agent_pool(1000)
def get_random_user_agent():
    return random.choice(USER_AGENT_POOL)

msg = {
    "sistem_terdeteksi": "Sistem Terdeteksi:",
    "masukkan_dork": "Masukkan dork:",
    "filter_domain": "Filter domain (misalnya .com, .gov):",
    "jumlah_hasil": "Masukkan jumlah hasil (1-100):",
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
    "masukkan_target": "Masukkan target doxing (nama, email, atau nomor telepon):",
    "masukkan_jumlah": "Masukkan jumlah hasil doxing (1-50):",
    "hasil_doxing": "Hasil Doxing:",
    "tentang_alat": "Tentang Alat Ini",
    "hapus_hasil": "Hapus Semua Hasil",
    "lihat_riwayat": "Lihat Riwayat Penelitian",
    "analisis_kerentanan": "Analisis Kerentanan",
    "masukkan_url": "Masukkan URL untuk analisis kerentanan:",
    "hasil_kerentanan": "Hasil Analisis Kerentanan"
}

# Fungsi untuk mendeteksi sistem
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

# Fungsi untuk menghasilkan nama file hasil
def generate_filename(prefix="hasil"):
    files = os.listdir(SAVE_DIR)
    nums = []
    for f in files:
        if f.startswith(f"{prefix}-") and f.endswith(".txt"):
            try:
                nums.append(int(f[len(f"{prefix}-"):-len(".txt")]))
            except:
                continue
    next_num = max(nums) + 1 if nums else 1
    return os.path.join(SAVE_DIR, f"{prefix}-{next_num}.txt")

# Banner dengan animasi dan efek modern
def display_banner():
    banner_text = r"""
██████╗ ██████╗  ██████╗ ██╗  ██╗
██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝
██████╔╝██████╔╝██║   ██║ ╚███╔╝ 
██╔══██╗██╔══██╗██║   ██║ ██╔██╗ 
██║  ██║██████╔╝╚██████╔╝██╔╝ ██╗
╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝
    """
    banner = Text.from_ansi(banner_text)
    banner.stylize("bold cyan", 0, 100)
    
    # Animasi warna
    colors = ["cyan", "magenta", "blue", "green", "yellow"]
    for i in range(0, len(banner_text)):
        color = random.choice(colors)
        banner.stylize(color, i, i+1)
    
    panel = Panel(
        Align.center(banner, vertical="middle"),
        title="[bold cyan]R-Dox Advanced[/bold cyan]",
        subtitle="[bold magenta]Untuk pengujian yang diotorisasi saja[/bold magenta]",
        style="blue",
        expand=False,
        padding=(1, 2),
        border_style="bright_blue"
    )
    
    # Animasi banner masuk
    console.clear()
    for i in range(1, 11):
        console.print(panel, height=min(i, 10))
        time.sleep(0.05)

# Animasi loading dengan efek modern
def loading_animation(message="Memuat", duration=2):
    with Progress(
        SpinnerColumn("dots", style="bright_cyan", speed=1.0),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        TimeElapsedColumn(),
        transient=True
    ) as progress:
        task = progress.add_task(f"[cyan]{message}...", total=100)
        start = time.time()
        while time.time() - start < duration:
            progress.update(task, advance=100 * (time.time() - start) / duration)
            time.sleep(0.05)

# Animasi teks mengetik
def type_effect(text, style="bold white", delay=0.03):
    for char in text:
        console.print(char, style=style, end="")
        sys.stdout.flush()
        time.sleep(delay)
    console.print()

def get_system_info():
    try:
        ip = requests.get("https://api.ipify.org", timeout=5).text
    except:
        ip = "Tidak Diketahui"
    return {
        "username": getpass.getuser(), 
        "sistem": platform.system(),
        "rilis": platform.release(), 
        "public_ip": ip,
        "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# Menu modern dengan layout dan animasi
def print_menu():
    layout = Layout()
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3)
    )
    
    # Header
    header_text = Text("R-Dox Advanced", justify="center", style="bold cyan on black")
    layout["header"].update(
        Panel(header_text, style="bright_blue", border_style="bright_cyan")
    )
    
    # Menu utama
    menu_table = Table.grid(expand=True, padding=(0, 2))
    menu_table.add_column(justify="center", ratio=1)
    menu_table.add_column(justify="center", ratio=1)
    menu_table.add_column(justify="center", ratio=1)
    
    menu_table.add_row(
        Panel("[green]1[/green] Mulai Pencarian Google Dork", border_style="green"),
        Panel("[green]2[/green] Lihat Hasil Terakhir", border_style="green"),
        Panel("[green]3[/green] Generate Random Dorks", border_style="green")
    )
    menu_table.add_row(
        Panel("[green]4[/green] Ekspor Hasil ke CSV", border_style="green"),
        Panel("[green]5[/green] Pengumpulan Informasi Website", border_style="green"),
        Panel("[green]6[/green] Lihat Riwayat Penelitian", border_style="green")
    )
    menu_table.add_row(
        Panel("[green]7[/green] Hapus Semua Hasil", border_style="green"),
        Panel("[green]8[/green] Tentang Alat Ini", border_style="green"),
        Panel("[green]9[/green] Doxing", border_style="green")
    )
    menu_table.add_row(
        Panel("[green]10[/green] Analisis Kerentanan", border_style="red"),
        Panel("[green]0[/green] Keluar", border_style="red"),
        Panel(f"[yellow]{sistem_terdeteksi}[/yellow]", border_style="yellow")
    )
    
    layout["main"].update(
        Panel(
            menu_table,
            title=f"[bold yellow]{msg['menu_utama']}[/bold yellow]",
            border_style="bright_magenta",
            padding=(1, 2)
        )
    )
    
    # Footer
    footer_text = Text(f"{msg['pilih_opsi']} ", style="bold yellow", end="")
    layout["footer"].update(
        Panel(footer_text, border_style="bright_blue")
    )
    
    console.print(layout)

# Fungsi search_with_retry() tanpa parameter pause
def search_with_retry(query, num_results, max_retries=10, base_delay=5):
    attempt = 0
    while attempt < max_retries:
        try:
            return list(search(query, num_results=num_results))
        except (requests.exceptions.HTTPError, RemoteDisconnected) as err:
            delay_retry = base_delay * (2 ** attempt)
            console.print(f"[yellow]Error: {err}. Mencoba ulang dalam {delay_retry} detik (Attempt {attempt+1}/{max_retries})[/yellow]")
            time.sleep(delay_retry)
            attempt += 1
    return []

# Fungsi doxing (menu 9)
def doxing_info():
    target = console.input(f"\n[bold red]{msg['masukkan_target']}[/bold red] ").strip()
    if not target:
        console.print("[red]Target tidak boleh kosong![/red]")
        return

    # Animasi pencarian
    with console.status("[bold cyan]Mencari informasi target...[/bold cyan]", spinner="dots") as status:
        # Jika target merupakan nomor telepon (memungkinkan spasi, '-', dan optional '+')
        if re.fullmatch(r"^\+?\d[\d\s\-]+$", target):
            # Jika sudah ada kode negara (diawali "+"), gunakan langsung
            if target.startswith("+"):
                query_variants = [
                    f'"{target}"',
                    f'"{target[1:]}"',  # versi tanpa tanda '+'
                    f'"{target}" phone',
                    f'site:tellows.net "{target}"',
                    f'site:whoscall.com "{target}"'
                ]
            else:
                kode_negara = console.input("[bold red]Masukkan kode negara (misalnya: +62):[/bold red] ").strip()
                if kode_negara and not kode_negara.startswith("+"):
                    kode_negara = f"+{kode_negara}"
                query_variants = [
                    f'"{kode_negara}{target}"',
                    f'"{target}"',
                    f'"{kode_negara}{target}" phone',
                    f'site:tellows.net "{kode_negara}{target}"',
                    f'site:whoscall.com "{kode_negara}{target}"'
                ]
        else:
            query_variants = [
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

        # Ambil jumlah hasil doxing satu kali
        jumlah = int(console.input(f"[bold red]{msg['masukkan_jumlah']}[/bold red] "))
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
        
        try:
            for q in query_variants:
                status.update(f"[cyan]Mencari: {q}[/cyan]")
                results = search_with_retry(q, num_results=jumlah)
                for url in results:
                    hasil_set.add(url)
                    if len(hasil_set) >= jumlah:
                        break
                if len(hasil_set) >= jumlah:
                    break
                time.sleep(random.uniform(1, 3))
            
            if hasil_set:
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("No", style="dim", width=4)
                table.add_column("URL")
                
                for idx, url in enumerate(hasil_set, 1):
                    table.add_row(str(idx), f"[link={url}]{url}[/link]")
                
                console.print(table)
                
                # Tawarkan untuk menyimpan hasil
                save = console.input("\n[bold yellow]Simpan hasil doxing? (y/n): [/bold yellow]").lower()
                if save == 'y':
                    filename = generate_filename("doxing")
                    with open(filename, 'w') as f:
                        f.write("\n".join(hasil_set))
                    console.print(f"[green]Hasil doxing disimpan ke: {filename}[/green]")
            else:
                console.print("[yellow]Tidak ada informasi publik ditemukan.[/yellow]")
        except Exception as e:
            console.print(f"[red]Error saat doxing: {e}[/red]")
        finally:
            requests.get = original_get

# Fungsi pencarian Google Dork (menu 1)
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
        
        with Progress(
            SpinnerColumn("dots", style="bright_cyan"),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=None),
            TimeElapsedColumn(),
            transient=True
        ) as progress:
            task = progress.add_task("[cyan]Mencari hasil...", total=pages)
            
            results = []
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
                    progress.console.print(f"[white]{len(results)}. [green]{url}[/green]")
                    time.sleep(delay)
                    progress.update(task, advance=1)
                    
                    if len(results) >= MAX_RESULTS:
                        progress.console.print("[yellow]Jumlah hasil maksimum tercapai. Berhenti...[/yellow]")
                        break
                
                requests.get = original_get
            except Exception as e:
                progress.console.print(f"[red]Error pencarian: {e}[/red]")
            
            if results:
                with open(filename, 'w') as f:
                    f.write("\n".join(results))
                
                # Tampilkan animasi penyimpanan
                for i in range(1, 11):
                    progress.console.print(f"[cyan]Menyimpan hasil... [{'█'*i}{' '*(10-i)}] {i*10}%[/cyan]")
                    time.sleep(0.1)
                
                console.print(f"\n[green]{msg['hasil_disimpan'].format(n=len(results), file=filename)}[/green]\n")
                
                # Tampilkan preview hasil
                preview_table = Table(show_header=True, header_style="bold magenta", title="Preview Hasil")
                preview_table.add_column("No", style="dim", width=4)
                preview_table.add_column("URL")
                
                for idx, url in enumerate(results[:5], 1):
                    preview_table.add_row(str(idx), f"[link={url}]{url}[/link]")
                
                console.print(preview_table)
                
                if len(results) > 5:
                    console.print(f"[dim]Menampilkan 5 dari {len(results)} hasil. Lihat file untuk selengkapnya.[/dim]")
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
        
        # Tampilan modern dengan tabs
        table = Table(title=f"[bold green]Hasil dari {latest_file}[/bold green]", box="double")
        table.add_column("No", justify="right", style="cyan")
        table.add_column("URL", style="magenta")
        
        for idx, url in enumerate(content[:20], 1):
            table.add_row(str(idx), f"[link={url}]{url}[/link]")
        
        console.print(table)
        console.print(f"\n[dim]Menampilkan 20 dari {len(content)} hasil. Lihat file lengkap untuk daftar selengkapnya.[/dim]\n")
        
        # Tampilkan statistik
        domains = {}
        for url in content:
            domain = urlparse(url).netloc
            domains[domain] = domains.get(domain, 0) + 1
        
        domain_table = Table(title="[bold yellow]Statistik Domain[/bold yellow]", box="round")
        domain_table.add_column("Domain", style="green")
        domain_table.add_column("Jumlah", justify="right", style="cyan")
        
        for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True)[:5]:
            domain_table.add_row(domain, str(count))
        
        console.print(domain_table)
        
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
            "inurl:dashboard", "inurl:adminpanel", "inurl:cpanel", "intitle:'control panel'", "inurl:manage"
        ],
        "Sensitive Info": [
            "intitle:index.of", "intext:password", "intext:username", "intext:credentials", "intext:secret",
            "intext:confidential", "intext:private", "intext:backup", "intext:'database dump'", "intext:'sql dump'"
        ],
        "Vulnerabilities": [
            "inurl:wp-config.php", "inurl:config.php", "inurl:phpinfo.php", "inurl:shell.php", "inurl:adminer.php",
            "inurl:login.php", "inurl:upload.php", "inurl:exec.php", "inurl:cmd.php", "inurl:debug"
        ],
        "Databases": [
            "filetype:sql", "intext:'DB_PASSWORD'", "intext:'DB_USER'", "intext:'DB_HOST'", "intext:'mysql_fetch_array'",
            "intext:'SQL syntax'", "intext:'Warning: mysql_connect()'", "intext:'phpMyAdmin'", "inurl:phpmyadmin", "intext:'database error'"
        ]
    }
    
    # Tampilan modern dengan panel
    console.print(Panel("[bold cyan]Dork Acak untuk Berbagai Kategori[/bold cyan]", style="blue"))
    
    for kategori, dorks in dork_categories.items():
        selected = random.choice(dorks)
        panel = Panel(
            f"[green]{selected}[/green]",
            title=f"[bold yellow]{kategori}[/bold yellow]",
            border_style="bright_green" if kategori == "Files" else "cyan",
            padding=(1, 2)
        )
        console.print(panel)
    
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
            urls = [line.strip() for line in infile if line.strip()]
            if not urls:
                console.print("\n[yellow]Tidak ada URL yang ditemukan dalam file tersebut.[/yellow]\n")
                return
            with open(csv_file, 'w', newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(["ID", "URL", "Domain"])
                for idx, url in enumerate(urls, 1):
                    domain = urlparse(url).netloc
                    writer.writerow([idx, url, domain])
        
        # Animasi penyelesaian
        console.print(f"\n[green]Mengekspor data...[/green]")
        for i in range(1, 11):
            console.print(f"[cyan]Proses ekspor [{'█'*i}{' '*(10-i)}] {i*10}%[/cyan]")
            time.sleep(0.1)
        
        console.print(f"\n[green]{msg['hasil_disimpan'].format(n=len(urls), file=csv_file)}[/green]\n")
    except Exception as e:
        console.print(f"[red]Ekspor gagal: {e}[/red]")

# Fungsi analisis kerentanan baru
def vulnerability_scan():
    url = console.input(f"\n[bold red]{msg['masukkan_url']}[/bold red] ").strip()
    if not url:
        console.print("[red]URL tidak boleh kosong![/red]")
        return
    
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    try:
        # Animasi pemindaian
        with Progress(
            SpinnerColumn("dots", style="bright_red"),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=None),
            TimeElapsedColumn(),
            transient=True
        ) as progress:
            task = progress.add_task("[red]Memindai kerentanan...", total=100)
            
            # Langkah 1: Cek koneksi dasar
            progress.update(task, description="[red]Memeriksa koneksi...", advance=10)
            try:
                response = requests.get(url, timeout=10, allow_redirects=False)
            except Exception as e:
                progress.console.print(f"[red]Gagal terhubung ke {url}: {e}[/red]")
                return
            
            # Langkah 2: Analisis header
            progress.update(task, description="[red]Menganalisis header...", advance=20)
            security_issues = []
            security_headers = ["Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options", 
                               "Strict-Transport-Security", "X-XSS-Protection"]
            
            for header in security_headers:
                if header not in response.headers:
                    security_issues.append(f"Header keamanan [bold red]{header}[/bold red] tidak ditemukan")
            
            # Langkah 3: Cek metode HTTP yang berbahaya
            progress.update(task, description="[red]Memeriksa metode HTTP...", advance=30)
            dangerous_methods = ["PUT", "DELETE", "TRACE", "CONNECT"]
            try:
                options_response = requests.options(url, timeout=5)
                allowed_methods = options_response.headers.get('Allow', '').split(',')
                for method in dangerous_methods:
                    if method in allowed_methods:
                        security_issues.append(f"Metode HTTP [bold red]{method}[/bold red] diizinkan")
            except:
                pass
            
            # Langkah 4: Cek kerentanan XSS dasar
            progress.update(task, description="[red]Memeriksa kerentanan XSS...", advance=40)
            test_payload = "<script>alert('XSS')</script>"
            test_url = f"{url}?test={test_payload}"
            try:
                test_response = requests.get(test_url, timeout=5)
                if test_payload in test_response.text:
                    security_issues.append(f"Kerentanan [bold red]XSS[/bold red] terdeteksi di parameter URL")
            except:
                pass
            
            # Langkah 5: Cek kerentanan SQL Injection dasar
            progress.update(task, description="[red]Memeriksa kerentanan SQLi...", advance=50)
            sql_payload = "' OR '1'='1"
            sql_url = f"{url}?id={sql_payload}"
            try:
                sql_response = requests.get(sql_url, timeout=5)
                if "sql" in sql_response.text.lower() or "syntax" in sql_response.text.lower():
                    security_issues.append(f"Kerentanan [bold red]SQL Injection[/bold red] terdeteksi di parameter URL")
            except:
                pass
            
            # Langkah 6: Cek versi server yang rentan
            progress.update(task, description="[red]Memeriksa versi server...", advance=60)
            server_header = response.headers.get('Server', '')
            vulnerable_servers = {
                "Apache": ["2.2", "2.4.0-2.4.20"],
                "nginx": ["1.4.0-1.4.3", "1.5.0-1.5.7"],
                "IIS": ["7.0", "7.5", "8.0"]
            }
            
            for server, versions in vulnerable_servers.items():
                if server in server_header:
                    for version in versions:
                        if version in server_header:
                            security_issues.append(f"Versi server [bold red]{server} {version}[/bold red] memiliki kerentanan yang diketahui")
            
            progress.update(task, advance=100)
        
        # Tampilkan hasil
        console.print(f"\n[bold red]{msg['hasil_kerentanan']} untuk {url}[/bold red]\n")
        
        if security_issues:
            for issue in security_issues:
                console.print(f"• {issue}")
            
            # Ringkasan tingkat keamanan
            risk_level = "Tinggi" if len(security_issues) > 3 else "Sedang" if len(security_issues) > 1 else "Rendah"
            console.print(f"\n[bold]Tingkat Risiko Keseluruhan: [red]{risk_level}[/red][/bold]")
            
            # Rekomendasi
            console.print("\n[bold yellow]Rekomendasi:[/bold yellow]")
            console.print("- Perbarui server dan aplikasi ke versi terbaru")
            console.print("- Terapkan header keamanan yang tepat")
            console.print("- Lakukan audit keamanan menyeluruh")
            console.print("- Gunakan Web Application Firewall (WAF)")
        else:
            console.print("[green]Tidak ditemukan kerentanan keamanan yang jelas.[/green]")
            console.print("[yellow]Catatan: Pemindaian ini hanya mendeteksi kerentanan dasar.[/yellow]")
        
        # Tawarkan untuk menyimpan hasil
        save = console.input("\n[bold yellow]Simpan hasil analisis? (y/n): [/bold yellow]").lower()
        if save == 'y':
            filename = generate_filename("vuln-scan")
            with open(filename, 'w') as f:
                f.write(f"Hasil Analisis Kerentanan untuk {url}\n")
                f.write("="*50 + "\n\n")
                if security_issues:
                    f.write("Kerentanan yang Ditemukan:\n")
                    for issue in security_issues:
                        f.write(f"- {issue}\n")
                else:
                    f.write("Tidak ditemukan kerentanan keamanan yang jelas.\n")
                f.write("\nCatatan: Pemindaian ini hanya mendeteksi kerentanan dasar.")
            console.print(f"[green]Hasil disimpan ke: {filename}[/green]")
    
    except Exception as e:
        console.print(f"[red]Error saat analisis: {e}[/red]")

def website_info_gathering():
    url = console.input("\n[bold]Masukkan URL yang akan dianalisis (misalnya: contoh.com):[/bold] ").strip()
    if not url:
        console.print("[red]URL tidak boleh kosong![/red]")
        return
    
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    try:
        console.print("\n[bold cyan]Mengumpulkan informasi lanjutan...[/bold cyan]\n")
        
        # Gunakan progress bar untuk proses pengumpulan informasi
        with Progress(
            SpinnerColumn("dots", style="bright_cyan"),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=None),
            TimeElapsedColumn(),
            transient=True
        ) as progress:
            task = progress.add_task("[cyan]Memproses...", total=100)
            
            progress.update(task, description="[cyan]Mengirim permintaan...", advance=10)
            start_time = time.time()
            response = requests.get(url, timeout=10, allow_redirects=True)
            elapsed = time.time() - start_time
            
            progress.update(task, description="[cyan]Memproses HTML...", advance=20)
            final_url = response.url
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.string.strip() if soup.title else "Judul tidak ditemukan"
            
            progress.update(task, description="[cyan]Menganalisis meta data...", advance=30)
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
            
            progress.update(task, description="[cyan]Mencari informasi DNS...", advance=40)
            domain = urlparse(url).netloc
            ip_address = socket.gethostbyname(domain)
            
            progress.update(task, description="[cyan]Melakukan WHOIS lookup...", advance=50)
            domain_info = whois.whois(domain)
            
            progress.update(task, description="[cyan]Menganalisis header...", advance=60)
            security_headers = ["Content-Security-Policy", "X-Frame-Options", "X-XSS-Protection", 
                              "Strict-Transport-Security", "X-Content-Type-Options"]
            header_results = {}
            
            for header in security_headers:
                header_results[header] = response.headers.get(header, "Tidak Ditemukan")
            
            progress.update(task, description="[cyan]Memeriksa SSL...", advance=70)
            ssl_info = {}
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
                        ssl_info = {
                            "Issuer": cert_details.get('issuer', {}),
                            "Subject": cert_details.get('subject', {}),
                            "Expires": cert_details.get('notAfter', ''),
                            "Serial Number": cert_details.get('serialNumber', '')
                        }
                except Exception as e:
                    ssl_info = {"Error": str(e)}
            
            progress.update(task, description="[cyan]Memindai port...", advance=80)
            common_ports = {80: "HTTP", 443: "HTTPS", 22: "SSH", 21: "FTP", 25: "SMTP", 53: "DNS"}
            port_status = {}
            
            for port, service in common_ports.items():
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((domain, port))
                port_status[port] = "Terbuka" if result == 0 else "Tertutup"
                sock.close()
            
            progress.update(task, advance=100)
        
        # Tampilkan hasil dalam panel modern
        console.print(Panel(f"[bold green]Informasi Dasar[/bold green]", style="blue"))
        info_table = Table.grid(padding=(0, 2))
        info_table.add_column(style="bold cyan")
        info_table.add_column()
        
        info_table.add_row("URL Asli", url)
        info_table.add_row("URL Akhir", final_url)
        info_table.add_row("Status HTTP", f"{response.status_code}")
        info_table.add_row("Waktu Respons", f"{elapsed:.2f} detik")
        info_table.add_row("Judul Halaman", title)
        info_table.add_row("Meta Deskripsi", meta_desc or "Tidak Tersedia")
        info_table.add_row("Meta Keywords", meta_keywords or "Tidak Tersedia")
        info_table.add_row("CMS/Generator", generator or "Tidak Terdeteksi")
        info_table.add_row("Tag H1", ", ".join(h1_tags) if h1_tags else "Tidak ditemukan")
        info_table.add_row("Domain", domain)
        info_table.add_row("Alamat IP", ip_address)
        
        console.print(info_table)
        
        # WHOIS Information
        console.print(Panel(f"[bold green]Informasi WHOIS[/bold green]", style="blue"))
        whois_table = Table.grid(padding=(0, 2))
        whois_table.add_column(style="bold cyan", width=20)
        whois_table.add_column(width=50)
        
        whois_table.add_row("Pendaftar", domain_info.get('registrar', 'Tidak Diketahui'))
        whois_table.add_row("Tanggal Pembuatan", str(domain_info.get('creation_date', 'Tidak Diketahui')))
        whois_table.add_row("Tanggal Kedaluwarsa", str(domain_info.get('expiration_date', 'Tidak Diketahui')))
        whois_table.add_row("Pemilik", domain_info.get('name', 'Tidak Diketahui'))
        whois_table.add_row("Organisasi", domain_info.get('org', 'Tidak Diketahui'))
        whois_table.add_row("Alamat", domain_info.get('address', 'Tidak Diketahui'))
        whois_table.add_row("Kota", domain_info.get('city', 'Tidak Diketahui'))
        whois_table.add_row("Negara", domain_info.get('country', 'Tidak Diketahui'))
        
        console.print(whois_table)
        
        # Header Security
        console.print(Panel(f"[bold green]Header Keamanan[/bold green]", style="blue"))
        header_table = Table("Header", "Nilai", style="bright_cyan")
        for header, value in header_results.items():
            header_table.add_row(header, value)
        console.print(header_table)
        
        # SSL Info
        if ssl_info:
            console.print(Panel(f"[bold green]Informasi Sertifikat SSL[/bold green]", style="blue"))
            ssl_table = Table.grid(padding=(0, 2))
            ssl_table.add_column(style="bold cyan", width=20)
            ssl_table.add_column(width=50)
            
            for key, value in ssl_info.items():
                if isinstance(value, dict):
                    value = ", ".join([f"{k}={v}" for k, v in value.items()])
                ssl_table.add_row(key, str(value))
            
            console.print(ssl_table)
        
        # Port Status
        console.print(Panel(f"[bold green]Status Port[/bold green]", style="blue"))
        port_table = Table("Port", "Layanan", "Status", style="bright_cyan")
        for port, service in common_ports.items():
            status = port_status[port]
            style = "green" if status == "Tertutup" else "red"
            port_table.add_row(str(port), service, f"[{style}]{status}[/{style}]")
        console.print(port_table)
        
        # Technology Detection
        tech_url = f"https://builtwith.com/{domain}"
        console.print(Panel(f"[bold green]Deteksi Teknologi[/bold green]", style="blue"))
        console.print(f"Kunjungi [blue]{tech_url}[/blue] untuk profil teknologi secara detail")
        
        # Tawarkan untuk membuka di browser
        open_browser = console.input("\n[bold yellow]Buka hasil BuiltWith di browser? (y/n): [/bold yellow]").lower()
        if open_browser == 'y':
            webbrowser.open(tech_url)
    
    except Exception as e:
        console.print(f"\n[red]Error saat analisis lanjutan: {e}[/red]\n")

def view_history():
    files = [f for f in os.listdir(SAVE_DIR) if f.startswith("hasil-")]
    if not files:
        console.print("\n[yellow]Tidak ada file penelitian yang ditemukan.[/yellow]\n")
        return
    
    files.sort(key=lambda x: int(x[len("hasil-"):-len(".txt")]) if x[len("hasil-"):-len(".txt")].isdigit() else 0, reverse=True)
    
    # Tampilan modern dengan panel
    console.print(Panel(f"[bold cyan]{msg['lihat_riwayat']}[/bold cyan]", style="blue"))
    
    table = Table(title="[bold green]Riwayat Penelitian[/bold green]", box="round")
    table.add_column("Tanggal", justify="left", style="cyan")
    table.add_column("Nama File", style="magenta")
    table.add_column("Ukuran", justify="right", style="green")
    table.add_column("Tipe", justify="center", style="yellow")
    
    for file in files[:10]:
        file_path = os.path.join(SAVE_DIR, file)
        file_date = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M")
        file_size = os.path.getsize(file_path)
        size_str = f"{file_size/1024:.1f} KB" if file_size < 1024*1024 else f"{file_size/(1024*1024):.1f} MB"
        
        file_type = "Dork"
        if "doxing" in file:
            file_type = "Doxing"
        elif "vuln" in file:
            file_type = "Vuln"
        
        table.add_row(file_date, file, size_str, file_type)
    
    console.print(table)
    console.print(f"\n[dim]Menampilkan {min(10, len(files))} dari {len(files)} file[/dim]\n")

def clear_results():
    confirm = console.input(f"\n[bold red]Yakin ingin menghapus SEMUA file penelitian? (y/n):[/bold red] ").lower()
    if confirm == 'y':
        try:
            # Animasi penghapusan
            with console.status("[bold red]Menghapus file...[/bold red]", spinner="dots") as status:
                time.sleep(1)
                for file in os.listdir(SAVE_DIR):
                    file_path = os.path.join(SAVE_DIR, file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        console.print(f"[red]Gagal menghapus {file_path}: {e}[/red]")
            
            console.print("\n[green]Semua file penelitian telah dihapus.[/green]\n")
        except Exception as e:
            console.print(f"\n[red]Error menghapus file: {e}[/red]\n")
    else:
        console.print("\n[cyan]Operasi dibatalkan.[/cyan]\n")

def about_tool():
    info = """
[bold cyan]R-Dox Advanced[/bold cyan] - Alat Penelitian Keamanan Modern

[bold]Versi:[/bold] 3.0
[bold]Pengembang:[/bold] Ethical Security Researcher

[bold]Fitur Utama:[/bold]
✓ Pencarian Google Dork dengan filter domain
✓ Doxing otomatis untuk nama, email, dan nomor telepon
✓ Pengumpulan informasi website lanjutan (DNS, WHOIS, SSL)
✓ Analisis kerentanan keamanan dasar
✓ Generator dork acak untuk berbagai kategori
✓ Ekspor hasil ke CSV
✓ Riwayat penelitian otomatis
✓ Tampilan modern dengan animasi dan warna

[bold]Peningkatan Versi Ini:[/bold]
• Animasi UI yang lebih modern dan responsif
• Analisis kerentanan terintegrasi
• Tampilan hasil dalam tabel interaktif
• Efek visual dan pewarnaan yang lebih kaya
• Sistem menu berbasis panel
• Fitur doxing yang ditingkatkan
• Statistik hasil otomatis
• Deteksi teknologi website

[bold]Penting:[/bold]
Alat ini hanya untuk [red]pengujian keamanan yang diotorisasi[/red].
Penggunaan tanpa izin dapat melanggar hukum.

[bold]Disclaimer:[/bold]
Pengembang tidak bertanggung jawab atas penyalahgunaan alat ini.
Selalu dapatkan izin sebelum menguji sistem apa pun.
    """
    console.print(Panel.fit(info, title=f"[bold cyan]{msg['tentang_alat']}[/bold cyan]", style="blue", padding=(1, 2)))

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    display_banner()
    
    # Tampilkan info sistem dengan animasi
    sys_info = get_system_info()
    sys_text = Text()
    sys_text.append("Sistem: ", style="bold cyan")
    sys_text.append(f"{sys_info['sistem']} {sys_info['rilis']}\n", style="bold yellow")
    sys_text.append("Pengguna: ", style="bold cyan")
    sys_text.append(f"{sys_info['username']}\n", style="bold yellow")
    sys_text.append("IP Publik: ", style="bold cyan")
    sys_text.append(f"{sys_info['public_ip']}\n", style="bold yellow")
    sys_text.append("Waktu: ", style="bold cyan")
    sys_text.append(sys_info['waktu'], style="bold yellow")
    
    console.print(Panel(sys_text, title="[bold magenta]Info Sistem[/bold magenta]", style="blue", padding=(1, 2)))
    
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
        elif choice == "10":
            vulnerability_scan()
        elif choice == "0":
            # Animasi keluar
            with console.status("[bold red]Keluar...[/bold red]", spinner="dots") as status:
                time.sleep(1)
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
