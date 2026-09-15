# HVAC 湿空气计算工具（hvac-psychro-tool）

一个面向暖通（HVAC）工程师的湿空气参数计算小工具：输入**干球温度**和**相对湿度**，即可输出**含湿量、露点温度、焓值**等常用参数。

本仓库也是作者零基础学习 Python 的实战项目——用自己熟悉的行业知识作为练习题材。

## 功能

- [x] 饱和水蒸气分压力计算
- [x] 含湿量计算
- [x] 露点温度计算（近似）
- [x] 湿空气焓值计算
- [ ] 焓湿图（psychrometric chart）绘制（规划中）
- [ ] 风量 / 冷负荷换算（规划中）

## 快速开始

### 环境要求

- Python 3.9+
- （可选，推荐）安装 [psychrolib](https://github.com/psychrometrics/psychrolib) 以获得更高精度：`pip install psychrolib`

### 运行

```bash
# 方式一：使用内置近似公式（零依赖，开箱即用）
python psychro_calc.py --tdb 26 --rh 60

# 方式二：使用 psychrolib（结果更精确）
pip install psychrolib
python psychro_calc.py --tdb 26 --rh 60
```

示例输出：

```
计算引擎：psychrolib（精确计算）
============================================
干球温度 tdb               26
相对湿度 RH                 60
饱和水蒸气分压力 Pws (Pa)   3360.53
水蒸气分压力 Pw (Pa)        2016.32
含湿量 d (g/kg)             12.665
露点温度 Tdp (℃)            17.76
湿空气焓 h (kJ/kg)          58.255
```

参数说明：

| 参数 | 含义 | 默认值 |
|---|---|---|
| `--tdb` | 干球温度（℃） | 必填 |
| `--rh` | 相对湿度（%，0~100） | 必填 |
| `--p` | 大气压（Pa） | 101325 |

## 学习计划（4 周）

| 周次 | 学习目标 | 练习任务 | 验收标准 |
|---|---|---|---|
| 第 1 周 | Python 基础：变量、类型、函数 | 在 `psychro_calc.py` 中新增计算函数（如湿球温度） | 脚本可运行、结果正确 |
| 第 2 周 | 条件判断、异常处理、命令行参数 | 增加输入校验（如 RH>100 时报错） | 非法输入能被拦截 |
| 第 3 周 | pandas + matplotlib：读数据、画图 | 用一组气象数据绘制温湿度曲线 | 生成一张图表 |
| 第 4 周 | Git 工作流、单元测试 | 补测试用例、完善 README | 测试通过、文档完整 |

## 参考资料

- [psychrolib（湿空气性质计算库）](https://github.com/psychrometrics/psychrolib)
- [廖雪峰 Python 教程](https://www.liaoxuefeng.com/wiki/1016959663602400)
- [菜鸟教程](https://www.runoob.com/python/python-tutorial.html)

## License

MIT
