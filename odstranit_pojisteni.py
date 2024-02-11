#!/usr/bin/python3
import pathlib
import tkinter as tk
from tkinter import messagebox
import pygubu
import sqlite3
from datetime import datetime
from cesta_do_db import Cesta_db

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "odstranit_pojisteni.ui"


class OdstranitPojisteniApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: tk.Toplevel = builder.get_object("toplevel1", master)

        self.poj_volba: tk.StringVar = None
        builder.import_variables(self)
        builder.connect_callbacks(self)

        #získání jména, příjmení, data narození příslušného pojištěnce z tabulky "pojistenci" na základě jeho primárního klíče uloženého v tabulce "aktual_pojistenec", primární klíč příslušného aktuálního pojištěnce posílá do tabulky "aktual_pojistenec" aplikace "list_pojistencu_v3" 
        self.db_file_cesta = Cesta_db().cesta_do_sql_db()
        conn = sqlite3.connect(self.db_file_cesta)
        cur = conn.cursor()
        cur.execute('SELECT "id_act_pojistenec" FROM aktual_pojistenec WHERE "id_act_poj" = 1')
        id_pojistenec = cur.fetchall()
        id_pojistenec = id_pojistenec[0]
        print(f'{id_pojistenec=}, {type(id_pojistenec)=}')
        sql_command = ('SELECT "jmeno_pojistence", "prijmeni_pojistence", "datum_narozeni" FROM "pojistenci" WHERE "id_pojistence" = ?')
        cur.execute(sql_command, (id_pojistenec))
        data = cur.fetchall()
        jmeno = data[0][0]
        prijmeni = data[0][1]
        dat_narozeni = data[0][2]
        print(f'{jmeno= }, {prijmeni= }, {dat_narozeni= }')
        conn.commit()

        #vložení údajů o pojištěnci do widgetu
        jmeno_label = self.builder.get_object("lbl_jmeno")
        prijmeni_label = self.builder.get_object("lbl_prijmeni")
        dat_narozeni_label = self.builder.get_object("lbl_datum_narozeni")
        id_pojistence_label = self.builder.get_object("lbl_id_pojistence")

        jmeno_label["text"] = (jmeno).capitalize()
        prijmeni_label["text"] = prijmeni.capitalize()
        dat_narozeni_label["text"] = dat_narozeni
        id_pojistence_label["text"] = id_pojistenec


        #Radiobutton definice
        self.rb_byt = builder.get_object("rb_byt")
        self.rb_dum = builder.get_object("rb_dum")
        self.rb_auto = builder.get_object("rb_auto")
        self.rb_cestovni = builder.get_object("rb_cestovni")
        self.rb_byt.invoke()    # invoke metoda = počáteční nastavení hodnoty buttonu na TRUE a zviditelnění v menu nabídce jako "on" při prvním spuštění okna
        #self.tk_volba = builder.get_variable("poj_volba")  #vložení tk atributu variable = tk_volba do atributu self.poj_volba,  tk naznačuje,že se jedná o objekt kt ne python
        self.entry_id_pojistence = id_pojistenec

       #odstranění nebo aktuakizace dat o pojištění 
    def on_Clicked_odstranit_data_pojisteni(self):
        id_pojistence = self.entry_id_pojistence[0]
        print(f'{id_pojistence= }')
        db_file_cesta = Cesta_db().cesta_do_sql_db()
        conn = sqlite3.connect(db_file_cesta)
        cur = conn.cursor()
        sjednano = "nesjednáno"
        castka = ''
        pl_od = ''
        pl_do = ''
        values = (sjednano, castka, pl_od, pl_do, id_pojistence)
        
        if self.rb_byt.instate(["selected"]):            
            sql_command = 'UPDATE pojistenci SET poj_byt_sjednano = ?, poj_byt_castka = ?, poj_byt_od = ?, poj_byt_do = ? WHERE "id_pojistence" = ?'
            cur.execute(sql_command, values)
            conn.commit()
            tk.messagebox.showinfo('Message', "požadovaná operace byla provedena")
            
        elif self.rb_dum.instate(["selected"]):            
            sql_command = 'UPDATE pojistenci SET poj_dum_sjednano = ?, poj_dum_castka = ?, poj_dum_od = ?, poj_dum_do = ? WHERE "id_pojistence" = ?'
            cur.execute(sql_command, values)
            conn.commit()
            tk.messagebox.showinfo('Message', "požadovaná operace byla provedena")
        
        elif self.rb_auto.instate(["selected"]):
            sql_command = 'UPDATE pojistenci SET poj_auta_sjednano = ?, poj_auta_castka = ?, poj_auta_od = ?, poj_auta_do = ? WHERE "id_pojistence" = ?'
            cur.execute(sql_command, values)
            conn.commit()
            tk.messagebox.showinfo('Message', "požadovaná operace byla provedena")

        elif self.rb_cestovni.instate(["selected"]):
            sql_command = 'UPDATE pojistenci SET poj_cest_sjednano = ?, poj_cest_castka = ?, poj_cest_od = ?, poj_cest_do = ? WHERE "id_pojistence" = ?'
            cur.execute(sql_command, values)
            conn.commit()
            tk.messagebox.showinfo('Message', "požadovaná operace byla provedena")
        else:
            print("pojisteni neni zvoleno")
            tk.messagebox.showinfo('Message', "neco se pokazilo ....")

    def onClickedZpet(self):
        self.mainwindow.destroy()

    def run(self):
        self.mainwindow.mainloop()

if __name__ == "__main__":
    app = OdstranitPojisteniApp()
    app.run()
