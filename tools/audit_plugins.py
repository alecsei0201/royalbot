"""
Offline safety & sanity checks for downloaded plugins.
- Compiles to bytecode (no execution).
- Simple heuristic checks.
- Moves failing files to app/ext/quarantine.
Usage:
  python tools/audit_plugins.py
"""
import os, py_compile, shutil, pathlib, re

PLUGINS_DIR = pathlib.Path("app/ext/plugins")
QUARANTINE_DIR = pathlib.Path("app/ext/quarantine")

def main():
    PLUGINS_DIR.mkdir(parents=True, exist_ok=True)
    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)

    count = 0
    bad = 0
    for f in PLUGINS_DIR.glob("*.py"):
        count += 1
        try:
            py_compile.compile(str(f), doraise=True)
        except Exception as e:
            print(f"[!] Syntax error: {f.name}: {e}")
            shutil.move(str(f), str(QUARANTINE_DIR / f.name))
            bad += 1
            continue
        # Basic heuristic: prevent obvious dangerous calls (user may refine this list)
        txt = f.read_text(encoding="utf-8", errors="ignore")
        if re.search(r'\bos\.system\(|subprocess\.', txt):
            print(f"[!] Suspicious: {f.name} uses shell/subprocess. Quarantine.")
            shutil.move(str(f), str(QUARANTINE_DIR / f.name))
            bad += 1
    print(f"Audit done. Checked: {count}, quarantined: {bad}, ok: {count-bad}")

if __name__ == "__main__":
    main()
