# Kafka Guidelines (example)

Generic Kafka conventions for the example portal. Replace `the-project` with
your tenant prefix.

## Topic naming

```
<tenant>.<domain>.<event>
the-project.lists.created
the-project.lists.updated
```

## Producer (generic Java)

```java
// Example only. No real client/host.
try (var producer = new KafkaProducer<String, byte[]>(props)) {
    var rec = new ProducerRecord<>("the-project.lists.created", key, avroBytes);
    producer.send(rec).get();
}
```

## Schema Registry

Schemas are AVRO (`.avdl`), registered in a Schema Registry. Consumers
resolve the writer schema by id. See `kafka/avro/` for the example set.
