---
name: jvm-kotlin-toolchain
description: Configure Gradle/Maven JVM and Kotlin compiler toolchains with deterministic versions across developer machines and CI. Use when a build breaks due to different JDK versions, when pinning Kotlin compiler args, or when reproducing CI locally.
---
# JVM Kotlin Toolchain

Pin JDK and Kotlin compiler versions using Gradle/Maven toolchains for reproducible builds across dev and CI.

## When to Use

- [done] Build breaks "works on my machine" (different JDK version locally vs CI)
- [done] Kotlin compiler version mismatch (lang-level vs compiler plugin version)
- [done] Multi-platform project (JVM + JS + Native) needs consistent Kotlin version
- [done] Reproducing CI build locally (toolchain auto-installs matching JDK)

## Workflow

### Gradle (toolchains)

```kotlin
java {
  toolchain {
    languageVersion.set(JavaLanguageVersion.of(17))
    vendor.set(JvmVendorSpec.ADOPTIUM)
  }
}
kotlin {
  jvmToolchain {
    languageVersion.set(JavaLanguageVersion.of(17))
  }
}
```

### Gradle (Kotlin compiler args)

```kotlin
tasks.withType<KotlinCompile> {
  kotlinOptions {
    jvmTarget = "17"
    freeCompilerArgs = listOf("-Xjsr305=strict", "-opt-in=kotlin.RequiresOptIn")
  }
}
```

### Maven (toolchains)

```xml
<properties>
  <maven.compiler.source>17</maven.compiler.source>
  <maven.compiler.target>17</maven.compiler.target>
  <kotlin.version>1.9.22</kotlin.version>
</properties>

<build>
  <plugins>
    <plugin>
      <groupId>org.jetbrains.kotlin</groupId>
      <artifactId>kotlin-maven-plugin</artifactId>
      <version>${kotlin.version}</version>
    </plugin>
  </plugins>
</build>
```

## Pitfalls

- Kotlin compiler version must match the Kotlin Gradle plugin version (do not mismatch)
- JDK toolchain version must be <= target environment JDK version
- `jvmTarget` must match `JavaLanguageVersion`. Otherwise ABI mismatch
- Check `org.gradle.java.home` is NOT set in CI (so toolchain auto-install works)
