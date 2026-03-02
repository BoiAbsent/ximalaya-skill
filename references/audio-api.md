# 音频API参考文档

## 目录
1. [概述](#概述)
2. [获取声音详情](#获取声音详情)
3. [获取播放地址](#获取播放地址)
4. [专辑声音列表](#专辑声音列表)
5. [声音统计](#声音统计)

## 概述

音频API模块提供声音信息查询、播放地址获取、声音列表等功能。

### 基础信息

- **Base URL**: `https://api.ximalaya.com`
- **鉴权方式**: OAuth 2.0
- **请求格式**: JSON
- **响应格式**: JSON

## 获取声音详情

### 接口地址

`GET /v1/tracks/{track_id}`

### 路径参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| track_id | Long | 是 | 声音ID |

### 响应示例

```json
{
  "ret": 0,
  "msg": "success",
  "data": {
    "track_id": 456789,
    "title": "声音标题",
    "album_id": 123456,
    "album_title": "专辑标题",
    "album_cover": "https://example.com/cover.jpg",
    "announcer_id": 789,
    "announcer_name": "主播名",
    "category_id": 1,
    "category_name": "有声书",
    "duration": 1800,
    "file_size": 36000000,
    "play_count": 10000,
    "like_count": 500,
    "comment_count": 100,
    "share_count": 50,
    "intro": "声音简介",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-02T00:00:00Z",
    "is_paid": false,
    "price": 0,
    "is_vip": false
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| track_id | Long | 声音ID |
| title | String | 声音标题 |
| album_id | Long | 所属专辑ID |
| album_title | String | 专辑标题 |
| duration | Integer | 时长（秒） |
| file_size | Long | 文件大小（字节） |
| play_count | Integer | 播放次数 |
| is_paid | Boolean | 是否付费 |
| price | Integer | 价格（分） |
| is_vip | Boolean | 是否VIP专享 |

### 使用场景

- 声音详情页
- 播放器信息展示
- 声音分享

## 获取播放地址

### 接口地址

`GET /v1/tracks/{track_id}/play_url`

### 路径参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| track_id | Long | 是 | 声音ID |

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| quality | String | 否 | 音质: low-低, standard-标准, high-高, super-超清，默认standard |

### 响应示例

```json
{
  "ret": 0,
  "msg": "success",
  "data": {
    "track_id": 456789,
    "play_url": "https://audio.ximalaya.com/xxx.mp3",
    "expire_time": 1672531200,
    "quality": "standard",
    "duration": 1800,
    "file_size": 36000000
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| play_url | String | 播放地址 |
| expire_time | Long | 过期时间（Unix时间戳） |
| quality | String | 实际音质 |

### 重要说明

1. **URL有效期**: 播放地址有有效期，通常为2小时
2. **防盗链**: 播放地址包含防盗链参数，直接使用即可
3. **音质选择**:
   - `low`: 适合网络较差的场景
   - `standard`: 默认音质，平衡质量和流量
   - `high`: 适合WiFi环境
   - `super`: 最高音质，仅部分内容支持

### 使用场景

- 音频播放
- 下载功能
- 音质切换

## 专辑声音列表

### 接口地址

`GET /v1/albums/{album_id}/tracks`

### 路径参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| album_id | Long | 是 | 专辑ID |

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | Integer | 否 | 页码，默认1 |
| limit | Integer | 否 | 每页数量，默认20，最大100 |
| sort | String | 否 | 排序: asc-正序, desc-倒序，默认asc |

### 响应示例

```json
{
  "ret": 0,
  "msg": "success",
  "data": {
    "total": 100,
    "page": 1,
    "limit": 20,
    "album_info": {
      "album_id": 123456,
      "title": "专辑标题",
      "cover_url": "https://example.com/cover.jpg",
      "track_count": 100
    },
    "list": [
      {
        "track_id": 456789,
        "title": "声音标题",
        "index": 1,
        "duration": 1800,
        "play_count": 10000,
        "created_at": "2023-01-01T00:00:00Z",
        "is_paid": false,
        "is_vip": false
      }
    ]
  }
}
```

### 使用场景

- 专辑详情页声音列表
- 播放列表
- 批量获取声音信息

## 声音统计

### 获取声音统计信息

**接口地址**: `GET /v1/tracks/{track_id}/stats`

**路径参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| track_id | Long | 是 | 声音ID |

**响应示例**:

```json
{
  "ret": 0,
  "msg": "success",
  "data": {
    "track_id": 456789,
    "play_count": 10000,
    "play_count_today": 100,
    "like_count": 500,
    "comment_count": 100,
    "share_count": 50,
    "collect_count": 200,
    "finish_rate": 75.5
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| play_count | Integer | 总播放次数 |
| play_count_today | Integer | 今日播放次数 |
| like_count | Integer | 点赞数 |
| comment_count | Integer | 评论数 |
| share_count | Integer | 分享数 |
| collect_count | Integer | 收藏数 |
| finish_rate | Float | 完播率（百分比） |

### 使用场景

- 数据分析
- 内容推荐
- 运营统计

## 错误码说明

| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| 30001 | 声音不存在 | 检查track_id是否正确 |
| 30002 | 专辑不存在 | 检查album_id是否正确 |
| 30003 | 无播放权限 | 需要购买或开通VIP |
| 30004 | 音质不支持 | 当前内容不支持该音质 |
| 30005 | 参数错误 | 检查请求参数格式 |
| 99999 | 系统错误 | 稍后重试或联系客服 |

## 使用示例

### 示例1：获取声音详情

```bash
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/tracks/456789
```

### 示例2：获取播放地址

```bash
# 获取标准音质播放地址
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/tracks/456789/play_url

# 获取高清音质播放地址
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/tracks/456789/play_url --params 'quality=high'
```

### 示例3：获取专辑声音列表

```bash
# 获取第一页声音（正序）
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/albums/123456/tracks --params 'page=1&limit=20&sort=asc'

# 获取最新20个声音（倒序）
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/albums/123456/tracks --params 'limit=20&sort=desc'
```

### 示例4：获取声音统计

```bash
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/tracks/456789/stats
```

## 最佳实践

### 1. 播放地址缓存

播放地址有有效期，建议：

- 缓存播放地址，记录过期时间
- 在过期前5分钟重新获取
- 播放前检查URL是否有效

### 2. 音质自适应

根据网络环境动态选择音质：

```bash
# WiFi环境使用高清
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/tracks/456789/play_url --params 'quality=high'

# 4G网络使用标准
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/tracks/456789/play_url --params 'quality=standard'
```

### 3. 分页加载声音列表

对于声音数量较多的专辑，分页加载：

```bash
# 第一页
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/albums/123456/tracks --params 'page=1&limit=20'

# 第二页
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/albums/123456/tracks --params 'page=2&limit=20'
```

### 4. 播放权限检查

在获取播放地址前，先检查声音详情：

1. 检查`is_paid`字段，如果是付费内容需先购买
2. 检查`is_vip`字段，如果是VIP专享需检查用户VIP状态
3. 检查声音是否可用（未下架、未删除）

### 5. 批量获取优化

如果需要获取多个声音的详情，建议：

- 先获取专辑声音列表（包含基本信息）
- 只对需要播放的声音获取详情和播放地址
- 避免一次性获取所有声音的完整详情

## 播放器集成建议

### 播放流程

1. 获取声音详情
2. 检查播放权限
3. 获取播放地址
4. 初始化播放器
5. 播放音频

### 播放进度上报

建议定期上报播放进度（可选功能）：

```bash
# 上报播放进度（示例接口，实际以平台为准）
python scripts/ximalaya_api_client.py --method POST --endpoint /v1/tracks/456789/play_progress --body '{"played_time": 300}'
```

### 错误处理

播放过程中可能遇到的问题：

- **播放地址过期**: 重新获取播放地址
- **网络错误**: 显示重试按钮
- **权限变更**: 提示用户重新购买或开通VIP
- **内容下架**: 显示提示信息
