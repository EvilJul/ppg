# 产品资料库-productes



## 数据表结构

```text
| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | BIGINT (PK) | 产品唯一ID |
| name | VARCHAR(200) | 产品名称，如“螺杆式冷水机组 MWPS-F1000” |
| category | VARCHAR(50) | 分类：主机/水泵/冷却塔/风机盘管/空气处理机组等 |
| brand | VARCHAR(50) | 品牌 |
| model_code | VARCHAR(100) | 型号编码（用于ERP对接） |
| cooling_capacity_kw | NUMERIC | 制冷量（kW） |
| heating_capacity_kw | NUMERIC | 制热量（kW） |
| power_kw | NUMERIC | 输入功率 |
| cop | NUMERIC | 能效比 |
| noise_db | NUMERIC | 噪音值（dB） |
| dimensions | JSONB | 外形尺寸 {length, width, height} |
| price_cny | NUMERIC | 当前单价（人民币） |
| energy_level | INT | 能效等级（1-5级） |
| tags | JSONB | 标签：["变频", "磁悬浮", "低温热泵"] |
| documentation_link | TEXT | 使用手册/PDF链接 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |
```



## Postgre SQL 建表

```postgresql
create database ppg_test;

create table products(
  id bigint(PK),
  name varchar(200),
  category varchar(50),
  mode_cope varchar(50),
  cooling_capacity_kw numeric,
  heating_capacity_kw numeric,
  power_km numeric,
  cop numeric,
  noise_db numeric,
  dimensions jsonb,
  price_cny numeric,
  energy_level int,
  created_at timestamp,
  updated_at timestamp
);
```

