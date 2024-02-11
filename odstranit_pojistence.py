#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from tkinter import messagebox
import pygubu
import sqlite3
from cesta_do_db import Cesta_db

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "odstranit_pojistence.ui"


class OdstranitPojistenceApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        self.builder.add_resource_path(PROJECT_PATH)
        self.builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: tk.Toplevel = builder.get_object("toplevel1", master)
        self.builder.connect_callbacks(self)

    #získání jména, příjmení, data narození příslušného pojištěnce z tabulky "pojistenci" na základě jeho primárního klíče uloženého v tabulce "aktual_pojistenec", primární klíč příslušného aktuálního pojištěnce posílá do tabulky "aktual_pojistenec" aplikace "list_pojistencu_v3" 
        self.db_file_cesta = Cesta_db().cesta_do_sql_db()
        conn = sqlite3.connect(self.db_file_cesta)
        cur = conn.cursor()
        cur.execute('SELECT "id_act_pojistenec" FROM aktual_pojistenec WHERE "id_act_poj" = 1')
        id_pojistenec = cur.fetchall()
        id_pojistenec = id_pojistenec[0]
        #print(f'{id_pojistenec=}, {type(id_pojistenec)=}')
        sql_command = ('SELECT "jmeno_pojistence", "prijmeni_pojistence", "datum_narozeni" FROM "pojistenci" WHERE "id_pojistence" = ?')
        cur.execute(sql_command, (id_pojistenec))
        data = cur.fetchall()
        jmeno = data[0][0]
        prijmeni = data[0][1]
        dat_narozeni = data[0][2]
        #print(f'{jmeno= }, {prijmeni= }, {dat_narozeni= }')
        conn.commit()

        jmeno_label = self.builder.get_object("lbl_jmeno")
        prijmeni_label = self.builder.get_object("lbl_prijmeni")
        dat_narozeni_label = self.builder.get_object("lbl_datum_narozeni")
        id_pojistence_label = self.builder.get_object("lbl_id_pojistence")

        jmeno_label["text"] = (jmeno).capitalize()
        prijmeni_label["text"] = prijmeni.capitalize()
        dat_narozeni_label["text"] = dat_narozeni
        id_pojistence_label["text"] = id_pojistenec

        self.entry_id_pojistence = id_pojistenec
        print(f'zde je hodnota {self.entry_id_pojistence=}')

    def on_Clicked_odstarnit_pojistence(self):
        id_pojistence = self.entry_id_pojistence
        print(f'tady jsem {id_pojistence= }, {type(id_pojistence)}')
        values = []
        values = (values.append(id_pojistence))
        print(f'{values= }')
        db_file_cesta = Cesta_db().cesta_do_sql_db()
        conn = sqlite3.connect(db_file_cesta)
        cur = conn.cursor()
        sql_command = ('DELETE FROM "pojistenci" WHERE "id_pojistence"= ?')
        cur.execute(sql_command, (id_pojistence))
        conn.commit()
        tk.messagebox.showinfo('Message', "Pojištěnec byl odstraněn ze seznamu")
        self.mainwindow.destroy()

    def onClickedZpet(self):
        self.mainwindow.destroy()

    def run(self):
        self.mainwindow.mainloop()




if __name__ == "__main__":
    app = OdstranitPojistenceApp()
    app.run()
