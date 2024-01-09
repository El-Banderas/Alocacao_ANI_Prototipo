
clean_old_tables = [
"DROP TABLE IF  EXISTS T_PROMOCAO;			",
"DROP TABLE IF  EXISTS T_ALOCACAO;			",
"DROP TABLE IF  EXISTS T_PROJETO;			",
"DROP TABLE IF  EXISTS T_PREFERENCIA;		",
"DROP TABLE IF  EXISTS T_AREA_TEMATICA;		",
"DROP TABLE IF  EXISTS T_TECNICO;			",
"DROP TABLE IF  EXISTS T_FASE;				",
"DROP TABLE IF  EXISTS T_TIPOLOGIA;			",
"DROP TABLE IF  EXISTS T_PROMOTOR;			",
]

create_tables = [
"""
CREATE TABLE T_AREA_TEMATICA (
	Id_Area		INTEGER	PRIMARY KEY NOT NULL,
    Sigla_Area  TEXT NOT NULL,
    Area		TEXT
);
""",
"""
CREATE TABLE T_TECNICO (
    Id_Tecnico	INTEGER PRIMARY KEY,
    Nome		TEXT    NOT NULL,
	Ativo		INTEGER DEFAULT 1,
	Data_Vinculo	date
);
""",
"""
CREATE TABLE T_FASE (
    Id_Fase		INTEGER PRIMARY KEY,
    Fase		TEXT    NOT NULL
);
""",
"""
CREATE TABLE T_TIPOLOGIA (
    Id_Tipologia	INTEGER PRIMARY KEY,
    Tipologia		TEXT    NOT NULL
);
""",
"""
CREATE TABLE T_PROMOTOR (
    Id_Promotor		INTEGER PRIMARY KEY,
    Nome			TEXT    NOT NULL,
	NIPC			INTEGER,
	Representante	TEXT,
	Contato			TEXT
);
""",
"""
CREATE TABLE T_PREFERENCIA (
    Id_Tecnico   	INTEGER NOT NULL,
    Id_Area			INTEGER NOT NULL,
    Valor_Pref	INTEGER NOT NULL,
	PRIMARY KEY (Id_Tecnico, Id_Area),
    FOREIGN KEY (Id_Tecnico) REFERENCES T_TECNICO (Id_Tecnico) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (Id_Area) REFERENCES T_AREA_TEMATICA (Id_Area) ON UPDATE CASCADE ON DELETE CASCADE
);
""",
"""
CREATE TABLE T_PROJETO (
    Id_Projeto   				INTEGER PRIMARY KEY NOT NULL,
    Sigla_Projeto 				TEXT NOT NULL,
	Nome						TEXT NOT NULL,
	Id_Tipologia				INTEGER,
	Id_Fase						INTEGER DEFAULT 0,
	Id_Area						INTEGER,
	Data_Inicio					date,
	Data_Fim					date,
	Esf_Prev_Analise 			REAL,
	Esf_Prev_Acompanhamento 	REAL,
    FOREIGN KEY (Id_Tipologia) REFERENCES T_TIPOLOGIA (Id_Tipologia) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (Id_Fase) REFERENCES T_FASE (Id_Fase) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (Id_Area) REFERENCES T_AREA_TEMATICA (Id_Area) ON UPDATE CASCADE ON DELETE CASCADE	
);
""",
"""
CREATE TABLE T_ALOCACAO (
    Id_Tecnico   				INTEGER NOT NULL,
    Id_Fase 					INTEGER NOT NULL,
	Id_Projeto					INTEGER NOT NULL,
	Data_Inicio					date,
	Data_Fim					date,
	Esforco			 			REAL,
	PRIMARY KEY	(Id_Tecnico, Id_Fase, Id_Projeto),
    FOREIGN KEY (Id_Tecnico) REFERENCES T_TECNICO (Id_Tecnico) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (Id_Fase) REFERENCES T_FASE (Id_Fase) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (Id_Projeto) REFERENCES T_PROJETO (Id_Projeto) ON UPDATE CASCADE ON DELETE CASCADE	
);
""",
"""
CREATE TABLE T_PROMOCAO(
    Id_Promotor   				INTEGER NOT NULL,
    Id_Projeto					INTEGER NOT NULL,
	Main			 			INTEGER,
	PRIMARY KEY	(Id_Promotor, Id_Projeto),
    FOREIGN KEY (Id_Promotor) REFERENCES T_PROMOTOR (Id_Promotor) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (Id_Projeto) REFERENCES T_PROJETO (Id_Projeto) ON UPDATE CASCADE ON DELETE CASCADE	
);
"""

]

insert_basics = [
"INSERT INTO T_AREA_TEMATICA VALUES(1, 'AGRO/BIO/QUI', 'Agricultura / Biologia / Quimica');",
"INSERT INTO T_AREA_TEMATICA VALUES(2, 'MAT/MEC/ENER/CONST', 'Materiais / Mecânica / Energia / Construção');",
"INSERT INTO T_AREA_TEMATICA VALUES(3, 'TIC/INST', 'Tecnologias da Informação e Comunicação');",

"INSERT INTO T_TECNICO (Id_Tecnico, Nome, Data_Vinculo) VALUES(1, 'Manuel Joaquim', '2010-12-01');",
"INSERT INTO T_TECNICO (Id_Tecnico, Nome, Data_Vinculo) VALUES(2, 'Luísa Clementina', '2012-10-01');",
"INSERT INTO T_TECNICO (Id_Tecnico, Nome, Data_Vinculo) VALUES(3, 'Jorge Morgadinho', '2014-02-01');",
"INSERT INTO T_TECNICO (Id_Tecnico, Nome, Data_Vinculo) VALUES(4, 'Andreia Miquelina', '2022-04-21');",

"INSERT INTO T_FASE VALUES(0, 'Não alocado');",
"INSERT INTO T_FASE VALUES(1, 'Análise');",
"INSERT INTO T_FASE VALUES(2, 'Contratação');",
"INSERT INTO T_FASE VALUES(3, 'Acompanhamento');",
"INSERT INTO T_FASE VALUES(4, 'Encerramento');",


]

