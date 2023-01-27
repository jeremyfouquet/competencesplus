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
$ python --version
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

## Structure
    .
    ├── app
        ├── main.py
        ├── extraire.py
        ├── analyser.py
        ├── connecter.py
        └── __init__.py
    ├── assets
    ├── tests
    ├── Makefile
    ├── config.json
    ├── LICENSE
    ├── requirements.txt
    └── README.md