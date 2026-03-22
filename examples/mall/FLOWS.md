# mall 电商系统 - 业务流程文档

> 本文档记录了 mall 项目所有核心业务流程，包含详细的流程步骤、数据流向和状态机转换，可基于本文档理解业务逻辑或重建相关功能。

---

## 一、核心业务流程总览

### 1.1 业务全景图

```mermaid
graph LR
    subgraph "用户端"
        U1[浏览商品] --> U2[搜索商品]
        U2 --> U3[查看详情]
        U3 --> U4[加入购物车]
        U4 --> U5[提交订单]
        U5 --> U6[支付]
        U6 --> U7[查看物流]
        U7 --> U8[确认收货]
        U8 --> U9[评价]
    end

    subgraph "管理端"
        M1[商品管理] --> M2[订单管理]
        M2 --> M3[会员管理]
        M3 --> M4[营销管理]
        M4 --> M5[内容管理]
    end

    U5 -.-> M2
    U8 -.-> M1
```

### 1.2 核心业务流程清单

| 序号 | 业务流程 | 复杂度 | 涉及模块 |
|------|----------|--------|----------|
| 1 | 用户登录注册 | 低 | ums |
| 2 | 商品浏览与搜索 | 中 | pms, es |
| 3 | 购物车管理 | 中 | cart |
| 4 | 订单创建与支付 | 高 | oms, payment |
| 5 | 订单发货与物流 | 中 | oms |
| 6 | 退货退款 | 高 | oms |
| 7 | 优惠券领取使用 | 中 | sms |
| 8 | 秒杀活动 | 高 | sms |
| 9 | 商品审核 | 低 | pms |
| 10 | 数据统计 | 中 | statistics |

---

## 二、用户模块业务流程

### 2.1 用户登录流程

```mermaid
flowchart TD
    A[用户打开登录页] --> B[输入用户名密码]
    B --> C[点击登录]
    C --> D{验证码通过?}
    D -->|否| E[提示验证码错误]
    E --> B
    D -->|是| F[调用登录接口]
    F --> G{账号密码正确?}
    G -->|否| H[提示用户名或密码错误]
    H --> B
    G -->|是| I[验证JWT Token]
    I --> J[设置Session]
    J --> K[返回登录成功]
    K --> L[跳转首页]
```

**关键接口**：

| 接口 | 方法 | 说明 |
|------|------|------|
| /admin/login | POST | 管理员登录 |
| /admin/logout | POST | 登出 |
| /admin/info | GET | 获取当前用户信息 |

### 2.2 权限校验流程

```mermaid
sequenceDiagram
    participant User
    participant Controller
    participant JwtFilter
    participant Security
    participant Service

    User->>Controller: 访问受保护资源
    Controller->>JwtFilter: 转发请求
    JwtFilter->>JwtFilter: 解析Token
    JwtFilter->>Service: 获取用户权限
    Service-->>JwtFilter: 返回权限列表
    JwtFilter->>Security: 校验权限
    Security-->>Controller: 权限校验通过
    Controller-->>User: 返回数据
```

---

## 三、商品模块业务流程

### 3.1 商品管理流程

```mermaid
flowchart TD
    A[管理员登录] --> B[进入商品管理]
    B --> C[选择商品分类]
    C --> D[管理品牌]
    D --> E[创建商品]
    E --> F[设置商品属性]
    F --> G[设置SKU]
    G --> H[提交审核]
    H --> I{审核通过?}
    I -->|是| J[上架商品]
    I -->|否| K[修改商品]
    K --> H
    J --> L[商品展示]
```

**商品状态流转**：

```mermaid
stateDiagram-v2
    [*] --> 草稿
    草稿 --> 待审核: 提交审核
    待审核 --> 审核通过: 审核通过
    待审核 --> 审核拒绝: 审核拒绝
    审核通过 --> 已上架: 上架
    已上架 --> 已下架: 下架
    已下架 --> 已上架: 上架
    审核拒绝 --> 草稿: 修改
    已上架 --> [*]
    已下架 --> [*]
```

### 3.2 商品搜索流程 (ES)

```mermaid
flowchart TD
    A[用户输入关键词] --> B[调用搜索接口]
    B --> C[构建ES查询]
    C --> D[执行分词]
    D --> E[ES索引查询]
    E --> F{有结果?}
    F -->|是| G[聚合计算]
    F -->|否| H[推荐商品]
    G --> I[排序打分]
    I --> J[返回结果]
    H --> J
    J --> K[前端渲染]
```

**搜索接口**：

| 接口 | 方法 | 说明 |
|------|------|------|
| /search | GET | 关键词搜索 |
| /search/aggregate | GET | 聚合查询 |

---

## 四、购物车业务流程

### 4.1 购物车流程

```mermaid
flowchart LR
    A[商品详情页] --> B[选择SKU]
    B --> C[选择数量]
    C --> D[加入购物车]
    D --> E{库存充足?}
    E -->|否| F[提示库存不足]
    E -->|是| G[购物车页面]
    G --> H[修改数量]
    H --> I{库存足够?}
    I -->|否| J[提示修改数量]
    I -->|是| K[去结算]
```

**购物车接口**：

| 接口 | 方法 | 说明 |
|------|------|------|
| /cart/add | POST | 添加商品 |
| /cart/list | GET | 购物车列表 |
| /cart/update | POST | 修改数量 |
| /cart/delete | DELETE | 删除商品 |

---

## 五、订单业务流程

### 5.1 订单创建流程

```mermaid
flowchart TD
    A[选择商品] --> B[进入结算页]
    B --> C[选择收货地址]
    C --> D[选择配送时间]
    D --> E[选择优惠券]
    E --> F[选择支付方式]
    F --> G[提交订单]
    G --> H{库存充足?}
    H -->|否| I[提示库存不足]
    H -->|是| J[锁定库存]
    J --> K[计算金额]
    K --> L[创建订单]
    L --> M[返回订单号]
```

### 5.2 订单状态流转

```mermaid
stateDiagram-v2
    [*] --> 待付款
    待付款 --> 待发货: 用户支付成功
    待付款 --> 已关闭: 超时/取消
    待发货 --> 待收货: 商家发货
    待收货 --> 已完成: 确认收货
    待收货 --> 售后中: 申请售后
    售后中 --> 已退款: 退款成功
    售后中 --> 待收货: 拒绝退款
    已完成 --> [*]
    已关闭 --> [*]
    已退款 --> [*]
```

### 5.3 订单发货流程

```mermaid
sequenceDiagram
    participant Admin
    participant OrderController
    participant OrderService
    participant OmsOrder
    participant物流

    Admin->>OrderController: 选择订单，点击发货
    OrderController->>OrderService: 传入订单ID和物流信息
    OrderService->>OmsOrder: 更新订单状态为"待收货"
    OmsOrder->>OrderService: 更新成功
    OrderService->>物流: 调用物流API获取运单号
    物流-->>OrderService: 返回运单号
    OrderService->>OmsOrder: 保存物流信息
    OrderService-->>OrderController: 返回成功
    OrderController-->>Admin: 显示发货成功
```

### 5.4 订单接口

| 接口 | 方法 | 说明 |
|------|------|------|
| /order/create | POST | 创建订单 |
| /order/list | GET | 订单列表 |
| /order/{id} | GET | 订单详情 |
| /order/delivery | POST | 发货 |
| /order/close | POST | 关闭订单 |
| /order/cancel | POST | 取消订单 |
| /order/delete | POST | 删除订单 |

---

## 六、退货退款流程

### 6.1 退货流程

```mermaid
flowchart TD
    A[用户申请退货] --> B[填写退货原因]
    B --> C[上传凭证]
    C --> D[提交申请]
    D --> E{商家审核?}
    E -->|拒绝| F[用户申诉/重新申请]
    E -->|通过| G[用户寄回商品]
    G --> H[商家确认收货]
    H --> I{商品完好?}
    I -->|是| J[退款]
    I -->|否| K[拒绝退款]
    J --> L[完成]
    F --> D
```

### 6.2 退款接口

| 接口 | 方法 | 说明 |
|------|------|------|
| /returnApply/list | GET | 退货申请列表 |
| /returnApply/{id} | GET | 退货详情 |
| /returnApply/confirm | POST | 确认收货 |
| /returnApply/reject | POST | 拒绝申请 |

---

## 七、营销模块业务流程

### 7.1 优惠券流程

```mermaid
flowchart TD
    A[用户进入领券中心] --> B[浏览优惠券]
    B --> C[点击领取]
    C --> D{已领取过?}
    D -->|是| E[提示已领取]
    D -->|否| F{达到领取上限?}
    F -->|是| G[提示无法领取]
    F -->|否| H[领取成功]
    H --> I[放入卡包]
    I --> J[下单时使用]
```

### 7.2 秒杀流程

```mermaid
flowchart TD
    A[用户进入秒杀专区] --> B[选择场次]
    B --> C[选择商品]
    C --> D[立即抢购]
    D --> E{是否在秒杀时间?}
    E -->|否| F[提示未开始/已结束]
    E -->|是| G{库存是否充足?}
    G -->|否| H[提示已售罄]
    G -->|是| I[预减库存]
    I --> J[进入排队]
    J --> K{排队成功?}
    K -->|否| L[提示抢购失败]
    K -->|是| M[创建订单]
    M --> N[真正减库存]
```

### 7.3 营销接口

| 接口 | 方法 | 说明 |
|------|------|------|
| /coupon/list | GET | 优惠券列表 |
| /coupon/{id} | GET | 优惠券详情 |
| /coupon/add | POST | 领取优惠券 |
| /flashPromotion/list | GET | 秒杀活动列表 |
| /flashSession/list | GET | 秒杀场次 |

---

## 八、数据同步流程

### 8.1 商品数据同步 (MySQL -> ES)

```mermaid
flowchart TD
    A[商品数据变更] --> B[调用搜索服务]
    B --> C[发送到RabbitMQ]
    C --> D[搜索服务消费消息]
    D --> E[操作ES索引]
    E --> F[ES索引更新成功]
    F --> G[同步完成]
```

### 8.2 库存同步流程

```mermaid
flowchart TD
    A[用户下单] --> B[预减库存]
    B --> C[创建订单]
    C --> D{支付成功?}
    D -->|是| E[真正减库存]
    D -->|否| F[回滚库存]
```

---

## 九、支付流程

### 9.1 支付流程

```mermaid
sequenceDiagram
    participant User
    participant Mall
    participant Payment
    participant Alipay/Wechat

    User->>Mall: 点击支付
    Mall->>Payment: 创建支付订单
    Payment->>Alipay/Wechat: 发起支付请求
    Alipay/Wechat-->>User: 跳转支付页面
    User->>Alipay/Wechat: 完成支付
    Alipay/Wechat-->>Mall: 异步通知支付结果
    Mall->>Mall: 更新订单状态
    Mall-->>User: 支付成功
```

---

## 十、关键业务规则

### 10.1 订单超时规则

| 场景 | 超时时间 | 处理方式 |
|------|----------|----------|
| 待付款 | 30分钟 | 自动关闭，释放库存 |
| 待收货 | 15天 | 自动确认收货 |
| 待评价 | 7天 | 自动好评 |

### 10.2 库存扣减规则

```java
// 伪代码
public boolean deductStock(Long skuId, Integer quantity) {
    // 1. 检查库存
    PmsSkuStock sku = skuDao.selectById(skuId);
    if (sku.getStock() < quantity) {
        return false; // 库存不足
    }

    // 2. 预扣库存 (乐观锁)
    int result = skuDao.deductStock(skuId, quantity);
    return result > 0;
}
```

### 10.3 价格计算规则

```
订单金额 = 商品总价 + 运费 - 优惠(优惠券 + 积分)
实际支付 = 订单金额 - 抵扣(积分)
```

---

## 十一、可逆生成指南

> 基于本文档可以理解业务逻辑并重建相关功能：

1. **按模块开发**：先开发用户模块，再开发商品，最后订单
2. **状态机实现**：每个业务流程都有明确的状态流转，按状态机实现
3. **接口对应**：每个流程都有对应的 Controller 接口，按接口文档实现

**核心开发顺序**：
1. ums（用户模块）→ 权限基础
2. pms（商品模块）→ 核心业务
3. oms（订单模块）→ 交易闭环
4. sms（营销模块）→ 运营能力
