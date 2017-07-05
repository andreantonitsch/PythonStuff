from urllib import request as r
from urllib import parse as p
from html.parser import HTMLParser
import json
import os

class RecipeFetcher(HTMLParser):
    def __init__(self, recipe_list, url_list):
        HTMLParser.__init__(self)
        self.found = 0
        self.list_result = 0
        self.results = 0
        self.recipe_list = recipe_list
        self.url_list = url_list
        self.data_list = []
        
    #def handle_comment(self, data):
    #	if " searchResults index:0 count:" in data:
    #		 self.found += 1
        
    def handle_starttag(self, tag, attrs):
        if tag == 'div' and attrs and  attrs[0][0] == 'class' and attrs[0][1] == 'o-ResultCard__m-MediaBlock m-MediaBlock':
            self.found = 1
        if tag == "a":
                get_next_button = False
                for name, value in attrs:
                    if name == "href" and self.found > 0:
                        if "http://www.foodnetwork.com/recipes/" in value and value not in self.data_list:
                            self.url_list.append(value)
                    
                    if get_next_button and name == "href": 
                        self.recipe_list.append(value)
                    
                    if name == "class" and value == "o-Pagination__a-Button o-Pagination__a-NextButton":
                        get_next_button = True
                

    def handle_endtag(self, tag):
        if tag == 'div':
            self.found = 0

    def handle_data(self, data):
        pass


class RecipeParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)

        self.recipe = {}

        self.ingredients = {}
        self.directions = {}

        self.key = ''		
        self.datawrite = False

        self.namefound = False

        # time
        self.timefound = False


        # yield
        self.yieldfound = False

        # level
        self.levelfound = False

        # ingredients
        self.ingredientsfound = False
        self.ingredientssection = False
        self.ingredientssection_name = False

        self.ingredients_section_key = 'General'

        # directions
        self.directionssection_name = False
        self.directions_section_key = 'General'
        self.directionsfound = False

    #def handle_comment(self, data):
    def clear(self):
        self.recipe = {}

        self.ingredients = {}
        self.directions = {}

        self.key = ''		
        self.datawrite = False

        self.namefound = False

        # time
        self.timefound = False


        # yield
        self.yieldfound = False

        # level
        self.levelfound = False

        # ingredients
        self.ingredientsfound = False
        self.ingredientssection = False
        self.ingredientssection_name = False

        self.ingredients_section_key = 'General'

        # directions
        self.directionssection_name = False
        self.directions_section_key = 'General'
        self.directionsfound = False
        
    def handle_starttag(self, tag, attrs):
        if tag == 'span' and attrs and  attrs[0][0] == 'class' and attrs[0][1] == 'o-AssetTitle__a-HeadlineText':
            self.namefound = True
            self.key = 'name'
            self.datawrite = True

        # time section
        if tag == 'section' and attrs and attrs[0][0] == 'class' and attrs[0][1] =="o-RecipeInfo o-Time":
            self.timefound = True
            
        if self.timefound and tag == 'dd' and attrs and  attrs[0][0] == 'class' and attrs[0][1] == 'o-RecipeInfo__a-Description--Total':
            self.key = 'totaltime'
            self.datawrite = True
        if self.timefound and tag == 'dd' and attrs and  attrs[0][0] == 'class' and attrs[0][1] == 'o-RecipeInfo__a-Description':
            self.key = 'activetime'
            self.datawrite = True

        # yield
        if tag == 'section' and attrs and attrs[0][0] == 'class' and attrs[0][1] == 'o-RecipeInfo o-Yield':
            self.yieldfound = True
        if self.yieldfound and tag == 'dd' and attrs and  attrs[0][0] == 'class' and attrs[0][1] == 'o-RecipeInfo__a-Description':
            self.key = 'yield'
            self.datawrite = True

        # ingredients
        if tag == 'div' and attrs and attrs[0][0] == 'class' and attrs[0][1] == 'o-Ingredients__m-Body':
            self.ingredientsfound = True
        if self.ingredientsfound and tag == 'h6' and attrs and attrs[0][0] == 'class' and attrs[0][1] == 'o-Ingredients__a-SubHeadline':
            self.ingredientssection_name = True

        if self.ingredientsfound and tag == 'label' and attrs and attrs[0][0] == 'class' and attrs[0][1] == 'o-Ingredients__a-ListItemText':
            self.datawrite = True
            
        # directions
        if tag == 'span' and attrs and attrs[0][0] == 'class' and attrs[0][1] == 'm-Directions__a-HeadlineText':
            self.directionssection_name = True
        if tag == 'span' and attrs and attrs[0][0] == 'class' and attrs[0][1] == 'm-Directions__a-HeadlineText':
            self.directionssection_name = True
        if tag == 'div' and attrs and attrs[0][0] == 'class' and attrs[0][1] == 'o-Method__m-Body':
            self.directionsfound = True
        if self.directionsfound and tag == 'p':
            self.datawrite = True

    def handle_endtag(self, tag):
        if tag == 'span':
            self.namefound = False
        elif tag == 'section':
            self.timefound = False
            self.levelfound = False
            self.yieldfound = False
        elif tag == 'div':
            self.ingredientsfound = False
            self.directionsfound = False
        elif tag == 'ul':
            self.ingredientssection = False
            self.ingredients_section_key = 'General'
        elif tag == 'h3':
            self.directions_section_key = 'General'


    def handle_data(self, data):
        
        if self.datawrite and not (self.ingredientsfound or self.directionsfound):
            data = data.replace('\\n', '')
            data = data.replace('\\xc2', '')
            data = data.replace('\\xa0', '')
            self.recipe[self.key] = data.strip()
            self.datawrite = False

        if self.ingredientssection_name:
            data = data.replace('\\n', '')
            data = data.replace('\\xc2', '')
            data = data.replace('\\xa0', '')
            self.ingredients[data.strip().replace(':','')] =  []
            self.ingredients_section_key = data.strip().replace(':','')
            self.ingredientssection_name  = False

        if self.directionssection_name:
            data = data.replace('\\n', '')
            data = data.replace('\\xc2', '')
            data = data.replace('\\xa0', '')
            self.directions[data.strip().replace(':','')] =  []
            self.directions_section_key = data.strip().replace(':','')
            self.directionssection_name  = False

        if self.datawrite and self.ingredientsfound:
            data = data.replace('\\n', '')
            data = data.replace('\\xc2', '')
            data = data.replace('\\xa0', '')
            if self.ingredients_section_key not in self.ingredients.keys():
                self.ingredients[self.ingredients_section_key] = []
            self.ingredients[self.ingredients_section_key].append(data.replace(':','').strip())
            self.datawrite = False

        if self.datawrite and self.directionsfound:
            data = data.replace('\\n', '')
            data = data.replace('\\xc2', '')
            data = data.replace('\\xa0', '')
            if self.directions_section_key not in self.directions.keys():
                self.directions[self.directions_section_key] = []
            self.directions[self.directions_section_key].append(data.strip())
            self.datawrite = False

query = 'cheesecake'
url_list = ['http://www.foodnetwork.com/search/' + query + '-']
recipe_list = []
parser  = RecipeFetcher(url_list, recipe_list)
recipeparser = RecipeParser()
recipe_counter = 0
try:
    os.mkdir('./recipes/'+ query)
except:
    pass

while url_list:
    while url_list and len(recipe_list) < 100:
        url = url_list.pop(0)
        data = r.urlopen(url)
        html =  data.read()
        parser.feed(str(html))
        print('loaded: ' + url)

    print('URLs loaded')

    
    while recipe_list:
        #try:
        url = recipe_list.pop(0)
        print('parsing: ' + url)
        data = r.urlopen(url)
        html =  data.read()
        recipeparser.clear()
        recipeparser.feed(str(html))
        recipe = {}
        recipe['info'] = recipeparser.recipe
        recipe['ingredients'] = recipeparser.ingredients
        recipe['directions'] = recipeparser.directions
        
        to_text = json.dumps(recipe)

        f = open('./recipes/'+ query + '/' + query +str(recipe_counter)+'.json', 'w')
        
        f.write(to_text)
        f.close()
        recipe_counter +=1
       # except:
       #     print(url, ' not found.')
