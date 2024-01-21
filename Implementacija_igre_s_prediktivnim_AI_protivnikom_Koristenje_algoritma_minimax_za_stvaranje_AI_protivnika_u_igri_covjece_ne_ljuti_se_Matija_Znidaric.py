import random

broj_polja = 30
pozicije = {'Igrač': [None]*4, 'AI': [None]*4}

def baci_kocku():
    return random.randint(1, 6)

def ima_moguce_poteze(igrac, bacanje):
    for p in pozicije[igrac]:
        if (p is None and bacanje == 6) or (p is not None and p != "Finished"):
            return True
    return False

def pojedi_figuricu(igrac, protivnik, nova_pozicija):
    for i, pos in enumerate(pozicije[protivnik]):
        if pos == nova_pozicija:
            pozicije[protivnik][i] = None
            break

def moze_postaviti_figuricu(igrac):
    return 0 not in pozicije[igrac]

def evaluiraj_potez(potez, je_pojedena):
    bodovi = 0
    if je_pojedena:
        bodovi = 7

    if potez == "Finished":
        return 10 + bodovi
    elif potez == 0:
        return 5 + bodovi
    elif potez is not None:
        return 1 + bodovi

    return -1 + bodovi

def pomakni_figuricu(igrac, figurica, bacanje):
    protivnik = 'AI' if igrac == 'Igrač' else 'Igrač'
    je_pojedena = False

    if pozicije[igrac][figurica] is None:
        if bacanje == 6:
            if not moze_postaviti_figuricu(igrac):
                return False, je_pojedena
            if 0 in pozicije[protivnik]:
                pojedi_figuricu(igrac, protivnik, 0)
                je_pojedena = True
            pozicije[igrac][figurica] = 0
            return True, je_pojedena
    elif pozicije[igrac][figurica] != "Finished":
        nova_pozicija = pozicije[igrac][figurica] + bacanje
        if nova_pozicija not in pozicije[igrac]:
            if nova_pozicija < broj_polja:
                if nova_pozicija in pozicije[protivnik]:
                    pojedi_figuricu(igrac, protivnik, nova_pozicija)
                    je_pojedena = True
                pozicije[igrac][figurica] = nova_pozicija
            else:
                pozicije[igrac][figurica] = "Finished"
            return True, je_pojedena

    return False, je_pojedena

def minmax_ai(bacanje):
    najbolji_rezultat = -float('inf')
    najbolji_potez = None

    for i in range(4):
        kopija_pozicija = pozicije['AI'][:]
        pomaknuto, je_pojedena = pomakni_figuricu('AI', i, bacanje)
        if pomaknuto:
            rezultat_poteza = pozicije['AI'][i]
            ocjena = evaluiraj_potez(rezultat_poteza, je_pojedena)
            if ocjena > najbolji_rezultat:
                najbolji_rezultat = ocjena
                najbolji_potez = i
            pozicije['AI'] = kopija_pozicija

    return najbolji_potez

def igraj():
    trenutni_igrac = 'Igrač'
    while True:
        bacanje = baci_kocku()
        print(f"{trenutni_igrac}, bacili ste: {bacanje}")

        if ima_moguce_poteze(trenutni_igrac, bacanje):
            if trenutni_igrac == 'Igrač':
                while True:
                    izbor = int(input(f"{trenutni_igrac}, odaberite figuricu (1-4): ")) - 1
                    if 0 <= izbor < 4:
                        pomaknuto, _ = pomakni_figuricu(trenutni_igrac, izbor, bacanje)
                        if pomaknuto:
                            break
            else:
                izbor = minmax_ai(bacanje)
                if izbor is not None:
                    pomakni_figuricu(trenutni_igrac, izbor, bacanje)
                    print(f"AI je pomaknuo figuricu {izbor + 1}\n")

        if all(p == "Finished" for p in pozicije[trenutni_igrac]):
            print(f"{trenutni_igrac} je pobjedio!")
            return

        print("\n Trenutne pozicije:")
        for igrac, poz in pozicije.items():
            print(f"{igrac}: {poz}")

        if bacanje != 6 or not ima_moguce_poteze(trenutni_igrac, bacanje):
            trenutni_igrac = 'AI' if trenutni_igrac == 'Igrač' else 'Igrač'

igraj()