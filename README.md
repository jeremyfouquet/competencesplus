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
    ├── app
        ├── main.py
        ├── extraire.py
        ├── analyser.py
        └── connecter.py
    ├── assets
    ├── tests
        ├── extraire_t.py
        ├── analyser_t.py
        ├── connecter_t.py
        └── mocks.csv
    ├── Makefile
    ├── config.json
    ├── LICENSE
    ├── requirements.txt
    └── README.md
