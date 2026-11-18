# -*- coding: utf-8 -*-
"""习题 4.5 参考答案（教师版，不对外发布）

用纯 numpy 实现 KNN 回归，验证题目可解并给出标准答案。
"""
import numpy as np

FEATURES = ["TPSA_Tot", "SAacc", "H_050", "MLOGP", "RDCHI", "GATS1p", "nN", "C_040"]


def load_csv(path):
    d = np.genfromtxt(path, delimiter=",", skip_header=1, encoding="utf-8-sig")
    return d[:, :-1], d[:, -1]


def fit_scaler(X):
    return X.mean(axis=0), X.std(axis=0)


def scale(X, mean, std):
    return (X - mean) / std


def knn_predict(Xtr, ytr, x, k):
    dist = np.sqrt(((Xtr - x) ** 2).sum(axis=1))
    idx = np.argsort(dist)[:k]
    return float(ytr[idx].mean())


def predict(Xtr, ytr, Xte, k, mean=None, std=None):
    if mean is None:
        mean, std = fit_scaler(Xtr)
    Xtr_s, Xte_s = scale(Xtr, mean, std), scale(Xte, mean, std)
    return np.array([knn_predict(Xtr_s, ytr, x, k) for x in Xte_s])


def rmse(y_pred, y_true):
    return float(np.sqrt(((y_pred - y_true) ** 2).mean()))


def r2(y_pred, y_true):
    ss_res = ((y_pred - y_true) ** 2).sum()
    ss_tot = ((y_true - y_true.mean()) ** 2).sum()
    return float(1.0 - ss_res / ss_tot)


def select_k(X, y, ks, folds=5, seed=42):
    """K 折交叉验证选最优 K，返回 (best_k, [(k, rmse), ...])"""
    rng = np.random.RandomState(seed)
    idx = rng.permutation(len(X))
    curve = []
    for k in ks:
        errs = []
        for f in range(folds):
            te = idx[f::folds]
            tr = np.setdiff1d(idx, te)
            pred = predict(X[tr], y[tr], X[te], k)
            errs.append(((pred - y[te]) ** 2).mean() ** 0.5)
        curve.append((k, float(np.mean(errs))))
    best_k = min(curve, key=lambda t: t[1])[0]
    return best_k, curve


if __name__ == "__main__":
    from pathlib import Path

    root = Path(__file__).resolve().parents[4]
    Xtr, ytr = load_csv(root / "p/4-5/train.csv")
    Xte, yte = load_csv(root / "p/4-5/test.csv")

    best_k, curve = select_k(Xtr, ytr, range(1, 16))
    print("交叉验证曲线：")
    for k, e in curve:
        print(f"  K={k:<3} RMSE={e:.3f}")
    print(f"\n最优 K = {best_k}")

    mean, std = fit_scaler(Xtr)
    pred = predict(Xtr, ytr, Xte, best_k, mean, std)
    print(f"测试集 RMSE = {rmse(pred, yte):.3f}  R2 = {r2(pred, yte):.3f}")

    raw = np.array([knn_predict(Xtr, ytr, x, best_k) for x in Xte])
    print(f"（对照）不标准化 RMSE = {rmse(raw, yte):.3f}  R2 = {r2(raw, yte):.3f}")
