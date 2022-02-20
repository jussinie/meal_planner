# Meal Planner -sovellus

Tässä sovelluksessa käyttäjät voivat luoda itselleen ruokalistan, jonka avulla seurata kalorien ja makroravinteiden saantiaan. Käyttäjä voi luoda reseptejä, jotka ovat näkyvissä muille käyttäjille. Muut käyttäjät voivat arvioida ja kommentoida reseptejä ja lisätä niitä myös omalle ruokalistalleen. Voisi sanoa, että sovelluksen on tarkoitus olla sovellettu versio esimerkkinä annetusta keskustelusovelluksesta.   

## Testaamisesta

Sovellus toimii osoitteessa https://secret-journey-84354.herokuapp.com/.
Mikäli käyttäjän lisääminen ei toimi, sovellusta voi testata tunnuksilla adminmies / adminmies.
Sovelluksen visuaalinen ilme on *edelleenkin* melkoisen rustiikkinen, CSS-tyylejä on käytetty asioiden testaamiseen eikä ulkoasua ole vielä hiottu. 
Valitettavasti en päässyt tässä palautuksessa niin pitkälle kuin toivoin, joten loppupalautukseen hiomista jäi hieman enemmän. 

## Sovelluksen ominaisuuksia:

 - Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
   - Käyttäjänimen (username) on oltava uniikki. Muuten tunnuksen luominen ei onnistu. Kenttien tarkistus on vielä tekemättä - pituuden ja iän on oltava integer-muotoista, painon float-muotoista ja sukupuolen tekstimuotoista dataa. Kaikki muut ovat tekstikenttiä. 
 - Käyttäjä voi lisätä itselleen pituuden ja painon sekä aktiivisuustason, jolloin sovellus laskee hänelle painoindeksin sekä päivittäisen kaloritarpeen. 
   - Tämä tapahtuu käyttäjän luomisen yhteydessä. Painon päivitysominaisuutta ja painoindeksin laskentaa ei ole vielä. 
 - Käyttäjä näkee listan reseptejä, joita hän voi lisätä omalle ruokalistalleen.
 - Käyttäjä voi luoda reseptejä sovellukseen. 
   - Paino grammoina tulee antaa int-tyyppisinä arvoina. Syötteiden tarkistusta ei vielä ole. 
 - Käyttäjä voi antaa reseptille sanallista palautetta.
   - Kommentointi onnistuu.
 - Käyttäjä voi muokata luomaansa reseptiä 
   - Ei vielä toiminnassa.
 - Käyttäjä voi ehdottaa ruoka-aineita lisättäväksi järjestelmään
    - Admin-käyttäjän on hyväksyttävä käyttäjien ehdottamat ruoka-aineet. 
 - Käyttäjä voi etsiä reseptejä sanahaun avulla
   - Ei vielä rakennettuna.
 - Ylläpitäjän oikeudet ovat muuten samanlaiset kuin normaalikäyttäjän, mutta hänen on hyväksyttävä käyttäjien ruoka-aine-ehdotuksia.

Nämä alkavat olla lopulliset featuret, mutta määrittely voi muuttua/täydentyä jonkin verran ennen lopullista palautusta.

