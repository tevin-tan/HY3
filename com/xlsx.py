# coding:utf-8

import os

import xlsxwriter

import report

r_dir = report.__path__[0]
l_p = os.path.join(r_dir, 'report.xlsx')


class XLS(object):
	"""测试报表"""

	def __init__(self):
		# 大写字母
		self.ch_i = [chr(i) for i in range(65, 91)]

		# now = time.strftime("%Y-%m-%d %H_%M_%S")
		# l_p = os.path.join(r_dir, now + '.xlsx')
		# l_p = os.path.join(r_dir, file_name + '_report.xlsx')
		print(l_p)
		self.workbook = xlsxwriter.Workbook(l_p)
		self.worksheet = self.workbook.add_worksheet("测试总况")
		# self.test_03(data)

		self.ItemStyle = self.workbook.add_format({
			'font_size': 10,  # 字体大小
			'bold': 1,  # 是否粗体
			'bg_color': '#101010',  # 表格背景颜色
			'font_color': '#FEFEFE',  # 字体颜色
			'align': 'center',  # 对齐方式，left,center,rigth,top,vcenter,bottom,vjustify
			'top': 2,  # 上边框，后面参数是线条宽度
			'left': 2,  # 左边框
			'right': 2,  # 右边框
			'bottom': 2,  # 底边框
			'text_wrap': 1,  # 自动换行，可在文本中加 '\n'来控制换行的位置
			'num_format': 'yyyy-mm-dd'  # 设定格式为日期格式，如：2017-07-01
			})

	# self.end()

	def end(self):
		self.workbook.close()

	# 设置模式
	@staticmethod
	def get_format(wd, option=None):
		return wd.add_format(option)

	# 设置居中
	@staticmethod
	def set_format_center(wd, num=1):
		return wd.add_format({
			'align': 'center',
			'valign': 'vcenter',
			'border': num,
			# 'font_color': '#5833ff',
			'font_color': '#0026cc',
			'bold': 1,
			})

	@staticmethod
	def set_format_left(wd, num=1):
		return wd.add_format({
			'align': 'left',
			'valign': 'vcenter',
			'font_color': '#0026cc',
			'border': num,
			'bold': 1,
			})

	@staticmethod
	def set_font_color(wd, color, num=1, ):
		return wd.add_format({
			'align': 'center',
			'valign': 'vcenter',
			# 'font_color': '#f70c0c',  # 字体色
			'font_color': color,  # 字体色
			'border': num,
			'bold': 1,  # 加粗
			})

	# 写数据
	def _write_center(self, worksheet, cl, data, wd):
		return worksheet.write(cl, data, self.set_format_center(wd))

	def _write_left(self, worksheet, cl, data, wd):
		return worksheet.write(cl, data, self.set_format_left(wd))

	def _write_font(self, worksheet, cl, data, wd, color):
		return worksheet.write(cl, data, self.set_font_color(wd, color))

	@staticmethod
	def set_border_(wd, num=1):
		return wd.add_format(dict()).set_border(num)

	# 生成饼形图
	@staticmethod
	def pie(workbook, worksheet):
		chart1 = workbook.add_chart({'type': 'pie'})
		chart1.add_series({
			'name': '接口测试统计',
			'categories': '=测试总况!$D$4:$D$5',
			'values': '=测试总况!$E$4:$E$5',
			})
		chart1.set_title({'name': '接口测试统计'})
		chart1.set_style(10)
		worksheet.insert_chart('A9', chart1, {'x_offset': 25, 'y_offset': 10})

	def test_02(self, worksheet):
		# 设置列行的宽高
		worksheet.set_column("A:A", 30)
		worksheet.set_column("B:B", 20)
		worksheet.set_column("C:C", 20)
		worksheet.set_column("D:D", 20)
		worksheet.set_column("E:E", 20)
		worksheet.set_column("F:F", 20)
		worksheet.set_column("G:G", 20)
		worksheet.set_column("H:H", 20)

		worksheet.set_row(1, 30)
		worksheet.set_row(2, 30)
		worksheet.set_row(3, 30)
		worksheet.set_row(4, 30)
		worksheet.set_row(5, 30)
		worksheet.set_row(6, 30)
		worksheet.set_row(7, 30)

		worksheet.merge_range('A1:H1', '测试详情', self.get_format(self.workbook, {
			'bold': True, 'font_size': 18, 'align': 'center',
			'valign': 'vcenter', 'bg_color': 'blue',
			'font_color': '#ffffff'
			}))

		self._write_center(worksheet, "A2", '用例ID', self.workbook)
		self._write_center(worksheet, "B2", '接口名称', self.workbook)
		self._write_center(worksheet, "C2", '接口协议', self.workbook)
		self._write_center(worksheet, "D2", 'URL', self.workbook)
		self._write_center(worksheet, "E2", '参数', self.workbook)
		self._write_center(worksheet, "F2", '预期值', self.workbook)
		self._write_center(worksheet, "G2", '实际值', self.workbook)
		self._write_center(worksheet, "H2", '测试结果', self.workbook)

		data = {
			"info": [
				{
					"t_id": "1001", "t_name": "登陆", "t_method": "post", "t_url": "http://XXX?login",
					"t_param": "{user_name:test,pwd:111111}",
					"t_hope": "{code:1,msg:登陆成功}",
					"t_actual": "{code:0,msg:密码错误}",
					"t_result": "失败"
					},
				{
					"t_id": "1002", "t_name": "商品列表", "t_method": "get", "t_url": "http://XXX?getFoodList",
					"t_param": "{}",
					"t_hope": "{code:1,msg:成功,info:[{name:123,detal:dfadfa,img:product/1.png},{name:456,detal:dfadfa,img:product/1.png}]}",
					"t_actual": "{code:1,msg:成功,info:[{name:123,detal:dfadfa,img:product/1.png},{name:456,detal:dfadfa,img:product/1.png}]}",
					"t_result": "成功"
					}],
			"test_sum": 100, "test_success": 20, "test_failed": 80
			}
		temp = 3
		for item in data["info"][:]:
			self._write_center(worksheet, "A" + str(temp), item["t_id"], self.workbook)
			self._write_center(worksheet, "B" + str(temp), item["t_name"], self.workbook)
			self._write_center(worksheet, "C" + str(temp), item["t_method"], self.workbook)
			self._write_center(worksheet, "D" + str(temp), item["t_url"], self.workbook)
			self._write_center(worksheet, "E" + str(temp), item["t_param"], self.workbook)
			self._write_center(worksheet, "F" + str(temp), item["t_hope"], self.workbook)
			self._write_center(worksheet, "G" + str(temp), item["t_actual"], self.workbook)
			self._write_center(worksheet, "H" + str(temp), item["t_result"], self.workbook)
			temp = temp + 1

	def test_01(self, worksheet):
		# 设置行高宽
		self.worksheet.set_column("A:A", 15)
		self.worksheet.set_column("B:B", 20)
		self.worksheet.set_column("C:C", 20)
		self.worksheet.set_column("D:D", 20)
		self.worksheet.set_column("E:E", 20)
		self.worksheet.set_column("F:F", 20)

		# 设置行高
		self.worksheet.set_row(1, 30)
		self.worksheet.set_row(2, 30)
		self.worksheet.set_row(3, 30)
		self.worksheet.set_row(4, 30)
		self.worksheet.set_row(5, 30)

		# 加粗处理
		define_format_h1 = self.get_format(self.workbook, dict(bold=True, font_size=18))
		define_format_h2 = self.get_format(self.workbook, dict(bold=True, font_size=14))
		# 加粗
		define_format_h1.set_border(1)
		define_format_h2.set_border(1)
		# 设置居中
		define_format_h1.set_align("center")
		define_format_h1.set_align("center")
		define_format_h2.set_align("center")
		define_format_h2.set_bg_color("blue")
		define_format_h2.set_color("#ffffff")
		# 合并单元格
		worksheet.merge_range('A1:F1', '测试报告总概况', define_format_h1)
		worksheet.merge_range('A2:F2', '测试概括', define_format_h2)
		worksheet.merge_range('A3:A6', '这里放图片', self.set_format_center(self.workbook))
		# 设置文字居中
		self._write_center(worksheet, "B3", '项目名称', self.workbook)
		self._write_center(worksheet, "B4", '接口版本', self.workbook)
		self._write_center(worksheet, "B5", '脚本语言', self.workbook)
		self._write_center(worksheet, "B6", '测试网络', self.workbook)

		data = {"test_name": "智商", "test_version": "v2.0.8", "test_pl": "android", "test_net": "wifi"}
		self._write_center(worksheet, "C3", data['test_name'], self.workbook)
		self._write_center(worksheet, "C4", data['test_version'], self.workbook)
		self._write_center(worksheet, "C5", data['test_pl'], self.workbook)
		self._write_center(worksheet, "C6", data['test_net'], self.workbook)

		self._write_center(worksheet, "D3", "接口总数", self.workbook)
		self._write_center(worksheet, "D4", "通过总数", self.workbook)
		self._write_center(worksheet, "D5", "失败总数", self.workbook)
		self._write_center(worksheet, "D6", "测试日期", self.workbook)

		data1 = {"test_sum": 100, "test_success": 80, "test_failed": 20, "test_date": "2018-10-10 12:10"}
		self._write_center(worksheet, "E3", data1['test_sum'], self.workbook)
		self._write_center(worksheet, "E4", data1['test_success'], self.workbook)
		self._write_center(worksheet, "E5", data1['test_failed'], self.workbook)
		self._write_center(worksheet, "E6", data1['test_date'], self.workbook)

		self._write_center(worksheet, "F3", "分数", self.workbook)
		worksheet.merge_range('F4:F6', '60', self.set_format_center(self.workbook))

		self.pie(self.workbook, worksheet)

	# 设置列宽
	def _set_sheet_column(self):

		for i in self.ch_i:
			if i == 'A':
				self.worksheet.set_column(i + ':' + i, 4)
			elif i == 'B':
				self.worksheet.set_column(i + ':' + i, 60)
			elif i == 'C' or i == 'G' or i == 'F':
				self.worksheet.set_column(i + ':' + i, 30)
			else:
				self.worksheet.set_column(i + ':' + i, 15)

	# 设置列宽
	def _set_sheet_row(self):
		self.worksheet.set_row(1, 25)
		for i in range(2, 1000):
			self.worksheet.set_row(i, 20)

	def test_03(self, data):
		# 设置列宽
		self._set_sheet_column()

		# 设置行高
		self._set_sheet_row()

		# 加粗处理
		define_format_h1 = self.get_format(self.workbook, dict(bold=True, font_size=18))
		define_format_h2 = self.get_format(self.workbook, dict(bold=True, font_size=14))

		# 加粗
		define_format_h1.set_border(1)
		define_format_h2.set_border(1)

		# 设置居中
		define_format_h1.set_align("center")
		define_format_h2.set_align("center")
		define_format_h2.set_bg_color("green")
		define_format_h2.set_color("#fafafa")

		# 合并单元格
		self.worksheet.merge_range('A1:G1', '测试报告总概况', define_format_h1)
		self.worksheet.merge_range('A2:G2', '测试概括', define_format_h2)

		self._write_center(self.worksheet, "A3", '序号', self.workbook)
		self._write_center(self.worksheet, "B3", '用例编号', self.workbook)
		self._write_center(self.worksheet, "C3", '申请件单号', self.workbook)
		self._write_center(self.worksheet, "D3", '执行结果', self.workbook)
		self._write_center(self.worksheet, "E3", '执行时长', self.workbook)
		self._write_center(self.worksheet, "F3", '开始时间', self.workbook)
		self._write_center(self.worksheet, "G3", '结束时间', self.workbook)

		n = 4
		for i in range(1, len(data) + 1):
			self._write_center(self.worksheet, "A" + str(n), i, self.workbook)
			n = n + 1
		count = 4
		for i in data:
			self._write_left(self.worksheet, "B" + str(count), i["name"], self.workbook)
			self._write_center(self.worksheet, "C" + str(count), i["apply_code"], self.workbook)
			if i['result'] is True:
				self._write_font(self.worksheet, "D" + str(count), i['result'], self.workbook, '#27b621')
			else:
				self._write_font(self.worksheet, "D" + str(count), i['result'], self.workbook, '#f70c0c')
			self._write_center(self.worksheet, "E" + str(count), i['u_time'], self.workbook)
			self._write_center(self.worksheet, "F" + str(count), i['s_time'], self.workbook)
			self._write_center(self.worksheet, "G" + str(count), i['e_time'], self.workbook)
			count = count + 1


if __name__ == '__main__':
	data2 = [
		dict(
			name="test_eyt_09_branch_manager_approval",
			apply_code="GZ20180330C14",
			result=False,
			u_time="1min30s",
			s_time='2018-03-24 20:13:24',
			e_time='2018-03-25 20:13:24',
			),
		dict(
			name="test_eyt_10_branch_manager_approval",
			apply_code="GZ20180330C15",
			result=True,
			u_time="2min30s",
			s_time='2018-03-24 20:13:24',
			e_time='2018-03-25 20:13:24',
			),
		]
	a = XLS()
	a.test_03(data2)
	a.end()
