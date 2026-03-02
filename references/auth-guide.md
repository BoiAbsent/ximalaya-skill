# 喜马拉雅OAuth 2.0鉴权指南

## 目录
1. [OAuth 2.0概述](#oauth-20概述)
2. [授权流程](#授权流程)
3. [Token获取与刷新](#token获取与刷新)
4. [常见问题](#常见问题)

## OAuth 2.0概述

喜马拉雅开放平台使用OAuth 2.0协议进行用户授权，允许第三方应用在用户授权后访问其喜马拉雅数据。

### 核心概念

- **CLIENT_ID**: 应用标识符，在开放平台创建应用后获取
- **CLIENT_SECRET**: 应用密钥，需保密存储
- **access_token**: 访问令牌，用于API调用鉴权
- **refresh_token**: 刷新令牌，用于获取新的access_token
- **授权码 (authorization_code)**: 临时授权凭证，用于换取access_token

## 授权流程

### 授权码模式（推荐）

适用于需要用户授权的第三方应用，流程如下：

1. **引导用户授权**
   ```
   GET https://oauth.ximalaya.com/oauth2/authorize
   参数:
     - client_id: 应用ID
     - response_type: 固定为"code"
     - redirect_uri: 回调地址
     - scope: 授权范围（如:user_info,album_read）
     - state: 防CSRF攻击的随机字符串
   ```

2. **用户确认授权**
   - 用户在喜马拉雅授权页面确认授权
   - 授权成功后跳转到redirect_uri，带上授权码code

3. **获取access_token**
   ```
   POST https://oauth.ximalaya.com/oauth2/token
   参数:
     - grant_type: 固定为"authorization_code"
     - client_id: 应用ID
     - client_secret: 应用密钥
     - code: 授权码
     - redirect_uri: 回调地址（需与步骤1一致）
   ```

4. **使用access_token调用API**
   - 在请求头中添加: `Authorization: Bearer {access_token}`
   - 所有API调用都需要携带此令牌

### 刷新Token流程

当access_token过期时，使用refresh_token获取新的access_token：

```
POST https://oauth.ximalaya.com/oauth2/token
参数:
  - grant_type: 固定为"refresh_token"
  - client_id: 应用ID
  - client_secret: 应用密钥
  - refresh_token: 刷新令牌
```

## Token获取与刷新

### Token响应格式

成功获取token后，响应示例：

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 7200,
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "scope": "user_info album_read"
}
```

### Token使用规范

1. **access_token有效期**: 通常为2小时（7200秒）
2. **refresh_token有效期**: 通常为30天
3. **存储要求**:
   - access_token: 可存储在内存或临时缓存
   - refresh_token: 必须安全存储，推荐加密后持久化
4. **刷新策略**:
   - 在access_token即将过期前自动刷新
   - 使用新token后，旧token立即失效
   - refresh_token使用后需更新为新的refresh_token

## 常见问题

### 1. 授权失败

**错误**: `invalid_client`
**原因**: client_id或client_secret错误
**解决**: 检查应用配置，确认凭证正确

**错误**: `invalid_grant`
**原因**: 授权码过期或已被使用
**解决**: 重新引导用户授权，获取新的授权码

### 2. Token无效

**错误**: `invalid_token`
**原因**: access_token已过期或无效
**解决**: 使用refresh_token刷新，或重新授权

### 3. 权限不足

**错误**: `insufficient_scope`
**原因**: 当前token权限不足
**解决**: 重新授权时申请更多scope

### 4. 回调地址不匹配

**错误**: `redirect_uri_mismatch`
**原因**: 回调地址与开放平台配置不一致
**解决**: 确保redirect_uri与平台配置完全一致

## 在Skill中使用

### 凭证获取流程

本Skill通过交互方式获取access_token：

1. **智能体引导用户完成OAuth授权**：
   - 向用户说明授权流程
   - 提供授权URL和参数说明
   - 指导用户获取access_token

2. **用户提供access_token**：
   - 用户在对话中提供获取到的access_token
   - access_token以明文形式传递（仅用于当前会话）

3. **脚本使用access_token**：
   ```bash
   python scripts/ximalaya_api_client.py --access-token <用户提供的token> --method GET --endpoint /v1/user/info
   ```

### Token管理建议

- **存储**: 建议仅在当前会话中使用，不持久化
- **刷新**: 当access_token过期时，引导用户重新获取
- **安全**: 提醒用户妥善保管access_token，不要泄露

### 自动刷新

当前版本不支持自动刷新token，如需刷新：
1. 使用refresh_token获取新的access_token
2. 引导用户在喜马拉雅平台重新授权
3. 用户提供新的access_token

### 安全建议

1. 不要在日志中打印access_token或refresh_token
2. 使用HTTPS进行所有API调用
3. 定期更新CLIENT_SECRET
4. 限制应用权限范围，仅申请必要的scope

## 授权范围说明

### 常用scope

| scope | 说明 | 使用场景 |
|-------|------|----------|
| user_info | 获取用户基本信息 | 用户中心、个性化推荐 |
| album_read | 读取专辑信息 | 浏览专辑、详情查询 |
| album_write | 管理专辑数据 | 专辑管理、内容发布 |
| audio_play | 播放音频内容 | 播放器、音频服务 |
| subscription | 管理用户订阅 | 订阅管理、收藏列表 |
| search | 搜索功能 | 内容搜索、推荐 |

### 申请原则

- 最小权限原则：只申请必要的scope
- 根据实际使用场景选择合适的权限组合
- 不同功能的模块可申请不同scope
