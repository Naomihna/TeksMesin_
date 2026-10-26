#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
TeksMesin - Bahasa Kita ke Bahasa Mesin
Tugas individu: mengubah bahasa kita menjadi bahasa mesin.

Cara kerja aplikasi ini sederhana. Setiap huruf yang kita ketik
punya kode angka, yang biasa disebut kode ASCII. Misalnya huruf
"A" itu 65, huruf "a" itu 97, dan spasi itu 32. Nah, angka itu
lalu diubah ke bentuk biner, yaitu deretan 0 dan 1 sepanjang
8 digit per byte. Jadi kata yang kita tulis berubah menjadi
deretan 0 dan 1, itulah yang dibaca mesin.

Aplikasi ini bisa dua arah:
  - Teks ke biner : tulis kalimat biasa, hasilnya kode biner.
  - Biner ke teks : tempel kode biner, hasilnya kalimat biasa.

Kode biner boleh ditulis pakai spasi antar byte atau disambung
terus, dua-duanya bisa dibaca. Kalau ada angka selain 0 dan 1,
atau panjangnya bukan kelipatan 8, aplikasi akan memberi tahu
lewat pesan di bawah tombol, bukan diam saja.

Huruf yang dipakai di sini mengikuti pengkodean UTF-8. Untuk
huruf biasa seperti a sampai z, angka, dan tanda baca, satu
huruf sama dengan satu byte, jadi sama persis dengan tabel
ASCII yang bisa dicari di Google. Huruf di luar itu, misalnya
huruf beraksen, akan memakai lebih dari satu byte, dan tabel
rincian di bawah akan menunjukkannya per byte.

Menjalankan dari source :  python TeksMesin.py
File hasil compile      :  TeksMesin.exe (klik dua kali, tanpa
                           perlu Python dan tanpa perlu compile lagi)
"""

import tkinter as tk
from tkinter import ttk


def text_to_binary(text):
    """Teks -> biner, 8 digit per byte, dipisah spasi."""
    data = text.encode("utf-8")
    return " ".join("{:08b}".format(byte) for byte in data)


def binary_to_text(code):
    """Biner -> teks. Boleh pakai spasi atau disambung terus.

    Melempar ValueError dengan pesan yang bisa ditampilkan ke
    pengguna bila kodenya tidak valid.
    """
    cleaned = "".join(code.split())
    if not cleaned:
        raise ValueError("Kode binernya masih kosong.")
    if any(ch not in "01" for ch in cleaned):
        raise ValueError("Kode biner hanya boleh berisi angka 0 dan 1.")
    if len(cleaned) % 8 != 0:
        raise ValueError(
            "Panjang kode biner harus kelipatan 8, karena satu huruf "
            "diwakili 8 digit. Sekarang panjangnya {} digit.".format(
                len(cleaned)))
    data = bytes(int(cleaned[i:i + 8], 2)
                 for i in range(0, len(cleaned), 8))
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError(
            "Byte-byte ini tidak membentuk huruf yang valid (bukan "
            "pengkodean UTF-8 yang benar).")


def byte_rows(data):
    """Satu baris per byte: (nomor, biner, desimal, karakter)."""
    rows = []
    for i, byte in enumerate(data, start=1):
        if byte == 32:
            char = "spasi"
        elif byte == 10:
            char = "enter"
        elif 33 <= byte <= 126:
            char = chr(byte)
        else:
            char = "-"
        rows.append((i, "{:08b}".format(byte), byte, char))
    return rows


class TeksMesinApp:
    BG = "#F1F5F9"
    PANEL = "#FFFFFF"
    INK = "#1E293B"
    MUTED = "#64748B"
    LINE = "#D9E2EC"
    ACCENT = "#0E7490"
    ACCENT_HOVER = "#0A5A70"
    ACCENT_PALE = "#E0F2F7"
    RED = "#B42318"

    MODE_TEXT = "teks"
    MODE_BINARY = "biner"

    def __init__(self, root):
        self.root = root
        self.root.title("TeksMesin | Bahasa Kita ke Bahasa Mesin")
        self.root.geometry("920x700")
        self.root.minsize(760, 600)
        self.root.configure(bg=self.BG)
        self.mode = self.MODE_TEXT
        self.setup_style()
        self.build_screen()

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background=self.BG)
        style.configure("TLabel", background=self.BG, foreground=self.INK,
                        font=("Segoe UI", 10))
        style.configure("Title.TLabel", background=self.BG, foreground=self.INK,
                        font=("Segoe UI Semibold", 22))
        style.configure("Subtitle.TLabel", background=self.BG,
                        foreground=self.MUTED, font=("Segoe UI", 10))
        style.configure("Small.TLabel", background=self.BG, foreground=self.MUTED,
                        font=("Segoe UI", 9))
        style.configure("TButton", font=("Segoe UI Semibold", 10),
                        padding=(14, 9), background=self.ACCENT,
                        foreground="#FFFFFF", borderwidth=0)
        style.map("TButton", background=[("active", self.ACCENT_HOVER)])
        style.configure("Plain.TButton", background=self.PANEL,
                        foreground=self.INK, borderwidth=1, relief="solid")
        style.map("Plain.TButton", background=[("active", "#EAF0F6")])
        style.configure("Treeview", background=self.PANEL,
                        fieldbackground=self.PANEL, foreground=self.INK,
                        rowheight=28, borderwidth=0, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#E8EEF4",
                        foreground="#334155", font=("Segoe UI Semibold", 9),
                        padding=(8, 8), relief="flat")

    def build_screen(self):
        outer = tk.Frame(self.root, bg=self.BG)
        outer.pack(fill="both", expand=True, padx=28, pady=22)

        # Kepala aplikasi.
        head = tk.Frame(outer, bg=self.BG)
        head.pack(fill="x", pady=(0, 4))
        titles = tk.Frame(head, bg=self.BG)
        titles.pack(side="left")
        tk.Label(titles, text="TeksMesin", bg=self.BG, fg=self.INK,
                 font=("Segoe UI Semibold", 22)).pack(anchor="w")
        tk.Label(titles, text="Bahasa kita diubah menjadi bahasa mesin "
                 "(kode biner).", bg=self.BG, fg=self.MUTED,
                 font=("Segoe UI", 10)).pack(anchor="w", pady=(2, 0))
        tk.Label(head, text="PYTHON  •  TKINTER", bg=self.BG, fg=self.MUTED,
                 font=("Segoe UI", 8, "bold")).pack(side="right", anchor="n")

        # Pilihan arah konversi.
        mode_row = tk.Frame(outer, bg=self.BG)
        mode_row.pack(fill="x", pady=(14, 10))
        tk.Label(mode_row, text="Mau diubah ke arah mana?",
                 bg=self.BG, fg=self.INK,
                 font=("Segoe UI Semibold", 10)).pack(side="left")
        self.btn_mode_text = tk.Button(
            mode_row, text="Teks ke biner", bg=self.ACCENT, fg="#FFFFFF",
            relief="flat", font=("Segoe UI Semibold", 10), padx=14, pady=6,
            command=lambda: self.set_mode(self.MODE_TEXT))
        self.btn_mode_text.pack(side="left", padx=(14, 6))
        self.btn_mode_binary = tk.Button(
            mode_row, text="Biner ke teks", bg=self.PANEL, fg=self.INK,
            relief="solid", font=("Segoe UI Semibold", 10), padx=14, pady=6,
            command=lambda: self.set_mode(self.MODE_BINARY))
        self.btn_mode_binary.pack(side="left")

        # Kotak masukan.
        self.input_label = tk.Label(outer, text="Tulis bahasa kita di sini:",
                                    bg=self.BG, fg=self.INK,
                                    font=("Segoe UI Semibold", 10))
        self.input_label.pack(anchor="w", pady=(4, 6))
        input_card = tk.Frame(outer, bg=self.PANEL,
                              highlightbackground=self.LINE,
                              highlightthickness=1)
        input_card.pack(fill="x")
        self.input_text = tk.Text(input_card, height=5, wrap="word",
                                  font=("Segoe UI", 11), fg=self.INK,
                                  bg=self.PANEL, relief="flat",
                                  padx=10, pady=10)
        self.input_text.pack(fill="x")

        # Tombol-tombol aksi.
        actions = tk.Frame(outer, bg=self.BG)
        actions.pack(fill="x", pady=(12, 6))
        ttk.Button(actions, text="Ubah sekarang",
                   command=self.convert).pack(side="left")
        ttk.Button(actions, text="Salin hasil", style="Plain.TButton",
                   command=self.copy_result).pack(side="left", padx=(8, 0))
        ttk.Button(actions, text="Isi contoh", style="Plain.TButton",
                   command=self.fill_example).pack(side="left", padx=(8, 0))
        ttk.Button(actions, text="Hapus", style="Plain.TButton",
                   command=self.clear_all).pack(side="left", padx=(8, 0))

        self.status_var = tk.StringVar(
            value="Tulis sesuatu di atas, lalu tekan Ubah sekarang.")
        self.status_label = tk.Label(outer, textvariable=self.status_var,
                                     bg=self.BG, fg=self.MUTED,
                                     font=("Segoe UI", 9), wraplength=860,
                                     justify="left")
        self.status_label.pack(anchor="w", pady=(0, 10))

        # Kotak hasil.
        self.output_label = tk.Label(outer, text="Hasilnya (bahasa mesin):",
                                     bg=self.BG, fg=self.INK,
                                     font=("Segoe UI Semibold", 10))
        self.output_label.pack(anchor="w", pady=(2, 6))
        output_card = tk.Frame(outer, bg=self.ACCENT_PALE,
                               highlightbackground=self.LINE,
                               highlightthickness=1)
        output_card.pack(fill="x")
        self.output_text = tk.Text(output_card, height=4, wrap="word",
                                   font=("Consolas", 11), fg=self.INK,
                                   bg=self.ACCENT_PALE, relief="flat",
                                   padx=10, pady=10)
        self.output_text.pack(fill="x")
        self.output_text.configure(state="disabled")

        # Tabel rincian per byte.
        tk.Label(outer, text="Rincian per byte (kode ASCII):",
                 bg=self.BG, fg=self.INK,
                 font=("Segoe UI Semibold", 10)).pack(anchor="w", pady=(14, 6))
        table_card = tk.Frame(outer, bg=self.PANEL,
                              highlightbackground=self.LINE,
                              highlightthickness=1)
        table_card.pack(fill="both", expand=True)
        columns = ("no", "biner", "desimal", "karakter")
        self.tree = ttk.Treeview(table_card, columns=columns, show="headings",
                                selectmode="browse")
        self.tree.heading("no", text="BYTE KE")
        self.tree.heading("biner", text="BINER (8 DIGIT)")
        self.tree.heading("desimal", text="KODE DESIMAL")
        self.tree.heading("karakter", text="KARAKTER")
        self.tree.column("no", width=90, anchor="center")
        self.tree.column("biner", width=260, anchor="center")
        self.tree.column("desimal", width=160, anchor="center")
        self.tree.column("karakter", width=180, anchor="center")
        scroll = ttk.Scrollbar(table_card, orient="vertical",
                               command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        tk.Label(outer, text="Satu huruf biasa = satu byte = 8 digit biner. "
                 "Contoh: huruf A itu 65, binernya 01000001.",
                 bg=self.BG, fg=self.MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(10, 0))

    def set_mode(self, mode):
        self.mode = mode
        if mode == self.MODE_TEXT:
            self.btn_mode_text.configure(bg=self.ACCENT, fg="#FFFFFF",
                                         relief="flat")
            self.btn_mode_binary.configure(bg=self.PANEL, fg=self.INK,
                                           relief="solid")
            self.input_label.configure(text="Tulis bahasa kita di sini:")
            self.output_label.configure(text="Hasilnya (bahasa mesin):")
        else:
            self.btn_mode_text.configure(bg=self.PANEL, fg=self.INK,
                                         relief="solid")
            self.btn_mode_binary.configure(bg=self.ACCENT, fg="#FFFFFF",
                                           relief="flat")
            self.input_label.configure(text="Tempel kode biner di sini:")
            self.output_label.configure(text="Hasilnya (bahasa kita):")
        # Kotak masukan ikut dibersihkan, supaya teks dari mode lama
        # tidak kebawa dan malah dianggap kode biner (atau sebaliknya).
        self.input_text.delete("1.0", "end")
        self.clear_output_only()
        self.set_status("Mode diubah. Tulis sesuatu di atas, lalu tekan "
                        "Ubah sekarang.")

    def set_status(self, message, error=False):
        self.status_var.set(message)
        self.status_label.configure(fg=self.RED if error else self.MUTED)

    def clear_output_only(self):
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.configure(state="disabled")
        for item in self.tree.get_children():
            self.tree.delete(item)

    def show_output(self, text):
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", text)
        self.output_text.configure(state="disabled")

    def show_rows(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in byte_rows(data):
            self.tree.insert("", "end", values=row)

    def convert(self):
        raw = self.input_text.get("1.0", "end").strip()
        if not raw:
            self.clear_output_only()
            self.set_status("Kotaknya masih kosong. Tulis dulu, baru diubah.",
                            error=True)
            return
        try:
            if self.mode == self.MODE_TEXT:
                result = text_to_binary(raw)
                data = raw.encode("utf-8")
                self.show_output(result)
                self.show_rows(data)
                self.set_status(
                    "{} karakter, {} byte. Setiap byte di tabel bawah "
                    "menunjukkan biner dan kode desimalnya.".format(
                        len(raw), len(data)))
            else:
                result = binary_to_text(raw)
                cleaned = "".join(raw.split())
                data = bytes(int(cleaned[i:i + 8], 2)
                             for i in range(0, len(cleaned), 8))
                self.show_output(result)
                self.show_rows(data)
                self.set_status(
                    "{} byte berhasil diubah kembali menjadi "
                    "{} karakter.".format(len(data), len(result)))
        except ValueError as exc:
            self.clear_output_only()
            self.set_status(str(exc), error=True)

    def copy_result(self):
        result = self.output_text.get("1.0", "end").strip()
        if not result:
            self.set_status("Belum ada hasil yang bisa disalin. Ubah dulu.",
                            error=True)
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(result)
        self.set_status("Hasil sudah disalin, tinggal ditempel di tempat lain.")

    def fill_example(self):
        self.input_text.delete("1.0", "end")
        if self.mode == self.MODE_TEXT:
            self.input_text.insert("1.0", "Halo, selamat pagi!")
        else:
            self.input_text.insert("1.0", "01001000 01100001 01101100 01101111")
        self.convert()

    def clear_all(self):
        self.input_text.delete("1.0", "end")
        self.clear_output_only()
        self.set_status("Sudah dibersihkan. Tulis sesuatu di atas, lalu "
                        "tekan Ubah sekarang.")


def main():
    root = tk.Tk()
    TeksMesinApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
