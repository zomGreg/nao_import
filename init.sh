#!/bin/bash

if [[ -n "$DBUSER" && -n "$DBPASS" && -n "$DBNAME" && -n "$DBHOST" ]]
then
	if [ $# -lt 1 ]
	then
	  echo "Usage: $0 start|stop|restart"
	  exit
	fi

	case "$1" in
	  restart)
	    PORT=${PORT:=5000}

      touch tmp/access.log
      touch tmp/error.log

	    if [ -a tmp/app.pid ]; then
        echo -n "Stopping App: "
        kill `cat tmp/app.pid`
        echo "done"
      else
        echo "Stopping App: done"
      fi

      echo -n "Starting App: "
      gunicorn -w 4 -b 0.0.0.0:$PORT --access-logfile tmp/access.log --error-logfile tmp/error.log -p tmp/app.pid --pythonpath api -D run:app
      echo "done"

      tail -f tmp/*.log
	  ;;
	  start)
	    PORT=${PORT:=5000}

	    touch tmp/access.log
	    touch tmp/error.log

	    echo -n "Starting App: "
	    gunicorn -w 4 -b 0.0.0.0:$PORT --access-logfile tmp/access.log --error-logfile tmp/error.log -p tmp/app.pid --pythonpath api -D run:app
	    echo "done"

      tail -f tmp/*.log
	  ;;
	  stop)
	    if [ -a tmp/app.pid ]; then
	      echo -n "Stopping App: "
	      kill `cat tmp/app.pid`
	      echo "done"
	    else
	      echo "Stopping App: done"
	    fi
	  ;;
		watch)
			echo "Watching for changes..."
			watchmedo shell-command --patterns="*.py" --recursive --command='echo "File ${watch_src_path} changed.  Restarting..." && kill -HUP `cat tmp/app.pid`' .
	esac
else
	echo "You must set the DBUSER, DBPASS, DBNAME, & DBHOST environment variables."
fi
