import random
import requests
print(r'''

.-------.     .-''-.  ,---.   .--. ______       ___    _  
\  _(`)_ \  .'_ _   \ |    \  |  ||    _ `''. .'   |  | | 
| (_ o._)| / ( ` )   '|  ,  \ |  || _ | ) _  \|   .'  | | 
|  (_,_) /. (_ o _)  ||  |\_ \|  ||( ''_'  ) |.'  '_  | | 
|   '-.-' |  (_,_)___||  _( )_\  || . (_) `. |'   ( \.-.| 
|   |     '  \   .---.| (_ o _)  ||(_    ._) '' (`. _` /| 
|   |      \  `-'    /|  (_,_)\  ||  (_.\.' / | (_ (_) _) 
/   )       \       / |  |    |  ||       .'   \ /  . \ / 
`---'        `'-..-'  '--'    '--''-----'`      ``-'`-'' 
                    Coder par Solvyrth
                https://github.com/Solvyrth
                        Version 1.0
              
                                                          
''')

COCHON_PENDU_STAGES = [
    [
        "   _____   ",
        "  (     )  ",
        "  ( o o )  ",
        "  /  V  \\  ",
        " /(     )\\ ",
        "  ^^   ^^  "
    ],
    [
        "   _____   ",
        "  (     )  ",
        "  ( o o )  ",
        "  /  V  \\  ",
        " /(     )\\ ",
        "  ^^   ^   "
    ],
    [
        "   _____   ",
        "  (     )  ",
        "  ( o o )  ",
        "  /  V  \\  ",
        " /(     )\\ ",
        "  ^    ^   "
    ],
    [
        "   _____   ",
        "  (     )  ",
        "  ( o o )  ",
        "  /  V  \\  ",
        " /(     )\\ ",
        "       ^   "
    ],
    [
        "   _____   ",
        "  (     )  ",
        "  ( o o )  ",
        "  /  V  \\  ",
        " /(     )\\ ",
        "           "
    ],
    [
        "   _____   ",
        "  (     )  ",
        "  ( x x )  ",
        "  /  V  \\  ",
        " /(     )\\ ",
        "           "
    ],
    [
        "   _____   ",
        "  (     )  ",
        "  ( x x )  ",
        "  /  V  \\  ",
        " /(     )\\ ",
        "  //   \\  "
    ]
]

WORDS = []

def afficher_cochon_pendu(erreurs):
    for ligne in COCHON_PENDU_STAGES[erreurs]:
        print(ligne)
    print()

def get_random_word():
    try:
        response = requests.get("https://random-word-api.herokuapp.com/word?lang=fr")
        if response.status_code == 200:
            word = response.json()[0]
            return word.lower()
    except Exception:
        pass

def jouer():
    mot = get_random_word()
    lettres_trouvees = set()
    lettres_ratees = set()
    essais = len(COCHON_PENDU_STAGES) - 1
    erreurs = 0

    print("Bienvenue au jeu du Cochon Pandu ! que le jeux commence !")
    afficher_cochon_pendu(erreurs)

    while erreurs < essais:
        mot_affiche = ' '.join([l if l in lettres_trouvees else '_' for l in mot])
        print(f"Mot : {mot_affiche}")
        print(f"Lettres ratées : {', '.join(sorted(lettres_ratees))}")
        afficher_cochon_pendu(erreurs)
        lettre = input("Proposez une lettre : ").lower()
        if not lettre.isalpha() or len(lettre) != 1:
            print("Veuillez entrer une seule lettre.")
            continue
        if lettre in lettres_trouvees or lettre in lettres_ratees:
            print("Vous avez déjà proposé cette lettre.")
            continue
        if lettre in mot:
            lettres_trouvees.add(lettre)
            if all(l in lettres_trouvees for l in mot):
                print(f"Bravo ! Vous avez sauvé le cochon ! Le mot était : {mot}")
                afficher_cochon_pendu(erreurs)
                return
        else:
            lettres_ratees.add(lettre)
            erreurs += 1
    print(f"Perdu ! Le cochon est pendu... Le mot était : {mot}")
    afficher_cochon_pendu(erreurs)

if __name__ == "__main__":
    jouer()
