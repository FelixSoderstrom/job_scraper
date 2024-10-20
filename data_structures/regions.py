"""
Unfortunately there are too many inconsistencies in how regions are shown
within the URL on blocket.
Therefore the only option I could think of was key value pairs and write
them all out separately.
At least this makes for easy access and little thinking. Silver lining!

As for the cities,
we can always use set(cities) to allow for faster iteration.
Unfortunately difflib did not support this. Bummer.
Hopefully the user that fucks with us intentionally wont get mad
because of this slight inconvenience!
What am I talking about? I don't get paid for this. I don't care about the user!

That was mean..
I'm sorry user..
Thanks for being here.
You know I love you! <3
"""

län = {
    "blekinge": "blekinge-laen",
    "dalarna": "dalarnas-laen",
    "gotland": "gotlands-laen",
    "gävleborg": "gaevleborgs-laen",
    "halland": "hallands-laen",
    "jämtland": "jaemtlands-laen",
    "jönköping": "joenkoepings-laen",
    "kalmar": "kalmar-laen",
    "kronoberg": "kronobergs-laen",
    "norrbotten": "norrbottens-laen",
    "skåne": "skaane-laen",
    "stockholm": "stockholms-laen",
    "södermanland": "soedermanlands-laen",
    "uppsala": "uppsala-laen",
    "värmland": "vaermlands-laen",
    "västerbotten": "vaesterbottens-laen",
    "västernorrland": "vaesternorrlands-laen",
    "västmanland": "vaestmanlands-laen",
    "västra götaland": "vaestra-goetalands-laen",
    "örebro": "oerebro-laen",
    "östergötland": "oestergoetlands-laen",
}

cities = [
    "karlshamn",
    "kaslskrona",
    "olofström",
    "ronneby",
    "sölvesborg",
    "avesta",
    "boslänge",
    "falun",
    "gangnef",
    "hedemora",
    "leksand",
    "ludvika",
    "malung-sälen",
    "mora",
    "orsa",
    "rättvik",
    "smedjebacken",
    "säter",
    "vansbro",
    "älvedalen",
    "gotland",
    "bollnäs",
    "gävle",
    "hofors",
    "hudviksvall",
    "ljusdal",
    "nordanstig",
    "ockelbo",
    "ovanåker",
    "sandviken",
    "söderhamn",
    "falkenberg",
    "halmstad",
    "hylte",
    "kungsbacka",
    "laholm",
    "varberg",
    "berg",
    "bräcke",
    "härjedalen",
    "krokom",
    "ragunda",
    "strömsund",
    "åre",
    "östersund",
    "aneby",
    "eksjö",
    "gislaved",
    "gnosjö",
    "habo",
    "jönköping",
    "mullsjö",
    "nässjö",
    "sävsjö",
    "tranås",
    "vaggeryd",
    "vetlanda",
    "värnamo",
    "borgholm",
    "emmaboda",
    "hultsfred",
    "högsby",
    "kalmar",
    "mönsterås",
    "mörbylånga",
    "nybro",
    "oskarshamn",
    "torsås",
    "vimmerby",
    "västervik",
    "alvesta",
    "lessebo",
    "ljungby",
    "markaryd",
    "tingsryd",
    "uppvidinge",
    "växjö",
    "älmhult",
    "arjeplog",
    "arvidsjaur",
    "boden",
    "gällivare",
    "haparanda",
    "jokkmokk",
    "kalix",
    "kiruna",
    "luleå",
    "pajala",
    "piteå",
    "älvsbyn",
    "överkalix",
    "övertorneå",
    "bjuv",
    "bromölla",
    "burlöv",
    "båstad",
    "eslöv",
    "helsingborg",
    "hässleholm",
    "höganäs",
    "hörby",
    "höör",
    "klippan",
    "kristianstad",
    "kävlinge",
    "landskrona",
    "lomma",
    "lund",
    "malmö",
    "osby",
    "perstorp",
    "simrishamn",
    "sjöbo",
    "skurup",
    "staffanstorp",
    "svalöv",
    "svedala",
    "tomelilla",
    "trelleborg",
    "vellinge",
    "ystad",
    "ängelholm",
    "åstorp",
    "örkeljunga",
    "östra göinge",
    "botkyrka",
    "danderyd",
    "ekerö",
    "haninge",
    "huddinge",
    "järfälla",
    "lidingö",
    "nacka",
    "norrtälje",
    "nykvarn",
    "nynäshamn",
    "salem",
    "sigtuna",
    "sollentuna",
    "solna",
    "stockholm",
    "sundbyberg",
    "södertälje",
    "tyresö",
    "täby",
    "upplands väsby",
    "upplands-bro",
    "vallentuna",
    "vaxholm",
    "värmdö",
    "österåker",
    "eskilstuna",
    "flen",
    "gnesta",
    "katrineholm",
    "nyköping",
    "oxelösund",
    "strängnäs",
    "trosa",
    "vingåker",
    "enköping",
    "heby",
    "håbo",
    "knivsta",
    "tierp",
    "uppsala",
    "älvkarleby",
    "östhammar",
    "arvika",
    "eda",
    "filipstad",
    "forshaga",
    "grums",
    "hagfors",
    "hammarö",
    "karlstad",
    "kil",
    "kristinehamn",
    "munkfors",
    "storfors",
    "sunne",
    "säffle",
    "torsby",
    "årjäng",
    "bjurholm",
    "dorotea",
    "lycksele",
    "malå",
    "nordmaling",
    "norsjö",
    "robertsfors",
    "skellefteå",
    "sorsele",
    "storuman",
    "umeå",
    "vilhelmina",
    "vindeln",
    "vännäs",
    "åsele",
    "härnösand",
    "kramfors",
    "sollefteå",
    "sundsvall",
    "timrå",
    "ånge",
    "örnsköldsvik",
    "arboga",
    "fagersta",
    "hallstahammar",
    "kungsör",
    "köping",
    "norberg",
    "sala",
    "skinnskatteberg",
    "surahammar",
    "västerås",
    "ale",
    "alingsås",
    "bengtsfors",
    "bollebygd",
    "borås",
    "dals-ed",
    "essunga",
    "falköping",
    "färgelanda",
    "grästorp",
    "gullspång",
    "göteborg",
    "götene",
    "herrljunga",
    "hjo",
    "härryda",
    "karlsborg",
    "kungälv",
    "lerum",
    "lidköping",
    "lilla edet",
    "lysekil",
    "mariestad",
    "mark",
    "mellerud",
    "munkedal",
    "mölndal",
    "orust",
    "partille",
    "skara",
    "skövde",
    "sotenäs",
    "stenungsund",
    "strömstad",
    "svenljunga",
    "tanum",
    "tibro",
    "tidaholm",
    "tjörn",
    "tranemo",
    "trollhättan",
    "töreboda",
    "uddevalla",
    "ulricehamn",
    "vara",
    "vänersborg",
    "vårgårda",
    "åmål",
    "öckerö",
    "askersund",
    "degerfors",
    "hallsberg",
    "hällefors",
    "karlskoga",
    "kumla",
    "laxå",
    "lekeberg",
    "lindesberg",
    "ljusnarsberg",
    "nora",
    "örebro",
    "boxholm",
    "finspång",
    "kinda",
    "linköping",
    "mjölby",
    "motala",
    "norrköping",
    "söderköping",
    "vadstena",
    "valdemarsvik",
    "ydre",
    "åtvidaberg",
    "ödeshög",
]
