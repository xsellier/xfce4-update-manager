# XFCE4 update manager

## Prerequisites

- [python3](https://www.python.org/downloads/)
- [python3-gi](https://wiki.gnome.org/Projects/PyGObject/)
- [pypi](https://pypi.python.org/pypi)
- [gksu](http://www.nongnu.org/gksu/)

### Install packages

Open a terminal and type

```shell
python3 setup.py install
```

### Run

```shell
python3 main.py
```

### Setup a cron job

```shell
crontab -e

# Execute every hour
0 * * * * /usr/bin/python3 /home/user/xfce4-update-manager/main.py
```