---
name: kafka-the-project
description: Kafka platform (the-project Streaming) guidelines, AVRO schema definitions, topic naming, ACLs, and Confluent Schema Registry patterns for the-project. Use when producing/consuming Kafka messages, defining AVRO schemas, configuring topics, or integrating with the the-project CDF (Common Data Format).
---

# Kafka - the-project the-project Streaming Platform

This skill documents the **the-project Kafka platform (the-project Streaming)** conventions, AVRO schema definitions (CDF - Common Data Format), and integration patterns for producing and consuming messages.

## Technology Stack

- **Platform**: Apache Kafka (the-project Streaming - the-project managed)
- **Schema Format**: Apache AVRO (`.avdl` IDL files)
- **Schema Registry**: Confluent Schema Registry
- **Serialization**: Confluent AVRO Serializer/Deserializer
- **Language**: Java (producers/consumers)
- **Libraries**: `org.apache.avro`, `io.confluent` (Kafka AVRO SerDe)

## When to Use This Skill

Use this skill when:

- [done] Producing or consuming messages on the the-project Kafka platform
- [done] Defining or evolving AVRO schemas for CDF data
- [done] Creating new Kafka topics for the-project applications
- [done] Configuring ACLs for Kafka producers/consumers
- [done] Integrating with Confluent Schema Registry
- [done] Working with vessel position data (AIS, LRIT, VMS, Sat-AIS)
- [done] Adding enrichment data to position reports (ship, voyage, MRS, incident, exemption, fisheries, anti-piracy)

## Topic Naming Convention

Topics **shall** follow a hierarchical naming structure:

```
<application>.<logical-grouping>.<event-name>
```

| Field           | Description                        | Example        |
|-----------------|------------------------------------|----------------|
| Application     | Application name (lowercase, dash) | `star-rtmps`   |
| Logical group   | Domain/data category               | `ais`          |
| Event name      | Specific event type                | `aton`         |
| **Topic name**  | Full topic name                    | `star-rtmps.ais.aton` |

### Rules

- Topic ownership belongs to the **application producing** messages.
- Topics **shall** have an AVRO schema associated in the Schema Registry.
- **Prefix ACLs** enforce naming structure (e.g., application `STAR RTMPS` can only create topics starting with `star-rtmps`).

## Topic Configuration Requirements

- **MUST** define `retention.bytes` (size-based retention) for all topics.
- **SHOULD** also define `retention.ms` (time-based retention).
- Applications **shall** monitor the size of storage used by their topics (JMX metric: `kafka.log.Log.Size.<TOPIC-NAME>`).

## ACL Requirements

- Producers and consumers **shall** have ACLs (access control lists) configured.
- Use prefixed ACLs (`--resource-pattern-type Prefixed`) to enforce topic naming structure.
- Each application gets a prefix matching its application name in the topic hierarchy.

## Monitoring

Applications **shall** track:

- Rate of failed authentication attempts
- Request latency
- Consumer lag
- Total number of consumer groups
- Quota metrics
- Storage size per topic-partition

## AVRO Schema Management

### Workflow

1. Contractor fetches current schema from **development** branch
2. Proposes changes in own branch (`<application-name>-<version>`)
3. Merges develop into own branch (sync any upstream changes)
4. Submits merge request for the-project review to development branch
5. the-project reviews and merges once accepted
6. Before FAT: contractor merges develop into own branch, tests, and adjusts
7. On production release: the-project promotes changes to **master** branch with version tag (e.g., `1.2`)

### Schema Evolution Rules

- **No optional fields** in AVRO: use `union { null, <type> }` instead to make fields optional.
- **Union changes**: Update all readers first with new schema, then update writers.
- **Field reordering**: Allowed freely: parser matches fields by name, not position.
- **Field renaming**: Add new name as alias in reader schema first, then update writer.
- **Adding fields**: Provide a default value (e.g., `null` for union-with-null types).
- **Removing fields**: Only if the field previously had a default value.

### AVRO DECIMAL Type

- DECIMAL is a Logical Type (not Primitive): defined as `{"type": "bytes", "logicalType": "decimal", "precision": N, "scale": M}`.
- **Prefer FLOAT/DOUBLE** over DECIMAL unless accuracy is critical (e.g., financial calculations).
- Schema evolution for DECIMAL is not fully tested: do not change representation or data type after writing DECIMAL data.

## Confluent Schema Registry

- the-project uses Confluent Schema Registry to avoid including AVRO schema in each message.
- **MUST** disable automatic schema registration in production:

```java
props.put(AbstractKafkaAvroSerDeConfig.AUTO_REGISTER_SCHEMAS, false);
```

- Use Confluent Control Center to manually register schemas in production.
- Auto-registration is acceptable in development environments only.

## AVRO Schema Reference (CDF)

Schemas are defined in `.avdl` (AVRO IDL) files for the the-project Common Data Format.

### Core Records

| Record | File | Description |
|--------|------|-------------|
| **PositionReport** | `position_report.avdl` | Main record: vessel position with source-specific data and enrichments |
| **ShipParticulars** | `ship_particulars.avdl` | Vessel identifiers and descriptors (IMO, MMSI, name, flag state, etc.) |

### Source-Specific Records (union in PositionReport.sourceSpecific)

| Record | File | Data Source |
|--------|------|-------------|
| **AisSpecific** | `ais_specific.avdl` | Terrestrial AIS (T-AIS) |
| **SatAisSpecific** | `sat_ais_specific.avdl` | Satellite AIS |
| **LritSpecific** | `lrit_specific.avdl` | Long Range Identification and Tracking |
| **VmsSpecific** | `vms_specific.avdl` | Vessel Monitoring System |

### Enrichment Records

| Record | File | Description |
|--------|------|-------------|
| **ShipEnrichment** | `ship_enrichment.avdl` | CSD ship details, risk profile, dimensions, banning/detention status |
| **VoyageEnrichment** | `voyage_enrichment.avdl` | SSN voyage data, ports, hazmat, security level |
| **MrsEnrichment** | `mrs_enrichment.avdl` | MRS (Maritime Reporting System) notifications |
| **IncidentEnrichment** | `incident_enrichment.avdl` | Incident notifications (POLREP, etc.) |
| **ExemptionEnrichment** | `exemption_enrichment.avdl` | Exemptions (hazmat, etc.) |
| **FisheriesEnrichment** | `fisheries_enrichment.avdl` | Fisheries-related data |
| **AntiPiracyEnrichment** | `anti_piracy_enrichment.avdl` | Anti-piracy enrichment |

### Common Types

Defined in `common_types.avdl`:

- **Fixed types**: `IsoCountryCode2` (2 bytes), `IsoCountryCode3` (3 bytes), `LocationCode` (5 bytes), `ImoNumber` (7 bytes)
- **PortInfo**: name, locode, eta, ata, atd, location_in_port
- **Enums**: `PositionAccuracy` (HIGH/LOW), `AisPositionMessageType`, `PscShipType` (45+ ship types), `NavigationalStatus`, `ShipRiskProfile`, `SecurityLevel`, `WasteDeliveryStatus`

### Update Records

| Record | File | Description |
|--------|------|-------------|
| **CsdUpdates** | `csd_updates.avdl` | CSD (Central Ship Database) update events |
| **OvrUpdates** | `ovr_updates.avdl` | OVR (Overview) update events |
| **OvrProjectSpecificUpdates** | `ovr_project_specific_updates.avdl` | OVR project-specific updates |

## Java Producer/Consumer Pattern

### AVRO Serialization Example

```java
import org.apache.avro.file.DataFileWriter;
import org.apache.avro.specific.SpecificDatumWriter;
import eu.europa.example.cdf.avro.*;

// Create datum writer for the AVRO record type
SpecificDatumWriter<PositionReport> datumWriter =
    new SpecificDatumWriter<>(PositionReport.class);

// Build a position report using the Builder pattern
PositionReport report = PositionReport.newBuilder()
    .setMessageId("MSG-001")
    .setSource("T-AIS")
    .setTimestamp(new DateTime())
    .setOriginator("PT")
    .setLatitude(38.7223d)
    .setLongitude(-9.1393d)
    .setParticulars(particulars)
    // ... other fields
    .build();
```

### Kafka Producer Configuration

```java
Properties props = new Properties();
props.put("bootstrap.servers", "<kafka-broker>");
props.put("key.serializer", "io.confluent.kafka.serializers.KafkaAvroSerializer");
props.put("value.serializer", "io.confluent.kafka.serializers.KafkaAvroSerializer");
props.put("schema.registry.url", "<schema-registry-url>");
// MUST disable auto-registration in production
props.put(AbstractKafkaAvroSerDeConfig.AUTO_REGISTER_SCHEMAS, false);
```

### Building Source-Specific Records

```java
// T-AIS specific
AisSpecific aisInfo = AisSpecific.newBuilder()
    .setMessageType(AisPositionMessageType.CLASS_A)
    .setNmea("<raw-nmea-sentence>")
    .build();
report.setSourceSpecific(aisInfo);

// VMS specific
VmsSpecific vmsInfo = VmsSpecific.newBuilder()
    .setNaf("//SR//AD/EEC//FR/ITA//...")
    .setFishingSerialTripNumber(12345)
    .build();
report.setSourceSpecific(vmsInfo);

// LRIT specific
LritSpecific lritInfo = LritSpecific.newBuilder()
    .setMessageType(1)
    .setResponseType(100)
    .setReferenceId("REF-001")
    .setMessageId("MSG-001")
    .build();
report.setSourceSpecific(lritInfo);
```

## Checklist for Kafka Work

- [ ] Topic name follows `<application>.<logical-grouping>.<event-name>` convention
- [ ] Topic has `retention.bytes` configured
- [ ] AVRO schema registered in Confluent Schema Registry
- [ ] `auto.register.schemas=false` in production configuration
- [ ] ACLs configured for producer and consumer applications
- [ ] Schema changes follow evolution rules (union null defaults, no breaking changes)
- [ ] Schema changes submitted via merge request to development branch
- [ ] Monitoring configured for topic storage, consumer lag, and auth failures

## Common Pitfalls

### Avoid

- Enabling `auto.register.schemas` in production: always register schemas manually via Confluent Control Center
- Adding fields without default values: breaks backward compatibility
- Using DECIMAL type unless strictly required (financial accuracy): prefer FLOAT/DOUBLE
- Changing DECIMAL representation after data has been written
- Creating topics without prefix ACLs: the-project enforces naming via prefix ACLs
- Renaming fields without first adding aliases in reader schemas

### Prefer

- Union with null (`union { null, <type> }`) for optional fields
- Builder pattern (`Record.newBuilder()...build()`) for constructing AVRO records
- `SpecificDatumWriter`/`SpecificDatumReader` for type-safe serialization
- Confluent AVRO SerDe (`KafkaAvroSerializer`/`KafkaAvroDeserializer`) for Kafka integration
- Defining `retention.bytes` AND `retention.ms` for all topics

## References

- Kafka guidelines: `.opencode/docs/architecture/kafka/guideline.md`
- AVRO CDF README: `.opencode/docs/architecture/kafka/README.md`
- AVRO schema files: `.opencode/docs/architecture/kafka/avro/*.avdl`
- Java producer example: `.opencode/docs/architecture/kafka/java/AppTest.java`
- Confluent Schema Registry tutorial: https://docs.confluent.io/current/schema-registry/schema_registry_tutorial.html
- Kafka multi-tenancy docs: https://kafka.apache.org/documentation/#multitenancy
