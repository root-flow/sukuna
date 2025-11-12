#!/usr/bin/env python3
"""
SUKUNA v11.0
Author: canmitm
Instagram: @canmitm
Python + C (x3) + Assembly (x3) + Full Pentest
"""

import os
import sys
import json
import time
import threading
import subprocess
import urllib.parse
import requests
from datetime import datetime

# === SUKUNA ===
SUKUNA_WORD = "I am the honored one."
AUTHOR = "canmitm"
INSTAGRAM = "@canmitm"

# === C MODÜLLERİ (3 ADET) ===
C_CODES = [
    """#include <stdio.h>\nint main() { printf("SUKUNA[C1]: %s\\n"); return 0; }""",
    """#include <stdio.h>\nint main() { printf("SUKUNA[C2]: Power overwhelming.\\n"); return 0; }""",
    """#include <stdio.h>\n#include <unistd.h>\nint main() { printf("SUKUNA[C3]: Domain Expansion.\\n"); sleep(1); return 0; }"""
]

# === ASSEMBLY MODÜLLERİ (3 ADET) ===
ASM_CODES = [
    """section .data\n    msg db "SUKUNA[ASM1]: %s", 10\n    len equ $ - msg\nsection .text\n    global _start\n_start:\n    mov rax, 1\n    mov rdi, 1\n    mov rsi, msg\n    mov rdx, len\n    syscall\n    mov rax, 60\n    xor rdi, rdi\n    syscall""",
    """section .data\n    msg db "SUKUNA[ASM2]: Malevolent Shrine.", 10\n    len equ $ - msg\nsection .text\n    global _start\n_start:\n    mov rax, 1\n    mov rdi, 1\n    mov rsi, msg\n    mov rdx, len\n    syscall\n    mov rax, 60\n    xor rdi, rdi\n    syscall""",
    """section .data\n    msg db "SUKUNA[ASM3]: Unlimited Void.", 10\n    len equ $ - msg\nsection .text\n    global _start\n_start:\n    mov rax, 1\n    mov rdi, 1\n    mov rsi, msg\n    mov rdx, len\n    syscall\n    mov rax, 60\n    xor rdi, rdi\n    syscall"""
]

# === PATHS ===
REPORT_DIR = "/var/lib/sukuna/reports"
EVIDENCE_DIR = "/var/lib/sukuna/evidence"
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(EVIDENCE_DIR, exist_ok=True)

# === MODES ===
MODES = {
    "1": {"name": "LIGHT",      "nmap": "-T3 -F",                 "sql_level": "1", "threads": 1, "time": "30s"},
    "2": {"name": "MEDIUM",     "nmap": "-T4 -F -sV",             "sql_level": "3", "threads": 3, "time": "2m"},
    "3": {"name": "DEEP",       "nmap": "-T4 -sV -p- -A",         "sql_level": "5", "threads": 5, "time": "10m"},
    "4": {"name": "LIGHTNING",  "nmap": "-T5 -F --min-rate 5000", "sql_level": "1", "threads": 10, "time": "30s"}
}

# === LOG ===
def log(msg, color=""):
    colors = {
        "green": "\033[92m", "red": "\033[91m", "yellow": "\033[93m",
        "cyan": "\033[96m", "orange": "\033[38;5;208m", "purple": "\033[95m",
        "bold": "\033[1m", "reset": "\033[0m"
    }
    c = colors.get(color, "")
    r = colors["reset"]
    print(f"{c}{msg}{r}")

# === C & ASM ÇALIŞTIR ===
def run_c_module(idx):
    src = f"/tmp/sukuna_c_{os.getpid()}_{idx}.c"
    bin_path = f"/tmp/sukuna_c_{os.getpid()}_{idx}"
    with open(src, "w") as f:
        f.write(C_CODES[idx] % SUKUNA_WORD if "%s" in C_CODES[idx] else C_CODES[idx])
    try:
        subprocess.run(["gcc", "-w", src, "-o", bin_path], timeout=5, check=True)
        out = subprocess.run([bin_path], capture_output=True, text=True, timeout=5).stdout.strip()
        for f in [src, bin_path]: 
            if os.path.exists(f): os.unlink(f)
        return out
    except: return f"C{idx+1} failed"

def run_asm_module(idx):
    src = f"/tmp/sukuna_asm_{os.getpid()}_{idx}.asm"
    obj = f"/tmp/sukuna_o_{os.getpid()}_{idx}.o"
    bin_path = f"/tmp/sukuna_asm_{os.getpid()}_{idx}"
    with open(src, "w") as f:
        f.write(ASM_CODES[idx])
    try:
        subprocess.run(["nasm", "-f", "elf64", src, "-o", obj], timeout=5, check=True)
        subprocess.run(["ld", obj, "-o", bin_path], timeout=5, check=True)
        out = subprocess.run([bin_path], capture_output=True, text=True, timeout=5).stdout.strip()
        for f in [src, obj, bin_path]: 
            if os.path.exists(f): os.unlink(f)
        return out
    except: return f"ASM{idx+1} failed"

# === 3 DİL TEST ===
def run_3lang():
    log("┌─ 3 DİL MODÜLLERİ ÇALIŞTIRILIYOR", "purple")
    for i in range(3):
        log(f"│ {run_c_module(i)}", "green")
        log(f"│ {run_asm_module(i)}", "yellow")
    log("└─ TAMAM", "purple")

# === TARAMALAR ===
def scan_nmap(target, mode):
    outfile = f"{REPORT_DIR}/nmap_{int(time.time())}.xml"
    cmd = ["nmap"] + MODES[mode]["nmap"].split() + ["-oX", outfile, target]
    log(f"[NMAP] {MODES[mode]['name']} → {target}", "cyan")
    try:
        subprocess.run(cmd, timeout=300, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        log(f"    Rapor: {os.path.basename(outfile)}", "green")
    except: log("    Timeout", "yellow")

def scan_sqlmap(url, mode):
    outdir = f"{REPORT_DIR}/sqlmap_{int(time.time())}"
    cmd = ["sqlmap", "-u", url, "--level", MODES[mode]["sql_level"], "--risk", "3", "--batch", "--random-agent", "--threads=5", "--output-dir", outdir]
    log(f"[SQLMAP] → {url}", "cyan")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if "vulnerable" in result.stdout.lower():
            log("    SQLi BULUNDU!", "red")
        else:
            log("    Temiz", "green")
    except: log("    Hata", "yellow")

def scan_xsser(url):
    cmd = ["xsser", "--url", url, "--auto", "--threads=5", "--batch"]
    log(f"[XSSER] → {url}", "cyan")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if "XSS" in result.stdout:
            log("    XSS BULUNDU!", "red")
        else:
            log("    Temiz", "green")
    except: log("    Hata", "yellow")

def scan_commix(url):
    log_file = f"{EVIDENCE_DIR}/rce_{int(time.time())}.log"
    cmd = ["commix", "--url", url, "--level=3", "--batch", "--output-file", log_file]
    log(f"[COMMIX] RCE → {url}", "cyan")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        output = result.stdout + result.stderr
        with open(log_file, "w") as f: f.write(output)
        if "payload" in output.lower():
            payload = [l for l in output.splitlines() if "payload" in l.lower()][0]
            log(f"    RCE → {payload}", "red")
            log(f"    Kanıt: {log_file}", "orange")
        else:
            log("    Temiz", "green")
    except: log("    Hata", "yellow")

def scan_nikto(url):
    outfile = f"{REPORT_DIR}/nikto_{int(time.time())}.txt"
    cmd = ["nikto", "-h", url, "-output", outfile]
    log(f"[NIKTO] → {url}", "cyan")
    try:
        subprocess.run(cmd, timeout=300)
        log(f"    Rapor: {os.path.basename(outfile)}", "green")
    except: log("    Hata", "yellow")

def scan_nuclei(url):
    outfile = f"{REPORT_DIR}/nuclei_{int(time.time())}.txt"
    cmd = ["nuclei", "-u", url, "-o", outfile, "-silent"]
    log(f"[NUCLEI] → {url}", "cyan")
    try:
        subprocess.run(cmd, timeout=300)
        log(f"    Rapor: {os.path.basename(outfile)}", "green")
    except: log("    Hata", "yellow")

# === ANA TARAMA ===
def full_scan(target, mode):
    log(f"\n┌─ SUKUNA TARAMA BAŞLADI", "bold")
    log(f"│ Target: {target}", "cyan")
    log(f"│ Mode: {MODES[mode]['name']} ({MODES[mode]['time']})", "cyan")
    log(f"│ Author: {AUTHOR} | Instagram: {INSTAGRAM}", "purple")
    log(f"└─ {'─' * 50}", "purple")

    run_3lang()

    if target.startswith(("http://", "https://")):
        scan_sqlmap(target, mode)
        scan_xsser(target)
        scan_commix(target)
        scan_nikto(target)
        scan_nuclei(target)
    else:
        scan_nmap(target, mode)

    log(f"\n[SUKUNA] {SUKUNA_WORD}", "orange")
    log(f"Raporlar: {REPORT_DIR}", "green")
    log(f"Kanıtlar: {EVIDENCE_DIR}", "orange")

# === GUI ===
def gui_mode():
    import tkinter as tk
    from tkinter import scrolledtext, messagebox

    root = tk.Tk()
    root.title("SUKUNA")
    root.geometry("1100x750")
    root.configure(bg="#000")

    tk.Label(root, text="SUKUNA", font=("Arial", 20, "bold"), fg="#0ff", bg="#000").pack(pady=10)
    tk.Label(root, text=SUKUNA_WORD, font=("Arial", 12), fg="#0f0", bg="#000").pack()
    tk.Label(root, text=f"Author: {AUTHOR} | Instagram: {INSTAGRAM}", fg="#888", bg="#000").pack()

    tk.Label(root, text="Target:", fg="#0f0", bg="#000").pack(anchor="w", padx=25)
    target_entry = tk.Entry(root, width=100, font=("Courier", 10))
    target_entry.pack(pady=5, padx=25)

    mode_var = tk.StringVar(value="4")
    for k, v in MODES.items():
        tk.Radiobutton(root, text=f"{k}) {v['name']} — {v['time']}", variable=mode_var, value=k, fg="#0f0", bg="#000", selectcolor="#111").pack(anchor="w", padx=45)

    log_area = scrolledtext.ScrolledText(root, height=28, bg="#111", fg="#0f0", font=("Courier", 9))
    log_area.pack(pady=10, padx=25, fill="both", expand=True)

    def start():
        t = target_entry.get().strip()
        m = mode_var.get()
        if not t:
            messagebox.showerror("Hata", "Target gerekli!")
            return
        log_area.delete(1.0, tk.END)
        threading.Thread(target=full_scan, args=(t, m), daemon=True).start()

    tk.Button(root, text="TARAMAYI BAŞLAT", command=start, bg="#f00", fg="white", font=("Arial", 16, "bold"), height=2).pack(pady=15)

    root.mainloop()

# === GİRİŞ ===
log(f"""
███████╗██╗   ██╗██╗  ██╗██╗   ██╗███╗   ██╗ █████╗ 
██╔════╝██║   ██║██║ ██╔╝██║   ██║████╗  ██║██╔══██╗
███████╗██║   ██║█████╔╝ ██║   ██║██╔██╗ ██║███████║
╚════██║██║   ██║██╔═██╗ ██║   ██║██║╚██╗██║██╔══██║
███████║╚██████╔╝██║  ██╗╚██████╔╝██║ ╚████║██║  ██║
╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝
""", "red")
log(f"{SUKUNA_WORD}", "orange")
log(f"Author: {AUTHOR} | Instagram: {INSTAGRAM}\n", "purple")

# === SEÇİM ===
choice = input("Terminal (1) | GUI (2): ").strip()
if choice == "2":
    gui_mode()
else:
    target = input("Target: ").strip()
    mode = input("Mode [1-4]: ").strip() or "4"
    if target:
        full_scan(target, mode)
    else:
        log("Target gerekli!", "red")

# === ÇIKIŞ ===
log(f"\n[SUKUNA] {SUKUNA_WORD}", "orange")
