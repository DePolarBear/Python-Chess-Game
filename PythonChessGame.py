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
            pozicia = pygame.mouse.get_pos()
            mysx, mysy = pygame.mouse.get_pos()
            stlpec = mysx // STVOREC
            riadok = mysy // STVOREC
            vybrane = (riadok, stlpec)

            print(vybrane)

    nakresli_dosku()
    nakresli_figurku()
    nakresli_vyber()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
