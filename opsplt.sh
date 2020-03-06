#!/bin/bash
PYENV_DIR=/opt/opsplt_env/bin/activate
PROJ_DIR=/opt/opsplt
UWSGI_FILE=${PROJ_DIR}/uwsgi.ini

if [[ $# -eq 0 ]];
then
	echo "Usage: $0 start | $0 stop | $0 restart"
fi

function start() {
	source ${PYENV_DIR}
	pid=`ps -ef | grep /opt/opsplt/uwsgi.ini | grep -v grep | wc -l`
	if [[ ${pid} -gt 0 ]];
	then
		cd ${PROJ_DIR}
    /opt/opsplt_env/bin/uwsgi --stop ${PROJ_DIR}/opsplt.pid
	fi
	/opt/opsplt_env/bin/uwsgi --ini ${UWSGI_FILE}
}

function stop() {
	source ${PYENV_DIR}
	pid=`ps -ef | grep /opt/opsplt/uwsgi.ini | grep -v grep | wc -l`
	if [[ ${pid} -gt 0 ]];
	then
		cd ${PROJ_DIR}
		/opt/opsplt_env/bin/uwsgi --stop ${PROJ_DIR}/opsplt.pid
	fi
}

function restart() {
	stop
	sleep 2
	start
}

case "$1" in
	"start")
		start
		;;
	"stop")
		stop
		;;
	"restart")
		restart
		;;
esac 
