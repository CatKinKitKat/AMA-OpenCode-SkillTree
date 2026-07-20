# Clash Mi on macOS: observed config layout

Observed app identity
- App: `/Applications/Clash Mi.app`
- App container: `~/Library/Containers/com.nebula.clashmi`
- Group container: `~/Library/Group Containers/group.com.nebula.clashmi`
- Running processes included app UI and system extension service.

Ground-truth files
- Controller: `~/Library/Group Containers/group.com.nebula.clashmi/service.json`
  - `core_path` -> `~/Library/Group Containers/group.com.nebula.clashmi/profiles/994560448.yaml`
  - `core_path_patch_final` -> `~/Library/Group Containers/group.com.nebula.clashmi/service_core_patch_final.json`
- Profile metadata: `~/Library/Group Containers/group.com.nebula.clashmi/profiles.json`
  - `current_id` -> `994560448.yaml`
  - remote `url` present, so edits can be overwritten by subscription refresh
  - fields present for overlay merges: `overwrite_rules`, `overwrite_proxy_groups`, `proxy_groups`, `rules`, `rules_for_proxy_groups`
- Generated runtime: `~/Library/Group Containers/group.com.nebula.clashmi/service_core_runtime_profile.yaml`
  - inspect only. Do not treat as primary durable edit target
- Patch metadata: `~/Library/Group Containers/group.com.nebula.clashmi/profile_patchs.json`
  - drives the active patch id and local patch inventory
- Local patch dir: `~/Library/Group Containers/group.com.nebula.clashmi/profilePatchs/`
  - YAML patches live here and can be attached to the active subscription by setting the subscription profile's `patch` field in `profiles.json`

Patch / overlay evidence
- App binary strings showed patch UI / merge behavior markers:
  - `profile_patchs.json`
  - `package:clashmi/screens/profiles_patch_board_screen.dart`
  - `package:clashmi/screens/add_profile_patch_by_url_screen.dart`
  - `package:clashmi/screens/add_profile_patch_by_import_from_file_screen.dart`
  - `profile_patch_buildin_overwrite`
  - `profile_patch_buildin_no_overwrite`
  - `overwrite-rules`
  - `overwrite-sub-rules`
- Practical implication: if the user wants custom rules that survive subscription refresh, prefer attaching a profile patch to the subscription rather than hand-editing the subscribed profile.
- Session-confirmed durable wiring for Clash Mi:
  - patch file in `profilePatchs/custom-rules.yaml`
  - patch inventory in `profile_patchs.json`
  - target subscription's `patch` field set in `profiles.json`
  - if needed for immediate runtime parity, `service.json` may also show `core_path_patch`, but the durable source of truth is the profile metadata + patch inventory.

Practical rule
- Primary user-editable source profile:
  - `~/Library/Group Containers/group.com.nebula.clashmi/profiles/994560448.yaml`
- Avoid editing runtime output:
  - `~/Library/Group Containers/group.com.nebula.clashmi/service_core_runtime_profile.yaml`
- Prefer patch layer for durable customization when subscription updates are enabled.

Useful probes
```bash
ps aux | rg -i 'Clash Mi|clashmi|mihomo|sing-box|clash'
lsof -p <pid> 2>/dev/null | rg -i 'yaml|json|profile|config|group containers|containers'
rg -n 'core_path|current_id|runtime-profile-save-path|url' "$HOME/Library/Group Containers/group.com.nebula.clashmi"
strings -a '/Applications/Clash Mi.app/Contents/Frameworks/App.framework/Versions/A/App' | rg 'profile_patch|overwrite-rules|overwrite-sub-rules|add_profile_patch|patch_board'
```

Observed warnings/logs
- `app.log` showed `VpnError:FullDiskAccessPermissionRequired`
- `service_core.log` showed rule-provider fetch errors and `bind: address already in use` on `:7890`

Rule syntax cleanup observed in session
- Normalize bad host rules before import:
  - bad: `DOMAIN,http://43.156.154.132:8668/,DIRECT`
  - safer: `DOMAIN,43.156.154.132,DIRECT`
- Remove trailing slash from domain suffix rules:
  - bad: `DOMAIN-SUFFIX,fk.hshwk.org/,DIRECT`
  - safer: `DOMAIN-SUFFIX,fk.hshwk.org,DIRECT`

Implications
- If behavior does not match edited config, inspect whether:
  1. subscription refresh overwrote the profile
  2. runtime regeneration copied from source after launch
  3. a patch layer is available but not attached to the current profile
  4. service failed for unrelated port/TCC reasons
