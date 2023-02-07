from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import re
import spacy
nlp = spacy.load('fr_core_news_md')
from tkinter import *


from connecter import connecter

class extraire:
    repertoire = './assets/'

    def commencer():
        """
        Interface graphique donnant le choix du nombre d'annonces par métier à extraire
        """
        def valider(val):
            """
            Ferme l'interface et appels les fonction aspirer_csv et nettoyer_enregistrer
            Parameters
            ----------
            val : str
                nombre textuelle d'annonces à extraire
            """
            root.destroy()
            extraire.aspirer_csv(int(val))
            extraire.nettoyer_enregistrer()
        root = Tk()
        root.title('Compétences Plus')
        titre = Label(text='Vous allez aspirer, nettoyer et stocker un corpus de compétences, pour 30 métiers du domaine informatique, depuis le site Pôle emploi')
        titre.pack(pady=20)
        label = Label(text='Entrez le nombre maximum d\'annonces à extraire par métiers :')
        label.pack(pady=5)
        entry = Entry(width=10)
        entry.pack(pady=5)
        btn = Button(text='Valider', command=lambda:valider(entry.get()))
        btn.pack(pady=20)
        root.mainloop()

    def charger_page_urls():
        """
        Retourne la liste des urls correspondant aux recherches d’annonces de tous les métiers du secteur ‘informatique-telecoms’
        Returns
        -------
        urls_jobs : list
            Liste d'url des recherches d'annonces par métier.
        """
        url = "https://candidat.pole-emploi.fr/offres/emploi/informatique-telecoms/s28"
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get(url)
        page = driver.page_source
        urls_jobs = []
        soup = BeautifulSoup(page, 'html.parser')
        for job in soup.find('div', {'id': 'metiers'}).find_all('a', {'class': 'media'}):
            urls_jobs.append('https://candidat.pole-emploi.fr'+job['href'])
        driver.quit()
        return urls_jobs

    def charger_liste_metiers(url, nb_jobs=1000):
        """
        Charge l’url passé en paramètre et extrait le contenu de la page HTML de n=nb_jobs annonces complète de l’url
        Parameters
        ----------
        url : str
            url de la page web des annonces à extraire.
        nb_jobs : int
            nombre d’annonces à extraire.
        Returns
        -------
        sources : list
            Liste des pages HTML extraites.
        """
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get(url)
        # accept les coockies
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="description"]/a'))).click()
        # recupere le nombre total d'offres chargés
        title = ''
        while len(title) == 0:
            title = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="zoneAfficherListeOffres"]/h1'))).text
        nb_offres_total = int(''.join(filter(str.isdigit, title)))
        if nb_offres_total-1 < nb_jobs:
            nb_jobs = nb_offres_total-1
        # attend le chargement du script perméttant d'ouvrir la fenetre secondaire
        time.sleep(20)
        # génère la fenêtre secondaire
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pagelink"]'))).click()
        sources = []
        for i in range(nb_jobs):
            # L'offre est extraite uniquement si elle est toujours en ligne
            try:
                WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, "labelPopinDetails")))
                sources.append(driver.page_source)
            except TimeoutException:
                pass
            button_next = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="PopinDetails"]/div/div/div/div[1]/div/div[2]/div/button[2]')))
            # Si ce n'est pas la dernière offre à extraire
            if i < nb_jobs-1:
                if button_next.get_attribute('disabled'):
                    driver.execute_script('arguments[0].removeAttribute("disabled")', button_next)
                button_next.click()
        driver.quit()
        return sources

    def decoder_attributs(source):
        """
        Décode le code source HTML passé en paramètre pour récupèrer une liste des attributs titre, identifiant, compétences et savoir-être professionnel
        Parameters
        ----------
        source : str
            code source de l'offre d'emploi à décoder
        Returns
        -------
        data : list
            Liste des attributs.
        """
        soup = BeautifulSoup(source, 'html.parser')
        data = []
        # Récupération le titre du métier
        secteur = soup.find("span", {"class": "withRemoveBtn"}).string
        data.append(secteur)

        # Récupération de l'identifiant de l'offre
        identifiant = ""
        identifiant_container = soup.find("span", {"itemprop": "value"})
        if identifiant_container:
            identifiant = identifiant_container.string
        data.append(identifiant)

        # Récupération des compétences
        competences = soup.find_all("span", {"class": "skill-competence"})
        competences_string = ""
        for i, row in enumerate(competences):
            competence = row.find("span", {"class": "skill-name"}).string
            competences_string += competence
            if i != len(competences) - 1:
                competences_string += '. '
        data.append(competences_string)

        # Récupération du savoir-être professionnels
        savoirs = soup.find_all("span", {"class": "skill-savoir"})
        savoirs_string = ""
        for i, row in enumerate(savoirs):
            savoir = row.find("span", {"class": "skill-name"}).string
            savoirs_string += savoir
            if i != len(savoirs) - 1:
                savoirs_string += '. '
        data.append(savoirs_string)
        return data

    def aspirer_csv(nb_sources):
        """
        Interface indiquant l'extraction en cours et le nombre déjà réalisé
        Parameters
        ----------
        nb_sources : int
            nombre d'annonces à extraire par métier
        """
        def update(nb_file):
            """
            Met à jours le nombre d'extraction déjà réalisé
            Parameters
            ----------
            nb_file : int
                nombre de métier déjà extrait
            """
            label.config(text="Aspiration "+str(nb_file)+"/30")
            root.update()
        def enregister(nb_sources):
            """
            Extrait n=nb_sources annonces pour chacun des 30 métiers les plus recherchés du domaine 'informatique-telecoms'
            Et structure le code HTML extrait en dataframe sous format df_"index_du_métier".csv sauvegarder localement dans un dossier assets
            Parameters
            ----------
            nb_sources : int
                nombre d'annonces à extraire par métier
            """
            sous_repertoire = 'csv'
            # créé le répertoir pour les fichiers csv s'il n'éxiste pas
            if not os.path.exists(extraire.repertoire+sous_repertoire):
                os.makedirs(extraire.repertoire+sous_repertoire)
            # calcul le nombre de fichier csv déjà sauvegarder
            debut = len([nom for nom in os.listdir(extraire.repertoire+sous_repertoire) if nom.endswith('csv')])
            update(debut)
            # liste de 30 urls de recherche d'offre d'emploi automatique par métier
            urls_jobs = extraire.charger_page_urls()
            # reprend la boucle en filtrant les urls déjà extraites
            for i_url, url_job in enumerate(urls_jobs[debut:]):
                sources = extraire.charger_liste_metiers(url_job, nb_sources)
                dataframe = []
                for source in sources:
                    dataframe.append(extraire.decoder_attributs(source))
                df = pd.DataFrame(dataframe, columns=['metier', 'identifiant', 'competences', 'savoir-etre'], dtype="string")
                df.to_csv(extraire.repertoire+sous_repertoire+"/df_"+str(i_url+debut)+".csv", index=False)
                update(i_url+debut+1)
            fichiers_csv = ["".join([extraire.repertoire+sous_repertoire, '/',f]) for f in os.listdir(extraire.repertoire+sous_repertoire) if f.endswith('csv')]
            df = pd.concat(map(pd.read_csv, fichiers_csv), ignore_index=True)
            df.to_csv(extraire.repertoire+"df_complet.csv", index=False)
            root.destroy()
        root = Tk()
        root.geometry('500x200')
        root.title('Compétences Plus')
        titre = Label(text='Aspiration en cours ...')
        titre.pack(pady=20)
        label = Label(text='Aspiration 0/30')
        label.pack(pady=20)
        enregister(nb_sources)
        root.mainloop()

    def normalisation(text):
        """
        Normalisation du texte en supprimant ponctuation, termes parasites puis en attribuant à chaque mot sa forme canonique grâce à la technique de lemmatisation
        Parameters
        ----------
        text : str
            texte initial à normaliser
        Returns
        -------
        sentence_clean : str
            Texte normalisé
        """
        punct_to_avoid = ['(', ')']
        terms_to_avoid = ['etc','h/f', '/', '-']
        sentence_w_punct = ''.join([i for i in text if i not in punct_to_avoid])
        tokenize_sentence = nlp(sentence_w_punct)
        words_lemmatize = (w.lemma_ for w in tokenize_sentence)
        words_w_stopwords = [w for w in words_lemmatize if w not in terms_to_avoid]
        sentence_clean = re.sub(r'\, \.', '.', ' '.join(w for w in words_w_stopwords))
        sentence_clean = re.sub(r'\.+', '.', sentence_clean)
        return sentence_clean

    def nettoyer_data(data):
        """
        Nettoyage et normalisation des ressources en supprimant les données dupliquées et vides puis en regroupant les colonnes 'competences' et 'savoir-etre' avant d'appeler la fonction normalisation
        Parameters
        ----------
        data : dataframe
            ressources initiale sous forme de dataframe
        Returns
        -------
        data : dataframe
            ressources nettoyé sous forme de dataframe
        """
        id_duplicated = data[data[['identifiant']].duplicated()].index
        data.drop(id_duplicated, inplace=True)
        id_emptyRows = data[data['competences'].isna() & data['savoir-etre'].isna()].index
        data.drop(id_emptyRows, inplace=True)
        data.fillna('', inplace=True)
        data['competences'] = data[['competences', 'savoir-etre']].apply('. '.join, axis=1)
        data.drop(['savoir-etre'], axis=1, inplace=True)
        data = data.applymap(str.lower)
        data['competences'] = data['competences'].apply(extraire.normalisation)
        data['competences'] = data['competences'].apply(lambda x: re.sub(r'^\. | \.$', '', x))
        data.reset_index(drop=True, inplace=True)
        return data

    def nettoyer_enregistrer():
        """
        Interface indiquant que le nettoyage est en cours puis appels les fonctions nettoyer_data et enregister_bdd
        """
        root = Tk()
        root.geometry('500x200')
        root.title('Compétences Plus')
        titre = Label(text='Nettoyage en cours ...')
        titre.pack(pady=20)
        root.update()
        data = extraire.nettoyer_data(pd.read_csv(extraire.repertoire+"df_complet.csv", dtype={'metier': "string", 'identifiant': "string", 'competences': "string", 'savoir-etre': "string"}))
        info = connecter.enregister_bdd(data) # enregistre le corpus de compétences en base de données et retourne un message de succes ou d'erreur
        titre.config(text=info)
        root.update()
        root.mainloop()

