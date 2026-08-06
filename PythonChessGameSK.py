import pygame

pygame.init()

# --- Konštanty (veci, ktoré sa nemenia) ---
STVOREC = 80                    # veľkosť jedného políčka v pixeloch
SIRKA = VYSKA = STVOREC * 8     # doska je 8x8 políčok -> 640x640

# Farby políčok (RGB)
SVETLA = (240, 217, 181)        # svetlé pole
TMAVA  = (181, 136, 99)         # tmavé pole

pismo = pygame.font.SysFont("Arial", 60)
male_pismo = pygame.font.SysFont("Arial", 40)

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
    pygame.draw.rect(screen, (0, 150, 0), (x, y, STVOREC, STVOREC), 2)

def nakresli_moznosti():
    if vybrane is None:
        return
    vyb_riadok, vyb_stlpec = vybrane
    figurka = doska[vyb_riadok][vyb_stlpec]
    zvyraznenie = pygame.Surface((STVOREC, STVOREC))   # malá plocha veľkosti políčka
    zvyraznenie.set_alpha(50)                          # priehľadnosť: 0 = neviditeľné, 255 = plné
    zvyraznenie.fill((0, 200, 0))                       # vyplň zelenou

    for r in range(8):
        for s in range(8):
            if je_tah_platny(doska, figurka, vyb_riadok, vyb_stlpec, r, s):
                x = s * STVOREC
                y = r * STVOREC
                screen.blit(zvyraznenie, (x, y))


def je_cesta_volna(doska, stary_riadok, stary_stlpec, novy_riadok, novy_stlpec):
    d_riadok = novy_riadok - stary_riadok
    d_stlpec = novy_stlpec - stary_stlpec

    if d_riadok > 0:
        krok_riadok = 1
    elif d_riadok < 0:
        krok_riadok = -1
    else:
        krok_riadok = 0

    if d_stlpec > 0:
        krok_stlpec = 1
    elif d_stlpec < 0:
        krok_stlpec = -1
    else:
        krok_stlpec = 0
    
    r = stary_riadok + krok_riadok
    s = stary_stlpec + krok_stlpec
    # kráčaj, kým si nedošiel na cieľ
    while (r, s) != (novy_riadok, novy_stlpec):
        if doska[r][s] != ".":
            return False        # niečo stojí v ceste
        r = r + krok_riadok     # ďalší krok
        s = s + krok_stlpec
    return True

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
            if (d_riadok == 0 or d_stlpec == 0) and je_cesta_volna(doska, stary_riadok, stary_stlpec, novy_riadok, novy_stlpec):
                return True
            else:
                return False
        if figurka.lower() == "b":
            if (abs(d_riadok) == abs(d_stlpec)) and je_cesta_volna(doska, stary_riadok, stary_stlpec, novy_riadok, novy_stlpec):
                return True
            else:
                return False
        if figurka.lower() == "q":
            if (d_riadok == 0 or d_stlpec == 0 or abs(d_riadok) == abs(d_stlpec)) and je_cesta_volna(doska, stary_riadok, stary_stlpec, novy_riadok, novy_stlpec):
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
            if (d_stlpec == 0 and d_riadok == 2 * smer and ciel == "." and stary_riadok == start) and je_cesta_volna(doska, stary_riadok, stary_stlpec, novy_riadok, novy_stlpec):
                return True
            if abs(d_stlpec) == 1 and d_riadok == smer and ciel != ".":
                return True

        return False

def je_sach(doska, farba):
    if farba == "w":
        kral = "K"
    else:
        kral = "k"

    if farba == "w":
        super_farba = "b"
    else:
        super_farba = "w"

    for r in range(8):
        for s in range(8):
            if doska[r][s] == kral:
                kral_riadok = r
                kral_stlpec = s
    for r in range(8):
        for s in range(8):
            f = doska[r][s]
            if f != ".":
                if f.isupper():
                    f_farba = "w"
                else:
                    f_farba = "b"
                if f_farba == super_farba:
                    if je_tah_platny(doska, f, r, s, kral_riadok, kral_stlpec):
                        return True
    return False

def ostane_kral_v_sachu(doska, farba, stary_riadok, stary_stlpec, novy_riadok, novy_stlpec):
    figurka = doska[stary_riadok][stary_stlpec]      # koho ťaháme
    povodny_ciel = doska[novy_riadok][novy_stlpec]   # čo bolo na cieli (možno súper, možno bodka)
    doska[novy_riadok][novy_stlpec] = figurka
    doska[stary_riadok][stary_stlpec] = "."
    v_sachu = je_sach(doska, farba)
    doska[stary_riadok][stary_stlpec] = figurka
    doska[novy_riadok][novy_stlpec] = povodny_ciel
    return v_sachu

def ma_legalny_tah(doska, farba):
    for fr in range(8):                 # figúrka: riadok
        for fs in range(8):             # figúrka: stĺpec
            f = doska[fr][fs]
            if f == ".":
                continue
            if f.isupper():
                f_farba = "w"
            else:
                f_farba = "b"
            if f_farba != farba:
                continue
            
            for cr in range(8):         # cieľ: riadok
                for cs in range(8):     # cieľ: stĺpec
                    if je_tah_platny(doska, f, fr, fs, cr, cs) and not ostane_kral_v_sachu(doska, farba, fr, fs, cr, cs):
                        return True
    return False

def nakresli_koniec():
    if koniec is None:
        return
    pruh = pygame.Surface((SIRKA, 100))    # široký ako doska, vysoký 100 px
    pruh.set_alpha(200)                     # dosť nepriehľadný, nech text vynikne
    pruh.fill((0, 0, 0))                    # čierny podklad
    screen.blit(pruh, (0, VYSKA // 2 - 50)) # zvisle na stred (polovica výšky mínus pol pruhu)
    obrazok = pismo.render(koniec, True, (255, 255, 255))
    sirka = obrazok.get_width()
    vyska = obrazok.get_height()
    x = SIRKA // 2 - sirka // 2
    y = VYSKA // 2 - vyska // 2
    screen.blit(obrazok, (x, y))

    pygame.draw.rect(screen, (70, 70, 70), restart_btn)          # sivý obdĺžnik tlačidla
    text_btn = male_pismo.render("Restart", True, (255, 255, 255))
    # a text vycentrovať na stred tlačidla:
    tx = restart_btn.centerx - text_btn.get_width() // 2
    ty = restart_btn.centery - text_btn.get_height() // 2
    screen.blit(text_btn, (tx, ty))

def nakresli_sach():
    for farba in ("w", "b"):              # skontroluj oboch kráľov
        if je_sach(doska, farba):          # je tento kráľ v šachu?
            if farba == "w":
                kral = "K"
            else:
                kral = "k"
            # nájdi kráľa na doske a zvýrazni jeho políčko
            for r in range(8):
                for s in range(8):
                    if doska[r][s] == kral:
                        x = s * STVOREC
                        y = r * STVOREC
                        pygame.draw.rect(screen, (200, 0, 0), (x, y, STVOREC, STVOREC), 2)

def nakresli_na_tahu():
    if na_tahu == "w":
        # biely je dole - pruh dole
        pygame.draw.rect(screen, (0, 200, 0), (0, VYSKA - 4, SIRKA, 4))
    else:
        # čierny je hore - pruh hore
        pygame.draw.rect(screen, (0, 200, 0), (0, 0, SIRKA, 4))

def nova_doska():
    return [
        ["r","n","b","q","k","b","n","r"],
        ["p"] * 8,
        ["."] * 8,
        ["."] * 8,
        ["."] * 8,
        ["."] * 8,
        ["P"] * 8,
        ["R","N","B","Q","K","B","N","R"],
    ]

doska = nova_doska()

running = True
vybrane = None
na_tahu = "w"      # biely začína
koniec = None      # kým hra beží; keď skončí, dáme sem text výsledku
restart_btn = pygame.Rect(SIRKA // 2 - 80, VYSKA // 2 + 60, 160, 50)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mysx, mysy = pygame.mouse.get_pos()
            if koniec is None:
                stlpec = mysx // STVOREC
                riadok = mysy // STVOREC
                
                if vybrane is None:
                    klik = doska[riadok][stlpec]
                    if klik != ".":
                        if klik.isupper():
                            farba_figurky = "w"
                        else:
                            farba_figurky = "b"
                        if farba_figurky == na_tahu:
                            vybrane = (riadok, stlpec)
                else:
                    stary_riadok, stary_stlpec = vybrane
                    figurka = doska[stary_riadok][stary_stlpec]
                    if je_tah_platny(doska, figurka, stary_riadok, stary_stlpec, riadok, stlpec) and not ostane_kral_v_sachu(doska, na_tahu, stary_riadok, stary_stlpec, riadok, stlpec):
                        doska[riadok][stlpec] = figurka
                        doska[stary_riadok][stary_stlpec] = "."
                        if figurka == "P" and riadok == 0:
                            doska[riadok][stlpec] = "Q"
                        if figurka == "p" and riadok == 7:
                            doska[riadok][stlpec] = "q"
                        vybrane = None
                        if na_tahu == "w":
                            na_tahu = "b"
                        else:
                            na_tahu = "w"
                        if not ma_legalny_tah(doska, na_tahu):
                            if je_sach(doska, na_tahu):
                                koniec = "MAT - vyhral " + ("cierny" if na_tahu == "w" else "biely")
                            else:
                                koniec = "PAT - remiza"
                    else:
                        vybrane = None
                print(vybrane)
            else:
                if restart_btn.collidepoint(mysx, mysy):
                    doska = nova_doska()
                    na_tahu = "w"
                    vybrane = None
                    koniec = None

    nakresli_dosku()
    if na_tahu == "w":
        titulok = "Na tahu: biely"
    else:
        titulok = "Na tahu: cierny"
    pygame.display.set_caption(titulok)
    nakresli_sach()
    nakresli_na_tahu()
    nakresli_moznosti()
    nakresli_figurku()
    nakresli_vyber()
    nakresli_koniec()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
