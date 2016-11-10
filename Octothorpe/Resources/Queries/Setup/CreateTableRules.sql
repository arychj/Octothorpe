CREATE TABLE tblRules(
	id					INTEGER PRIMARY KEY,
	ProducingService   	TEXT,
	EventType			TEXT,
    ConsumingService    TEXT,
    ConsumingMethod     TEXT,
	PayloadTransform	TEXT,
    IsActive            BOOLEAN
)

CREATE INDEX tblRules_PS-ET-CS-CM on tblRules (ProducingService, EventType)
