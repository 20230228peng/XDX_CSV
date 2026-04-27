import os
import wx
from UI.IndexUI import IndexFrame
from UI.NewProjectDialog import NewProjectDialog


class IndexMenuEvent(IndexFrame):

    def index_tool_6010(self, event):
        """

        """

        event.Skip()

    def index_tool_6011(self, event):
        event.Skip()

    def index_tool_6012(self, event):
        event.Skip()

    def index_tool_6030(self, event):
        event.Skip()

    def index_tool_6031(self, event):
        event.Skip()

    def index_tool_6040(self, event):
        event.Skip()

    def index_tool_6041(self, event):
        event.Skip()

    def dropdown_6042(self, event):
        event.Skip()

    def index_button_1(self, event):
        """
        新建项目
        :param event:
        :return:
        """

        # 确定 Data 根目录（使用当前工作目录下的 Data 文件夹）
        data_root = os.path.join(os.getcwd(), "Data")
        if not os.path.exists(data_root):
            os.makedirs(data_root)

        dlg = NewProjectDialog(self, data_root)
        if dlg.ShowModal() == wx.ID_OK:
            # 获取对话框中的数据
            project_name = dlg.m_textCtrl1.GetValue().strip()
            project_type = dlg.m_comboBox1.GetValue()
            creator = dlg.m_textCtrl2.GetValue().strip()
            create_date = dlg.m_datePicker1.GetValue().FormatISODate()
            project_folder = dlg.m_dirPicker2.GetPath().strip()  # 用户选择的最终路径

            # 检查数据完整性
            if not project_name:
                wx.MessageBox("项目名称不能为空", "提示", wx.OK | wx.ICON_WARNING)
                dlg.Destroy()
                return
            if not project_folder:
                wx.MessageBox("项目文件夹不能为空", "提示", wx.OK | wx.ICON_WARNING)
                dlg.Destroy()
                return

            # 确保项目文件夹存在（如果用户选择的路径不存在则创建）
            if not os.path.exists(project_folder):
                try:
                    os.makedirs(project_folder)
                except Exception as e:
                    wx.MessageBox(f"创建项目文件夹失败：{str(e)}", "错误", wx.OK | wx.ICON_ERROR)
                    dlg.Destroy()
                    return

            # 构建项目信息字典
            project_info = {
                "name": project_name,
                "type": project_type,
                "creator": creator,
                "create_date": create_date,
                "folder": project_folder
            }

            # 保存 .xdxproj 文件
            proj_file = os.path.join(project_folder, f"{project_name}.xdxproj")

            self.m_statusBar1.SetStatusText(project_folder,0)

            try:
                import json
                with open(proj_file, 'w', encoding='utf-8') as f:
                    json.dump(project_info, f, ensure_ascii=False, indent=4)
            except Exception as e:
                wx.MessageBox(f"保存项目文件失败：{str(e)}", "错误", wx.OK | wx.ICON_ERROR)
                dlg.Destroy()
                return

            # 刷新右侧文件树，显示项目文件夹内容
            if hasattr(self, 'm_panel1') and hasattr(self.m_panel1, 'load_project'):
                success = self.m_panel1.load_project(project_folder)
                if not success:
                    wx.MessageBox("加载项目文件树失败，请检查目录权限", "警告", wx.OK | wx.ICON_WARNING)
            else:
                wx.LogError("未找到文件树控件或 load_project 方法")

        dlg.Destroy()
        event.Skip()

    def index_button_2(self, event):
        """
        打开项目
        :param event:
        """
        # 创建文件选择对话框，只允许选择 .xdxproj 文件
        with wx.FileDialog(self, "打开项目文件", wildcard="项目文件 (*.xdxproj)|*.xdxproj",
                          style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # 用户取消了操作
            
            # 获取选择的文件路径
            proj_file_path = fileDialog.GetPath()
            
            try:
                # 读取 .xdxproj 文件
                import json
                with open(proj_file_path, 'r', encoding='utf-8') as f:
                    project_info = json.load(f)
                
                # 检查是否包含 "folder" 字段
                if "folder" not in project_info:
                    wx.MessageBox("项目文件中缺少 'folder' 字段", "错误", wx.OK | wx.ICON_ERROR)
                    return
                
                project_folder = project_info["folder"]
                
                # 检查项目文件夹是否存在
                if not os.path.exists(project_folder):
                    wx.MessageBox(f"项目文件夹不存在：{project_folder}\n\n请检查项目配置或重新创建项目。", 
                                 "警告", wx.OK | wx.ICON_WARNING)
                    return
                
                # 更新状态栏第一栏显示项目路径
                self.m_statusBar1.SetStatusText(project_folder, 0)
                
                # 刷新右侧文件树，显示项目文件夹内容
                if hasattr(self, 'm_panel1') and hasattr(self.m_panel1, 'load_project'):
                    success = self.m_panel1.load_project(project_folder)
                    if not success:
                        wx.MessageBox("加载项目文件树失败，请检查目录权限", "警告", wx.OK | wx.ICON_WARNING)
                    else:
                        # 在状态栏显示项目名称
                        project_name = project_info.get("name", "未命名项目")
                        self.m_statusBar1.SetStatusText(f"已打开项目：{project_name}", 1)
                else:
                    wx.LogError("未找到文件树控件或 LoadProject 方法")
                    
            except json.JSONDecodeError as e:
                wx.MessageBox(f"项目文件格式错误：{str(e)}", "错误", wx.OK | wx.ICON_ERROR)
            except Exception as e:
                wx.MessageBox(f"打开项目失败：{str(e)}", "错误", wx.OK | wx.ICON_ERROR)
        
        event.Skip()

    def index_button_3(self, event):
        """
        保存项目
        :event:
        """
        print("保存项目")
        event.Skip()

    def index_button_4(self, event):
        """
        项目设置
        :event:
        """
        print("项目设置")
        event.Skip()

    def index_button_5(self, event):
        event.Skip()

    def index_button_6(self, event):
        event.Skip()

    def index_button_7(self, event):
        event.Skip()