CREATE TABLE tblLogInstructions(
	id			INTEGER PRIMARY KEY,
	id_Service	INTEGER,
	Ident		TEXT,
	Payload		TEXT,
	GivenOn		DATETIME,
	CompletedOn	DATETIME
)