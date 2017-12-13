import requests # import the requests to gather the data from pokiapi
import json #import json to decode
from Exceptions import RequestError #import ReqestError from Exceptions


CLASS = ['id','name','types','stats'] # the information we need to make the comparison happen

# the following function is to make sure we get the data of the pokemon
def get_pokemons(id,url  = 'http://pokeapi.co/api/v2/pokemon'):
   pokemon1 = pokemon() # new pokemon objects
   if isinstance(id,int): # check if the user input is name or id ,if it is id(int), then convert it into string
       id = str(id)
   elif isinstance(id,str):# if the user input the name, change it into lower case
       id = id.lower()
   seq = [url,id]
   new_url = '/'.join(seq) # combine the user input with url to create url (which we want)
   response = requests.get(new_url)# get the data of this pokemon
   if response.status_code == 200: # if the url is right and this pokemon does exist ,processing...
        text = json.loads(response.text) # decode
        for name in text:  # go through the information and find the information wewant

            if name in CLASS: # if we find the information we find, do following
                if name == 'types': # gather all the types of this pokemon (list)
                    typelist = []
                    for index in range(0, len(text[name])):
                        typelist.append(text[name][index]['type']['name'])
                    setattr(pokemon1, name, typelist)
                elif name == 'stats': #gather all the information of this pokemon stats (dict)
                    dict = {}
                    for index in range(0,len(text[name])):
                        base_stats = text[name][index]['base_stat']
                        statsname = text[name][index]['stat']['name']
                        dict[statsname] = base_stats
                        setattr(pokemon1, name, dict)
                else:
                    setattr(pokemon1, name, text[name])# set the pokemone's id and name (str and int)
        return pokemon1
   else:
       raise RequestError(str(response.status_code))# if the status code is not 200, raise the exception

#the following function is to find which types that this pokemon ( parameter, list of types ) is super effective against
def getEffectiveType(listtype,url = 'http://pokeapi.co/api/v2/type'):
    list = []#initalize a list to store data
    for type in listtype: # for each type that this pokemon possess, do following
        seq = [url,type]
        new_url = '/'.join(seq)
        response = requests.get(new_url) # gather the information of this type
        if response.status_code == 200: # if the url is right
            text = json.loads(response.text) # decode
            for index in range(0,len(text['damage_relations']['double_damage_to'])): #find the types and store them in the list
                Effective_Type = text['damage_relations']['double_damage_to'][index]['name']
                if Effective_Type not in list:  # make sure it is a new type , we don't need replication
                    list.append(Effective_Type)



        else:
            raise RequestError(str(response.status_code)) # if the url is not right then raise the exception
    return list

# the following defines pokemone(object)
class pokemon:
    # constructor for pokemon
    def __init__(self,id = 0,name = None,types = None,basestats = None):
        self.id = id
        self.name = name
        self.types = types
        self.stats = basestats
    #comparision function
    def comparedTo(self,other):
        superEffective1 = False # boolean value if first pokemon's type counter second pokemon's type
        superEffective2 = False # boolean value if second pokemon's type counter first pokemon's type
        list1 = getEffectiveType(self.types) # gather information of the type
        for type in other.types: # go through the second pokemon's types
            if type in list1:
                superEffective1 = True #if there is a type that first pokemon posses is supeeffective against second one, change superEffective1 into true
        list2 = getEffectiveType(other.types) #gather information of the type
        for type in self.types: # go through the first pokemon's types
            if type in list2:
                superEffective2 = True #if there is a type that second pokemon posses is supeeffective against first one, change superEffective2 into true
        if (superEffective2 == True & superEffective1 == True) or (superEffective2 == False & superEffective1 == False) : #if both of them are supereffective against each other, compare their stats or both of them are not supereffective,compare their stats
            Pokemon1_stat = 0
            Pokemon2_stat = 0
            # go through both pokemon stats(dict), and add all the values up to get total
            for value in self.stats.values():
                Pokemon1_stat = Pokemon1_stat + value
            for value2 in other.stats.values():
                Pokemon2_stat = Pokemon2_stat + value2
            if Pokemon1_stat > Pokemon2_stat:
                return self.name
            elif Pokemon2_stat > Pokemon1_stat:
                return other.name
            else:
                return self.name


        elif (superEffective1 == True): # if first one is super effective ,return first's name
            return self.name
        elif (superEffective2 == True): # if second one is super effective ,return first's name
            return other.name





