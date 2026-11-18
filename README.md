# KNN 教材配套习题资源站

教材习题的配套数据集、代码骨架与二维码，放在这个仓库里，
通过 GitHub Pages 发布为静态站点。

站点地址：https://Yduidui.github.io/knn/

## 目录

```
index.html                  站点首页
p/4-5/                      习题 4.5 的题目页（二维码指向这里）
  index.html                页面：快速开始、数据说明、任务、评分点
  starter/                  可直接运行的代码目录（clone 后就能用）
    knn_tox.py              需要学生补完的骨架
    data/                   训练集与测试集
    tests/                  自动判分脚本
    requirements.txt
  starter.zip               同样的内容，给没装 git 的人下载
  train.csv test.csv        数据集单独副本
assets/qr/                  二维码源文件（4-5.svg 出书用，4-5.png 排版用）
exercises/ch04/prob-4-5/    题目源目录
  meta.json                 元数据：题号、标题、路径、基线指标
  problem.md                题面（供书稿排版）
  starter/                  代码骨架源文件，构建时同步到 p/4-5/starter/
  solution/                 参考答案
scripts/build.py            同步骨架 + 打包 + 生成二维码 + 检查链接 + 输出清单
config.json                 base_url 等配置
DEPLOY.md                   部署与排版说明
manifest.csv                生成物：每题的 URL、二维码、链接状态
```

## 依赖

生成二维码需要 segno，打包用标准库：

```bash
pip install segno pypng
```

## 习题 4.5 的基线结果

标准化后 5 折交叉验证最优 K=4，测试集 RMSE 1.072、R² 0.534；
不标准化时 R² 仅 0.309。这个差距是本题的核心考点。

数据来源：UCI QSAR aquatic toxicity（ID 505），CC BY 4.0，DOI 10.24432/C5SG7H。
