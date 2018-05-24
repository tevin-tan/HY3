#!/usr/bin/env bash

. /etc/init.d/functions
#echo "Stopping Tomcat ..."
/usr/local/tomcat/tomcat-8080-houseloan/bin/shutdown.sh
sleep 5
ps -ef |grep -v grep |grep java |grep tomcat>/dev/null 2>&1;pidstatus=$?

if [ "${pidstatus}" == 0 ];then
   echo "Stop tomcat failed, trying to force kill ..."
   kill -9 `ps -ef |grep -v grep |grep java|grep tomcat|awk '{print $2}'`
   ps -ef |grep -v grep |grep java |grep tomcat>/dev/null 2>&1;pidstatus=$?
   [ "${pidstatus}" == 0 ] && {
   action "Stop tomcat  ... " /bin/false
   exit 1
   }
fi
action "Stoped tomcat  ... " /bin/true
/usr/local/tomcat/tomcat-8080-houseloan/bin/start.sh