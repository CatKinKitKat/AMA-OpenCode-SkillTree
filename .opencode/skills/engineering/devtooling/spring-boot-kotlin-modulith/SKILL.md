---
name: spring-boot-kotlin-modulith
description: Design Spring Boot applications as runtime modules with Kotlin: internal packages, module boundaries, API consistency, and event-driven inter-module communication. Use when structuring a Spring Boot service with modulith, or when verifying that modules respect internal visibility.
---
# Spring Boot Kotlin Modulith

Design Spring Boot applications as runtime modules in Kotlin: internal packages, module boundaries, and event-driven inter-module communication.

## When to Use

- [done] Structuring a Spring Boot service with module boundaries (order, catalog, inventory)
- [done] Ensuring internal packages are not exposed via public API
- [done] Designing event-driven inter-module communication
- [done] Modularizing an existing Spring Boot service (extract layer to package)

## Workflow

### Module structure

```text
src/main/kotlin/com/example/catalog/
  CatalogApplication.kt
  api/            <- public REST API
  model/          <- domain model (internal)
  service/        <- internal business logic
  config/         <- infra config (internal)
```

### Internal visibility in Kotlin

```kotlin
// model is internal - not accessible from other packages
internal class Product(val id: String, val name: String)

// surface - public API
@RestController
class CatalogController(private val service: CatalogService)
```

## Pitfalls

- Kotlin `internal` is public on JVM bytecode. Enforce via ArchUnit tests or package-level module tests
- Cyclic module dependencies: use events (Spring ApplicationEvent) to break cycles
- `@Transactional` on `internal` service methods can cause ApplicationEvent leaks

## Module mapping

| Package | Visibility | Purpose |
|---------|-----------|---------|
| api/ | public | REST controllers, GraphQL resolvers |
| service/ | internal | business logic, transactions |
| model/ | internal | JPA entities, DTOs |
| config/ | internal | infrastructure (Kafka, DB, cache) |

## ArchUnit test (enforce boundaries)

```java
// test that service/ cannot see api/
ArchRule rule = noClasses()
  .that().resideInAPackage("..service..")
  .should().accessClassesThat().resideInAPackage("..api..");
```

```groovy
// Gradle dependency
testImplementation "com.tngtech.archunit:archunit-junit5-api:1.0.1"
```
