# ProjectInitializer

A collection of GitHub Actions workflows to quickly scaffold new projects with Docker CI/CD pipelines.

## Available Templates

| Template | Description | Tech Stack |
|----------|-------------|------------|
| Django | Python web framework | Python, Django, Gunicorn |
| FastAPI | Modern async API framework | Python, FastAPI, Uvicorn |
| React | Frontend SPA | Node.js, React, Vite, TypeScript |
| Vue | Frontend SPA | Node.js, Vue, Vite, TypeScript |
| PyTorch | Machine Learning project | Python, PyTorch, TensorBoard |
| Jupyter | Data Analysis project | Python, Jupyter Lab, Pandas |

## Features

Each generated project includes:

- ✅ Framework-specific project structure
- ✅ Dockerfile optimized for production
- ✅ GitHub Actions CI/CD pipeline
- ✅ Docker image build & push to DockerHub
- ✅ Trivy security scanning
- ✅ Version management via `release.yaml`

## Usage

1. Go to **Actions** tab in this repository
2. Select the desired `Init * Project` workflow
3. Click **Run workflow**
4. Fill in the parameters:
   - Project name
   - Framework version
   - Repository visibility (public/private)
5. Wait for the workflow to complete
6. Your new repository will be created with all files ready

## Required Secrets

Configure these secrets in your repository settings:

| Secret | Description | How to Get |
|--------|-------------|------------|
| `PAT_TOKEN` | GitHub Personal Access Token | GitHub Settings → Developer settings → Personal access tokens |
| `DOCKERHUB_USERNAME` | DockerHub username | Your DockerHub account username |
| `DOCKERHUB_TOKEN` | DockerHub access token | DockerHub → Account Settings → Security → New Access Token |

### PAT_TOKEN Permissions

When creating the Personal Access Token, select these permissions:
- `repo` (Full control of private repositories)
- `workflow` (Update GitHub Action workflows)

## Project Structure

```
ProjectInitializer/
├── .github/
│   └── workflows/
│       ├── init-django.yml
│       ├── init-fastapi.yml
│       ├── init-react.yml
│       ├── init-vue.yml
│       ├── init-pytorch.yml
│       └── init-jupyter.yml
│
├── templates/
│   ├── shared/                    # Shared across all projects
│   │   └── .github/workflows/
│   │       └── docker-build-push.yml
│   │
│   ├── django/
│   │   ├── Dockerfile.template
│   │   ├── .gitignore
│   │   └── .env.example
│   │
│   ├── fastapi/
│   ├── react/
│   ├── vue/
│   ├── pytorch/
│   └── jupyter/
│
└── LF/                            # AWS Lambda Function
    ├── lambda_function.py         # Main handler
    ├── template.yaml              # SAM deployment template
    └── README.md                  # Deployment instructions
```

## Generated Project CI/CD

Each generated project will have a `docker-build-push.yml` workflow that:

- **Triggers on:**
  - Push to `main` or `master` branch
  - Manual trigger via `workflow_dispatch` (for AWS integration)

- **Version format:**
  ```
  {branch}-{YYMMDD}-{version}-{commit_sha}
  ```
  Example: `main-241214-0.1.0-abc1234`

- **Image tags:**
  - `{dockerhub_username}/{repo_name}:{version}`
  - `{dockerhub_username}/{repo_name}:latest`

## Customization

### Adding New Templates

1. Create a new folder under `templates/`
2. Add framework-specific files (Dockerfile.template, .gitignore, etc.)
3. Create a new workflow in `.github/workflows/init-{framework}.yml`
4. Use `{{PLACEHOLDER}}` syntax in templates for variable substitution

### Modifying CI/CD Pipeline

Edit `templates/shared/.github/workflows/docker-build-push.yml` to modify the CI/CD pipeline for all projects.

## AWS Lambda Deployment

The `LF/` folder contains an AWS Lambda function for programmatic API access.

### Quick Deploy with SAM

```bash
cd LF
sam build
sam deploy --guided
```

You'll need:
- GitHub PAT with `repo` + `workflow` permissions
- AWS CLI configured

See [LF/README.md](LF/README.md) for detailed deployment instructions.

---

# AWS Lambda API Documentation

This project includes an AWS Lambda function for programmatic access to all features via REST API.

## Lambda Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GITHUB_TOKEN` | GitHub PAT with `repo` + `workflow` permissions | `ghp_xxxxxxxxxxxx` |
| `GITHUB_OWNER` | GitHub username or organization | `hz3866` |
| `GITHUB_REPO` | This template repository name | `ProjectInitializer` |

## API Endpoint

All requests use **POST** method with JSON body.

**URL:**
```
https://{ask-author-for-url}
```

**Method:** `POST`

**Headers:**
```
Content-Type: application/json
```

---

## Method 1: `init` - Create New Project

Creates a new repository from a template with full CI/CD setup.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `method` | string | ✅ | Must be `"init"` |
| `project_type` | string | ✅ | Template type (see options below) |
| `project_name` | string | ✅ | Repository name (letters, numbers, underscores) |
| `python_version` | string | ❌ | Python version (for Python projects) |
| `django_version` | string | ❌ | Django version (for Django only) |
| `fastapi_version` | string | ❌ | FastAPI version (for FastAPI only) |
| `pytorch_version` | string | ❌ | PyTorch version (for PyTorch only) |
| `node_version` | string | ❌ | Node.js version (for React/Vue) |
| `react_version` | string | ❌ | React version (for React only) |
| `vue_version` | string | ❌ | Vue version (for Vue only) |
| `repo_visibility` | string | ❌ | `"public"` or `"private"` (default: `"public"`) |

### Available Options

| Project Type | Versions Available |
|--------------|-------------------|
| `django` | python: `3.10`, `3.11`, `3.12` / django: `4.2`, `5.0`, `5.1` |
| `fastapi` | python: `3.10`, `3.11`, `3.12` / fastapi: `0.109`, `0.110`, `0.111`, `0.115` |
| `pytorch` | python: `3.10`, `3.11`, `3.12` / pytorch: `2.1`, `2.2`, `2.3`, `2.4`, `2.5` |
| `jupyter` | python: `3.10`, `3.11`, `3.12` |
| `react` | node: `18`, `20`, `22` / react: `18`, `19` |
| `vue` | node: `18`, `20`, `22` / vue: `3.4`, `3.5` |

### Example: Create Django Project

**URL:**
```
https://{ask-author-for-url}
```

**Method:** `POST`

**Payload:**
```json
{
  "method": "init",
  "project_type": "django",
  "project_name": "my_django_app",
  "python_version": "3.12",
  "django_version": "5.1",
  "repo_visibility": "public"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Workflow triggered successfully",
  "project_type": "django",
  "project_name": "my_django_app",
  "inputs": {
    "project_name": "my_django_app",
    "python_version": "3.12",
    "django_version": "5.1",
    "repo_visibility": "public"
  },
  "repository_url": "https://github.com/hz3866/my_django_app"
}
```

### Example: Create FastAPI Project

**URL:**
```
https://{ask-author-for-url}
```

**Method:** `POST`

**Payload:**
```json
{
  "method": "init",
  "project_type": "fastapi",
  "project_name": "my_api_service",
  "python_version": "3.11",
  "fastapi_version": "0.115"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Workflow triggered successfully",
  "project_type": "fastapi",
  "project_name": "my_api_service",
  "inputs": {
    "project_name": "my_api_service",
    "python_version": "3.11",
    "fastapi_version": "0.115",
    "repo_visibility": "public"
  },
  "repository_url": "https://github.com/hz3866/my_api_service"
}
```

### Example: Create React Project

**URL:**
```
https://{ask-author-for-url}
```

**Method:** `POST`

**Payload:**
```json
{
  "method": "init",
  "project_type": "react",
  "project_name": "my_react_frontend",
  "node_version": "20",
  "react_version": "19"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Workflow triggered successfully",
  "project_type": "react",
  "project_name": "my_react_frontend",
  "inputs": {
    "project_name": "my_react_frontend",
    "node_version": "20",
    "react_version": "19",
    "repo_visibility": "public"
  },
  "repository_url": "https://github.com/hz3866/my_react_frontend"
}
```

### Example: Create Vue Project

**URL:**
```
https://{ask-author-for-url}
```

**Method:** `POST`

**Payload:**
```json
{
  "method": "init",
  "project_type": "vue",
  "project_name": "my_vue_app",
  "node_version": "20",
  "vue_version": "3.5"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Workflow triggered successfully",
  "project_type": "vue",
  "project_name": "my_vue_app",
  "inputs": {
    "project_name": "my_vue_app",
    "node_version": "20",
    "vue_version": "3.5",
    "repo_visibility": "public"
  },
  "repository_url": "https://github.com/hz3866/my_vue_app"
}
```

### Example: Create PyTorch Project

**URL:**
```
https://{ask-author-for-url}
```

**Method:** `POST`

**Payload:**
```json
{
  "method": "init",
  "project_type": "pytorch",
  "project_name": "ml_training_pipeline",
  "python_version": "3.11",
  "pytorch_version": "2.5"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Workflow triggered successfully",
  "project_type": "pytorch",
  "project_name": "ml_training_pipeline",
  "inputs": {
    "project_name": "ml_training_pipeline",
    "python_version": "3.11",
    "pytorch_version": "2.5",
    "repo_visibility": "public"
  },
  "repository_url": "https://github.com/hz3866/ml_training_pipeline"
}
```

### Example: Create Jupyter Project

**URL:**
```
https://{ask-author-for-url}
```

**Method:** `POST`

**Payload:**
```json
{
  "method": "init",
  "project_type": "jupyter",
  "project_name": "data_analysis",
  "python_version": "3.11"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Workflow triggered successfully",
  "project_type": "jupyter",
  "project_name": "data_analysis",
  "inputs": {
    "project_name": "data_analysis",
    "python_version": "3.11",
    "repo_visibility": "public"
  },
  "repository_url": "https://github.com/hz3866/data_analysis"
}
```

### Error Response

**Payload:**
```json
{
  "method": "init",
  "project_type": "django",
  "project_name": "123_invalid"
}
```

**Response:**
```json
{
  "error": "Validation error",
  "message": "Invalid project_name. Must start with a letter and contain only letters, numbers, and underscores."
}
```

---

## Method 2: `search` - List Repositories and Branches

Lists all repositories under the GitHub owner (excluding `ProjectInitializer`) with their branches.

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `method` | string | ✅ | - | Must be `"search"` |
| `include_branches` | boolean | ❌ | `true` | Whether to fetch branches for each repo |
| `per_page` | integer | ❌ | `100` | Number of repos to return (max: 100) |

### Example: List All Repos with Branches

**URL:**
```
https://{ask-author-for-url}
```

**Method:** `POST`

**Payload:**
```json
{
  "method": "search",
  "include_branches": true
}
```

**Response:**
```json
{
  "success": true,
  "count": 3,
  "repositories": [
    {
      "name": "my_django_app",
      "full_name": "hz3866/my_django_app",
      "description": null,
      "url": "https://github.com/hz3866/my_django_app",
      "default_branch": "master",
      "private": false,
      "updated_at": "2024-12-15T10:30:00Z",
      "language": "Python",
      "branches": [
        {
          "name": "master",
          "protected": false
        },
        {
          "name": "develop",
          "protected": false
        }
      ]
    },
    {
      "name": "my_react_frontend",
      "full_name": "hz3866/my_react_frontend",
      "description": "React frontend application",
      "url": "https://github.com/hz3866/my_react_frontend",
      "default_branch": "main",
      "private": true,
      "updated_at": "2024-12-14T15:20:00Z",
      "language": "TypeScript",
      "branches": [
        {
          "name": "main",
          "protected": false
        }
      ]
    }
  ]
}
```

### Example: List Repos Without Branches

**URL:**
```
https://{ask-author-for-url}
```

**Method:** `POST`

**Payload:**
```json
{
  "method": "search",
  "include_branches": false
}
```

**Response:**
```json
{
  "success": true,
  "count": 3,
  "repositories": [
    {
      "name": "my_django_app",
      "full_name": "hz3866/my_django_app",
      "description": null,
      "url": "https://github.com/hz3866/my_django_app",
      "default_branch": "master",
      "private": false,
      "updated_at": "2024-12-15T10:30:00Z",
      "language": "Python"
    }
  ]
}
```

---

## Method 3: `build` - Trigger Docker Build & Push

Triggers the `docker-build-push.yml` workflow for a specific repository and branch.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `method` | string | ✅ | Must be `"build"` |
| `repo` | string | ✅ | Repository name (e.g., `"my_django_app"`) |
| `branch` | string | ✅ | Branch name (e.g., `"master"`, `"main"`, `"develop"`) |

### Example: Build from Master Branch

**URL:**
```
https://{ask-author-for-url}
```

**Method:** `POST`

**Payload:**
```json
{
  "method": "build",
  "repo": "my_django_app",
  "branch": "master"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Docker build workflow triggered successfully",
  "repository": "my_django_app",
  "branch": "master",
  "workflow": "docker-build-push.yml",
  "repository_url": "https://github.com/hz3866/my_django_app",
  "actions_url": "https://github.com/hz3866/my_django_app/actions"
}
```

### Example: Build from Feature Branch

**URL:**
```
https://{ask-author-for-url}
```

**Method:** `POST`

**Payload:**
```json
{
  "method": "build",
  "repo": "my_django_app",
  "branch": "feature/user_auth"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Docker build workflow triggered successfully",
  "repository": "my_django_app",
  "branch": "feature/user_auth",
  "workflow": "docker-build-push.yml",
  "repository_url": "https://github.com/hz3866/my_django_app",
  "actions_url": "https://github.com/hz3866/my_django_app/actions"
}
```

### Error: Repository Not Found

**Payload:**
```json
{
  "method": "build",
  "repo": "non_existent_repo",
  "branch": "master"
}
```

**Response:**
```json
{
  "error": "Repository not found",
  "message": "Repository 'non_existent_repo' does not exist or is not accessible"
}
```

### Error: Branch Not Found

**Payload:**
```json
{
  "method": "build",
  "repo": "my_django_app",
  "branch": "non_existent_branch"
}
```

**Response:**
```json
{
  "error": "Branch not found",
  "message": "Branch 'non_existent_branch' does not exist in repository 'my_django_app'"
}
```

### Error: Workflow Not Found

**Payload:**
```json
{
  "method": "build",
  "repo": "old_repo_without_workflow",
  "branch": "master"
}
```

**Response:**
```json
{
  "error": "Workflow not found",
  "message": "Workflow 'docker-build-push.yml' does not exist in repository 'old_repo_without_workflow'. Make sure the repository was created with ProjectInitializer."
}
```

---

## Method 4: `status` - Get Workflow Run Status

Gets recent workflow runs for a repository to check build status.

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `method` | string | ✅ | - | Must be `"status"` |
| `repo` | string | ✅ | - | Repository name |
| `workflow` | string | ❌ | `"docker-build-push.yml"` | Workflow filename |
| `per_page` | integer | ❌ | `5` | Number of runs to return (max: 20) |

### Example: Get Recent Build Status

**URL:**
```
https://{ask-author-for-url}
```

**Method:** `POST`

**Payload:**
```json
{
  "method": "status",
  "repo": "my_django_app"
}
```

**Response:**
```json
{
  "success": true,
  "repository": "my_django_app",
  "workflow": "docker-build-push.yml",
  "total_count": 15,
  "runs": [
    {
      "id": 12345678901,
      "status": "completed",
      "conclusion": "success",
      "branch": "master",
      "commit_sha": "abc1234",
      "created_at": "2024-12-15T10:30:00Z",
      "updated_at": "2024-12-15T10:35:00Z",
      "url": "https://github.com/hz3866/my_django_app/actions/runs/12345678901"
    },
    {
      "id": 12345678900,
      "status": "completed",
      "conclusion": "failure",
      "branch": "develop",
      "commit_sha": "def5678",
      "created_at": "2024-12-14T15:20:00Z",
      "updated_at": "2024-12-14T15:25:00Z",
      "url": "https://github.com/hz3866/my_django_app/actions/runs/12345678900"
    },
    {
      "id": 12345678899,
      "status": "in_progress",
      "conclusion": null,
      "branch": "master",
      "commit_sha": "ghi9012",
      "created_at": "2024-12-15T11:00:00Z",
      "updated_at": "2024-12-15T11:02:00Z",
      "url": "https://github.com/hz3866/my_django_app/actions/runs/12345678899"
    }
  ]
}
```

### Example: Get More Runs

**URL:**
```
https://{ask-author-for-url}
```

**Method:** `POST`

**Payload:**
```json
{
  "method": "status",
  "repo": "my_django_app",
  "per_page": 20
}
```

### Status Values

| Status | Description |
|--------|-------------|
| `queued` | Workflow is waiting to run |
| `in_progress` | Workflow is currently running |
| `completed` | Workflow has finished |

### Conclusion Values (when status is `completed`)

| Conclusion | Description |
|------------|-------------|
| `success` | All jobs passed ✅ |
| `failure` | One or more jobs failed ❌ |
| `cancelled` | Workflow was cancelled |
| `skipped` | Workflow was skipped |
| `timed_out` | Workflow timed out |

---

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

### Common Errors

| HTTP Code | Error | Cause |
|-----------|-------|-------|
| 400 | Invalid method | `method` field is missing or invalid |
| 400 | Validation error | Invalid input parameters |
| 400 | Missing required field | Required field not provided |
| 404 | Repository not found | Repository doesn't exist |
| 404 | Branch not found | Branch doesn't exist |
| 404 | Workflow not found | Workflow file not in repository |
| 500 | GitHub API error | GitHub API returned an error |
| 500 | Server configuration error | Missing environment variables |

---

## Complete Workflow Example

### Step 1: Create a new Django project

**URL:**
```
https://{ask-author-for-url}
```

**Method:** `POST`

**Payload:**
```json
{
  "method": "init",
  "project_type": "django",
  "project_name": "my_awesome_app",
  "python_version": "3.12",
  "django_version": "5.1",
  "repo_visibility": "public"
}
```

### Step 2: Wait for project creation (~30 seconds)

### Step 3: Verify project appears in search

**URL:**
```
https://{ask-author-for-url}
```

**Method:** `POST`

**Payload:**
```json
{
  "method": "search"
}
```

### Step 4: Trigger a Docker build

**URL:**
```
https://{ask-author-for-url}
```

**Method:** `POST`

**Payload:**
```json
{
  "method": "build",
  "repo": "my_awesome_app",
  "branch": "master"
}
```

### Step 5: Check build status

**URL:**
```
https://{ask-author-for-url}
```

**Method:** `POST`

**Payload:**
```json
{
  "method": "status",
  "repo": "my_awesome_app"
}
```

---

## License

MIT
