import tkinter as tk
from tkinter import simpledialog, messagebox
from models.item import Item
from models.user import User
from models.item_type import ItemType
from models.category import Category
from utils.validator import Validator
import json
import os

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("物品管理系统")
        self.root.geometry("1000x1000")  # 调整窗口尺寸，使其更大
        self.root.config(bg="#f0f0f0")  # 设置背景颜色

        # 存储用户信息以及其他辅助数据
        self.user = None
        self.categories = []  # 存储所有类别
        self.users_db = []  # 模拟数据库来保存用户信息，待管理员审核
        self.items = []
        
        self.file_path = './items.json'

        # 读取 JSON 文件并解析为 Python 对象
        with open(self.file_path, 'r', encoding='utf-8') as file:
            items_data = json.load(file)

        # 循环遍历 JSON 中的每个条目，创建对应的 Item 实例
        for item_data in items_data:

            # 创建物品类型对象
            item_type_name = item_data["item_type"]["type_name"]
            item_attributes = item_data["item_type"]["attributes"]

            # 创建物品类型和物品对象
            item_type = ItemType(item_type_name, item_attributes)

            # 创建 Item 实例
            item = Item(
                name=item_data['name'],
                description=item_data['description'],
                address=item_data['address'],
                contact=item_data['contact'],
                email=item_data['email'],
                item_type=item_type  # 直接传递字典
            )
            self.items.append(item)

        # 初始化管理员账号（admin，123456）
        self.admin_username = "admin"
        self.admin_password = "123456"

        # 登录状态
        self.logged_in = False
        self.user_type = None  # None, '普通用户', '管理员'
        
        self.item_types = [
            ItemType("食品", {"保质期": "2024-12-31", "数量": "100"}),
            ItemType("书籍", {"作者": "未知", "出版社": "未知"}),
            ItemType("工具", {"材质": "钢", "重量": "1.5kg"})
        ]

        self.create_widgets()

    def create_widgets(self):
        # 登录界面
        if not self.logged_in:
            self.show_login()
        else:
            self.show_main_menu()

    def show_main_menu(self):
        # 主菜单界面
        self.clear_window()
        
        self.root.title(f"欢迎，{self.user_type}")
        
        # 设置grid布局的行列数量
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # 主菜单中的按钮
        row = 0  # 初始化行号

        if self.user_type == "管理员":
            # 管理员用户菜单
            self.approve_admin_button = tk.Button(self.root, text="审核用户注册", command=self.show_admin_screen)
            self.approve_admin_button.grid(row=row, column=0, pady=5, sticky="ew")
            row += 1

            self.set_new_item_type_button = tk.Button(self.root, text="设置新的物品类型", command=self.set_new_item_type)
            self.set_new_item_type_button.grid(row=row, column=0, pady=5, sticky="ew")
            row += 1

            self.edit_item_type_button = tk.Button(self.root, text="修改物品类型", command=self.edit_item_type)
            self.edit_item_type_button.grid(row=row, column=0, pady=5, sticky="ew")
            row += 1

            self.add_item_button = tk.Button(self.root, text="添加物品", command=self.show_item_management_screen)
            self.add_item_button.grid(row=row, column=0, pady=5, sticky="ew")
            row += 1

            self.search_item_button = tk.Button(self.root, text="搜寻物品", command=self.search_item)
            self.search_item_button.grid(row=row, column=0, pady=5, sticky="ew")
            row += 1

            self.delete_item_button = tk.Button(self.root, text="删除物品", command=self.delete_item)
            self.delete_item_button.grid(row=row, column=0, pady=5, sticky="ew")
            row += 1

            self.view_item_list_button = tk.Button(self.root, text="显示物品列表", command=self.view_item_list)
            self.view_item_list_button.grid(row=row, column=0, pady=5, sticky="ew")
            row += 1

            self.logout_button = tk.Button(self.root, text="退出登录", command=self.show_login_screen)
            self.logout_button.grid(row=row, column=0, pady=5, sticky="ew")
        
        elif self.user_type == "普通用户":
            # 普通用户菜单
            self.add_item_button = tk.Button(self.root, text="添加物品", command=self.show_item_management_screen)
            self.add_item_button.grid(row=row, column=0, pady=10, sticky="ew")
            row += 1

            self.search_item_button = tk.Button(self.root, text="搜寻物品", command=self.search_item)
            self.search_item_button.grid(row=row, column=0, pady=10, sticky="ew")
            row += 1

            self.delete_item_button = tk.Button(self.root, text="删除物品", command=self.delete_item)
            self.delete_item_button.grid(row=row, column=0, pady=10, sticky="ew")
            row += 1

            self.view_item_list_button = tk.Button(self.root, text="显示物品列表", command=self.view_item_list)
            self.view_item_list_button.grid(row=row, column=0, pady=10, sticky="ew")

            self.logout_button = tk.Button(self.root, text="退出登录", command=self.show_login_screen)
            self.logout_button.grid(row=row, column=0, pady=10, sticky="ew")

        # 设置按钮的宽度以确保一致性
        for widget in self.root.grid_slaves():
            widget.grid_configure(ipadx=10, ipady=5)

    # 删除物品的方法
    def delete_item(self):
        # 创建一个新的窗口用于删除物品
        delete_window = tk.Toplevel(self.root)
        delete_window.title("删除物品")

        # 如果物品列表为空，弹出警告
        if not self.items:
            messagebox.showwarning("警告", "物品列表为空，无法删除！")
            return

        # 提取物品名称列表
        item_names = [item.name for item in self.items]

        # 创建下拉菜单
        item_to_delete = tk.StringVar()
        item_dropdown = tk.OptionMenu(delete_window, item_to_delete, *item_names)
        item_dropdown.pack(pady=10)

        # 确认删除的函数
        def confirm_delete():
            item_name = item_to_delete.get()
            if item_name:
                # 在这里添加删除物品的逻辑
                self.delete_item_from_list(item_name)
                messagebox.showinfo("成功", f"已成功删除物品: {item_name}")
                delete_window.destroy()  # 关闭删除窗口
            else:
                messagebox.showwarning("警告", "请选择要删除的物品！")

        # 创建确认删除按钮
        confirm_button = tk.Button(delete_window, text="确认删除", command=confirm_delete)
        confirm_button.pack(pady=10)

    # 删除物品的逻辑
    def delete_item_from_list(self, item_name):
        # 根据物品名称删除物品，假设物品是字典，且通过名称找到对应物品并删除
        self.items = [item for item in self.items if item.name != item_name]
        self.save_to_json_delete()

    def view_item_list(self):
        # 创建一个新的窗口显示物品列表
        view_window = tk.Toplevel(self.root)
        view_window.title("物品列表")

        # 假设物品列表保存在 self.items 中
        item_list_text = tk.Text(view_window, width=50, height=20)
        item_list_text.pack(pady=10)

        # 将物品信息添加到文本框中
        for item in self.items:
            item_dict = item.to_dict()  # 将 Item 转换为字典
            item_list_text.insert(tk.END, f"物品名称: {item_dict['name']}\n物品类型: {item_dict['item_type']}\n\n")

        item_list_text.config(state=tk.DISABLED)  # 禁止编辑文本框

    def show_login(self):
        # 设置标题
        title_label = tk.Label(self.root, text="欢迎登录", font=("Arial", 16))
        title_label.place(relx=0.5, rely=0.1, anchor="center")  # 使用place居中标题

        # 用户名标签和输入框
        self.label_username = tk.Label(self.root, text="用户名:")
        self.label_username.place(relx=0.35, rely=0.25, anchor="e")  # 使用place设置标签位置
        self.entry_username = tk.Entry(self.root)
        self.entry_username.place(relx=0.45, rely=0.25, anchor="w")  # 输入框与标签位置对齐

        # 密码标签和输入框
        self.label_password = tk.Label(self.root, text="密码:")
        self.label_password.place(relx=0.35, rely=0.35, anchor="e")  # 设置密码标签位置
        self.entry_password = tk.Entry(self.root, show='*')
        self.entry_password.place(relx=0.45, rely=0.35, anchor="w")  # 设置密码输入框位置

        # 登录按钮
        self.btn_login = tk.Button(self.root, text="登录", width=15, command=self.login)
        self.btn_login.place(relx=0.5, rely=0.45, anchor="center")  # 登录按钮居中

        # 注册按钮
        self.btn_register = tk.Button(self.root, text="注册", width=15, command=self.register)
        self.btn_register.place(relx=0.5, rely=0.55, anchor="center")  # 注册按钮居中

        # 状态标签
        self.status_label = tk.Label(self.root, text="状态：未登录", fg="red")
        self.status_label.place(relx=0.5, rely=0.65, anchor="center")  # 状态标签居中


    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if Validator.validate_non_empty(username) and Validator.validate_non_empty(password):
            # 如果是管理员账号，登录管理员界面
            if username == self.admin_username and password == self.admin_password:
                self.user = username
                self.status_label.config(text=f"状态：欢迎 {username}")
                self.logged_in = True
                self.user_type = "管理员"
                self.show_main_menu()
                return

            # 查找普通用户
            user = self.find_user_by_username(username)

            if user and user.password == password:
                if user.is_verified:
                    self.user = user
                    self.status_label.config(text=f"状态：欢迎 {username}")
                    self.logged_in = True
                    if username == "admin" and password == "123456":
                        self.user_type = "管理员"
                    else:
                        self.user_type = "普通用户"
                    self.show_main_menu()
                else:
                    messagebox.showerror("登录失败", "账户未通过管理员审核")
            else:
                messagebox.showerror("登录失败", "用户名或密码错误")
        else:
            messagebox.showerror("输入错误", "用户名或密码不能为空")

    def set_new_item_type(self):
        # 弹出对话框让用户输入新的物品类型名称
        new_item_type_name = simpledialog.askstring("输入物品类型", "请输入新的物品类型名称:")

        # 如果用户没有输入或者点击取消，返回
        if not new_item_type_name:
            return

        # 弹出对话框让用户输入物品的属性（仅输入属性名）
        attributes_input = simpledialog.askstring("输入物品属性", "请输入属性名称（以逗号分隔，例如：保质期, 数量）:")

        # 如果用户没有输入属性，返回
        if not attributes_input:
            return

        # 解析用户输入的属性并转换为字典格式（默认值为空字符串）
        attributes_dict = {}
        try:
            for attribute in attributes_input.split(","):
                key = attribute.strip()  # 仅使用属性名
                attributes_dict[key] = ""  # 属性值默认为空字符串
        except ValueError:
            messagebox.showerror("错误", "属性格式错误，请按照 '属性名' 的格式输入！")
            return

        # 创建新的ItemType对象
        new_item_type = ItemType(new_item_type_name, attributes_dict)

        # 将新的物品类型对象添加到列表中
        self.item_types.append(new_item_type)

        # 弹出消息框提示用户添加成功
        messagebox.showinfo("成功", f"物品类型 '{new_item_type_name}' 已添加！")

    def show_item_types(self):
        # 弹出对话框显示所有已有物品类型
        item_types_str = "\n".join([item_type.type_name for item_type in self.item_types])
        messagebox.showinfo("已有物品类型", f"当前已有物品类型:\n{item_types_str}")

    def edit_item_type(self):
        # 弹出一个窗口让用户选择物品类型进行修改
        top = tk.Toplevel(self.root)
        top.title("选择物品类型")

        # 显示已有的物品类型的 Listbox
        listbox = tk.Listbox(top, height=5)
        for item_type in self.item_types:
            listbox.insert(tk.END, item_type.type_name)
        listbox.grid(row=0, column=0, padx=10, pady=10)

        def on_select():
            selected_index = listbox.curselection()
            print(f"Selected index: {selected_index}")  # 调试输出
            if selected_index:
                selected_name = self.item_types[selected_index[0]].type_name
                print(f"Selected name: {selected_name}")  # 调试输出
                self.selected_item_type = self.get_item_type_by_name(selected_name)
                if self.selected_item_type:
                    print("Item type found and set.")  # 调试输出
                else:
                    print("Item type not found!")  # 调试输出
                self.show_edit_fields(top)  # 显示修改字段
                # top.destroy()  # 关闭选择窗口
            else:
                messagebox.showwarning("选择无效", "请先选择一个物品类型！")

        confirm_button = tk.Button(top, text="确认选择", command=on_select)
        confirm_button.grid(row=1, column=0, pady=10)

    def get_item_type_by_name(self, type_name):
        # 根据物品类型名称获取对应的物品类型对象
        for item_type in self.item_types:
            if item_type.type_name == type_name:
                return item_type
        return None

    def show_edit_fields(self, top):
        # 如果没有选择物品类型，则返回
        if not self.selected_item_type:
            return

        # 清空窗口内容，准备显示新的输入框
        for widget in top.winfo_children():
            widget.grid_forget()

        # 显示当前物品类型
        label = tk.Label(top, text=f"编辑 {self.selected_item_type.type_name} 的属性")
        label.grid(row=0, column=0, padx=10, pady=10)

        # 创建一个字典存储输入框
        entry_fields = {}
        row = 1

        # 遍历并显示现有的属性（只显示属性名，即 key）
        for attribute in self.selected_item_type.attributes:
            # 显示属性名
            label = tk.Label(top, text=f"属性名 ({attribute})")
            label.grid(row=row, column=0, padx=10, pady=5)
            
            # 输入框允许编辑属性名 (key)
            key_entry = tk.Entry(top)
            key_entry.insert(0, attribute)  # 显示当前的属性名
            key_entry.grid(row=row, column=1, padx=10, pady=5)
            
            entry_fields[attribute] = key_entry
            row += 1

        # 新增属性的输入框
        new_key_label = tk.Label(top, text="新属性名")
        new_key_label.grid(row=row, column=0, padx=10, pady=5)
        new_key_entry = tk.Entry(top)
        new_key_entry.grid(row=row, column=1, padx=10, pady=5)
        row += 1

        # 添加新属性按钮
        def add_new_attribute():
            new_key = new_key_entry.get().strip()

            if not new_key:
                messagebox.showerror("输入错误", "新属性名不能为空！")
                return

            # 检查是否已存在相同的属性名
            if new_key in self.selected_item_type.attributes:
                messagebox.showerror("输入错误", f"属性名 {new_key} 已经存在！")
                return

            # 添加新的属性
            self.selected_item_type.attributes[new_key] = 1
            messagebox.showinfo("修改成功", f"新属性 {new_key} 已添加！")
            self.show_edit_fields(top)  # 重新加载窗口，显示新添加的属性

        add_button = tk.Button(top, text="添加新属性", command=add_new_attribute)
        add_button.grid(row=row, column=0, columnspan=2, pady=10)

        # 保存修改按钮的回调函数
        def save_changes():
            for old_key, key_entry in entry_fields.items():
                new_key = key_entry.get().strip()

                if not new_key:
                    messagebox.showerror("输入错误", f"属性 {old_key} 不能为空！")
                    return

                # 修改现有的属性名
                if new_key != old_key:
                    # Remove the old key-value pair
                    if old_key in self.selected_item_type.attributes:
                        del self.selected_item_type.attributes[old_key]
                    
                    # Add the new key-value pair (make sure you know the value you want to assign to the new key)
                    self.selected_item_type.attributes[new_key] = 1  # Replace `some_value` with the actual value

            # 显示保存成功的提示信息
            messagebox.showinfo("修改成功", f"{self.selected_item_type.type_name} 的属性已更新！")
            top.destroy()

        # # 保存修改按钮
        # save_button = tk.Button(top, text="保存修改", command=save_changes)
        # save_button.grid(row=row, column=0, columnspan=2, pady=10)

        # 取消修改按钮
        def cancel_changes():
            top.destroy()

        # # 返回按钮
        # self.btn_back_to_main = tk.Button(self.root, text="返回", font=("Arial", 14), bg="#f44336", fg="white", command=self.show_main_menu)
        # self.btn_back_to_main.grid(row=10, column=0, columnspan=2, padx=10, pady=10, ipadx=10, ipady=10)

        # 删除属性按钮
        def delete_attribute(attribute):
            def confirm_delete():
                self.selected_item_type.attributes.remove(attribute)
                messagebox.showinfo("删除成功", f"属性 {attribute} 已删除！")
                self.show_edit_fields(top)  # 重新加载窗口，更新显示

            confirm = messagebox.askyesno("确认删除", f"确定要删除属性 {attribute} 吗？")
            if confirm:
                confirm_delete()

        # 显示删除按钮
        for attribute in self.selected_item_type.attributes:
            delete_button = tk.Button(top, text=f"删除 {attribute}", command=lambda a=attribute: delete_attribute(a))
            delete_button.grid(row=row, column=2, padx=10, pady=5)
            row += 1

    def register(self):
        # 显示注册界面
        self.clear_window()

        # 设置grid布局的行列数量
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_columnconfigure(4, weight=1)

        # 设置控件的边距
        padx, pady = 10, 5

        # 用户名输入框
        self.label_username = tk.Label(self.root, text="用户名")
        self.label_username.grid(row=0, column=2, padx=padx, pady=pady, sticky="w")
        self.entry_username = tk.Entry(self.root)
        self.entry_username.grid(row=0, column=3, padx=padx, pady=pady, sticky="w")

        # 密码输入框
        self.label_password = tk.Label(self.root, text="密码")
        self.label_password.grid(row=1, column=2, padx=padx, pady=pady, sticky="w")
        self.entry_password = tk.Entry(self.root, show='*')
        self.entry_password.grid(row=1, column=3, padx=padx, pady=pady, sticky="w")

        # 地址输入框
        self.label_address = tk.Label(self.root, text="地址")
        self.label_address.grid(row=2, column=2, padx=padx, pady=pady, sticky="w")
        self.entry_address = tk.Entry(self.root)
        self.entry_address.grid(row=2, column=3, padx=padx, pady=pady, sticky="w")

        # 联系方式输入框
        self.label_contact = tk.Label(self.root, text="联系方式")
        self.label_contact.grid(row=3, column=2, padx=padx, pady=pady, sticky="w")
        self.entry_contact = tk.Entry(self.root)
        self.entry_contact.grid(row=3, column=3, padx=padx, pady=pady, sticky="w")

        # 提交注册按钮
        self.btn_submit_registration = tk.Button(self.root, text="提交注册", command=self.submit_registration)
        self.btn_submit_registration.grid(row=4, column=2, columnspan=2, pady=(10, 5))

        # 返回登录按钮
        self.btn_back_to_login = tk.Button(self.root, text="返回登录", command=self.show_login_screen)
        self.btn_back_to_login.grid(row=5, column=2, columnspan=2, pady=5)

    def submit_registration(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        address = self.entry_address.get()
        contact = self.entry_contact.get()

        if Validator.validate_non_empty(username) and Validator.validate_non_empty(password):
            # 假设管理员审核通过标志位默认为 False
            user = User(username, password, address, contact, role="user", is_verified=False)
            self.users_db.append(user)
            messagebox.showinfo("注册成功", "您的账户已提交，等待管理员审核")
            self.show_login_screen()
        else:
            messagebox.showerror("输入错误", "请填写完整的注册信息")

    def show_login_screen(self):
        # 清除当前窗口中的控件
        self.logged_in = False
        self.user_type = None
        self.clear_widgets()
        self.create_widgets()

    def show_item_management_screen(self):
        # # 切换到物品管理界面
        if self.user_type == "普通用户":
            self.add_item_button.grid_forget()
            self.search_item_button.grid_forget()
            self.delete_item_button.grid_forget()
            self.view_item_list_button.grid_forget()
            self.logout_button.grid_forget()
        elif self.user_type == "管理员":
            self.approve_admin_button.grid_forget()
            self.set_new_item_type_button.grid_forget()
            self.edit_item_type_button.grid_forget()
            self.add_item_button.grid_forget()
            self.search_item_button.grid_forget()
            self.delete_item_button.grid_forget()
            self.view_item_list_button.grid_forget()
            self.logout_button.grid_forget()

        # 设置背景颜色和字体大小
        self.root.configure(bg="#f0f0f0")

        # 标题
        self.title_label = tk.Label(self.root, text="物品管理", font=("Arial", 20), bg="#f0f0f0", pady=20)
        self.title_label.grid(row=0, column=0, columnspan=2)

        # 物品类型选择
        self.label_item_type = tk.Label(self.root, text="物品类型", font=("Arial", 12), bg="#f0f0f0")
        self.label_item_type.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.item_type_var = tk.StringVar(value="选择物品类型")
        self.item_type_menu = tk.OptionMenu(self.root, self.item_type_var, *[item_type.type_name for item_type in self.item_types], command=self.on_item_type_change)
        self.item_type_menu.config(font=("Arial", 12), width=20)
        self.item_type_menu.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # 物品名称
        self.label_item_name = tk.Label(self.root, text="物品名称", font=("Arial", 12), bg="#f0f0f0")
        self.label_item_name.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_item_name = tk.Entry(self.root, font=("Arial", 12))
        self.entry_item_name.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # 物品描述
        self.label_description = tk.Label(self.root, text="物品描述", font=("Arial", 12), bg="#f0f0f0")
        self.label_description.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_description = tk.Entry(self.root, font=("Arial", 12))
        self.entry_description.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # 物品地址
        self.label_address = tk.Label(self.root, text="物品地址", font=("Arial", 12), bg="#f0f0f0")
        self.label_address.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entry_address = tk.Entry(self.root, font=("Arial", 12))
        self.entry_address.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        # 物品联系人手机
        self.label_phone_number = tk.Label(self.root, text="物品联系人手机", font=("Arial", 12), bg="#f0f0f0")
        self.label_phone_number.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.entry_phone_number = tk.Entry(self.root, font=("Arial", 12))
        self.entry_phone_number.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        # 物品联系人邮箱
        self.label_email_address = tk.Label(self.root, text="物品联系人邮箱", font=("Arial", 12), bg="#f0f0f0")
        self.label_email_address.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.entry_email_address = tk.Entry(self.root, font=("Arial", 12))
        self.entry_email_address.grid(row=6, column=1, padx=10, pady=10, sticky="ew")

        # 动态显示特定属性的字段
        self.extra_fields_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.extra_fields_frame.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # 保存物品按钮
        self.save_button = tk.Button(self.root, text="保存物品", font=("Arial", 14), bg="#4CAF50", fg="white", command=self.save_item)
        self.save_button.grid(row=8, column=0, columnspan=2, padx=10, pady=20, ipadx=10, ipady=10)

        # 状态标签
        self.status_label = tk.Label(self.root, text=f"状态：欢迎 {self.user}", font=("Arial", 12), bg="#f0f0f0")
        self.status_label.grid(row=9, column=0, columnspan=2, pady=10)

        # 返回按钮
        self.btn_back_to_main = tk.Button(self.root, text="返回", font=("Arial", 14), bg="#f44336", fg="white", command=self.show_main_menu)
        self.btn_back_to_main.grid(row=10, column=0, columnspan=2, padx=10, pady=10, ipadx=10, ipady=10)

        # 确保网格系统对齐
        self.root.grid_columnconfigure(1, weight=1)  # 让第二列自动扩展

    def on_item_type_change(self, selected_name):
        """处理物品类型选择变化后，动态显示对应的属性输入框"""
        # 清空之前的额外字段
        for widget in self.extra_fields_frame.winfo_children():
            widget.destroy()

        # 获取选中的物品类型
        selected_item = next(item_type for item_type in self.item_types if item_type.type_name == selected_name)

        # 动态生成物品类型的属性输入框
        row_offset = 0  # 属性的起始行
        self.item_attributes = {}  # 存储属性输入框

        for attribute, value in selected_item.attributes.items():
            label = tk.Label(self.extra_fields_frame, text=attribute, font=("Arial", 12), bg="#f0f0f0")
            label.grid(row=row_offset, column=0, padx=10, pady=10, sticky="w")
            entry = tk.Entry(self.extra_fields_frame, font=("Arial", 12))
            entry.grid(row=row_offset, column=1, padx=10, pady=10, sticky="ew")
            self.item_attributes[attribute] = entry
            row_offset += 1

    def show_attributes(self, item):
        """根据选择的ItemType显示相关属性"""
        attributes_text = "\n".join([f"{key}: {value}" for key, value in item.attributes.items()])
        self.attributes_label.config(text=attributes_text)

    def save_item(self):
        item_name = self.entry_item_name.get().strip()
        description = self.entry_description.get().strip()
        address = self.entry_address.get().strip()
        phone_number = self.entry_phone_number.get().strip()
        email_address = self.entry_email_address.get().strip()
        item_type_name = self.item_type_var.get()

        # 验证物品名称和描述
        if not item_name or not description:
            messagebox.showerror("输入错误", "物品名称和描述不能为空！")
            return

        # 获取物品类型的配置
        selected_item_type = next((item_type for item_type in self.item_types if item_type.type_name == item_type_name), None)
        if selected_item_type is None:
            messagebox.showerror("输入错误", "请选择正确的物品类型！")
            return

        # 获取物品类型的每个属性值
        item_attributes = {}
        for attribute, entry in self.item_attributes.items():
            value = entry.get().strip()
            if not value:
                messagebox.showerror("输入错误", f"{attribute}不能为空！")
                return
            item_attributes[attribute] = value

        # 创建物品类型和物品对象
        item_type = ItemType(item_type_name, item_attributes)
        item = Item(item_name, description, address, phone_number, email_address, item_type)

        # 物品保存逻辑，假设有数据库或集合来保存物品数据
        try:
            # 添加物品到列表
            self.items.append(item)

            # 保存物品列表到 JSON 文件
            self.save_to_json()

            messagebox.showinfo("成功", "物品保存成功！")
            self.clear_fields()  # 清空输入框
        except Exception as e:
            messagebox.showerror("保存失败", f"物品保存失败: {str(e)}")

    def save_to_json(self):
        """将物品列表保存到JSON文件"""
        try:
            # 将物品列表转换为字典列表
            items_data = [item.to_dict() for item in self.items]

            # 检查文件是否存在
            if os.path.exists("items.json"):
                # 如果文件存在，先读取现有数据
                with open("items.json", "r", encoding="utf-8") as f:
                    existing_data = json.load(f)

                # 将新的物品数据追加到现有数据中
                existing_data.extend(items_data)

                # 将更新后的数据写回 JSON 文件
                with open("items.json", "w", encoding="utf-8") as f:
                    json.dump(existing_data, f, ensure_ascii=False, indent=4)
            else:
                # 如果文件不存在，直接创建一个新的 JSON 文件并写入物品数据
                with open("items.json", "w", encoding="utf-8") as f:
                    json.dump(items_data, f, ensure_ascii=False, indent=4)

            messagebox.showinfo("保存成功", "物品列表已成功保存到JSON文件")
            
        except Exception as e:
            messagebox.showerror("保存失败", f"保存到JSON文件失败: {str(e)}")

    def save_to_json_delete(self):
        """将物品列表保存到JSON文件"""
        try:
            # 将物品列表转换为字典列表
            items_data = [item.to_dict() for item in self.items]


            # 如果文件不存在，直接创建一个新的 JSON 文件并写入物品数据
            with open("items.json", "w", encoding="utf-8") as f:
                json.dump(items_data, f, ensure_ascii=False, indent=4)

            messagebox.showinfo("保存成功", "物品列表已成功保存到JSON文件")
            
        except Exception as e:
            messagebox.showerror("保存失败", f"保存到JSON文件失败: {str(e)}")

    def clear_fields(self):
        """清空输入框"""
        self.entry_item_name.delete(0, tk.END)
        self.entry_description.delete(0, tk.END)
        self.entry_address.delete(0, tk.END)
        self.entry_phone_number.delete(0, tk.END)
        self.entry_email_address.delete(0, tk.END)
        # 清空物品类型和属性相关的输入框
        for entry in self.item_attributes.values():
            entry.delete(0, tk.END)

    def search_item(self):
        # 搜寻物品界面
        self.clear_window()

        self.root.title("搜寻物品")
        
        # 物品类型选择
        tk.Label(self.root, text="选择物品类型:", font=("Arial", 12)).grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.selected_type = tk.StringVar(value=self.item_types[0].type_name)  # 设置默认值
        
        # 物品类型下拉菜单
        type_names = [item.type_name for item in self.item_types]  # 获取所有物品类型名称
        type_menu = tk.OptionMenu(self.root, self.selected_type, *type_names)
        type_menu.grid(row=0, column=1, padx=20, pady=10, sticky="w")
        
        # 关键字输入
        tk.Label(self.root, text="输入关键字:", font=("Arial", 12)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.keyword_entry = tk.Entry(self.root, font=("Arial", 12), width=25)
        self.keyword_entry.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        # 搜索按钮
        self.search_button = tk.Button(self.root, text="搜索", font=("Arial", 14), bg="#4CAF50", fg="white", command=self.perform_search)
        self.search_button.grid(row=2, column=0, columnspan=2, pady=20, padx=20, ipadx=10, ipady=10)

        # 返回按钮
        self.btn_back_to_main = tk.Button(self.root, text="返回", font=("Arial", 14), bg="#f44336", fg="white", command=self.show_main_menu)
        self.btn_back_to_main.grid(row=3, column=0, columnspan=2, padx=20, pady=20, ipadx=10, ipady=10)
    
    def perform_search(self):
        item_type = str(self.selected_type.get()).lower()  # 获取选择的物品类型并转为小写
        keyword = self.keyword_entry.get().lower()  # 获取输入的关键字并转为小写

        # 假设 items 是从一个 JSON 文件加载的列表
        with open("items.json", "r", encoding="utf-8") as file:
            items = json.load(file)

        # 过滤物品，找到符合条件的物品
        matched_items = [
            item for item in items
            if (item["item_type"]["type_name"].lower() == item_type and
                (keyword in item["name"].lower() or keyword in item["description"].lower()))
        ]

        # 如果有匹配的物品，打印出来
        if matched_items:
            result_text = "\n".join([f"物品名: {item['name']}, 类型: {item['item_type']['type_name']}, 描述: {item['description']}" for item in matched_items])
            messagebox.showinfo("搜索结果", f"搜索完成, 找到以下物品:\n{result_text}")
        else:
            messagebox.showinfo("搜索结果", "没有找到匹配的物品")

    def show_admin_screen(self):
        # 切换到管理员界面
        self.clear_widgets()

        self.label_admin_title = tk.Label(self.root, text="管理员审核用户")
        self.label_admin_title.grid(row=0, column=0, columnspan=2)

        self.users_listbox = tk.Listbox(self.root)
        self.users_listbox.grid(row=1, column=0, columnspan=2)
        self.refresh_user_listbox()

        self.btn_approve_user = tk.Button(self.root, text="审核通过", command=self.approve_user)
        self.btn_approve_user.grid(row=2, column=0)

        # 返回按钮
        self.btn_back_to_main = tk.Button(self.root, text="返回", font=("Arial", 14), bg="#f44336", fg="white", command=self.show_main_menu)
        self.btn_back_to_main.grid(row=10, column=0, columnspan=2, padx=10, pady=10, ipadx=10, ipady=10)

    def refresh_user_listbox(self):
        self.users_listbox.delete(0, tk.END)
        for user in self.users_db:
            if not user.is_verified:
                self.users_listbox.insert(tk.END, f"{user.username} - 待审核")

    def approve_user(self):
        selected_user_index = self.users_listbox.curselection()

        if selected_user_index:
            selected_user = self.users_db[selected_user_index[0]]
            selected_user.approve()
            messagebox.showinfo("审核通过", f"{selected_user.username} 已通过审核")
            self.refresh_user_listbox()
        else:
            messagebox.showerror("选择错误", "请先选择一个用户进行审核")

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.grid_forget()

    def find_user_by_username(self, username):
        for user in self.users_db:
            if user.username == username:
                return user
        return None

    def logout(self):
        # 退出登录
        self.logged_in = False
        self.user_type = None
        self.show_login_screen()

    def clear_window(self):
        # 清空当前窗口的所有组件
        for widget in self.root.winfo_children():
            widget.destroy()