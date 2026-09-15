#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HVAC 湿空气计算工具（hvac-psychro-tool）

输入干球温度与相对湿度，计算常用湿空气参数：
- 饱和水蒸气分压力
- 含湿量
- 露点温度（近似）
- 湿空气焓值

优先使用 psychrolib（更精确）；未安装时使用内置近似公式。
"""
from __future__ import annotations

import argparse
import math

# 标准大气压，单位 Pa
STANDARD_PRESSURE = 101325.0

try:
    import psychrolib
    HAS_PSYCHROLIB = True
    psychrolib.SetUnitSystem(psychrolib.SI)
except ImportError:
    HAS_PSYCHROLIB = False


# ---------- 内置近似公式（Magnus 公式等） ----------

def saturation_pressure_magnus(tdb: float) -> float:
    """Magnus 公式计算饱和水蒸气分压力（Pa），tdb 为干球温度（℃）。"""
    return 610.94 * math.exp((17.625 * tdb) / (243.04 + tdb))


def humidity_ratio(tdb: float, rh: float, pressure: float = STANDARD_PRESSURE) -> float:
    """含湿量（kg 水蒸气 / kg 干空气）。"""
    pws = saturation_pressure_magnus(tdb)
    pw = rh / 100.0 * pws
    return 0.621945 * pw / (pressure - pw)


def dew_point(tdb: float, rh: float) -> float:
    """露点温度（℃），由水蒸气分压力反算的近似公式。"""
    pws = saturation_pressure_magnus(tdb)
    pw = rh / 100.0 * pws
    gamma = math.log(pw / 610.94)
    return (243.04 * gamma) / (17.625 - gamma)


def enthalpy(tdb: float, rh: float, pressure: float = STANDARD_PRESSURE) -> float:
    """湿空气比焓（kJ/kg 干空气）。"""
    w = humidity_ratio(tdb, rh, pressure)
    return 1.006 * tdb + w * (2501.0 + 1.86 * tdb)


# ---------- 计算入口（psychrolib 优先） ----------

def calc(tdb: float, rh: float, pressure: float = STANDARD_PRESSURE) -> dict:
    """计算全部参数，返回带说明的键值对。"""
    if HAS_PSYCHROLIB:
        pws = psychrolib.GetSatVapPres(tdb)
        pw = rh / 100.0 * pws
        w = psychrolib.GetHumRatioFromRelHum(tdb, rh / 100.0, pressure)
        tdp = psychrolib.GetTDewPointFromVapPres(pw)
        h = psychrolib.GetMoistAirEnthalpy(tdb, w)
    else:
        pws = saturation_pressure_magnus(tdb)
        pw = rh / 100.0 * pws
        w = humidity_ratio(tdb, rh, pressure)
        tdp = dew_point(tdb, rh)
        h = enthalpy(tdb, rh, pressure)

    return {
        "干球温度 tdb": tdb,
        "相对湿度 RH": rh,
        "饱和水蒸气分压力 Pws (Pa)": round(pws, 2),
        "水蒸气分压力 Pw (Pa)": round(pw, 2),
        "含湿量 d (g/kg)": round(w * 1000.0, 3),
        "露点温度 Tdp (℃)": round(tdp, 2),
        "湿空气焓 h (kJ/kg)": round(h, 3),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="HVAC 湿空气计算工具")
    parser.add_argument("--tdb", type=float, required=True, help="干球温度（℃）")
    parser.add_argument("--rh", type=float, required=True, help="相对湿度（0-100，单位：%%）")
    parser.add_argument("--p", type=float, default=STANDARD_PRESSURE, help="大气压（Pa），默认 101325")
    args = parser.parse_args()

    if not (0 <= args.rh <= 100):
        parser.error("相对湿度必须在 0~100 之间")

    engine = "psychrolib（精确计算）" if HAS_PSYCHROLIB else "内置近似公式（安装 psychrolib 可获得更高精度）"
    print(f"计算引擎：{engine}")
    print("=" * 44)
    for key, value in calc(args.tdb, args.rh, args.p).items():
        print(f"{key:<24} {value}")


if __name__ == "__main__":
    main()
