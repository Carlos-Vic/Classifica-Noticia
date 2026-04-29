INSERT INTO erros (url, label, erro, dataColeta)
VALUES (%s,%s,%s,%s)
ON CONFLICT (url) DO UPDATE SET erro = EXCLUDED.erro, dataColeta = EXCLUDED.dataColeta