import wx
import os
import wx.xrc
import wx.dataview
import gettext
_ = gettext.gettext


class IndexPanel(wx.Panel):
    def __init__(self, parent, bg_image_path=None, *args, **kw):
        super(IndexPanel, self).__init__(parent, *args, **kw)

        # 加载背景图片（如果提供路径且文件存在）
        self.background_bmp = None
        if bg_image_path:
            try:
                self.background_bmp = wx.Bitmap(bg_image_path)
            except:
                pass

        # 绑定绘制事件
        if self.background_bmp and self.background_bmp.IsOk():
            self.Bind(wx.EVT_PAINT, self.on_paint)
            self.Bind(wx.EVT_SIZE, self.on_size)

        # 主水平布局
        bSizer4 = wx.BoxSizer(wx.HORIZONTAL)

        # ==================== 左侧：文件树 ====================
        # 使用 DataViewTreeCtrl 替代自定义模型
        self.m_dataViewTreeCtrl = wx.dataview.DataViewTreeCtrl(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
            wx.dataview.DV_NO_HEADER
        )
        self.m_dataViewTreeCtrl.SetMinSize(wx.Size(150, -1))
        self.m_dataViewTreeCtrl.SetMaxSize(wx.Size(180, -1))

        # 设置图像列表（16x16图标）
        self.image_list = wx.ImageList(16, 16)
        # 系统标准图标
        folder_bmp = wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16, 16))
        file_bmp = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16, 16))
        home_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_HOME, wx.ART_OTHER, (16, 16))
        # 可根据需要添加更多自定义图标
        self.folder_icon = self.image_list.Add(folder_bmp)
        self.file_icon = self.image_list.Add(file_bmp)
        self.home_icon = self.image_list.Add(home_bmp)

        self.m_dataViewTreeCtrl.SetImageList(self.image_list)

        bSizer4.Add(self.m_dataViewTreeCtrl, 1, wx.EXPAND, 5)

        # ==================== 右侧区域：原有控件 ====================
        bSizer5 = wx.BoxSizer(wx.VERTICAL)
        bSizer6 = wx.BoxSizer(wx.VERTICAL)

        # 加载数据行
        bSizer7 = wx.BoxSizer(wx.HORIZONTAL)
        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, _(u"加载数据："), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        bSizer7.Add(self.m_staticText2, 0, wx.ALL, 5)

        self.m_dirPicker1 = wx.DirPickerCtrl(
            self, wx.ID_ANY, wx.EmptyString, _(u"Select a folder"),
            wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL
        )
        bSizer7.Add(self.m_dirPicker1, 1, wx.ALL, 5)
        bSizer6.Add(bSizer7, 0, wx.EXPAND, 5)

        # 分割线
        bSizer8 = wx.BoxSizer(wx.HORIZONTAL)
        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, _(u"分割线 >> "), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer8.Add(self.m_staticText1, 0, wx.ALL, 5)
        self.m_staticline1 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer8.Add(self.m_staticline1, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        bSizer6.Add(bSizer8, 0, wx.EXPAND, 5)

        # 图例区域（保留原有）
        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _(u"图例")), wx.VERTICAL)
        gSizer1 = wx.GridSizer(0, 2, 0, 0)
        self.m_panel4 = wx.Panel(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        gSizer1.Add(self.m_panel4, 1, wx.EXPAND | wx.ALL, 5)
        self.m_panel5 = wx.Panel(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        gSizer1.Add(self.m_panel5, 1, wx.EXPAND | wx.ALL, 5)
        sbSizer1.Add(gSizer1, 1, wx.EXPAND, 5)
        bSizer6.Add(sbSizer1, 1, wx.EXPAND, 5)

        bSizer5.Add(bSizer6, 1, wx.EXPAND, 5)

        # 计算按钮
        bSizer9 = wx.BoxSizer(wx.VERTICAL)
        self.m_button1 = wx.Button(self, wx.ID_ANY, _(u"计算"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer9.Add(self.m_button1, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        bSizer5.Add(bSizer9, 1, wx.EXPAND, 5)

        bSizer4.Add(bSizer5, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer4)
        self.Layout()

        # 保存项目根目录
        self.project_root = None

        # 绑定事件
        self.m_dirPicker1.Bind(wx.EVT_DIRPICKER_CHANGED, self.on_dir_changed)
        self.m_button1.Bind(wx.EVT_BUTTON, self.on_calc)

    # ==================== 文件树填充逻辑 ====================
    def load_project(self, project_folder_path):
        """
        加载项目文件夹，刷新文件树
        :param project_folder_path: 项目文件夹路径
        """
        if not os.path.isdir(project_folder_path):
            wx.MessageBox(f"项目文件夹不存在：{project_folder_path}", "错误", wx.OK | wx.ICON_ERROR)
            return False

        self.project_root = project_folder_path
        self.m_dataViewTreeCtrl.DeleteAllItems()

        # 创建根节点（项目空间）
        root_item = self.m_dataViewTreeCtrl.AppendContainer(
            wx.dataview.NullDataViewItem,
            os.path.basename(project_folder_path),
            icon=self.folder_icon
        )
        self.m_dataViewTreeCtrl.SetItemData(root_item, project_folder_path)

        # 递归填充子节点
        self._populate_tree(root_item, project_folder_path)

        # 展开根节点
        self.m_dataViewTreeCtrl.Expand(root_item)

        return True

    def _populate_tree(self, parent_item, parent_path):
        """
        递归填充目录树
        :param parent_item: 父节点项
        :param parent_path: 父节点路径
        """
        try:
            entries = sorted(os.listdir(parent_path))
        except (PermissionError, OSError):
            return

        # 先添加子文件夹
        dirs = [e for e in entries if os.path.isdir(os.path.join(parent_path, e))]
        for d in dirs:
            dir_path = os.path.join(parent_path, d)
            container_item = self.m_dataViewTreeCtrl.AppendContainer(
                parent_item, d, icon=self.folder_icon
            )
            self.m_dataViewTreeCtrl.SetItemData(container_item, dir_path)
            self._populate_tree(container_item, dir_path)

        # 再添加文件
        files = [e for e in entries if os.path.isfile(os.path.join(parent_path, e))]
        for f in files:
            file_path = os.path.join(parent_path, f)
            item = self.m_dataViewTreeCtrl.AppendItem(parent_item, f, icon=self.file_icon)
            self.m_dataViewTreeCtrl.SetItemData(item, file_path)

    # ==================== 事件处理 ====================
    def on_dir_changed(self, event):
        """用户选择文件夹后自动加载"""
        folder_path = self.m_dirPicker1.GetPath()
        if folder_path and os.path.isdir(folder_path):
            self.load_project(folder_path)
            # 可选：将路径保存到状态栏
            parent = self.GetParent()
            while parent and not hasattr(parent, 'm_statusBar1'):
                parent = parent.GetParent()
            if parent and hasattr(parent, 'm_statusBar1'):
                parent.m_statusBar1.SetStatusText(folder_path, 0)
        event.Skip()

    def on_calc(self, event):
        """计算按钮点击事件（根据实际需求实现）"""
        wx.MessageBox("计算功能待实现", "提示", wx.OK | wx.ICON_INFORMATION)
        event.Skip()

    # ==================== 背景绘制（保留） ====================
    def on_size(self, event):
        event.Skip()
        self.Refresh()

    def on_paint(self, event):
        if not self.background_bmp or not self.background_bmp.IsOk():
            event.Skip()
            return

        w, h = self.GetClientSize()
        if w == 0 or h == 0:
            return

        bmp = wx.Bitmap(w, h)
        mem_dc = wx.MemoryDC(bmp)
        img = self.background_bmp.ConvertToImage()
        img = img.Scale(w, h, wx.IMAGE_QUALITY_HIGH)
        scaled_bmp = wx.Bitmap(img)
        mem_dc.DrawBitmap(scaled_bmp, 0, 0)

        paint_dc = wx.PaintDC(self)
        paint_dc.Blit(0, 0, w, h, mem_dc, 0, 0)
        self.Layout()
        event.Skip()

    def __del__(self):
        pass