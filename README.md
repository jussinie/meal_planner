# Meal Planner -sovellus

Tässä sovelluksessa käyttäjät voivat luoda itselleen päivittäisen ruokalistan, jonka avulla seurata kalorien ja makroravinteiden saantiaan. Käyttäjä voi luoda reseptejä, jotka ovat näkyvissä muille käyttäjille. Muut käyttäjät voivat arvioida ja kommentoida reseptejä ja lisätä niitä myös omalle ruokalistalleen. Voisi sanoa, että sovelluksen on tarkoitus olla sovellettu versio esimerkkinä annetusta keskustelusovelluksesta.   

## Sovelluksen ominaisuuksia:

Sovellus toimii osoitteessa https://secret-journey-84354.herokuapp.com/
Sovelluksen visuaalinen ilme on vielä melkoisen rustiikkinen, CSS-tyylejä on käytetty vasta asioiden testaamiseen. 

 - Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
   - Käyttäjänimen (username) on oltava uniikki. Muuten tunnuksen luominen ei onnistu. Kentissä ei ole vielä tarkistuksia, vaan pituuden ja iän on oltava integer-muotoista, painon float-muotoista ja sukupuolen tekstimuotoista dataa. Kaikki muut ovat tekstikenttiä. 
 - Käyttäjä voi lisätä itselleen pituuden ja painon sekä aktiivisuustason, jolloin sovellus laskee hänelle painoindeksin sekä päivittäisen kaloritarpeen. 
   - Tämä tapahtuu käyttäjän luomisen yhteydessä. Painon päivitysominaisuutta ei vielä ole. 
 - Käyttäjä näkee listan reseptejä, joita hän voi lisätä omalle ruokalistalleen.
   - Tämä toimii, mutta ruokalista on vain lista lisätyistä ruoista. Tarkoitus on tehdä siitä toiminnallisempi siten, että käyttäjä näkee kuinka paljon "kaloribudjettia" on jäljellä tai kuinka paljon se on jo ylitetty. 
 - Käyttäjä voi luoda reseptejä sovellukseen. 
   - Toimii rajallisesti. Reseptiin on tällä hetkellä mahdollista lisätä vain yksi ainesosa. Paino grammoina tulee antaa int-tyyppisinä arvoina.
 - Käyttäjä voi arvioida reseptejä antamalla niille arvosanan.
   - Tätä toiminnallisuutta ei vielä ole.
 - Käyttäjä voi antaa reseptille myös sanallista palautetta.
   - Kommentointi onnistuu.
 - Käyttäjä voi muokata luomaansa reseptiä 
   - Ei vielä toiminnassa.
 - Käyttäjä voi ehdottaa ruoka-aineita lisättäväksi järjestelmään
   - Tällä hetkellä kaikki "ehdotukset" menevät suoraan tietokantaan. Syötteitä ei tarkisteta. Kalorit ja makroravinteet tulee antaa float-tyyppisinä.
 - Käyttäjä voi etsiä reseptejä sanahaun avulla
   - Ei vielä rakennettuna.
 - Ylläpitäjä voi lisätä järjestelmään ruoka-aineita ja hyväksyä käyttäjien ruoka-aine-ehdotuksia.
   - Käyttäjillä voi olla admin rooli jo nyt, mutta mitään siihen liittyvää toiminnallisuutta ei vielä ole valmiina.

Tämä on alustava määrittely ja voi muuttua/täydentyä jonkin verran kurssin edetessä.

