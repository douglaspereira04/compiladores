# Analisador Léxico

O programa tem como entrada um arquivo de definição dos tokens e um arquivo de código a ser analisado. Para executar o programa:
```
make clean venv
make run token_file_path=my_token_file code_file_path=my_code_file
```
No comando, "token_file_path" deve receber o caminho do arquivo com as definições dos tokens e "code_file_path" deve receber o caminho do arquivo com o código a ser analisado.\
Um terceiro argumento pode ser adicionado, "output", recebendo o caminho para o arquivo de saída, onde será apresentada a tabela de símbolos. Se não definido o caminho, a tabela de símbolos é apresentada no terminal.

## Arquivo de tokens
- O arquivo de tokens deve ter em cada uma de suas linha a definição de um token;
- A definição deve iniciar pelo nome do token, depois um caractere de espaço, e então a expressão regular correspondente;
- Há uma entrada especial "literals, que trata tokens que podem ser representados por um único caractere;
- Todo caractere na definição de literals será um token do mesmo nome do caractere;
- Há uma entrada especial "ignore", que trata dos caracteres que devem ser ignorardos.
- Há também a entrada especial IDENT. Nela devem estar, separados por espaços, quais tokens serão guardados na tabela de símbolos.

Exemplo de conteúdo de um arquivo de tokens:
```
DEF def
RETURN return
IF if
ELSE else
TRUE true
FALSE false
STRING ".*"
FLOAT [\+-]?[0-9]+\.[0-9]+
INT [\+-]?[0-9]+
ID ([a-z]|[A-Z]|[0-9])+([a-z]|[A-Z]|_|[0-9])*
relop <|>|<=|>=|==|!=
BOOLOP (\|\||&&)
literals +-*/=<>(){},;
ignore   	
IDENT ID
```
É importante notar que mesmo a entrada "ignore" aparentar vazia, a linha é composta por "ignore"(sendo o nome da entrada),"espaço"(sendo usado como separador entre nome da entrada e integrantes da entrada),"espaço"(sendo usado como integrante da entrada) e "tabulação".\
**A aceitação dos tokens respeita uma ordem de precedência. Essa ordem é a mesma da definição do aquivo, exceto para a definição dos "literals", que independente de onde que foram inseridos no arquivo, estarão no final da ordem.**\
**O arquivo de texto deve ter aumenos um token não "literals".**

## Arquivo de código
Qualquer texto dentro do arquivo será analisado.\
Exemplo:
```
def minha_funcao(param1,param2){
	a = +1 * -2 / +-50 - 30.0 + 12;
	b = a < 50;
	print("mensagem")
	if(b && param1){
		return (param1 || param2);
	} else {
		return true;
	}
}

```
A saída esperada são duas tabelas, uma com todos os lexemas encontrados, e uma com a tabela de simbolos.
```
╒═════════╤══════════════╤═════════╤═══════════╕
│ TOKEN   │ LEXEMA       │   LINHA │   POSIÇÃO │
╞═════════╪══════════════╪═════════╪═══════════╡
│ DEF     │ def          │       1 │         0 │
├─────────┼──────────────┼─────────┼───────────┤
│ ID      │ minha_funcao │       1 │         4 │
├─────────┼──────────────┼─────────┼───────────┤
│ (       │ (            │       1 │        16 │
├─────────┼──────────────┼─────────┼───────────┤
│ ID      │ param1       │       1 │        17 │
├─────────┼──────────────┼─────────┼───────────┤
│ ,       │ ,            │       1 │        23 │
├─────────┼──────────────┼─────────┼───────────┤
│ ID      │ param2       │       1 │        24 │
├─────────┼──────────────┼─────────┼───────────┤
│ )       │ )            │       1 │        30 │
├─────────┼──────────────┼─────────┼───────────┤
│ {       │ {            │       1 │        31 │
├─────────┼──────────────┼─────────┼───────────┤
│ ID      │ b            │       2 │        34 │
├─────────┼──────────────┼─────────┼───────────┤
│ =       │ =            │       2 │        36 │
├─────────┼──────────────┼─────────┼───────────┤
│ ID      │ a            │       2 │        38 │
├─────────┼──────────────┼─────────┼───────────┤
│ relop   │ <            │       2 │        40 │
├─────────┼──────────────┼─────────┼───────────┤
│ INT     │ 50           │       2 │        42 │
├─────────┼──────────────┼─────────┼───────────┤
│ +       │ +            │       2 │        45 │
├─────────┼──────────────┼─────────┼───────────┤
│ FLOAT   │ 22.2         │       2 │        47 │
├─────────┼──────────────┼─────────┼───────────┤
│ ;       │ ;            │       2 │        51 │
├─────────┼──────────────┼─────────┼───────────┤
│ IF      │ if           │       3 │        54 │
├─────────┼──────────────┼─────────┼───────────┤
│ (       │ (            │       3 │        56 │
├─────────┼──────────────┼─────────┼───────────┤
│ ID      │ b            │       3 │        57 │
├─────────┼──────────────┼─────────┼───────────┤
│ BOOLOP  │ &&           │       3 │        59 │
├─────────┼──────────────┼─────────┼───────────┤
│ ID      │ param1       │       3 │        62 │
├─────────┼──────────────┼─────────┼───────────┤
│ )       │ )            │       3 │        68 │
├─────────┼──────────────┼─────────┼───────────┤
│ {       │ {            │       3 │        69 │
├─────────┼──────────────┼─────────┼───────────┤
│ RETURN  │ return       │       4 │        73 │
├─────────┼──────────────┼─────────┼───────────┤
│ (       │ (            │       4 │        80 │
├─────────┼──────────────┼─────────┼───────────┤
│ ID      │ param1       │       4 │        81 │
├─────────┼──────────────┼─────────┼───────────┤
│ BOOLOP  │ ||           │       4 │        88 │
├─────────┼──────────────┼─────────┼───────────┤
│ ID      │ param2       │       4 │        91 │
├─────────┼──────────────┼─────────┼───────────┤
│ )       │ )            │       4 │        97 │
├─────────┼──────────────┼─────────┼───────────┤
│ ;       │ ;            │       4 │        98 │
├─────────┼──────────────┼─────────┼───────────┤
│ }       │ }            │       5 │       101 │
├─────────┼──────────────┼─────────┼───────────┤
│ }       │ }            │       6 │       103 │
╘═════════╧══════════════╧═════════╧═══════════╛
╒══════════════╤═════════════════════════════╕
│ LEXEMA       │ POSIÇÕES                    │
╞══════════════╪═════════════════════════════╡
│ minha_funcao │ [(1, 4)]                    │
├──────────────┼─────────────────────────────┤
│ param1       │ [(1, 17), (3, 62), (4, 81)] │
├──────────────┼─────────────────────────────┤
│ param2       │ [(1, 24), (4, 91)]          │
├──────────────┼─────────────────────────────┤
│ b            │ [(2, 34), (3, 57)]          │
├──────────────┼─────────────────────────────┤
│ a            │ [(2, 38)]                   │
╘══════════════╧═════════════════════════════╛


```
No caso de uma entrada com um erro léxico, uma mensagem de erro aparecerá no terminal.\
Exemplo:
```
Illegal character § at pos 78, line 3
```
