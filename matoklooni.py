#! -*- coding:utf8 -*-

from time import sleep
from random import randint
from sense_hat import SenseHat


# globaalit
Tila = 'valikko'


class Omena:
    def __init__(self):
        self.sijainti = (1,1)
        self.varitys = (200, 10, 15)
    def piirra(self):
        sense.set_pixel(self.sijainti[0],self.sijainti[1], self.varitys)
    def siirra(self):
        self.sijainti = (randint(0,7),randint(0,7))

# Määritellään mato
class Mato:
    def __init__(self):
        self.pisteet = 0
        self.liikkeet = 0
        self.pelataan = True
        self.suunta = (0,-1)              # ylös
        self.varitys = (0, 200, 10)       # vihertävä
        self.solut = [(3,7),(3,6),(3,5)]  # madon palat
    def piirra(self):
        for s in self.solut:
            sense.set_pixel(s[0],s[1], self.varitys)
    def putsaa(self):
        # poistetaan vanhin
        self.solut.pop(0)
    def liiku(self):
        # Otetaan nykyinen sijainti
        x,y = self.solut[-1]
        # Lasketaan siirtymä suunnan avulla
        siirry = (x + self.suunta[0], y + self.suunta[1])
        # Osuttiin itseen
        if siirry in self.solut:
            self.pelataan = False
        # lopuksi uusi lisätää appendilla:
        self.solut.append(siirry)
        # statistiikkaa:
        self.liikkeet += 1

# suunta ohjaukset matoon
def suunta_ylos(event):
    global Tila
    if Tila == 'valikko':
        return
    # Nykyinen sijainti
    x,y = mato.solut[-1]
    if y < 0:
        mato.pelataan = False
    elif event.action == 'pressed':
        # Suunta ei saa olla alas kun mennään ylös
        if mato.suunta != (0,1):
            mato.suunta = (0,-1)
    print(event)

def suunta_alas(event):
    global Tila
    if Tila == 'valikko':
        return
    # Nykyinen sijainti
    x,y = mato.solut[-1]
    if y > 7:
        mato.pelataan = False
    elif event.action == 'pressed':
        # Suunta ei saa olla alas kun mennään ylös
        if mato.suunta != (0,-1):
            mato.suunta = (0,1)
    print(event)

def suunta_vasen(event):
    global Tila
    if Tila == 'valikko':
        return
    # Nykyinen sijainti
    x,y = mato.solut[-1]
    if x < 0:
        mato.pelataan = False
    elif event.action == 'pressed':
        # Suunta ei saa olla alas kun mennään ylös
        if mato.suunta != (1,0):
            mato.suunta = (-1,0)
    print(event)

def suunta_oikea(event):
    global Tila
    if Tila == 'valikko':
        return
    # Nykyinen sijainti
    x,y = mato.solut[-1]
    if x > 7:
        mato.pelataan = False
    elif event.action == 'pressed':
        # Suunta ei saa olla alas kun mennään ylös
        if mato.suunta != (-1,0):
            mato.suunta = (1,0)
    print(event)

def startti(event):
    global Tila
    if Tila == 'pelissa':
        return
    # Vaihdetaan tila:
    Tila = 'pelissa'

# Peliskyli omana funktiona
def pelataan():
    # Tarkistus ja siirtymä
    mato.liiku()
    # refernssiksi uusi sijainti:
    mx,my = mato.solut[-1]
    # mentiin yli x akselilla
    if mx < 0 or mx > 7:
        mato.pelataan = False
    # mentiin yli y akselilla
    if my < 0 or my > 7:
        mato.pelataan = False
    # Osutaan omenaan
    if (mx,my) == omena.sijainti:
        mato.pisteet += 1
        omena.siirra()
    # jos saatiin omena, ei putsata häntää
    else:
        # Pitää hännän kurissa
        mato.putsaa()
    return mato.pelataan

def valikko():
    global Tila
    while True:
        if Tila == 'pelissa':
            peli()
            Tila = 'valikko'
        else:
            sense.show_message('valmis', text_colour=(10, 180, 10))

def alusta_peli():
    # luodaan mato ja omena
    global mato
    global omena
    mato = Mato()
    omena = Omena()

# pelin sykli omana funktiona koska halutaan valikko
def peli():
    # Nollataan ruutu aluksi
    sense.clear(musta)
    # luodaan uudelleen oliot
    alusta_peli()
    while pelataan():      # pelifunktio kunnes ei pelata
        if mato.pelataan is False:
            break          # poistutaan while loopista
        mato.piirra()      # piirretään mato
        omena.piirra()     # piirretään omena
        sleep(0.25)        # odotetaan 1/4 osa sekuntia
        sense.clear(musta) # nollataan ruutu jälleen

    # lopputeksti vierivänä viestinä.
    msg = "Peli ohi. P:"+str(mato.pisteet)+", L:"+str(mato.liikkeet)
    sense.show_message(msg, text_colour=(randint(0,255), randint(0,255), randint(0,255)))


# Luodaan viite ledeihin ja sensehat piiriin
sense = SenseHat()

# Määritellään mustan väri
musta = (0, 0, 0)

# luodaan linkitykset painikkeisiin ja madon funktioihin
sense.stick.direction_up = suunta_ylos
sense.stick.direction_down = suunta_alas
sense.stick.direction_left = suunta_vasen
sense.stick.direction_right = suunta_oikea
sense.stick.direction_middle = startti

# luodaan oliot alkuun
mato = Mato()
omena = Omena()

# Käynnistetään valikko
valikko()
