# coding:utf-8

# 客户信息-业务基本信息

# 元素定位
loc_cust_info = dict(
	je_id="apply_module_apply_amount",  # 金额
	dkts_id="apply_module_apply_period",  # 贷款天数
	fgsjlxm_id="apply_module_branch_manager_name",  # 分公司经理姓名
	fgsjlgh_id="apply_module_branch_manager",  # 分公司经理工号
	tdzb_id="apply_module_team_group_name",  # 团队组别
	tdjlxm_id="apply_module_team_manager_name",  # 团队经理姓名
	tdjlgh_id="apply_module_team_manager",  # 团队经理工号
	khjlxm_id="apply_module_sale_name",  # 客户经理姓名
	khjlgh_id="apply_module_sale",  # 客户经理工号
	lsyjsr_id="apply_module_month_income",  # 流水月均收入
	zyyjbz_name="checkApprove",  # 专员意见备注
	)

# 客户基本信息 - 借款人/共贷人/担保人信息
loc_borrower = dict(
	jkrxm='//*[@id="datagrid-row-r1-2-0"]/td[5]/div/table/tbody/tr/td/input',  # 借款人姓名
	sfzhm='//*[@id="datagrid-row-r1-2-0"]/td[6]/div/table/tbody/tr/td/input',  # 身份证号码
	sjycd=dict(
		locate="_easyui_textbox_input3",
		value="_easyui_combobox_i2_1",
		),  # 受教育程度
	hyzk=dict(
		locate="_easyui_textbox_input4",
		value="_easyui_combobox_i3_0",
		),  # 婚姻状况
	jtdzxx="_easyui_textbox_input5",  # 家庭地址信息
	xxfs='//*[@id="datagrid-row-r1-2-0"]/td[11]/div/table/tbody/tr/td/input',  # 联系方式
	dwmc='//*[@id="datagrid-row-r1-2-0"]/td[12]/div/table/tbody/tr/td/input',  # 单位名称
	gsgm=dict(
		# a="div.datagrid-view2 > div.datagrid-body",
		a="//*[@id=\"_easyui_textbox_input6\"]",
		b=".//*[@id='datagrid-row-r1-2-0']/td[12]/div/table/tbody/tr/td/span/span/a",  # 下拉列表
		c="//*[@id=\"_easyui_combobox_i4_3\"]",  # 元素选择
		locate="_easyui_textbox_input6",
		value="_easyui_combobox_i4_3",
		),  # 公司规模
	sshy=dict(
		locate="_easyui_textbox_input7",
		value="_easyui_combobox_i5_8",
		),  # 所属行业
	zw="_easyui_textbox_input9",  # 职位
	rzrq='//*[@id="datagrid-row-r1-2-0"]/td[17]/div/table/tbody/tr/td/input',  # 入职日期
	gzyx="_easyui_textbox_input10",  # 工作年限
	yjsr="_easyui_textbox_input11",  # 月均收入
	sfysb="input[type=\"checkbox\"]",  # 是否有社保
	)

# 物业信息
loc_property = {
	'name_cqr':     'propertyOwner',  # 产权人
	'name_fczh':    'propertyNo',  # 房产证号
	"name_sfsdwy":  "propertyStatus",  # 是否涉贷物业
	"name_fl":      "propertyAge",  # 房龄
	"name_jzmj":    "propertyArea",  # 建筑面积
	"name_djj":     "registrationPrice",  # 等级价
	"name_address": {
		"provice":  "propertyAddressProvince",
		"city":     "propertyAddressCity",
		"distinct": "propertyAddressDistinct",
		"detail":   "propertyAddressDetail"
		},  # 地址
	"name_pggxjzz": "evaluationSumAmount",  # 评估公允价总值
	"name_pggxjjz": "evaluationNetAmount",  # 评估公允价净值
	"name_slpgzz":  "slSumAmount",  # 世联评估总值
	"name_slpgjz":  "slPrice",  # 世联评估净值
	"name_zjpgzz":  "agentSumAmout",  # 中介评估总值
	"name_zjpgjz":  "agentNetAmount",  # 中介评估净值
	"name_wpzz":    "netSumAmount",  # 网评总值
	"name_wpjz":    "netAmount",  # 网评净值
	"name_ddpgzz":  "localSumAmount",  # 当地评估总值
	"name_ddpgjz":  "localNetValue",  # 当地评估净值
	"name_wyptms":  "remark",  # 物业配套描述
	"name_ddpgly":  "localAssessmentOrigin",  # 当地评估来源
	"name_pgly":    "assessmentOrigin",  # 评估来源
	"name_pgqkms":  "evaluationCaseDescrip",  # 评估情况描述

	}
