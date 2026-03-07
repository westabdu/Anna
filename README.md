# 🤖 A.N.N.A Mobile Ultimate
**Adaptive Neural Network Assistant – Yeni Nesil Yapay Zeka Asistanınız**

![Android](https://img.shields.io/badge/Platform-Android-3DDC84?style=for-the-badge&logo=android&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flet](https://img.shields.io/badge/Framework-Flet-00A6D6?style=for-the-badge&logo=flutter&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

---

## 📖 Hakkında

**A.N.N.A (Advanced Neural Network Assistant)**, Android cihazlar için özel olarak geliştirilmiş, çift çekirdekli yapay zeka desteği sunan, artırılmış gerçeklik (AR) ve gelişmiş sesli komut yeteneklerine sahip yeni nesil bir asistandır.

Masaüstü bilgisayarların işlem gücünü mobilin özgürlüğüyle birleştiren bu proje; günlük işlerinizi otomatize eder, telefonunuzun donanımını analiz eder ve kameranız aracılığıyla dünyayı daha akıllıca yorumlamanızı sağlar.

---

---

## ✨ Öne Çıkan Özellikler

| Kategori | Özellikler |
| :--- | :--- |
| **🧠 Yapay Zeka** | Gemini & Groq API entegrasyonu ile kesintisiz, hızlı ve doğal sohbet |
| **🕶️ AR & OCR** | Gerçek zamanlı metin okuma, QR/barkod tarama, nesne tanıma, renk analizi |
| **🎤 Sesli Asistan** | Wake word ("Jarvis", "Bilgisayar") ile eller serbest komut, Edge-TTS/gTTS desteği |
| **🔐 Güvenlik** | PIN kodu, desen kilidi, biyometrik parmak izi ve çok katmanlı giriş sistemi |
| **📱 Sistem** | Batarya, depolama, RAM, CPU bilgileri; rehber yönetimi ve arama simülasyonu |
| **🌤️ Günlük Araçlar** | Canlı hava durumu, güncel haberler, zamanlanmış hatırlatıcılar |
| **🎨 Dinamik Tema** | 3 farklı tema (Koyu, Okyanus, Buz) ve glassmorphism efektli modern arayüz |

---

---

## 🖼️ Ekran Görüntüleri

> *Not: Ekran görüntüleri yakında eklenecektir.*

<p align="center">
  <img src="https://via.placeholder.com/200x400.png?text=Giris+Ekrani" width="200" alt="Giriş Ekranı"/>
  <img src="https://via.placeholder.com/200x400.png?text=Sohbet+Arayuzu" width="200" alt="Sohbet Arayüzü"/>
  <img src="https://via.placeholder.com/200x400.png?text=AR+Kamera" width="200" alt="AR Kamera"/>
</p>

---

## 📂 Klasör Yapısı

Proje, sürdürülebilirlik ve modülerlik esasına göre aşağıdaki gibi yapılandırılmıştır:

```text
anna_mobile/
├── src/
│   ├── api/                  # Dış API servisleri
│   │   ├── gemini.py
│   │   ├── groq.py
│   │   ├── weather.py
│   │   └── news.py
│   ├── auth/                 # Güvenlik ve giriş sistemleri
│   │   └── login.py
│   ├── modules/              # Temel mobil fonksiyonlar
│   │   ├── ar_vision.py      # Artırılmış gerçeklik ve kamera
│   │   ├── contacts.py
│   │   ├── ocr.py            # Görüntü işleme
│   │   ├── phone.py
│   │   ├── reminders.py
│   │   ├── about.py          # Sistem künyesi
│   │   └── mobile_voice_enhanced.py # Ses motoru
│   └── utils/                # Yardımcı araçlar ve UI
│       └── theme.py
├── main.py                   # Uygulama ana giriş noktası (Entry Point)
├── requirements.txt          # Python bağımlılıkları (Saf liste)
└── pyproject.toml            # Flet/Flutter derleme ayarları
```

---
## 🚀 Hızlı Kurulum

Kendi bilgisayarınızda A.N.N.A'yı çalıştırmak için aşağıdaki adımları izleyin:

```bash
### 1. Depoyu Klonlayın
git clone https://github.com/westabdu/anna_mobile.git
cd anna_mobile

2. Sanal Ortam Oluşturun

python -m venv venv
# Linux / macOS
source venv/bin/activate
#windows
venv\Scripts\activate

3. Bağımlılıkları Yükleyin

pip install --upgrade pip
pip install -r requirements.txt

4. API Anahtarlarını Ayarlayın

Proje dizininde bir .env dosyası oluşturun ve içine şu bilgileri yerleştirin 

GEMINI_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key
OPENWEATHER_API_KEY=your_openweather_key
NEWS_API_KEY=your_news_key
PICOVOICE_ACCESS_KEY=your_picvoice_key

5. Uygulamayı Çalıştırın
python main.py
```
---

## 📱 APK Oluşturma (Build Alma)
```bash
Uygulamayı Android cihazlarınızda test etmek için kendi APK'nızı derleyebilirsiniz:

# Sanal Ortam Aktifken
flet build apk --release 
# Çalışmazsa 
flet build apk

Oluşan APK dosyası build/apk/ klasörü içerisinde bulunacaktır.
```

---

## 🔑 API Anahtarları Kaynakları
Sistemin Tam Kapasite Çalışması İçin Aşşağıdaki API Anahtarlarına İhtiyacınız Vardır:

| API | Kaynak |
| :--- | :--- |
| **Google Gemini API** | Google AI studio |
| **Groq API** | Groq Console |
| **OpenWeather API** | openWeather |
| **NewsAPI** | NewsAPI |
| **Picovoice (Wake Word)** | Picovoice Console |

---

---
🤝 Katkıda Bulunma

Bu Projeye Katkı Sağlamak İsterseniz:

1.Depoyu Fork Edin.
2.Yeni Bir Dal Oluşturun: git checkout -b yeni-ozellik
3.Değişikliklerinizi commit edin: git commit -m 'Harika bir özellik eklendi'
4.Dalınızı push edin: git push origin yeni-ozellik
5.Bir Pull Request açın.

---

---

👨‍💻 Geliştirici & İletişim
Westabdu tarafından geliştirilmiştir.

GitHub: @westabdu

Instagram: @westabdu

E-posta: abdurahmansabsabi372@gmail.com

---

<div align="center"> <p>Projeyi faydalı bulduysanız ⭐️ bırakmayı unutmayın!</p> <p>📄 <strong>Lisans:</strong> Bu proje MIT Lisansı ile lisanslanmıştır.</p> </div>
