"""Gunicorn settings."""

# import multiprocessing
from os import getenv

# workers = multiprocessing.cpu_count() * 2 + 1  # production
workers = 2  # DEV ONLY!!!
worker_class = "sync"

timeout = 30  # in sec, for client requests

max_requests = 1000  # before auto reload
max_requests_jitter = 100  # add random num

accesslog = "-"  # access logs to stdout
errorlog = "-"   # error logs to stderr
loglevel = "info"

bind = f"{getenv('DJANGO_HOST', None)}:{getenv('DJANGO_PORT', None)}"

# daemon = True

threads = 4  # for each worker (use in threading)

graceful_timeout = 30  # before forcing connections to close

reload = True  # auto reload

# secure_scheme_headers = {'X-FORWARDED-PROTO': 'https'}
