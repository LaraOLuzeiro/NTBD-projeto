----------------------- CRIAÇÃO DAS DIMENSÕES --------------------------

CREATE TABLE Dimensao_Produto(
	PK_produto SERIAL PRIMARY KEY,
	nome_produto VARCHAR(200),
	cultura_especie VARCHAR(100)
);

CREATE TABLE Dimensao_Tempo(
	PK_tempo SERIAL PRIMARY KEY,
	mes INT NOT NULL,
	ano INT NOT NULL,
	trimestre INT NULL, 
	mes_por_extenso VARCHAR(100)
);

CREATE TABLE Dimensao_Local(
	PK_local SERIAL PRIMARY KEY,
	estado VARCHAR(100),
	regiao VARCHAR(100),
	pais VARCHAR(100)
);

----------------------- CRIAÇÃO DA TABELA FATO --------------------------

CREATE TABLE Fato_Cotacao(
	PK_produto INT,
	PK_tempo INT,
	PK_comercializacao VARCHAR(50),
	PK_local INT,
	preco REAL,

	PRIMARY KEY(PK_produto, PK_tempo, PK_comercializacao, PK_local),
	FOREIGN KEY(PK_produto) REFERENCES Dimensao_Produto(PK_produto)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	FOREIGN KEY(PK_tempo) REFERENCES Dimensao_Tempo(PK_tempo)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	FOREIGN KEY(PK_local) REFERENCES Dimensao_Local(PK_local)
		ON UPDATE CASCADE
		ON DELETE CASCADE
	);