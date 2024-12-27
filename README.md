# Item-Resurrection-CS3331-FinalProject
# 物品复活软件（Items-Revival）

## 项目简介
在大学生的日常生活中，许多物品由于各种原因难以舍弃，但又因占用空间而成为烦恼。本软件致力于帮助学生更好地管理这些物品，提供一个平台以便于重新利用、转赠或处理不再需要的物品。用户可以通过本软件对物品进行分类、记录详细信息、进行添加、搜索以及删除等操作，让物品“复活”，从而更好地发挥它们的价值。

“物品复活系统（Items-Revival）”是一款基于 Python 和 Tkinter 开发的桌面应用程序。它结合 SQLite 数据库存储物品信息，提供用户友好的图形界面（GUI）进行交互，支持物品的管理功能，如添加、搜索、删除等操作。这款软件特别适合大学生群体，用于管理闲置物品，减少浪费并优化空间使用。

该项目是为 CS3331 软件工程课程（2024-2025-1学期）的课程项目而开发的。

---

## 主要功能

### 1. **物品管理功能**
本系统支持对物品进行全面的管理，用户可以轻松地对每一件物品进行增、查、改、删等操作。
- 物品添加，用户可以输入物品的基本信息，包括：
  - 物品名称
  - 物品类别（如：食品、书籍、工具等）
  - 物品描述
  - 物品存放地址
  - 联系人信息（如手机号码、电子邮件等）
  - 系统会根据物品的类别，动态生成额外的扩展属性。例如：
    - 食品类别：用户需要输入保质期、数量等信息。
    - 书籍类别：用户需要填写作者、出版社等信息。
    - 工具类别：用户需要填写品牌、型号等信息。
- 物品搜索：
  - 按类别搜索。
  - 可以根据名称和描述中的关键字辅助搜索
- 物品删除：
  - 可以根据物品名称删除某物体
  - 删除操作动态更新到数据库
- 物品查看列表：
  - 可以查看数据库中现有的所有物品以及其类别
### 2. **用户注册功能**
- 用户注册
  - 当用户还没有账号时，可以提交注册请求
  - 管理员可以批准注册请求
    
### 2. **物品类别添加，修改功能**
- 物品类别添加
  - 管理员可以添加新的物品类别
  - 管理员可以进一步添加新物品类别的各类属性
- 物品类别修改
  - 管理员可以对已有的物品类别进行修改
  - 管理员可以对已有的物品类别添加新属性
  - 管理员可以对已有的物品类别删除新属性
    
## 技术栈

- **语言**：Python
- **界面**：Tkinter
- **数据库**：JSON

---

## 用例模型

### **1.参与者**
**管理员**：系统的管理者，负责物品的添加、搜索、删除、查看，新账号注册等操作。
**普通用户**：系统的直使用者，负责物品的添加、搜索、删除、查看，普通用户的注册审批，物品类别的修改，添加物品类别等操作。

### **2.用例列表**
| **用例编号** | **用例名称**        | **描述**            |
|----------|-------------------|---------------------------------------|
| UC01     | 搜索物品           | 用户/管理员可以根据条件（如名称、类别等）搜索物品 |
| UC02     | 添加物品           | 用户/管理员可以添加新的物品到系统中             |
| UC03     | 删除物品           | 用户/管理员可以删除系统中的物品                 |
| UC04     | 查看物品详情       | 用户/管理员可以查看某个物品的详细信息            |
| UC05     | 登录系统           | 用户/管理员可以通过用户名和密码登录系统          |
| UC06     | 修改物品类别       | 管理员可以修改物品的类别信息                    |
| UC07     | 添加物品类别	     | 管理员可以添加新的物品类别                      |
| UC08     | 注册新账号         | 用户可以注册一个新账号                         |
| UC09     | 审批普通用户注册	 | 管理员审核并批准普通用户的注册申请               |
![用例图](https://github.com/user-attachments/assets/4f71d854-6aee-4dd9-91d3-2977599f3035)

## 针对用例画顺序图

### **UC01：搜索物品**
- **主要参与者**：用户/管理员
- **目标**：根据条件（如名称、类别等）搜索物品
- **基本流程**：
  1. 用户/管理员输入类别和关键词
  2. 系统从数据库比对类别和关键词
  3. 系统将匹配到的物品显示在界面中

### **UC02：添加物品**
- **主要参与者**：用户/管理员
- **目标**：将新物品添加到系统中
- **基本流程**：
  1. 用户/管理员点击“添加物品”按钮
  2. 系统显示添加物品的输入表单
  3. 用户/管理员填写物品信息并提交
  4. 系统将物品信息保存到数据库
  5. 系统反馈操作结果

### **UC03：删除物品**
- **主要参与者**：用户/管理员
- **目标**：从系统中删除某个物品
- **基本流程**：
  1. 用户/管理员在物品列表中选择要删除的物品
  2. 用户/管理员确认删除
  3. 系统将该物品从数据库中删除
  4. 系统反馈操作结果

### **UC04：查看物品详情**
- **主要参与者**：用户/管理员
- **目标**：查看某个物品的详细信息
- **基本流程**：
  1. 用户/管理员点击“查看物品详情”按钮
  2. 系统加载所有物品的详细信息
  3. 系统显示所有物品的详细信息页面

### **UC05：登录系统**
- **主要参与者**：用户/管理员
- **目标**：通过用户名和密码登录系统
- **基本流程**：
  1. 用户/管理员输入用户名和密码。
  2. 系统验证用户名和密码
  3. 系统返回登录结果（成功或失败）

### **UC06：修改物品类别**
- **主要参与者**：管理员
- **目标**：修改物品的类别信息
- **基本流程**：
  1. 管理员在物品列表中选择需要修改类别的物品
  2. 系统展示修改类别的界面
  3. 管理员添加或删除类别属性
  4. 系统更新物品类别信息
  5. 系统反馈操作结果

### **UC07：添加物品类别**
- **主要参与者**：管理员
- **目标**：添加新的物品类别
- **基本流程**：
  1. 管理员进入物品类别管理页面
  2. 系统显示现有类别列表和添加类别的选项
  3. 管理员填写新类别名称及新属性并提交
  4. 系统保存新类别到数据库
  5. 系统反馈操作结果

### **UC08：注册新账号**
- **主要参与者**：用户
- **目标**：用户注册新账号
- **基本流程**：
  1. 用户点击注册按钮
  2. 系统显示注册表单
  3. 用户填写信息并提交注册申请
 
### **UC09：审批普通用户注册**
- **主要参与者**：管理员
- **目标**：管理员审核并批准普通用户的注册申请。
- **基本流程**：
  1. 管理员查看待审批的用户注册申请
  2. 管理员批准或拒绝用户申请
  3. 系统根据管理员的决定更新用户状态
  4. 系统反馈审批结果

---

## 类图
<img width="575" alt="位图" src="https://github.com/user-attachments/assets/1517b1f1-2aa3-473e-93fc-10ab2abee89f" />
