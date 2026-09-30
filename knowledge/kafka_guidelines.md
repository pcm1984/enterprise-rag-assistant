# Kafka Guidelines

## When to Use Kafka

Kafka should be used for asynchronous event-driven communication when
multiple independent consumers need to process events.

Kafka is appropriate when consumers may need to process events
independently, when event replay is required, or when producers should
not depend on the availability of downstream consumers.

Kafka should generally not be introduced when a simple synchronous
request-response interaction is sufficient.

## Event Design

Events should represent meaningful business events rather than
low-level implementation details.

Event consumers should be idempotent because messages may be
delivered more than once.

## Reliability

Important events should use appropriate delivery guarantees and
monitoring.

Consumer lag should be monitored to detect processing delays.
