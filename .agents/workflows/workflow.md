---
description: HR Candidate Screening Project
---

/Verdiğim workflow'a göre Recruiment pipeline tracker uygulaması yapıcaksın:
-trigger (cv yükleme) -function (pdf parse etme)
-external api (google sheet'se aday bilgileri kaydetme)
-external api (gemini ai cv analizi ve aday sınıflandırması).  
-Api keylerim ve slack'im hazır.
 
### 1. Python Sanal Ortamını (Virtual Environment) Oluştur
 
 
### 2. requirements.txt dosyası oluştur ve gerekli kütüphane bağımlılıklarını yükle
 
 
### 3. .env dosyasını oluştur ve bu anahtarları yaz:
 
-Gemini_API_Key="GEMİNİ_ANAHTARI"
-GOOGLE_CREDENTIALS_FILE=credentials.json
-GOOGLE_SHEET_ID="GOOGLE_SHEET_ID"
-SLACK_WEBHOOK_URL="SLACK_WEBHOOK_URL"

 
### 4. Frontend Klasörü
Projeyi çalıştırmadan önce, arayüzün doğru görünmesi için `templates` klasörünün altında `index.html` dosyasının bulunduğundan emin ol.
 
### 5. Sunucuyu Başlat
 