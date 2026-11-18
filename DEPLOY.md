# 部署到 GitHub Pages

整个流程只有一次配置，之后加题只需推文件。

## 一、建仓库

1. 登录 GitHub，新建仓库，**名字尽量短**（推荐 `knn` 或 `book`）。
   名字越短，二维码里的 URL 越短，点阵越稀疏，印刷越好扫。
2. 权限选 **Public**（免费账号的 Pages 只支持公开仓库）。
3. 不要勾选自动生成 README，保持空仓库。

## 二、推送文件

仓库已经初始化并提交，本机也已配好 SSH 密钥（`~/.ssh/id_ed25519_github`），
只需把公钥加到 GitHub 后推送：

```bash
# 首次：把公钥内容粘到 https://github.com/settings/keys
cat ~/.ssh/id_ed25519_github.pub

# 验证连通
ssh -T git@github.com

# 推送
git push -u origin main
```

远程地址用的是 SSH（`git@github.com:Yduidui/knn.git`）。
本机 HTTPS 走代理会被拦，所以不要换回 https 地址。

如果换一台机器，或想用 HTTPS，命令是：

```bash
git remote set-url origin https://github.com/Yduidui/knn.git
git push -u origin main   # 需要 Personal Access Token，不能只用密码
```

## 三、开启 Pages

1. 仓库页 → **Settings** → 左侧 **Pages**
2. Source 选 **Deploy from a branch**
3. Branch 选 **main**，目录选 **/ (root)**，点 Save
4. 等 1–2 分钟，页面顶部会出现访问地址，形如
   `https://Yduidui.github.io/knn/`

仓库根目录里的 `.nojekyll` 是刻意放的，用来关掉 Jekyll 处理，
不要删，否则带下划线的文件可能加载失败。

## 四、回填地址、重新生成二维码

先用浏览器打开 `https://Yduidui.github.io/knn/p/4-5/`，
确认题目页正常、三个下载按钮都能点。

然后改 `config.json` 的第一行：

```json
"base_url": "https://Yduidui.github.io/knn"
```

重新生成：

```bash
python scripts/build.py
```

会覆盖 `assets/qr/4-5.svg` 和 `4-5.png`，同时刷新 `manifest.csv`
里的 URL 和链接状态。此时状态列应显示 `200`。

## 五、插进书稿

- Word 排版用 `assets/qr/4-5.png`，插入宽度设为 **32mm**，居中，不要缩放成正方形以外的比例。
- 出书或需要放大时用 `4-5.svg`，矢量不失真。
- 二维码下面加一行小五号灰字：`扫码获取数据集与代码包　Yduidui.github.io/knn/p/4-5`

## 六、几个必须知道的限制

**国内访问**：GitHub Pages 在国内时通时不通，教育网内通常正常，手机流量不保证。
印刷前一定要用多台手机实测，扫不出来就改用学校域名或对象存储方案。

**URL 长度与印刷尺寸**：`https://Yduidui.github.io/knn/p/4-5/` 是 36 字符，
纠错等级 H 下是 37×37 模块（含静区 45×45）。
32mm 成品对应模块尺寸约 0.71mm，能扫但不算宽裕。
若用户名较长导致 URL 超过 55 字符，把印刷尺寸放大到 35mm。

**链接不能改**：二维码一旦印出去就固定了。所以二维码只指向 `/p/4-5/` 这个目录页，
页面里的文件名、下载方式、说明文字都可以随便改，不用重印。
绝不要二维码直接指向 zip 文件。
