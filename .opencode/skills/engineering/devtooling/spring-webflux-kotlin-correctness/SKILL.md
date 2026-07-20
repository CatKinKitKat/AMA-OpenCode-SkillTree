---
name: spring-webflux-kotlin-correctness
description: Correctness patterns for Spring WebFlux with Kotlin: suspension, error handling, backpressure, and testing without blocking. Use when auditing or fixing a non-obvious WebFlux/Kotlin bug, or when writing a new reactive endpoint with coroutines.
---
# Spring WebFlux Kotlin Correctness

Correctness patterns for Spring WebFlux with Kotlin coroutines: suspension, error handling, backpressure, and testing.

## When to Use

- [done] Writing a new reactive endpoint using suspend functions
- [done] Auditing an existing WebFlux service for bugs (blocking calls in reactive pipeline)
- [done] Fixing backpressure or memory-pressure issues
- [done] Writing tests for reactive endpoints without blocking

## Common Pitfalls

| Anti-pattern | Symptom | Fix |
|--------------|---------|-----|
| `block()` in suspending controller | Thread starvation, NPE on no thread | Use `awaitSingle()` or return Deferred directly |
| Missing `@Transactional` (reactive) | No rollback | Use `@Transactional` with R2DBC / explicit transaction API |
| Misuse of `Mono.delay` inside `flatMap` | Unbounded concurrency, memory pressure | Use `flatMapSequential` or concat with `delayElements` |
| `collectList()` on unbounded stream | OOM | Use `window`, `buffer`, or limit |
| Mixing WebFlux + Spring MVC | 50% response rate, port conflict | Pick one. Do not have both `spring-boot-starter-web` and `spring-boot-starter-webflux` |

## Correct patterns

```kotlin
// Controller with coroutines (non-blocking)
@GetMapping("/{id}")
suspend fun findById(@PathVariable id: String): Product =
    service.findById(id) ?: throw ResponseStatusException(HttpStatus.NOT_FOUND)

// Service with R2DBC + coroutines
suspend fun findById(id: String): Product? =
    productRepository.findById(id) ?: null
```

## Testing

```kotlin
@Test
fun `findById returns product`() = runTest {
  val product = service.findById("p1")
  assertEquals("p1", product?.id)
}
```

Use `@WebFluxTest` with `WebTestClient` instead of MockMvc for reactive tests.

## Anti-pattern table

| Anti-pattern | Symptom | Fix |
|--------------|---------|-----|
| `block()` in suspending controller | Thread starvation | Use `awaitSingle()` or return Deferred |
| Missing `@Transactional` (reactive) | No rollback | Use R2DBC/ReactiveTransactionManager |
| `Mono.delay` in `flatMap` | Unbounded concurrency | Use `flatMapSequential` |
| `collectList()` on unbounded stream | OOM | Use `window` / `buffer` / `limit` |

## Correct test pattern

```kotlin
@Test
fun `findById returns product`() = runTest {
  val product = service.findById("p1")
  assertEquals("p1", product?.id)
}
```

Use `@WebFluxTest` with `WebTestClient` for reactive tests.
