import pygame

pygame.init()

# --- Konštanty (veci, ktoré sa nemenia) ---
STVOREC = 80                    # veľkosť jedného políčka v pixeloch
SIRKA = VYSKA = STVOREC * 8     # doska je 8x8 políčok -> 640x640

# Farby políčok (RGB)
SVETLA = (240, 217, 181)        # svetlé pole
TMAVA  = (181, 136, 99)         # tmavé pole

pismo = pygame.font.SysFont("Arial", 60)

screen = pygame.display.set_mode((SIRKA, VYSKA))
pygame.display.set_caption("Python Chess")
clock = pygame.time.Clock()

def nakresli_dosku():
    for riadok in range(8):             # 0 až 7 (osem riadkov)
        for stlpec in range(8):         # 0 až 7 (osem stĺpcov)
            # striedanie farieb: keď je súčet párny -> svetlá, inak tmavá
            if (riadok + stlpec) % 2 == 0:
                farba = SVETLA
            else:
                farba = TMAVA
            # obdĺžnik: (x, y, šírka, výška)
            x = stlpec * STVOREC
            y = riadok * STVOREC
            pygame.draw.rect(screen, farba, (x, y, STVOREC, STVOREC))

def nakresli_figurku():
    for riadok in range(8):             # 0 až 7 (osem riadkov)
        for stlpec in range(8):         # 0 až 7 (osem stĺpcov)
            figurka = doska[riadok][stlpec]
            if figurka != ".":  # Podmienka vykreslenia
                if figurka.isupper():  # Volba farby figurky, ak je pismeno velke biela aj nie je velke cierna
                    farba = (255, 255, 255)   # biela
                else:
                    farba = (0, 0, 0)         # čierna
                obrazok = pismo.render(figurka, True, farba)
                sirka = obrazok.get_width()  # Vypocet sirky pismenka
                vyska = obrazok.get_height()  # Vypocet vysky pismenka
                x = stlpec * STVOREC + (STVOREC - sirka) // 2  # Pozicia pismenka + centrovanie
                y = riadok * STVOREC + (STVOREC - vyska) // 2  # Pozicia pismenka + centrovanie
                screen.blit(obrazok, (x, y))  # Vykreslenie pismenka na suradnicu x a y

def nakresli_vyber():
    if vybrane is None:
        return
    riadok, stlpec = vybrane
    x = stlpec * STVOREC
    y = riadok * STVOREC
    pygame.draw.rect(screen, (0, 255, 0), (x, y, STVOREC, STVOREC), 2)

def je_cesta_volna(doska, stary_riadok, stary_stlpec, novy_riadok, novy_stlpec):

def je_tah_platny(doska, figurka, stary_riadok, stary_stlpec, novy_riadok, novy_stlpec):
    ciel = doska[novy_riadok][novy_stlpec]
    if (novy_riadok, novy_stlpec) == (stary_riadok, stary_stlpec):
        return False
    if ciel != "." and ciel.isupper() == figurka.isupper():
        return False
    else:
        d_riadok = novy_riadok - stary_riadok
        d_stlpec = novy_stlpec - stary_stlpec

        if figurka.lower() == "r":
            if d_riadok == 0 or d_stlpec == 0:
                return True
            else:
                return False
        if figurka.lower() == "b":
            if abs(d_riadok) == abs(d_stlpec):
                return True
            else:
                return False
        if figurka.lower() == "q":
            if d_riadok == 0 or d_stlpec == 0 or abs(d_riadok) == abs(d_stlpec):
                return True
            else:
                return False
        if figurka.lower() == "n":
            if (abs(d_riadok) == 2 and abs(d_stlpec) == 1) or (abs(d_riadok) == 1 and abs(d_stlpec) == 2):
                return True
            else:
                return False
        if figurka.lower() == "k":
            if abs(d_riadok) <= 1 and abs(d_stlpec) <= 1:
                return True
            else:
                return False
        if figurka.lower() == "p":
            if figurka.isupper():
                smer = -1        # biely ide hore (menšie riadky)
                start = 6
            else:
                smer = 1         # čierny ide dole (väčšie riadky)
                start = 1
            if d_stlpec == 0 and d_riadok == smer and ciel == ".":
                return True
            if d_stlpec == 0 and d_riadok == 2 * smer and ciel == "." and stary_riadok == start:
                return True
            if abs(d_stlpec) == 1 and d_riadok == smer and ciel != ".":
                return True

        return False


doska = [
    ["r","n","b","q","k","b","n","r"],
    ["p"] * 8,
    ["."] * 8,
    ["."] * 8,
    ["."] * 8,
    ["."] * 8,
    ["P"] * 8,
    ["R","N","B","Q","K","B","N","R"]
]

#for i in range(8):
#    riadok = [".",".",".",".",".",".",".","."]
#    doska.append(riadok)

for r in doska:
    print(r)


running = True
vybrane = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mysx, mysy = pygame.mouse.get_pos()
            stlpec = mysx // STVOREC
            riadok = mysy // STVOREC
            
            if vybrane is None:
                if doska[riadok][stlpec] != ".":
                    vybrane = (riadok, stlpec)
            else:
                stary_riadok, stary_stlpec = vybrane
                figurka = doska[stary_riadok][stary_stlpec]
                if je_tah_platny(doska, figurka, stary_riadok, stary_stlpec, riadok, stlpec):
                    doska[riadok][stlpec] = figurka
                    doska[stary_riadok][stary_stlpec] = "."
                    vybrane = None
                else:
                    vybrane = None



            print(vybrane)

    nakresli_dosku()
    nakresli_figurku()
    nakresli_vyber()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
