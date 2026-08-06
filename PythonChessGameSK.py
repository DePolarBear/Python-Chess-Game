import pygame

pygame.init()

# --- Konštanty (veci, ktoré sa nemenia) ---
STVOREC = 100
DOSKA = STVOREC * 8          # 800 - rozmer dosky (šírka aj výška)
PANEL = 200                  # šírka bočného panelu
SIRKA = DOSKA + PANEL        # celková šírka okna
VYSKA = DOSKA                # výška okna = výška dosky

# Farby políčok (RGB)
SVETLA = (240, 217, 181)        # svetlé pole
TMAVA  = (181, 136, 99)         # tmavé pole

pismo = pygame.font.SysFont("Arial", 60)
male_pismo = pygame.font.SysFont("Arial", 40)

screen = pygame.display.set_mode((SIRKA, VYSKA))
pygame.display.set_caption("Python Chess")
clock = pygame.time.Clock()

obrazky = {}                          # prázdny slovník, naplníme ho
for pismeno in "PRNBQKprnbqk":        # prejdi všetkých 12 písmen
    if pismeno.isupper():
        farba = "w"
    else:
        farba = "b"
    nazov = "figurky/" + farba + pismeno.upper() + ".svg"   # napr. figurky/wP.svg
    obr = pygame.image.load_sized_svg(nazov, (STVOREC, STVOREC))
    obr = obr.convert_alpha()
    obrazky[pismeno] = obr

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
                obrazok = obrazky[figurka]
                x = stlpec * STVOREC
                y = riadok * STVOREC
                screen.blit(obrazok, (x, y))

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

def je_rosada_mozna(doska, farba, stary_riadok, stary_stlpec, novy_stlpec, biely_kral_hybal, cierny_kral_hybal, veza_hybala):
    # riadok kráľa podľa farby
    if farba == "w":
        r = 7
        kral_hybal = biely_kral_hybal
    else:
        r = 0
        kral_hybal = cierny_kral_hybal

    # 1) kráľ sa nesmel hýbať
    if kral_hybal:
        return False

    # 2) kráľ nesmie byť práve v šachu
    if je_sach(doska, farba):
        return False

    if novy_stlpec == 6:
        # KRÁTKA rošáda (doprava, veža v rohu stĺpec 7)
        veza_stlpec = 7
        medzi = [5, 6]            # tieto stĺpce musia byť prázdne
        cez = [4, 5, 6]          # cez tieto kráľ prechádza (nesmú byť napadnuté)
    elif novy_stlpec == 2:
        # DLHÁ rošáda (doľava, veža v rohu stĺpec 0)
        veza_stlpec = 0
        medzi = [1, 2, 3]
        cez = [4, 3, 2]
    else:
        return False             # nie je to platný cieľ rošády

    if veza_hybala[(r, veza_stlpec)]:
        return False

    if farba == "w":
        veza = "R"
    else:
        veza = "r"
    if doska[r][veza_stlpec] != veza:
        return False

    for st in medzi:
        if doska[r][st] != ".":
            return False

    kral_pismeno = doska[r][stary_stlpec]        # kráľ (K alebo k)
    for st in cez:
        povodne = doska[r][st]
        doska[r][stary_stlpec] = "."             # vyprázdni pôvodné
        doska[r][st] = kral_pismeno              # polož kráľa na skúšané políčko
        napadnute = je_sach(doska, farba)
        doska[r][st] = povodne
        doska[r][stary_stlpec] = kral_pismeno
        if napadnute:
            return False
           
    return True

def nakresli_koniec():
    if koniec is None:
        return
    pruh = pygame.Surface((DOSKA, 100))    # široký ako doska, vysoký 100 px
    pruh.set_alpha(200)                     # dosť nepriehľadný, nech text vynikne
    pruh.fill((0, 0, 0))                    # čierny podklad
    screen.blit(pruh, (0, VYSKA // 2 - 50)) # zvisle na stred (polovica výšky mínus pol pruhu)
    obrazok = pismo.render(koniec, True, (255, 255, 255))
    sirka = obrazok.get_width()
    vyska = obrazok.get_height()
    x = DOSKA // 2 - sirka // 2
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
        pygame.draw.rect(screen, (0, 200, 0), (0, VYSKA - 4, DOSKA, 4))
    else:
        # čierny je hore - pruh hore
        pygame.draw.rect(screen, (0, 200, 0), (0, 0, DOSKA, 4))

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

def nakresli_cas():
    # čierny - úplne hore, vycentrovaný
    cb = int(cas_b)
    text_b = f"{cb // 60}:{cb % 60:02d}"
    obr_b = pismo.render(text_b, True, (255, 255, 255))
    xb = DOSKA + PANEL // 2 - obr_b.get_width() // 2
    screen.blit(obr_b, (xb, 20))

    # biely - úplne dole, vycentrovaný
    cw = int(cas_w)
    text_w = f"{cw // 60}:{cw % 60:02d}"
    obr_w = pismo.render(text_w, True, (255, 255, 255))
    xw = DOSKA + PANEL // 2 - obr_w.get_width() // 2
    yw = VYSKA - 20 - obr_w.get_height()
    screen.blit(obr_w, (xw, yw))

    # Restart - vertikálne v strede panelu
    pygame.draw.rect(screen, (70, 70, 70), restart_btn)
    text_btn = male_pismo.render("Restart", True, (255, 255, 255))
    tx = restart_btn.centerx - text_btn.get_width() // 2
    ty = restart_btn.centery - text_btn.get_height() // 2
    screen.blit(text_btn, (tx, ty))

doska = nova_doska()
hra_bezi = False      # časovač beží až po prvom ťahu
cas_w = 600.0      # biely - 10 minút v sekundách
cas_b = 600.0      # čierny - 10 minút v sekundách
running = True
vybrane = None
na_tahu = "w"      # biely začína
en_passant_ciel = None
biely_kral_hybal = False
cierny_kral_hybal = False
veza_hybala = {
    (7, 0): False,   # biela veža vľavo (dlhá strana)
    (7, 7): False,   # biela veža vpravo (krátka strana)
    (0, 0): False,   # čierna veža vľavo
    (0, 7): False,   # čierna veža vpravo
}
koniec = None      # kým hra beží; keď skončí, dáme sem text výsledku
restart_btn = pygame.Rect(DOSKA + PANEL // 2 - 80, VYSKA // 2 - 25, 160, 50)

while running:
    ms = clock.tick(60)
    sekundy = ms / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mysx, mysy = pygame.mouse.get_pos()
            if restart_btn.collidepoint(mysx, mysy):
                doska = nova_doska()
                na_tahu = "w"
                vybrane = None
                koniec = None
                hra_bezi = False
                cas_w = 600.0
                cas_b = 600.0
            elif koniec is None:
                stlpec = mysx // STVOREC
                riadok = mysy // STVOREC
                if riadok < 8 and stlpec < 8:
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
                        if figurka.lower() == "k" and stary_riadok == riadok and abs(stlpec - stary_stlpec) == 2 and je_rosada_mozna(doska, na_tahu, stary_riadok, stary_stlpec, stlpec, biely_kral_hybal, cierny_kral_hybal, veza_hybala):
                            # presun kráľa
                            doska[riadok][stlpec] = figurka
                            doska[stary_riadok][stary_stlpec] = "."
                            hra_bezi = True
                            # presun veže podľa strany
                            if stlpec == 6:
                                doska[riadok][5] = doska[riadok][7]
                                doska[riadok][7] = "."
                            else:
                                doska[riadok][3] = doska[riadok][0]
                                doska[riadok][0] = "."
                            # kráľ sa pohol
                            en_passant_ciel = None
                            if na_tahu == "w":
                                biely_kral_hybal = True
                            else:
                                cierny_kral_hybal = True
                            vybrane = None
                            # prepni hráča + kontrola matu
                            if na_tahu == "w":
                                na_tahu = "b"
                            else:
                                na_tahu = "w"
                            if not ma_legalny_tah(doska, na_tahu):
                                if je_sach(doska, na_tahu):
                                    koniec = "MAT - vyhral " + ("cierny" if na_tahu == "w" else "biely")
                                else:
                                    koniec = "PAT - remiza"

                        elif figurka.lower() == "p" and en_passant_ciel is not None and (riadok, stlpec) == en_passant_ciel:
                            # posuň svojho pešiaka na cieľ (prázdne políčko)
                            doska[riadok][stlpec] = figurka
                            doska[stary_riadok][stary_stlpec] = "."
                            hra_bezi = True
                            doska[stary_riadok][stlpec] = "."
                            en_passant_ciel = None
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

                        elif je_tah_platny(doska, figurka, stary_riadok, stary_stlpec, riadok, stlpec) and not ostane_kral_v_sachu(doska, na_tahu, stary_riadok, stary_stlpec, riadok, stlpec):
                            doska[riadok][stlpec] = figurka
                            doska[stary_riadok][stary_stlpec] = "."
                            hra_bezi = True
                            if figurka == "P" and riadok == 0:
                                doska[riadok][stlpec] = "Q"
                            if figurka == "p" and riadok == 7:
                                doska[riadok][stlpec] = "q"
                            if figurka == "K":
                                biely_kral_hybal = True
                            if figurka == "k":
                                cierny_kral_hybal = True
                            if (stary_riadok, stary_stlpec) in veza_hybala:
                                veza_hybala[(stary_riadok, stary_stlpec)] = True
                            if figurka.lower() == "p" and abs(riadok - stary_riadok) == 2:
                                en_passant_ciel = ((riadok + stary_riadok) // 2, stlpec)
                            else:
                                en_passant_ciel = None
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

    nakresli_dosku()
    pygame.draw.rect(screen, (50, 50, 55), (DOSKA, 0, PANEL, VYSKA))
    nakresli_cas()
    if na_tahu == "w":
        titulok = "Na tahu: biely"
    else:
        titulok = "Na tahu: cierny"
    if koniec is None and hra_bezi:
        if na_tahu == "w":
            cas_w = cas_w - sekundy
        else:
            cas_b = cas_b - sekundy
        if cas_w <= 0:
            koniec = "CAS VYPRSAL - vyhral cierny"
        if cas_b <= 0:
            koniec = "CAS VYPRSAL - vyhral biely"
    pygame.display.set_caption(titulok)
    nakresli_sach()
    nakresli_na_tahu()
    nakresli_moznosti()
    nakresli_figurku()
    nakresli_vyber()
    nakresli_koniec()

    pygame.display.flip()

pygame.quit()
