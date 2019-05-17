#!/bin/bash
PYENV_DIR=/opt/py36/bin/activate
PROJ_DIR=/opt/opsplt
UWSGI_FILE=${PROJ_DIR}/uwsgi.ini

if [[ $# -eq 0 ]];
then
	echo "Usage: $0 start | $0 stop | $0 restart"
fi

function start() {
	source ${PYENV_DIR}
	pid=`ps -ef | grep uwsgi | grep -v grep | wc -l`
	if [[ ${pid} -gt 0 ]];
	then
		cd ${PROJ_DIR}
		uwsgi --stop ${PROJ_DIR}/opsplt.pid
	fi
	uwsgi --ini ${UWSGI_FILE}
}

function stop() {
	source ${PYENV_DIR}
	pid=`ps -ef | grep uwsgi | grep -v grep | wc -l`
	if [[ ${pid} -gt 0 ]];
	then
		cd ${PROJ_DIR}
		uwsgi --stop ${PROJ_DIR}/opsplt.pid
	fi
}

function restart() {
	stop
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
