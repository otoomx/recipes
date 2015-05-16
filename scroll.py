from  elasticsearch import Elasticsearch, helpers

es = Elasticsearch(['http://192.168.1.5'])


style_map = {
  "34":"American Amber Ale",
  "73":"American Barleywine",
  "35":"American Brown Ale",
  "49":"American IPA",
  "33":"American Pale Ale",
  "46":"American Stout",
  "21":"American Wheat or Rye Beer",
  "41":"Baltic Porter",
  "66":"Belgian Blond Ale",
  "70":"Belgian Dark Strong Ale",
  "67":"Belgian Dubbel",
  "69":"Belgian Golden Strong Ale",
  "56":"Belgian Pale Ale",
  "59":"Belgian Specialty Ale",
  "68":"Belgian Tripel",
  "60":"Berliner Weisse",
  "58":"Biere de Garde",
  "19":"Blonde Ale",
  "7":"Bohemian Pilsener",
  "39":"Brown Porter",
  "23":"California Common Beer",
  "76":"Christmas/Winter Specialty Spiced Beer",
  "8":"Classic American Pilsner",
  "77":"Classic Rauchbier",
  "18":"Cream Ale",
  "11":"Dark American Lager",
  "16":"Doppelbock",
  "5":"Dortmunder Export",
  "42":"Dry Stout",
  "52":"Dunkelweizen",
  "24":"Dusseldorf Altbier",
  "17":"Eisbock",
  "72":"English Barleywine",
  "48":"English IPA",
  "27":"Extra Special/Strong Bitter (English Pale Ale)",
  "62":"Flanders Brown Ale/Oud Bruin",
  "61":"Flanders Red Ale",
  "45":"Foreign Extra Stout",
  "74":"Fruit Beer",
  "65":"Fruit Lambic",
  "6":"German Pilsner (Pils)",
  "64":"Gueuze",
  "50":"Imperial IPA",
  "31":"Irish Red Ale",
  "20":"Kolsch",
  "1":"Lite American Lager",
  "14":"Maibock/Helles Bock",
  "36":"Mild",
  "12":"Munich Dunkel",
  "4":"Munich Helles",
  "38":"Northern English Brown Ale",
  "22":"Northern German Altbier",
  "44":"Oatmeal Stout",
  "10":"Oktoberfest/Marzen",
  "71":"Old Ale",
  "78":"Other Smoked Beer",
  "3":"Premium American Lager",
  "40":"Robust Porter",
  "54":"Roggenbier (German Rye Beer)",
  "47":"Russian Imperial Stout",
  "57":"Saison",
  "13":"Schwarzbier (Black Beer)",
  "30":"Scottish Export 80/-",
  "29":"Scottish Heavy 70/-",
  "28":"Scottish Light 60/-",
  "37":"Southern English Brown",
  "26":"Special/Best/Premium Bitter",
  "80":"Specialty Beer",
  "75":"Spice, Herb, or Vegetable Beer",
  "2":"Standard American Lager",
  "25":"Standard/Ordinary Bitter",
  "63":"Straight (Unblended) Lambic",
  "32":"Strong Scotch Ale",
  "43":"Sweet Stout",
  "15":"Traditional Bock",
  "9":"Vienna Lager",
  "53":"Weizenbock",
  "51":"Weizen/Weissbier",
  "55":"Witbier",
  "79":"Wood-Aged Beer"}



# Initialize the scroll
page = es.search(
  index = 'recipes',
  doc_type = 'recipe',
  scroll = '2m',
  search_type = 'scan',
  size = 1000,
  body = {
    # Your query's body
    })
sid = page['_scroll_id']
scroll_size = page['hits']['total']
  
  # Start scrolling
while (scroll_size > 0):

    print "Scrolling..."
    page = es.scroll(scroll_id = sid, scroll = '2m')
    # Update the scroll ID
    sid = page['_scroll_id']
    # Get the number of results that we returned in the last scroll
    scroll_size = len(page['hits']['hits'])
    print "scroll size: " + str(scroll_size)
    
    bulk_actions = []

    for hit in page['hits']['hits']:

      source = hit['_source']
      source['style'] = style_map.get(str(hit['_source']['style_id']), None)
      print style_map.get(str(hit['_source']['style_id']), None)
      # action = {
      #   "_index": "rescipes",
      #   "_type": "recipe",
      #   "_id": hit['_id'],
      #   '_opt_type':'update',
      #   "doc": {
      #       "style":style_map.get(str(hit['_source']['style_id']), None)
      #       }
      # }

      res = es.update( index = 'recipes',id=hit['_id'],doc_type='recipe', body= {"doc": {
            "style":style_map.get(str(hit['_source']['style_id']), None)
            }})
      print res


    # Do something with the obtained page