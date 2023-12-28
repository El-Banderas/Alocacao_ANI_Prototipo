# Pedido geral
```json
{
    "projects" : [
        Lista projetos
    ],
    "tecnicos" : [
        Lista técnicos
    ],
    "alocacao" : [
        Lista alocações
    ]
} 
```
# Descrição projeto
```json
{
    "id" : "str",
    "sigla": "str",
    "nome": "str",
    "Tipologia": "str",
    "Fase": "int?",
    "area": "str", // This could be trouble, see later
    "Data inicio": "dd/mm/yyyy",
    "Data fim": "dd/mm/yyyy",
    // Esforços previstos são calculados por nós, ao inserir na BD
    "promotores": [Lista promotores]   
}
```

# Descrição promotores
```json
{
    "id" : "str",
    "nome": "str",
    "NIPC" : "str",
    "representante": "str",
    "contato": "tlm ou mail?"
}
```

# Descrição técnicos
```json
{
    "id" : "str",
    "nome": "str",
    "ativo": "boolean",
    "Data_vinculo": "dd/mm/yyyy",
    // Preferência tem de vir de nós, default tudo a 1?
}
```
# Descrição alocação
```json
{
    "id técnico" : "str",
    "fase": "int?",
    "nome proj": "str",
    "Data inicio": "dd/mm/yyyy",
    "Data fim": "dd/mm/yyyy",
    // Esforço é calculado por nós
}
```

# Notas
Acho que seria melhor dar-lhes um exemplo de uma resposta possível

Porque é que a alocação na nossa BD tem referência ao projeto através da sigla? 