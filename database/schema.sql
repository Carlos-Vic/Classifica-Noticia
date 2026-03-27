CREATE TABLE IF NOT EXISTS artigos(
    idMateria INTEGER PRIMARY KEY AUTOINCREMENT,
    portal TEXT NOT NULL,
    titulo TEXT NOT NULL,
    subtitulo TEXT,
    texto TEXT NOT NULL,
    dataPublicacao TEXT,
    label TEXT NOT NULL,
    url TEXT NOT NULL,
    dataColeta TEXT
);