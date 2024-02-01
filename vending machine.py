from tkinter import *
from tkinter import messagebox
import mysql.connector
from tkinter import ttk


class Vending_Machine(Tk):
    def __init__(self):
        super().__init__()
        self.title("Vending Machine")
        self.geometry("850x600")

        # Koneksi ke database
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="registrasi"
        )

        # Membuat kursor
        self.cursor = self.db.cursor()

        # Membuat dan menampilkan GUI
        self.tampilan_gui()

    def tampilan_gui(self):

        Label(self, text="Merk").grid(row=0, column=0, padx=10, pady=10)
        self.merk_entry = Entry(self, width=50)
        self.merk_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(self, text="Minuman").grid(row=1, column=0, padx=10, pady=10)
        self.minuman_entry = Entry(self, width=50)
        self.minuman_entry.grid(row=1, column=1, padx=10, pady=10)

        Label(self, text="Snack").grid(row=2, column=0, padx=10, pady=10)
        self.snack_entry = Entry(self, width=50)
        self.snack_entry.grid(row=2, column=1, padx=10, pady=10)

        Label(self, text="Harga").grid(row=3, column=0, padx=10, pady=10)
        self.harga_entry = Text(self, width=37, height=1)
        self.harga_entry.grid(row=3, column=1, padx=10, pady=10)

        Button(self, text="Simpan Data",
               command=self.simpan_data).grid(row=4, column=0, columnspan=2, pady=10)

        # Menambahkan Treeview
        self.tree = ttk.Treeview(self, columns=("Merk", "Minuman", "Snack", "Harga"), show="headings")
        self.tree.heading("Merk", text="Merk")
        self.tree.heading("Minuman", text="Minuman")
        self.tree.heading("Snack", text="Snack")
        self.tree.heading("Harga", text="Harga")
        self.tree.grid(row=5, column=0, columnspan=6, pady=10, padx=10)

        # Menambahkan tombol refresh data
        Button(self, text="Refresh Data", command=self.tampilkan_data).grid(row=6, column=0, columnspan=2, pady=10, padx=10)

        # Menambahkan tombol delete data
        Button(self, text="Delete Data", command=self.hapus_data).grid(row=6,
column=1, columnspan=2, pady=10, padx=10)

        # Menambahkan tombol update data
        Button(self, text="Update Data", command=self.update_data).grid(row=6,
column=2, columnspan=2, pady=10, padx=10)
        
        # Menambahkan tombol update data
        Button(self, text="Print Data", command=self.update_data).grid(row=6,
column=3, columnspan=2, pady=10, padx=10)

        self.tampilkan_data()

    def simpan_data(self):
        merk = self.merk_entry.get()
        minuman = self.minuman_entry.get()
        snack = self.snack_entry.get()
        harga = self.harga_entry.get("1.0", END)

        query = "INSERT INTO vending_machine (merk, minuman, snack, harga) VALUES (%s, %s, %s, %s)"
        values = (merk, minuman, snack, harga)

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo("Sukses", "Data berhasil disimpan!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

        self.merk_entry.delete(0, END)
        self.minuman_entry.delete(0, END)
        self.snack_entry.delete(0, END)
        self.harga_entry.delete("1.0", END)

    def tampilkan_data(self):
        # Hapus data pada treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Ambil data dari database
        self.cursor.execute("SELECT * FROM vending_machine")
        data = self.cursor.fetchall()

        # Masukkan data ke treeview
        for row in data:
            self.tree.insert("", "end", values=row)

    def hapus_data(self):
        selected_item = self.tree.selection()
    
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang akan dihapus.")
            return
        confirmation = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?")
        if confirmation:
            for item in selected_item:
                data = self.tree.item(item, 'values')
                merk_to_delete = data[0]

                query = "DELETE FROM vending_machine WHERE merk = %s"
                values = (merk_to_delete,)

                try:
                    self.cursor.execute(query, values)
                    self.db.commit()
                    messagebox.showinfo("Sukses", "Data berhasil dihapus!")
                except Exception as e:
                    messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

            self.tampilkan_data()

    def update_data(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang akan diupdate.")
            return

        # Ambil data terpilih dari treeview
        data = self.tree.item(selected_item[0], 'values')

        # Tampilkan form update dengan data terpilih
        self.merk_entry.insert(0, data[0])
        self.minuman_entry.insert(0, data[1])
        self.snack_entry.insert(0, data[2])
        self.harga_entry.insert("1.0", data[3])

        # Menambahkan tombol update di form
        Button(self, text="Update", command=lambda:
self.proses_update(data[0])).grid(row=4, column=1, columnspan=2, pady=10)

    def proses_update(self, merk_to_update):
        merk = self.merk_entry.get()
        minuman = self.minuman_entry.get()
        snack = self.snack_entry.get()
        harga = self.harga_entry.get("1.0", END)

        query = "UPDATE vending_machine SET merk=%s, minuman=%s, snack=%s, harga=%s WHERE merk=%s"
        values = (merk, minuman, snack, harga, merk_to_update)

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo("Sukses", "Data berhasil diupdate!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

        # Bersihkan form setelah update
        self.merk_entry.delete(0, END)
        self.minuman_entry.delete(0, END)
        self.snack_entry.delete(0, END)
        self.harga_entry.delete("1.0", END)
   
        # Tampilkan kembali data setelah diupdate
        self.tampilkan_data()

if __name__ == "__main__":
    app = Vending_Machine()
    app.mainloop()
