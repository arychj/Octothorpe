CREATE TABLE tblRules(
	id					INTEGER PRIMARY KEY,
	id_ServiceTriggerer	INTEGER,
	id_ServiceReceiver	INTEGER,
	EventType			TEXT,
	Transform			TEXT
)