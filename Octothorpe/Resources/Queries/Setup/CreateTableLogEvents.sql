CREATE TABLE tblLogEvents(
	id			INTEGER PRIMARY KEY,
	id_Service	INTEGER,
	Payload		TEXT,
	EmittedOn	DATETIME
)

--Outcome, Artifact, Product, Result