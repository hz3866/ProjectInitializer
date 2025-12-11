# Project Initializer Workflows



A collection of GitHub Actions workflows for automatically creating project repositories.


```python
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
```

## Prerequisites

1. Create a Personal Access Token (PAT) in your GitHub account with `repo` and `workflow` permissions
2. Add `PAT_TOKEN` in your template repository: Settings → Secrets and variables → Actions
3. Place all `.yml` files in the `.github/workflows/` directory of your template repository

## API Usage

All requests use POST method with the following headers:

```
Authorization: token YOUR_PAT_TOKEN
Accept: application/vnd.github+json
```

Base URL format:
```
https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_FILE}/dispatches
```

Success response: `204 No Content`

---

## 1. Django Project

**Workflow file**: `init-django.yml`

**Parameters**:

| Parameter | Required | Type | Options | Default |
|-----------|----------|------|---------|---------|
| `project_name` | ✅ | string | - | - |
| `python_version` | ✅ | choice | `3.10`, `3.11`, `3.12` | `3.11` |
| `django_version` | ✅ | choice | `4.2`, `5.0`, `5.1` | `5.0` |
| `repo_visibility` | ✅ | choice | `public`, `private` | `public` |

**cURL Example**:

```bash
curl -X POST \
  -H "Authorization: token YOUR_PAT_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/OWNER/REPO/actions/workflows/init-django.yml/dispatches \
  -d '{
    "ref": "main",
    "inputs": {
      "project_name": "my-django-app",
      "python_version": "3.11",
      "django_version": "5.0",
      "repo_visibility": "public"
    }
  }'
```

**Python Example**:

```python
import requests

response = requests.post(
    "https://api.github.com/repos/OWNER/REPO/actions/workflows/init-django.yml/dispatches",
    headers={
        "Authorization": "token YOUR_PAT_TOKEN",
        "Accept": "application/vnd.github+json"
    },
    json={
        "ref": "main",
        "inputs": {
            "project_name": "my-django-app",
            "python_version": "3.11",
            "django_version": "5.0",
            "repo_visibility": "public"
        }
    }
)

print("Success!" if response.status_code == 204 else f"Failed: {response.text}")
```

---

## 2. FastAPI Project

**Workflow file**: `init-fastapi.yml`

**Parameters**:

| Parameter | Required | Type | Options | Default |
|-----------|----------|------|---------|---------|
| `project_name` | ✅ | string | - | - |
| `python_version` | ✅ | choice | `3.10`, `3.11`, `3.12` | `3.11` |
| `fastapi_version` | ✅ | choice | `0.109`, `0.110`, `0.111`, `0.115` | `0.115` |
| `repo_visibility` | ✅ | choice | `public`, `private` | `public` |

**cURL Example**:

```bash
curl -X POST \
  -H "Authorization: token YOUR_PAT_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/OWNER/REPO/actions/workflows/init-fastapi.yml/dispatches \
  -d '{
    "ref": "main",
    "inputs": {
      "project_name": "my-api",
      "python_version": "3.11",
      "fastapi_version": "0.115",
      "repo_visibility": "public"
    }
  }'
```

**Python Example**:

```python
import requests

response = requests.post(
    "https://api.github.com/repos/OWNER/REPO/actions/workflows/init-fastapi.yml/dispatches",
    headers={
        "Authorization": "token YOUR_PAT_TOKEN",
        "Accept": "application/vnd.github+json"
    },
    json={
        "ref": "main",
        "inputs": {
            "project_name": "my-api",
            "python_version": "3.11",
            "fastapi_version": "0.115",
            "repo_visibility": "public"
        }
    }
)

print("Success!" if response.status_code == 204 else f"Failed: {response.text}")
```

---

## 3. PyTorch Project

**Workflow file**: `init-pytorch.yml`

**Parameters**:

| Parameter | Required | Type | Options | Default |
|-----------|----------|------|---------|---------|
| `project_name` | ✅ | string | - | - |
| `python_version` | ✅ | choice | `3.10`, `3.11`, `3.12` | `3.11` |
| `pytorch_version` | ✅ | choice | `2.1`, `2.2`, `2.3`, `2.4`, `2.5` | `2.5` |
| `repo_visibility` | ✅ | choice | `public`, `private` | `public` |

**cURL Example**:

```bash
curl -X POST \
  -H "Authorization: token YOUR_PAT_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/OWNER/REPO/actions/workflows/init-pytorch.yml/dispatches \
  -d '{
    "ref": "main",
    "inputs": {
      "project_name": "my-ml-project",
      "python_version": "3.11",
      "pytorch_version": "2.5",
      "repo_visibility": "public"
    }
  }'
```

**Python Example**:

```python
import requests

response = requests.post(
    "https://api.github.com/repos/OWNER/REPO/actions/workflows/init-pytorch.yml/dispatches",
    headers={
        "Authorization": "token YOUR_PAT_TOKEN",
        "Accept": "application/vnd.github+json"
    },
    json={
        "ref": "main",
        "inputs": {
            "project_name": "my-ml-project",
            "python_version": "3.11",
            "pytorch_version": "2.5",
            "repo_visibility": "public"
        }
    }
)

print("Success!" if response.status_code == 204 else f"Failed: {response.text}")
```

---

## 4. Jupyter Project

**Workflow file**: `init-jupyter.yml`

**Parameters**:

| Parameter | Required | Type | Options | Default |
|-----------|----------|------|---------|---------|
| `project_name` | ✅ | string | - | - |
| `python_version` | ✅ | choice | `3.10`, `3.11`, `3.12` | `3.11` |
| `repo_visibility` | ✅ | choice | `public`, `private` | `public` |

**cURL Example**:

```bash
curl -X POST \
  -H "Authorization: token YOUR_PAT_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/OWNER/REPO/actions/workflows/init-jupyter.yml/dispatches \
  -d '{
    "ref": "main",
    "inputs": {
      "project_name": "my-analysis",
      "python_version": "3.11",
      "repo_visibility": "public"
    }
  }'
```

**Python Example**:

```python
import requests

response = requests.post(
    "https://api.github.com/repos/OWNER/REPO/actions/workflows/init-jupyter.yml/dispatches",
    headers={
        "Authorization": "token YOUR_PAT_TOKEN",
        "Accept": "application/vnd.github+json"
    },
    json={
        "ref": "main",
        "inputs": {
            "project_name": "my-analysis",
            "python_version": "3.11",
            "repo_visibility": "public"
        }
    }
)

print("Success!" if response.status_code == 204 else f"Failed: {response.text}")
```

---

## 5. React Project

**Workflow file**: `init-react.yml`

**Parameters**:

| Parameter | Required | Type | Options | Default |
|-----------|----------|------|---------|---------|
| `project_name` | ✅ | string | - | - |
| `node_version` | ✅ | choice | `18`, `20`, `22` | `20` |
| `react_version` | ✅ | choice | `18`, `19` | `19` |
| `repo_visibility` | ✅ | choice | `public`, `private` | `public` |

**cURL Example**:

```bash
curl -X POST \
  -H "Authorization: token YOUR_PAT_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/OWNER/REPO/actions/workflows/init-react.yml/dispatches \
  -d '{
    "ref": "main",
    "inputs": {
      "project_name": "my-react-app",
      "node_version": "20",
      "react_version": "19",
      "repo_visibility": "public"
    }
  }'
```

**Python Example**:

```python
import requests

response = requests.post(
    "https://api.github.com/repos/OWNER/REPO/actions/workflows/init-react.yml/dispatches",
    headers={
        "Authorization": "token YOUR_PAT_TOKEN",
        "Accept": "application/vnd.github+json"
    },
    json={
        "ref": "main",
        "inputs": {
            "project_name": "my-react-app",
            "node_version": "20",
            "react_version": "19",
            "repo_visibility": "public"
        }
    }
)

print("Success!" if response.status_code == 204 else f"Failed: {response.text}")
```

---

## 6. Vue Project

**Workflow file**: `init-vue.yml`

**Parameters**:

| Parameter | Required | Type | Options | Default |
|-----------|----------|------|---------|---------|
| `project_name` | ✅ | string | - | - |
| `node_version` | ✅ | choice | `18`, `20`, `22` | `20` |
| `vue_version` | ✅ | choice | `3.4`, `3.5` | `3.5` |
| `repo_visibility` | ✅ | choice | `public`, `private` | `public` |

**cURL Example**:

```bash
curl -X POST \
  -H "Authorization: token YOUR_PAT_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/OWNER/REPO/actions/workflows/init-vue.yml/dispatches \
  -d '{
    "ref": "main",
    "inputs": {
      "project_name": "my-vue-app",
      "node_version": "20",
      "vue_version": "3.5",
      "repo_visibility": "public"
    }
  }'
```

**Python Example**:

```python
import requests

response = requests.post(
    "https://api.github.com/repos/OWNER/REPO/actions/workflows/init-vue.yml/dispatches",
    headers={
        "Authorization": "token YOUR_PAT_TOKEN",
        "Accept": "application/vnd.github+json"
    },
    json={
        "ref": "main",
        "inputs": {
            "project_name": "my-vue-app",
            "node_version": "20",
            "vue_version": "3.5",
            "repo_visibility": "public"
        }
    }
)

print("Success!" if response.status_code == 204 else f"Failed: {response.text}")
```

---

## Python Wrapper Class

```python
import requests
from typing import Literal

class ProjectInitializer:
    def __init__(self, owner: str, repo: str, token: str):
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json"
        }
    
    def _dispatch(self, workflow: str, inputs: dict) -> bool:
        response = requests.post(
            f"{self.base_url}/{workflow}/dispatches",
            headers=self.headers,
            json={"ref": "main", "inputs": inputs}
        )
        return response.status_code == 204
    
    def create_django(
        self,
        project_name: str,
        python_version: Literal["3.10", "3.11", "3.12"] = "3.11",
        django_version: Literal["4.2", "5.0", "5.1"] = "5.0",
        repo_visibility: Literal["public", "private"] = "public"
    ) -> bool:
        return self._dispatch("init-django.yml", {
            "project_name": project_name,
            "python_version": python_version,
            "django_version": django_version,
            "repo_visibility": repo_visibility
        })
    
    def create_fastapi(
        self,
        project_name: str,
        python_version: Literal["3.10", "3.11", "3.12"] = "3.11",
        fastapi_version: Literal["0.109", "0.110", "0.111", "0.115"] = "0.115",
        repo_visibility: Literal["public", "private"] = "public"
    ) -> bool:
        return self._dispatch("init-fastapi.yml", {
            "project_name": project_name,
            "python_version": python_version,
            "fastapi_version": fastapi_version,
            "repo_visibility": repo_visibility
        })
    
    def create_pytorch(
        self,
        project_name: str,
        python_version: Literal["3.10", "3.11", "3.12"] = "3.11",
        pytorch_version: Literal["2.1", "2.2", "2.3", "2.4", "2.5"] = "2.5",
        repo_visibility: Literal["public", "private"] = "public"
    ) -> bool:
        return self._dispatch("init-pytorch.yml", {
            "project_name": project_name,
            "python_version": python_version,
            "pytorch_version": pytorch_version,
            "repo_visibility": repo_visibility
        })
    
    def create_jupyter(
        self,
        project_name: str,
        python_version: Literal["3.10", "3.11", "3.12"] = "3.11",
        repo_visibility: Literal["public", "private"] = "public"
    ) -> bool:
        return self._dispatch("init-jupyter.yml", {
            "project_name": project_name,
            "python_version": python_version,
            "repo_visibility": repo_visibility
        })
    
    def create_react(
        self,
        project_name: str,
        node_version: Literal["18", "20", "22"] = "20",
        react_version: Literal["18", "19"] = "19",
        repo_visibility: Literal["public", "private"] = "public"
    ) -> bool:
        return self._dispatch("init-react.yml", {
            "project_name": project_name,
            "node_version": node_version,
            "react_version": react_version,
            "repo_visibility": repo_visibility
        })
    
    def create_vue(
        self,
        project_name: str,
        node_version: Literal["18", "20", "22"] = "20",
        vue_version: Literal["3.4", "3.5"] = "3.5",
        repo_visibility: Literal["public", "private"] = "public"
    ) -> bool:
        return self._dispatch("init-vue.yml", {
            "project_name": project_name,
            "node_version": node_version,
            "vue_version": vue_version,
            "repo_visibility": repo_visibility
        })


# Usage Example
if __name__ == "__main__":
    init = ProjectInitializer(
        owner="your-username",
        repo="project-templates",
        token="your-pat-token"
    )
    
    # Create Django project
    if init.create_django("my-blog", python_version="3.12", django_version="5.1"):
        print("Django project creation triggered!")
    
    # Create React project
    if init.create_react("my-app", node_version="22", react_version="19"):
        print("React project creation triggered!")
```

---

## Notes

1. **project_name rules**: Must start with a letter and contain only letters, numbers, hyphens `-`, and underscores `_`
2. **API response**: Returns `204 No Content` on success, workflow runs asynchronously in background
3. **Check execution status**: Visit `https://github.com/{OWNER}/{REPO}/actions`
4. **PAT permissions**: Requires `repo` and `workflow` scopes