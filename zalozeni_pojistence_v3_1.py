#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from tkinter import messagebox
import sqlite3
import os
from cesta_do_db import Cesta_db
from datetime import datetime

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "zalozeni_pojistence_v3.ui"
#print(f'{PROJECT_PATH =}')

class DataCheck():
    def __init__(self, jmeno, prijmeni, datum_narozeni, email, telefon, ulice, cislo_popisne, mesto, psc):
        self._jmeno = jmeno
        self._prijmeni = prijmeni
        self._datum_narozeni = datum_narozeni
        self._email = email
        self._telefon = telefon
        self._ulice = ulice
        self._cislo_popisne = cislo_popisne
        self._mesto = mesto
        self._psc = psc
        self.znak_kontrola = True
        self.cislo_kontrola = True
        self.znaky = ('!','@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '/', '-', '=', ':', '<', '>','§', '\\', '?')
        self.znaky_mail = ('!', '#', '$', '%', '^', '&', '*', '(', ')', '+', '/', '-', '=', ':', '<', '>','§', '\\', '?')
        self.cisla = ("1","2","3","4","5","6","7","8","9","0")

    def check_znaku(self, hodnota):
        for znak in hodnota:
            if znak in self.znaky:
                self.znak_kontrola = False
                break
        return self.znak_kontrola
    
    def check_cislo(self, hodnota):
        if hodnota.startswith(self.cisla):
            self.znak_kontrola = False
        return self.znak_kontrola

    @property
    def jmeno(self):
        return self._jmeno
    
    @jmeno.setter
    def jmeno(self, hodnota):
        k1 = self.check_znaku(hodnota)
        k2 = self.check_cislo(hodnota)
        if hodnota is None or not k1 or not k2:
            tk.messagebox.showerror('Message', 'Vložené jméno neodpovídá jmenným zvyklostem\nOpravte jméno a zopakujte vložení.')
            self.znak_kontrola = False
        else:
            self._jmeno = hodnota.strip().lower().capitalize()
                
    @property
    def prijmeni(self):
        return self._prijmeni
    
    @prijmeni.setter
    def prijmeni(self, hodnota):
        k1 = self.check_znaku(hodnota)
        k2 = self.check_cislo(hodnota)
        if hodnota is None or not k1 or not k2:
            tk.messagebox.showerror('Message', 'Vložené příjmení neodpovídá jmenným zvyklostem\nOpravte příjmení a zopakujte vložení.')
            self.znak_kontrola = False 
        else:
            self._prijmeni = hodnota.strip().lower().capitalize()

    @property
    def datum_narozeni(self):
        return self._datum_narozeni
    
    @datum_narozeni.setter
    def datum_narozeni(self, hodnota):
        #print('kontrola datumu')
        #print(f'{hodnota =}')
        try:
            if hodnota is not None:
                test = str(datetime.strptime(hodnota, '%d.%m.%Y'))
                self._datum_narozeni = hodnota
                print(f'vlozeno {self._datum_narozeni= }')

            else:
                print('chyba v datumu')
                self._narozeni_kontrola = False
        except:
                tk.messagebox.showerror('Message', 'vložený "datum" není platný datum\nZadejte platný "datum"')
                self.znak_kontrola = False


    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, hodnota):
        if hodnota is not None:
            for znak in hodnota:
                if znak in self.znaky_mail:
                    self.znak_kontrola = False
                    tk.messagebox.showerror('Message', 'Vložený mail neodpovídá zvyklostem\nOpravte mail a zopakujte vložení.')
                    break
            if hodnota.startswith(self.znaky) or hodnota.count("@") >= 2:
                tk.messagebox.showerror('Message', 'Vložený mail neodpovídá zvyklostem\nOpravte mail a zopakujte vložení.')
                self.znak_kontrola = False
            else:
                self._email = hodnota.strip().lower()
        else:
            tk.messagebox.showerror('Message', 'Vložený mail neodpovídá zvyklostem\nOpravte mail a zopakujte vložení.')
            self.znak_kontrola = False

    @property
    def telefon(self):
        return self._telefon
    
    @telefon.setter
    def telefon(self, hodnota):
        self._telefon = hodnota.strip()
        if hodnota is None or not hodnota.isdigit() or len(hodnota) != 9:
            tk.messagebox.showerror('Message', 'Vložené tel.číslo neodpovídá tel.číslu\nOpravte číslo telefonu a zopakujte vložení.')
            self.znak_kontrola = False
        else:
            self._telefon = hodnota.strip()

    @property
    def ulice(self):
        return self._ulice
    
    @ulice.setter
    def ulice(self, hodnota):
        self._ulice = hodnota.strip().capitalize()
        k1 = self.check_znaku(hodnota)
        if hodnota is None or not k1:
            tk.messagebox.showerror('Message', 'Vložený název ulice neodpovídá jmenným zvyklostem\nOpravte název ulice a zopakujte vložení.')
            self.znak_kontrola = False
        else:
            self._ulice = hodnota.strip().capitalize()

    @property
    def cislo_popisne(self):
        return self._cislo_popisne
    
    @cislo_popisne.setter
    def cislo_popisne(self, hodnota):
        if hodnota is None or not hodnota.isdigit():
            tk.messagebox.showerror('Message', 'Vložené číslo popisné číslo neodpovídá číslu\nOpravte číslo popisné a zopakujte vložení.')
            self.znak_kontrola = False
        else:
            self._cislo_popisne = hodnota.strip()

    @property
    def mesto(self):
        return self._mesto
    
    @mesto.setter
    def mesto(self, hodnota):
        self.check_znaku(hodnota)
        if hodnota is None or not self.znak_kontrola:
            tk.messagebox.showerror('Message', 'Vložené jméno města neodpovídá jmenným zvyklostem\nOpravte jméno města a zopakujte vložení.')
            self.znak_kontrola = False
        else:
            h = hodnota.strip().split()
            h[0] = h[0].capitalize()
            if len(h) == 2: 
                h[1] = h[1].capitalize()
            elif len(h) == 3:
                    h[1] = h[1].lower()
                    h[2] = h[2].capitalize()
            hodnota = " ".join(h)
            self._mesto = hodnota

    @property
    def psc(self):
        return self._psc
    
    @psc.setter
    def psc(self, hodnota):
        def psc_uprava(hodnota):
            v = ""
            hodnota= hodnota.strip()
            h = list(hodnota)
            for dig in h:
                if dig.isdigit():
                    v = v + dig
            return v
        
        if hodnota is None:
            tk.messagebox.showerror('Message', 'Zadejte psč\na zopakujte vložení.')
            self.znak_kontrola = False
        else:
            psc_upr = psc_uprava(hodnota)
            if len(psc_upr) != 5:
                tk.messagebox.showerror('Message', 'Vložené psč je nesprávné \nOpravte psč a zopakujte vložení.')
                self.znak_kontrola = False
            else:
                self._psc = psc_upr
              

# třída pro instanci, která ve svých vlastnostech bude napojena na formulář "zalozeni_pojistence_v3.ui"
# a uloží vtupní data z formuláře do databáze
class ZalozeniPojistenceV3App:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        self.builder.add_resource_path(PROJECT_PATH)
        self.builder.add_from_file(PROJECT_UI)
        # Main widget 
        self.mainwindow: tk.Toplevel = builder.get_object(
            "zalozeni_window", master)
        self.builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    # Button - metoda na obdržení vtupních dat po stisku tlačítka "Uložit data pojištěnce"
    def onClickedUlozitPojistence(self):
        datacheck = DataCheck("","","","","","","","","")
        self.entry_jmeno = self.builder.get_object("entr_jm_pojistenec").get()
        #print(f'{self.entry_jmeno= }')
        self.entry_prijmeni = self.builder.get_object("entr_prijmeni_pojistenec").get()
        #print(f'{self.entry_prijmeni= }')
        self.entry_datum_narozeni = self.builder.get_object("entr_datum_narozeni").get()
        #print(f'{self.entry_datum_narozeni= }')
        self.entry_email = self.builder.get_object('entr_email_pojistenec').get()
        #print(f'{self.entry_email= }')
        self.entry_telefon = self.builder.get_object('entr_tel_pojistenec').get()
        #print(f'{self.entry_telefon= }')
        self.entry_ulice = self.builder.get_object('entr_ulice').get()
        #print(f'{self.entry_ulice= }')
        self.entry_cislo_popisne = self.builder.get_object('entr_cislo_popisne').get()
        #print(f'{self.entry_cislo_popisne= }')
        self.entry_mesto = self.builder.get_object('entr_mesto').get()
        #print(f'{self.entry_mesto= }')
        self.entry_psc = self.builder.get_object('entr_psc').get()
        #print(f'{self.entry_psc= }')

        datacheck.jmeno = self.entry_jmeno
        datacheck.prijmeni = self.entry_prijmeni
        datacheck.datum_narozeni = self.entry_datum_narozeni
        datacheck.email = self.entry_email
        datacheck.telefon = self.entry_telefon
        datacheck.ulice = self.entry_ulice
        datacheck.cislo_popisne = self.entry_cislo_popisne
        datacheck.mesto = self.entry_mesto
        datacheck.psc = self.entry_psc

        #print(f'{datacheck.znak_kontrola= }')
        if not datacheck.znak_kontrola:
            return
        
        # Název nového adresáře
        folder_name = "Databaze_pro_zaverecnou_praci"
        # Vytvořte cestu k novému adresáři
        path = os.path.join(os.getenv("APPDATA"), folder_name)
        # Vytvořte nový adresář, pokud ještě neexistuje
        if not os.path.exists(path):
            os.makedirs(path)

        # Název souboru databáze
        db_filename = 'seznam_pojistencu.db'
        # Vytvoří cestu k souboru vytvořením cesty k novému adresáři a připojením názvu souboru
        db_file_path = os.path.join(path, db_filename)
        conn = sqlite3.connect(db_file_path)    # vytvoření konektivity na sql db
        cur = conn.cursor()    # kurzor

        # vložení dat do db
        sql_command = "INSERT INTO pojistenci (jmeno_pojistence, prijmeni_pojistence, datum_narozeni, email_pojistence, telefon_pojistence, ulice_pojistence, cp_pojistence, mesto_pojistence, psc_pojistence) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        values =  (datacheck.jmeno, datacheck.prijmeni, datacheck.datum_narozeni, datacheck._email, datacheck._telefon, datacheck._ulice, datacheck._cislo_popisne, datacheck._mesto, datacheck._psc)
        cur.execute(sql_command, values)    # příkaz k vložení
        conn.commit()     # potvzení vložení
        conn.close()      # zavření db
       

        # zpráva o uložení dat
        tk.messagebox.showinfo('Message', 'data o pojistenci byla zkontrolovana a ulozena do DB')

    # metoda k zavření okna
    def onClickedDestrWindowNewInsured(self):
        self.mainwindow.destroy()


if __name__ == "__main__":
    app = ZalozeniPojistenceV3App()
    app.run()
