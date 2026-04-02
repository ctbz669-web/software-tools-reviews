from moviepy.editor import *
from moviepy.video.fx.all import resize
import numpy as np

# 配置
OUTPUT_PATH = "/Volumes/WorkData/ctbzai/outputs/v11-anime-sample.mp4"
RESOLUTION = (1920, 1080)
FPS = 30

# 加载图片（使用生成的动漫图片）
# 实际路径需要根据生成的图片位置调整
img_files = [
    "/Users/kevin/.openclaw/workspace/media/v11_anime_logo.png",
    "/Users/kevin/.openclaw/workspace/media/v11_anime_finance.png", 
    "/Users/kevin/.openclaw/workspace/media/v11_anime_data.png",
    "/Users/kevin/.openclaw/workspace/media/v11_anime_team.png",
    "/Users/kevin/.openclaw/workspace/media/v11_anime_cta.png"
]

# 场景时长配置
scenes = [
    {"img": img_files[0], "duration": 8, "name": "开场Logo"},
    {"img": img_files[1], "duration": 10, "name": "频道定位"},
    {"img": img_files[2], "duration": 6, "name": "数据可视化过渡"},
    {"img": img_files[3], "duration": 6, "name": "核心价值"},
    {"img": img_files[4], "duration": 5, "name": "结尾CTA"}
]

def create_ken_burns_clip(image_path, duration, zoom_direction="in"):
    """创建Ken Burns效果的视频片段"""
    img = ImageClip(image_path)
    
    # 确保图片填满画面并裁剪
    img_resized = img.resize(height=RESOLUTION[1]*1.3)  # 放大30%用于移动空间
    
    if zoom_direction == "in":
        # 从稍远推近
        def scale(t):
            return 1.0 + 0.15 * (t / duration)
        def pos(t):
            x = RESOLUTION[0]/2
            y = RESOLUTION[1]/2 + 20 * np.sin(t * 0.5)
            return (x, y)
    elif zoom_direction == "out":
        # 从近拉远
        def scale(t):
            return 1.15 - 0.15 * (t / duration)
        def pos(t):
            x = RESOLUTION[0]/2
            y = RESOLUTION[1]/2
            return (x, y)
    else:  # pan
        # 平移效果
        def scale(t):
            return 1.05
        def pos(t):
            x = RESOLUTION[0]/2 - 50 * np.sin(t * 0.3)
            y = RESOLUTION[1]/2
            return (x, y)
    
    clip = img_resized.set_duration(duration)
    clip = clip.resize(lambda t: scale(t))
    clip = clip.set_position(lambda t: pos(t))
    clip = clip.set_duration(duration)
    
    # 居中并裁剪到目标分辨率
    final = CompositeVideoClip([
        ColorClip(size=RESOLUTION, color=(0,0,0)).set_duration(duration),
        clip
    ], size=RESOLUTION)
    
    return final

def add_speed_lines(frame, intensity=0.3):
    """添加漫画速度线效果"""
    # 简化的速度线效果 - 通过overlay实现
    return frame

# 创建所有场景
clips = []
for i, scene in enumerate(scenes):
    zoom_type = ["in", "out", "pan", "in", "out"][i % 5]
    clip = create_ken_burns_clip(scene["img"], scene["duration"], zoom_type)
    clips.append(clip)

# 拼接所有片段
final_video = concatenate_videoclips(clips, method="compose")

# 生成配音文本
voiceover_text = """
欢迎来到草台班子研究室！我们专注于财经深度研究，用数据说话，严谨分析每一个投资机会。订阅我们，一起探索财富增长的秘密！
"""

# 保存配音文本供后续TTS使用
with open("/tmp/v11_voiceover.txt", "w", encoding="utf-8") as f:
    f.write(voiceover_text.strip())

print(f"视频基础结构已创建，总时长: {final_video.duration}秒")
print(f"输出路径: {OUTPUT_PATH}")
print(f"配音文本已保存到: /tmp/v11_voiceover.txt")

# 先导出无声版本，等待配音
final_video.write_videofile(
    "/tmp/v11_video_noaudio.mp4",
    fps=FPS,
    codec="libx264",
    audio=False,
    preset="fast"
)

print("无声视频已导出到: /tmp/v11_video_noaudio.mp4")
