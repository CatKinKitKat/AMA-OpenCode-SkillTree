---
name: jaxrs-jersey
description: JAX-RS with Jersey for REST APIs in Java-resources, Path, GET/POST, Produces, Consumes. Use for legacy the-backend REST code paths only; for the-backend migration target work use Java 25 + Spring Boot 4.0.2 on Tomcat 11.
---

# JAX-RS Jersey - the-backend (Legacy)

Skill for **REST** APIs with **JAX-RS (Jersey)** in legacy the-backend code paths. For current the-backend migration target implementation, prefer Spring Boot controllers and the `java-spring-microservices` skill.

## Technology Stack (the-backend)

- **JAX-RS:** Jersey (reference implementation)
- **Runtime:** Legacy runtime only
- **Module:** `alerts-services-rest` (legacy packaging references may still exist in historical docs)
- **Base URL:** Environment-specific legacy path

## When to Use This Skill

- Create or modify REST endpoints in the-backend (alerts, rules, distribution-lists, notifications)
- Define path, HTTP methods, Produces/Consumes
- Handle parameters (path, query, body) and JSON responses (Jackson)

## Resource Pattern

```java
@Path("/rest")
@Consumes(MediaType.APPLICATION_JSON)
@Produces(MediaType.APPLICATION_JSON)
public class MyResource {

  @GET
  @Path("/alerts")
  public Response listAlerts(@QueryParam("status") String status) {
    // ...
  }

  @GET
  @Path("/alerts/{id}")
  public Response getAlert(@PathParam("id") Long id) {
    // ...
  }

  @POST
  @Path("/alerts")
  public Response createAlert(AlertDto dto) {
    // ...
  }

  @PUT
  @Path("/alerts/{id}")
  public Response updateAlert(@PathParam("id") Long id, AlertDto dto) {
    // ...
  }

  @DELETE
  @Path("/alerts/{id}")
  public Response deleteAlert(@PathParam("id") Long id) {
    // ...
  }
}
```

- **@Path:** URI for resource or method.
- **@GET / @POST / @PUT / @DELETE:** HTTP method.
- **@PathParam / @QueryParam:** path and query parameters.
- **@Consumes / @Produces:** body format (usually `application/json`).

## the-backend Endpoints (Reference)

- **Alerts:** GET/POST /alerts, GET/PUT/DELETE /alerts/{id}, GET /alerts/{id}/history
- **Rules:** GET/POST /rules, PUT/DELETE /rules/{id}
- **Distribution lists:** GET/POST /distribution-lists, PUT /distribution-lists/{id}
- **Notifications:** POST /notifications, GET /notifications/{id}

Content-Type: `application/json`. Charset UTF-8. Authentication depends on the environment (Basic Auth / Token).

## Best Practices

- Use DTOs for request/response and Jackson for JSON.
- Keep responses consistent (status codes, error messages).
- Validate input (Bean Validation when applicable).

## Reference

- Eclipse Jersey: https://eclipse-ee4j.github.io/jersey/
- Context7 library ID: `/eclipse-ee4j/jersey`
