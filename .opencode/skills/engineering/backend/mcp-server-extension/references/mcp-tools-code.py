"""
Actual code added to mcp_serve.py (2026-04-24) to expose skills via MCP.

Paste these into create_mcp_server() before `return mcp`.
"""

# =====================================================================
# Skills & Routing — expose all skills and routing rules to MCP clients
# =====================================================================

def _get_skills_dir() -> Path:
    try:
        from agent_constants import get_agent_home
        return get_agent_home() / "skills"
    except ImportError:
        return Path(os.environ.get("AGENT_HOME", Path.home() / ".agent")) / "skills"

def _get_routing_dir() -> Path:
    try:
        from agent_constants import get_agent_home
        return get_agent_home() / "routing"
    except ImportError:
        return Path(os.environ.get("AGENT_HOME", Path.home() / ".agent")) / "routing"

def _scan_skills() -> list[dict]:
    """Walk skills dir and return metadata for every SKILL.md found."""
    skills_dir = _get_skills_dir()
    if not skills_dir.exists():
        return []
    try:
        import yaml
    except ImportError:
        yaml = None  # type: ignore
    results = []
    for skill_md in skills_dir.rglob("SKILL.md"):
        try:
            raw = skill_md.read_text(encoding="utf-8")[:6000]
            fm = {}
            body = raw
            if raw.startswith("---"):
                parts = raw.split("---", 2)
                if len(parts) >= 3 and yaml:
                    try:
                        fm = yaml.safe_load(parts[1]) or {}
                    except Exception:
                        fm = {}
                    body = parts[2].strip()
            desc = fm.get("description", "")
            if not desc:
                for line in body.split("\n"):
                    line = line.strip()
                    if line and not line.startswith("#"):
                        desc = line[:512]
                        break
            rel = skill_md.parent.relative_to(skills_dir)
            results.append({
                "name": fm.get("name", skill_md.parent.name),
                "description": desc,
                "category": str(rel.parts[0]) if len(rel.parts) > 1 else None,
                "path": str(skill_md),
                "tags": fm.get("tags", []),
            })
        except Exception:
            continue
    results.sort(key=lambda s: (s.get("category") or "", s["name"]))
    return results

def _load_routing() -> str:
    """Load skill-router.md content."""
    router = _get_routing_dir() / "skill-router.md"
    if router.exists():
        return router.read_text(encoding="utf-8")
    return "(skill-router.md not found)"

def _load_skill_content(name: str) -> str | None:
    """Load full SKILL.md content for a named skill."""
    skills_dir = _get_skills_dir()
    if not skills_dir.exists():
        return None
    try:
        import yaml as _yaml
    except ImportError:
        _yaml = None
    for skill_md in skills_dir.rglob("SKILL.md"):
        try:
            raw = skill_md.read_text(encoding="utf-8")
            fm = {}
            if raw.startswith("---"):
                parts = raw.split("---", 2)
                if len(parts) >= 3 and _yaml:
                    try:
                        fm = _yaml.safe_load(parts[1]) or {}
                    except Exception:
                        fm = {}
            if fm.get("name") == name or skill_md.parent.name == name:
                return raw
        except Exception:
            continue
    return None

def _route_skill(query: str) -> list[dict]:
    """Match a task description against routing rules and skill metadata."""
    router_text = _load_routing()
    skills = _scan_skills()
    q = query.lower()
    matches = []

    # 1. Match against skill-router.md trigger lines
    for line in router_text.split("\n"):
        line = line.strip()
        if not line.startswith("-") or "\u2192" not in line:
            continue
        triggers, _, target = line.partition("\u2192")
        triggers = triggers.lstrip("- ").strip()
        target = target.strip().strip("`")
        trigger_words = [t.strip() for t in triggers.replace("\u3001", ",").split(",") if t.strip()]
        score = sum(1 for tw in trigger_words if tw.lower() in q or q in tw.lower())
        if score > 0 or any(tw.lower() in q for tw in trigger_words):
            skill_meta = next((s for s in skills if s["name"] == target), None)
            matches.append({
                "skill": target,
                "triggers": triggers,
                "score": score,
                "description": skill_meta["description"] if skill_meta else "",
            })

    # 2. Deduplicate and sort by score
    seen = set()
    deduped = []
    for m in sorted(matches, key=lambda x: -x["score"]):
        if m["skill"] not in seen:
            seen.add(m["skill"])
            deduped.append(m)
    return deduped

# -- skill_list -----------------------------------------------------------

@mcp.tool()
def skill_list(category: Optional[str] = None) -> str:
    """List all available the agent skills with metadata.

    Returns skill names, descriptions, categories, and tags.
    Use skill_view() to load full content of a specific skill.
    Use skill_route() to find skills matching a task description.

    Args:
        category: Optional category filter (e.g., "mlops", "software-development")
    """
    skills = _scan_skills()
    if category:
        skills = [s for s in skills if s.get("category") == category]
    return json.dumps({
        "count": len(skills),
        "skills": skills,
    }, indent=2, ensure_ascii=False)

# -- skill_view -----------------------------------------------------------

@mcp.tool()
def skill_view(name: str, file_path: Optional[str] = None) -> str:
    """Load the full content of a the agent skill.

    Returns the complete SKILL.md with YAML frontmatter and instructions.
    Optionally load a specific file within the skill (references, templates).

    Args:
        name: Skill name (e.g., "ddd-project-guardrails", "old-code")
        file_path: Optional sub-path within skill (e.g., "references/api.md")
    """
    skills_dir = _get_skills_dir()
    try:
        import yaml as _yaml
    except ImportError:
        _yaml = None
    skill_dir = None
    for skill_md in skills_dir.rglob("SKILL.md"):
        try:
            raw = skill_md.read_text(encoding="utf-8")
            fm = {}
            if raw.startswith("---"):
                parts = raw.split("---", 2)
                if len(parts) >= 3 and _yaml:
                    try:
                        fm = _yaml.safe_load(parts[1]) or {}
                    except Exception:
                        fm = {}
            if fm.get("name") == name or skill_md.parent.name == name:
                skill_dir = skill_md.parent
                break
        except Exception:
            continue

    if not skill_dir:
        return json.dumps({"success": False, "error": f"Skill '{name}' not found."})

    if file_path:
        target = skill_dir / file_path
        if not target.exists():
            files = [str(p.relative_to(skill_dir)) for p in skill_dir.rglob("*") if p.is_file()]
            return json.dumps({
                "success": False,
                "error": f"File '{file_path}' not found in skill '{name}'.",
                "available_files": files[:30],
            }, ensure_ascii=False)
        content = target.read_text(encoding="utf-8")
        return json.dumps({
            "success": True,
            "skill": name,
            "file": file_path,
            "content": content,
        }, ensure_ascii=False)
    else:
        content = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        linked = []
        for sub in ["references", "templates", "scripts", "assets"]:
            sub_dir = skill_dir / sub
            if sub_dir.exists():
                for f in sub_dir.rglob("*"):
                    if f.is_file():
                        linked.append(str(f.relative_to(skill_dir)))
        return json.dumps({
            "success": True,
            "skill": name,
            "content": content,
            "linked_files": linked[:30],
        }, ensure_ascii=False)

# -- skill_route ----------------------------------------------------------

@mcp.tool()
def skill_route(query: str) -> str:
    """Find the agent skills matching a task description.

    Matches against routing rules (Chinese and English triggers) and skill
    metadata. Returns ranked list of matching skills.

    Args:
        query: Task description in any language, e.g.:
            - "我要做 DDD 项目" → ddd-project-guardrails
            - "古法编程" → old-code
            - "fine-tune a model" → axolotl, unsloth, etc.
    """
    matches = _route_skill(query)
    if not matches:
        skills = _scan_skills()
        q = query.lower()
        for s in skills:
            desc = (s.get("description", "") + " " + " ".join(str(t) for t in s.get("tags", []))).lower()
            if any(word in desc for word in q.split() if len(word) > 2):
                matches.append({
                    "skill": s["name"],
                    "triggers": "(description match)",
                    "score": 0,
                    "description": s["description"],
                })
    return json.dumps({
        "query": query,
        "matches": matches[:10],
        "hint": "Use skill_view(name) to load full skill content.",
    }, indent=2, ensure_ascii=False)

# -- routing_rules --------------------------------------------------------

@mcp.tool()
def routing_rules() -> str:
    """Get the full the agent skill routing table.

    Returns the complete skill-router.md which maps task triggers (Chinese and
    English) to skill names. Use this to understand how the agent routes tasks
    to skills, and to replicate the routing in your own agent.
    """
    return json.dumps({
        "content": _load_routing(),
        "path": str(_get_routing_dir() / "skill-router.md"),
    }, ensure_ascii=False)
