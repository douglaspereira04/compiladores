from la.lex_analyser import LexicalAnalyser, LexicalException
import sys


def read_file(file_path):
    f = open(file_path, "r")
    data = f.read() 
    f.close()
    return data

def write_file(file_path, string):
    f = open(file_path, "w")
    f.write(string)
    f.close()


# First command line argument is tokens file path
# Second command line argument is path of file with code to be analysed
# Third command line argument is path of output file
if __name__ == "__main__":
    output_path = None
    token_file = None
    data_file = None

    if(len(sys.argv)==3):
        [_, token_file, data_file] = sys.argv 
    else:
        [_, token_file, data_file, output_path] = sys.argv 

    data = read_file(data_file)

    la = LexicalAnalyser()
    la.from_file(token_file)
    la.input(data)
    
    try:
        while True:
            token = la.token()
            if (not token):
                break #no more tokens
    except LexicalException as e:
        print(e)
    else:
        symbol_table = la.symbol_table
        if(output_path):
            write_file(output_path,symbol_table.to_string())
        else:
            print(symbol_table.to_string())

