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
│ ID      │ a            │       2 │        34 │
├─────────┼──────────────┼─────────┼───────────┤
│ =       │ =            │       2 │        36 │
├─────────┼──────────────┼─────────┼───────────┤
│ INT     │ +1           │       2 │        38 │
├─────────┼──────────────┼─────────┼───────────┤
│ *       │ *            │       2 │        41 │
├─────────┼──────────────┼─────────┼───────────┤
│ INT     │ -2           │       2 │        43 │
├─────────┼──────────────┼─────────┼───────────┤
│ /       │ /            │       2 │        46 │
├─────────┼──────────────┼─────────┼───────────┤
│ +       │ +            │       2 │        48 │
├─────────┼──────────────┼─────────┼───────────┤
│ INT     │ -50          │       2 │        49 │
├─────────┼──────────────┼─────────┼───────────┤
│ -       │ -            │       2 │        53 │
├─────────┼──────────────┼─────────┼───────────┤
│ FLOAT   │ 30.0         │       2 │        55 │
├─────────┼──────────────┼─────────┼───────────┤
│ +       │ +            │       2 │        60 │
├─────────┼──────────────┼─────────┼───────────┤
│ INT     │ 12           │       2 │        62 │
├─────────┼──────────────┼─────────┼───────────┤
│ ;       │ ;            │       2 │        64 │
├─────────┼──────────────┼─────────┼───────────┤
│ ID      │ b            │       3 │        67 │
├─────────┼──────────────┼─────────┼───────────┤
│ =       │ =            │       3 │        69 │
├─────────┼──────────────┼─────────┼───────────┤
│ ID      │ a            │       3 │        71 │
├─────────┼──────────────┼─────────┼───────────┤
│ relop   │ <            │       3 │        73 │
├─────────┼──────────────┼─────────┼───────────┤
│ INT     │ 50           │       3 │        75 │
├─────────┼──────────────┼─────────┼───────────┤
│ ;       │ ;            │       3 │        77 │
├─────────┼──────────────┼─────────┼───────────┤
│ ID      │ print        │       4 │        80 │
├─────────┼──────────────┼─────────┼───────────┤
│ (       │ (            │       4 │        85 │
├─────────┼──────────────┼─────────┼───────────┤
│ STRING  │ "mensagem"   │       4 │        86 │
├─────────┼──────────────┼─────────┼───────────┤
│ )       │ )            │       4 │        96 │
├─────────┼──────────────┼─────────┼───────────┤
│ IF      │ if           │       5 │        99 │
├─────────┼──────────────┼─────────┼───────────┤
│ (       │ (            │       5 │       101 │
├─────────┼──────────────┼─────────┼───────────┤
│ ID      │ b            │       5 │       102 │
├─────────┼──────────────┼─────────┼───────────┤
│ BOOLOP  │ &&           │       5 │       104 │
├─────────┼──────────────┼─────────┼───────────┤
│ ID      │ param1       │       5 │       107 │
├─────────┼──────────────┼─────────┼───────────┤
│ )       │ )            │       5 │       113 │
├─────────┼──────────────┼─────────┼───────────┤
│ {       │ {            │       5 │       114 │
├─────────┼──────────────┼─────────┼───────────┤
│ RETURN  │ return       │       6 │       118 │
├─────────┼──────────────┼─────────┼───────────┤
│ (       │ (            │       6 │       125 │
├─────────┼──────────────┼─────────┼───────────┤
│ ID      │ param1       │       6 │       126 │
├─────────┼──────────────┼─────────┼───────────┤
│ BOOLOP  │ ||           │       6 │       133 │
├─────────┼──────────────┼─────────┼───────────┤
│ ID      │ param2       │       6 │       136 │
├─────────┼──────────────┼─────────┼───────────┤
│ )       │ )            │       6 │       142 │
├─────────┼──────────────┼─────────┼───────────┤
│ ;       │ ;            │       6 │       143 │
├─────────┼──────────────┼─────────┼───────────┤
│ }       │ }            │       7 │       146 │
├─────────┼──────────────┼─────────┼───────────┤
│ ELSE    │ else         │       7 │       148 │
├─────────┼──────────────┼─────────┼───────────┤
│ {       │ {            │       7 │       153 │
├─────────┼──────────────┼─────────┼───────────┤
│ RETURN  │ return       │       8 │       157 │
├─────────┼──────────────┼─────────┼───────────┤
│ TRUE    │ true         │       8 │       164 │
├─────────┼──────────────┼─────────┼───────────┤
│ ;       │ ;            │       8 │       168 │
├─────────┼──────────────┼─────────┼───────────┤
│ }       │ }            │       9 │       171 │
├─────────┼──────────────┼─────────┼───────────┤
│ }       │ }            │      10 │       173 │
╘═════════╧══════════════╧═════════╧═══════════╛
╒══════════════╤═══════════════════════════════╕
│ LEXEMA       │ POSIÇÕES                      │
╞══════════════╪═══════════════════════════════╡
│ minha_funcao │ [(1, 4)]                      │
├──────────────┼───────────────────────────────┤
│ param1       │ [(1, 17), (5, 107), (6, 126)] │
├──────────────┼───────────────────────────────┤
│ param2       │ [(1, 24), (6, 136)]           │
├──────────────┼───────────────────────────────┤
│ a            │ [(2, 34), (3, 71)]            │
├──────────────┼───────────────────────────────┤
│ b            │ [(3, 67), (5, 102)]           │
├──────────────┼───────────────────────────────┤
│ print        │ [(4, 80)]                     │
╘══════════════╧═══════════════════════════════╛

```
No caso de uma entrada com um erro léxico, uma mensagem de erro aparecerá no terminal.\
Exemplo:
```
Illegal character § at pos 78, line 3
```
