# Meal Planner -sovellus

Tässä sovelluksessa käyttäjät voivat luoda itselleen ruokalistan, jonka avulla seurata kalorien ja makroravinteiden saantiaan. Käyttäjä voi luoda reseptejä, jotka ovat näkyvissä muille käyttäjille. Muut käyttäjät voivat arvioida ja kommentoida reseptejä ja lisätä niitä myös omalle ruokalistalleen. Voisi sanoa, että sovelluksen on tarkoitus olla sovellettu versio esimerkkinä annetusta keskustelusovelluksesta.   

## Testaamisesta

Sovellus toimii osoitteessa https://secret-journey-84354.herokuapp.com/.
Mikäli käyttäjän lisääminen ei toimi, sovellusta voi testata tunnuksilla adminmies / adminmies.
Huom! Kaikki luodut käyttäjät saavat tässä vaiheessa automaattisesti admin-roolin, eli ainesosien hyväksyminen / hylkääminen on mahdollista.

## Sovelluksen ominaisuuksia:

 - Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
   - Käyttäjänimen (username) on oltava uniikki. Muuten tunnuksen luominen ei onnistu. 
 - Käyttäjä voi lisätä itselleen pituuden ja painon, jolloin sovellus laskee hänelle päivittäisen kaloritarpeen. 
   - Tämä tapahtuu käyttäjän luomisen yhteydessä. 
 - Käyttäjä näkee Recipes-sivulta listan reseptejä, joita hän voi lisätä omalle ruokalistalleen.
 - Käyttäjä voi luoda reseptejä sovellukseen.  
 - Käyttäjä voi antaa reseptille sanallista palautetta.
 - Käyttäjä voi ehdottaa ruoka-aineita lisättäväksi järjestelmään
    - Admin-käyttäjän on hyväksyttävä käyttäjien ehdottamat ruoka-aineet. 
 - Käyttäjä voi etsiä reseptejä sanahaun avulla
    - Sanahaku ei ole aivan Googlen veroinen
 - Ylläpitäjän oikeudet ovat muuten samanlaiset kuin normaalikäyttäjän, mutta hän voi hyväksyä / hylätä käyttäjien ruoka-aine-ehdotuksia.
