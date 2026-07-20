---
name: java-spring-microservices
description: the-backend backend migration and development on Java 25 + Spring Boot 4.0.2 running on Tomcat 11. Use when implementing or migrating the-backend services from legacy JDK8/the-legacy-app deployments to the the-project target runtime, with independent Maven modules and external Notification Engine import.
---

# Java Spring - the-backend/Tomcat (the-project)

This skill documents the **actual the-backend/tomcat implementation model** and migration target.

## Technology Stack (the-backend Target)

- **Java**: 25
- **Spring Boot Parent**: 4.0.2 (`spring-boot-starter-parent`)
- **Runtime Container**: Apache Tomcat 11
- **Build Tool**: Maven 3.9+
- **Persistence**: Oracle DB + Spring Data JPA (Hibernate)
- **Messaging**: ActiveMQ (`spring-boot-starter-activemq`)
- **API Docs**: SpringDoc OpenAPI (`springdoc-openapi-starter-webmvc-ui`)
- **Namespaces**: Jakarta (`jakarta.*`)

## Migration Baseline

- Source platform: **JDK 8 + the-legacy-app + EAR deployment**
- Target platform: **JDK 25 + Spring Boot 4.0.2 + Tomcat 11 + WAR deployment**
- Do not use Java 11 / Spring Boot 2.7.x assumptions for the-backend target modules.

## Module and Dependency Model (the-backend)

the-backend/tomcat is organized as **independent Maven projects** with a shared parent/BOM:

- `alerts-pom` (parent POM, packaging `pom`)
- `alerts-utils` (JAR)
- `alerts-model` (JAR)
- `alerts-proxies` (JAR)
- `alerts-services-rest` (WAR)
- `alerts-engine-processor` (WAR)

Rules:

- Keep modules independent and buildable on their own.
- Inherit shared versions/plugins from `alerts-pom`.
- **Exception**: the-backend imports Link Notification Engine model from:
  - `the-backend/tomcat/libs/external-notification-model.jar`
  - installed via `maven-install-plugin` as `com.the-project.notification:external-notification-model:3.0.0-SNAPSHOT`.

## When to Use This Skill

Use this skill when:

- [done] Migrating the-backend code from the-legacy-app/EAR to Tomcat/WAR
- [done] Updating Spring Boot/Jakarta code in the-backend modules
- [done] Creating/changing REST endpoints in `alerts-services-rest`
- [done] Updating engine logic in `alerts-engine-processor`
- [done] Managing shared model/proxy/utils dependencies
- [done] Resolving parent POM and dependency management issues

## the-backend/Tomcat Build and Deploy Flow

```bash
# 1) Install parent BOM
cd the-backend/tomcat/alerts-pom
mvn clean install

# 2) Build shared jars
cd ../alerts-utils && mvn clean install
cd ../alerts-model && mvn clean install
cd ../alerts-proxies && mvn clean install

# 3) Build deployables
cd ../alerts-services-rest && mvn clean package
cd ../alerts-engine-processor && mvn clean package

# 4) Deploy WARs to Tomcat 11
# - alerts-services-rest/target/alerts-services-rest.war
# - alerts-engine-processor/target/alerts-engine-processor.war
```

Use local helper scripts when available (`deploy-local-tomcat.*`, `build-all-modules.*`, `test-all-modules.*`).

## Required Patterns

### Architecture
- **MUST** keep the-backend modules decoupled (no hidden cross-module coupling).
- **MUST** use parent POM for version/plugin alignment.
- **MUST** package deployable services as WAR for Tomcat 11.

### Dependency Management
- **MUST** centralize shared versions in `alerts-pom`.
- **MUST** keep internal dependencies (`model`, `utils`, `proxies`) version-aligned with `${project.version}`.
- **MUST** use Jakarta-compatible dependencies (`jakarta.*`) in migrated modules.

### Runtime
- **MUST** use provided Tomcat dependency scope in WAR modules.
- **MUST** keep Oracle JDBC and JPA/Hibernate configuration aligned with module runtime.
- **MUST** keep ActiveMQ integration aligned with the-backend environment properties.

## Practical Dependency Notes

Common dependencies found in the-backend/tomcat modules:

- `spring-boot-starter-web`
- `spring-boot-starter-data-jpa`
- `spring-boot-starter-activemq`
- `spring-boot-starter-mail`
- `springdoc-openapi-starter-webmvc-ui`
- `org.hibernate.orm:hibernate-spatial`
- `org.geolatte:geolatte-geom`
- `com.oracle.database.jdbc:ojdbc11`
- `com.the-project.notification:external-notification-model`

## Checklist for the-backend Changes

- [ ] Parent POM already installed (`alerts-pom`)
- [ ] Correct module-level dependencies declared
- [ ] No legacy the-legacy-app/EAR assumptions in new code
- [ ] WAR packaging preserved for REST and engine modules
- [ ] Jakarta imports used in migrated classes
- [ ] Notification model dependency resolves from local install/plugin step
- [ ] Module tests pass (`mvn test` where enabled)

## Common Pitfalls

### Avoid
- Using old Java EE (`javax`) imports in migrated classes when `jakarta` is required
- Reintroducing EAR/the-legacy-app-specific deployment assumptions
- Coupling modules directly instead of relying on declared Maven dependencies
- Forgetting notification model local install step during clean builds

### Prefer
- Parent-managed versions and plugins
- Explicit module boundaries and dependency contracts
- Tomcat 11-compatible WAR deployment behavior

## References

- the-backend/tomcat parent POM: `the-backend/tomcat/alerts-pom/pom.xml`
- the-backend/tomcat README: `the-backend/tomcat/README.md`
- Maven docs: https://maven.apache.org/
