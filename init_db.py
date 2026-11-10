import sqlite3

DB_NAME = "kutuphane.db"

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

def veritabani_olustur(db_path=DB_NAME):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS kitaplar")

    cursor.execute("""
        CREATE TABLE kitaplar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            baslik TEXT NOT NULL,
            yazar TEXT NOT NULL,
            kategori TEXT NOT NULL,
            yayin_yili INTEGER,
            sayfa_sayisi INTEGER,
            isbn TEXT
        )
    """)

    cursor.executemany("""
        INSERT INTO kitaplar (baslik, yazar, kategori, yayin_yili, sayfa_sayisi, isbn)
        VALUES (?, ?, ?, ?, ?, ?)
    """, KITAPLAR_VERISI)

    conn.commit()
    conn.close()
    print(f"Başarılı: '{db_path}' veritabanı oluşturuldu ve {len(KITAPLAR_VERISI)} kitap eklendi.")

if __name__ == "__main__":
    veritabani_olustur()
