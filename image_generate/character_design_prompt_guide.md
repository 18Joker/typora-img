# 鹅鸭杀角色Logo设计提示词生成指南

## 一、任务概述

为"鹅鸭杀"（Goose Goose Duck）游戏设计角色头像Logo，使用AI图片生成工具批量生成。

---

## 二、输入要求

1. **参考图片文件夹**：提供官方角色参考图（如 `images/duck/` 和 `images/goose/`）
2. **已有设计文件夹**：提供已完成的设计图（如 `final/duck/`）
3. **对比两个文件夹**，找出尚未设计完成的角色

---

## 三、JSON输出格式

每个角色设计6个提示词变体，统一输出为JSON数组：

```json
[
  {
    "task_id": "duck_角色名_v1",
    "type": "text_to_image",
    "prompt": "英文提示词",
    "prompt_zh": "中文提示词",
    "size": "1024x1024",
    "output_path": "image2/duck/duck_角色名_v1.png"
  }
]
```

**字段说明**：
- `task_id`：格式为 `{阵营}_{角色名}_{版本号}`，如 `duck_刺客_v1`
- `type`：固定为 `text_to_image`
- `prompt`：英文提示词，用于AI生成
- `prompt_zh`：中文提示词，用于理解和审核
- `size`：固定为 `1024x1024`
- `output_path`：输出路径，格式为 `image2/{阵营}/{文件名}`

---

## 四、统一风格模板

### 英文模板开头（必填）
```
American retro comic book pop-art style, 1:1 square headshot extreme close-up.
```

### 中文模板开头（必填）
```
美式复古漫画波普风格，1：1正方形头像极近特写。
```

---

## 五、角色设计步骤

### 步骤1：查看官方参考图
- 仔细观察官方素材的**核心元素**（如：武器、服饰、道具、表情）
- 记录角色的**配色方案**和**关键特征**

### 步骤2：确定角色阵营
- **鸭阵营（duck）**：邪恶、狡猾、阴谋、坏笑
- **鹅阵营（goose）**：正义、勇敢、守护、阳光

### 步骤3：设计6个变体
每个角色设计6个不同角度/表情/道具的变体，保持：
- 统一的风格（美式复古漫画波普风格）
- 统一的构图（1:1正方形头像极近特写）
- 统一的背景风格（放射线速度线）

### 步骤4：输出JSON
将6个变体整理为JSON格式，确保结构一致。

---

## 六、踩过的坑（重要！）

### 坑1：风格不统一
**问题**：不同角色的风格差异太大，不像同一系列
**解决**：所有角色必须使用完全相同的开头模板：
```
American retro comic book pop-art style, 1:1 square headshot extreme close-up.
```

### 坑2：敏感内容
**问题**：刀具、血迹等元素可能触发审核
**解决**：
- ❌ 不要使用：blood、bloody、gore、wound
- ❌ 不要使用：real knife、sharp blade
- ✅ 改用：toy knife、plastic blade、rubber sword
- ✅ 描述为：colorful、cartoonish、harmless

### 坑3：表情过于恐怖
**问题**：邪恶表情设计得太过分，引人不适
**解决**：
- 表情控制在"调皮/狡猾/得意"范围
- 避免"恐怖/恶心/血腥"的描述
- 使用词汇：mischievous、devious、sly、cunning、wicked grin（而非menacing、terrifying、grotesque）

### 坑4：忘记参考官方元素
**问题**：设计出的角色与官方形象差距太大
**解决**：
- 必须先查看官方参考图
- 保留角色的**核心识别元素**（如食鸟鸭的烤鸡腿、鸭子的刀具）
- 在prompt中明确描述这些核心元素

### 坑5：圆形边框问题
**问题**：有些角色不需要圆形边框，但设计时加了
**解决**：确认官方素材是否有边框元素，没有则不要添加

### 坑6：角色辨识度低
**问题**：白色鸭子设计得太像"大白鹅"，无法区分
**解决**：为每个角色添加**独特的道具或服饰**（如：厨师帽、围巾、武器、眼镜等）

---

## 七、背景元素词库

### 鸭阵营（邪恶风格）
- 深紫、品红、青柠绿、电紫、霓虹粉
- 速度线、放射线、同心圆环、半调网点
- 暗色调、高对比度

### 鹅阵营（正义风格）
- 天蓝、金色、白色、阳光黄
- 星光、光芒、盾牌元素
- 明亮色调、温暖感

---

## 八、表情词库

### 邪恶/狡猾（鸭阵营）
- mischievous（调皮）
- devious（狡猾）
- sly（诡诈）
- cunning（精明）
- wicked grin（邪恶坏笑）
- scheming（算计）
- plotting（密谋）
- smug（得意）

### 正义/阳光（鹅阵营）
- brave（勇敢）
- confident（自信）
- determined（坚定）
- heroic（英勇）
- cheerful（开朗）
- friendly（友好）

---

## 九、完整示例

### 角色：刺客（鸭阵营）
```json
{
  "task_id": "duck_刺客_v1",
  "type": "text_to_image",
  "prompt": "American retro comic book pop-art style, 1:1 square headshot extreme close-up. A menacing cartoon duck assassin with narrowed cunning eyes, wearing a dark tactical vest. It holds a sleek black silenced pistol close to its face with a cold, confident smirk. Bold black ink outlines, comic-style hatching shadows. High contrast gunmetal grey and deep charcoal lighting from below. Background of dark steel blue and silver radial speed lines, clean composition, no body.",
  "prompt_zh": "美式复古漫画波普风格，1：1正方形头像极近特写。一只威胁性的卡通鸭刺客，眯着狡猾的眼睛，穿着深色战术背心。它将一把光滑的黑色消音手枪举近脸旁，带着冷酷自信的坏笑。粗黑墨水勾边，漫画风格排线阴影。高对比度枪灰色与深炭灰光从下方打亮。背景为深钢蓝与银色放射线速度线，干净构图，无身体。",
  "size": "1024x1024",
  "output_path": "image2/duck/duck_刺客_v1.png"
}
```

---

## 十、工作流程总结

1. **查看官方参考图** → 提取核心元素
2. **确定阵营和风格** → 鸭邪恶/鹅正义
3. **设计6个变体** → 不同表情、道具、角度
4. **检查敏感内容** → 避免血迹、真实武器、恐怖元素
5. **统一JSON格式** → 确保结构一致
6. **检查辨识度** → 每个角色有独特元素，不会混淆
