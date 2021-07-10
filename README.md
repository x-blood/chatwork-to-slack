# chatwork-to-slack
A serverless function that sends Chatwork message events to Slack. This function uses Chatwork's webhook. If you are not authorized, you need to apply to the administrator.

## Example Messages
![image](https://user-images.githubusercontent.com/8668892/125169475-45382580-e1e5-11eb-948b-82ae1bf4a5f6.png)

## Requirement
- Python:3.8
- AWS Chalice

## 1. Setup Method
### 1-1. Virtual environment (venv)
```bash
$ python3 -m venv myvenv
$ source ./myvenv/bin/activate
```

### 1-2. Installing AWS Chalice
```bash
$ pip install chalice
```

### 1-3. Setting environment variables
config.json is the target of .gitignore in this repository because it contains important information. Set the following values

| name | Sample value | remarks |
----|----|----
| SLACK_WEBHOOK_URL | https://hooks.slack.com/services/xxxx/xxxx/xxxx |  |
| SLACK_CHANNEL_ID | XXXXXXXXXXX |  |
| ALLOWED_TOKENS | ABC, DEF | Specify a comma-separated list of Chatwork webhook tokens. |

#### Example of config.json description
```json
{
  "version": "2.0",
  "app_name": "chatwork-to-slack",
  "stages": {
    "dev": {
      "api_gateway_stage": "api",
      "environment_variables": {
        "SLACK_WEBHOOK_URL": "https://hooks.slack.com/services/xxxx/xxxxx/xxxx",
        "SLACK_CHANNEL_ID": "XXXXXXXXXXX",
        "ALLOWED_TOKENS": "ABC, DEF"
      }
    },
    "prd": {
      "api_gateway_stage": "api",
      "environment_variables": {
        "SLACK_WEBHOOK_URL": "https://hooks.slack.com/services/xxxx/xxxx/xxxx",
        "SLACK_CHANNEL_ID": "XXXXXXXXXXX",
        "ALLOWED_TOKENS": "GHI"
      }
    }
  }
}

```

## 2. Deploy
Deploy for each stage described in config.json. It is recommended to set the default AWS profile in advance.

```bash
# For the development environment
$ chalice deploy --stage dev
```