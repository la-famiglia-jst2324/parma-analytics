SELECT destination
FROM notification_channel
WHERE id IN (:channel_ids)
    AND entity_type = :entity_type
    AND channel_type = :channel_type;
