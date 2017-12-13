
#main function for comparison between two pokemons with help of pokeapi

import request # import request.py
import sys # import sys for input through command_line_argument
from Exceptions import TooManyArguements #input TooManyArguments from exception.py
def main(argv):
    if len(argv) != 2: # if the number of arguments is not equal to 2, then raise the exception
        raise TooManyArguements("the numbers of arguments should be 2")
    else:
        pokemon1 = request.get_pokemons(argv[0]) #input the first pokemon
        pokemon2 = request.get_pokemons(argv[1]) #input the second pokemon
        sys.stdout.write(pokemon1.comparedTo(pokemon2)) #output the result






if __name__ =="__main__":
    main(sys.argv[1:]) # call the main function in order to output the result