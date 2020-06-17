# 基础环境
python3.6
yum install -y sshpass rabbitmq-server redis mariadb-server mariadb-devel
rabbitmqctl add_vhost vhost
rabbitmqctl add_user opsplt opsplt
rabbitmqctl set_permissions -p vhost opsplt ".*" ".*" ".*"
# pip install
cd opsplt
pip install -r requirements
# 启动
nohup python manage.py runserver 0.0.0.0:8000 > opsplt.log 2>&1 &
nohup python manage.py celery worker -l debug > opsplt-celery.log 2>&1 &
