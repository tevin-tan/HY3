import os

import paramiko
import yaml

import config


def sshclient_execmd(hostname, port, username, password, execmd):
	paramiko.util.log_to_file("paramiko.log")
	
	s = paramiko.SSHClient()
	s.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 跳过了远程连接中选择‘是’的环节,
	
	s.connect(hostname=hostname, port=port, username=username, password=password)
	stdin, stdout, stderr = s.exec_command(execmd)
	# stdin.write("Y")  # Generally speaking, the first c?onnection, need a simple interaction.
	ot = stdout.read()
	print('--------', ot)
	print(str(ot, encoding='utf-8'))
	
	# print()
	# s1 = str(ot, encoding='utf-8').split('\n')
	# print(s1)
	s.close()
	return str(ot, encoding='utf-8')


def main():
	rdir = config.__path__[0]
	pth = os.path.join(rdir, 'hostinfo')
	with open(pth, 'r', encoding='utf-8') as f:
		temp = yaml.load(f)
		host_ip = temp['SIT']['IP']
		port = temp['SIT']['port']
		host_name = temp['SIT']['username']
		host_password = temp['SIT']['password']
	
	execmd = \
		' cd /web/apache-tomcat-7.0.69/logs; tail -10 catalina.out  > 1.txt ; ' \
		'cat 1.txt | grep "短信" | awk -F"验证码：" \'{print $2}\' ' \
		'| awk -F\'，\' \'{print $1}\' | tail -1'
	
	# execmd = 'cd /web/apache-tomcat-7.0.69/logs; tail -10 catalina.out  > 1.txt ; cat 1.txt '
	print(execmd)
	sshclient_execmd(host_ip, port, host_name, host_password, execmd)

# if __name__ == "__main__":
# 	main()
