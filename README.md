# Pad

Pad is a notepad.cc clone written in Python

## Installation on dev

```bash
git clone https://github.com/dotzero/Pad
cd Pad
pip install -r requirements.txt
python app.py
```

## Configuration

Configuration should be declared within `app.py` file.

You can declare via a Redis URL containing the database.

```python
app.config['REDIS_URL'] = "redis://:password@localhost:6379/0"
```

To turn off debug mode

```python
app.run(debug=False)
```

## Installation on production

Example of `wsgi.py`

```python
from app import app

# set password for redis
app.config['REDIS_URL'] = "redis://:strongpassword@localhost:6379/0"

if __name__ == "__main__":
    app.run()
```

Example of `uwsgi.ini`

```ini
[uwsgi]
; env
virtualenv = /path/virtual_env/dir
chdir = /path/project/dir
pythonpath = .

; app
wsgi-file = wsgi.py
callable = app

; other
pidfile = /tmp/uwsgi_pad.pid
master = true
processes = 2
harakiri = 30
buffer-size = 32768
vacuum = true
	
[prod]
ini = :uwsgi
socket = 127.0.0.1:8001
stats = 127.0.0.1:8002
```

Example of `supervisor.conf`

```ini
[program:pad_uwsgi]
; env
user=username
environment=HOME="/home/username",USER="username"
directory=/path/project/dir

; run command
command=/usr/local/bin/uwsgi --ini uwsgi/uwsgi.ini:prod

; logs
stdout_logfile=/var/log/supervisor/%(program_name)s-std.log
stderr_logfile=/var/log/supervisor/%(program_name)s-err.log
stdout_logfile_maxbytes=10MB
stdout_logfile_backups=10
stdout_capture_maxbytes=1MB

; autorun
autostart=true
autorestart=true
```
