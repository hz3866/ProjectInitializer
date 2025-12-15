# Lambda Function Deployment

This folder contains the AWS Lambda function for ProjectInitializer API.

## Files

| File | Description |
|------|-------------|
| `lambda_function.py` | Main Lambda handler with all API methods |
| `template.yaml` | AWS SAM template for deployment |

## Prerequisites

1. AWS CLI configured with appropriate credentials
2. AWS SAM CLI installed
3. GitHub Personal Access Token with `repo` + `workflow` permissions

## Deployment Options

### Option 1: AWS SAM (Recommended)

```bash
# Navigate to LF folder
cd LF

# Build
sam build

# Deploy (first time - guided)
sam deploy --guided

# Deploy (subsequent times)
sam deploy
```

During guided deployment, you'll be prompted for:
- **Stack Name**: `projectinitializer-api`
- **AWS Region**: Your preferred region
- **GitHubToken**: Your GitHub PAT
- **GitHubOwner**: Your GitHub username (e.g., `hz3866`)
- **GitHubRepo**: `ProjectInitializer`

### Option 2: AWS Console (Manual)

1. Go to AWS Lambda Console
2. Create new function:
   - Runtime: Python 3.11
   - Handler: `lambda_function.lambda_handler`
3. Upload `lambda_function.py`
4. Add Environment Variables:
   - `GITHUB_TOKEN`: Your GitHub PAT
   - `GITHUB_OWNER`: Your GitHub username
   - `GITHUB_REPO`: `ProjectInitializer`
5. Create API Gateway trigger:
   - Type: REST API
   - Method: POST
   - Path: `/project`
   - Enable CORS

### Option 3: AWS CLI

```bash
# Create deployment package
zip lambda.zip lambda_function.py

# Create Lambda function
aws lambda create-function \
  --function-name ProjectInitializer \
  --runtime python3.11 \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://lambda.zip \
  --role arn:aws:iam::{ACCOUNT_ID}:role/{LAMBDA_ROLE} \
  --environment Variables="{GITHUB_TOKEN=ghp_xxx,GITHUB_OWNER=hz3866,GITHUB_REPO=ProjectInitializer}"

# Update function code
aws lambda update-function-code \
  --function-name ProjectInitializer \
  --zip-file fileb://lambda.zip
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GITHUB_TOKEN` | GitHub PAT (repo + workflow) | `ghp_xxxxxxxxxxxx` |
| `GITHUB_OWNER` | GitHub username/org | `hz3866` |
| `GITHUB_REPO` | Template repo name | `ProjectInitializer` |

## API Endpoints

After deployment, your API endpoint will be:

```
POST https://{api-id}.execute-api.{region}.amazonaws.com/prod/project
```

## Testing

### Test with curl

```bash
# Test search method
curl -X POST https://{your-api-url}/prod/project \
  -H "Content-Type: application/json" \
  -d '{"method": "search"}'

# Test init method
curl -X POST https://{your-api-url}/prod/project \
  -H "Content-Type: application/json" \
  -d '{
    "method": "init",
    "project_type": "django",
    "project_name": "test-project"
  }'
```

### Test locally with SAM

```bash
# Start local API
sam local start-api --env-vars env.json

# env.json format:
# {
#   "ProjectInitializerFunction": {
#     "GITHUB_TOKEN": "ghp_xxx",
#     "GITHUB_OWNER": "hz3866",
#     "GITHUB_REPO": "ProjectInitializer"
#   }
# }
```

## IAM Permissions

The Lambda execution role needs basic permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

Note: No additional AWS permissions are needed since the function only calls GitHub API.

## Updating

After modifying `lambda_function.py`:

```bash
# With SAM
sam build && sam deploy

# With AWS CLI
zip lambda.zip lambda_function.py
aws lambda update-function-code \
  --function-name ProjectInitializer \
  --zip-file fileb://lambda.zip
```
