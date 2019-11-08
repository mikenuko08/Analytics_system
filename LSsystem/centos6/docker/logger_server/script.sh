#!/bin/bash
#===================================
# Script Name   : scriptlog.sh
# Description   : This script outputs the operation log for each user to the specified directory.
#===================================

LOGDIR=/var/log/script
LOGFILE=$(date +%s)_$(whoami).log
_SCRIPT=/usr/bin/script
#export TERM=dumb

P_PROC=`ps -ef|grep $PPID|grep bash|awk '{print $8}'`

if [ "$P_PROC" = -bash ]; then
  #/bin/script -faq ${LOGFILE}
  # タイムスタンプを追加
  ${_SCRIPT} -fq >(awk '{print strftime("%s"), $0} {fflush() }'>> ${LOGDIR}/${LOGFILE})
  exit
fi
unset _SCRIPT
unset P_PROC
