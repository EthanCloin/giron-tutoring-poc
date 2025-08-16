import os


workers = int(os.environ.get("GUNICORN_PROCESSES", "2"))
threads = int(os.environ.get("GUNICORN_THREADS", "4"))
# timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))

# TODO: make this an env var?
bind = os.environ.get("GUNICORN_BIND", "unix:/tmp/gunicorn2.sock")
forwarded_allow_ips = "*"
secure_scheme_headers = {"X-Forwarded-Proto": "https"}

