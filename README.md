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
└── templates/
    ├── shared/                    # Shared across all projects
    │   └── .github/workflows/
    │       └── docker-build-push.yml
    │
    ├── django/
    │   ├── Dockerfile.template
    │   ├── .gitignore
    │   └── .env.example
    │
    ├── fastapi/
    ├── react/
    ├── vue/
    ├── pytorch/
    └── jupyter/
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

## AWS Integration

To trigger builds from AWS (e.g., via Lambda or EventBridge):

```bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer ${GITHUB_PAT}" \
  https://api.github.com/repos/{owner}/{repo}/actions/workflows/docker-build-push.yml/dispatches \
  -d '{"ref":"main"}'
```

## Customization

### Adding New Templates

1. Create a new folder under `templates/`
2. Add framework-specific files (Dockerfile.template, .gitignore, etc.)
3. Create a new workflow in `.github/workflows/init-{framework}.yml`
4. Use `{{PLACEHOLDER}}` syntax in templates for variable substitution

### Modifying CI/CD Pipeline

Edit `templates/shared/.github/workflows/docker-build-push.yml` to modify the CI/CD pipeline for all projects.

## License

MIT
