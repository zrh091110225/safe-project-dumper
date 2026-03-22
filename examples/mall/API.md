# API 文档

## 接口规范

### 通用响应

```json
{
  "code": 200,
  "message": "操作成功",
  "data": {}
}
```

### 分页响应

```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    "list": [],
    "totalCount": 100,
    "pageNum": 1,
    "pageSize": 10
  }
}
```

## 后台管理 API (mall-admin:8080)

### 1. 权限管理 (Ums)

#### 管理员

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 登录 | POST | /admin/login | 用户登录 |
| 登出 | POST | /admin/logout | 用户登出 |
| 列表 | GET | /admin/list | 管理员列表 |
| 创建 | POST | /admin/create | 创建管理员 |
| 更新 | POST | /admin/update/{id} | 更新管理员 |
| 删除 | DELETE | /admin/delete/{id} | 删除管理员 |

#### 角色

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 列表 | GET | /role/list | 角色列表 |
| 创建 | POST | /role/create | 创建角色 |
| 更新 | POST | /role/update/{id} | 更新角色 |
| 删除 | DELETE | /role/delete/{id} | 删除角色 |
| 分配权限 | POST | /role/updatePermission | 更新角色权限 |

#### 资源

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 列表 | GET | /resource/list | 资源列表 |
| 分类 | GET | /resourceCategory/list | 资源分类列表 |

### 2. 商品管理 (Pms)

#### 品牌

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 列表 | GET | /brand/list | 品牌列表 |
| 创建 | POST | /brand/create | 创建品牌 |
| 更新 | POST | /brand/update/{id} | 更新品牌 |
| 删除 | DELETE | /brand/delete/{id} | 删除品牌 |

#### 商品分类

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 列表 | GET | /productCategory/list | 分类列表 |
| 树形 | GET | /productCategory/listWithTree | 分类树形 |
| 创建 | POST | /productCategory/create | 创建分类 |
| 更新 | POST | /productCategory/update/{id} | 更新分类 |
| 删除 | DELETE | /productCategory/delete/{id} | 删除分类 |

#### 商品属性

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 列表 | GET | /attribute/list | 属性列表 |
| 创建 | POST | /attribute/create | 创建属性 |
| 更新 | POST | /attribute/update/{id} | 更新属性 |
| 删除 | DELETE | /attribute/delete/{id} | 删除属性 |

### 3. 订单管理 (Oms)

#### 订单

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 列表 | GET | /order/list | 订单列表 |
| 详情 | GET | /order/{id} | 订单详情 |
| 发货 | POST | /order/delivery | 发货 |
| 关闭 | POST | /order/close | 关闭订单 |

#### 退款

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 列表 | GET | /returnApply/list | 退款申请列表 |
| 审核 | POST | /returnApply/confirm | 审核退款 |

### 4. 营销管理 (Sms)

#### 优惠券

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 列表 | GET | /coupon/list | 优惠券列表 |
| 创建 | POST | /coupon/create | 创建优惠券 |
| 更新 | POST | /coupon/update/{id} | 更新优惠券 |
| 删除 | DELETE | /coupon/delete/{id} | 删除优惠券 |

#### 秒杀

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 列表 | GET | /flashPromotion/list | 秒杀活动列表 |
| 场次 | GET | /flashSession/list | 秒杀场次 |

### 5. 内容管理 (Cms)

#### 专题

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 列表 | GET | /subject/list | 专题列表 |
| 创建 | POST | /subject/create | 创建专题 |

## 前台商城 API (mall-portal:8085)

### 1. 用户

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 注册 | POST | /member/register | 用户注册 |
| 登录 | POST | /member/login | 用户登录 |
| 登出 | POST | /member/logout | 用户登出 |
| 详情 | GET | /member/info | 用户信息 |

### 2. 商品

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 搜索 | GET | /product/search | 商品搜索 |
| 详情 | GET | /product/{id} | 商品详情 |
| 推荐 | GET | /product/recommend | 推荐商品 |

### 3. 购物车

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 列表 | GET | /cart/list | 购物车列表 |
| 添加 | POST | /cart/add | 添加商品 |
| 更新 | POST | /cart/update | 更新数量 |
| 删除 | DELETE | /cart/{id} | 删除商品 |

### 4. 订单

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 创建 | POST | /order/create | 创建订单 |
| 列表 | GET | /order/list | 订单列表 |
| 详情 | GET | /order/{id} | 订单详情 |
| 取消 | POST | /order/cancel | 取消订单 |

## 搜索服务 API (mall-search:8081)

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 搜索 | GET | /search | 商品搜索 |
| 聚合 | GET | /search/aggregate | 聚合查询 |

## 错误码

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |
