---
name: spring-boot-modulith-reactive-kotlin
description: Build reactive Spring Boot services with Kotlin coroutines + Kotlin Modulith pattern: reactive repositories, internal module boundaries, and event-driven communication without blocking calls.
---
# Spring Boot Modulith Reactive Kotlin

Reactive Spring Boot services with Kotlin coroutines and Modulith module boundaries.

## When to Use

- [done] Building a new reactive Spring Boot service with Kotlin
- [done] Organizing a coroutine-based service into internal modules
- [done] Migrating a blocking Modulith service to reactive (WebFlux)
- [done] Designing event-driven reactive flows between modules

## Tech Stack

- Spring Boot 3+ (WebFlux)
- Kotlin 1.9+ with coroutines
- Spring for Apache Kafka (reactive) or Reactor Kafka
- R2DBC (reactive database access)
- Kotlin Modulith pattern (package-private internal modules)

## Workflow

### Coroutine controller

```kotlin
@GetMapping("/products/{id}")
suspend fun getProduct(@PathVariable id: String): ResponseEntity<Product> =
    service.findById(id)
        ?.let { ResponseEntity.ok(it) }
        ?: ResponseEntity.notFound().build()
```

### Reactive repository

```kotlin
interface ProductRepository : ReactiveCrudRepository<Product, String>
```

### Module structure

Same as non-reactive: api/ (public), service/ (internal), model/ (internal).

## Pitfalls

- Do not call `block()` in coroutine context. Defeats the purpose
- R2DBC transactions differ from JDBC: no `@Transactional` rollback on `IllegalStateException`
- Modulith internal packages: enforce with ArchUnit tests
- Do not share coroutine scope between modules. Publish events instead
