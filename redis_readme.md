1. lunch ubuntu WSL
2. sudo service redis-server start
3.  redis-cli 
    127.0.0.1:6379> ping
    PONG
source ~/r_test/bin/activate - venv

python manage.py rqworker --with-scheduler