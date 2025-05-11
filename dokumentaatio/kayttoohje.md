# Käyttöohje
Lataa projektin viimeisimmän releasen lähdekoodi githubista. [Release-linkki](https://github.com/Mrivu/Ohjelmistotekniikka/releases/tag/Final-release)

## Pelin käynnistäminen
Aja seuraava komento ladatussa repositoriossa

```
poetry run invoke start
```

## Pelin ohjeet 
Peli on balatro-inspiroitu noppapeli. Tavoitteena on saavuttaa jokaisen tason asettama tavoite, summaamalla omat nopat.
Kannattaa kerätä monta samaa tulosta, sillä kolme tai enemmän samaa noppaa kasvattaa niiden kerrointa:
```
if amount == 3:
    mul = 1.5
if amount == 4:
    mul = 2
if amount == 5:
    mul = 3
if amount == 6:
    mul = 4
```

### Noppien heitto
Noppia voi heittää uudelleen re-roll napista. Valitse nopat, mitä haluat heittää uudelleen klikkaamalla niitä ja klikkaa sitten re-roll nappia. Jos kuitenkin haluat heittää kaikki nopat uudelleen, voit yksinkertaisesti painaa re-roll nappia valitsematta yhtään noppaa.

### Raha, kauppa ja päivitykset
Jokaisen tason jälkeen, pääset kauppaan jossa voit käyttää rahaa jotka olet ansainnut tasoissa. Rahasi näkyy vasemmassa alakulmassa ja sitä saa tasoista enemmän, kun olet käyttänyt vähemmän re-rolleja ja/tai saanut tarvittua suuremman tuloksen. Kaupasta löytyy staattisia parannuksia, jotka kasvattava re-rollejen määrää, kaupassa näkyvien päivitysten maksimimäärää, kaupassa näkyvien päivitysten harvinaisuutta sekä ostettujen päivitysten maksimia. Voit myös ostaa päivityksiä, jotka antavat bonuksia tai luovat muita mielenkiintoisia käänteitä. Päivityksiä voi myydä milloin tahansa kaupassa ja tieto siitä, mitä ne tekevät löytyy klikkaamalla päivitystä.