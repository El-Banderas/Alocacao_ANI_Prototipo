# Informação para alocação

## Pedido Técnico, 
Lista de técnicos, de avaliação (Recebe todos)

```json
{
    "ID" : "int",
    "Nome" : "str",
    // Ativo : boolean, preenchido por nós, default true
    "Data_vinculo": "str", // DD/MM/AAAA
}
```
## Pedido projetos
Lista de projetos
Parâmetro: 
DataInicio (str) 
DataFim (str) 
Qual é a página (int)

```json
{
    "ID" : "int",
    "Sigla" : "str",
    "Nome" : "str",
    "Tipologia": "str", // Copromoção, individual, mobilizador
    // "Fase": "int",  Inserido por nós, ver se já tem alocação e a partir daí calcular se aprovado, ....
    "Area": "str",
    "Data inicio": "str", // DD/MM/AAAA
    "Data fim": "str", // DD/MM/AAAA
    // Ativo : boolean, preenchido por nós, default true
    "ID_Promotores" : ["int"], // Lista id promotores
    "Area Tematica": "str",
    // Esforço previsto calculado por nós

    "Tec_analise": "int", // ID, pode já estar presente ou não
    "Tec_acompanhamento": "int", // ID, pode já estar presente ou não
}
```

## Pedido promotores
Get, parâmetro: 
ID promotor

```json
{
    "ID" : "int",
    "Nome": "str",
    "NIPC": "int",
    "Representante": "str",
    "Contato": "int",

}
```
# Informação para site