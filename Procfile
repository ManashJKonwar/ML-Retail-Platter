worker-windows: celery -A tasks worker --without-gossip --without-mingle --without-heartbeat -O fair -P gevent -l INFO -f logs\tasks.log
worker-linux: celery -A tasks worker --without-gossip --without-mingle --without-heartbeat -O fair -P prefork -c 8 -l INFO -f logs\tasks.log
worker-purge: celery -A tasks purge