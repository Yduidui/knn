# -*- coding: utf-8 -*-
"""习题 4.5 自动判分（学生自测用）

在题目目录下运行：
    pip install -r requirements.txt
    pytest -q

全部通过说明实现正确；任何一项失败会指出具体问题。
"""
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import knn_tox as m  # noqa: E402


# ------------------------------------------------------------------ 数据读取
def test_数据规模():
    Xtr, ytr = m.load_csv(str(ROOT / "data/train.csv"))
    Xte, yte = m.load_csv(str(ROOT / "data/test.csv"))
    assert Xtr.shape == (436, 8), f"训练集特征形状应为 (436, 8)，实际 {Xtr.shape}"
    assert ytr.shape == (436,), f"训练集标签形状应为 (436,)，实际 {ytr.shape}"
    assert Xte.shape == (110, 8)


# ------------------------------------------------------------------ 标准化
def test_标准化器参数():
    Xtr, _ = m.load_csv(str(ROOT / "data/train.csv"))
    mean, std = m.fit_scaler(Xtr)
    assert mean.shape == (8,) and std.shape == (8,)
    assert mean[0] == pytest.approx(47.2357, abs=0.01), "第一列均值不对"
    assert mean[1] == pytest.approx(56.1343, abs=0.01), "第二列均值不对"
    assert std[0] == pytest.approx(46.8811, abs=0.01), "第一列标准差不对，注意用总体标准差 ddof=0"
    assert std[1] == pytest.approx(66.0250, abs=0.01), "第二列标准差不对"
    assert np.all(std > 0), "标准差不应为 0"


def test_标准化后零均值单位方差():
    Xtr, _ = m.load_csv(str(ROOT / "data/train.csv"))
    mean, std = m.fit_scaler(Xtr)
    Xs = m.scale(Xtr, mean, std)
    assert Xs.shape == Xtr.shape
    assert np.allclose(Xs.mean(axis=0), 0, atol=1e-8), "标准化后各列均值应为 0"
    assert np.allclose(Xs.std(axis=0), 1, atol=1e-8), "标准化后各列标准差应为 1"


def test_标准化不修改原数组():
    Xtr, _ = m.load_csv(str(ROOT / "data/train.csv"))
    mean, std = m.fit_scaler(Xtr)
    before = Xtr.copy()
    m.scale(Xtr, mean, std)
    assert np.allclose(Xtr, before), "scale 不应修改传入的数组"


# ------------------------------------------------------------------ 预测
def test_knn_近邻为1时取最近点():
    Xtr = np.array([[0.0, 0.0], [1.0, 0.0], [10.0, 10.0]])
    ytr = np.array([1.0, 2.0, 3.0])
    assert m.knn_predict(Xtr, ytr, np.array([0.1, 0.0]), 1) == pytest.approx(1.0)
    assert m.knn_predict(Xtr, ytr, np.array([9.0, 9.0]), 1) == pytest.approx(3.0)


def test_knn_近邻为3时取平均():
    Xtr = np.array([[0.0, 0.0], [1.0, 0.0], [2.0, 0.0], [100.0, 0.0]])
    ytr = np.array([1.0, 2.0, 4.0, 100.0])
    assert m.knn_predict(Xtr, ytr, np.array([0.5, 0.0]), 3) == pytest.approx(7.0 / 3)


def test_knn_返回浮点数():
    Xtr = np.array([[0.0], [1.0]])
    ytr = np.array([1.0, 3.0])
    out = m.knn_predict(Xtr, ytr, np.array([0.4]), 1)
    assert isinstance(out, float), "应返回 float 而不是数组"


# ------------------------------------------------------------------ 指标
def test_指标函数():
    pred = np.array([1.0, 2.0, 3.0])
    true = np.array([1.0, 2.0, 3.0])
    assert m.rmse(pred, true) == pytest.approx(0.0)
    assert m.r2(pred, true) == pytest.approx(1.0)

    pred = np.array([1.0, 2.0, 4.0])
    true = np.array([1.0, 2.0, 3.0])
    assert m.rmse(pred, true) == pytest.approx(np.sqrt(1 / 3))
    assert m.r2(pred, true) == pytest.approx(0.5)


# ------------------------------------------------------------------ 选 K
def test_选择K返回结构():
    Xtr, ytr = m.load_csv(str(ROOT / "data/train.csv"))
    Xtr, ytr = Xtr[:120], ytr[:120]
    best_k, curve = m.select_k(Xtr, ytr, [1, 3, 5], folds=3)
    assert isinstance(best_k, (int, np.integer))
    assert best_k in (1, 3, 5)
    assert len(curve) == 3
    for k, e in curve:
        assert isinstance(e, (float, np.floating))
        assert e > 0
    best = min(curve, key=lambda t: t[1])[1]
    assert min(e for _, e in curve) == pytest.approx(best)


# ------------------------------------------------------------------ 端到端（核心判分）
def test_端到端预测精度():
    """标准化后 K=4 在测试集上的 R2 应不低于 0.45。

    未做标准化时 R2 只有约 0.31，会在这里失败。
    """
    Xtr, ytr = m.load_csv(str(ROOT / "data/train.csv"))
    Xte, yte = m.load_csv(str(ROOT / "data/test.csv"))

    mean, std = m.fit_scaler(Xtr)
    pred = m.predict_all(Xtr, ytr, Xte, 4, mean, std)
    score = m.r2(pred, yte)

    assert score >= 0.45, (
        f"测试集 R2 = {score:.3f}，低于 0.45。"
        "最常见原因是训练集与测试集没有使用同一套 mean/std 标准化，"
        "或距离计算前忘了 scale。"
    )
    assert score <= 0.95, f"测试集 R2 = {score:.3f} 高得异常，请检查是否把测试集标签泄漏进了训练"
