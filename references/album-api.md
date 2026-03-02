# 专辑API参考文档

## 目录
1. [概述](#概述)
2. [获取专辑详情](#获取专辑详情)
3. [获取专辑列表](#获取专辑列表)
4. [分类浏览](#分类浏览)
5. [热门推荐](#热门推荐)

## 概述

专辑API模块提供专辑信息查询、分类浏览、热门推荐等功能。

### 基础信息

- **Base URL**: `https://api.ximalaya.com`
- **鉴权方式**: OAuth 2.0 (部分接口支持匿名访问)
- **请求格式**: JSON
- **响应格式**: JSON

## 获取专辑详情

### 接口地址

`GET /v1/albums/{album_id}`

### 路径参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| album_id | Long | 是 | 专辑ID |

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| include_tracks | Boolean | 否 | 是否包含声音列表，默认false |
| page | Integer | 否 | 声音列表页码，默认1 |
| limit | Integer | 否 | 每页声音数量，默认20 |

### 响应示例

```json
{
  "ret": 0,
  "msg": "success",
  "data": {
    "album_id": 123456,
    "title": "专辑标题",
    "subtitle": "副标题",
    "cover_url": "https://example.com/cover.jpg",
    "cover_url_large": "https://example.com/cover_large.jpg",
    "announcer_id": 789,
    "announcer_name": "主播名",
    "announcer_avatar": "https://example.com/avatar.jpg",
    "category_id": 1,
    "category_name": "有声书",
    "tags": ["标签1", "标签2"],
    "intro": "专辑简介",
    "track_count": 100,
    "play_count": 1000000,
    "subscribe_count": 50000,
    "share_count": 10000,
    "comment_count": 5000,
    "is_finished": true,
    "update_frequency": "每日更新",
    "last_updated": "2023-01-01T00:00:00Z",
    "created_at": "2020-01-01T00:00:00Z",
    "tracks": {
      "total": 100,
      "page": 1,
      "limit": 20,
      "list": [
        {
          "track_id": 456789,
          "title": "声音标题",
          "index": 1,
          "duration": 1800,
          "play_count": 10000,
          "created_at": "2023-01-01T00:00:00Z"
        }
      ]
    }
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| album_id | Long | 专辑ID |
| title | String | 专辑标题 |
| cover_url | String | 封面图URL |
| announcer_name | String | 主播名称 |
| category_name | String | 分类名称 |
| intro | String | 专辑简介 |
| track_count | Integer | 声音总数 |
| play_count | Integer | 播放次数 |
| is_finished | Boolean | 是否完结 |
| tracks | Object | 声音列表（当include_tracks=true时返回） |

### 使用场景

- 专辑详情页展示
- 专辑推荐
- 声音列表加载

## 获取专辑列表

### 接口地址

`GET /v1/albums`

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| category_id | Integer | 否 | 分类ID |
| page | Integer | 否 | 页码，默认1 |
| limit | Integer | 否 | 每页数量，默认20，最大100 |
| sort | String | 否 | 排序: latest-最新, hot-热门, recommend-推荐 |

### 响应示例

```json
{
  "ret": 0,
  "msg": "success",
  "data": {
    "total": 1000,
    "page": 1,
    "limit": 20,
    "list": [
      {
        "album_id": 123456,
        "title": "专辑标题",
        "cover_url": "https://example.com/cover.jpg",
        "announcer_name": "主播名",
        "category_name": "有声书",
        "track_count": 100,
        "play_count": 1000000,
        "is_finished": true,
        "updated_at": "2023-01-01T00:00:00Z"
      }
    ]
  }
}
```

### 使用场景

- 分类专辑列表
- 发现页内容
- 推荐流展示

## 分类浏览

### 获取分类树

**接口地址**: `GET /v1/categories`

**请求参数**: 无

**响应示例**:

```json
{
  "ret": 0,
  "msg": "success",
  "data": [
    {
      "category_id": 1,
      "name": "有声书",
      "icon_url": "https://example.com/icon.png",
      "parent_id": 0,
      "level": 1,
      "children": [
        {
          "category_id": 101,
          "name": "小说",
          "icon_url": "https://example.com/icon.png",
          "parent_id": 1,
          "level": 2
        }
      ]
    }
  ]
}
```

### 使用场景

- 分类导航
- 筛选条件展示
- 分类推荐

## 热门推荐

### 获取热门专辑

**接口地址**: `GET /v1/albums/hot`

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| category_id | Integer | 否 | 分类ID，不传则返回全站热门 |
| limit | Integer | 否 | 返回数量，默认10，最大50 |

**响应示例**:

```json
{
  "ret": 0,
  "msg": "success",
  "data": [
    {
      "album_id": 123456,
      "title": "专辑标题",
      "cover_url": "https://example.com/cover.jpg",
      "announcer_name": "主播名",
      "hot_score": 95.5,
      "rank": 1
    }
  ]
}
```

### 获取推荐专辑

**接口地址**: `GET /v1/albums/recommend`

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| limit | Integer | 否 | 返回数量，默认10 |

**注意**: 此接口需要用户登录，基于用户偏好推荐

### 获取新上架专辑

**接口地址**: `GET /v1/albums/latest`

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| category_id | Integer | 否 | 分类ID |
| limit | Integer | 否 | 返回数量，默认20 |

## 错误码说明

| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| 20001 | 专辑不存在 | 检查album_id是否正确 |
| 20002 | 分类不存在 | 检查category_id是否正确 |
| 20003 | 参数错误 | 检查请求参数格式 |
| 99999 | 系统错误 | 稍后重试或联系客服 |

## 使用示例

### 示例1：获取专辑详情

```bash
# 获取专辑基本信息
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/albums/123456

# 获取专辑详情及前20个声音
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/albums/123456 --params 'include_tracks=true&page=1&limit=20'
```

### 示例2：获取分类下的专辑列表

```bash
# 获取有声书分类的专辑，按热度排序
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/albums --params 'category_id=1&sort=hot&page=1&limit=20'
```

### 示例3：获取分类树

```bash
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/categories
```

### 示例4：获取热门专辑

```bash
# 获取全站热门专辑
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/albums/hot --params 'limit=10'

# 获取有声书分类热门专辑
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/albums/hot --params 'category_id=1&limit=10'
```

## 最佳实践

### 1. 分页加载

当获取专辑列表或声音列表时，建议采用分页加载：

```bash
# 第一页
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/albums --params 'page=1&limit=20'

# 第二页
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/albums --params 'page=2&limit=20'
```

### 2. 按需加载声音列表

专辑详情接口支持可选的声音列表，建议：

- 列表页只获取专辑基本信息（不设置include_tracks）
- 详情页才加载声音列表（设置include_tracks=true）

这样可以减少数据传输量，提升性能。

### 3. 缓存策略

对于不常变化的数据，可以缓存：

- 分类树：缓存24小时
- 热门专辑：缓存1小时
- 专辑详情：缓存10分钟

### 4. 图片优化

专辑返回多个尺寸的封面图：

- `cover_url`: 普通尺寸（建议列表页使用）
- `cover_url_large`: 大尺寸（建议详情页使用）

根据实际需求选择合适的尺寸，节省流量。
