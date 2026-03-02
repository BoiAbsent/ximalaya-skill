# 搜索API参考文档

## 目录
1. [概述](#概述)
2. [关键词搜索](#关键词搜索)
3. [搜索建议](#搜索建议)
4. [热门搜索词](#热门搜索词)
5. [搜索结果过滤](#搜索结果过滤)

## 概述

搜索API模块提供全文搜索、关键词建议、热门搜索等功能，帮助用户快速找到想要的内容。

### 基础信息

- **Base URL**: `https://api.ximalaya.com`
- **鉴权方式**: OAuth 2.0（部分接口支持匿名访问）
- **请求格式**: JSON
- **响应格式**: JSON

## 关键词搜索

### 接口地址

`GET /v1/search`

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | String | 是 | 搜索关键词 |
| type | String | 否 | 搜索类型: all-全部, album-专辑, track-声音, user-用户，默认all |
| category_id | Integer | 否 | 分类ID，用于过滤分类 |
| page | Integer | 否 | 页码，默认1 |
| limit | Integer | 否 | 每页数量，默认20，最大100 |
| sort | String | 否 | 排序: relevance-相关度, hot-热度, latest-最新，默认relevance |

### 响应示例

```json
{
  "ret": 0,
  "msg": "success",
  "data": {
    "keyword": "关键词",
    "total": 1500,
    "took": 25,
    "page": 1,
    "limit": 20,
    "results": [
      {
        "type": "album",
        "id": 123456,
        "title": "专辑标题",
        "cover_url": "https://example.com/cover.jpg",
        "announcer_name": "主播名",
        "category_name": "有声书",
        "play_count": 1000000,
        "highlight": "专辑<em>关键词</em>介绍"
      },
      {
        "type": "track",
        "id": 456789,
        "title": "声音标题",
        "album_title": "专辑标题",
        "album_id": 123456,
        "duration": 1800,
        "play_count": 10000,
        "highlight": "声音<em>关键词</em>内容"
      }
    ]
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| keyword | String | 搜索关键词 |
| total | Integer | 结果总数 |
| took | Integer | 搜索耗时（毫秒） |
| results | Array | 搜索结果列表 |
| type | String | 结果类型: album/track/user |
| id | Long | 结果ID |
| highlight | String | 高亮显示的匹配文本 |

### 使用场景

- 搜索框搜索
- 发现页推荐
- 内容查找

## 搜索建议

### 接口地址

`GET /v1/search/suggest`

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | String | 是 | 输入关键词 |
| limit | Integer | 否 | 返回数量，默认10，最大20 |

### 响应示例

```json
{
  "ret": 0,
  "msg": "success",
  "data": {
    "keyword": "关键词",
    "suggests": [
      {
        "text": "关键词完整匹配",
        "type": "exact",
        "count": 100
      },
      {
        "text": "关键词相关词1",
        "type": "related",
        "count": 50
      },
      {
        "text": "关键词相关词2",
        "type": "related",
        "count": 30
      }
    ]
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| text | String | 建议文本 |
| type | String | 类型: exact-精确匹配, related-相关词 |
| count | Integer | 匹配结果数量 |

### 使用场景

- 搜索框实时建议
- 搜索引导
- 输入联想

## 热门搜索词

### 接口地址

`GET /v1/search/hot`

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| category_id | Integer | 否 | 分类ID，不传则返回全站热门 |
| limit | Integer | 否 | 返回数量，默认10，最大50 |

### 响应示例

```json
{
  "ret": 0,
  "msg": "success",
  "data": [
    {
      "keyword": "热门词1",
      "rank": 1,
      "hot_value": 10000,
      "trend": "up"
    },
    {
      "keyword": "热门词2",
      "rank": 2,
      "hot_value": 8000,
      "trend": "down"
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| keyword | String | 热门词 |
| rank | Integer | 排名 |
| hot_value | Integer | 热度值 |
| trend | String | 趋势: up-上升, down-下降, stable-稳定 |

### 使用场景

- 首页热门搜索
- 搜索推荐
- 趋势分析

## 搜索结果过滤

### 高级搜索

在关键词搜索的基础上，可以组合更多过滤条件：

#### 按分类过滤

```bash
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/search --params 'keyword=关键词&category_id=1&type=album'
```

#### 按类型过滤

```bash
# 只搜索专辑
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/search --params 'keyword=关键词&type=album'

# 只搜索声音
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/search --params 'keyword=关键词&type=track'

# 只搜索用户
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/search --params 'keyword=关键词&type=user'
```

#### 排序方式

```bash
# 按相关度排序
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/search --params 'keyword=关键词&sort=relevance'

# 按热度排序
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/search --params 'keyword=关键词&sort=hot'

# 按最新排序
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/search --params 'keyword=关键词&sort=latest'
```

## 错误码说明

| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| 40001 | 关键词为空 | 检查keyword参数 |
| 40002 | 关键词过长 | 关键词长度限制100字符 |
| 40003 | 无搜索结果 | 返回空结果列表，提示用户更换关键词 |
| 40004 | 分类不存在 | 检查category_id是否正确 |
| 40005 | 参数错误 | 检查请求参数格式 |
| 99999 | 系统错误 | 稍后重试或联系客服 |

## 使用示例

### 示例1：基本搜索

```bash
# 搜索所有类型
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/search --params 'keyword=关键词&page=1&limit=20'

# 只搜索专辑
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/search --params 'keyword=关键词&type=album&page=1&limit=20'
```

### 示例2：分类搜索

```bash
# 搜索有声书分类下的内容
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/search --params 'keyword=关键词&category_id=1&type=album'
```

### 示例3：搜索建议

```bash
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/search/suggest --params 'keyword=关&limit=10'
```

### 示例4：热门搜索词

```bash
# 获取全站热门搜索词
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/search/hot --params 'limit=10'

# 获取有声书分类热门搜索词
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/search/hot --params 'category_id=1&limit=10'
```

## 最佳实践

### 1. 搜索建议优化

实现实时搜索建议：

```bash
# 用户输入时实时获取建议（防抖处理）
python scripts/ximalaya_api_client.py --method GET --endpoint /v1/search/suggest --params 'keyword=输入内容'
```

建议：
- 输入2个字符后开始触发
- 使用防抖（debounce）避免频繁请求
- 显示建议数量不超过10条

### 2. 搜索结果展示

#### 综合搜索结果

当`type=all`时，结果包含多种类型，建议分组展示：

```json
{
  "albums": [...],  // 专辑结果
  "tracks": [...],  // 声音结果
  "users": [...]    // 用户结果
}
```

#### 高亮显示

使用`highlight`字段突出显示匹配关键词：

```html
专辑<em>关键词</em>介绍
```

### 3. 分页加载

搜索结果支持分页，建议：

- 首次加载20条结果
- 滚动到底部时自动加载下一页
- 缓存已加载的搜索结果

### 4. 搜索历史

维护用户搜索历史（客户端实现）：

- 记录用户搜索关键词
- 支持删除历史记录
- 点击历史记录快速搜索

### 5. 无结果处理

当搜索无结果时：

```json
{
  "ret": 0,
  "msg": "success",
  "data": {
    "total": 0,
    "results": []
  }
}
```

建议：
- 显示"未找到相关结果"
- 提供搜索建议
- 推荐热门内容

### 6. 搜索性能优化

- **缓存热门搜索**: 热门搜索结果缓存5分钟
- **预加载**: 用户输入时预加载可能的搜索词
- **异步搜索**: 搜索请求异步处理，不阻塞UI

## 搜索策略建议

### 用户场景适配

| 场景 | 推荐参数 | 说明 |
|------|----------|------|
| 首次搜索 | type=all, sort=relevance | 综合搜索，按相关度排序 |
| 发现内容 | type=album, sort=hot | 搜索热门专辑 |
| 找具体声音 | type=track, sort=relevance | 精确搜索声音 |
| 找主播 | type=user, sort=hot | 搜索热门主播 |

### 搜索关键词处理

1. **去除特殊字符**: 保留中文、英文、数字
2. **统一大小写**: 英文统一小写
3. **去除空格**: 首尾空格去除，中间连续空格合并
4. **同义词扩展**: 可选功能，扩展同义词搜索

### 搜索排序策略

- **相关度排序**: 优先展示匹配度高、质量好的内容
- **热度排序**: 优先展示热门、受欢迎的内容
- **最新排序**: 优先展示最新发布的内容

根据场景选择合适的排序方式。
