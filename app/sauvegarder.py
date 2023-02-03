from tkinter import *
from connecter import connecter

class sauvegarder:
    def commencer():
        root = Tk()
        root.geometry('500x200')
        root.title('Compétences Plus')
        titre = Label(text='Sauvergarde en cours ...')
        titre.pack(pady=20)
        info = connecter.save_bdd_csv()
        if info == 'Succes Enregistrement':
            titre.config(text="Sauvergarde Terminé")
        else:
            titre.config(text=info)
        root.update()
        root.mainloop()



