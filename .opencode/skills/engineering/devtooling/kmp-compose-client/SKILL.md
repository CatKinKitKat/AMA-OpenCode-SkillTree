---
name: kmp-compose-client
description: Compose Multiplatform shared UI across Android, iOS, Desktop, and Web. Use when building a cross-platform Compose UI, integrating platform-specific resources, or debugging Compose Multiplatform build issues.
---
# KMP Compose Client

Compose Multiplatform shared UI: Android, iOS, Desktop, Web.

## When to Use

- [done] Building a new cross-platform Compose UI feature
- [done] Integrating platform-specific resources (Android: vector drawables, iOS: SF Symbols)
- [done] Debugging KMP build issues ( Gradle cache, iOS framework packaging, JS canvas)
- [done] Migrating an existing app feature to Compose Multiplatform

## Tech Stack

- Compose Multiplatform 1.5+
- Kotlin 1.9+
- Gradle (KMP plugin)
- Skia / CanvasKit (Web rendering)
- iOS: CocoaPods for framework packaging
- Android: Material3 Compose

## Workflow

### Setup

```kotlin
// build.gradle.kts
plugins {
  id("org.jetbrains.compose") version "1.5.10"
  id("org.jetbrains.kotlin.multiplatform") version "1.9.22"
}

kotlin {
  jvm()
  android()
  iosX64(); iosArm64(); iosSimulatorArm64()
  js { browser() }
  sourceSets {
    val commonMain by getting { dependencies { implementation(compose.runtime) } }
    val androidMain by getting { dependencies { implementation(compose.ui) } }
    val iosMain by getting { dependencies { ... } }
  }
}
```

### Shared UI

```kotlin
@Composable
fun Greeting(name: String) {
  Text(text = "Hello, $name!", style = MaterialTheme.typography.headlineMedium)
}
```

### Platform resources

- Common: `drawable/`, `font/` under `src/commonMain/resources/`
- Android: overrides in `src/androidMain/res/`
- iOS: overrides in `src/iosMain/resources/`

## Pitfalls

- iOS simulator runs on arm64 now. Always use `iosSimulatorArm64` unless you are on Intel Mac
- Web: use `CanvasKit` renderer (not DOM renderer) for performance
- Webpack / WASM: Compose for Web uses WASM by default. Ensure CI installs Node
- iOS release builds need `xcodebuild -workspace` (not Gradle alone)
