# mall 电商系统 - 项目概览

## 项目简介

一套完整的电商系统，包括前台商城系统及后台管理系统，基于 Spring Boot + MyBatis 实现。

## 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Spring Boot | 2.7.5 | 框架 |
| MyBatis | 3.5.10 | ORM 框架 |
| MySQL | 8.0+ | 数据库 |
| Druid | 1.2.14 | 连接池 |
| Redis | - | 缓存 |
| Elasticsearch | - | 搜索 |
| RabbitMQ | - | 消息队列 |
| MinIO | - | 对象存储 |
| JWT | 0.9.1 | 认证 |
| Swagger | 3.0.0 | API 文档 |

## 模块架构

```
mall (父项目)
├── mall-common          # 公共模块
├── mall-mbg            # MyBatis Generator 代码生成
├── mall-security       # 安全模块 (Spring Security + JWT)
├── mall-demo           # 示例模块
├── mall-admin          # 后台管理系统 (8080)
├── mall-search         # 搜索模块
└── mall-portal         # 前台商城系统
```

## 核心功能

### 后台管理系统 (mall-admin)

- 商品管理（品牌、分类、属性）
- 订单管理（订单、售后、退款）
- 会员管理（会员、等级）
- 营销管理（优惠券、秒杀、活动）
- 内容管理（专题、公告）
- 权限管理（角色、资源、菜单）

### 前台商城 (mall-portal)

- 用户注册登录
- 商品搜索
- 购物车
- 订单流程
- 会员中心

### 搜索服务 (mall-search)

- Elasticsearch 全文搜索
- 商品搜索
- 聚合查询

## 技术亮点

1. **微服务架构** - 模块化设计
2. **前后端分离** - RESTful API
3. **权限认证** - JWT + Spring Security
4. **Swagger 文档** - API 自动生成
5. **Docker 部署** - 容器化支持

## 快速开始

```bash
# 克隆项目
git clone https://github.com/macrozheng/mall.git

# 导入数据库
# 详见 document/mall.sql

# 运行后台管理系统
cd mall-admin
mvn spring-boot:run

# 运行前台商城
cd mall-portal
mvn spring-boot:run
```

## 端口配置

| 服务 | 端口 |
|------|------|
| mall-admin | 8080 |
| mall-portal | 8085 |
| mall-search | 8081 |
| MySQL | 3306 |
| Redis | 6379 |
| Elasticsearch | 9200 |
| RabbitMQ | 5672 |
| MinIO | 9000 |

## 相关文档

- [架构设计](./ARCHITECTURE.md)
- [API 文档](./API.md)
- [数据库设计](./DATABASE.md)
- [业务流程](./FLOWS.md)
