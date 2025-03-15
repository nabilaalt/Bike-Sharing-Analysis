# Analisis Data dengan Python - Dicoding

## 📌 Deskripsi Proyek
Proyek ini merupakan bagian dari pembelajaran analisis data di Dicoding. Dalam proyek ini, dilakukan eksplorasi dan analisis data menggunakan Python serta berbagai pustaka data science. Analisis dilakukan terhadap data penyewaan sepeda untuk memahami pola penggunaan berdasarkan berbagai faktor seperti waktu, hari, dan kondisi cuaca.

## 📊 Tujuan Analisis
1. Menentukan pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda.
2. Menganalisis pola penyewaan sepeda pada hari kerja, hari libur, dan hari biasa.
3. Mengidentifikasi periode waktu dengan jumlah penyewaan sepeda tertinggi dan terendah.

## 🔧 Teknologi dan Tools yang Digunakan
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook 

## 🚀 Cara Install dan Menjalankan Proyek

### 1. **Clone Repository**
```bash
git clone https://github.com/nabilaalt/analisis-data-dicoding.git
cd "C:\Users\Lenovo\Documents\Program\Python\analisis data"
```

### 2. **Buat Virtual Environment (Opsional, tetapi Disarankan)**
```bash
python -m venv venv
```
Aktifkan virtual environment sesuai dengan sistem operasi Anda:
- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **MacOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 3. **Install Dependencies**
Disarankan untuk menginstal pustaka yang dibutuhkan menggunakan `requirements.txt` agar memastikan kompatibilitas pustaka dengan proyek ini.
```bash
pip install -r requirements.txt
```

### 4. **Jalankan Jupyter Notebook**
```bash
jupyter notebook
```
Kemudian, buka file `notebook.ipynb` untuk mulai menjalankan analisis.

### 5. **Menjalankan Dashboard**
Jika proyek ini memiliki dashboard yang perlu dijalankan, pastikan Anda berada di direktori yang sesuai, lalu jalankan perintah berikut:
```bash
python "C:\Users\Lenovo\Documents\Program\Python\analisis data\dashboard.py"
```
### 6. **Run Streamlit Apps**
```bash
streamlit run dashboard.py
```

## 📈 Hasil Analisis

1. **Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda**  
   Cuaca cerah menunjukkan jumlah penyewaan sepeda tertinggi, sedangkan kondisi berkabut atau mendung juga memiliki tingkat penyewaan yang cukup baik. Sebaliknya, hujan mengurangi jumlah penyewaan secara signifikan, menunjukkan bahwa cuaca buruk berdampak negatif terhadap aktivitas penyewaan sepeda.

2. **Pola Penyewaan Sepeda Berdasarkan Hari**  
   Penyewaan sepeda lebih tinggi pada hari kerja dibandingkan akhir pekan, dengan Jumat sebagai hari dengan jumlah penyewaan tertinggi dan Minggu sebagai yang terendah. Selain itu, hari biasa memiliki tingkat penyewaan lebih tinggi dibandingkan hari libur nasional.

3. **Pola Penyewaan Berdasarkan Waktu**  
   Jumlah penyewaan sepeda tertinggi terjadi pada siang hari (12:00 - 18:00), menunjukkan bahwa banyak orang menggunakan sepeda untuk keperluan kerja atau aktivitas lainnya. Sementara itu, penyewaan sepeda paling rendah terjadi pada malam hari (00:00 - 06:00), yang mencerminkan minimnya aktivitas penggunaan sepeda pada waktu tersebut.

---
_Proyek ini dibuat untuk memenuhi tugas Analisis Data di Dicoding._