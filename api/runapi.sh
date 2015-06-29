# needed by mjpg-streamer binary
echo "export LD_LIBRARY_PATH=/usr/local/lib/"

sudo gunicorn --pid "/var/run/xm.pid" --bind 0.0.0.0:80  hear:app
