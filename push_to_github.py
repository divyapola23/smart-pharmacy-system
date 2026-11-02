"""Push the Smart Pharmacy System project directly to GitHub using GitHub's REST API.
Does not require git.exe or admin rights. Works with any valid GitHub Personal Access Token.
"""
import os
import sys
import json
import base64
import urllib.request
import urllib.error

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Files and folders to ignore when pushing
IGNORE_DIRS = {".venv", "__pycache__", ".git", ".gemini", "tests/__pycache__"}
IGNORE_FILES = {
    "cloudflared.exe",  # 55MB binary - should not be in git
    "tunnel.log",
    "PUBLIC_LINK.txt",
    "OPEN_PUBLIC_LINK.url",
    "pharmacy.db.bak",
}
IGNORE_EXTS = {".pyc", ".log"}

def api_request(url, token, data=None, method="GET"):
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "Smart-Pharmacy-Uploader")
    if data is not None:
        req.add_header("Content-Type", "application/json")
        encoded_data = json.dumps(data).encode("utf-8")
    else:
        encoded_data = None
    
    try:
        with urllib.request.urlopen(req, data=encoded_data) as response:
            res_body = response.read().decode("utf-8")
            return json.loads(res_body) if res_body else {}
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        try:
            err_json = json.loads(err_msg)
            raise RuntimeError(f"GitHub API Error ({e.code}): {err_json.get('message', err_msg)}")
        except Exception:
            raise RuntimeError(f"GitHub API Error ({e.code}): {err_msg}")

def get_files_to_push():
    file_map = {}
    for root, dirs, files in os.walk(ROOT_DIR):
        # Prune ignored directories in-place so os.walk does not descend into them
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for f in files:
            if f in IGNORE_FILES:
                continue
            ext = os.path.splitext(f)[1]
            if ext in IGNORE_EXTS:
                continue
            
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, ROOT_DIR).replace("\\", "/")
            file_map[rel_path] = full_path
    return file_map

def push_project(token, repo_name="smart-pharmacy-system", is_private=False):
    print("=" * 65, flush=True)
    print("  Smart Pharmacy System - Direct GitHub Uploader", flush=True)
    print("=" * 65, flush=True)
    print("\n[1/5] Verifying GitHub authentication token...", flush=True)
    user_data = api_request("https://api.github.com/user", token)
    username = user_data["login"]
    print(f"      Authenticated successfully as: @{username}", flush=True)

    print(f"\n[2/5] Checking repository '{repo_name}' on your GitHub account...")
    repo_url = f"https://api.github.com/repos/{username}/{repo_name}"
    repo_exists = False
    try:
        api_request(repo_url, token)
        repo_exists = True
        print(f"      Repository exists: https://github.com/{username}/{repo_name}")
    except RuntimeError:
        print(f"      Creating new repository 'https://github.com/{username}/{repo_name}'...")
        create_payload = {
            "name": repo_name,
            "description": "Smart Pharmacy Inventory and Medicine Waste Management System (Flask + SQLite)",
            "private": is_private,
            "auto_init": True
        }
        api_request("https://api.github.com/user/repos", token, data=create_payload, method="POST")
        print("      Repository created successfully!")

    print("\n[3/5] Scanning project files...", flush=True)
    files = get_files_to_push()
    print(f"      Found {len(files)} files to upload (binaries & venv excluded).", flush=True)

    print("\n[4/5] Uploading files to GitHub...", flush=True)
    tree_items = []
    count = 0
    for rel_path, full_path in files.items():
        count += 1
        print(f"      [{count}/{len(files)}] Uploading {rel_path}...", flush=True)
        with open(full_path, "rb") as f:
            content = f.read()

        blob_payload = {
            "content": base64.b64encode(content).decode("ascii"),
            "encoding": "base64"
        }
        blob_res = api_request(f"https://api.github.com/repos/{username}/{repo_name}/git/blobs", token, data=blob_payload, method="POST")
        tree_items.append({
            "path": rel_path,
            "mode": "100644",
            "type": "blob",
            "sha": blob_res["sha"]
        })
    print(f"      All {len(files)} files uploaded successfully.", flush=True)

    print("\n[5/5] Creating Git commit & publishing to 'main' branch...")
    # Get base tree from current main if available
    base_tree_sha = None
    parent_commit_sha = None
    try:
        ref_data = api_request(f"https://api.github.com/repos/{username}/{repo_name}/git/refs/heads/main", token)
        parent_commit_sha = ref_data["object"]["sha"]
        commit_data = api_request(f"https://api.github.com/repos/{username}/{repo_name}/git/commits/{parent_commit_sha}", token)
        base_tree_sha = commit_data["tree"]["sha"]
    except Exception:
        pass

    tree_payload = {"tree": tree_items}
    if base_tree_sha:
        tree_payload["base_tree"] = base_tree_sha
    tree_res = api_request(f"https://api.github.com/repos/{username}/{repo_name}/git/trees", token, data=tree_payload, method="POST")

    commit_payload = {
        "message": "Initial commit: Smart Pharmacy System (Web application, database, and docs)",
        "tree": tree_res["sha"]
    }
    if parent_commit_sha:
        commit_payload["parents"] = [parent_commit_sha]
    commit_res = api_request(f"https://api.github.com/repos/{username}/{repo_name}/git/commits", token, data=commit_payload, method="POST")

    # Update or create reference
    ref_payload = {"sha": commit_res["sha"], "force": True}
    try:
        api_request(f"https://api.github.com/repos/{username}/{repo_name}/git/refs/heads/main", token, data=ref_payload, method="PATCH")
    except Exception:
        create_ref = {"ref": "refs/heads/main", "sha": commit_res["sha"]}
        api_request(f"https://api.github.com/repos/{username}/{repo_name}/git/refs", token, data=create_ref, method="POST")

    print("\n" + "=" * 65)
    print("  >>> SUCCESS! PROJECT PUSHED TO GITHUB <<<")
    print("=" * 65)
    print(f"\n  GitHub URL: https://github.com/{username}/{repo_name}\n")
    print("=" * 65)
    return f"https://github.com/{username}/{repo_name}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        token = sys.argv[1].strip()
    else:
        token = input("Enter your GitHub Personal Access Token (classic with 'repo' scope): ").strip()
    
    if not token:
        sys.exit("Token is required.")
    
    repo = sys.argv[2].strip() if len(sys.argv) > 2 else "smart-pharmacy-system"
    push_project(token, repo)
