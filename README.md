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

```
POST https://{your-api-gateway-url}/prod/project
Content-Type: application/json
```

All requests use **POST** method with a JSON body containing a `method` field.

---

## Method 1: `init` - Create New Project

Creates a new repository from a template with full CI/CD setup.

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `method` | string | ✅ | Must be `"init"` |
| `project_type` | string | ✅ | Template type (see options below) |
| `project_name` | string | ✅ | Repository name (letters, numbers, hyphens, underscores) |
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

### Example Request - Django Project

```bash
curl -X POST https://{api-url}/prod/project \
  -H "Content-Type: application/json" \
  -d '{
    "method": "init",
    "project_type": "django",
    "project_name": "my-django-app",
    "python_version": "3.12",
    "django_version": "5.1",
    "repo_visibility": "private"
  }'
```

### Example Response - Success

```json
{
  "success": true,
  "message": "Workflow triggered successfully",
  "project_type": "django",
  "project_name": "my-django-app",
  "inputs": {
    "project_name": "my-django-app",
    "python_version": "3.12",
    "django_version": "5.1",
    "repo_visibility": "private"
  },
  "repository_url": "https://github.com/hz3866/my-django-app"
}
```

### Example Request - FastAPI Project

```bash
curl -X POST https://{api-url}/prod/project \
  -H "Content-Type: application/json" \
  -d '{
    "method": "init",
    "project_type": "fastapi",
    "project_name": "my-api-service",
    "python_version": "3.11",
    "fastapi_version": "0.115"
  }'
```

### Example Request - React Project

```bash
curl -X POST https://{api-url}/prod/project \
  -H "Content-Type: application/json" \
  -d '{
    "method": "init",
    "project_type": "react",
    "project_name": "my-react-frontend",
    "node_version": "20",
    "react_version": "19"
  }'
```

### Example Request - PyTorch Project

```bash
curl -X POST https://{api-url}/prod/project \
  -H "Content-Type: application/json" \
  -d '{
    "method": "init",
    "project_type": "pytorch",
    "project_name": "ml-training-pipeline",
    "python_version": "3.11",
    "pytorch_version": "2.5"
  }'
```

### Example Response - Error

```json
{
  "error": "Validation error",
  "message": "Invalid project_name. Must start with a letter and contain only letters, numbers, hyphens, and underscores."
}
```

---

## Method 2: `search` - List Repositories and Branches

Lists all repositories under the GitHub owner (excluding `ProjectInitializer`) with their branches.

### Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `method` | string | ✅ | - | Must be `"search"` |
| `include_branches` | boolean | ❌ | `true` | Whether to fetch branches for each repo |
| `per_page` | integer | ❌ | `100` | Number of repos to return (max: 100) |

### Example Request

```bash
curl -X POST https://{api-url}/prod/project \
  -H "Content-Type: application/json" \
  -d '{
    "method": "search",
    "include_branches": true
  }'
```

### Example Response

```json
{
  "success": true,
  "count": 3,
  "repositories": [
    {
      "name": "my-django-app",
      "full_name": "hz3866/my-django-app",
      "description": null,
      "url": "https://github.com/hz3866/my-django-app",
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
        },
        {
          "name": "feature/user-auth",
          "protected": false
        }
      ]
    },
    {
      "name": "my-react-frontend",
      "full_name": "hz3866/my-react-frontend",
      "description": "React frontend application",
      "url": "https://github.com/hz3866/my-react-frontend",
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
    },
    {
      "name": "ml-training-pipeline",
      "full_name": "hz3866/ml-training-pipeline",
      "description": "PyTorch ML project",
      "url": "https://github.com/hz3866/ml-training-pipeline",
      "default_branch": "master",
      "private": false,
      "updated_at": "2024-12-13T08:45:00Z",
      "language": "Python",
      "branches": [
        {
          "name": "master",
          "protected": false
        },
        {
          "name": "experiment/new-model",
          "protected": false
        }
      ]
    }
  ]
}
```

### Example Request - Without Branches

```bash
curl -X POST https://{api-url}/prod/project \
  -H "Content-Type: application/json" \
  -d '{
    "method": "search",
    "include_branches": false
  }'
```

---

## Method 3: `build` - Trigger Docker Build & Push

Triggers the `docker-build-push.yml` workflow for a specific repository and branch.

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `method` | string | ✅ | Must be `"build"` |
| `repo` | string | ✅ | Repository name (e.g., `"my-django-app"`) |
| `branch` | string | ✅ | Branch name (e.g., `"master"`, `"main"`, `"develop"`) |

### Example Request

```bash
curl -X POST https://{api-url}/prod/project \
  -H "Content-Type: application/json" \
  -d '{
    "method": "build",
    "repo": "my-django-app",
    "branch": "master"
  }'
```

### Example Response - Success

```json
{
  "success": true,
  "message": "Docker build workflow triggered successfully",
  "repository": "my-django-app",
  "branch": "master",
  "workflow": "docker-build-push.yml",
  "repository_url": "https://github.com/hz3866/my-django-app",
  "actions_url": "https://github.com/hz3866/my-django-app/actions"
}
```

### Example Request - Build from Feature Branch

```bash
curl -X POST https://{api-url}/prod/project \
  -H "Content-Type: application/json" \
  -d '{
    "method": "build",
    "repo": "my-django-app",
    "branch": "feature/user-auth"
  }'
```

### Example Response - Repository Not Found

```json
{
  "error": "Repository not found",
  "message": "Repository 'non-existent-repo' does not exist or is not accessible"
}
```

### Example Response - Branch Not Found

```json
{
  "error": "Branch not found",
  "message": "Branch 'non-existent-branch' does not exist in repository 'my-django-app'"
}
```

### Example Response - Workflow Not Found

```json
{
  "error": "Workflow not found",
  "message": "Workflow 'docker-build-push.yml' does not exist in repository 'my-django-app'. Make sure the repository was created with ProjectInitializer."
}
```

---

## Method 4: `status` - Get Workflow Run Status

Gets recent workflow runs for a repository to check build status.

### Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `method` | string | ✅ | - | Must be `"status"` |
| `repo` | string | ✅ | - | Repository name |
| `workflow` | string | ❌ | `"docker-build-push.yml"` | Workflow filename |
| `per_page` | integer | ❌ | `5` | Number of runs to return (max: 20) |

### Example Request

```bash
curl -X POST https://{api-url}/prod/project \
  -H "Content-Type: application/json" \
  -d '{
    "method": "status",
    "repo": "my-django-app"
  }'
```

### Example Response

```json
{
  "success": true,
  "repository": "my-django-app",
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
      "url": "https://github.com/hz3866/my-django-app/actions/runs/12345678901"
    },
    {
      "id": 12345678900,
      "status": "completed",
      "conclusion": "failure",
      "branch": "develop",
      "commit_sha": "def5678",
      "created_at": "2024-12-14T15:20:00Z",
      "updated_at": "2024-12-14T15:25:00Z",
      "url": "https://github.com/hz3866/my-django-app/actions/runs/12345678900"
    },
    {
      "id": 12345678899,
      "status": "in_progress",
      "conclusion": null,
      "branch": "master",
      "commit_sha": "ghi9012",
      "created_at": "2024-12-15T11:00:00Z",
      "updated_at": "2024-12-15T11:02:00Z",
      "url": "https://github.com/hz3866/my-django-app/actions/runs/12345678899"
    }
  ]
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

### Example Request - Get More Runs

```bash
curl -X POST https://{api-url}/prod/project \
  -H "Content-Type: application/json" \
  -d '{
    "method": "status",
    "repo": "my-django-app",
    "per_page": 20
  }'
```

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

Here's a complete example of creating a project and then building it:

### Step 1: Create a new Django project

```bash
curl -X POST https://{api-url}/prod/project \
  -H "Content-Type: application/json" \
  -d '{
    "method": "init",
    "project_type": "django",
    "project_name": "my-awesome-app",
    "python_version": "3.12",
    "django_version": "5.1",
    "repo_visibility": "public"
  }'
```

### Step 2: Wait for project creation (~30 seconds)

### Step 3: Verify project appears in search

```bash
curl -X POST https://{api-url}/prod/project \
  -H "Content-Type: application/json" \
  -d '{
    "method": "search"
  }'
```

### Step 4: Trigger a Docker build

```bash
curl -X POST https://{api-url}/prod/project \
  -H "Content-Type: application/json" \
  -d '{
    "method": "build",
    "repo": "my-awesome-app",
    "branch": "master"
  }'
```

### Step 5: Check build status

```bash
curl -X POST https://{api-url}/prod/project \
  -H "Content-Type: application/json" \
  -d '{
    "method": "status",
    "repo": "my-awesome-app"
  }'
```

---

## License

MIT
