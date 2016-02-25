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
app.REDIS_URL = "redis://:password@localhost:6379/0"
```

To turn off debug mode

```python
app.run(debug=False)
```
