CREATE TABLE tblInstructions(
	id			INTEGER PRIMARY KEY,
	Ident		TEXT UNIQUE,
    Level       INTEGER NOT NULL,
	Service     TEXT NOT NULL,
    Method      TEXT NOT NULL,
	Payload		TEXT,
	GivenOn		DATETIME NOT NULL,
	CompletedOn	DATETIME
)
