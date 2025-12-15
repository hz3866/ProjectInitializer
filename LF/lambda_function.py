import json
import os
import urllib.request
import urllib.error
from typing import Any

# Configuration from environment variables
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_OWNER = os.environ.get("GITHUB_OWNER")
GITHUB_REPO = os.environ.get("GITHUB_REPO")  # ProjectInitializer repo

# Excluded repositories
EXCLUDED_REPOS = ["ProjectInitializer"]

# Allowed project types and their configurations
PROJECT_CONFIGS = {
    "django": {
        "workflow": "init-django.yml",
        "required": ["project_name"],
        "optional": {
            "python_version": {"options": ["3.10", "3.11", "3.12"], "default": "3.11"},
            "django_version": {"options": ["4.2", "5.0", "5.1"], "default": "5.0"},
            "repo_visibility": {"options": ["public", "private"], "default": "public"},
        },
    },
    "fastapi": {
        "workflow": "init-fastapi.yml",
        "required": ["project_name"],
        "optional": {
            "python_version": {"options": ["3.10", "3.11", "3.12"], "default": "3.11"},
            "fastapi_version": {"options": ["0.109", "0.110", "0.111", "0.115"], "default": "0.115"},
            "repo_visibility": {"options": ["public", "private"], "default": "public"},
        },
    },
    "pytorch": {
        "workflow": "init-pytorch.yml",
        "required": ["project_name"],
        "optional": {
            "python_version": {"options": ["3.10", "3.11", "3.12"], "default": "3.11"},
            "pytorch_version": {"options": ["2.1", "2.2", "2.3", "2.4", "2.5"], "default": "2.5"},
            "repo_visibility": {"options": ["public", "private"], "default": "public"},
        },
    },
    "jupyter": {
        "workflow": "init-jupyter.yml",
        "required": ["project_name"],
        "optional": {
            "python_version": {"options": ["3.10", "3.11", "3.12"], "default": "3.11"},
            "repo_visibility": {"options": ["public", "private"], "default": "public"},
        },
    },
    "react": {
        "workflow": "init-react.yml",
        "required": ["project_name"],
        "optional": {
            "node_version": {"options": ["18", "20", "22"], "default": "20"},
            "react_version": {"options": ["18", "19"], "default": "19"},
            "repo_visibility": {"options": ["public", "private"], "default": "public"},
        },
    },
    "vue": {
        "workflow": "init-vue.yml",
        "required": ["project_name"],
        "optional": {
            "node_version": {"options": ["18", "20", "22"], "default": "20"},
            "vue_version": {"options": ["3.4", "3.5"], "default": "3.5"},
            "repo_visibility": {"options": ["public", "private"], "default": "public"},
        },
    },
}


def create_response(status_code: int, body: Any) -> dict:
    """Create API Gateway response."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,X-Api-Key",
            "Access-Control-Allow-Methods": "POST,OPTIONS",
        },
        "body": json.dumps(body),
    }


def github_api_request(endpoint: str, method: str = "GET", data: dict = None) -> tuple[bool, Any]:
    """Make a request to GitHub API."""
    url = f"https://api.github.com{endpoint}"
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "ProjectInitializer-Lambda",
    }
    
    payload = json.dumps(data).encode("utf-8") if data else None
    
    try:
        req = urllib.request.Request(url, data=payload, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status == 204:
                return True, None
            return True, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        return False, f"GitHub API error: {e.code} - {error_body}"
    except urllib.error.URLError as e:
        return False, f"Network error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"


def validate_project_name(name: str) -> bool:
    """Validate project name format."""
    if not name or len(name) < 1 or len(name) > 100:
        return False
    import re
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", name))


def validate_inputs(project_type: str, inputs: dict) -> tuple[bool, str]:
    """Validate inputs against project configuration."""
    if project_type not in PROJECT_CONFIGS:
        return False, f"Invalid project_type. Must be one of: {', '.join(PROJECT_CONFIGS.keys())}"
    
    config = PROJECT_CONFIGS[project_type]
    
    for field in config["required"]:
        if field not in inputs or not inputs[field]:
            return False, f"Missing required field: {field}"
    
    if not validate_project_name(inputs.get("project_name", "")):
        return False, "Invalid project_name. Must start with a letter and contain only letters, numbers, hyphens, and underscores."
    
    for field, rules in config["optional"].items():
        if field in inputs:
            if inputs[field] not in rules["options"]:
                return False, f"Invalid {field}. Must be one of: {', '.join(rules['options'])}"
    
    return True, ""


def build_workflow_inputs(project_type: str, inputs: dict) -> dict:
    """Build workflow inputs with defaults."""
    config = PROJECT_CONFIGS[project_type]
    workflow_inputs = {}
    
    for field in config["required"]:
        workflow_inputs[field] = inputs[field]
    
    for field, rules in config["optional"].items():
        workflow_inputs[field] = inputs.get(field, rules["default"])
    
    return workflow_inputs


# =============================================================================
# Method: init - Create new project (existing functionality)
# =============================================================================
def handle_init(body: dict) -> dict:
    """Handle project initialization request."""
    project_type = body.get("project_type", "").lower()
    if not project_type:
        return create_response(400, {
            "error": "Missing project_type",
            "message": f"project_type is required. Must be one of: {', '.join(PROJECT_CONFIGS.keys())}"
        })
    
    is_valid, error_message = validate_inputs(project_type, body)
    if not is_valid:
        return create_response(400, {
            "error": "Validation error",
            "message": error_message
        })
    
    config = PROJECT_CONFIGS[project_type]
    workflow_inputs = build_workflow_inputs(project_type, body)
    
    # Trigger workflow
    endpoint = f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/workflows/{config['workflow']}/dispatches"
    success, result = github_api_request(endpoint, method="POST", data={
        "ref": "master",
        "inputs": workflow_inputs
    })
    
    if success:
        return create_response(200, {
            "success": True,
            "message": "Workflow triggered successfully",
            "project_type": project_type,
            "project_name": workflow_inputs["project_name"],
            "inputs": workflow_inputs,
            "repository_url": f"https://github.com/{GITHUB_OWNER}/{workflow_inputs['project_name']}"
        })
    else:
        return create_response(500, {
            "error": "GitHub API error",
            "message": result
        })


# =============================================================================
# Method: search - List all repositories and their branches
# =============================================================================
def handle_search(body: dict) -> dict:
    """
    List all repositories (excluding ProjectInitializer) and their branches.
    
    Optional body parameters:
    - include_branches: bool (default: true) - Whether to fetch branches for each repo
    - per_page: int (default: 100) - Number of repos per page
    """
    include_branches = body.get("include_branches", True)
    per_page = min(body.get("per_page", 100), 100)  # Max 100
    
    # Fetch all repositories
    repos_endpoint = f"/users/{GITHUB_OWNER}/repos?per_page={per_page}&sort=updated&direction=desc"
    success, repos_data = github_api_request(repos_endpoint)
    
    if not success:
        return create_response(500, {
            "error": "Failed to fetch repositories",
            "message": repos_data
        })
    
    # Filter out excluded repos
    filtered_repos = [
        repo for repo in repos_data 
        if repo["name"] not in EXCLUDED_REPOS
    ]
    
    # Build response
    result = []
    for repo in filtered_repos:
        repo_info = {
            "name": repo["name"],
            "full_name": repo["full_name"],
            "description": repo.get("description"),
            "url": repo["html_url"],
            "default_branch": repo["default_branch"],
            "private": repo["private"],
            "updated_at": repo["updated_at"],
            "language": repo.get("language"),
        }
        
        # Fetch branches if requested
        if include_branches:
            branches_endpoint = f"/repos/{GITHUB_OWNER}/{repo['name']}/branches?per_page=100"
            branch_success, branches_data = github_api_request(branches_endpoint)
            
            if branch_success:
                repo_info["branches"] = [
                    {
                        "name": branch["name"],
                        "protected": branch.get("protected", False)
                    }
                    for branch in branches_data
                ]
            else:
                repo_info["branches"] = []
                repo_info["branches_error"] = "Failed to fetch branches"
        
        result.append(repo_info)
    
    return create_response(200, {
        "success": True,
        "count": len(result),
        "repositories": result
    })


# =============================================================================
# Method: build - Trigger docker build & push for a specific repo and branch
# =============================================================================
def handle_build(body: dict) -> dict:
    """
    Trigger docker-build-push workflow for a specific repository and branch.
    
    Required body parameters:
    - repo: str - Repository name (e.g., "my-django-app")
    - branch: str - Branch name (e.g., "main", "master", "develop")
    """
    repo = body.get("repo")
    branch = body.get("branch")
    
    # Validate required fields
    if not repo:
        return create_response(400, {
            "error": "Missing required field",
            "message": "repo is required"
        })
    
    if not branch:
        return create_response(400, {
            "error": "Missing required field",
            "message": "branch is required"
        })
    
    # Check if repo is in excluded list
    if repo in EXCLUDED_REPOS:
        return create_response(400, {
            "error": "Invalid repository",
            "message": f"Cannot build {repo}"
        })
    
    # Verify repository exists
    repo_endpoint = f"/repos/{GITHUB_OWNER}/{repo}"
    repo_success, repo_data = github_api_request(repo_endpoint)
    
    if not repo_success:
        return create_response(404, {
            "error": "Repository not found",
            "message": f"Repository '{repo}' does not exist or is not accessible"
        })
    
    # Verify branch exists
    branch_endpoint = f"/repos/{GITHUB_OWNER}/{repo}/branches/{branch}"
    branch_success, branch_data = github_api_request(branch_endpoint)
    
    if not branch_success:
        return create_response(404, {
            "error": "Branch not found",
            "message": f"Branch '{branch}' does not exist in repository '{repo}'"
        })
    
    # Trigger docker-build-push workflow
    workflow_file = "docker-build-push.yml"
    dispatch_endpoint = f"/repos/{GITHUB_OWNER}/{repo}/actions/workflows/{workflow_file}/dispatches"
    
    dispatch_success, dispatch_result = github_api_request(
        dispatch_endpoint, 
        method="POST", 
        data={"ref": branch}
    )
    
    if dispatch_success:
        return create_response(200, {
            "success": True,
            "message": "Docker build workflow triggered successfully",
            "repository": repo,
            "branch": branch,
            "workflow": workflow_file,
            "repository_url": f"https://github.com/{GITHUB_OWNER}/{repo}",
            "actions_url": f"https://github.com/{GITHUB_OWNER}/{repo}/actions"
        })
    else:
        # Check if workflow file exists
        if "Could not find" in str(dispatch_result) or "No workflow" in str(dispatch_result):
            return create_response(404, {
                "error": "Workflow not found",
                "message": f"Workflow '{workflow_file}' does not exist in repository '{repo}'. Make sure the repository was created with ProjectInitializer."
            })
        
        return create_response(500, {
            "error": "Failed to trigger workflow",
            "message": dispatch_result
        })


# =============================================================================
# Method: status - Get workflow run status (bonus feature)
# =============================================================================
def handle_status(body: dict) -> dict:
    """
    Get recent workflow runs for a repository.
    
    Required body parameters:
    - repo: str - Repository name
    
    Optional body parameters:
    - workflow: str - Workflow filename (default: "docker-build-push.yml")
    - per_page: int - Number of runs to fetch (default: 5, max: 20)
    """
    repo = body.get("repo")
    workflow = body.get("workflow", "docker-build-push.yml")
    per_page = min(body.get("per_page", 5), 20)
    
    if not repo:
        return create_response(400, {
            "error": "Missing required field",
            "message": "repo is required"
        })
    
    # Fetch workflow runs
    runs_endpoint = f"/repos/{GITHUB_OWNER}/{repo}/actions/workflows/{workflow}/runs?per_page={per_page}"
    success, runs_data = github_api_request(runs_endpoint)
    
    if not success:
        return create_response(500, {
            "error": "Failed to fetch workflow runs",
            "message": runs_data
        })
    
    runs = []
    for run in runs_data.get("workflow_runs", []):
        runs.append({
            "id": run["id"],
            "status": run["status"],
            "conclusion": run.get("conclusion"),
            "branch": run["head_branch"],
            "commit_sha": run["head_sha"][:7],
            "created_at": run["created_at"],
            "updated_at": run["updated_at"],
            "url": run["html_url"]
        })
    
    return create_response(200, {
        "success": True,
        "repository": repo,
        "workflow": workflow,
        "total_count": runs_data.get("total_count", 0),
        "runs": runs
    })


# =============================================================================
# Main Lambda Handler
# =============================================================================
def lambda_handler(event: dict, context: Any) -> dict:
    """
    AWS Lambda handler for GitHub Actions management.
    
    POST body must include "method" field:
    
    1. method: "init" - Create new project
       {
           "method": "init",
           "project_type": "django|fastapi|pytorch|jupyter|react|vue",
           "project_name": "my-project",
           ...
       }
    
    2. method: "search" - List all repositories and branches
       {
           "method": "search",
           "include_branches": true  // optional, default true
       }
    
    3. method: "build" - Trigger docker build for a repo
       {
           "method": "build",
           "repo": "my-django-app",
           "branch": "main"
       }
    
    4. method: "status" - Get workflow run status
       {
           "method": "status",
           "repo": "my-django-app",
           "workflow": "docker-build-push.yml",  // optional
           "per_page": 5  // optional
       }
    """
    # Handle CORS preflight
    if event.get("httpMethod") == "OPTIONS":
        return create_response(200, {"message": "OK"})
    
    # Check environment variables
    if not all([GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO]):
        return create_response(500, {
            "error": "Server configuration error",
            "message": "Missing required environment variables"
        })
    
    # Parse request body
    try:
        if isinstance(event.get("body"), str):
            body = json.loads(event["body"])
        else:
            body = event.get("body", {})
    except json.JSONDecodeError:
        return create_response(400, {
            "error": "Invalid JSON",
            "message": "Request body must be valid JSON"
        })
    
    # Get method
    method = body.get("method", "").lower()
    
    # Route to appropriate handler
    if method == "init":
        return handle_init(body)
    elif method == "search":
        return handle_search(body)
    elif method == "build":
        return handle_build(body)
    elif method == "status":
        return handle_status(body)
    else:
        return create_response(400, {
            "error": "Invalid method",
            "message": "method must be one of: init, search, build, status",
            "available_methods": {
                "init": "Create a new project from template",
                "search": "List all repositories and branches",
                "build": "Trigger docker build & push for a repo",
                "status": "Get workflow run status"
            }
        })


# =============================================================================
# Local Testing
# =============================================================================
if __name__ == "__main__":
    os.environ["GITHUB_TOKEN"] = "your-token"
    os.environ["GITHUB_OWNER"] = "hz3866"
    os.environ["GITHUB_REPO"] = "ProjectInitializer"
    
    # Test search
    print("=" * 50)
    print("Testing: search")
    print("=" * 50)
    test_search = {
        "httpMethod": "POST",
        "body": json.dumps({
            "method": "search",
            "include_branches": True
        })
    }
    result = lambda_handler(test_search, None)
    print(json.dumps(json.loads(result["body"]), indent=2))
    
    # Test build
    print("\n" + "=" * 50)
    print("Testing: build")
    print("=" * 50)
    test_build = {
        "httpMethod": "POST",
        "body": json.dumps({
            "method": "build",
            "repo": "my-django-app",
            "branch": "main"
        })
    }
    result = lambda_handler(test_build, None)
    print(json.dumps(json.loads(result["body"]), indent=2))
    
    # Test status
    print("\n" + "=" * 50)
    print("Testing: status")
    print("=" * 50)
    test_status = {
        "httpMethod": "POST",
        "body": json.dumps({
            "method": "status",
            "repo": "my-django-app"
        })
    }
    result = lambda_handler(test_status, None)
    print(json.dumps(json.loads(result["body"]), indent=2))
