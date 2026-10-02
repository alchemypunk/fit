# 晨练推拉腿计划

手机端的训练卡片页面：选星期 → 左右滑动看每一步动作（上图下文），底部可切到"说明"看整体方案。

- `index.html`：卡片式手机页面（GitHub Pages 直接打开的就是它）
- `data.js`：动作、图示、训练日数据，两个页面共用
- `plan-full.html`：同一方案的长文版，由 `build.py` 生成，适合在电脑上通读
- `img/`：动作分解照片，来自公有领域的 Free Exercise DB（见 `img/SOURCE.md`）

改完 `index.html` 或 `data.js` 后运行 `python3 build.py` 重新生成长文版。

## 发布到 GitHub Pages

1. 在 GitHub 新建一个仓库（例如 `fit`），把本目录推上去。
2. 仓库 Settings → Pages → Build and deployment → Source 选 **Deploy from a branch**，Branch 选 `main` / `(root)`，保存。
3. 一两分钟后访问 `https://<你的用户名>.github.io/fit/`，手机上打开后可以"添加到主屏幕"。

页面是单文件、无外部依赖，也可以直接用微信或浏览器打开本地的 `index.html`。
