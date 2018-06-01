import wx


class MainWindow(wx.Frame):
	"""We simply derive a new class of Frame."""
	
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(400, 400))
		self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
		self.CreateStatusBar()  # 创建位于窗口的底部的状态栏
		
		# 设置菜单
		filemenu = wx.Menu()
		menuItem = filemenu.Append(wx.ID_ABOUT, "&About", " Information about this program")

		self.Bind(wx.EVT_MENU, self.OnAbout, menuItem)
		
		# wx.ID_ABOUT和wx.ID_EXIT是wxWidgets提供的标准ID
		filemenu.Append(wx.ID_ABOUT, u"关于", u"关于程序的信息")
		filemenu.AppendSeparator()
		filemenu.Append(wx.ID_EXIT, u"退出", u"终止应用程序")
		
		# 创建菜单栏
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, u"文件")
		self.SetMenuBar(menuBar)
		self.Show(True)


app = wx.App(False)
frame = MainWindow(None, title=u"我的记事本")
app.MainLoop()
