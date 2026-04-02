#!/usr/bin/env python3
"""
v11 动漫风格测试样片 - 纯Python实现
35秒，1920x1080，动漫风格
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# 配置
OUTPUT_PATH = "/Volumes/WorkData/ctbzai/outputs/v11-anime-sample.mp4"
RESOLUTION = (1920, 1080)
FPS = 30
TOTAL_FRAMES = FPS * 35  # 35秒

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_gradient_background(width, height, color1, color2):
    """创建渐变背景"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    c1 = hex_to_rgb(color1)
    c2 = hex_to_rgb(color2)
    
    for y in range(height):
        ratio = y / height
        r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
        g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
        b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img

def add_speed_lines(img, frame_num, center=None, intensity=0.3):
    """添加漫画速度线效果"""
    draw = ImageDraw.Draw(img, 'RGBA')
    width, height = img.size
    if center is None:
        center = (width // 2, height // 2)
    
    # 速度线参数
    num_lines = 40
    max_radius = max(width, height)
    
    for i in range(num_lines):
        angle = (i / num_lines) * 360 + frame_num * 0.5
        rad = np.radians(angle)
        
        # 动态效果
        speed = 1 + (frame_num % 60) / 30
        
        for r in range(100, max_radius // 2, int(15 * speed)):
            x = int(center[0] + r * np.cos(rad))
            y = int(center[1] + r * np.sin(rad))
            
            if 0 <= x < width and 0 <= y < height:
                alpha = int(100 * intensity * (1 - r / max_radius))
                if alpha > 10:
                    draw.ellipse([x-1, y-1, x+1, y+1], fill=(255, 255, 255, alpha))
    
    return img

def add_concentration_lines(img, frame_num, center=None):
    """添加集中线效果（日本漫画常用）"""
    draw = ImageDraw.Draw(img, 'RGBA')
    width, height = img.size
    if center is None:
        center = (width // 2, height // 2)
    
    # 集中线 - 从中心向外辐射
    num_lines = 60
    pulse = 1 + 0.2 * np.sin(frame_num * 0.1)
    
    for i in range(num_lines):
        angle = (i / num_lines) * 360
        rad = np.radians(angle)
        
        start_r = 50 * pulse
        end_r = max(width, height) // 2
        
        x1 = int(center[0] + start_r * np.cos(rad))
        y1 = int(center[1] + start_r * np.sin(rad))
        x2 = int(center[0] + end_r * np.cos(rad))
        y2 = int(center[1] + end_r * np.sin(rad))
        
        alpha = int(80 + 40 * np.sin(frame_num * 0.05 + i * 0.1))
        draw.line([(x1, y1), (x2, y2)], fill=(255, 255, 255, alpha), width=2)
    
    return img

def draw_text_with_shadow(draw, text, position, font, fill, shadow_color=(255, 140, 66), shadow_offset=(4, 4)):
    """绘制带阴影的文字"""
    x, y = position
    sx, sy = shadow_offset
    # 阴影
    draw.text((x + sx, y + sy), text, font=font, fill=shadow_color)
    # 主文字
    draw.text((x, y), text, font=font, fill=fill)

def create_scene1_frames(output_dir):
    """场景1: 开场Logo (0-8秒)"""
    print("创建场景1: 开场Logo...")
    frames = []
    duration = 8
    
    # 尝试加载字体
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 100)
        font_small = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 40)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    for frame in range(FPS * duration):
        # 深蓝渐变背景
        img = create_gradient_background(RESOLUTION[0], RESOLUTION[1], "1a3775", "0d1b3a")
        
        # 添加速度线效果
        img = add_speed_lines(img, frame, intensity=0.4)
        
        draw = ImageDraw.Draw(img)
        
        # 主标题 - 带弹跳动画
        bounce = 20 * np.sin(frame * 0.1) * np.exp(-frame * 0.02)
        text = "草台班子研究室"
        bbox = draw.textbbox((0, 0), text, font=font_large)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (RESOLUTION[0] - text_w) // 2
        y = (RESOLUTION[1] - text_h) // 2 - 50 + bounce
        
        draw_text_with_shadow(draw, text, (x, y), font_large, (255, 255, 255))
        
        # 副标题 - 延迟1秒出现
        if frame >= FPS:
            text2 = "Grassroots Research Lab"
            bbox2 = draw.textbbox((0, 0), text2, font=font_small)
            text_w2 = bbox2[2] - bbox2[0]
            x2 = (RESOLUTION[0] - text_w2) // 2
            y2 = y + 120
            draw_text_with_shadow(draw, text2, (x2, y2), font_small, (255, 255, 255), shadow_color=(200, 200, 200))
        
        # 淡入淡出
        if frame < 15:  # 0.5秒淡入
            alpha = int(255 * frame / 15)
            overlay = Image.new('RGBA', RESOLUTION, (0, 0, 0, 255 - alpha))
            img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        elif frame > FPS * duration - 15:  # 0.5秒淡出
            fade_frame = FPS * duration - frame
            alpha = int(255 * fade_frame / 15)
            overlay = Image.new('RGBA', RESOLUTION, (0, 0, 0, 255 - alpha))
            img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        
        frames.append(img)
    
    return frames

def create_scene2_frames(output_dir):
    """场景2: 频道定位 (8-18秒)"""
    print("创建场景2: 频道定位...")
    frames = []
    duration = 10
    
    try:
        font_main = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 80)
        font_sub = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 70)
    except:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()
    
    texts = [
        ("财经深度研究", 0, 4, (255, 255, 255)),
        ("数据驱动决策", 3, 7, (100, 200, 255)),
        ("洞察市场趋势", 6, 10, (255, 255, 255))
    ]
    
    for frame in range(FPS * duration):
        # 紫蓝渐变背景
        img = create_gradient_background(RESOLUTION[0], RESOLUTION[1], "2d1e5a", "1a0f3c")
        img = add_concentration_lines(img, frame)
        
        draw = ImageDraw.Draw(img)
        
        t = frame / FPS
        for text, start, end, color in texts:
            if start <= t < end:
                bbox = draw.textbbox((0, 0), text, font=font_main)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]
                x = (RESOLUTION[0] - text_w) // 2
                y = (RESOLUTION[1] - text_h) // 2
                draw_text_with_shadow(draw, text, (x, y), font_main, color)
        
        frames.append(img)
    
    return frames

def create_scene3_frames(output_dir):
    """场景3: 核心价值 (18-30秒)"""
    print("创建场景3: 核心价值...")
    frames = []
    duration = 12
    
    try:
        font_main = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 75)
    except:
        font_main = ImageFont.load_default()
    
    texts = [
        ("严谨研究方法", 0, 4, (255, 255, 255)),
        ("独立客观分析", 4, 8, (255, 100, 100)),
        ("专业投资视角", 8, 12, (255, 255, 255))
    ]
    
    for frame in range(FPS * duration):
        # 深紫渐变背景
        img = create_gradient_background(RESOLUTION[0], RESOLUTION[1], "3c2864", "1f1432")
        img = add_speed_lines(img, frame, intensity=0.3)
        
        draw = ImageDraw.Draw(img)
        
        t = frame / FPS
        for text, start, end, color in texts:
            if start <= t < end:
                bbox = draw.textbbox((0, 0), text, font=font_main)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]
                x = (RESOLUTION[0] - text_w) // 2
                y = (RESOLUTION[1] - text_h) // 2
                draw_text_with_shadow(draw, text, (x, y), font_main, color)
        
        frames.append(img)
    
    return frames

def create_scene4_frames(output_dir):
    """场景4: CTA结尾 (30-35秒)"""
    print("创建场景4: CTA结尾...")
    frames = []
    duration = 5
    
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 120)
        font_small = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 50)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    for frame in range(FPS * duration):
        # 亮橙渐变背景
        img = create_gradient_background(RESOLUTION[0], RESOLUTION[1], "FF6432", "CC3300")
        
        # 强烈集中线效果
        img = add_concentration_lines(img, frame * 2)
        
        draw = ImageDraw.Draw(img)
        
        # 主CTA文字 - 脉冲效果
        pulse = 1 + 0.1 * np.sin(frame * 0.2)
        text = "立即订阅！"
        bbox = draw.textbbox((0, 0), text, font=font_large)
        text_w = int((bbox[2] - bbox[0]) * pulse)
        text_h = int((bbox[3] - bbox[1]) * pulse)
        x = (RESOLUTION[0] - text_w) // 2
        y = (RESOLUTION[1] - text_h) // 2 - 50
        
        draw_text_with_shadow(draw, text, (x, y), font_large, (255, 255, 255), shadow_color=(0, 0, 0))
        
        # 英文副标题
        if frame >= FPS // 2:
            text2 = "SUBSCRIBE NOW"
            bbox2 = draw.textbbox((0, 0), text2, font=font_small)
            text_w2 = bbox2[2] - bbox2[0]
            x2 = (RESOLUTION[0] - text_w2) // 2
            y2 = y + 140
            draw_text_with_shadow(draw, text2, (x2, y2), font_small, (255, 255, 255))
        
        # 淡出效果
        if frame > FPS * duration - 15:
            fade_frame = FPS * duration - frame
            alpha = int(255 * fade_frame / 15)
            overlay = Image.new('RGBA', RESOLUTION, (0, 0, 0, 255 - alpha))
            img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        
        frames.append(img)
    
    return frames

def save_frames_as_video(frames, output_path, fps=30):
    """将帧序列保存为视频"""
    print(f"保存视频到: {output_path}")
    
    # 创建临时帧目录
    temp_dir = "/tmp/v11_frames"
    os.makedirs(temp_dir, exist_ok=True)
    
    # 保存帧为图片
    for i, frame in enumerate(frames):
        frame_path = os.path.join(temp_dir, f"frame_{i:05d}.png")
        frame.save(frame_path)
    
    # 使用ffmpeg合成视频
    cmd = f"ffmpeg -y -framerate {fps} -i {temp_dir}/frame_%05d.png -c:v libx264 -pix_fmt yuv420p -crf 23 '{output_path}'"
    os.system(cmd)
    
    # 清理临时帧
    import shutil
    shutil.rmtree(temp_dir)
    
    print(f"✅ 视频已保存: {output_path}")

def main():
    print("=" * 50)
    print("v11 动漫风格测试样片 - 草台班子研究室")
    print("=" * 50)
    
    # 创建输出目录
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    # 创建所有场景的帧
    all_frames = []
    
    all_frames.extend(create_scene1_frames("/tmp"))
    all_frames.extend(create_scene2_frames("/tmp"))
    all_frames.extend(create_scene3_frames("/tmp"))
    all_frames.extend(create_scene4_frames("/tmp"))
    
    print(f"\n总帧数: {len(all_frames)} (约 {len(all_frames)/FPS:.1f} 秒)")
    
    # 保存视频
    save_frames_as_video(all_frames, OUTPUT_PATH, FPS)
    
    # 验证文件
    if os.path.exists(OUTPUT_PATH):
        size = os.path.getsize(OUTPUT_PATH)
        print(f"✅ 文件大小: {size / 1024 / 1024:.2f} MB")
    else:
        print("❌ 视频创建失败")

if __name__ == "__main__":
    main()
