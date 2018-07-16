#!/usr/bin/env bash

count=3

function def_service_path(){
	#审批服务
	web_houseloan=/web/apache-tomcat-7.0.69
	#财务服务
	web_eam=/usr/local/tomcat-eam
	#资产对接 服务
	web_eam_batch=/usr/local/application/eam-batch
}


function def_service_process(){
	#获取审批系统服务进程号
	houseloan_info=$(ps -efww|grep -w $web_houseloan|grep -v catalina.out|grep -v grep|cut -c 9-15)
	#财务进程号
	eam_info=$(ps -efww|grep -w $web_eam|grep -v catalina.out|grep -v grep|cut -c 9-15)
	#资产对接进程号
	eam_batch_info=$(ps -efww|grep -w $web_eam_batch|grep -v eam-batch.log|grep -v grep|cut -c 9-15)
}

function def_email(){
	# 邮件服务地址
	email_host=906919789@qq.com,lumiayx@163.com
	email_title=房贷SIT服务器信息
	email_log=/data/svn-project/email
	email_sit_house_loan_log=sit-house-loan.log
	email_sit_eam_log=sit-eam.log
	email_sit_eam_batch=sit-eam-batch.log
}


function generate_log(){

	if [ -f "$email_log/$email_sit_house_loan_log" ];then
	 sit_house_loan_count=$(grep -o '1' "$email_log/$email_sit_house_loan_log" | wc -l)
	 if [ "$sit_house_loan_count" -ge "$count" ];then
	  $web_houseloan/bin/startup.sh
	  rm -rf $email_log/$email_sit_house_loan_log
	  echo "[SIT] The approval application server is being restarted" > log.txt
	  mailx -s $email_title $email_host < log.txt
	 else
	  echo ""
	 fi
	else
	 echo ""
	fi

	if [ -f "$email_log/$email_sit_eam_log" ];then
	 sit_eam_count=$(grep -o '1' "$email_log/$email_sit_eam_log" | wc -l)
	 if [ "$sit_eam_count" -ge "$count" ];then
	  $web_eam/bin/startup.sh
	  rm -rf $email_log/$email_sit_eam_log
	  echo "[SIT] The finance application server is being restarted" > log.txt
	  mailx -s $email_title $email_host < log.txt
	 else
	  echo ""
	 fi
	else
	 echo ""
	fi

	if [ -f "$email_log/$email_sit_eam_batch" ];then
	 sit_eam_batch_count=$(grep -o '1' "$email_log/$email_sit_eam_batch" | wc -l)
	 if [ "$sit_eam_batch_count" -ge "$count" ];then
	  $web_eam_batch/bin/start.sh
	  rm -rf $email_log/$email_sit_eam_batch
	  echo "[SIT] The finance run app is being restarted" > log.txt
	  mailx -s $email_title $email_host < log.txt
	 else
	  echo ""
	 fi
	else
	 echo ""
	fi
}


function generate_mail(){
	if [ ! -n "$houseloan_info" ];then
	  echo "1" >> $email_log/$email_sit_house_loan_log
	  echo "sit The approval server was shut down" > log.txt
	  mailx -s $email_title $email_host < log.txt
	  echo -e "approval status：\033[31m CLOSE \033[0m"
	else
		echo -e "approval status：\033[32m OPEN \033[0m"
		for i in $houseloan_info
		do
			echo "Approval PID：$i"
		done
	fi
	echo ""

	if [ ! -n "$eam_info" ];then
	  echo "1" >> $email_log/$email_sit_eam_log
	  echo "sit The finance application server was shut down" > log.txt
	  mailx -s $email_title $email_host < log.txt
	  echo -e "financial status：\033[31m CLOSE \033[0m"
	else
	  echo -e "financial status：\033[32m OPEN \033[0m"
		for i in $eam_info
		do
			echo "financial PID: $i"
		done
	fi
	echo ""

	 if [ ! -n "$eam_batch_info" ];then
	   echo "1" >> $email_log/$email_sit_eam_batch
	   echo "sit The finance runs the server by CLOSE" > log.txt
	   mailx -s $email_title $email_host < log.txt
		echo -e "Financial running status：\033[31m CLOSE \033[0m"
	  else
		echo -e "Financial running status：\033[32m OPEN \033[0m"
			  for i in $eam_batch_info
			  do
					   echo "Financial run batch PID: $i"
			  done
	  fi
	echo ""
}

function select_run(){

	echo ""
	echo "The existing packaged version"
	echo ""
	#房贷审批主干
	echo "Number[1] HouseLoan Main trunck    ==>truck"
	echo ""
	#房贷审批分支
	echo "Number[2] HouseLoan Main branch    ==>v3.8.0"
	echo ""
	#房贷大数据主干
	echo "Number[3] Mortgage big data backbone  ==>v1.0"
	echo ""
	#审批日志查看
	echo "Number[4] Approval log view"
	echo ""
	#财务日志查看
	echo "Number[5] Financial log view"
	echo ""
	#审批模板刷新
	echo "Number[6] Approval template refresh"
	echo ""
	#审批打包定时任务设置
	echo "Number[7] Approve packaging timing task Settings"
	echo ""
	#财务系统主干
	echo "Number[8] Financial system backbone    ==>truck"
	echo ""
	#财务系统跑批
	echo "Number[9] The financial system runs    ==>truck"
	echo ""
	#更新大数据API
	echo "Number[10] Update the big data API"
	echo ""
	echo "=============================================="
#	read -p  "请输入待打包命令Number(退出请按q):" version
	case $1 in
		"1")
			echo "===================Will soon deploy the main mortgage approval trunk================="
		 	sh ./truck.sh
			;;
		"2")
			echo "===================The mortgage approval branch will be deployed soon v3.8.0==========="
		  	sh ./3.8.sh
			;;
		"3")
			echo "==================The main package of mortgage big data will be deployed soon============="
			sh ./paltform.sh
			;;
		"4")
			sh ./houseLoanLog.sh
			;;
		"5")
			sh ./eam_shell/eamLog.sh
			;;
		"6")
			sh ./template.sh
			;;
		"7")
			#sh ./crontab/house_cron.sh
			;;
		"8")
			sh ./eam_shell/eam-trunk.sh
			;;
		"9")
			sh ./eam_shell/eam-batch.sh
			;;
		"10")
			sh ./update_paltform_api.sh
			;;
		"q" | "Q")
			echo "=========================Quite success！==================="
			;;
		*)
			echo "=================There is no such branch!=================="
		   	echo "please enter correct num:";
			exit -1
			;;
	esac
}


function main(){
	if [ -z $1 ];then
		echo "Args: Pleas input an args"
		exit -1
	fi

	def_service_path
	def_service_process
	def_email
	select_run $1
	generate_log
	generate_mail
}

main $1
