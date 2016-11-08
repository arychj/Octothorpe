SELECT  id as Id,
        ConsumingService,
        ConsumingMethod,
        PayloadTransform
FROM    tblRules
WHERE   ProducingService = :producing_service AND
        EventType = :event_type AND
        IsActive = 1
