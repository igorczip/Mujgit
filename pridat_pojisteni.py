#!/usr/bin/python3
import pathlib
import tkinter as tk
from tkinter import messagebox
import pygubu
import sqlite3
from datetime import datetime
from cesta_do_db import Cesta_db

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "pridat_pojisteni.ui"

class Pojisteni():
    def __init__(self, castka, platnost_od, platnost_do):
        self._byt = "byt"
        self._dum = "dum"
        self._auto = "auto"
        self._cestovni = "cestovni"
        self._castka_pojistky = castka
        self._platnost_od = platnost_od
        self._platnost_do = platnost_do
        self.castka_platna = False
        self.datum_od_platny = False
        self.datum_do_platny = False
    @property
    def castka_pojistky(self):
        return self._castka_pojistky
    @castka_pojistky.setter
    def castka_pojistky(self, hodnota):
        try:
            hodnota = int(hodnota)
        except:
            hodnota = None
        if hodnota is None or not isinstance(hodnota, int) or hodnota <= 0:
            #zprava o kontrole v částky
            tk.messagebox.showinfo('Message', 'Vložená částka je menší nebo rovna nule\nnebo není číselná hodnota\nOpravte částku a zopakujte vložení.')
        else:
            self._castka_pojistky = hodnota
            self.castka_platna = True
            
    @property
    def platnost_od(self):
        return self._platnost_od
    @platnost_od.setter
    def platnost_od(self, hodnota):
        print('kontrola datumu do')
        print(f'{hodnota =}')
        try:
            if hodnota is not None:
                self._platnost_od = datetime.strptime(hodnota, '%d.%m.%Y')
                #self._platnost_od = hodnota
                print(f'vlozeno {self._platnost_od= }')
                self.datum_od_platny = True
            else:
                print('chyba datumu od')
        except:
            tk.messagebox.showerror('Message', 'vložený "datum_od" není platný datum\nZadejte platný "datum_od"')
    
    @property
    def platnost_do(self):
        return self._platnost_do
    @platnost_do.setter
    def platnost_do(self, hodnota):
        print('kontrola datumu do')
        print(f'{hodnota =}')
        try:
            if hodnota is not None:
                self._platnost_do = datetime.strptime(hodnota, '%d.%m.%Y')
                #self._platnost_do = hodnota
                print(f'vlozeno {self._platnost_do= }')
                self.datum_do_platny = True
            else:
                print('chyba datumu do')
        except:
                tk.messagebox.showerror('Message', 'vložený "datum_do" není platný datum\nZadejte platný "datum_do"')


class PridatPojisteniApp:
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


        #Radiobutton definice
        self.rb_byt = builder.get_object("rb_byt")
        self.rb_dum = builder.get_object("rb_dum")
        self.rb_auto = builder.get_object("rb_auto")
        self.rb_cestovni = builder.get_object("rb_cestovni")
        self.rb_byt.invoke()    # invoke metoda = počáteční nastavení hodnoty buttonu na TRUE a zviditelnění v menu nabídce jako "on" při prvním spuštění okna
        #self.tk_volba = builder.get_variable("poj_volba")  #vložení tk atributu variable = tk_volba do atributu self.poj_volba,  tk naznačuje,že se jedná o objekt kt ne python

        #navázání na widget entry data
        
        #self.entry_castka = builder.get_object("entry_castka_pojistky")
        #self.entry_pl_od = builder.get_object("entr_platnost_od")
        #self.entry_pl_do = builder.get_object("entr_platnost_do")
        self.entry_id_pojistence = id_pojistenec

    def on_Clicked_vlozit_data_pojisteni(self):
        pojisteni = Pojisteni(0,"","")
        id_pojistence = self.entry_id_pojistence[0]

        self.entry_castka = self.builder.get_object("entry_castka_pojistky").get()
        self.entry_pl_od = self.builder.get_object("entr_platnost_od").get()
        self.entry_pl_do = self.builder.get_object("entr_platnost_do").get()
        #print(f'{id_pojistence= }')
        castka = self.entry_castka
        pl_od = str(self.entry_pl_od)
        pl_do = str(self.entry_pl_do)
        
        pojisteni.castka_pojistky = castka
        pojisteni.platnost_od = pl_od
        pojisteni.platnost_do = pl_do

        if not pojisteni.castka_platna or not pojisteni.datum_od_platny or not pojisteni.datum_do_platny:
            return

        
        db_file_cesta = Cesta_db().cesta_do_sql_db()
        conn = sqlite3.connect(db_file_cesta)
        cur = conn.cursor()

        if self.rb_byt.instate(["selected"]):
            sjednano = "sjednáno"
            sql_command = 'UPDATE pojistenci SET poj_byt_sjednano = ?, poj_byt_castka = ?, poj_byt_od = ?, poj_byt_do = ? WHERE "id_pojistence" = ?'
            values = (sjednano, castka, pl_od, pl_do, id_pojistence)
            cur.execute(sql_command, values)
            conn.commit()
            
        elif self.rb_dum.instate(["selected"]):
            sjednano = "sjednáno"
            sql_command = 'UPDATE pojistenci SET poj_dum_sjednano = ?, poj_dum_castka = ?, poj_dum_od = ?, poj_dum_do = ? WHERE "id_pojistence" = ?'            
            values = (sjednano, castka, pl_od, pl_do, id_pojistence)
            cur.execute(sql_command, values)
            conn.commit()
        
        elif self.rb_auto.instate(["selected"]):
            sjednano = "sjednáno"
            sql_command = 'UPDATE pojistenci SET poj_auta_sjednano = ?, poj_auta_castka = ?, poj_auta_od = ?, poj_auta_do = ? WHERE "id_pojistence" = ?'
            values = (sjednano, castka, pl_od, pl_do, id_pojistence)
            cur.execute(sql_command, values)
            conn.commit()

        elif self.rb_cestovni.instate(["selected"]):
            sjednano = "sjednáno"
            sql_command = 'UPDATE pojistenci SET poj_cest_sjednano = ?, poj_cest_castka = ?, poj_cest_od = ?, poj_cest_do = ? WHERE "id_pojistence" = ?'
            values = (sjednano, castka, pl_od, pl_do, id_pojistence)
            cur.execute(sql_command, values)
            conn.commit()
        else:
            print("pojisteni neni nezvoleno")
        
        tk.messagebox.showinfo('Messsage', 'Data o pojištění byla aktualizována/ založena')

        self.mainwindow.destroy()
    
    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = PridatPojisteniApp()
    app.run()
