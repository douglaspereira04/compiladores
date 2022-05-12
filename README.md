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
STRING \"(\\.|[^\"])*\"
FLOAT ([0-9])+.([0-9])+
INT [0-9]+
IDENT (_*)([a-z]|[A-Z]|_|[0-9])+
RELOP (<|>|<=|>=|==)
BOOLOP (\|\||&&)
literals +-*/=<>(){},;
ignore   		
```
É importante notar que mesmo a entrada "ignore" aparentar vazia, a linha é composta por "ignore"(sendo o nome da entrada),"espaço"(sendo usado como separador entre nome da entrada e integrantes da entrada),"espaço"(sendo usado como integrante da entrada) e "tabulação".
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
A saída esperada é uma tabela de símbolos. As colunas são de token do lexema encontrado, lexema, linha do lexema e posição inicial do lexema. 
```
╒═════════╤══════════════╤═════════╤═══════════╕
│ TOKEN   │ LEXEMA       │   LINHA │   POSIÇÃO │
╞═════════╪══════════════╪═════════╪═══════════╡
│ DEF     │ def          │       1 │         0 │
├─────────┼──────────────┼─────────┼───────────┤
│ IDENT   │ minha_funcao │       1 │         4 │
├─────────┼──────────────┼─────────┼───────────┤
│ (       │ (            │       1 │        16 │
├─────────┼──────────────┼─────────┼───────────┤
│ IDENT   │ param1       │       1 │        17 │
├─────────┼──────────────┼─────────┼───────────┤
│ ,       │ ,            │       1 │        23 │
├─────────┼──────────────┼─────────┼───────────┤
│ IDENT   │ param2       │       1 │        24 │
├─────────┼──────────────┼─────────┼───────────┤
│ )       │ )            │       1 │        30 │
├─────────┼──────────────┼─────────┼───────────┤
│ {       │ {            │       1 │        31 │
├─────────┼──────────────┼─────────┼───────────┤
│ IDENT   │ a            │       2 │        34 │
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
│ IDENT   │ b            │       3 │        67 │
├─────────┼──────────────┼─────────┼───────────┤
│ =       │ =            │       3 │        69 │
├─────────┼──────────────┼─────────┼───────────┤
│ IDENT   │ a            │       3 │        71 │
├─────────┼──────────────┼─────────┼───────────┤
│ RELOP   │ <            │       3 │        73 │
├─────────┼──────────────┼─────────┼───────────┤
│ INT     │ 50           │       3 │        75 │
├─────────┼──────────────┼─────────┼───────────┤
│ ;       │ ;            │       3 │        77 │
├─────────┼──────────────┼─────────┼───────────┤
│ IDENT   │ print        │       4 │        80 │
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
│ IDENT   │ b            │       5 │       102 │
├─────────┼──────────────┼─────────┼───────────┤
│ BOOLOP  │ &&           │       5 │       104 │
├─────────┼──────────────┼─────────┼───────────┤
│ IDENT   │ param1       │       5 │       107 │
├─────────┼──────────────┼─────────┼───────────┤
│ )       │ )            │       5 │       113 │
├─────────┼──────────────┼─────────┼───────────┤
│ {       │ {            │       5 │       114 │
├─────────┼──────────────┼─────────┼───────────┤
│ RETURN  │ return       │       6 │       118 │
├─────────┼──────────────┼─────────┼───────────┤
│ (       │ (            │       6 │       125 │
├─────────┼──────────────┼─────────┼───────────┤
│ IDENT   │ param1       │       6 │       126 │
├─────────┼──────────────┼─────────┼───────────┤
│ BOOLOP  │ ||           │       6 │       133 │
├─────────┼──────────────┼─────────┼───────────┤
│ IDENT   │ param2       │       6 │       136 │
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

```

