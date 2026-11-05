# AI Code Study 学习导航站优化计划

> 目标：把当前 21 门教程的静态 HTML 站点，改造成像“菜鸟教程”一样能被搜索引擎大规模收录、能带来持续流量的 AI 学习导航站，并逐步接入变现。

---

## 一、现状基线

- **站点形态**：纯静态 HTML（23 个 `.html` 文件），共享 `assets/style.css` 与 `assets/site.js`。
- **内容规模**：21 门教程 + 1 个首页，每篇 5000–8000 字，含代码、速查表、自检清单。
- **已有优势**：垂直赛道清晰、内容深度够、UI 干净、内链/面包屑/搜索已有雏形。
- **主要缺口**：缺 `canonical`/Open Graph/结构化数据/robots/sitemap/404，无流量分析，无变现触点。

---

## 二、分阶段执行计划

### 阶段 1：技术 SEO 基础（1–2 周）
让搜索引擎能正确抓取、理解并展示站点。

| # | 任务 | 交付物 | 验收标准 |
|---|------|--------|----------|
| 1.1 | 统一全站 `<head>` SEO 标签 | 所有 `.html` 更新 | 每页含 `canonical`、Open Graph、Twitter Card、JSON-LD Schema |
| 1.2 | 修复旧版孤立页 | `Kimi-Code-CLI-本地上手指南.html` | 添加 canonical 指向 `kimi-code.html` + 自动跳转 |
| 1.3 | 生成站点地图 | `sitemap.xml` | 包含全部有效页面，格式合法，可提交 Search Console |
| 1.4 | 添加 robots 协议 | `robots.txt` | 允许全部抓取，并指向 sitemap |
| 1.5 | 制作通用 OG 图 | `assets/og.png` | 1200×630，社交分享时显示 |
| 1.6 | 添加 404 页 | `404.html` | 风格一致，带返回首页和热门教程链接 |
| 1.7 | 搜索控制台准备 | 文档记录 | 站长可去 Google/Bing 提交 sitemap |

### 阶段 2：内容矩阵扩张（持续进行）
把“21 门教程”扩展为覆盖大量长尾关键词的“几百页学习导航站”。

| # | 任务 | 示例页面 | 目的 |
|---|------|----------|------|
| 2.1 | 安装/入门页 | `ollama-install.html` | 抢“Ollama 安装”类搜索词 |
| 2.2 | 对比页 | `ai-coding-agents-compare.html` | 抢“Claude Code vs Codex vs Kimi Code”决策型流量 |
| 2.3 | 速查表页 | `langchain-cheatsheet.html` | 收藏回流、长尾覆盖 |
| 2.4 | 学习路线页 | `ai-learning-roadmap.html` | 大词、引流到付费产品 |
| 2.5 | 报错解决页 | `claude-code-401-fix.html` | 高意图、低竞争 |
| 2.6 | 内链模板化 | 所有新/旧页 | 每篇长尾页必须链回核心教程，核心教程链向相关长尾页 |

### 阶段 3：用户体验与留存
把一次性访问变成多次回访。

| # | 任务 | 说明 |
|---|------|------|
| 3.1 | 搜索增强 | 支持内容级搜索、热门搜索提示 |
| 3.2 | 学习进度云同步 | 目前 localStorage，后续可加账号/邮件 |
| 3.3 | 邮件/社群订阅 | 每页底部加“AI 工具周报”订阅框 |
| 3.4 | 最近更新/热门标签 | 首页动态区块 |
| 3.5 | 深色模式/打印样式 | 提升技术读者体验 |

### 阶段 4：变现接入
流量起来后逐步接入。

| # | 任务 | 适用阶段 |
|---|------|----------|
| 4.1 | 联盟链接 | 早期即可接入（阿里云百炼、OpenAI/Claude API、Cursor、云服务器等） |
| 4.2 | 信息流广告 | Google AdSense / 百度联盟，月 UV 过万后接入 |
| 4.3 | 付费收录/推荐位 | 工具导航页成熟后 |
| 4.4 | 付费数字产品 | 速查电子书、项目模板、面试题库 |
| 4.5 | B 端服务 | 企业培训、技术咨询 |

---

## 三、执行记录

| 阶段 | 任务 | 状态 | 备注 |
|------|------|------|------|
| 1.1 | 统一 `<head>` SEO 标签 | ✅ 已完成 | 24 个页面注入 canonical / OG / Twitter Card / JSON-LD |
| 1.2 | 修复旧版孤立页 | ✅ 已完成 | `Kimi-Code-CLI-本地上手指南.html` 已加 canonical + noindex |
| 1.3 | `sitemap.xml` | ✅ 已完成 | 23 个有效 URL，已排除旧版页与 404 页 |
| 1.4 | `robots.txt` | ✅ 已完成 | 允许全站抓取，指向 sitemap |
| 1.5 | `assets/og.png` | ✅ 已完成 | 1200×630 品牌图，已引用到全站 OG/Twitter |
| 1.6 | `404.html` | ✅ 已完成 | 风格一致，含热门教程入口 |
| 1.7 | 搜索控制台准备 | ✅ 已完成 | 直接提交 `sitemap.xml` 即可 |
| 1.8 | 百度统计接入 | ✅ 已完成 | 全站 25 个 HTML 页面已注入百度统计脚本 |
| 1.9 | 独立 JS 配置 | ✅ 已完成 | `assets/config.js` + 统计脚本从配置读取 baiduId |
| 1.10 | 主题切换 | ✅ 已完成 | 深色/浅色/跟随系统，按钮动态注入导航 |
| 1.11 | 联系我们页 | ✅ 已完成 | 新增 `contact.html`，全站导航已加入口 |
| 1.12 | 阅读进度条 | ✅ 已完成 | `assets/site.js` 动态创建，零 HTML 改动 |
| 1.13 | 返回顶部按钮 | ✅ 已完成 | `assets/site.js` 动态创建，滚动 400px 后显示 |
| 1.14 | 面包屑 Schema | ✅ 已完成 | 根据 `nav[aria-label="面包屑"]` 动态生成 JSON-LD |
| 1.15 | 真实域名与 GitHub 配置 | ✅ 已完成 | 域名、联系方式、OG 图、CNAME、Git remote 已更新 |
| 2.2 | 对比页样例 | ✅ 已完成 | 新增 `ai-coding-agents-compare.html`，首页已加入口 |

---

## 四、本次交付物清单

| 文件/目录 | 说明 |
|-----------|------|
| `doc/optimization-plan.md` | 本计划文档 |
| `scripts/apply_seo.py` | 批量注入 SEO / 统计 / 配置脚本，可重复运行 |
| `scripts/generate_sitemap.py` | 自动生成 `sitemap.xml` 脚本 |
| `scripts/generate_og_image.py` | 生成 1200×630 OG 图脚本 |
| `scripts/add_contact_link.py` | 批量为全站导航添加“联系我们”入口 |
| `sitemap.xml` | 站点地图，23 个 URL |
| `robots.txt` | 搜索引擎抓取协议 |
| `404.html` | 404 错误页 |
| `assets/og.png` | 社交分享图（已带真实域名） |
| `assets/config.js` | 全站独立配置文件（站点信息、统计 ID、联系方式、联盟链接） |
| `contact.html` | 联系我们页 |
| `ai-coding-agents-compare.html` | 高价值长尾页样例：编码 Agent 横向对比 |
| `.gitignore` | Git 忽略规则 |
| `CNAME` | GitHub Pages 自定义域名绑定 |
| 全部 `.html` | 已注入 canonical、Open Graph、Twitter Card、Schema.org |

---

## 五、关键配置

- **站点域名**：`https://ai-code-study.chiguashentan.com` 已写入 `scripts/apply_seo.py`、`scripts/generate_sitemap.py`、`scripts/generate_og_image.py`、`assets/config.js`、`robots.txt`、`CNAME`。
- **全站配置入口**：`assets/config.js` 集中管理站点信息、百度统计 ID、联系方式、联盟链接、功能开关。修改后全站（包括统计脚本）自动生效。
- **GitHub 仓库**：`https://github.com/wuxiumu/ai-code-study` 已写入 `assets/config.js`、`contact.html`，本地已 `git init` 并添加 remote。
- **联盟链接占位**：`ai-coding-agents-compare.html` 中的工具推荐区域已预留为内容位，真实运营时可在“推荐组合”“下一步”等区域替换为阿里云百炼、OpenAI、Claude、Cursor、云服务器等联盟链接。

---

## 六、后续建议

1. **立即提交**：去 [Google Search Console](https://search.google.com/search-console) 和 [Bing Webmaster Tools](https://www.bing.com/webmasters) 提交 `sitemap.xml`。
2. **接入分析**：推荐 Plausible 或 Google Analytics 4，跟踪哪些关键词页带来流量。
3. **持续扩内容**：按阶段 2 清单批量生产安装页、对比页、速查表、报错页，目标 3 个月内达到 50+ 页。
4. **变现接入**：流量稳定后，先上联盟链接，再考虑广告和付费产品。
5. **工程升级**：当页面数超过 50 时，建议迁移到 Astro / Hugo / VitePress，用 Markdown + 模板维护，降低后续 SEO 迭代成本。
