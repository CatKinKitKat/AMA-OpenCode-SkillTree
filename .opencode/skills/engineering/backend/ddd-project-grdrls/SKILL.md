---
name: ddd-project-grdrls
description: >
Use when a user asks the agent to design, scaffold, refactor, or implement a non-trivial software project, service, platform, or architecture. Enforces slow-is-smooth DDD discipline: strategic design first, tactical design second, implementation last; prevents rushing into code before domain boundaries, ubiquitous language, ACLs, and pure domain models are established.
tags: 
version: 1
---


Goal
- Prevent the agent from becoming an eager code generator on project work.
- Force a production-grade DDD path: domain first, code second.
- Surface missing business context before implementation.
- Protect against weak typing, boundary leakage, hidden filtering logic, and infrastructure-driven design.

Activate when
- The user asks to start a new software project.
- The user asks for architecture, scaffolding, system design, or project structure.
- The user asks to refactor an existing codebase with unclear boundaries.
- The user describes symptoms like dicts everywhere, missing serialized fields, REST/WSS mismatch, silent candidate drops, if/else routing sprawl, or domain logic leaking into handlers/services.
- The task is large enough that rushing into code would create design debt.

Do not use when
- The task is a tiny one-file script with no meaningful domain.
- The user asks for a narrowly scoped bugfix inside an already-confirmed model.

Non-negotiable rules
1. Do not jump straight to implementation for non-trivial projects.
2. Work in 3 explicit stages only:
   - Stage 1: Strategic Design
   - Stage 2: Tactical Design
   - Stage 3: Implementation & Evolution
3. At the end of each stage, summarize outputs and stop.
4. Do not continue unless the user explicitly confirms: "继续", "确认进入下一阶段", or equivalent.
5. If key business facts are missing, ask targeted clarification questions before modeling.
6. Enforce ubiquitous language. Once terms are chosen, reuse them consistently.
7. Keep business logic in the domain layer, not in controllers, handlers, jobs, routers, or application services.
8. Separate external schemas from domain models with an Anti-Corruption Layer.
9. Separate pure computation from policy/routing/filtering.
10. Prefer strong typed domain objects over ad hoc dict/json maps for core entities.

Default collaboration protocol
1. First identify whether enough information exists to start Stage 1.
2. If not enough, ask only the minimal blocking questions:
   - project name
   - project goal
   - core business flow
   - key entities/objects
   - external systems/integrations
   - constraints
   - non-functional requirements
   - existing system/repo, if any
3. Then produce Stage 1 only.
4. Wait for confirmation.
5. Then produce Stage 2 per bounded context.
6. Wait for confirmation.
7. Then implement one aggregate or one use case at a time in Stage 3.

Required design lens
When reviewing or designing a system, always test for these failure modes:
- weakly typed core models
- serialized field loss
- API DTOs mixed with domain entities
- external payloads leaking into domain logic
- data providers doing business inference
- pure calculations mixed with filtering or routing
- silent discard logic inside computation paths
- application services carrying business rules
- persistence model dictating aggregate boundaries
- inconsistent terminology across modules

Preferred target architecture
Organize the design around these layers when applicable:
1. Domain Model Layer
   - Entities
   - Value Objects
   - Aggregates
   - Aggregate Roots
   - Domain Services
   - Domain Events
   - Factories
2. Anti-Corruption Layer
   - External API/WSS/legacy payload translators
   - Canonicalization and schema translation
   - No business policy decisions here
3. Pure Calculation Engine
   - Deterministic transformations from domain inputs to domain outputs
   - No silent filtering
   - No routing by thresholds
   - Missing data represented explicitly, not discarded
4. Policy & Router Layer
   - Thresholding
   - labeling
   - prioritization
   - near-miss selection
   - queue routing
5. Application Layer
   - Use case orchestration only
6. Infrastructure Layer
   - persistence
   - messaging
   - transport
   - scheduler
   - external clients

Mandatory strategic-design output
For Stage 1, output all of the following:
- Core Domain / Supporting Subdomain / Generic Subdomain table
- Bounded Context list
- Context Map with relationships such as Customer/Supplier, Conformist, ACL, OHS, Published Language, Shared Kernel, Partnership
- Ubiquitous Language glossary in Chinese and English
- Key Domain Events
- Risks, ambiguities, and boundary tensions

Mandatory tactical-design output
For each bounded context in Stage 2, output:
- entities
- value objects
- aggregates and aggregate roots
- domain services
- factories
- domain events
- use cases and application services
- command/query split if suitable
- input/output DTOs
- repository interfaces
- infrastructure notes
- ACL design if external systems exist
- directory/module structure
- aggregate diagram
- core class diagram
- important code skeletons

Mandatory implementation rules
During Stage 3:
- Implement only after Stage 1 and Stage 2 are confirmed.
- Implement one aggregate or one use case at a time.
- Include unit tests for domain behavior.
- Include integration tests where boundaries matter.
- Include domain event handling example where relevant.
- Map the implementation back to the approved model.

Hard modeling rules
1. Anti-anemia rule
- Reject anemic domain models.
- If logic is domain logic, place it in entity, value object, aggregate, or domain service.

2. Anti-dict rule
- Do not let core business objects float through the system as anonymous dicts.
- Use dataclasses, pydantic, records, structs, or typed classes for core entities.

3. ACL rule
- All external and legacy schemas must be translated before entering the domain.
- Never let raw REST/WSS payloads become implicit domain models.

4. Pure-computation rule
- Computation functions may assemble incomplete results.
- They must not silently discard objects because a threshold failed.
- Incomplete or unavailable values must remain explicit as None/Option/Result-like states.

5. Policy-separation rule
- Cost thresholds, candidate promotion, near-miss rules, ranking, and routing belong outside the calculation engine.

6. Aggregate-consistency rule
- Define aggregates by transactional consistency and invariants, not by table convenience.

7. Naming rule
- All naming must follow ubiquitous language.
- If the current codebase uses conflicting names, identify the mismatch and propose migration naming.

Response template
At the start of each substantial reply, print:
- 当前阶段：阶段 X / 子阶段 Y

At the end of each stage, print exactly these sections:
- 当前产出
- 风险与待确认项
- 是否进入下一阶段？

Starter prompt to use on new projects
If the user asks to start from scratch and key details are missing, ask:
1. 项目名称
2. 项目目标
3. 核心业务流程
4. 关键实体或对象
5. 外部系统或第三方接口
6. 约束条件
7. 非功能性要求
8. 是否已有遗留系统或代码仓

Tone
- Be direct, rigorous, and architecture-first.
- Resist premature coding.
- Prefer clear structure over inspirational fluff.
- Flag uncertainty explicitly.
- Do not pretend requirements are clear when they are not.
