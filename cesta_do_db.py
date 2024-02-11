import sqlite3
import os
from tkinter import messagebox

class Cesta_db():
    
    @classmethod
    def cesta_do_sql_db(cls):
        # název adresáře db
        folder_name = "Databaze_pro_zaverecnou_praci"
        # cesta k adresáři
        try:
             cesta = os.path.join(os.getenv("APPDATA"), folder_name)
             # vytvoření adresáře, pokud neexistuje
             if not os.path.exists(cesta):
                os.makedirs(cesta)
        except:
            messagebox.showerror("Nepodařilo se vytvořit složku " + cesta + ", zkontrolujte prosím svá oprávnění.")
        # jméno souboru databáze
        db_filename = 'seznam_pojistencu.db'
        # vytvoření cesty k db souboru
        db_file_cesta = os.path.join(cesta, db_filename)
        return db_file_cesta
    
    @classmethod
    def vytvor_strukturu_db(cls):
        db_cesta = Cesta_db().cesta_do_sql_db()
        conn = sqlite3.connect(db_cesta)
        cur = conn.cursor()
        sql_command =   '''
                        CREATE TABLE IF NOT EXISTS "pojistenci" (
                            id_pojistence INTEGER PRIMARY KEY,
                            jmeno_pojistence TEXT,
                            prijmeni_pojistence TEXT,
                            datum_narozeni TEXT,
                            email_pojistence TEXT,
                            telefon_pojistence TEXT,
                            ulice_pojistence TEXT,
                            cp_pojistence TEXT,
                            mesto_pojistence TEXT,
                            psc_pojistence INTEGER,
                            poj_byt_sjednano TEXT,
                            poj_byt_castka INTEGER,
                            poj_byt_od TEXT,
                            poj_byt_do TEXT,
                            poj_dum_sjednano TEXT,
                            poj_dum_castka INTEGER,
                            poj_dum_od TEXT,
                            poj_dum_do TEXT,
                            poj_auta_sjednano TEXT,
                            poj_auta_castka TEXT,
                            poj_auta_od TEXT,
                            poj_auta_do TEXT,
                            poj_cest_sjednano TEXT,
                            poj_cest_castka INTEGER,
                            poj_cest_od TEXT,
                            poj_cest_do TEXT
                            );
                        '''
        cur.execute(sql_command)
        conn.commit()

        sql_command =   '''
                        CREATE TABLE IF NOT EXISTS "aktual_pojistenec" (
                            id_act_poj INTEGER PRIMARY KEY,
                            id_act_pojistenec INTEGER DEFAULT 0
                            );
                        '''
        cur.execute(sql_command)
        conn.commit()

        sql_command =   '''
                        INSERT INTO "aktual_pojistenec" (id_act_pojistenec) VALUES (0);
                        '''
        cur.execute(sql_command)
        conn.commit()
        conn.close()


if __name__ == "__main__":
     db_file_path = str(Cesta_db().cesta_do_sql_db())
     print(f'{db_file_path= }')
     Cesta_db().vytvor_strukturu_db()


