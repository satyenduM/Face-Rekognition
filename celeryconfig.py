import os

broker_url = os.environ.get('REDIS_URL')
result_backend = os.environ.get('REDIS_URL')
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True