import random
import hangmanpics


class Akasztofa:

    # ez osztály változó, nem példány változó
    # minden objektumpéldánynál ugyanaz értéke
    ervenyes_betuk = "aábcdeéfghiíjklmnoóöőpqrstuúüűvwxyz"

    # konstruktor
    def __init__(self, fajlnev):
        self.fajlnev = fajlnev
        self.feladott_szo = ""
        self.feladvany_allasa = []
        self.hibak_szama = 0
        self.tippelt_betuk = []
        self.korabbi_feladvanyok = []

        kilep = False
        while not kilep:
            self.intro()
            self.uj()
            self.jatek()
            kilep = self.kilep_teszt()

        print("Viszlát!")

    """
    Új játékot kezd
    - inicializálja a változókat
    - a megadott fájlból betölti a szavakat
      és véletlenszerűen választ egyet közülük,
      míg olyat nem választ, ami még nem volt feladva.
    """

    def uj(self):
        print("Kezdődjön a játék!\n")
        self.hibak_szama = 0
        self.tippelt_betuk = []

        fh = open(self.fajlnev, "r", encoding="utf-8")
        szavak = fh.readlines()
        fh.close()

        # Új feladványhoz véletlenszerüen választunk egy szót a listáról
        # Az előző feladványokat eltároljuk, így kétszer nem adja fel ugyanazt.
        uj_feladvany = ""
        while uj_feladvany == "":
            uj_feladvany = random.choice(szavak).rstrip()
            if uj_feladvany in self.korabbi_feladvanyok:
                uj_feladvany = ""
        self.korabbi_feladvanyok.append(uj_feladvany)
        self.feladott_szo = uj_feladvany

        # az állást mutató listát készítünk annyi aláhúzás jelből,
        # ahány karakter hosszú a feladott szó
        self.feladvany_allasa = ["_"] * len(self.feladott_szo)

    def intro(self):
        valasztas = input(
            "Üdvözlet az Akasztófa-játékban!\n\nSzeretné elolvasni a szabályokat? [i/n] "
        ).lower()
        if valasztas == "i":
            print(
                "A kitalálandó szót a szóban szereplő betűk számával megegyező "
                "számú és elrendezésű vízszintes vonal reprezentálja. "
                "A találgató játékos javasol egy betűt, mely ha szerepel a kitalálandó "
                "szóban, a betű helyének megfelelő vonalakra ráírásra kerül. "
                "Amennyiben a betű nem szerepel a kitalálandó szóban, úgy egy "
                "stilizált akasztófa egy része kerül lerajzolásra.\n\n"
                "A játék akkor ér véget, ha az akasztófa (és a benne lévő emberalak) "
                "teljes egészében megformálásra kerül, vagy kérdező az összes betűt "
                "kitalálja."
            )

    """
    Bekérünk egy betűt tippnek.
    A következő hibákra figyel:
    - Ha nem csak egy betűt adott meg
    - Ha nem magyar ABC-nek megfelelő betűt adott meg
    - Ha korábban tippelt betűt adott meg.
    Hiba esetén kiüríti a bekért betűt tároló változó értékét,
    és addig ismétli a ciklust, míg nem kap megfelelőt.
    """

    def tipp_bekerese(self):
        betu = ""
        while betu == "":
            betu = input("Tipp: ").lower()
            if len(betu) != 1:
                print("Érvénytelen tipp: csak egy betűt kell megadni!")
                betu = ""
            elif betu not in Akasztofa.ervenyes_betuk:
                print("Érvénytelen tipp: csak a magyar abc betűit tippelheted!")
                betu = ""
            elif betu in self.tippelt_betuk:
                print("Érvénytelen tipp: már tippelted ezt a betűt!")
                betu = ""
        return betu

    """
    Kiírja az állást, és ha az akasztoval paraméter igaz,
    akkor kirajzolja az akasztófát is
    """

    def allas_megjelenitese(self, akasztofaval=True):
        if akasztofaval:
            print(hangmanpics.HANGMANPICS[self.hibak_szama - 1])
        print("A feladvány: ", " ".join(self.feladvany_allasa))
        if len(self.tippelt_betuk):
            print("Ezeket a betűket már tippelte:", ", ".join(self.tippelt_betuk))

    """
    A játék végigjátszása:
    - bekér egy betűt
    - ha szerepel a szóban, frissíti az állást
    - ha nem szerepel, növeli a hibák számát
    - ha vége van a játéknak, kiírja az üzeneteket és a függvény kilép
    """

    def jatek(self):

        # állás megjelenítése az akasztófa nélkül
        self.allas_megjelenitese(akasztofaval=False)

        # ciklus a játék végéig
        vege = False
        while not vege:
            betu = self.tipp_bekerese()
            self.tippelt_betuk.append(betu)

            # vizsgáljuk a találatot
            if betu in self.feladott_szo:
                print("A megadott betű szerepel a szóban!")

                # feladványban kicseréljük az aláhúzást a betűre
                i = 0
                while i < len(self.feladott_szo):
                    if self.feladott_szo[i] == betu:
                        self.feladvany_allasa[i] = betu
                    i += 1

                kitalalando_betuk = 0
                i = 0
                while i < len(self.feladvany_allasa):
                    if self.feladvany_allasa[i] == "_":
                        kitalalando_betuk += 1
                    i += 1

                # ellenőrizzük, hogy megvan-e az összes betű
                if kitalalando_betuk == 0:
                    vege = True

            else:
                print("Sajnos nincs benne a betű a feladott szóban :(")
                self.hibak_szama += 1

                # ellenőrizzük, hogy elfogytak-e az életek
                if self.hibak_szama == 7:
                    vege = True


            self.allas_megjelenitese()

            if vege:
                if self.hibak_szama == 7:
                    print("Sajnos vesztettél!")
                    print(f"A feladvány \"{self.feladott_szo}\" volt")
                else:
                    print("Nyertél!")

    """
    Megkérdezzük a felhasználót, hogy ki akar-e lépni.
    Csak i/n-t fogadunk el.
    """

    def kilep_teszt(self):
        valasztas = ""
        while valasztas == "":
            valasztas = input("Szeretnél mégegyet játszani? [i/n]").lower()
            if valasztas not in ["i", "n"]:
                print("Érvénytelen választás.")
                valasztas = ""  # hibás választásnál kiürítjük a változót, és a while ezt vizsgálja

        # érdekesség: nem előre beállított boolean változó értékével térünk vissza,
        # hanem a logikai kifejezés eredményével
        # igaz, ha a felhasználó a "n"-t választotta.
        return valasztas == "n"
