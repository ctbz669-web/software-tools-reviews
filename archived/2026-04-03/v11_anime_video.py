#!/usr/bin/env python3
"""
v11 动漫风格测试样片 - 草台班子研究室频道介绍
35秒，16:9，动漫/漫画风格
"""

from moviepy.editor import *
from moviepy.video.fx.all import resize, fadein, fadeout
import numpy as np

# 配置
OUTPUT_PATH = "/Volumes/WorkData/ctbzai/outputs/v11-anime-sample.mp4"
RESOLUTION = (1920, 1080)
FPS = 30
TOTAL_DURATION = 35

# 使用渐变色彩背景创建动漫风格场景
def create_anime_scene(duration, color_scheme, scene_name):
    """创建动漫风格的场景背景"""
    
    # 基于场景类型选择颜色
    if color_scheme == "logo":
        base_color = (25, 55, 109)  # 深蓝
        accent_color = (255, 140, 66)  # 橙色
    elif color_scheme == "finance":
        base_color = (45, 30, 90)  # 紫蓝
        accent_color = (100, 200, 255)  # 亮蓝
    elif color_scheme == "data":
        base_color = (20, 30, 60)  # 深黑蓝
        accent_color = (255, 180, 80)  # 金黄
    elif color_scheme == "value":
        base_color = (60, 40, 100)  # 深紫
        accent_color = (255, 100, 100)  # 红橙
    else:  # cta
        base_color = (255, 100, 50)  # 亮橙
        accent_color = (255, 255, 255)  # 白
    
    # 创建基础背景
    bg = ColorClip(size=RESOLUTION, color=base_color).set_duration(duration)
    
    # 添加动态速度线效果 (speed lines)
    def make_speed_lines(t):
        """生成漫画速度线效果"""
        frame = np.zeros((RESOLUTION[1], RESOLUTION[0], 3), dtype=np.uint8)
        frame[:, :] = base_color
        
        center_x, center_y = RESOLUTION[0] // 2, RESOLUTION[1] // 2
        
        # 动态速度线
        speed = 3 + int(t * 2)
        for angle in range(0, 360, 10):
            rad = np.radians(angle + t * 20)
            for r in range(50, max(RESOLUTION) // 2, speed * 3):
                x = int(center_x + r * np.cos(rad))
                y = int(center_y + r * np.sin(rad))
                if 0 <= x < RESOLUTION[0] and 0 <= y < RESOLUTION[1]:
                    intensity = max(0, 1 - r / (max(RESOLUTION) // 2))
                    for i in range(2):
                        if 0 <= x + i < RESOLUTION[0] and 0 <= y + i < RESOLUTION[1]:
                            frame[y + i, x + i] = tuple(min(255, int(c + intensity * 100)) for c in accent_color)
        
        return frame
    
    speed_lines = VideoClip(make_speed_lines, duration=duration)
    
    # 合并背景
    scene = CompositeVideoClip([bg, speed_lines.set_opacity(0.4)], size=RESOLUTION)
    
    return scene

# 创建文字标题
def create_title_clip(text, duration, start_time, position="center", fontsize=80):
    """创建动漫风格的标题文字"""
    txt_clip = TextClip(
        text,
        fontsize=fontsize,
        color="white",
        font="Arial-Bold",
        stroke_color="black",
        stroke_width=3,
        method="caption",
        size=(RESOLUTION[0] - 200, None),
        align="center"
    ).set_duration(duration).set_start(start_time)
    
    # 添加动漫风格的阴影效果
    shadow = TextClip(
        text,
        fontsize=fontsize,
        color=hex_to_rgb("#FF8C42"),  # 橙色阴影
        font="Arial-Bold",
        method="caption",
        size=(RESOLUTION[0] - 200, None),
        align="center"
    ).set_duration(duration).set_start(start_time).set_position((position[0]+4, position[1]+4) if isinstance(position, tuple) else lambda t: (position(t)[0]+4, position(t)[1]+4) if callable(position) else (4, 4))
    
    # 弹跳动画效果
    def bounce_pos(t):
        y_offset = 20 * np.sin(t * 3) * np.exp(-t * 2)
        if position == "center":
            return (RESOLUTION[0]/2 - txt_clip.w/2, RESOLUTION[1]/2 - txt_clip.h/2 + y_offset)
        return position
    
    txt_clip = txt_clip.set_position(bounce_pos)
    shadow = shadow.set_position(lambda t: (bounce_pos(t)[0]+4, bounce_pos(t)[1]+4))
    
    return shadow, txt_clip

def hex_to_rgb(hex_color):
    """十六进制颜色转RGB元组"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# 场景1: 开场Logo (0-8秒)
scene1_duration = 8
scene1 = create_anime_scene(scene1_duration, "logo", "开场")

# Logo文字
logo_shadow, logo_text = create_title_clip(
    "草台班子研究室",
    scene1_duration,
    0,
    fontsize=100
)
logo_shadow2, logo_sub = create_title_clip(
    "Grassroots Research Lab",
    scene1_duration - 1,
    1,
    position=lambda t: (RESOLUTION[0]/2 - 300, RESOLUTION[1]/2 + 80),
    fontsize=40
)

scene1_final = CompositeVideoClip([
    scene1,
    logo_shadow.set_opacity(0.6),
    logo_text,
    logo_shadow2.set_opacity(0.5),
    logo_sub
], size=RESOLUTION).fadein(0.5)

# 场景2: 频道定位 (8-18秒)
scene2_duration = 10
scene2 = create_anime_scene(scene2_duration, "finance", "财经定位")

s2_shadow1, s2_text1 = create_title_clip(
    "财经深度研究",
    4,
    0,
    fontsize=80
)
s2_shadow2, s2_text2 = create_title_clip(
    "数据驱动决策",
    4,
    3,
    fontsize=70
)
s2_shadow3, s2_text3 = create_title_clip(
    "洞察市场趋势",
    3,
    6,
    fontsize=70
)

scene2_final = CompositeVideoClip([
    scene2,
    s2_shadow1.set_opacity(0.6),
    s2_text1,
    s2_shadow2.set_opacity(0.6),
    s2_text2,
    s2_shadow3.set_opacity(0.6),
    s2_text3
], size=RESOLUTION)

# 场景3: 核心价值 (18-30秒)
scene3_duration = 12
scene3 = create_anime_scene(scene3_duration, "value", "核心价值")

s3_shadow1, s3_text1 = create_title_clip(
    "严谨研究方法",
    4,
    0,
    fontsize=75
)
s3_shadow2, s3_text2 = create_title_clip(
    "独立客观分析",
    4,
    4,
    fontsize=75
)
s3_shadow3, s3_text3 = create_title_clip(
    "专业投资视角",
    4,
    8,
    fontsize=75
)

scene3_final = CompositeVideoClip([
    scene3,
    s3_shadow1.set_opacity(0.6),
    s3_text1,
    s3_shadow2.set_opacity(0.6),
    s3_text2,
    s3_shadow3.set_opacity(0.6),
    s3_text3
], size=RESOLUTION)

# 场景4: CTA结尾 (30-35秒)
scene4_duration = 5
scene4 = create_anime_scene(scene4_duration, "cta", "CTA")

cta_shadow, cta_text = create_title_clip(
    "立即订阅！",
    scene4_duration,
    0,
    fontsize=120
)
cta_shadow2, cta_sub = create_title_clip(
    "SUBSCRIBE NOW",
    scene4_duration - 0.5,
    0.5,
    position=lambda t: (RESOLUTION[0]/2 - 200, RESOLUTION[1]/2 + 100),
    fontsize=50
)

scene4_final = CompositeVideoClip([
    scene4,
    cta_shadow.set_opacity(0.7),
    cta_text,
    cta_shadow2.set_opacity(0.6),
    cta_sub
], size=RESOLUTION).fadeout(0.5)

# 拼接所有场景
final_video = concatenate_videoclips([
    scene1_final,
    scene2_final,
    scene3_final,
    scene4_final
], method="compose")

print(f"视频创建完成，总时长: {final_video.duration}秒")
print(f"输出路径: {OUTPUT_PATH}")

# 导出视频（无声版本，等待配音）
final_video.write_videofile(
    "/tmp/v11_base.mp4",
    fps=FPS,
    codec="libx264",
    audio=False,
    preset="fast",
    threads=4
)

print("基础视频已导出到: /tmp/v11_base.mp4")
