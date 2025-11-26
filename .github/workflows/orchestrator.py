#!/usr/bin/env python3
import yaml, sys
manifest_path = sys.argv[1] if len(sys.argv) > 1 else "godhead/manifests/manifest.yaml"
with open(manifest_path) as f:
    manifest = yaml.safe_load(f)
print("[INFO] Running tasks in manifest...")
for task in manifest.get("tasks", []):
    if task.get("auto", False):
        print(f"[RUN] {task['name']}")
        # Placeholder: implement task modules or subprocess calls
