# CompetencesPlus

Application de recherche et analyse de compétences en informatique

## Version

1.0.0

## Projet

## Auteur

Jeremy Fouquet

## Url Projet

https://github.com/jeremyfouquet/competencesplus.git

## license

MIT License

## Exigences

Version Python utilisé = 3.9
Version Python nécéssaire >= 3.7

Vérifier la version Python:
```
$ python3 --version
```

Mettre à jours la version de Python:
```
$ sudo apt update
$ sudo apt install pythonX.X
```

Les packages utilisé sont dans `requirements.txt`

## Utilisation

Executer le programme
```
$ make run
```

Nettoyer le cache
```
$ make clean
```

Installer les packages suivant (pouvant être manquant sur le système linux):
- python3-venv
- python3-tk
```
$ make linux_packages
```

## Structure
    .
    ├── app : contient les modules du programme
        ├── main.py
        ├── extraire.py
        ├── analyser.py
        └── connecter.py
    ├── assets : contient les fichiers d'extractions
    ├── tests : contient les modules de tests unitaires
        ├── extraire_t.py
        ├── analyser_t.py
        ├── connecter_t.py
        └── mocks.csv
    ├── Makefile : contient les directives d'automatisation de tests, de nettoyage, d'installation de dépendances et de lancement du programme
    ├── config.json : contient les congigurations de connection PostgreSQL
    ├── LICENSE : contient la licence MIT
    ├── requirements.txt : contient toutes les dépendances et version nécessaires
    └── README.md : contient la description du programme et la documentation technique
