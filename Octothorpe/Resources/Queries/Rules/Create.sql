INSERT INTO tblRules
    (ProducingService, EventType, ConsumingService, ConsumingMethod, PayloadTransform, IsActive)
    VALUES
    (:producing_service, :event_type, :consuming_service, :consuming_method, :payload_transform, 1)
