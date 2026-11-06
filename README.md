# Stalemated's Stonecutter Template

A [Stonecutter](https://stonecutter.kikugie.dev/) template for Fabric, Forge and NeoForge, from 1.20 to 26.3. [S-Lib](https://github.com/Stalemated/s-lib) comes as an optional dependency: a mod that doesn't use it can drop it in a few steps.

---

## Requirements

- JDK 25 to run Gradle.
- Python 3.10 or newer for `scripts/new_mod.py`.
- S-Lib in your mavenLocal, because `gradle.properties` sets `slibLocal=true`. Once S-Lib 4.0.0 is on Modrinth, delete that line to download S-Lib from there instead.

## Create a new mod

1. Copy the template or create a repository from it on GitHub.
2. Rename it:

```bash
python scripts/new_mod.py --id my_mod --name "My Mod" --package com.example.mymod
```

   - `--class-prefix` sets the prefix of the main classes (default: the id in PascalCase, `MyMod`).
   - `--artifact` sets the jar and Maven name (default: the id with dashes, `my-mod`).
   - `--dry-run` prints the changes without writing them.
3. Rewrite this README and delete `scripts/`.
4. Fill `mod.description`, `mod.author`, `mod.sources`, `publish.modrinth_id` and `publish.curseforge_id` in `stonecutter.properties.toml`.

## Layout

| File                                                                 | Responsibility                                                                                                                     |
|----------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| `settings.gradle.kts`                                                | Plugins and the list of nodes (`match(version, loaders...)`), plus `vcsVersion`                                                    |
| `stonecutter.gradle.kts`                                             | Active node, loader constants and string replacements                                                                              |
| `stonecutter.properties.toml`                                        | Mod data, dependency versions and publishing data, per version and per loader                                                      |
| `build.fabric.gradle.kts`                                            | Loom through loom-back-compat, Fabric API and runs                                                                                 |
| `build.forge.gradle.kts`                                             | ModDevGradle legacyforge, mixin refmap and `MixinConfigs`                                                                          |
| `build.neoforge.gradle.kts`                                          | ModDevGradle; renames `neoforge.mods.toml` to `mods.toml` before 1.20.5                                                            |
| `buildSrc/.../mod-conventions.gradle.kts`                            | Java version, coordinates, metadata expansion, LICENSE in the jar, JUnit, `buildAndCollect`                                        |
| `buildSrc/.../mod-publishing.gradle.kts`                             | maven-publish, Modrinth and CurseForge                                                                                             |
| `buildSrc/.../slib.gradle.kts`                                       | The S-Lib layer: repositories, S-Lib, YACL and Mod Menu                                                                            |
| `buildSrc/.../neoforge-mutex.gradle.kts`, `publish-mutex.gradle.kts` | Run one NeoForge decompile and one mavenLocal publish at a time                                                                    |
| `src/main/java/.../TemplateMod.java`, `TemplateModClient.java`       | Common and client init                                                                                                             |
| `src/main/java/.../loader/`                                          | One entrypoint per loader, each inside its `//? if <loader>` block                                                                 |
| `src/main/java/.../mixin/`                                           | An example mixin                                                                                                                   |
| `src/main/java/.../config/`                                          | The S-Lib layer: config model, manager and screen                                                                                  |
| `src/main/resources/`                                                | `fabric.mod.json`, `META-INF/mods.toml` (Forge), `META-INF/neoforge.mods.toml`, `pack.mcmeta` (Forge), the mixin config and assets |
| `scripts/`                                                           | `new_mod.py` and its tests                                                                                                         |

## Useful commands

The sources in git are written for `1.20.1-fabric`. To work on another node:

```bash
./gradlew "Set active project to 1.21.1-neoforge"
```

Go back before committing:

```bash
./gradlew "Reset active project"
```

Run, build and test:

```bash
./gradlew :1.21.1-neoforge:runClient
```

```bash
./gradlew :1.21.1-neoforge:runServer
```

```bash
./gradlew build
```

```bash
./gradlew buildAndCollect
```

- Each node runs in `run/<node>`.
- `build` builds and tests every node; `:<node>:build` builds one.
- `buildAndCollect` copies the jars to `build/libs/<mod version>/`.

## Versions and loaders

| Node    | Minecraft                                   | Fabric | Forge | NeoForge |
|---------|---------------------------------------------|--------|-------|----------|
| 1.20.1  | 1.20 - 1.20.1                               | Yes    | Yes   |          |
| 1.20.4  | 1.20.2 - 1.20.4 (NeoForge: 1.20.4)          | Yes    |       | Yes      |
| 1.20.6  | 1.20.5 - 1.20.6                             | Yes    |       | Yes      |
| 1.21.1  | 1.21 - 1.21.1                               | Yes    |       | Yes      |
| 1.21.4  | 1.21.2 - 1.21.4                             | Yes    |       | Yes      |
| 1.21.5  | 1.21.5                                      | Yes    |       | Yes      |
| 1.21.6  | 1.21.6                                      |        |       | Yes      |
| 1.21.8  | 1.21.6 - 1.21.8 (NeoForge: 1.21.7 - 1.21.8) | Yes    |       | Yes      |
| 1.21.10 | 1.21.9 - 1.21.10                            | Yes    |       | Yes      |
| 1.21.11 | 1.21.11                                     | Yes    |       | Yes      |
| 26.1    | 26.1                                        | Yes    |       | Yes      |
| 26.2    | 26.2                                        | Yes    |       | Yes      |
| 26.3    | 26.3                                        | Yes    |       | Yes      |

### Remove a version

1. If the version holds the active node or `vcsVersion`, move to a node you keep first:
   - run `./gradlew "Set active project to <kept node>"`, which also updates `stonecutter active` in `stonecutter.gradle.kts`;
   - set `vcsVersion = "<kept node>"` in `settings.gradle.kts`.
2. Remove its loaders from its `match(...)` line in `settings.gradle.kts`, or the whole line.
3. Optionally, delete its tables from `stonecutter.properties.toml`.
4. Run `./gradlew build`.

### Remove a loader

1. Move the active node and `vcsVersion` to a node you keep, as above.
2. Remove the loader from every `match(...)` line.
3. Delete its files:
   - Fabric: `build.fabric.gradle.kts`, `fabric.mod.json`, `loader/TemplateModFabric.java` and `loader/TemplateModFabricClient.java`.
   - Forge: `build.forge.gradle.kts`, `META-INF/mods.toml`, `pack.mcmeta` and `loader/TemplateModForge.java`.
   - NeoForge: `build.neoforge.gradle.kts`, `META-INF/neoforge.mods.toml` and `loader/TemplateModNeoForge.java`.
4. Optionally, delete its keys from `stonecutter.properties.toml`:
   - Fabric: `deps.fabric_loader`, `loomx.loom_version`, `deps.fabric_api` and `deps.modmenu`.
   - Forge: `deps.forge_loader`.
   - NeoForge: `mod.neoforge_compat` and `deps.neo_loader`.
5. Leave `constants { match(loader, "fabric", "neoforge", "forge") }` in `stonecutter.gradle.kts` as it is, so every `//? if <loader>` block still parses.
6. Run `./gradlew build`.

### Add a version

1. Add `match("<version>", "<loaders>")` to `settings.gradle.kts`.
2. Copy the tables of the closest version in `stonecutter.properties.toml` and update `mod.mc_releases`, `mod.mc_compat`, `deps.fabric_api`, `deps.neo_loader`, `deps.yacl` and `deps.modmenu`. When a loader supports fewer releases than the version table lists, give that loader's table its own `mod.mc_releases`, as `[neoforge."1.20.4"]` does.
3. Fix what no longer compiles with versioned comments, for example `//? if >=1.21.9 {`.

## S-Lib

The S-Lib layer adds:

- S-Lib, and YACL as a compile-only dependency plus a development runtime one.
- Mod Menu in Fabric runs.
- An example synced config in `config/`, its YACL screen and the config button (`SLibConfigScreens`).
- A JUnit test that builds the screen and checks the lang file (`SLibTesting`).
- The `s_lib` dependency in the three metadata files, and `s-lib`/`yacl` as publishing relations.

### Where S-Lib comes from

- With the Gradle property `slibLocal`, from mavenLocal: `com.stalemated.lib:s-lib-<loader>:<deps.slib>+<mc>`.
  - The template sets `slibLocal=true` in its `gradle.properties`.
  - Publish S-Lib first with `./gradlew publishToMavenLocal` in the S-Lib repository.
- Without it, from the Modrinth maven: `maven.modrinth:s-lib:<deps.slib>+<mc>-<loader>`. This needs S-Lib versions whose Modrinth version number names the loader, from 4.0.0 on.
- Fabric nodes resolve their mods while Gradle configures the build, so a missing S-Lib breaks every command, including `"Set active project to ..."`.
- `-PnoYacl` starts runs without YACL, Mod Menu and the Forge parsers.

### Remove S-Lib

1. In `stonecutter.properties.toml`:
   - delete `deps.slib` and every `deps.yacl` and `deps.modmenu` line;
   - set `publish.requires = []` and `publish.optional = []`.
2. Remove `id("slib")` from the three `build.<loader>.gradle.kts`.
3. Delete `buildSrc/src/main/kotlin/slib.gradle.kts`.
4. Delete the `config` package under `src/main/java` and its test under `src/test/java`.
5. Remove `TemplateModConfigs.register();` from `TemplateMod.init()`, the `SLibConfigScreens.register(...)` line from `TemplateModClient.init()`, and their imports.
6. Remove the `"s_lib"` dependency from `fabric.mod.json` and the `s_lib` `[[dependencies.${id}]]` block from both `mods.toml` files.
7. Delete `assets/<mod id>/lang/en_us.json` if nothing else uses it.
8. Delete `slibLocal=true` from `gradle.properties`.
9. Run `./gradlew build`.

## Publishing

1. Fill `publish.modrinth_id` and `publish.curseforge_id`, and set `publish.type` to `stable`, `beta` or `alpha`.
2. Add a `## <mod.version>` section to `Changelog.md`: that section is the published changelog.
3. Set the `MODRINTH_TOKEN` and `cf_token` environment variables.
4. Check the upload without sending it. A dry run needs no token:

```bash
./gradlew publishMods -PpublishDryRun
```

5. Publish every node, or one with `:<node>:publishMods`:

```bash
./gradlew publishMods
```

- Each file is published with the version number `<mod.version>+<mc>-<loader>`, so the Modrinth maven serves the right jar for each loader.
- `mod.mc_releases` lists the Minecraft versions shown on Modrinth and CurseForge.
- `mod.environment` (`both`, `client` or `server`) sets Fabric's `environment` and CurseForge's client and server flags.
- `./gradlew publishToMavenLocal` publishes `<mod.group>:<mod.artifact>-<loader>:<mod.version>+<mc>` for other local projects.

## License

[MIT](LICENSE)
