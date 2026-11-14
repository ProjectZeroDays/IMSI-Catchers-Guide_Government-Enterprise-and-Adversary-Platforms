python3 tools/patch_readme.py --dry-run     # 1. read the report, change nothing
python3 tools/patch_readme.py --all         # 2. apply, fetching plates
python3 tools/patch_readme.py --check       # 3. expect RED; fill VERIFY.md; re-check