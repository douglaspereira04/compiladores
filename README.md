# Analisador Léxico

O programa tem como entrada um arquivo de definição dos tokens e um arquivo de código a ser analisado. Para executar o programa:
```
python3 main.py token_file_path code_file_path
```
No comando, "token_file_path" é o caminho do arquivo com as definições dos tokens e "code_file_path" é o caminho do arquivo com o código a ser analisado.

## Arquivo de tokens
- O arquivo de tokens deve ter em cada uma de suas linha a definição de um token.
- A definição deve iniciar pelo nome do token, depois um caractere de espaço, e então a expressão regular correspondente.
- Também há uma entrada especial "literals, que trata tokens que podem ser representados por um único caractere.
- Todo caractere na definição de literals será um token do mesmo nome do caractere.

Exemplo de conteúdo de um arquivo de tokens:
```
DEF def
RETURN return
IF if
ELSE else
TRUE true
FALSE false
IDENT ([a-z]|[A-Z]|_|[0-9])+
INT [0-9]+
FLOAT [0-9]+.\..[0-9]+
STRING ".*"
RELOP (<|>|<=|>=|==)
BOOLOP (\|\||&&)
literals +-*/=<>(){},;
```
A aceitação dos tokens respeita uma ordem de precedência. Essa ordem é a mesma da definição do aquivo, exceto para a definição dos "literals", que independente de onde que foram inseridos no arquivo, estarão no final da ordem.

## Arquivo de código
Qualquer texto dentro do arquivo será analisado.
Exemplo:
```
def minha_funcao(param1,param2){
	a = 1 *2 / 50 - 300 +12;
	b = a < 50;
	if(b && param1){
		return (param1 || param2);
	} else {
		return true;
	}
}
```


