Os dois primeiros pedidos são os mais prioritários.

# Informação para alocação

## Pedido Técnico

Lista contendo todos técnicos

```json
{
    "ID" : "int",
    "Nome" : "str",
}
```

## Pedido projetos
Lista de projetos, que pode ser paginado ou não. Cada página contêm 100 projetos.
Parâmetros: 
- DataInicio (str), no formato DD/MM/AAAA 
- DataFim (str), no formato DD/MM/AAAA
- Qual é a página (int). Se a página for menor que 0, resposta deve conter todos os projetos.

```json
{
    "ID" : "int",
    "Sigla" : "str",
    "Nome" : "str",
    "Tipologia": "str", // Copromoção, individual, mobilizador
     "Fase": "int",  // A discutir na reunião 
    "Area": "str",
    "Data inicio": "str", // DD/MM/AAAA
    "Data fim": "str", // DD/MM/AAAA
    "ID_Promotores" : ["int"], // Lista id promotores
    "Area Tematica": "str",

    "Tec_analise": "int", // ID, pode já estar presente ou não, quando não existe, preencher com null/undefined...
    "Tec_acompanhamento": "int", // ID, pode já estar presente ou não, quando não existe, preencher com null/undefined...
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
