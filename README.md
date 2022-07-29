# Analisador Léxico/Sintático/Semântico

Para executar o programa você precisa ter o Python 3.8 e o make instalados. Para instalar execute:
```
apt install python3.8 python3.8-venv make
```

O programa tem como entrada um arquivo de definição dos tokens e um arquivo de código a ser analisado. Para executar o programa:
```
make clean venv
make run code_file_path=my_code_file
```

Os exemplos se encontram no diretório samples. Para executar o analisador sobre os códigos de teste:
```
make run code_file_path=samples/ccc_code_1.ccc
make run code_file_path=samples/ccc_code_2.ccc
make run code_file_path=samples/ccc_code_3.ccc
```

## Arquivo de código
Qualquer texto dentro do arquivo será analisado.\
Exemplo:
```
{ int a ; i = 0 ;
a = 22; 
int i; 

while ( i < 47+ 232) {
    a = a +31;
};
boolean k;
k = false;
if (a > 932){
    k = true;
};
}

```

No caso de uma entrada com um erro léxico, uma mensagem de erro aparecerá no terminal.\
Exemplo:
```
Illegal character @ at pos 110, line 10
```
No caso de uma entrada com um erro sintático, será apresentado no terminal a forma sentencial e o símbolo não esperado.\
Exemplo:
```
Unexpected symbol } at pos 139, line 10
```
Em entradas com erro semântica, serão possíveis erros:
```
Incompatible operands in expression next to = at pos 88, line 8
Unexpected break at pos 136, line 9
Redeclaration of ident at pos 141, line 10 already declared at pos 57, line 5
```
