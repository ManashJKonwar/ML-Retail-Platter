worker-windows: celery -A tasks worker --without-gossip --without-mingle --without-heartbeat -O fair -P gevent -c 4 -l INFO -f logs\tasks.log -Q pricing_queue  
worker-linux: celery -A tasks worker --without-gossip --without-mingle --without-heartbeat -O fair -P prefork -c 4 -l INFO -f logs\tasks.log -Q pricing_queue
worker-purge: celery -A tasks purge -Q pricing_queue