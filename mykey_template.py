
oai_config = {
    'apikey':'sk-uklURcj',
    'apibase':"http://243.55.19.137:2001",
    'model':"openai/gpt-5.1",
    'api_mode':"chat_completions",  # optional: "chat_completions" | "responses"
    'max_retries': 2,               # optional: retries for 429/timeout/5xx
    'connect_timeout': 10,          # optional: seconds
    'read_timeout': 120             # optional: seconds (stream read)
}

# or

sider_cookie = 'token=Bearer%20eyJhbGciOiJIUz...'

# feel free to add more ~
oai_config2 = {
    'apikey':'sk-uklURcj...',
    'apibase':"http://243.55.19.137:2001",
    'model':"claude-opus-4-6-20260206"
}


claude_config = {
    'apikey':'klURcj...',
    'apibase':"http://233.85.13.149:2001",
    'model':"claude-opus"
}

# If you need them
# tg_bot_token = '84102K2gYZ...'
# tg_allowed_users = [6806...]
# qq_app_id = '123456789'
# qq_app_secret = 'xxxxxxxxxxxxxxxx'
# qq_allowed_users = ['your_user_openid']  # 留空或 ['*'] 表示允许所有 QQ 用户
# fs_app_id = 'cli_xxxxxxxxxxxxxxxx'
# fs_app_secret = 'xxxxxxxxxxxxxxxx'
# fs_allowed_users = ['ou_xxxxxxxxxxxxxxxx']  # 留空或 ['*'] 表示允许所有飞书用户
# wecom_bot_id = 'your_bot_id'
# wecom_secret = 'your_bot_secret'
# wecom_allowed_users = ['your_user_id']  # 留空或 ['*'] 表示允许所有企业微信用户
# wecom_welcome_message = '你好，我在线上。'
# dingtalk_client_id = 'your_app_key'
# dingtalk_client_secret = 'your_app_secret'
# dingtalk_allowed_users = ['your_staff_id']  # 留空或 ['*'] 表示允许所有钉钉用户

# proxy = "http://127.0.0.1:2082"
