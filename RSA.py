# Clés d'exemple :
# e = 17 , n = 3233
# d = 2753 , n = 3233

import hashlib


def mod_exp(base, exp, mod):
    """Exponentiation modulaire rapide"""
    return pow(base, exp, mod)


# ----------- FONCTION DE HACHAGE -----------

def H(message):
    """Crée une empreinte numérique (Hash) du message"""
    h = hashlib.sha256(message.encode()).hexdigest()
    return int(h, 16)


# ----------- CONVERSION : TEXTE <-> BLOCS -----------

def texte_vers_blocs(message, n):
    """Transforme chaque caractère en son code ASCII"""
    blocs = []

    for c in message:
        code = ord(c)

        if code >= n:
            print(f"Erreur : n={n} est trop petit pour le caractère '{c}'")
            return None

        blocs.append(code)

    return blocs


def blocs_vers_texte(blocs):
    """Transforme les codes ASCII en texte"""
    return "".join(chr(b) for b in blocs)


# ----------- CHIFFREMENT -----------

def chiffrer(message, e, n):
    blocs = texte_vers_blocs(message, n)

    if blocs is None:
        return None

    # Formule : C = M^e mod n
    return [mod_exp(m, e, n) for m in blocs]


# ----------- DÉCHIFFREMENT -----------

def dechiffrer(blocs, d, n):
    # Formule : M = C^d mod n
    clair = [mod_exp(c, d, n) for c in blocs]
    return blocs_vers_texte(clair)


# ----------- MENU PRINCIPAL -----------

while True:

    print("\n" + "=" * 25)
    print("        MENU RSA")
    print("=" * 25)
    print("1 - Chiffrement")
    print("2 - Déchiffrement")
    print("3 - Signature")
    print("4 - Vérification")
    print("5 - Quitter")

    choix = input("\nChoix : ")

    # ----------- CHIFFREMENT -----------

    if choix == "1":

        msg = input("Message à chiffrer : ")
        e = int(input("Entrez l'exposant public (e) : "))
        n = int(input("Entrez le module (n) : "))

        resultat = chiffrer(msg, e, n)

        if resultat:
            print("Message chiffré :")
            print(" ".join(map(str, resultat)))

    # ----------- DÉCHIFFREMENT -----------

    elif choix == "2":

        data = input("Entrez les blocs chiffrés (séparés par un espace) : ")
        blocs = list(map(int, data.split()))

        d = int(input("Entrez votre clé privée (d) : "))
        n = int(input("Entrez votre module (n) : "))

        message = dechiffrer(blocs, d, n)

        print("Message déchiffré :")
        print(message)

    # ----------- SIGNATURE -----------

    elif choix == "3":

        msg = input("Message à signer : ")

        d = int(input("Entrez votre clé privée (d) : "))
        n = int(input("Entrez votre module (n) : "))

        # Signature = Hash(message)^d mod n
        signature = mod_exp(H(msg), d, n)

        print("Signature générée :")
        print(signature)

    # ----------- VÉRIFICATION -----------

    elif choix == "4":

        msg = input("Message clair reçu : ")

        sig = int(input("Entrez la signature à vérifier : "))
        e = int(input("Entrez la clé publique de l'expéditeur (e) : "))
        n = int(input("Entrez le module (n) : "))

        h_original = H(msg) % n
        h_decrypte = mod_exp(sig, e, n)

        if h_original == h_decrypte:
            print("\n✓ Signature VALIDE")
            print("Authenticité confirmée.")
        else:
            print("\n✗ Signature INVALIDE")
            print("Le message a été modifié ou la clé est incorrecte.")

    # ----------- QUITTER -----------

    elif choix == "5":

        print("Fin du programme.")
        break

    # ----------- ERREUR -----------

    else:
        print("Option non reconnue.")