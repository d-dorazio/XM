#!/bin/sh
### BEGIN INIT INFO
# Provides:          XM API
# Required-Start:    $local_fs $network $named $time $syslog
# Required-Stop:     $local_fs $network $named $time $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Description:       XM API service
### END INIT INFO


XMAPI="/home/pi/XM/api"         # xm api dir
SCRIPT=$XMAPI/"runapi.sh"

PIDFILE="/var/run/xm.pid"

start() {
  if [ -f "/var/run/$PIDNAME" ] && kill -0 "$(cat /var/run/"$PIDNAME")"; then
    echo 'Service already running' >&2
    return 1
  fi
  echo 'Starting service¦' >&2
  cd $XMAPI
  $SCRIPT &
  echo 'Service started' >&2

  sleep 2
  until curl --fail http://127.0.0.1/api/open_eyes; do
    sleep 2
  done

}

stop() {
  if [ ! -f "$PIDFILE" ] || ! kill -0 "$(cat $PIDFILE)"
  then
    echo 'Service not running' >&2
    return 1
  fi
  echo 'Stopping service¦' >&2

  curl http://127.0.0.1/api/shutup
  curl http://127.0.0.1/api/close_eyes
  kill -15 "$(cat "$PIDFILE")" && rm -f "$PIDFILE"
  echo 'Service stopped' >&2
}

status() {
  if [ ! -f "$PIDFILE" ] || ! kill -0 "$(cat $PIDFILE)"
  then
    echo 'Service not running' >&2
    return 1
  else
    echo 'Service running'
  fi

}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart)
    stop
    start
    ;;
  status)
    status
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|status}"
esac
