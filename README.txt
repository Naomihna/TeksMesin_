Tugas Individu
TeksMesin - Bahasa Kita ke Bahasa Mesin

Aplikasi ini dibuat pakai Python, tampilannya pakai Tkinter.
Intinya gampang: kita nulis kalimat biasa, terus aplikasi ini
ngubah kalimat itu jadi deretan 0 dan 1, alias bahasa mesin.
Sebaliknya juga bisa, kode biner ditempel, terus diubah lagi
jadi kalimat biasa.

Cara jalaninnya, tinggal klik dua kali file TeksMesin.exe.
Nggak perlu install Python, nggak perlu compile lagi.

Cara pakainya:
Pertama pilih dulu mau ke arah mana, ada tombol Teks ke biner
sama Biner ke teks di atas. Terus tulis di kotak yang atas,
lalu tekan Ubah sekarang. Hasilnya muncul di kotak bawah,
plus ada tabel rincian per byte di bawahnya, jadi kelihatan
tiap huruf itu kode desimalnya berapa dan binernya apa.
Kalau mau nyoba cepat, tekan aja Isi contoh. Kalau hasilnya
mau dipakai di tempat lain, tekan Salin hasil. Kalau mau
mulai dari awal lagi, tekan Hapus.

Sedikit penjelasan biar gampang kalau ditanya: tiap huruf itu
punya kode angka, namanya kode ASCII. Contohnya huruf A itu
65, terus 65 itu kalau diubah ke biner jadi 01000001, jadi
satu huruf itu diwakili 8 digit biner. Kode desimalnya bisa
dilihat juga di Google, tinggal cari tabel ASCII.

Buat Colab sama GitHub: file TeksMesin_Colab.ipynb ini tinggal
di-upload ke Google Colab lewat menu File, terus Upload notebook,
habis itu jalankan semua selnya dari atas ke bawah. Kalau mau
taruh di GitHub, tinggal bikin repository baru, terus upload
file TeksMesin.py, TeksMesin_Colab.ipynb, sama README ini.
Nanti notebooknya juga bisa dibuka langsung dari GitHub lewat
Colab. Versi Colab ini isinya logika konversi yang sama, cuma
pakai kolom isian, soalnya tampilan jendela Tkinter itu nggak
bisa jalan di browser Colab.

Versi webnya juga ada, namanya index.html, satu file saja dan
langsung bisa jalan di browser. Cara menampilkannya lewat
GitHub Pages ada di file CARA_GITHUB_PAGES.txt, intinya
tinggal upload index.html ke folder paling atas di repository,
terus nyalakan Pages di Settings repository.

Isi folder ini:
TeksMesin.exe, ini file yang udah di-compile, ini yang
dikumpulin.
TeksMesin.py, ini file Python aslinya, buat yang mau lihat
kodenya.
TeksMesin_Colab.ipynb, ini versi notebooknya buat Colab.
index.html, ini versi webnya buat GitHub Pages.
CARA_GITHUB_PAGES.txt, ini cara menampilkan versi webnya.
README.txt, file ini.

Satu catatan kecil, karena file exe ini nggak pakai tanda
tangan digital, kadang Windows nampilin peringatan SmartScreen
pas pertama kali dibuka. Kalau muncul, pilih aja More info,
terus Run anyway.
