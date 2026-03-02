---
name: ximalaya-api
description: 提供喜马拉雅开放平台API的完整使用指南和调用能力；当用户需要调用喜马拉雅用户接口、获取专辑信息、搜索音频内容或管理订阅收藏时使用
dependency:
  python:
    - requests>=2.28.0
---

# 喜马拉雅开放平台API集成

## 任务目标
- 本Skill用于：集成喜马拉雅开放平台API，实现音频内容的搜索、获取、播放和管理
- 能力包含：用户鉴权、专辑查询、音频搜索、分类浏览、订阅管理、评论互动
- 触发条件：用户需要访问喜马拉雅音频内容、搜索专辑、获取声音详情或管理个人喜马拉雅数据

## 前置准备

### 依赖说明
```
requests>=2.28.0
```

### 凭证获取流程（执行时交互）

本Skill使用OAuth 2.0授权，access_token在Skill执行过程中通过交互获取：

**步骤1：引导用户完成OAuth授权**

向用户说明OAuth授权流程：
1. 访问喜马拉雅开放平台：https://open.ximalaya.com
2. 创建应用或使用已有应用，获取CLIENT_ID和CLIENT_SECRET
3. 使用OAuth授权流程获取access_token

**授权流程（由用户在喜马拉雅平台完成）**：
```
1. 引导用户访问授权页面：
   GET https://oauth.ximalaya.com/oauth2/authorize
   参数：client_id, response_type=code, redirect_uri, scope, state

2. 用户确认授权后，获取授权码code

3. 使用授权码换取access_token：
   POST https://oauth.ximalaya.com/oauth2/token
   参数：grant_type=authorization_code, client_id, client_secret, code, redirect_uri

4. 获取access_token，用于后续API调用
```

**步骤2：获取用户的access_token**

在对话中向用户询问：
> "请提供您的喜马拉雅access_token，用于API调用鉴权。"

**步骤3：使用access_token调用API**

将用户提供的access_token作为参数传递给脚本：
```bash
python scripts/ximalaya_api_client.py --access-token <用户提供的token> --method GET --endpoint /v1/user/info
```

**重要说明**：
- access_token由用户提供，Skill不预配置任何凭证
- 智能体负责引导用户完成授权流程
- access_token仅用于当前会话，不建议持久化存储

## 操作步骤

### 标准流程

1. **理解用户需求**
   - 识别用户意图：搜索音频、获取专辑、用户信息、管理订阅等
   - 确定所需的API模块和接口
   - 参考[API文档索引](#资源索引)选择合适的接口

2. **获取用户凭证（首次调用时）**
   - 向用户说明OAuth授权流程（参考[auth-guide.md](references/auth-guide.md)）
   - 引导用户访问喜马拉雅开放平台完成授权
   - 在对话中向用户询问access_token
   - 保存用户提供的access_token用于后续调用

3. **构建API请求**
   - 根据API文档确定请求参数
   - 智能体理解业务场景，构建合理的参数组合
   - 调用`scripts/ximalaya_api_client.py`执行API调用，传递access_token参数

4. **处理响应数据**
   - 解析API返回的JSON数据
   - 根据用户需求提取关键信息
   - 生成友好的响应格式

### 分支流程

**当用户需要搜索音频内容**：
- 使用搜索API模块（见[search-api.md](references/search-api.md)）
- 支持关键词搜索、分类筛选、排序等
- 返回匹配的专辑、声音或用户列表

**当用户需要获取专辑详情**：
- 使用专辑API模块（见[album-api.md](references/album-api.md)）
- 获取专辑基本信息、声音列表、标签等
- 支持分页获取声音列表

**当用户需要管理订阅**：
- 使用订阅相关API（见[user-api.md](references/user-api.md)）
- 支持订阅/取消订阅专辑
- 获取用户订阅列表

## 资源索引

### 必要脚本
- **[scripts/ximalaya_api_client.py](scripts/ximalaya_api_client.py)**
  - 用途：统一的API调用客户端，处理OAuth鉴权和HTTP请求
  - 核心功能：
    - 自动获取和刷新access_token
    - 统一的错误处理机制
    - 支持GET/POST/PUT/DELETE方法
  - 使用方式：
    ```bash
    python /workspace/projects/ximalaya-api/scripts/ximalaya_api_client.py --access-token <用户的token> --method GET --endpoint /v1/albums --params 'category_id=1&limit=20'
    ```

### 领域参考
- **[references/auth-guide.md](references/auth-guide.md)**
  - 何时读取：首次使用或遇到鉴权问题时
  - 内容：OAuth 2.0授权流程详解、token获取与刷新机制

- **[references/user-api.md](references/user-api.md)**
  - 何时读取：需要获取用户信息、管理订阅收藏时
  - 内容：用户信息API、订阅列表、收藏管理等接口说明

- **[references/album-api.md](references/album-api.md)**
  - 何时读取：需要查询专辑信息、分类浏览时
  - 内容：专辑详情、专辑列表、分类树等接口说明

- **[references/audio-api.md](references/audio-api.md)**
  - 何时读取：需要获取声音详情、播放地址时
  - 内容：声音信息、播放URL、声音统计等接口说明

- **[references/search-api.md](references/search-api.md)**
  - 何时读取：需要搜索内容时
  - 内容：全文搜索、关键词搜索、搜索结果过滤等接口说明

## API模块概览

### 1. 用户模块
- 获取用户信息
- 订阅管理
- 收藏管理
- 历史记录

### 2. 专辑模块
- 专辑详情查询
- 专辑列表（分类、推荐）
- 分类树浏览
- 热门专辑

### 3. 音频模块
- 声音详情查询
- 播放URL获取
- 声音列表
- 声音统计

### 4. 搜索模块
- 关键词搜索
- 分类搜索
- 搜索建议
- 热门搜索词

## 注意事项

- 仅在需要时读取详细的API文档，优先使用SKILL.md中的快速指引
- access_token由用户在对话中提供，首次使用时需引导用户完成OAuth授权
- API调用失败时，检查：
  1. access_token是否有效或过期
  2. 请求参数是否符合API规范
  3. access_token是否有足够的权限（scope）
- 智能体负责业务逻辑理解和参数构建，脚本负责技术性API调用
- 注意API调用频率限制，合理设置请求间隔
- 用户提供的access_token仅用于当前会话，不建议持久化或分享

## 使用示例

### 示例1：搜索专辑
**功能说明**：根据关键词搜索相关专辑
**执行方式**：
1. 智能体理解用户搜索意图，提取关键词
2. 如首次调用，向用户询问access_token
3. 参考[search-api.md](references/search-api.md)确定搜索参数
4. 调用脚本执行搜索API
5. 智能体解析结果并展示匹配的专辑

**关键参数**：
- `--access-token`: 用户提供的访问令牌
- `keyword`: 搜索关键词
- `category_id`: 分类ID（可选）
- `page`: 页码
- `limit`: 每页数量

**示例命令**：
```bash
python scripts/ximalaya_api_client.py --access-token <用户的token> --method GET --endpoint /v1/search --params 'keyword=科幻&page=1&limit=20'
```

### 示例2：获取专辑详情
**功能说明**：获取指定专辑的完整信息
**执行方式**：
1. 获取专辑ID
2. 调用脚本查询专辑详情API
3. 智能体提取关键信息（标题、主播、简介、声音数等）
4. 可选：进一步获取专辑的声音列表

**关键参数**：
- `--access-token`: 用户提供的访问令牌
- `album_id`: 专辑ID
- `include_tracks`: 是否包含声音列表

**示例命令**：
```bash
python scripts/ximalaya_api_client.py --access-token <用户的token> --method GET --endpoint /v1/albums/123456
```

### 示例3：管理用户订阅
**功能说明**：订阅或取消订阅专辑，查看订阅列表
**执行方式**：
1. 智能体确认用户操作意图（订阅/取消/查看）
2. 调用相应的订阅管理API
3. 解析操作结果并反馈给用户

**关键参数**：
- `--access-token`: 用户提供的访问令牌
- `album_id`: 专辑ID（订阅/取消订阅时）
- `action`: 操作类型（subscribe/unsubscribe）

**示例命令**：
```bash
# 查看订阅列表
python scripts/ximalaya_api_client.py --access-token <用户的token> --method GET --endpoint /v1/user/subscriptions

# 订阅专辑
python scripts/ximalaya_api_client.py --access-token <用户的token> --method POST --endpoint /v1/user/subscriptions --body '{"album_id": 123456}'
```

## 错误处理

常见错误及处理方式：

1. **401 Unauthorized**
   - 原因：access_token无效或过期
   - 处理：脚本会自动尝试刷新token，失败时需重新授权

2. **429 Too Many Requests**
   - 原因：超出API调用频率限制
   - 处理：降低请求频率，增加请求间隔

3. **404 Not Found**
   - 原因：请求的资源不存在
   - 处理：检查专辑ID、声音ID等参数是否正确

4. **400 Bad Request**
   - 原因：请求参数错误
   - 处理：参考API文档检查参数格式和必填项

## 扩展指南

当需要集成更多API时：
1. 在references/目录下创建对应的API文档
2. 按照统一格式编写文档（格式定义、参数说明、示例）
3. 在SKILL.md的资源索引中添加新文档链接
4. 如需特殊处理，可扩展ximalaya_api_client.py脚本
