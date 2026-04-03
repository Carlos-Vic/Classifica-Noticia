WITH tb_count AS(
    SELECT portal, count(*) AS quantidade
    FROM portais_demanda
    GROUP BY portal
)

SELECT * FROM tb_count
ORDER BY quantidade DESC