DROP TABLE IF  EXISTS T_PROMOCAO;					/* 2 */
DROP TABLE IF  EXISTS T_ALOCACAO;					/* 2 */
DROP TABLE IF  EXISTS T_PROJETO;					/* 1 */
DROP TABLE IF  EXISTS T_PREFERENCIA;				/* 1 */
DROP TABLE IF  EXISTS T_AREA_TEMATICA;				/* 0 */
DROP TABLE IF  EXISTS T_TECNICO;					/* 0 */
DROP TABLE IF  EXISTS T_FASE;						/* 0 */
DROP TABLE IF  EXISTS T_TIPOLOGIA;					/* 0 */
DROP TABLE IF  EXISTS T_PROMOTOR;					/* 0 */

CREATE TABLE T_AREA_TEMATICA (
	Id_Area		INTEGER	PRIMARY KEY NOT NULL,
    Sigla_Area  TEXT NOT NULL,
    Area		TEXT
);

CREATE TABLE T_TECNICO (
    Id_Tecnico	INTEGER PRIMARY KEY,
    Nome		TEXT    NOT NULL,
	Ativo		INTEGER DEFAULT 1,
	Data_Vinculo	date
);

CREATE TABLE T_FASE (
    Id_Fase		INTEGER PRIMARY KEY,
    Fase		TEXT    NOT NULL
);

CREATE TABLE T_TIPOLOGIA (
    Id_Tipologia	INTEGER PRIMARY KEY,
    Tipologia		TEXT    NOT NULL
);

CREATE TABLE T_PROMOTOR (
    Id_Promotor		INTEGER PRIMARY KEY,
    Nome			TEXT    NOT NULL,
	NIPC			INTEGER,
	Representante	TEXT,
	Contato			TEXT
);

CREATE TABLE T_PREFERENCIA (
    Id_Tecnico   	INTEGER NOT NULL,
    Id_Area			INTEGER NOT NULL,
    Valor_Pref	INTEGER NOT NULL,
	PRIMARY KEY (Id_Tecnico, Id_Area),
    FOREIGN KEY (Id_Tecnico) REFERENCES T_TECNICO (Id_Tecnico) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (Id_Area) REFERENCES T_AREA_TEMATICA (Id_Area) ON UPDATE CASCADE ON DELETE CASCADE
);

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

CREATE TABLE T_PROMOCAO(
    Id_Promotor   				INTEGER NOT NULL,
    Id_Projeto					INTEGER NOT NULL,
	Main			 			INTEGER,
	PRIMARY KEY	(Id_Promotor, Id_Projeto),
    FOREIGN KEY (Id_Promotor) REFERENCES T_PROMOTOR (Id_Promotor) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (Id_Projeto) REFERENCES T_PROJETO (Id_Projeto) ON UPDATE CASCADE ON DELETE CASCADE	
);


INSERT INTO T_AREA_TEMATICA VALUES(1, 'AGRO/BIO/QUI', 'Agricultura / Biologia / Quimica');
INSERT INTO T_AREA_TEMATICA VALUES(2, 'MAT/MEC/ENER/CONST', 'Materiais / Mecânica / Energia / Construção');
INSERT INTO T_AREA_TEMATICA VALUES(3, 'TIC/INST', 'Tecnologias da Informação e Comunicação');

INSERT INTO T_TECNICO (Id_Tecnico, Nome, Data_Vinculo) VALUES(1, 'Manuel Joaquim', '2010-12-01');
INSERT INTO T_TECNICO (Id_Tecnico, Nome, Data_Vinculo) VALUES(2, 'Luísa Clementina', '2012-10-01');
INSERT INTO T_TECNICO (Id_Tecnico, Nome, Data_Vinculo) VALUES(3, 'Jorge Morgadinho', '2014-02-01');
INSERT INTO T_TECNICO (Id_Tecnico, Nome, Data_Vinculo) VALUES(4, 'Andreia Miquelina', '2022-04-21');

INSERT INTO T_FASE VALUES(0, 'Não alocado');
INSERT INTO T_FASE VALUES(1, 'Análise');
INSERT INTO T_FASE VALUES(2, 'Contratação');
INSERT INTO T_FASE VALUES(3, 'Acompanhamento');
INSERT INTO T_FASE VALUES(4, 'Encerramento');


INSERT INTO T_TIPOLOGIA VALUES(1, 'Copromoção');
INSERT INTO T_TIPOLOGIA VALUES(2, 'Individual');
INSERT INTO T_TIPOLOGIA VALUES(3, 'Mobilizadora');

INSERT INTO T_PROMOTOR VALUES(1, 'SONAE MC', 523123123, 'Martim Castro', 'mcastro@sonaemc.com');
INSERT INTO T_PROMOTOR VALUES(2, 'STCP', 523123123, 'Marta Curto', 'mcurto@stcp.pt');
INSERT INTO T_PROMOTOR VALUES(3, 'ANA', 501123123, 'Mariana Mesquita', 'm.mesquita@ana.pt');
INSERT INTO T_PROMOTOR VALUES(4, 'UBI', 503123123, 'Paulina Lopes', 'plopes@ubi.pt');
INSERT INTO T_PROMOTOR VALUES(5, 'Nestlé Portugal', 515123123, 'Nuno Pinto', 'np45@nestle.com');
INSERT INTO T_PROMOTOR VALUES(6, 'Bolinas SA', 553123123, 'Joana Bolinas', 'joana.bolinas@bsa.pt');

INSERT INTO T_PREFERENCIA (Id_Tecnico, Id_Area, Valor_Pref) VALUES(1, 1, 90);
INSERT INTO T_PREFERENCIA (Id_Tecnico, Id_Area, Valor_Pref) VALUES(1, 2, 110);
INSERT INTO T_PREFERENCIA (Id_Tecnico, Id_Area, Valor_Pref) VALUES(1, 3, 100);
INSERT INTO T_PREFERENCIA (Id_Tecnico, Id_Area, Valor_Pref) VALUES(2, 1, 100);
INSERT INTO T_PREFERENCIA (Id_Tecnico, Id_Area, Valor_Pref) VALUES(2, 2, 110);
INSERT INTO T_PREFERENCIA (Id_Tecnico, Id_Area, Valor_Pref) VALUES(2, 3, 90);
INSERT INTO T_PREFERENCIA (Id_Tecnico, Id_Area, Valor_Pref) VALUES(3, 1, 60);
INSERT INTO T_PREFERENCIA (Id_Tecnico, Id_Area, Valor_Pref) VALUES(3, 2, 120);
INSERT INTO T_PREFERENCIA (Id_Tecnico, Id_Area, Valor_Pref) VALUES(3, 3, 50);
INSERT INTO T_PREFERENCIA (Id_Tecnico, Id_Area, Valor_Pref) VALUES(4, 1, 110);
INSERT INTO T_PREFERENCIA (Id_Tecnico, Id_Area, Valor_Pref) VALUES(4, 2, 110);
INSERT INTO T_PREFERENCIA (Id_Tecnico, Id_Area, Valor_Pref) VALUES(4, 3, 100);

INSERT INTO T_PROJETO (Id_Projeto, Sigla_Projeto, Nome, Id_Tipologia, Id_Fase, Id_Area, Data_Inicio, Data_Fim, Esf_Prev_Analise, Esf_Prev_Acompanhamento)
			VALUES(1, 'P2030/12', 'Fator Máximo', 2, 0, 1, '2023-01-01', '2025-12-31', 123.5, 26.5);
INSERT INTO T_PROJETO (Id_Projeto, Sigla_Projeto, Nome, Id_Tipologia, Id_Fase, Id_Area, Data_Inicio, Data_Fim, Esf_Prev_Analise, Esf_Prev_Acompanhamento)
			VALUES(2, 'P2030/15', 'Peixe Fresco', 1, 1, 2, '2023-05-01', '2025-12-31', 13.5, 20.5);
INSERT INTO T_PROJETO (Id_Projeto, Sigla_Projeto, Nome, Id_Tipologia, Id_Fase, Id_Area, Data_Inicio, Data_Fim, Esf_Prev_Analise, Esf_Prev_Acompanhamento)
			VALUES(3, 'P2020/202', 'Calçado Flex', 1, 1, 3, '2022-05-21', '2025-12-31', 63.5, 46.5);
INSERT INTO T_PROJETO (Id_Projeto, Sigla_Projeto, Nome, Id_Tipologia, Id_Fase, Id_Area, Data_Inicio, Data_Fim, Esf_Prev_Analise, Esf_Prev_Acompanhamento)
			VALUES(4, 'PNORTE/25', 'Hiper22', 2, 1, 1, '2022-10-01', '2030-12-31', 14.5, 27.5);			
INSERT INTO T_PROJETO (Id_Projeto, Sigla_Projeto, Nome, Id_Tipologia, Id_Fase, Id_Area, Data_Inicio, Data_Fim, Esf_Prev_Analise, Esf_Prev_Acompanhamento)
			VALUES(5, 'PNORTE/32', 'Leite para todos', 2, 2, 2, '2023-01-01', '2029-12-31', 22.5, 46.7);
INSERT INTO T_PROJETO (Id_Projeto, Sigla_Projeto, Nome, Id_Tipologia, Id_Fase, Id_Area, Data_Inicio, Data_Fim, Esf_Prev_Analise, Esf_Prev_Acompanhamento)
			VALUES(6, 'P2030/202', 'Reciclex', 3, 2, 3, '2023-02-10', '2028-12-31', 23.5, 6.5);
INSERT INTO T_PROJETO (Id_Projeto, Sigla_Projeto, Nome, Id_Tipologia, Id_Area, Data_Inicio, Data_Fim, Esf_Prev_Analise, Esf_Prev_Acompanhamento)
			VALUES(7, 'POPN/2024', 'Polinex', 1, 2,  '2023-02-10', '2026-12-31', 23.5, 6.5);

			
			
INSERT INTO T_ALOCACAO (Id_Tecnico, Id_Fase, Id_Projeto, Data_Inicio, Data_Fim, Esforco)
			VALUES(1, 2, 1,  '2023-02-10', '2025-12-31', 12.5);
INSERT INTO T_ALOCACAO (Id_Tecnico, Id_Fase, Id_Projeto, Data_Inicio, Data_Fim, Esforco)
			VALUES(2, 1, 1,  '2023-02-10', '2025-12-31', 13.5);
INSERT INTO T_ALOCACAO (Id_Tecnico, Id_Fase, Id_Projeto, Data_Inicio, Data_Fim, Esforco)
			VALUES(2, 1, 2,  '2023-02-10', '2025-12-31', 20.5);
INSERT INTO T_ALOCACAO (Id_Tecnico, Id_Fase, Id_Projeto, Data_Inicio, Data_Fim, Esforco)
			VALUES(3, 1, 3,  '2023-02-10', '2025-12-31', 21.5);
INSERT INTO T_ALOCACAO (Id_Tecnico, Id_Fase, Id_Projeto, Data_Inicio, Data_Fim, Esforco)
			VALUES(3, 3, 4,  '2023-02-10', '2025-12-31', 32.5);
INSERT INTO T_ALOCACAO (Id_Tecnico, Id_Fase, Id_Projeto, Data_Inicio, Data_Fim, Esforco)
			VALUES(4, 1, 5,  '2023-02-10', '2025-12-31', 34.5);
INSERT INTO T_ALOCACAO (Id_Tecnico, Id_Fase, Id_Projeto, Data_Inicio, Data_Fim, Esforco)
			VALUES(4, 1, 6,  '2023-02-10', '2025-12-31', 11.5);
INSERT INTO T_ALOCACAO (Id_Tecnico, Id_Fase, Id_Projeto, Data_Inicio, Data_Fim, Esforco)
			VALUES(4, 3, 7,  '2023-02-10', '2025-12-31', 31.5);			

INSERT INTO T_PROMOCAO (Id_Promotor, Id_Projeto, main) VALUES(1,1, 1);
INSERT INTO T_PROMOCAO (Id_Promotor, Id_Projeto, main) VALUES(2,1, 0);
INSERT INTO T_PROMOCAO (Id_Promotor, Id_Projeto, main) VALUES(2,2, 1);
INSERT INTO T_PROMOCAO (Id_Promotor, Id_Projeto, main) VALUES(3,3, 1);
INSERT INTO T_PROMOCAO (Id_Promotor, Id_Projeto, main) VALUES(4,4, 1);
INSERT INTO T_PROMOCAO (Id_Promotor, Id_Projeto, main) VALUES(5,5, 1);
INSERT INTO T_PROMOCAO (Id_Promotor, Id_Projeto, main) VALUES(6,6, 1);
INSERT INTO T_PROMOCAO (Id_Promotor, Id_Projeto, main) VALUES(6,7, 0);


				