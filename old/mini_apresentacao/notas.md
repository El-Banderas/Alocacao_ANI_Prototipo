# Ordem de funcionamento

1. Gestor insere dados sobre projetos e técnicos em Excel1 (como o do protótipo entregue).

2. Programa calcula atribuições dos técnicos aos projetos, e gera um Excel específico para cada técnico, como o desta pasta.
A pasta contendo os Exceis deve estar numa pasta do OneDrive, assim quando um técnico alterar, o gestor tem acesso, sem precisar de fazer download.

3. Programa também pode dividir as várias tarefas que um projeto tem, e calcula uma ordem de prioridades, podendo ter vários fatores como data de início do projeto, urgência, etc... <br> Se essa ordenação for aceite, e tendo em conta estimativas da duração das tarefas, é possível ter uma previsão de quando serão concluídas. Como existem tarefas condicionais, por exemplo processo ser aceite, podemos calcular apenas as tarefas que estão na "linha da frente". Desta forma, um técnico teria algo deste género:

Tarefas a realizar -> Proj3-T3 ; Proj2-T7 ; ...

4. Os técnicos vão atualizando os Exceis com as tarefas que vão fazendo. Alteram a tarefa atual que fazem, e assim há progresso na conclusão de tarefas.

5. No fim de uma iteração, tipo uma semana, gestor corre o programa, e consegue ver quanto é que falta para cada técnico, e ver se há desbalanceamento de trabalho. 

## Opcionais:

- Considerar um técnico ausente (p. ex. doença). Os projetos alocados a esse técnico são distribuídas pelos outros, e a única alteração que implica é no recálculo da ordem das tarefas a realizar por cada técnico.

- Caso o trabalho de um dos técnicos comece a atrasar, e ele fique sobrecarregado, fazer uma redistribuição. Este cenário é complexo porque não estamos a alocar projetos, mas tarefas, complicando em termos de heurística e cenários.

- Adicionar projetos. Seria apenas descobrir qual o melhor técnico para tratar disso, e juntava à lista de projetos dele. 

# Coisas a decidir:

- Frontend, como apresentar os dados;
- Quais os parâmetros das heurísticas, e consequentemente dos Exceis.

# Proposta de organização
## Visto que temos pouco tempo

Dividir o trabalho em quatro grupos:
- Mockups para frontend;
- Partir os projetos em várias tarefas;
- Encontrar e testar heurísticas de atribuição de tarefas a técnicos;
- Arranjar exceis, tendo em conta heurísticas, e facilidade de utilização.
<br>Cada subgrupo reúne para decidir os aspetos mais específicos, e encontra alternativas. Depois, nas reuniões semanais discute-se as alternativas. Tenho de falar com o pessoal que faz mockups para não pedirem coisas muito mágicas ;) 
