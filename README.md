# KNN 教材配套习题资源站

教材各章习题的配套数据集、代码骨架与二维码，全部放在这个仓库里，
通过 GitHub Pages 发布为静态站点。

## 目录

```
index.html                  站点首页，列出全部题目
p/4-5/                      习题 4.5 的题目页（二维码指向这里）
  index.html                页面：数据说明、下载、任务、评分点
  train.csv test.csv        数据集
  starter.zip               学生下载的代码包（由 scripts/build.py 生成）
assets/qr/                  二维码源文件（4-5.svg 出书用，4-5.png 排版用）
exercises/ch04/prob-4-5/    题目源目录
  meta.json                 元数据：题号、标题、路径、基线指标
  problem.md                题面（供书稿排版）
  starter/                  代码骨架源文件，会被打包成 p/4-5/starter.zip
  tests/                    自动判分脚本（在 starter 内）
  solution/                 教师版参考答案，不对外发布
scripts/build.py            打包 + 生成二维码 + 检查链接 + 输出清单
config.json                 base_url 等配置
DEPLOY.md                   部署到 GitHub Pages 的步骤
manifest.csv                生成物：每题的 URL、二维码、链接状态
```

## 加一道新题

1. 复制 `exercises/ch04/prob-4-5/`，改 `meta.json`
2. 新建 `p/<id>/`，放数据与页面
3. `python scripts/build.py`
4. 根 `index.html` 加一张卡片
5. 提交推送

## 依赖

生成二维码需要 segno，打包用标准库：

```bash
pip install segno pypng
```

## 习题 4.5 的基线结果

标准化后 5 折交叉验证最优 K=4，测试集 RMSE 1.072、R² 0.534；
不标准化时 R² 仅 0.309。这个差距是本题的核心考点。

数据来源：UCI QSAR aquatic toxicity（ID 505），CC BY 4.0，DOI 10.24432/C5SG7H。
