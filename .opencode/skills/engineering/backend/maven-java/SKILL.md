---
name: maven-java
description: Maven POM structure, dependency management, and build lifecycle for the-project Java projects. For the-backend/tomcat, use this skill to manage independent Maven modules, Spring Boot parent/BOM settings, WAR packaging for Tomcat 11, and shared/external dependencies.
---

# Maven Java - the-backend/Tomcat, the-surveillance-system, the-web-portal

Skill for **Maven** Java projects in the the-backend, the-surveillance-system, and the-web-portal repositories. Reference documentation: [Apache Maven](https://maven.apache.org/).

## Technology Stack (the-project)

| Project | Java | Maven | Packaging |
|---------|------|-------|-----------|
| **the-backend (tomcat)** | 25 | 3.9+ | WAR (services + engine), JAR (model/utils/proxies) |
| **the-surveillance-system** | 1.8 | 3.5.3+ | RPM (via Ant/Maven) |
| **the-web-portal** | 1.8 | 3.x | JAR (portlets the-portal-platform) |

## When to Use This Skill

- Modify or create Maven modules (parent POM, child modules)
- Manage dependencies and versions (Spring Boot, Jakarta, Hibernate, Oracle JDBC, etc.)
- Configure plugins (compiler, surefire, war, spring-boot, install-file, etc.)
- Interpret the-backend/tomcat modular structure (independent modules, no reactor aggregation)

## POM Basics

- **groupId / artifactId / version:** identify the artifact.
- **packaging:** jar, war, ear, pom (aggregator).
- **parent:** inherit configuration and dependencyManagement from a parent POM.
- **modules:** list of sub-modules in multi-module projects.

## the-backend/Tomcat Structure

```
the-backend/tomcat/
+-- alerts-pom/            # Parent POM/BOM (packaging pom; no module aggregation)
+-- alerts-utils/          # JAR
+-- alerts-model/          # JAR
+-- alerts-proxies/        # JAR
+-- alerts-services-rest/  # WAR (Tomcat)
+-- alerts-engine-processor/ # WAR (Tomcat)
+-- libs/external-notification-model.jar # External dependency installed during validate
```

- Parent POM (`alerts-pom`) inherits from `spring-boot-starter-parent:4.0.2` and sets `java.version=25`.
- Child modules are **independent projects** (build/test individually) and inherit shared dependency/plugin management from parent.
- Deployables are WAR files for Tomcat 11, replacing legacy EAR/the-legacy-app deployment.

## Build Lifecycle

- `mvn clean` - cleans `target`.
- `mvn compile` - compiles.
- `mvn test` - runs tests (JUnit, SoapUI when configured).
- `mvn package` - generates JAR/WAR.
- `mvn install` - installs to the local repository.

Typical the-backend/tomcat flow:

1. `cd alerts-pom && mvn clean install`
2. Build modules in dependency order (`utils` -> `model` -> `proxies` -> `services-rest` / `engine-processor`)
3. Deploy generated WARs to Tomcat 11

## Dependencies (the-project Context)

- **the-backend/tomcat:** Spring Boot 4.0.2, Spring MVC/JPA, Jakarta APIs, Hibernate Spatial, Oracle JDBC (`ojdbc11`), ActiveMQ, SpringDoc, SLF4J/Logback.
- **the-backend external import:** `com.the-project.notification:external-notification-model` from local `libs/external-notification-model.jar` via `maven-install-plugin`.
- **the-web-portal:** the-portal-platform kernel, Spring, Apache CXF.
- **the-surveillance-system:** CLS Commons, Oracle DB, Kafka, JMS, Protobuf, CXF.

Avoid version conflicts: use `dependencyManagement` in the parent and exclude transitive dependencies when needed.

## Best Practices

- Centralize versions in the parent POM.
- Use correct scopes: compile, provided, test.
- Do not duplicate dependencies across sibling modules. Declare them in the module that uses them.

## Reference

- Apache Maven: https://maven.apache.org/
- Context7 library ID: `/apache/maven`
