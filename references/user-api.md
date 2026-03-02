# 用户API参考文档

## 目录
1. [概述](#概述)
2. [获取用户信息](#获取用户信息)
3. [订阅管理](#订阅管理)
4. [收藏管理](#收藏管理)
5. [历史记录](#历史记录)

## 概述

用户API模块提供用户信息查询、订阅管理、收藏管理等功能。所有接口都需要OAuth鉴权。

### 基础信息

- **Base URL**: `https://api.ximalaya.com`
- **鉴权方式**: OAuth 2.0 (Bearer Token)
- **请求格式**: JSON
- **响应格式**: JSON

### 通用响应格式

```json
{
  "ret": 0,
  "msg": "success",
  "data": {
    // 具体数据
  }
}
```

## 获取用户信息

### 获取当前用户信息

**接口地址**: `GET /v1/user/info`

**请求参数**: 无（从token中识别用户）

**响应示例**:

```json
{
  "ret": 0,
  "msg": "success",
  "data": {
    "user_id": 12345678,
    "nickname": "用户昵称",
    "avatar_url": "https://example.com/avatar.jpg",
    "gender": 1,
    "signature": "个性签名",
    "followers_count": 100,
    "following_count": 50,
    "created_at": "2020-01-01T00:00:00Z"
  }
}
```

**字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| user_id | Long | 用户ID |
| nickname | String | 用户昵称 |
| avatar_url | String | 头像URL |
| gender | Integer | 性别: 0-未知, 1-男, 2-女 |
| signature | String | 个性签名 |
| followers_count | Integer | 粉丝数 |
| following_count | Integer | 关注数 |
| created_at | String | 注册时间 |

**使用场景**:
- 用户中心展示
- 个性化推荐
- 账号信息更新

## 订阅管理

### 获取订阅列表

**接口地址**: `GET /v1/user/subscriptions`

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | Integer | 否 | 页码，默认1 |
| limit | Integer | 否 | 每页数量，默认20，最大100 |

**响应示例**:

```json
{
  "ret": 0,
  "msg": "success",
  "data": {
    "total": 150,
    "page": 1,
    "limit": 20,
    "list": [
      {
        "album_id": 123456,
        "title": "专辑标题",
        "cover_url": "https://example.com/cover.jpg",
        "announcer_name": "主播名",
        "track_count": 100,
        "play_count": 1000000,
        "subscribe_time": "2023-01-01T00:00:00Z"
      }
    ]
  }
}
```

**使用场景**:
- 我的订阅页面
- 订阅更新提醒
- 个性化推荐

### 订阅专辑

**接口地址**: `POST /v1/user/subscriptions`

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| album_id | Long | 是 | 专辑ID |

**请求示例**:

```json
{
  "album_id": 123456
}
```

**响应示例**:

```json
{
  "ret": 0,
  "msg": "订阅成功"
}
```

### 取消订阅

**接口地址**: `DELETE /v1/user/subscriptions/{album_id}`

**路径参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| album_id | Long | 是 | 专辑ID |

**响应示例**:

```json
{
  "ret": 0,
  "msg": "取消订阅成功"
}
```

## 收藏管理

### 获取收藏列表

**接口地址**: `GET /v1/user/favorites`

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | String | 否 | 类型: album/track/all，默认all |
| page | Integer | 否 | 页码，默认1 |
| limit | Integer | 否 | 每页数量，默认20 |

**响应示例**:

```json
{
  "ret": 0,
  "msg": "success",
  "data": {
    "total": 50,
    "page": 1,
    "limit": 20,
    "list": [
      {
        "id": 123456,
        "type": "album",
        "title": "专辑标题",
        "cover_url": "https://example.com/cover.jpg",
        "created_at": "2023-01-01T00:00:00Z"
      }
    ]
  }
}
```

### 添加收藏

**接口地址**: `POST /v1/user/favorites`

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | String | 是 | 类型: album/track |
| target_id | Long | 是 | 专辑ID或声音ID |

**请求示例**:

```json
{
  "type": "album",
  "target_id": 123456
}
```

### 取消收藏

**接口地址**: `DELETE /v1/user/favorites/{type}/{target_id}`

**路径参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | String | 是 | 类型: album/track |
| target_id | Long | 是 | 专辑ID或声音ID |

## 历史记录

### 获取播放历史

**接口地址**: `GET /v1/user/play_history`

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | Integer | 否 | 页码，默认1 |
| limit | Integer | 否 | 每页数量，默认20 |

**响应示例**:

```json
{
  "ret": 0,
  "msg": "success",
  "data": {
    "total": 200,
    "page": 1,
    "limit": 20,
    "list": [
      {
        "track_id": 456789,
        "track_title": "声音标题",
        "album_id": 123456,
        "album_title": "专辑标题",
        "play_time": 180,
        "played_at": "2023-01-01T12:00:00Z"
      }
    ]
  }
}
```

**字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| track_id | Long | 声音ID |
| track_title | String | 声音标题 |
| album_id | Long | 专辑ID |
| album_title | String | 专辑标题 |
| play_time | Integer | 播放时长（秒） |
| played_at | String | 播放时间 |

## 错误码说明

| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| 10001 | 用户不存在 | 检查token是否有效 |
| 10002 | 权限不足 | 检查scope权限 |
| 10003 | 专辑不存在 | 检查album_id是否正确 |
| 10004 | 已订阅 | 重复订阅，无需处理 |
| 10005 | 未订阅 | 无法取消订阅 |
| 99999 | 系统错误 | 稍后重试或联系客服 |

## 使用示例

### 示例1：获取用户信息和订阅列表

```bash
# 获取用户信息
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/user/info

# 获取订阅列表
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/user/subscriptions --params 'page=1&limit=10'
```

### 示例2：订阅专辑

```bash
python scripts/ximalaya_api_client.py --method POST --endpoint /v1/user/subscriptions --body '{"album_id": 123456}'
```

### 示例3：取消订阅

```bash
python scripts/ximalaya_api_client.py --method DELETE --endpoint /v1/user/subscriptions/123456
```
