# Flask & SQLite3 Kütüphane Veritabanı

Bu proje, klasik Flask klasör mimarisi (`app.py`, `templates/`, `static/`) ve SQLite3 kullanılarak hazırlanmış 50 kitaplık örnek bir web uygulamasıdır.

## Klasör Yapısı
- `app.py`: Ana Flask uygulaması ve yönlendirmeler (routes)
- `init_db.py`: SQLite veritabanını (`kutuphane.db`) sıfırdan oluşturan ve 50 kitabı ekleyen kurulum betiği
- `kutuphane.db`: 50 kitap kaydını barındıran hazır SQLite3 veritabanı dosyası
- `templates/index.html`: Jinja2 & HTML5 şablon dosyası
- `static/style.css`: Özel CSS tasarım dosyası
- `requirements.txt`: Gerekli Python paketleri

## Kurulum ve Çalıştırma

1. Gerekli kütüphaneyi yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

2. Uygulamayı başlatın (`kutuphane.db` zaten paketin içinde hazırdır, silerseniz otomatik yeniden oluşturulur):
   ```bash
   python app.py
   ```

3. Tarayıcınızdan `http://127.0.0.1:5000` adresine gidin.
