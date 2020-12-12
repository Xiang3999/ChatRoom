import json

# 打开 config 配置文件
with open('config.json') as config_file:
    config = json.load(config_file)

# 返回config
def get_config():
    return config
