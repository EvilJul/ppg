# 历史项目库-projects_his



## 表结构

| 字段名                        | 类型         | 说明                                   |
| ----------------------------- | ------------ | -------------------------------------- |
| id                            | BIGINT (PK)  | 项目ID                                 |
| name                          | VARCHAR(200) | 项目名称                               |
| client_name                   | VARCHAR(100) | 客户单位                               |
| project_type                  | VARCHAR(50)  | 类型：医院/写字楼/工厂/学校等          |
| area_sqm                      | NUMERIC      | 建筑面积（㎡）                         |
| location_city                 | VARCHAR(50)  | 所在城市（用于调用气候数据）           |
| total_cooling_load_kw         | NUMERIC      | 总冷负荷                               |
| total_heating_load_kw         | NUMERIC      | 总热负荷                               |
| system_type                   | VARCHAR(100) | 系统类型：多联机/VAV/水系统/地源热泵等 |
| selected_products             | JSONB        | 所选设备列表 [{product_id, qty}, ...]  |
| total_cost_cny                | NUMERIC      | 总成本                                 |
| annual_energy_consumption_kwh | NUMERIC      | 年耗电量                               |
| solution_summary              | TEXT         | 方案摘要（可用于NLP训练）              |
| file_attachments              | JSONB        | 关联文件：["方案.pdf", "图纸.dwg"]     |
| success_rating                | INT          | 客户满意度评分（1-5）                  |
| created_at                    | TIMESTAMP    |                                        |





## sql

```postgresql
create table projects_his(
  id BIGSERIAL primary key ,
  name varchar(200) not null,
  client_name varchar(200) not null,
  project_type varchar(50),
  area_sqm numeric,
  location_city varchar(50),
  total_heating_load_kw numeric,
  total_cooling_load_kw numeric,
  system_type varchar(100),
  selected_products jsonb,
  total_cost_cny numeric,
  annual_energy_consumption_kwh numeric,
  solution_summary text,
  file_attachments jsonb,
  success_rating int,
  create_at timestamp
);
```

