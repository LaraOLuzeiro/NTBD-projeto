-- RENAN
-- Qual o preço médio da soja em grãos (60 kg) no estado do RS no ano de 2022?

SELECT nome_produto, pk_comercializacao, estado, ano, AVG(preco) as preco_medio
FROM fato_cotacao NATURAL JOIN dimensao_produto 
NATURAL JOIN dimensao_tempo NATURAL JOIN dimensao_local
WHERE estado = 'Mato Grosso' AND nome_produto = 'SOJA EM GRÃOES (60 KG)'AND ano = 2022
GROUP BY nome_produto, pk_comercializacao, estado, ano, pk_local