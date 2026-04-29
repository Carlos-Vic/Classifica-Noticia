INSERT INTO erros (url, label, erro, dataColeta)
VALUES (%s,%s,%s,%s)
ON CONFLICT (url) DO NOTHING