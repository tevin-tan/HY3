from selenium.webdriver.common.action_chains import ActionChains

import config
import os
import time
import yaml
from com import ssh
from com.login import Login
from com.pobj.TaskCenter import PendingTask

rdir = config.__path__[0]
pth = os.path.join(rdir, 'hostinfo')
with open(pth, 'r', encoding='utf-8') as f:
	temp = yaml.load(f)
	host_ip = temp['SIT']['IP']
	port = temp['SIT']['port']
	host_name = temp['SIT']['username']
	host_password = temp['SIT']['password']

page = Login('xn018170')
task_search = PendingTask.PendingTask.task_search(page, 'GZ20180314X01')
ActionChains(page.driver).double_click(task_search).perform()

page.driver.switch_to_frame("myIframeImage1")
page.driver.find_element_by_link_text("合同签约").click()
time.sleep(1)
page.driver.find_element_by_xpath('//*[@id="apply_electronSign_info"]/div[3]/div/table/tbody/tr[2]/td[5]/a[1]').click()
time.sleep(2)
page.driver.find_element_by_xpath('//*[@id="electronSignDetails"]/div/div/div[3]/div[1]/p[1]/input').click()

page.driver.find_element_by_xpath('//*[@id="sentCodeMessage"]').click()

execmd = ' cd /web/apache-tomcat-7.0.69/logs; tail -10 catalina.out  > 1.txt ; ' \
         'cat 1.txt | grep "短信" | awk -F"验证码：" \'{print $2}\' ' \
         '| awk -F\'，\' \'{print $1}\' | tail -1'

# 获取短信验证码
res = ssh.sshclient_execmd(host_ip, port, host_name, host_password, execmd)
# 输入验证码
page.driver.find_element_by_xpath('//*[@id="checkcodeInput"]').send_keys(res)
# 确认
page.driver.find_element_by_xpath(
		'//*[@id="electronSignDetails"]/div/div/div[3]/div[1]/p[4]/button[1]').click()
# 关闭浏览器
page.driver.close()
