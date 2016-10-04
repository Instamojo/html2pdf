# Gunicorn Configuration File.
# See: http://docs.gunicorn.org/en/latest/settings.html

bind = '0.0.0.0:80'

# Send error logs to stderr
errorlog = '-'
accesslog='-'

workers = 3
threads = 1

# Workers silent for more than this many seconds are killed and restarted.
timeout = 300

# Restart workers once in a while, to limit memory leaks, if any.
max_requests = 300
max_requests_jitter = 60

# By preloading an application you can save some RAM resources as well as speed up server boot times.
preload_app = True
