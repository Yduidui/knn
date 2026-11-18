# 习题 4.5 · KNN 回归预测水生急性毒性

本目录是代码骨架，需要你补完 `knn_tox.py` 中四个标记为「待完成」的函数。

## 环境

```bash
pip install -r requirements.txt
```

只需要 numpy 和 pytest，不需要 sklearn。

## 目录

```
knn_tox.py              需要你修改的文件
data/train.csv          训练集 436 条
data/test.csv           测试集 110 条
tests/test_knn_tox.py   自动判分脚本
```

## 运行

```bash
pytest -q
```

10 项测试全绿即完成。其中「端到端预测精度」这一项要求测试集 R² 不低于 0.45，
如果没做标准化，这一项必然失败。

## 直接运行

```bash
python knn_tox.py
```

会打印交叉验证曲线和测试集指标。

## 四个待完成函数

| 函数 | 作用 |
|---|---|
| `fit_scaler` | 求每列均值和标准差（总体标准差，ddof=0） |
| `scale` | 用给定 mean/std 标准化，不修改原数组 |
| `knn_predict` | 对单个样本取 k 个最近邻标签的平均 |
| `select_k` | K 折交叉验证为每个候选 K 估误差，返回最优 K 与曲线 |

## 一个提醒

`select_k` 里标准化只能在每一折的训练部分 fit，再用同一套 mean/std 去处理验证部分。
在划分数据之前就对全量做标准化，会让验证集的信息泄漏进训练，交叉验证结果会偏乐观。
