1. Säkerhetsaspekter
I min app så har jag inte använt mig av någon api-nyckel utan jag kör SmolLm lokalt. SmolLM laddas ner vid första uppstart och sparas lokalt i cachen. Om jag däremot hade använt mig av API-nycklar så hade jag skyddat dom genom att spara informationen för nycklen i en .env fil. Jag hade sedan lagt till .env i gitignore för att säkerställa att den inte följer in till github.
Konsekvenserna av att pusha upp .env till github kan vara väldigt allvarliga. Har du tex informationen för din API-nyckel i den filen innebär det tex att obehöriga kan komma åt din databas eller llm. På så vis kan den personen tex radera din databas eller utnyttja llm i ditt namn vilket i sin tur kan resultera i att jag får betala för det användandet.
För att säkerställa att det enbart går att ladda upp csv filer, så har jag lagt till logik i koden som kontrollerar att filen har .csv som filtyp. På så sätt så får man ett felmeddelande om man försöker ladda upp en annan filtyp.
Jag har däremot inte gjort någon logik som kontrollerar att innehållet i filen faktiskt har rätt struktur.
Detta hade jag i så fall löst med ett pydantic schema för att validera datan som lästs in från filen.

2. Dataskydd (GDPR)
Så som min tjänst fungerar i dagsläget så körs llm:en lokalt. Den laddas ner första gången appen körs. Det innebär att ingen data skickas över nätet, därav så är hanteringen av personuppgifter inte ett problem. 
Om jag däremot skulle gå live med tjänsten och använda en llm som inte är lokal, hade jag behövt skydda personuppgifter och/eller annan känslig information från att laddas upp. Detta innebär att se till att tex API-nycklar inte följer med upp på github, att känslig information inte hårdkodads samt att datan från csv filer som laddas upp sanitäras innan datan lagras. Det senare kan utföras med förtränade NLP-modeller tex Microsoft's Presidio eller Huggingface privacy filter.

3. AI-risker och ansvar
Små llm:er, såsom den jag använder i appen, når sin gräns väldigt snabbt. Man behöver vara väldigt noggrann med hur stora dataset man laddar upp, samt hur mycket av datan man ger llm:en att jobba med.
Detta var något jag upptäckte när jag gjorde mina första tester för att se responsen från modellen baserat på datasetet jag laddat upp. Jag fick väldigt konstiga svar som många gånger inte alls var relevant till informationen i datasetet.
En annan sak jag märkte var hur viktigt det var att prompta modellen rätt för att begränsa vilken typ av svar man fick tillbaka. På så sätt var svaren bara relevanta för det datasetet som var uppladdat.
När det kommer till bias så är det just nu ett stort problem, och det är att modellen bara ser de 10 första raderna i datasetet. Det riskerar att ge en skev analys beroende på vilken typ av fråga som ställs.
Skulle jag tex fråga vad genomsnitts inkomsten är, så blir den missvisande då modellen bara tar med innehållet från de 10 första raderna.

4. Designval
Det som gör Runnable och | operatorn kraftfullt är att bland annat att ansvaret delas upp på de olika delarna, tex promptbuilder bygger prompten, llm:en genererar svaret osv. Detta bidrar till att varje steg i kedjan kan testas separat.
Koden blir mer lättläst när man delar upp ansvaret på varje del i kedjan. Skulle hela kedjan skrivas i en enda funktion, hade det blivit väldigt rörigt.

