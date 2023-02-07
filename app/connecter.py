import pandas as pd
import psycopg2
import json
import csv
from tkinter import *


class connecter:
    repertoire = './assets/'

    def connecter_bdd():
        """
        Se connecte à la base postgreSql
        Returns
        -------
        conn : connection
            connexion psycopg2
        """
        # charge les informations de configuration depuis le fichier config.json
        with open('config.json') as mon_fichier:
            config = json.load(mon_fichier)
        conn = psycopg2.connect(
            user = config['user'],
            password = config['password'],
            host = config['host'],
            port = config['port'],
            database = config['database'])
        return conn

    def enregister_bdd(data):
        """
        Enregistre les données passés en paramettre dans une table 'competences'
        Si la connexion réussi : retourne un message de succes
        Si la connexion échoue : retourne un message d'erreur
        Parameters
        -------
        data : dataframe
            corpus de compétences sous format dataframe
        Returns
        -------
        m : str
            information succes ou erreur
        """
        try:
            conn = connecter.connecter_bdd()
            cur = conn.cursor()
            # valide les modifications automatiquement
            conn.autocommit = True
            # créé la table 'compétences' si celle si n'existe pas
            cur.execute('''CREATE TABLE IF NOT EXISTS competences(
                identifiant TEXT PRIMARY KEY NOT NULL,
                metier TEXT NOT NULL,
                competences TEXT NOT NULL,
                date TIMESTAMP without time zone DEFAULT now()
                );''')

            # Pour chacune des ressources de 'data' insert ou met à jours une ligne avec les données correspondantes dans la table 'compétences'
            for index, row in data.iterrows():
                cur.execute('''INSERT INTO competences(identifiant, metier, competences)
                    VALUES(%s,%s,%s)
                    ON CONFLICT ON CONSTRAINT competences_pkey
                    DO UPDATE SET metier = EXCLUDED.metier, competences = EXCLUDED.competences, "date" = EXCLUDED.date;''',
                    (row.identifiant, row.metier, row.competences))
            # ferme la connexion
            cur.close()
            conn.close()
            return 'Succes Enregistrement'
        except (Exception, psycopg2.Error) as error :
            m = 'Erreur Nettoyage/Enregistrement\n'+str(error)
            return m

    def sauvegarder():
        """
        Interface graphique indiquant que la sauvegarde est en cours ou bien terminé avec succes ou echec
        """
        root = Tk()
        root.geometry('500x200')
        root.title('Compétences Plus')
        titre = Label(text='Sauvergarde en cours ...')
        titre.pack(pady=20)
        info = connecter.sauvegarder_bdd_csv()
        if info == 'Succes Enregistrement':
            titre.config(text="Sauvergarde Terminé")
        else:
            titre.config(text=info)
        root.update()
        root.mainloop()

    def sauvegarder_bdd_csv():
        """
        Charge la base de donnée pour enregistrer les données dans un fichier csv
        Si la connexion réussi : retourne un message de succes
        Si la connexion échoue : retourne un message d'erreur
        Returns
        -------
        m : str
            information succes ou erreur
        """
        try:
            conn = connecter.connecter_bdd()
            cur = conn.cursor()
            cur.execute('''SELECT identifiant, metier, competences FROM competences
                ORDER BY metier ASC, "date" DESC;''')
            header = [[row[0] for row in cur.description]]
            with open(connecter.repertoire+'bdd_competences.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(header)
                writer.writerows(cur.fetchall())
            # ferme la connexion
            cur.close()
            conn.close()
            return 'Succes Enregistrement'
        except (Exception, psycopg2.Error) as error :
            m = 'Erreur Sauvergarde\n'+str(error)
            return m

    def charger_bdd_ou_csv():
        """
        Charge la base de donnée ou le fichier local csv
        Si la connexion réussi : retourne un message de succes
        Si la connexion échoue : retourne un message d'erreur
        Returns
        -------
        df : dataframe
            dataframe du corpus de competences
        """
        try:
            conn = connecter.connecter_bdd()
            cur = conn.cursor()
            cur.execute('''SELECT identifiant, metier, competences, "date" FROM competences
                ORDER BY metier ASC, "date" DESC;''')
            columns = [row[0] for row in cur.description]
            data = cur.fetchall()
            df = pd.DataFrame(data=data, columns=columns)
            # ferme la connexion
            cur.close()
            conn.close()
            return df
        except (Exception, psycopg2.Error) as error :
            df = pd.read_csv(connecter.repertoire+"bdd_competences.csv", dtype={'metier': "string", 'identifiant': "string", 'competences': "string", 'date': "datetime64[ns]"})
            return df
