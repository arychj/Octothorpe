CREATE TABLE tblRules(
	id					INTEGER PRIMARY KEY,
	ProducingService   	TEXT,
	EventType			TEXT,
    ConsumingService    TEXT,
    ConsumingMethod     TEXT,
	PayloadTransform	TEXT,
    IsActive            BOOLEAN
)
