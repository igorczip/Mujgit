import datetime
import tkinter as tk
from tkinter import messagebox
import pygubu
import os
import pathlib
import sqlite3
from cesta_do_db import Cesta_db
from zalozeni_pojistence_v3_1 import ZalozeniPojistenceV3App
from pridat_pojisteni import PridatPojisteniApp
from odstranit_pojisteni import OdstranitPojisteniApp
from odstranit_pojistence import OdstranitPojistenceApp
from navod_na_pouziti_app import NavodNaPouzitiAppApp

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "list_pojistencu_v3.ui"

class Pojistenec():
    def __init__(self, id_pojistence, jmeno, prijmeni, datum_narozeni, email, telefon, ulice, cislopopisne, mesto, psc, poj_bytu= "nepojištěno", poj_bytu_castka=0, poj_bytu_od="", poj_bytu_do="", poj_dum="nepojištěno", poj_dum_castka=0, poj_dum_od="", poj_dum_do="", poj_auto="nepojištěno", poj_auto_castka=0, poj_auto_od="", poj_auto_do="", poj_cest="nepojištěno", poj_cest_castka=0, poj_cest_od="", poj_cest_do=""):
        self.id_pojistence = id_pojistence
        self.jmeno = jmeno
        self.prijmeni = prijmeni
        self.datum_narozeni = datum_narozeni
        self.email = email
        self.telefon = telefon
        self.ulice = ulice
        self.cislopopisne = cislopopisne
        self.mesto = mesto
        self.psc = psc
        self.poj_bytu = poj_bytu
        self.poj_bytu_castka = poj_bytu_castka
        self.poj_bytu_od = poj_bytu_od
        self.poj_bytu_do = poj_bytu_do
        self.poj_dum = poj_dum
        self.poj_dum_castka = poj_dum_castka
        self.poj_dum_od = poj_dum_od
        self.poj_dum_do = poj_dum_do
        self.poj_auto = poj_auto
        self.poj_auto_castka = poj_auto_castka
        self.poj_auto_od = poj_auto_od
        self.poj_auto_do = poj_auto_do
        self.poj_cest = poj_cest
        self.poj_cest_castka = poj_cest_castka
        self.poj_cest_od = poj_cest_od
        self.poj_cest_do = poj_cest_do
        
 
    def __str__(self):
        return self.jmeno

class Databaze():
    
    def __init__(self, soubor):
        self.soubor = soubor
        self.uzivatele = []

    def pridejUzivatele(self, id_pojistence, jmeno, prijmeni, datum_narozeni, email, telefon, ulice, cislopopisne, mesto, psc, poj_bytu, poj_bytu_castka,   poj_bytu_od, poj_bytu_do, poj_dum, poj_dum_castka, poj_dum_od, poj_dum_do, poj_auto, poj_auto_castka, poj_auto_od, poj_auto_do, poj_cest, poj_cest_castka, poj_cest_od, poj_cest_do):
        jmeno = jmeno.capitalize()
        prijmeni = prijmeni.capitalize()
        u = Pojistenec(id_pojistence, jmeno, prijmeni, datum_narozeni, email, telefon, ulice, cislopopisne, mesto, psc, poj_bytu, poj_bytu_castka, poj_bytu_od, poj_bytu_do, poj_dum, poj_dum_castka, poj_dum_od, poj_dum_do, poj_auto, poj_auto_castka, poj_auto_od, poj_auto_do, poj_cest, poj_cest_castka, poj_cest_od, poj_cest_do)
        self.uzivatele.append(u)

    def vratVsechny(self):
        return self.uzivatele
    
    def nacti_db(self):
        self.uzivatele = []
        seznam_dat_uzivatelu = []
        db_file_cesta = Cesta_db().cesta_do_sql_db()        
        conn = sqlite3.connect(db_file_cesta)
        cur = conn.cursor()
        cur.execute('SELECT * FROM "pojistenci" ORDER BY "prijmeni_pojistence"' )
        data = cur.fetchall()
        conn.commit()
        for d in data:
            seznam_dat_uzivatelu.append(d)   #pridavani radku tabulky "pojistenci"

        for d in range(0,len(seznam_dat_uzivatelu)):
            id_pojistence, jmeno, prijmeni, datum_narozeni, email, telefon, ulice, cislopopisne, mesto, psc, poj_bytu, poj_bytu_castka, poj_bytu_od, poj_bytu_do, poj_dum, poj_dum_castka, poj_dum_od, poj_dum_do, poj_auto, poj_auto_castka, poj_auto_od, poj_auto_do, poj_cest, poj_cest_castka, poj_cest_od, poj_cest_do = seznam_dat_uzivatelu[d]

            self.pridejUzivatele(id_pojistence, jmeno, prijmeni, datum_narozeni, email, telefon, ulice, cislopopisne, mesto, psc, poj_bytu, poj_bytu_castka, poj_bytu_od, poj_bytu_do, poj_dum, poj_dum_castka, poj_dum_od, poj_dum_do, poj_auto, poj_auto_castka, poj_auto_od, poj_auto_do, poj_cest, poj_cest_castka, poj_cest_od, poj_cest_do)

        #conn.close() 

class Aplikace():
    def __init__(self, master):
        self.master = master
        self.db = Databaze(Cesta_db().cesta_do_sql_db)
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: tk.Toplevel = builder.get_object("Frame_1", master)       
        builder.connect_callbacks(self)

    def ziskejUzivatele(self, evt):
        listbox = self.builder.get_object("listUzivatelu")
        i = listbox.curselection()[0] + 1 if len(listbox.curselection()) > 0 else None
        if len(self.db.uzivatele) == 0 or i == None:
            return

        id_pojistence_label = self.builder.get_object('id_pojistenceLabel')
        jmeno_label = self.builder.get_object("jmenoLabel")
        prijmeni_label = self.builder.get_object("prijmeniLabel")
        datum_narozeni_label = self.builder.get_object("datum_narozeniLabel")
        email_label = self.builder.get_object('emailLabel')
        telefon_label = self.builder.get_object('telefonLabel')
        ulice_label = self.builder.get_object('uliceLabel')
        cislopopisne_label = self.builder.get_object('cislopopisneLabel')
        mesto_label = self.builder.get_object('mestoLabel')
        psc_label = self.builder.get_object('pscLabel')
        sjednano_byt_label = self.builder.get_object("lbl_sjednano_byt")
        sjednano_dum_label = self.builder.get_object("lbl_sjednano_dum")
        sjednano_auto_label = self.builder.get_object("lbl_sjednano_auto")
        sjednano_cest_label = self.builder.get_object("lbl_sjednano_cest")
        castka_byt_label = self.builder.get_object("lbl_byt_castka")
        castka_dum_label = self.builder.get_object("lbl_dum_castka")
        castka_auto_label = self.builder.get_object("lbl_auto_castka")
        castka_cest_label = self.builder.get_object("lbl_cest_castka")
        byt_od_label = self.builder.get_object("lbl_byt_od")
        dum_od_label = self.builder.get_object("lbl_dum_od")
        auto_od_label = self.builder.get_object("lbl_auto_od")
        cest_od_label = self.builder.get_object("lbl_cest_od")
        byt_do_label = self.builder.get_object("lbl_byt_do")
        dum_do_label = self.builder.get_object("lbl_dum_do")
        auto_do_label = self.builder.get_object("lbl_auto_do")
        cest_do_label = self.builder.get_object("lbl_cest_do")

        u = self.db.uzivatele[i-1]
        sjednano_byt_label["text"] = ""
        sjednano_dum_label["text"] = ""
        sjednano_auto_label["text"] = ""
        sjednano_cest_label["text"] = ""        
        castka_byt_label["text"] = ""
        castka_dum_label["text"] = ""
        castka_auto_label["text"] = ""
        castka_cest_label["text"] = ""
        byt_od_label["text"] = ""
        dum_od_label["text"] = ""
        auto_od_label["text"] = ""
        cest_od_label["text"] = ""
        byt_do_label["text"] = ""
        dum_do_label["text"] = ""
        auto_do_label["text"] = ""
        cest_do_label["text"] = ""    

        id_pojistence_label["text"] = u.id_pojistence
        jmeno_label["text"] = (u.jmeno).capitalize()
        prijmeni_label["text"] = (u.prijmeni).capitalize()
        datum_narozeni_label["text"] = u.datum_narozeni    #.strftime("%d.%m.%Y")
        email_label["text"] = u.email
        telefon_label["text"] = u.telefon
        ulice_label["text"] = (u.ulice).capitalize()
        cislopopisne_label["text"] = u.cislopopisne
        mesto_label["text"] = (u.mesto).capitalize()
        psc_label["text"] = u.psc
        sjednano_byt_label["text"] = u.poj_bytu
        sjednano_dum_label["text"] = u.poj_dum
        sjednano_auto_label["text"] = u.poj_auto
        sjednano_cest_label["text"] = u.poj_cest
        if u.poj_bytu_castka == None:
            castka_byt_label["text"] = ""
        else:
            castka_byt_label["text"] = (str(u.poj_bytu_castka) + " Kč")
        if u.poj_dum_castka == None:
            u.poj_dum_castka = ""
        else:
            castka_dum_label["text"] = (str(u.poj_dum_castka) + " Kč")
        if u.poj_auto_castka == None:
            u.poj_auto_castka = ""
        else:
            castka_auto_label["text"] = (str(u.poj_auto_castka) + " Kč")
        if u.poj_cest_castka == None:
            u.poj_cest_castka = ""
        else:
            castka_cest_label["text"] = (str(u.poj_cest_castka) + " Kč")
        byt_od_label["text"] = u.poj_bytu_od
        dum_od_label["text"] = u.poj_dum_od
        auto_od_label["text"] = u.poj_auto_od
        cest_od_label["text"] = u.poj_cest_od
        byt_do_label["text"] = u.poj_bytu_do
        dum_do_label["text"] = u.poj_dum_do
        auto_do_label["text"] = u.poj_auto_do
        cest_do_label["text"] = u.poj_cest_do

        db_file_cesta = Cesta_db().cesta_do_sql_db()        
        conn = sqlite3.connect(db_file_cesta)
        cur = conn.cursor()
        sql_command = 'UPDATE aktual_pojistenec SET id_act_pojistenec = ? WHERE "id_act_poj" = 1'
        values = [u.id_pojistence]
        cur.execute(sql_command, values)
        conn.commit()
        conn.close()

    def tlacitkoPrehledClicked(self):
        try:
            self.db.nacti_db()
        except:
            messagebox.showerror("Chyba", "Databázi se nepodařilo načíst, .db soubor zřejmě neexisituje\nkliněte na tlačítko 'Prvotní Vytvoření databáze pojištěnců'")
            return
        listbox = self.builder.get_object("listUzivatelu")
        listbox.delete(0,tk.END)
        for u in self.db.vratVsechny():
            text = ("             " + u.jmeno + " " + u.prijmeni + "    " + u.datum_narozeni)
            listbox.insert(tk.END, text)
    
    def onClickedNovyPojistenec(self):
        ZalozeniPojistenceV3App(master= self.mainwindow)
    
    def onClickedEditByt(self):
        PridatPojisteniApp(master= self.mainwindow)

    def onClickedDeleteByt(self):
        OdstranitPojisteniApp(master= self.mainwindow)

    def onClickedEditDum(self):
        PridatPojisteniApp(master= self.mainwindow)

    def onClickedDeleteDum(self):
        OdstranitPojisteniApp(master= self.mainwindow)

    def onClickedEditAuto(self):
        PridatPojisteniApp(master= self.mainwindow)

    def onClickedDeleteAuto(self):
        OdstranitPojisteniApp(master= self.mainwindow)

    def onClickedEditCestovni(self):
        PridatPojisteniApp(master= self.mainwindow)

    def onClickedDeleteCestovni(self):
        OdstranitPojisteniApp(master= self.mainwindow)
    
    def onClickedDeletePojistenec(self):
        OdstranitPojistenceApp(master= self.mainwindow)

    def onClickedNavod(self):
        NavodNaPouzitiAppApp(master=self.mainwindow)

    def onCallVytvoritDB(self):
        Cesta_db().vytvor_strukturu_db()
        tk.messagebox.showinfo('Message', 'pokud již databáze nebyla vytvořena,\n bylo provedeno její vytvoření\n soubor db = "seznam_pojistencu.db" ')

    def onClickedCloseApp(self):
        self.mainwindow.destroy()


root = tk.Tk()
aplikace = Aplikace(root)
root.mainloop()
