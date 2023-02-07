from tkinter import *
from extraire import extraire
from analyser import analyser
from connecter import connecter

class main:
    value = -1
    def commencer():
        """
        Interface graphique donnant 3 choix d'action à l'utilisateur
        """
        def choix(val):
            """
            Affect a value la valeur du paramettre val puis ferme l'interface
            Parameters
            ----------
            val : int
                choix de l'action
            """
            main.value = val
            root.destroy()
        root = Tk()
        root.title('Compétences Plus')
        label = Label(text='Que souhaitez vous faire ?')
        label.pack(pady=20)
        btn1 = Button(text='Créer/Extraire un corpus de compétences', command=lambda:choix(1))
        btn1.pack(pady=20)
        btn2 = Button(text='Sauvergarder la base de données au fromat CSV', command=lambda:choix(2))
        btn2.pack(pady=20)
        btn3 = Button(text='Analyser/Évaluer un corpus de compétences', command=lambda:choix(3))
        btn3.pack(pady=20)
        root.mainloop()
        if main.value == 1:
            # création du corpus de compétences
            extraire.commencer()
        elif main.value == 2:
            # sauvagarde la base de données dans un fichier csv
            connecter.sauvegarder()
        elif main.value == 3:
            # évaluation du corpus de compétences
            analyser.commencer()
        else :
            exit(0)
        main.value = -1
        main.commencer()


if __name__ == "__main__":
    main.commencer()

