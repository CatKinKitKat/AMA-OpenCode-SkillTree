---
name: vsco-code-repl-beep-patc
description: Patch the VS Code OpenAI Codex extension so the agent/Codex reply completion triggers an audible macOS beep and optional VS Code toast when the shipped extension ignores desktop-notification-show.
tags: 
version: 1
---


Goal
- Make the agent/Codex in VS Code emit a sound when a reply completes.
- Prefer patching the installed extension bundle only when no exposed setting exists.

Use when
- User says the agent/Codex in VS Code should beep or play a sound after replying.
- Extension settings expose no audio-cue option for reply completion.
- You are on macOS and can use `afplay`.

Prereqs
1. Inspect the installed extension package first.
   - Typical path: `~/.vscode/extensions/openai.chatgpt-<version>-darwin-arm64/`
2. Confirm no direct configuration exists in `package.json` for reply-complete audio.
3. Search `out/extension.js` for `desktop-notification-show`.

Key findings
- In the shipped Codex VS Code extension bundle, `desktop-notification-show` may be explicitly ignored:
  - `case\"desktop-notification-show\":case\"desktop-notification-hide\":break;`
- Patching that branch restores sound only if the webview/runtime actually emits `desktop-notification-show`.
- Empirical finding: reply completion may not travel through `desktop-notification-show` at all.
- Empirical finding: a coarse `log-message` completion heuristic can fire at the wrong time and is not reliable for true reply-end semantics.
- Better fallback patch point exists in the webview bundle reducer handling streamed thread events:
  - `webview/assets/index-*.js`
  - reducer branch: `case\`turn/completed\`` inside the function that folds thread events into turn state (seen around `Zfe(...)` in current bundle)
- If extension-side notification patch is insufficient, prefer triggering audio directly from the webview on `turn/completed` / final assistant completion path instead of routing through ignored desktop notifications.

Patch recipe
1. Backup target file.
   - `cp out/extension.js out/extension.js.bak-agent-beep`
2. Replace the ignore branch with a handler that:
   - calls `vscode.window.showInformationMessage(...)`
   - spawns `afplay /System/Library/Sounds/Glass.aiff`
3. Use a detached child process so the extension host does not block:
   - `require("node:child_process").spawn("afplay", ["/System/Library/Sounds/Glass.aiff"], { detached: true, stdio: "ignore" }).unref()`
4. Validate syntax:
   - `node --check <full path to out/extension.js>`
5. Tell user to run `Developer: Reload Window`.

If no beep occurs at true reply completion
6. Do not trust a broad `log-message` heuristic as the final fix. It can beep at the wrong time.
7. Inspect `webview/assets/index-*.js` for the thread-event reducer that handles:
   - `turn/completed`
   - `item/completed`
   - `item/agentMessage/delta`
8. Prefer patching the reducer branch for `turn/completed` or the final assistant-message completion path to trigger audio locally in the webview.
   - Lowest-friction fallback: `window.parent.postMessage({ type: 'desktop-notification-show', title: 'the agent', body: '回复完成' }, '*')`
   - More robust fallback when parent routing is unreliable: call audio playback directly in the webview bundle, e.g. `new Audio(<data-uri-or-local-safe-source>).play().catch(() => {})`
9. If using the webview path, also consider adding a tiny listener in `webview/index.html` for `desktop-notification-show` as a backup, but do not assume that listener alone fixes missing upstream events.
10. Validate syntax for patched JS bundle(s) and reload the VS Code window again.

Known-good replacement shape
```js
case"desktop-notification-show":{
  try{
    let n=r?.title??"the agent",o=r?.body??r?.message??"回复完成";
    ke.window.showInformationMessage(`${n}: ${o}`);
    require("node:child_process").spawn("afplay",["/System/Library/Sounds/Glass.aiff"],{detached:!0,stdio:"ignore"}).unref()
  }catch(n){
    Y().warning("[agent-beep] desktop notification failed",{safe:{error:String(n)},sensitive:{}})
  }
  break
}
case"desktop-notification-hide":break;
```

Verification
- `node --check` exits 0.
- Manual smoke test:
  1. reload VS Code window
  2. trigger a the agent/Codex reply
  3. confirm toast + sound
- Optional direct audio test:
  - `afplay /System/Library/Sounds/Glass.aiff`

Pitfalls
- This edits installed extension output, not source.
- Extension updates overwrite the patch.
- Bundle is minified. Patch exact unique string, not broad regex.
- `search_files` may not show the minified branch cleanly after patch. Rely on exact replace success + `node --check`.
- On non-macOS systems, replace `afplay` with platform-appropriate audio command.
- `desktop-notification-show` restoration alone may still produce no sound if reply completion never emits that message.
- A `log-message`-based hook is tempting but can fire before true reply completion.
- `window.parent.postMessage(...)` from the webview may also fail to surface if the host does not route arbitrary message types back into the extension handler. Direct in-webview audio is the stronger fallback.

Rollback
- Restore backup:
  - `cp out/extension.js.bak-agent-beep out/extension.js`
- Or reinstall/update the extension.

When not to use
- If the extension already exposes a supported reply-audio setting.
- If user only wants standard VS Code audio cues. Then prefer settings over patching installed code.
