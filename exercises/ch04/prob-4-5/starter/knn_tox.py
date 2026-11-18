# -*- coding: utf-8 -*-
"""习题 4.5 · KNN 回归：预测有机污染物对大型溞的急性毒性

使用说明
--------
1. 只允许使用 numpy，不要调用 sklearn（本题考的是原理，不是调包）
2. 需要你补完四个函数：fit_scaler / scale / knn_predict / select_k
3. 补完后在题目目录下运行 `pytest -q` 自测

数据字段
--------
前 8 列是分子描述符，最后一列 LC50 = -log(mmol/L)，值越大毒性越强。
"""
import numpy as np

FEATURES = ["TPSA_Tot", "SAacc", "H_050", "MLOGP", "RDCHI", "GATS1p", "nN", "C_040"]


def load_csv(path):
    """读取 CSV，返回 (X, y)。已给出。"""
    d = np.genfromtxt(path, delimiter=",", skip_header=1, encoding="utf-8-sig")
    return d[:, :-1], d[:, -1]


# ---------------------------------------------------------------- 待完成 1
def fit_scaler(X):
    """计算每一列的均值和标准差。

    参数
    ----
    X : ndarray, shape (n_samples, n_features)

    返回
    ----
    (mean, std) : 两个 shape 均为 (n_features,) 的数组
    std 使用总体标准差（ddof=0）
    """
    raise NotImplementedError("请实现 fit_scaler")


# ---------------------------------------------------------------- 待完成 2
def scale(X, mean, std):
    """用给定的 mean / std 对 X 做标准化，返回新数组，不修改原数组。"""
    raise NotImplementedError("请实现 scale")


# ---------------------------------------------------------------- 待完成 3
def knn_predict(X_train, y_train, x, k):
    """对单个样本 x 做 KNN 回归预测。

    参数
    ----
    X_train : 已标准化的训练特征, shape (n, d)
    y_train : 训练标签, shape (n,)
    x       : 单个待测样本, shape (d,)
    k       : 近邻个数

    返回
    ----
    float : k 个最近邻标签的算术平均

    提示：欧氏距离 = sqrt(sum((X_train - x)^2))，可用 np.argsort 取前 k 个。
    """
    raise NotImplementedError("请实现 knn_predict")


# ---------------------------------------------------------------- 待完成 4
def select_k(X, y, ks, folds=5, seed=42):
    """用 K 折交叉验证为每个候选 K 估计误差，返回最优 K 与曲线。

    参数
    ----
    X, y : 未标准化的全量训练数据
    ks   : 候选 K 值列表，例如 range(1, 16)

    返回
    ----
    (best_k, curve)
      best_k : 交叉验证 RMSE 最小的 K
      curve  : [(k, rmse), ...]，顺序与 ks 一致

    注意：标准化只能在每一折的训练部分上 fit，再用同一个 mean/std 去 transform 验证部分，
    否则会造成信息泄漏。
    """
    raise NotImplementedError("请实现 select_k")


# ---------------------------------------------------------------- 工具函数（已给出）
def rmse(y_pred, y_true):
    return float(np.sqrt(((y_pred - y_true) ** 2).mean()))


def r2(y_pred, y_true):
    ss_res = ((y_pred - y_true) ** 2).sum()
    ss_tot = ((y_true - y_true.mean()) ** 2).sum()
    return float(1.0 - ss_res / ss_tot)


def predict_all(X_train, y_train, X_test, k, mean, std):
    """批量预测，已给出。"""
    Xtr = scale(X_train, mean, std)
    Xte = scale(X_test, mean, std)
    return np.array([knn_predict(Xtr, y_train, x, k) for x in Xte])


if __name__ == "__main__":
    Xtr, ytr = load_csv("data/train.csv")
    Xte, yte = load_csv("data/test.csv")

    best_k, curve = select_k(Xtr, ytr, range(1, 16))
    print("K   RMSE")
    for k, e in curve:
        print(f"{k:<3} {e:.3f}")
    print(f"\n最优 K = {best_k}")

    mean, std = fit_scaler(Xtr)
    pred = predict_all(Xtr, ytr, Xte, best_k, mean, std)
    print(f"测试集 RMSE = {rmse(pred, yte):.3f}  R2 = {r2(pred, yte):.3f}")
