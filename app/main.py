from tkinter import *
from extraire import extraire
from analyser import analyser
from connecter import connecter

class main:
    value = -1
    def commencer():
        def choix(val):
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
            extraire.commencer()
        elif main.value == 2:
            connecter.sauvegarder()
        elif main.value == 3:
            analyser.commencer()
        else :
            exit(0)
        main.value = -1
        main.commencer()


if __name__ == "__main__":
    main.commencer()

