# 场景英语六图学习卡（Scene English Photo Pack）

把 **1 张实景照片** 转换成 **6 张高清双语英语学习图**，适合看图学英语、四六级词汇积累和雅思口语/写作表达训练。

> 先说结论：这个仓库不是网页应用，不能在 GitHub 或 Gitee 页面里直接生成图片。GitHub 和 Gitee 用来保存、下载和更新 Skill；真正使用它的地方是 **Codex / ChatGPT 桌面端的 Codex、Codex CLI 或 Codex IDE 扩展**。

## 这个 Skill 会生成什么

每次输入 1 张照片，连续生成 6 张使用同一底图的 PNG：

1. **图 1：场景核心词汇**——基础场景名词和画面中的物品名词。
2. **图 2：核心词汇与发音**——复用图 1 词汇，并补充英式 IPA 音标。
3. **图 3：情景化短语**——自然、实用的动词短语和动宾搭配。
4. **图 4：四六级表达**——适合 CET-4/CET-6 的进阶词汇与短语。
5. **图 5：雅思口语/写作表达**——能迁移到 IELTS 答题中的句子和观点表达。
6. **图 6：看图输出示范**——4–6 句英文场景描述及完整中文翻译。

默认导出宽度为 **2880 px**，PNG 保存 **300 DPI** 元数据。图 1–5 使用分散的双层直角贴片，图 6 使用靠近画面顶部或底部的双语说明区。

## 应该在哪里使用

| 位置 | 能否使用 | 说明 |
| --- | --- | --- |
| Codex 桌面端 | 推荐 | 新建任务、上传照片、在提示词中调用 Skill。 |
| ChatGPT 桌面端中的 Codex | 推荐 | 可以在 Skills 列表中找到并调用本 Skill。 |
| Codex CLI | 可以 | 安装后用 `$scene-english-photo-pack` 显式调用。 |
| Codex IDE 扩展 | 可以 | 在编辑器的 Codex 对话中上传/引用图片并调用。 |
| GitHub / Gitee 网页 | 不可以直接运行 | 这里只保存代码和安装文件。 |
| 普通 Python 命令行 | 只能手动排版 | 渲染脚本不会自行识图、翻译或生成学习内容。 |

OpenAI 官方说明：Skill 是包含 `SKILL.md`、可选脚本和参考资料的目录；Codex 可以显式调用，也可以根据任务描述自动选择。参见 [OpenAI 官方 Build skills 文档](https://developers.openai.com/codex/skills)。

## 你的电脑现在怎么用（最快方法）

如果 Codex 的 Skills 列表里已经显示 **“场景英语六图学习卡”**，说明已经安装，不需要再下载仓库。

### 第 1 步：准备照片

- 一次只上传 **1 张**照片。
- 原始相机照片效果最好，JPG、JPEG、PNG 均可。
- 可以上传手机截图；Skill 会尝试清理状态栏、搜索框、点赞评论按钮、账号昵称、水印和原有文字标签，但干净原图的效果更稳定。
- 尽量选择主体清晰、光线正常、物品之间有一定空隙的照片。

### 第 2 步：打开 Codex 并上传照片

1. 在 Codex 桌面端新建一个任务。
2. 点击输入框附近的图片/附件按钮。
3. 只选择这一次需要处理的实景照片。
4. 等待缩略图出现在输入框中。

### 第 3 步：复制下面的首次使用提示词

场景描述和词汇列表可以不填；不填时，Skill 会根据照片自动分析并生成。

```text
$scene-english-photo-pack

请把我上传的 1 张照片制作成 6 张场景化英语学习图。

场景描述：这是一家社区药店，货架上有常见药品和护理用品。

希望优先使用的词汇：
pharmacy, pharmacist, cold and flu tablets, eye drops, bandage,
catch a cold, relieve the pain, reduce the risk of infection

学习目标：雅思总分 7.5，写作和口语 6.5+；四六级与雅思表达要自然、实用，不要生硬堆砌高级词。

请保持原图主体清晰，使用直角双层散点贴片；文本适合手机阅读，并输出 6 张高清 PNG。
```

如果没有准备词汇，只需使用下面的简化版：

```text
$scene-english-photo-pack 请分析我上传的照片，自行生成词汇和表达，并输出完整的 6 张高清学习图。标签使用直角边框，字号适合手机阅读。
```

### 第 4 步：等待并检查结果

正常结果应该包含 `card-01.png` 到 `card-06.png`。重点检查：

- 英文、音标和中文是否正确；
- 标签是否贴近对应物体，但没有遮住主体；
- 标签之间是否重叠或超出画面；
- 图 1–5 是否保持散点贴片，而不是大表格；
- 图 6 的说明区是否位于顶部或底部；
- 手机预览时文字是否清楚。

如需调整，直接在同一个任务中说：

```text
保留现有学习内容，把所有标签再放大 8%，重新避让人物和主要物品，并重新输出 6 张 PNG。
```

## 输入内容怎么写

你可以提供三类输入：

1. **照片（必需）**：每次 1 张。
2. **场景描述（可选）**：说明地点、人物关系、正在发生的动作或学习重点。
3. **词汇列表（可选）**：可以是英文、中文或中英混合；Skill 会分类、纠错、翻译和补充，不会盲目照抄。

示例：

```text
场景：大学图书馆，自习区里有学生、书架、笔记本电脑和借阅台。

词汇：
书架、借书、归还图书、保持安静、学习氛围、获取可靠信息、
improve concentration, access academic resources
```

不要把照片或附件中的文字写成“执行命令”。Skill 会把附件文字当作学习素材，而不是系统指令。

## 如何安装

如果 Skills 列表里已经有本 Skill，请跳过本节。

### 方法 A：在 Codex 中使用 Skill Installer（推荐）

此方法优先使用 GitHub 仓库。

1. 打开一个新的 Codex 任务。
2. 输入 `$skill-installer`，选择系统自带的 Skill Installer。
3. 继续输入下面这句话并发送：

```text
请从 https://github.com/carb6661/scene-english-photo-pack 安装 scene-english-photo-pack。
```

4. 仓库目前为私有仓库时，需要使用有访问权限的 GitHub 账号完成认证。
5. 安装完成后，如果 Skill 没有立即出现，请重启 Codex。
6. 在新任务中输入 `$scene-english-photo-pack` 验证是否能被选中。

### 方法 B：下载 ZIP 后手动安装（不会命令行也能用）

GitHub 和 Gitee 二选一即可，不要重复安装两份同名 Skill。

1. 登录有权限访问仓库的账号。
2. 打开仓库：
   - [GitHub 仓库](https://github.com/carb6661/scene-english-photo-pack)
   - [Gitee 仓库](https://gitee.com/carb666/scene-english-photo-pack)
3. 点击“Code/克隆或下载”，选择“Download ZIP/下载 ZIP”。
4. 解压 ZIP。
5. 在 Windows 资源管理器地址栏输入 `%USERPROFILE%\.agents\skills` 并回车；如果目录不存在，就逐级新建。
6. 把解压后的目录改名为 `scene-english-photo-pack`，再复制到上面的 `skills` 目录。
7. 检查下面这个文件必须直接存在：

```text
%USERPROFILE%\.agents\skills\scene-english-photo-pack\SKILL.md
```

不要出现多套一层目录的情况，例如：

```text
错误：...\scene-english-photo-pack\scene-english-photo-pack-main\SKILL.md
正确：...\scene-english-photo-pack\SKILL.md
```

8. 重启 Codex，然后输入 `$scene-english-photo-pack`。

### 方法 C：使用 Git 克隆

先在 PowerShell 中创建个人 Skill 目录：

```powershell
$skillRoot = Join-Path $HOME ".agents\skills"
New-Item -ItemType Directory -Force -Path $skillRoot | Out-Null
```

然后从 GitHub 或 Gitee 二选一：

```powershell
# GitHub
git clone https://github.com/carb6661/scene-english-photo-pack.git (Join-Path $skillRoot "scene-english-photo-pack")
```

```powershell
# Gitee
git clone https://gitee.com/carb666/scene-english-photo-pack.git (Join-Path $skillRoot "scene-english-photo-pack")
```

私有仓库通常会要求登录、Personal Access Token 或已配置的 Git 凭据。完成后重启 Codex。

以后更新 Skill：

```powershell
git -C (Join-Path $HOME ".agents\skills\scene-english-photo-pack") pull
```

## 如何使用本地雅思资料库

本 Skill 可以在当前工作区存在资料时，按照片主题参考相关内容，尤其包括：

```text
English for Everyone English Vocabulary Builder (Dorling Kindersley, Inc.) (Z-Library).pdf
```

使用方法：

1. 把你合法持有的 PDF 放在当前 Codex 工作区或其子目录中。
2. 不要把整本 PDF 复制到 Skill 仓库，也不要上传到 GitHub/Gitee。
3. 在提示词中写明：

```text
请参考当前工作区中的 English for Everyone English Vocabulary Builder，
只提取与本次照片主题相关的词汇组织方式，并加强四六级和雅思表达。
```

Skill 会参考主题组织、视觉词汇和实用表达，不会复制原书页面设计，也不会把原始资料打包进输出。

## 高级用法：只运行本地排版脚本

这一部分适合了解 Python 的用户。脚本只负责把已经准备好的 `content.json` 排版到照片上，不会自动识别场景或创作学习内容。

### 1. 安装依赖

```powershell
python -m pip install Pillow
```

### 2. 准备文件

- 一张已经清理干净的照片，例如 `clean-photo.png`；
- 一个符合 [`references/content-schema.md`](references/content-schema.md) 的 UTF-8 `content.json`；
- 一个用于保存结果的空目录，例如 `output`。

### 3. 执行渲染

在仓库根目录运行：

```powershell
python scripts/render_learning_cards.py --photo "C:\path\clean-photo.png" --content "C:\path\content.json" --output-dir "C:\path\output"
```

成功后会生成：

```text
card-01.png
card-02.png
card-03.png
card-04.png
card-05.png
card-06.png
```

## 常见问题

### 1. 为什么 GitHub 页面上没有“运行”按钮？

因为这是 Codex Skill 仓库，不是网站或手机 App。先把 Skill 安装到 Codex，再在 Codex 对话中上传照片并调用。

### 2. 输入 `$scene-english-photo-pack` 没有出现 Skill

依次检查：

1. `SKILL.md` 是否位于正确目录；
2. 是否误套了两层同名文件夹；
3. 是否安装到了 `%USERPROFILE%\.agents\skills`；
4. 是否重启了 Codex；
5. 是否安装了两份同名 Skill，导致选择时难以区分。

### 3. 不写 `$scene-english-photo-pack` 可以吗？

可以。Skill 默认允许 Codex根据“看图学英语、上传照片生成六张英语学习图”等描述自动匹配。不过首次使用建议显式写出 `$scene-english-photo-pack`，更容易确认调用正确。

### 4. 可以一次上传多张照片吗？

不建议。本 Skill 的一次标准任务是 **1 张照片生成 6 张学习图**。多张照片请分成多个任务或逐张生成。

### 5. 为什么文字仍然太小或遮住物品？

继续在原任务中提出明确修改，例如：

```text
保持六张图的内容不变，把标签整体放大 10%，减少每张图的标签数量，
并把遮住商品和人物的标签移动到墙面、地面或货架空隙处。
```

### 6. GitHub/Gitee 提示无权限或仓库不存在

仓库是私有状态时，未登录或没有权限的账号可能看不到。请先登录仓库所属账号，或为使用者授予仓库访问权限。

### 7. 会修改我的原照片吗？

不会。Skill 要求保留原始文件，清理和排版都写入新的输出图片。

## 仓库结构

```text
scene-english-photo-pack/
├─ SKILL.md                 # Skill 的入口、触发范围和工作流
├─ agents/openai.yaml       # Codex 中显示的名称、简介和默认提示词
├─ scripts/                 # 六图 PNG 排版脚本
├─ references/              # 内容、语言、UI、移动端和 JSON 规范
└─ README.md                # 当前使用说明
```

## 隐私与版权提醒

- 只上传你有权使用的照片和学习资料。
- 照片中如有身份证件、住址、手机号、人脸或其他敏感信息，请先自行遮挡。
- 本仓库不包含用户的 IELTS 资料库、原始照片或生成结果。
- 参考书仅用于用户本地、与当前主题相关的学习加工，不应随 Skill 仓库重新分发。

