UPDATE  tblInstructions
SET     ProcessingOn = :processing_on,
        CompletedOn = :completed_on
WHERE   id = :id
