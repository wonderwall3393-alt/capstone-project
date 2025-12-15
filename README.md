# Sphinx Net

[![Stars](https://img.shields.io/github/stars/username/sphinx-net.svg)](https://github.com/wonderwall3393-alt/capstone-project/stargazers)
[![Forks](https://img.shields.io/github/forks/username/sphinx-net.svg)](https://github.com/wonderwall3393-alt/capstone-project/network/members)
[![Watchers](https://img.shields.io/github/watchers/username/sphinx-net.svg)](https://github.com/wonderwall3393-alt/capstone-project/watchers)
[![GitHub license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/wonderwall3393-alt/capstone-project/blob/main/LICENSE)
[![platform](https://img.shields.io/badge/platform-Python_Native-blue.svg)](https://python.org/)

**Sphinx Net** adalah platform rekomendasi telekomunikasi (Telco) komprehensif yang dirancang untuk membantu pengguna menemukan paket internet yang paling tepat berdasarkan perilaku mereka menggunakan algoritma pencocokan berbasis AI. Proyek ini merupakan bagian dari **Capstone Project Tim A25-CS026**.

Berikan Bintang ⭐ pada repositori ini jika Anda menyukainya 😉.

![Sphinx Net Preview](./assets/screenshot/main-page.png)

## ✨ Tentang Sphinx Net

**Sphinx Net** menyediakan solusi cerdas untuk mempersonalisasi pengalaman internet Anda. Berbeda dengan penyedia layanan umum, platform kami menggunakan **Machine Learning** untuk menganalisis perangkat, kebiasaan penggunaan, dan anggaran Anda guna merekomendasikan paket data yang paling sesuai, mencegah pemborosan kuota, dan meningkatkan kepuasan pelanggan.

## 🏦 Fitur Utama

1.  ### 🤖 Rekomendasi Berbasis AI

    Dapatkan saran paket yang dipersonalisasi berdasarkan perilaku Anda menggunakan model RandomForest Classifier.

2.  ### 📝 Sistem Survei Interaktif

    Survei langkah demi langkah yang komprehensif untuk memahami kebutuhan spesifik Anda (Gaming, Streaming, atau Pekerjaan).

3.  ### 🔐 Fitur Autentikasi

    Sistem login dan registrasi yang aman untuk mengelola profil dan riwayat pembelian Anda.

4.  ### 📊 Visualisasi Data

    Pantau penggunaan data dan detail paket Anda melalui dasbor intuitif dengan grafik CSS native.

5.  ### 💳 Simulasi Transaksi

    Rasakan proses checkout yang mulus dengan pembuatan faktur digital dan verifikasi pembayaran.

6.  ### 📱 Desain Responsif

    Antarmuka yang dioptimalkan sepenuhnya dan bekerja sempurna di Desktop, Tablet, dan perangkat Seluler.

7.  ### 👤 Manajemen Profil Pengguna

    Kelola informasi pribadi dan lihat status paket aktif dengan mudah.

8.  ### 🌐 Halaman Landing Dinamis

    Manajemen status UI (User Interface) secara real-time untuk tamu dan pengguna yang sudah login.

## Tangkapan Layar (Screenshots)

### Antarmuka Pengguna

|                                                            |                                                               |                                                                 |
| :--------------------------------------------------------: | :-----------------------------------------------------------: | :-------------------------------------------------------------: |
|                     **Halaman Login**                      |                      **Halaman Daftar**                       |                        **Halaman Utama**                        |
|     ![Login Page](./assets/screenshot/login-page.png)      |    ![Register Page](./assets/screenshot/register-page.png)    |         ![Main Page](./assets/screenshot/main-page.png)         |
|                     **Halaman Survey**                     |                   **Halaman Katalog Paket**                   |                      **Pembayaran Sukses**                      |
|    ![Survey Page](./assets/screenshot/survey-page.png)     |  ![Pakckage Data Page](./assets/screenshot/package-page.png)  | ![Payment Success](./assets/screenshot/payment-succes-page.png) |
|                     **Invoice Sukses**                     |                     **Halaman Informasi**                     |                         **Halaman Tim**                         |
| ![Invoice Succes](./assets/screenshot/invoice-payment.png) | ![Information Page](./assets/screenshot/information-page.png) |         ![Team Page](./assets/screenshot/team-page.png)         |
|               **Halaman Tentang Sphinx Net**               |                   **Halaman Hubungi Kami**                    |                      **Halaman Dashboard**                      |
|     ![About Us](./assets/screenshot/about-us-page.png)     |      ![Contact](./assets/screenshot/contact-us-page.png)      |        ![About](./assets/screenshot/dashboard-page.png)         |

## 🛠️ Teknologi yang Digunakan (Tech Stack)

| Fitur            | Teknologi                                                                                                                                                                                                                                                                                                                                     |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Frontend Core    | ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) |
| Backend Server   | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) (Native HTTP Server)                                                                                                                                                                                                                   |
| Machine Learning | ![Scikit-Learn](https://img.shields.io/badge/scikit_learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white) ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)                                                                                                      |
| Penyimpanan Data | ![JSON](https://img.shields.io/badge/json-5E5C5C?style=for-the-badge&logo=json&logoColor=white)                                                                                                                                                                                                                                               |
| Ikon             | [FontAwesome](https://fonts.google.com/specimen/Inter?query=inter)                                                                                                                                                                                                                                                                            |
| Animasi          | [AOS Library](https://michalsnik.github.io/aos/)                                                                                                                                                                                                                                                                                              |
| Visualisasi Data | Native CSS Conic Gradients                                                                                                                                                                                                                                                                                                                    |

## 🚀 Cara Menjalankan

1.  Clone repositori ini

    ```bash
    git clone (https://github.com/wonderwall3393-alt/capstone-project))
    ```

2.  Masuk ke direktori proyek

    ```bash
    cd capstone-project
    ```

3.  Jalankan Server Backend (Python)

    ```bash
    # Pastikan Anda sudah menginstal Python
    python backend/hybrid_ml_survey_server.py
    ```

4.  Jalankan Aplikasi

    Buka file `index.html` atau `home-before.html` di browser Anda, atau gunakan live server.

## Kontributor

**Farid Fajar Abdillah**
<br>
[![Farid Fajar - LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/farid-fajar-abdilah-87ba18336/)
[![Farid Fajar - GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/wonderwall3393-alt)

**Ghulam Mushthofa**
<br>
[![Ghulam Mushthofa - LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ghulam-mushthofa)
[![Ghulam Mushthofa - GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ghulambelajar)

**Ahmad Nugrahadi**
<br>
[![Ahmad Nugrahadi - LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/nhadi23/)
[![Ahmad Nugrahadi - GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Nhadi23)

**Nasrun Adetiya**
<br>
[![Nasrun Adetiya - LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/nasyrun-adetiya-14b4a428b/)
[![Nasrun Adetiya - GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/adit321rr)

**Fathan Rezah**
<br>
[![Fathan Rezah - LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mas-rezah-04301727b/)
[![Fathan Rezah - GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/masrezah)

## 📚 Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file [LICENSE](LICENSE) untuk detail selengkapnya.

---

Terima kasih telah mengunjungi **Sphinx Net**! Mari hubungkan dunia dengan rekomendasi internet yang lebih baik.
