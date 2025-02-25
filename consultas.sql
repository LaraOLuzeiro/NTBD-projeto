-- RENAN
-- Qual o preço médio da soja em grãos (60 kg) no estado do RS no ano de 2022?

SELECT nome_produto, estado, ano, AVG(preco) as preco_medio
FROM fato_cotacao NATURAL JOIN dimensao_produto 
NATURAL JOIN dimensao_tempo NATURAL JOIN dimensao_local
WHERE estado = 'Mato Grosso do Sul' AND nome_produto = 'SOJA EM GRÃOS (60 kg)' AND ano = 2022
GROUP BY nome_produto, estado, ano, pk_local

--Daniella

-- Quantos porcento caiu o preço da CARNE BOVINA DIANTEIRO COM OSSO (15 kg) no Amazonas de fevereiro de 2023 para outubro de 2023?
SELECT distinct nome_produto, estado, ROUND(((SELECT preco FROM preco_fevereiro_e_outubro WHERE mes_por_extenso = 'Outubro') * 100 / (SELECT preco FROM preco_fevereiro_e_outubro WHERE mes_por_extenso = 'Fevereiro')) :: NUMERIC, 2) AS porcentagem
from preco_fevereiro_e_outubro

CREATE OR REPLACE VIEW preco_fevereiro_e_outubro(nome_produto, estado, mes_por_extenso, ano, preco) AS
	SELECT nome_produto, estado, mes_por_extenso, ano, preco
	FROM fato_cotacao NATURAL JOIN Dimensao_tempo NATURAL JOIN dimensao_local NATURAL JOIN dimensao_produto
	WHERE nome_produto = 'CARNE BOVINA DIANTEIRO COM OSSO (15 kg)' AND estado = 'Amazonas' AND ano = 2023 AND mes_por_extenso = 'Fevereiro' 
	UNION  
	SELECT nome_produto, estado, mes_por_extenso, ano, preco
	FROM fato_cotacao NATURAL JOIN Dimensao_tempo NATURAL JOIN dimensao_local NATURAL JOIN dimensao_produto
	WHERE nome_produto = 'CARNE BOVINA DIANTEIRO COM OSSO (15 kg)' AND estado = 'Amazonas' AND ano = 2023 AND mes_por_extenso = 'Outubro';
