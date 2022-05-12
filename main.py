from la.lex_analyser import LexicalAnalyser
import sys


def file_to_data(file_path):
    f = open(file_path, "r")
    data = f.read() 
    f.close()
    return data


#first command line argument is tokens file path
#second command line argument is path of file with code to be analysed

#Token file takes tokens and regexes for each line
#Each line must start with the token name, then a space character, and then the regex
#There is also a special entry "literals", that takes single characters
#Example    1:IDENT ident
#           2:FLOAT_CONSTANT [0-9]+.\..[0-9]+
#           3:RELOP (<|>|<=|>=|==)
#           4:literals +-*\=<>:
#
#Every character in the "literals" line will be a separeted token

if __name__ == "__main__":

    [_, token_file, data_file] = sys.argv

    data = file_to_data(data_file)

    la = LexicalAnalyser()
    la.from_file(token_file)
    la.analysis(data)

