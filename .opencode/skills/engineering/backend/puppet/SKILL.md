---
name: puppet
description: Puppet manifests, classes, modules, and Hiera hierarchy for infrastructure as code. Use when working on the-backend-puppet-roles, profiles, Hiera data, or node configuration for the-legacy-app, the-surveillance-system, and the-project Platform deployment.
---

# Puppet - the-backend-puppet

Skill for **Puppet** in the `the-backend-puppet` repository (the-project Platform Infrastructure as Code). Reference documentation: [Puppet Core](https://www.puppet.com/docs/puppet/).

## Technology Stack (the-project)

- **Puppet:** 7.x (open-source)
- **Language:** Puppet DSL, Ruby (facts/functions), Bash (scripts)
- **Data:** Hiera 5 (YAML)
- **Runtime:** Linux (RHEL/CentOS 7/8)
- **Project:** `the-backend-puppet/code/environments/production/`

## When to Use This Skill

- Change roles (`role::the-backend::wls`, `role::the-backend::the-surveillance-system`) or profiles
- Add or edit Hiera data (nodes, groups, common)
- Create or modify manifests and modules (site-modules, profile, role)
- Configure the-legacy-app, the-surveillance-system, datasources, JMS via Puppet

## Structure (the-backend-puppet)

- **Roles:** `site-modules/role/manifests/the-backend/` - entry point by node type (wls, the-surveillance-system).
- **Profiles:** `site-modules/profile/manifests/the-backend/` - reusable configuration (wls_setup, wls, the-surveillance-system).
- **Hiera data:** `code/environments/production/data/nodes/` (and hierarchy in `hiera.yaml`).

## Hiera

- **hiera.yaml:** defines `defaults` (datadir, data_hash) and `hierarchy`.
- Lookup order: node-specific to location/group to common (example below).
- Per-node data: `nodes/%{trusted.certname}.yaml`.
- Per-OS data: `os/%{facts.os.family}.yaml`.

Hierarchy example:

```yaml
---
version: 5
defaults:
  datadir: data
  data_hash: yaml_data
hierarchy:
  - name: "Per-node data"
    path: "nodes/%{trusted.certname}.yaml"
  - name: "Per-OS defaults"
    path: "os/%{facts.os.family}.yaml"
  - name: "Common data"
    path: "common.yaml"
```

## Classes and Parameters

- Class parameters with type and (optionally) default via Hiera.
- Example: `class my_module (String $source, String $config) { ... }`.
- Values in Hiera: `my_module::source: 'value'`, `my_module::config: 'value'`.

## Nodes and Roles

- **role::the-backend::wls:** the-legacy-app servers (the-backend EARs, datasources, JMS).
- **role::the-backend::the-surveillance-system:** the-surveillance-system servers (RPM Module 3, imdate).
- Orchestrator: specific profile for deploy/restart on the-surveillance-system nodes via SSH.

## Best Practices

- Use Hiera for data, do not hardcode values in manifests.
- Keep roles thin (only include profiles). Keep logic in profiles.
- Keep class and parameter names aligned with conventions (namespace, snake_case).

## Reference

- Puppet documentation: https://www.puppet.com/docs/puppet/
- Context7 library ID: `/websites/help_puppet_core_current`
