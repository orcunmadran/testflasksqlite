import sqlite3
import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
DB_NAME = "kutuphane.db"

# 50 Adet Kitap Verisi (Başlık, Yazar, Kategori, Yayın Yılı, Sayfa Sayısı, ISBN)
KITAPLAR_VERISI = [
    ("İnce Memed 1", "Yaşar Kemal", "Türk Edebiyatı", 1955, 436, "9789750807145"),
    ("Tutunamayanlar", "Oğuz Atay", "Türk Edebiyatı", 1972, 724, "9789754700114"),
    ("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", "Türk Edebiyatı", 1961, 382, "9789759955762"),
    ("Kürk Mantolu Madonna", "Sabahattin Ali", "Türk Edebiyatı", 1943, 160, "9789753638029"),
    ("Puslu Kıtalar Atlası", "İhsan Oktay Anar", "Türk Edebiyatı", 1995, 238, "9789754704723"),
    ("Kara Kitap", "Orhan Pamuk", "Türk Edebiyatı", 1990, 444, "9789750826085"),
    ("Aylak Adam", "Yusuf Atılgan", "Türk Edebiyatı", 1959, 192, "9789750800542"),
    ("Çalıkuşu", "Reşat Nuri Güntekin", "Türk Edebiyatı", 1922, 544, "9789751026064"),
    ("Huzur", "Ahmet Hamdi Tanpınar", "Türk Edebiyatı", 1949, 415, "9789759955779"),
    ("Kuyucaklı Yusuf", "Sabahattin Ali", "Türk Edebiyatı", 1937, 221, "9789753638036"),
    ("Yaban", "Yakup Kadri Karaosmanoğlu", "Türk Edebiyatı", 1932, 215, "9789754700589"),
    ("Bereketli Topraklar Üzerinde", "Orhan Kemal", "Türk Edebiyatı", 1954, 405, "9789752894587"),
    ("Sinekli Bakkal", "Halide Edib Adıvar", "Türk Edebiyatı", 1936, 476, "9789750708244"),
    ("Eylül", "Mehmet Rauf", "Türk Edebiyatı", 1901, 288, "9789754587098"),
    ("Anayurt Oteli", "Yusuf Atılgan", "Türk Edebiyatı", 1973, 144, "9789750800573"),
    ("Tehlikeli Oyunlar", "Oğuz Atay", "Türk Edebiyatı", 1973, 479, "9789754700541"),
    ("Benim Adım Kırmızı", "Orhan Pamuk", "Türk Edebiyatı", 1998, 472, "9789750826054"),
    ("Serenad", "Zülfü Livaneli", "Türk Edebiyatı", 2011, 481, "9786050900286"),
    ("Aşk-ı Memnu", "Halit Ziya Uşaklıgil", "Türk Edebiyatı", 1900, 514, "9789754587111"),
    ("Suç ve Ceza", "Fyodor Dostoyevski", "Dünya Klasikleri", 1866, 687, "9789754589023"),
    ("Sefiller", "Victor Hugo", "Dünya Klasikleri", 1862, 1724, "9789754589405"),
    ("1984", "George Orwell", "Bilim Kurgu & Distopya", 1949, 352, "9789750718533"),
    ("Hayvan Çiftliği", "George Orwell", "Bilim Kurgu & Distopya", 1945, 152, "9789750719387"),
    ("Cesur Yeni Dünya", "Aldous Huxley", "Bilim Kurgu & Distopya", 1932, 272, "9789756902165"),
    ("Fahrenheit 451", "Ray Bradbury", "Bilim Kurgu & Distopya", 1953, 208, "9786053757818"),
    ("Dönüşüm", "Franz Kafka", "Dünya Klasikleri", 1915, 74, "9789754587449"),
    ("Dava", "Franz Kafka", "Dünya Klasikleri", 1925, 256, "9789750726422"),
    ("Bülbülü Öldürmek", "Harper Lee", "Dünya Klasikleri", 1960, 355, "9789755705859"),
    ("Yüzyıllık Yalnızlık", "Gabriel García Márquez", "Dünya Klasikleri", 1967, 464, "9789750719363"),
    ("Yabancı", "Albert Camus", "Felsefe & Düşünce", 1942, 112, "9789750726439"),
    ("Veba", "Albert Camus", "Dünya Klasikleri", 1947, 304, "9789750726460"),
    ("Savaş ve Barış", "Lev Tolstoy", "Dünya Klasikleri", 1869, 1225, "9789754587166"),
    ("Anna Karenina", "Lev Tolstoy", "Dünya Klasikleri", 1877, 1062, "9789754587159"),
    ("Karamazov Kardeşler", "Fyodor Dostoyevski", "Dünya Klasikleri", 1880, 840, "9789754589030"),
    ("Yeraltından Notlar", "Fyodor Dostoyevski", "Dünya Klasikleri", 1864, 140, "9789754589047"),
    ("Simyacı", "Paulo Coelho", "Dünya Edebiyatı", 1988, 184, "9789750726438"),
    ("Küçük Prens", "Antoine de Saint-Exupéry", "Dünya Klasikleri", 1943, 112, "9789750726415"),
    ("Don Kişot", "Miguel de Cervantes", "Dünya Klasikleri", 1605, 863, "9789750802584"),
    ("İlahi Komedya", "Dante Alighieri", "Dünya Klasikleri", 1320, 798, "9789753294003"),
    ("Dune", "Frank Herbert", "Bilim Kurgu & Distopya", 1965, 712, "9786053754794"),
    ("Vakıf", "Isaac Asimov", "Bilim Kurgu & Distopya", 1951, 256, "9786053756668"),
    ("Mülksüzler", "Ursula K. Le Guin", "Bilim Kurgu & Distopya", 1974, 344, "9789753420167"),
    ("Yüzüklerin Efendisi: Yüzük Kardeşliği", "J.R.R. Tolkien", "Fantastik", 1954, 528, "9789753421621"),
    ("Hobbit", "J.R.R. Tolkien", "Fantastik", 1937, 336, "9789752733732"),
    ("Sapiens: İnsan Türünün Kısa Bir Tarihi", "Yuval Noah Harari", "Tarih & Bilim", 2011, 412, "9786055029357"),
    ("Homo Deus: Yarının Kısa Bir Tarihi", "Yuval Noah Harari", "Tarih & Bilim", 2015, 448, "9786059915663"),
    ("Kozmos", "Carl Sagan", "Tarih & Bilim", 1980, 384, "9789752107724"),
    ("Zamanın Kısa Tarihi", "Stephen Hawking", "Tarih & Bilim", 1988, 256, "9786051118574"),
    ("Türlerin Kökeni", "Charles Darwin", "Tarih & Bilim", 1859, 502, "9786051715308"),
    ("Devlet", "Platon", "Felsefe & Düşünce", -375, 376, "9789754587173")
]

def get_db_connection():
    """SQLite veritabanı bağlantısı oluşturur ve satırları sözlük (dict) gibi döndürür."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Veritabanı tablosunu oluşturur ve eğer boşsa 50 kitabı ekler."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabloyu oluştur
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kitaplar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            baslik TEXT NOT NULL,
            yazar TEXT NOT NULL,
            kategori TEXT NOT NULL,
            yayin_yili INTEGER,
            sayfa_sayisi INTEGER,
            isbn TEXT
        )
    """)
    
    # Kayıt sayısını kontrol et, boşsa 50 kitabı ekle
    cursor.execute("SELECT COUNT(*) FROM kitaplar")
    kayit_sayisi = cursor.fetchone()[0]
    
    if kayit_sayisi == 0:
        cursor.executemany("""
            INSERT INTO kitaplar (baslik, yazar, kategori, yayin_yili, sayfa_sayisi, isbn)
            VALUES (?, ?, ?, ?, ?, ?)
        """, KITAPLAR_VERISI)
        conn.commit()
        print(f"[BİLGİ] '{DB_NAME}' oluşturuldu ve 50 kitap kaydı eklendi.")
    
    conn.close()

# HTML5 Arayüz Şablonu (Jinja2 + Bootstrap 5)
HTML_SABLONU = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask & SQLite Kitap Veritabanı</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8fafc; font-family: system-ui, -apple-system, sans-serif; }
        .sql-banner { background-color: #1e293b; color: #38bdf8; font-family: monospace; padding: 12px 16px; border-radius: 8px; }
        .table-hover tbody tr:hover { background-color: #f1f5f9; }
    </style>
</head>
<body>
    <header class="bg-dark text-white py-4 mb-4 shadow-sm">
        <div class="container d-flex justify-content-between align-items-center">
            <div>
                <h1 class="h3 mb-1">📚 Kütüphane Veritabanı (Flask + SQLite3)</h1>
                <p class="text-secondary mb-0 small">Veriler Python arka ucundaki <code>kutuphane.db</code> dosyasından okunmaktadır.</p>
            </div>
            <div class="text-end">
                <span class="badge bg-primary fs-6">Listelenen: {{ kitaplar|length }} / 50</span>
                <a href="/api/kitaplar" target="_blank" class="btn btn-sm btn-outline-light ms-2">JSON API Gör</a>
            </div>
        </div>
    </header>

    <main class="container mb-5">
        <!-- Arama ve Filtreleme Formu -->
        <section class="card shadow-sm border-0 mb-4">
            <div class="card-body">
                <form method="GET" action="/" class="row g-3 align-items-end">
                    <div class="col-md-5">
                        <label for="arama" class="form-label fw-semibold small text-secondary">Kitap Adı, Yazar veya ISBN Ara</label>
                        <input type="text" class="form-control" id="arama" name="q" value="{{ arama }}" placeholder="Örn: Sabahattin Ali, Dune, 1984...">
                    </div>
                    <div class="col-md-4">
                        <label for="kategori" class="form-label fw-semibold small text-secondary">Kategoriye Göre Filtrele</label>
                        <select class="form-select" id="kategori" name="kategori">
                            <option value="">Tüm Kategoriler</option>
                            {% for kat in kategoriler %}
                                <option value="{{ kat }}" {% if secili_kategori == kat %}selected{% endif %}>{{ kat }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="col-md-3 d-flex gap-2">
                        <button type="submit" class="btn btn-primary w-100">Sorgula</button>
                        <a href="/" class="btn btn-outline-secondary">Sıfırla</a>
                    </div>
                </form>
            </div>
        </section>

        <!-- Çalıştırılan SQL Sorgusu Bilgisi -->
        <section class="mb-3">
            <div class="sql-banner shadow-sm">
                <span class="text-secondary">Çalışan SQL:</span> {{ calisan_sql }}
            </div>
        </section>

        <!-- Kitap Tablosu -->
        <section class="card shadow-sm border-0">
            <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                    <thead class="table-light">
                        <tr>
                            <th>#ID</th>
                            <th>Kitap Başlığı</th>
                            <th>Yazar</th>
                            <th>Kategori</th>
                            <th>Yayın Yılı</th>
                            <th>Sayfa</th>
                            <th>ISBN</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% if kitaplar %}
                            {% for kitap in kitaplar %}
                            <tr>
                                <td class="text-secondary fw-bold">{{ kitap['id'] }}</td>
                                <td class="fw-semibold">{{ kitap['baslik'] }}</td>
                                <td>{{ kitap['yazar'] }}</td>
                                <td><span class="badge bg-secondary bg-opacity-10 text-dark border">{{ kitap['kategori'] }}</span></td>
                                <td>{{ "M.Ö. " ~ (kitap['yayin_yili'] | abs) if kitap['yayin_yili'] < 0 else kitap['yayin_yili'] }}</td>
                                <td>{{ kitap['sayfa_sayisi'] }}</td>
                                <td><code class="text-muted">{{ kitap['isbn'] }}</code></td>
                            </tr>
                            {% endfor %}
                        {% else %}
                            <tr>
                                <td colspan="7" class="text-center py-4 text-muted">Arama kriterlerinize uygun kitap kaydı bulunamadı.</td>
                            </tr>
                        {% endif %}
                    </tbody>
                </table>
            </div>
        </section>
    </main>
</body>
</html>
"""

@app.route("/")
def index():
    arama = request.args.get("q", "").strip()
    secili_kategori = request.args.get("kategori", "").strip()
    
    conn = get_db_connection()
    
    # Dinamik SQL sorgusu oluşturma (SQL Injection korumalı parametreli yapı)
    sorgu = "SELECT * FROM kitaplar WHERE 1=1"
    parametreler = []
    
    if arama:
        sorgu += " AND (baslik LIKE ? OR yazar LIKE ? OR isbn LIKE ?)"
        arama_terimi = f"%{arama}%"
        parametreler.extend([arama_terimi, arama_terimi, arama_terimi])
        
    if secili_kategori:
        sorgu += " AND kategori = ?"
        parametreler.append(secili_kategori)
        
    sorgu += " ORDER BY id ASC"
    
    kitaplar = conn.execute(sorgu, parametreler).fetchall()
    
    # Filtre menüsü için benzersiz kategorileri çek
    kategoriler_rows = conn.execute("SELECT DISTINCT kategori FROM kitaplar ORDER BY kategori").fetchall()
    kategoriler = [row["kategori"] for row in kategoriler_rows]
    
    conn.close()
    
    # Ekranda gösterilecek bilgi amaçlı SQL metni
    gorunen_sql = sorgu
    for p in parametreler:
        gorunen_sql = gorunen_sql.replace("?", f"'{p}'", 1)

    return render_template_string(
        HTML_SABLONU,
        kitaplar=kitaplar,
        kategoriler=kategoriler,
        arama=arama,
        secili_kategori=secili_kategori,
        calisan_sql=gorunen_sql
    )

@app.route("/api/kitaplar")
def api_kitaplar():
    """Veritabanındaki tüm kayıtları JSON formatında döndüren REST API uç noktası."""
    conn = get_db_connection()
    kitaplar = conn.execute("SELECT * FROM kitaplar ORDER BY id ASC").fetchall()
    conn.close()
    return jsonify([dict(kitap) for kitap in kitaplar])

if __name__ == "__main__":
    init_db()  # Uygulama başlarken veritabanını ve 50 kaydı hazırla
    app.run(debug=True, host="127.0.0.1", port=5000)