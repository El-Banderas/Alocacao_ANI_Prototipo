# Informação para alocação

## Pedido Técnico, 
Lista de técnicos, de avaliação (Recebe todos)

```json
{
    "ID" : "int",
    "Nome" : "str",
    // Ativo : boolean, preenchido por nós, default true, verificar se existe na outSystems
    "Data_vinculo": "str", // DD/MM/AAAA, não vem no pedido, é nossa
}

Notas nossas:
- Depois utilizador pode meter no site se técnico ativo ou não
```
## Pedido projetos
Lista de projetos
Parâmetro: 
DataInicio (str)  
DataFim (str) 
Qual é a página (int), se < 0 trazer todos os dados
100 projetos por página

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
    "ID_Promotores" : ["int"], // Lista id promotores
    "Area Tematica": "str",
    // Esforço previsto calculado por nós

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

0 -> Não alocado

1 -> Análise alocado

2 -> Acompanhamento

3 -> Rejeitado

4-> Concluído