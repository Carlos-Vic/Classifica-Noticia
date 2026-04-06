SELECT label, portal, count(*) AS total
FROM artigos
GROUP BY portal, label