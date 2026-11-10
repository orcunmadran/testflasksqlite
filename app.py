import sqlite3
import os
from flask import Flask, render_template, request, jsonify
from init_db import veritabani_olustur, DB_NAME

app = Flask(__name__)

def get_db_connection():
    """SQLite veritabanı bağlantısı açar ve sütun isimleriyle erişim sağlar."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    arama = request.args.get("q", "").strip()
    secili_kategori = request.args.get("kategori", "").strip()
    
    conn = get_db_connection()
    
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
    
    # Açılır liste (select) için benzersiz kategorileri al
    kategoriler_rows = conn.execute("SELECT DISTINCT kategori FROM kitaplar ORDER BY kategori").fetchall()
    kategoriler = [row["kategori"] for row in kategoriler_rows]
    
    conn.close()
    
    # Arayüzde çalışan SQL'i göstermek için formatlama
    gorunen_sql = sorgu
    for p in parametreler:
        gorunen_sql = gorunen_sql.replace("?", f"'{p}'", 1)

    return render_template(
        "index.html",
        kitaplar=kitaplar,
        kategoriler=kategoriler,
        arama=arama,
        secili_kategori=secili_kategori,
        calisan_sql=gorunen_sql
    )

@app.route("/api/kitaplar")
def api_kitaplar():
    """Kitap listesini JSON olarak döndüren API uç noktası."""
    conn = get_db_connection()
    kitaplar = conn.execute("SELECT * FROM kitaplar ORDER BY id ASC").fetchall()
    conn.close()
    return jsonify([dict(kitap) for kitap in kitaplar])

if __name__ == "__main__":
    # Eğer veritabanı dosyası henüz oluşturulmamışsa otomatik oluştur
    if not os.path.exists(DB_NAME):
        veritabani_olustur()
    app.run(debug=True, host="127.0.0.1", port=5000)
