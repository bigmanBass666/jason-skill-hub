# 软件设计原则详细参考

## 目录

1. [SOLID 原则](#solid-原则)
   - [SRP 单一职责原则](#srp-单一职责原则)
   - [OCP 开闭原则](#ocp-开闭原则)
   - [LSP 里氏替换原则](#lsp-里氏替换原则)
   - [ISP 接口隔离原则](#isp-接口隔离原则)
   - [DIP 依赖倒置原则](#dip-依赖倒置原则)
2. [DRY 家族](#dry-家族)
3. [组合/复用原则](#组合复用原则)
4. [简洁原则](#简洁原则)
5. [其他实用原则](#其他实用原则)

---

## SOLID 原则

### SRP 单一职责原则

**定义**: 一个类/模块应该只有一个引起它变化的原因。

**违反模式 1: God Object**

```python
class UserManager:
    def create_user(self, data): ...
    def send_welcome_email(self, user): ...
    def generate_report(self, user): ...
    def export_to_csv(self, users): ...
    def authenticate(self, username, password): ...
```

变化原因: 用户逻辑变了、邮件模板变了、报告格式变了、导出格式变了、认证方式变了 → 5 个变化原因。

**修复: 按变化原因拆分**

```python
class UserService:
    def create_user(self, data): ...

class EmailService:
    def send_welcome_email(self, user): ...

class ReportService:
    def generate_report(self, user): ...

class ExportService:
    def export_to_csv(self, users): ...

class AuthService:
    def authenticate(self, username, password): ...
```

**违反模式 2: 函数做太多事**

```python
def process_order(order):
    validated = validate_order(order)       # 验证
    priced = calculate_price(validated)     # 计价
    charged = charge_credit_card(priced)    # 支付
    shipped = arrange_shipping(charged)     # 物流
    notified = send_confirmation(shipped)   # 通知
    return notified
```

**修复: 编排者模式**

```python
def process_order(order):
    validated = validator.validate(order)
    priced = pricer.calculate(validated)
    charged = payment_processor.charge(priced)
    shipped = shipping_arranger.arrange(charged)
    notifier.confirm(shipped)
    return shipped
```

`process_order` 变成纯编排者，每个步骤委托给专职模块。

**违反模式 3: 一个模块因为两个不同的使用者而变化**

```python
class Employee:
    def calculate_pay(self): ...      # 财务部门关心
    def report_hours(self): ...       # 项目管理部门关心
    def save(self): ...               # 数据库管理员关心
```

**修复: 按参与者拆分接口/门面**

```python
class PayCalculator:
    def calculate_pay(self, employee): ...

class HourReporter:
    def report_hours(self, employee): ...

class EmployeeRepository:
    def save(self, employee): ...
```

**检测信号**:
- 函数超过 50 行
- 类的 import 超过 10 个
- 类有超过 3 个不同领域的依赖
- 改一个需求要改同一个类的多个不相关方法
- 类名包含 "Manager" / "Handler" / "Util" / "Helper"

---

### OCP 开闭原则

**定义**: 软件实体应该对扩展开放，对修改封闭。新增功能时，应该新增代码，而不是修改已有代码。

**违反模式 1: 类型分发**

```python
def calculate_area(shape):
    if shape.type == "circle":
        return math.pi * shape.radius ** 2
    elif shape.type == "rectangle":
        return shape.width * shape.height
    elif shape.type == "triangle":      # 每加一种形状都要改这里
        return 0.5 * shape.base * shape.height
```

**修复: 多态/策略模式**

```python
class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

class Circle(Shape):
    def area(self) -> float:
        return math.pi * self.radius ** 2

class Rectangle(Shape):
    def area(self) -> float:
        return self.width * self.height

# 新增形状 = 新增类，零改动已有代码
class Triangle(Shape):
    def area(self) -> float:
        return 0.5 * self.base * self.height
```

**违反模式 2: 硬编码映射表**

```python
_PLATFORM_COMPONENTS = {
    "nvidia": {"scraper": "NvidiaScraper", "tester": "NvidiaTester"},
    "zhipu": {"scraper": "ZhipuScraper", "tester": "ZhipuTester"},
    # 每加一个平台都要改这个字典
}
```

**修复: 自描述/注册机制**

```python
# 每个平台在 __init__.py 声明自己的 SPEC
SPEC = {"scraper_cls": "NvidiaScraper", "tester_cls": "NvidiaTester", ...}

# 调度器动态加载，零改动
spec = get_platform_spec(platform)
scraper = create_component(platform, "scraper")
```

**违反模式 3: 回调地狱中的条件分支**

```python
def handle_event(event):
    if event.type == "click":
        ...
    elif event.type == "hover":
        ...
    elif event.type == "keydown":
        ...
```

**修复: 事件映射表/观察者模式**

```python
_handlers = {
    "click": handle_click,
    "hover": handle_hover,
    "keydown": handle_keydown,
}

def handle_event(event):
    handler = _handlers.get(event.type)
    if handler:
        handler(event)
```

**检测信号**:
- `if/elif` 按类型/名称/枚举值分支
- 硬编码的映射字典
- argparse choices 写死列表
- 新增类型时需要修改 switch/case

---

### LSP 里氏替换原则

**定义**: 子类对象必须能够替换其父类对象，而不破坏程序的正确性。

**违反模式 1: 子类抛出父类没有的异常**

```python
class Bird:
    def fly(self) -> float: ...

class Penguin(Bird):
    def fly(self):
        raise NotImplementedError("企鹅不会飞")  # 违反 LSP
```

**修复: 重新设计继承层次**

```python
class Bird: ...
class FlyingBird(Bird):
    def fly(self) -> float: ...
class Penguin(Bird): ...  # 不继承 FlyingBird
```

**违反模式 2: 子类悄悄改变行为语义**

```python
class Rectangle:
    def set_width(self, w): self._w = w
    def set_height(self, h): self._h = h

class Square(Rectangle):
    def set_width(self, w):
        self._w = self._h = w    # 改了宽也改了高，语义变了
    def set_height(self, h):
        self._w = self._h = h
```

**修复: 正方形不是矩形的子类**

```python
class Shape: ...
class Rectangle(Shape): ...
class Square(Shape): ...  # 独立类，不继承 Rectangle
```

**检测信号**:
- 子类方法抛出 `NotImplementedError`
- 子类方法体是 `pass` 或 `raise`
- isinstance 检查后走不同逻辑
- 子类方法的行为语义与父类文档描述不一致

---

### ISP 接口隔离原则

**定义**: 客户端不应该被迫依赖它不使用的方法。

**违反模式: 胖接口**

```python
class Animal(ABC):
    @abstractmethod
    def walk(self): ...
    @abstractmethod
    def swim(self): ...
    @abstractmethod
    def fly(self): ...

class Dog(Animal):
    def walk(self): return "walking"
    def swim(self): return "swimming"
    def fly(self): raise NotImplementedError  # 狗不会飞
```

**修复: 按能力拆分接口**

```python
class Walkable(ABC):
    @abstractmethod
    def walk(self): ...

class Swimmable(ABC):
    @abstractmethod
    def swim(self): ...

class Flyable(ABC):
    @abstractmethod
    def fly(self): ...

class Dog(Walkable, Swimmable):  # 只实现需要的
    def walk(self): return "walking"
    def swim(self): return "swimming"
```

**检测信号**:
- 实现类有空方法或抛 NotImplementedError
- 客户端只调用接口的 2/10 方法
- 接口方法数超过 7 个

---

### DIP 依赖倒置原则

**定义**: 高层模块不应该依赖低层模块，两者都应该依赖抽象。抽象不应该依赖细节，细节应该依赖抽象。

**违反模式: 直接依赖具体类**

```python
class OrderService:
    def __init__(self):
        self.repository = PostgresOrderRepository()  # 硬编码依赖
        self.notifier = EmailNotifier()               # 硬编码依赖

    def create_order(self, data):
        order = self.repository.save(data)
        self.notifier.send(order)
        return order
```

**修复: 依赖注入**

```python
class OrderService:
    def __init__(self, repository: OrderRepository, notifier: Notifier):
        self.repository = repository
        self.notifier = notifier

# 在组合根注入具体实现
service = OrderService(
    repository=PostgresOrderRepository(),
    notifier=EmailNotifier(),
)
```

**违反模式: 在业务代码中 new 对象**

```python
def process_payment(order):
    gateway = StripeGateway(api_key="...")  # 业务逻辑依赖具体支付网关
    gateway.charge(order.total)
```

**修复: 工厂/注册表**

```python
def process_payment(order, gateway: PaymentGateway):
    gateway.charge(order.total)
```

**检测信号**:
- 业务代码中直接 `import` 具体实现类
- `__init__` 中 `self.xxx = ConcreteClass()`
- 测试时必须 mock 整个模块才能隔离

---

## DRY 家族

### DRY — Don't Repeat Yourself

**定义**: 系统中每一项知识都必须有单一、无歧义的权威表示。

**违反模式: 复制粘贴代码**

```python
# user_api.py
def validate_email(email):
    if "@" not in email:
        raise ValueError("Invalid email")

# order_api.py
def validate_email(email):       # 复制粘贴！
    if "@" not in email:
        raise ValueError("Invalid email")
```

**修复: 提取共享模块**

```python
# validators.py
def validate_email(email):
    if "@" not in email:
        raise ValueError("Invalid email")
```

### SSOT — Single Source of Truth

**定义**: 数据只有一个权威来源，其他地方通过引用获取。

**违反模式: 同一数据存在多处**

```python
# platforms.yaml
display_name: "NVIDIA NIM"

# platforms/nvidia/__init__.py
SPEC = {"display_name": "NVIDIA NIM"}  # 重复！改一处忘改另一处
```

**修复: SPEC 只声明 YAML 中没有的字段**

```python
SPEC = {
    "scraper_cls": "NvidiaScraper",   # 只声明 YAML 没有的
    "legacy_mode": True,
    "capabilities": ["reasoning"],
}
# display_name 从 YAML 读取
```

### OAOO — Once And Only Once

**定义**: 逻辑只写一次。比 DRY 更强调"行为"而非"知识"。

与 DRY 的区别: DRY 关注数据/知识的唯一性，OAOO 关注行为逻辑的唯一性。

---

## 组合/复用原则

### Composition over Inheritance — 组合优于继承

**定义**: 优先使用"有"关系（组合）而非"是"关系（继承）来实现代码复用。

**违反模式: 继承层级过深**

```python
class Vehicle: ...
class MotorVehicle(Vehicle): ...
class Car(MotorVehicle): ...
class ElectricCar(Car): ...
class AutonomousElectricCar(ElectricCar): ...  # 5 层继承
```

**修复: 组合/混入**

```python
class Vehicle:
    def __init__(self, powertrain, driver=None):
        self.powertrain = powertrain    # 组合: 电动/燃油
        self.driver = driver            # 组合: 人工/自动驾驶

electric = Vehicle(powertrain=ElectricMotor(), driver=Autopilot())
```

### Law of Demeter — 迪米特法则

**定义**: 一个对象应该对其他对象有最少的了解。只和直接朋友说话，不跟陌生人说话。

**违反模式: 链式调用穿越**

```python
order.customer.address.city    # 穿越了 3 层
department.manager.salary.calculate()  # 穿越了 2 层
```

**修复: 委托方法**

```python
order.get_customer_city()       # Order 委托给 Customer
department.get_manager_salary()  # Department 委托给 Manager
```

**合理例外**: Builder 模式、Fluent API、ORM 查询链不算违反。

---

## 简洁原则

### KISS — Keep It Simple, Stupid

**定义**: 能简单就别复杂。代码复杂度不应超过需求复杂度。

**违反信号**:
- 3 行需求写了 30 行代码
- 用了设计模式但只有 1 个实现
- 抽象层比实现层还复杂

### YAGNI — You Aren't Gonna Need It

**定义**: 别提前写"以后可能用到"的代码。

**违反信号**:
- 接口有方法但只有 1 个实现
- 配置项有 10 个但只用了 3 个
- "先预留着，以后会用到"

---

## 其他实用原则

### Convention over Configuration — 约定优于配置

**定义**: 遵循约定可以减少配置。只有偏离约定时才需要显式配置。

**示例**: `platforms/<name>/__init__.py` 里放 SPEC 就是约定，不需要额外配置文件声明"SPEC 在哪里"。

### Principle of Least Surprise — 最少惊讶原则

**定义**: 系统的行为应该符合用户的直觉预期。

**违反示例**: `-m` 参数接受快捷名称而非完整 ID → 用户传完整 ID 会报错 → 惊讶。

### Separation of Concerns — 关注点分离

**定义**: 不同关注点应该在不同模块中处理。

**经典违反**: MVC 之前，HTML/SQL/业务逻辑全混在一个文件里。
