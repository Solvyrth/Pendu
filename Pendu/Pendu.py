import tkinter as tk
from tkinter import messagebox
import random
import os
import unicodedata
import webbrowser

# Chargement du dictionnaire français
FRENCH_DICTIONARY_PATH = "mots_francais.txt"
if not os.path.exists(FRENCH_DICTIONARY_PATH):
    exit(1)

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

with open(FRENCH_DICTIONARY_PATH, encoding="utf-8") as f:
    WORDS = [strip_accents(w.strip().split()[0].lower()) for w in f if w.strip() and w[0].isalpha() and len(w.strip().split()[0]) > 3 and '-' not in w and "'" not in w]

PENDU_STAGES = [
    """
           \n           \n           \n           \n           \n           \n____       
    """,
    """
           \n |         \n |         \n |         \n |         \n |         \n_|___      
    """,
    """
  ______   \n |/        \n |         \n |         \n |         \n |         \n_|___      
    """,
    """
  ______   \n |/     |  \n |         \n |         \n |         \n |         \n_|___      
    """,
    """
  ______   \n |/     |  \n |      |  \n |         \n |         \n |         \n_|___      
    """,
    """
  ______   \n |/     |  \n |      |  \n |      O  \n |         \n |         \n_|___      
    """,
    """
  ______   \n |/     |  \n |      |  \n |      O  \n |      |  \n |         \n_|___      
    """,
    """
  ______   \n |/     |  \n |      |  \n |      O  \n |     /|  \n |         \n_|___      
    """,
    """
  ______   \n |/     |  \n |      |  \n |      O  \n |     /|\\ \n |         \n_|___      
    """,
    """
  ______   \n |/     |  \n |      |  \n |      O  \n |     /|\\ \n |     /   \n_|___      
    """,
    """
  ______   \n |/     |  \n |      |  \n |      O  \n |     /|\\ \n |     / \\ \n_|___      
    """
]

class PenduApp:
    def __init__(self, master):
        self.master = master
        master.title("Jeu du Pendu")
        self.score_joueur = 0
        self.score_ordi = 0
        self.label_score = tk.Label(master, text=self.get_score_text(), font=("Arial", 14, "bold"))
        self.label_score.pack(pady=5)
        self.reset_game()

        self.label_pendu = tk.Label(master, font=("Courier", 14), justify="left")
        self.label_pendu.pack(pady=10)

        self.label_mot = tk.Label(master, font=("Courier", 18))
        self.label_mot.pack(pady=10)

        self.label_lettres = tk.Label(master, text="Lettres ratées : ", font=("Arial", 12))
        self.label_lettres.pack(pady=5)

        self.entry = tk.Entry(master, font=("Arial", 14))
        self.entry.pack(pady=5)
        self.entry.bind('<Return>', lambda event: self.proposer())

        self.bouton = tk.Button(master, text="Proposer", command=self.proposer, font=("Arial", 12))
        self.bouton.pack(pady=5)

        self.label_info = tk.Label(master, text="Proposez une lettre ou un mot.", font=("Arial", 10))
        self.label_info.pack(pady=5)

        # Frame pour les crédits
        credits_frame = tk.Frame(master)
        credits_frame.pack(side=tk.BOTTOM, pady=10)
        
        # Texte des crédits
        tk.Label(credits_frame, text="Développé par Solvyrth • ", font=("Arial", 11),
                fg="#424242").pack(side=tk.LEFT)
        
        # Lien GitHub cliquable avec style macOS
        github_label = tk.Label(credits_frame, text="GitHub", font=("Arial", 11, "underline"),
                               fg="#007AFF", cursor="hand2")
        github_label.pack(side=tk.LEFT)
        github_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/Solvyrth"))
        # Effet hover
        github_label.bind("<Enter>", lambda e: github_label.config(fg="#0051D0"))
        github_label.bind("<Leave>", lambda e: github_label.config(fg="#007AFF"))

        self.afficher()

    def get_score_text(self):
        return f"👤 Joueur : {self.score_joueur}    |    🤖 Ordinateur : {self.score_ordi}"

    def reset_game(self):
        self.mot = random.choice(WORDS)
        self.lettres_trouvees = set()
        self.lettres_ratees = set()
        self.erreurs = 0
        self.max_erreurs = len(PENDU_STAGES) - 1
        self.fini = False
        if hasattr(self, 'label_score'):
            self.label_score.config(text=self.get_score_text())

    def afficher(self):
        self.label_pendu.config(text=PENDU_STAGES[self.erreurs])
        mot_affiche = ' '.join([l if l in self.lettres_trouvees else '_' for l in self.mot])
        self.label_mot.config(text=mot_affiche)
        self.label_lettres.config(text=f"Lettres ratées : {', '.join(sorted(self.lettres_ratees))}")

    def proposer(self):
        if self.fini:
            self.reset_game()
            self.afficher()
            self.label_info.config(text="Nouvelle partie ! Proposez une lettre ou un mot.")
            return
        proposition = self.entry.get().lower().strip()
        proposition = strip_accents(proposition)
        self.entry.delete(0, tk.END)
        if not proposition.isalpha():
            self.label_info.config(text="Veuillez entrer uniquement des lettres.")
            return
        if len(proposition) == 1:
            lettre = proposition
            if lettre in self.lettres_trouvees or lettre in self.lettres_ratees:
                self.label_info.config(text="Vous avez déjà proposé cette lettre.")
                return
            if lettre in self.mot:
                self.lettres_trouvees.add(lettre)
                if all(l in self.lettres_trouvees for l in self.mot):
                    self.score_joueur += 1
                    self.afficher()
                    self.label_score.config(text=self.get_score_text())
                    messagebox.showinfo("Gagné !", f"Bravo ! Vous avez trouvé le mot : {self.mot}")
                    self.fini = True
                    self.label_info.config(text="Cliquez sur Proposer ou appuyez sur Entrée pour rejouer.")
                    return
            else:
                self.lettres_ratees.add(lettre)
                self.erreurs += 1
        else:
            if proposition == self.mot:
                self.score_joueur += 1
                self.lettres_trouvees = set(self.mot)
                self.afficher()
                self.label_score.config(text=self.get_score_text())
                messagebox.showinfo("Gagné !", f"Bravo ! Vous avez trouvé le mot : {self.mot}")
                self.fini = True
                self.label_info.config(text="Cliquez sur Proposer ou appuyez sur Entrée pour rejouer.")
                return
            else:
                self.erreurs += 1
                self.label_info.config(text="Ce n'est pas le bon mot.")
        if self.erreurs >= self.max_erreurs:
            self.score_ordi += 1
            self.afficher()
            self.label_score.config(text=self.get_score_text())
            messagebox.showerror("Perdu !", f"Le bonhomme est pendu... Le mot était : {self.mot}")
            self.fini = True
            self.label_info.config(text="Cliquez sur Proposer ou appuyez sur Entrée pour rejouer.")
            return
        self.afficher()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x500")  # Largeur x Hauteur
    app = PenduApp(root)
    root.mainloop()
