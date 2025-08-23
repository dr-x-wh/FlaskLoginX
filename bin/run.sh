#!/bin/bash

export RUN_MAIN=false
echo "对比差异"
flask db migrate -m "init"
echo "执行数据库迁移"
flask db upgrade

echo "启动 Gunicorn"
export RUN_MAIN=true
gunicorn -c gunicorn.py run:app
