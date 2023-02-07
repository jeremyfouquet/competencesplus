import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from tkinter import *
from tkinter import ttk
from connecter import connecter

class analyser:

    def commencer():
        corpus_e = analyser.equilibre_data(connecter.charger_bdd_ou_csv())

        def choix(val):
            root.destroy()
            analyser.visualiser_resultat(val, corpus_e)

        root = Tk()
        root.title('Compétences Plus')
        label = Label(text='Vous allez voir les compétences les plus recherchées par les recruteurs ainsi que les métiers possédants le plus de compétences en communs pour votre métier')
        label.pack(pady=20)
        label1 = Label(text='Choissez votre métier dans la liste')
        label1.pack(pady=5)
        listeCombo = ttk.Combobox(values=list(analyser.grp_metier(corpus_e).index.values), state='readonly', width=50)
        listeCombo.current(0)
        listeCombo.pack()
        btn1 = Button(text='valider', command=lambda:choix(listeCombo.get()))
        btn1.pack(pady=20)
        root.mainloop()

    def grp_metier(data):
        """
        retourne un dataframe en 2 colonnes (metier, nb_ligne)
        Params
        -------
        data : dataframe
            dataframe du corpus de compétences en 4 colonnes (identifiant, metier, competences, date)
        Return
        -------
        result : dataframe
            dataframe du corpus de compétences groupé par metier et avec une colonne du nombre de ligne par metier
        """
        result = data.groupby('metier')['identifiant'].nunique().sort_values(ascending=False).reset_index(name='nb_ligne').set_index('metier')
        return result

    def mediane(data, colname, f=False):
        """
        retourne la mediane d'une série de nombre
        Params
        -------
        data : dataframe
            dataframe du corpus de compétences groupé par metier
        colname : str
            nom de la colonne dont est calculé la mediane
        f : boolean
            False par defaut, si True retourne une valeur float en resultat
        Return
        -------
        m : integer|float
            medianne de la colonne colname de data
        """
        m = data[colname].median()
        if not f:
            m = int(m)
        return m

    def equilibre_data(data):
        """
        Equilibre les données du corpus passé en paramettre en supprimant les métiers non représentatif et en gardant uniquement un nombre n de données >= à la mediane
        Params
        -------
        data : dataframe
            dataframe du corpus de compétences en 4 colonnes (identifiant, metier, competences, date)
        """
        result = analyser.grp_metier(data)
        median = analyser.mediane(result, 'nb_ligne')
        result = result[result['nb_ligne'] >= median]
        median = analyser.mediane(result, 'nb_ligne')
        # Supprime tout les metiers dont le nombre de ligne est inferieur à la valeur de 'median'
        new_data = data[data['metier'].isin(result.index.values) == True]
        # Garde un nombre max de ligne n=median par metier
        new_data = new_data.groupby('metier', as_index=False).apply(lambda x: x.iloc[:median]).reset_index(drop=True)
        return new_data

    def competences_occurences(data, nb=15, metier=None):
        """
        Affiche les n=nb compétences les plus fréquentes ainsi que leurs nombre de répétition par metier=metier
        Params
        -------
        data : dataframe
            dataframe du corpus de compétences en 4 colonnes (identifiant, metier, competences, date)
        nb : int
            nombre de compétences à afficher
        metier : str
            titre du metier pour lequel nous souhaitons visualiser la fréquences des compétences
        Return
        -------
        result : dataframe
            dataframe des fréquences des n=nb compétences les plus présente dans le corpus
        """
        text = ''
        if metier:
            text = '.'.join(data[data['metier'] == metier]['competences'])
        else:
            text = '.'.join(data['competences'])
        list_comp = list(dict.fromkeys([s.strip() for s in text.split('.') if not len(s.strip()) == 0]))
        # création d'un dataframe avec une liste d'index correspondant aux compétences
        result = pd.DataFrame(index=list_comp)
        # créé une colonne avec le nombre de fois où l'index est trouvé dans le texte
        result['nb_occ'] = result.index.to_series().apply(lambda x: text.count(x))
        result.sort_values(by='nb_occ', ascending=False, inplace=True)
        return result[:nb]

    def metier_competences(data):
        """
        Créé et retourne un dataframe en regroupant l'ensemble des compétence par metier
        Params
        -------
        data : dataframe
            dataframe du corpus de compétences en 4 colonnes (identifiant, metier, competences, date)
        Return
        -------
        result : dataframe
            dataframe groupé par metier en 2 colonnes (metier, competences)
        """
        result = data.copy()
        result['full_comp'] = result.groupby(['metier'])['competences'].transform(lambda x : ' . '.join(x))
        result = result[['metier', 'full_comp']].rename({'full_comp': 'competences'}, axis=1)
        result.drop_duplicates(inplace=True)
        result.reset_index(drop=True, inplace=True)
        return result

    def tf_idf(data, metier):
        """
        Convertie la colonne 'competences' à l'aide de TfidfVectorizer au format TF-IDF (fréquence de terme - fréquence de document inverse) avec la distance cosinus pour trouver les voisins les plus proches du metier en parametre.
        Params
        -------
        data : dataframe
            dataframe du corpus de compétences en 4 colonnes (identifiant, metier, competences, date)
        metier : str
            titre du metier à partir duquel nous calculons la distance
        Return
        -------
        result : dataframe
            dataframe en 2 colonnes (metier, distance calculé à partir du score tf-idf)
        """
        result = analyser.metier_competences(data)
        tfidf_vect = TfidfVectorizer()
        tfidf_weight = tfidf_vect.fit_transform(result['competences'])
        nn_cosine = NearestNeighbors(metric='cosine', algorithm='brute')
        nn_cosine.fit(tfidf_weight)
        index = result[result['metier'] == metier].index[0]
        cosine, indices = nn_cosine.kneighbors(tfidf_weight[index], n_neighbors = len(result))
        neighbors_cosine = pd.DataFrame({'tfidf': cosine.flatten(), 'id': indices.flatten()})
        nearest_info = result.merge(neighbors_cosine, right_on='id', left_index=True).sort_index().drop(['id', 'competences'], axis=1)
        #filtre les metiers dont la distance est superieur à la mediane
        nearest_info = nearest_info[nearest_info['tfidf']<=analyser.mediane(nearest_info, 'tfidf', True)]
        return nearest_info

    def visualiser_resultat(metier, data):
        corpus_c = analyser.competences_occurences(data, metier=metier)
        liste_c = list(corpus_c.index.values)
        corpus_tfidf = analyser.tf_idf(data, metier)
        liste_tfidf = list(corpus_tfidf['metier'].values)
        root = Tk()
        root.title('Compétences Plus')
        root.geometry('800x600')

        frame = Frame(root)
        frame.pack(fill=BOTH, expand=1)

        canvas = Canvas(frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=1)

        scrollb = ttk.Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
        scrollb.pack(side=RIGHT, fill=Y)

        canvas.bind('<Configure>', lambda e: canvas.config(scrollregion = canvas.bbox(ALL)))
        canvas.configure(yscrollcommand=scrollb.set)

        s_frame = Frame(canvas)
        canvas.create_window((0,0), window=s_frame, anchor="nw")

        Label(s_frame, text=f'Metier choisi : {metier}').pack(pady=20)
        Label(s_frame, text=f'Voici la liste des {len(liste_c)} compétences les plus recherchées par les recruteurs', bg="yellow").pack(pady=5)
        for l in liste_c:
            Label(s_frame, text=l).pack()
        Label(s_frame, text=f'Voici la liste des {len(liste_tfidf)} métiers les plus proches', bg="yellow").pack(pady=5)
        for l in liste_tfidf:
            Label(s_frame, text=l).pack()

        root.mainloop()

