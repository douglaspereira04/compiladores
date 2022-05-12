from la.lex_analyser import LexicalAnalyser
import sys


def file_to_data(file_path):
    f = open(file_path, "r")
    data = f.read() 
    f.close()
    return data


# First command line argument is tokens file path
# Second command line argument is path of file with code to be analysed
if __name__ == "__main__":
    [_, token_file, data_file] = sys.argv

    data = file_to_data(data_file)

    la = LexicalAnalyser()
    la.from_file(token_file)
    la.input(data)
    while True:
        token = la.token()
        if not token:
            break #no more tokens

    symbol_table = la.symbol_table
    print(symbol_table.to_string())

