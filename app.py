from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

"""
Nama : Muhammad Faza Abiyyu
NIM : 2211102010
Kelas : S1-IF-10-K
"""


# Local Database dengan XAMPP
def db_connection():
    conn = None
    try:
        conn = pymysql.connect(
            host="127.0.0.1",
            database="pemrograman_fungsional",
            user="root",
            # password="",
            port=3306,
            cursorclass=pymysql.cursors.DictCursor,
        )
    except pymysql.Error as e:
        print(e)
    return conn


@app.route("/books", methods=["GET", "POST", "PUT", "DELETE"])
def manage_books():
    conn = db_connection()
    cursor = conn.cursor()
    # GET untuk menampilkan data dari tabel
    if request.method == "GET":
        cursor.execute("SELECT * FROM books")
        books = [
            dict(
                idbuku=row["idbuku"],
                nama_buku=row["nama_buku"],
                penulis=row["penulis"],
                rating=row["rating"],
                halaman=row["halaman"],
                tanggal_terbit=row["tanggal_terbit"],
                penerbit=row["penerbit"],
                stok=row["stok"],
            )
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)
    # POST untuk menambahkan data dari tabel
    if request.method == "POST":
        add_nama_buku = request.form["nama_buku"]
        add_penulis = request.form["penulis"]
        add_rating = request.form["rating"]
        add_halaman = request.form["halaman"]
        add_tanggal_terbit = request.form["tanggal_terbit"]
        add_penerbit = request.form["penerbit"]
        add_stok = request.form["stok"]

        query_insert = """
            INSERT INTO books (nama_buku, penulis, rating, halaman, tanggal_terbit, penerbit, stok)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query_insert,
            (
                add_nama_buku,
                add_penulis,
                add_rating,
                add_halaman,
                add_tanggal_terbit,
                add_penerbit,
                add_stok,
            ),
        )
        conn.commit()
        return "Berhasil Menambahkan Data Buku."
    # PUT untuk memperbarui data dari tabel
    if request.method == "PUT":
        update_idbuku = request.form["idbuku"]
        update_nama_buku = request.form["nama_buku"]
        update_penulis = request.form["penulis"]
        update_rating = request.form["rating"]
        update_halaman = request.form["halaman"]
        update_tanggal_terbit = request.form["tanggal_terbit"]
        update_penerbit = request.form["penerbit"]
        update_stok = request.form["stok"]

        query_update = """
            UPDATE books
            SET nama_buku=%s, penulis=%s, rating=%s, halaman=%s, tanggal_terbit=%s, penerbit=%s, stok=%s
            WHERE idbuku=%s
        """

        cursor.execute(
            query_update,
            (
                update_nama_buku,
                update_penulis,
                update_rating,
                update_halaman,
                update_tanggal_terbit,
                update_penerbit,
                update_stok,
                update_idbuku,
            ),
        )
        conn.commit()
        return "Berhasil Memperbarui Data Buku."
    # DELETE untuk menghapus data dari tabel
    if request.method == "DELETE":
        delete_idbuku = request.form["idbuku"]

        query_delete = """DELETE FROM books WHERE idbuku=%s"""

        cursor.execute(query_delete, (delete_idbuku,))
        conn.commit()
        return "Berhasil Menghapus Data Buku."


if __name__ == "__main__":
    app.run(debug=True)
