#!/bin/bash
# v11 动漫风格测试样片 - FFmpeg版本
# 35秒，1920x1080，16:9

OUTPUT="/Volumes/WorkData/ctbzai/outputs/v11-anime-sample.mp4"
TEMP_DIR="/tmp/v11_frames"
mkdir -p $TEMP_DIR

# 创建35秒的视频，30fps = 1050帧
FPS=30
DURATION=35
TOTAL_FRAMES=$((FPS * DURATION))

# 场景定义
# 场景1: 开场Logo (0-8秒) - 深蓝色+橙色
# 场景2: 频道定位 (8-18秒) - 紫蓝色+亮蓝
# 场景3: 核心价值 (18-30秒) - 深紫+红橙  
# 场景4: CTA结尾 (30-35秒) - 亮橙色+白

echo "创建动漫风格视频帧..."

# 使用ffmpeg直接生成带效果的视频
ffmpeg -y -f lavfi -i color=c=1a3775:s=1920x1080:d=8 \n  -vf "
    geq=lum='p(X,Y)':cb='128':cr='128',
    drawtext=text='草台班子研究室':fontcolor=white:fontsize=100:x=(w-text_w)/2:y=(h-text_h)/2:fontfile=/System/Library/Fonts/Helvetica.ttc:shadowcolor=FF8C42:shadowx=4:shadowy=4,
    drawtext=text='Grassroots Research Lab':fontcolor=white:fontsize=40:x=(w-text_w)/2:y=(h+100)/2:fontfile=/System/Library/Fonts/Helvetica.ttc:enable='gte(t,1)',
    fade=t=in:st=0:d=0.5,
    fade=t=out:st=7.5:d=0.5
  " -t 8 -c:v libx264 -pix_fmt yuv420p /tmp/v11_scene1.mp4

ffmpeg -y -f lavfi -i color=c=2d1e5a:s=1920x1080:d=10 \n  -vf "
    drawtext=text='财经深度研究':fontcolor=white:fontsize=80:x=(w-text_w)/2:y=(h-text_h)/2-100:fontfile=/System/Library/Fonts/Helvetica.ttc:enable='between(t\,0\,4)',
    drawtext=text='数据驱动决策':fontcolor=64C8FF:fontsize=70:x=(w-text_w)/2:y=(h-text_h)/2:fontfile=/System/Library/Fonts/Helvetica.ttc:enable='between(t\,3\,7)',
    drawtext=text='洞察市场趋势':fontcolor=white:fontsize=70:x=(w-text_w)/2:y=(h-text_h)/2+100:fontfile=/System/Library/Fonts/Helvetica.ttc:enable='between(t\,6\,10)',
    fade=t=in:st=0:d=0.3
  " -t 10 -c:v libx264 -pix_fmt yuv420p /tmp/v11_scene2.mp4

ffmpeg -y -f lavfi -i color=c=3c2864:s=1920x1080:d=12 \n  -vf "
    drawtext=text='严谨研究方法':fontcolor=white:fontsize=75:x=(w-text_w)/2:y=(h-text_h)/2-80:fontfile=/System/Library/Fonts/Helvetica.ttc:enable='between(t\,0\,4)',
    drawtext=text='独立客观分析':fontcolor=FF6464:fontsize=75:x=(w-text_w)/2:y=(h-text_h)/2+20:fontfile=/System/Library/Fonts/Helvetica.ttc:enable='between(t\,4\,8)',
    drawtext=text='专业投资视角':fontcolor=white:fontsize=75:x=(w-text_w)/2:y=(h-text_h)/2+120:fontfile=/System/Library/Fonts/Helvetica.ttc:enable='between(t\,8\,12)',
    fade=t=in:st=0:d=0.3
  " -t 12 -c:v libx264 -pix_fmt yuv420p /tmp/v11_scene3.mp4

ffmpeg -y -f lavfi -i color=c=FF6432:s=1920x1080:d=5 \n  -vf "
    drawtext=text='立即订阅！':fontcolor=white:fontsize=120:x=(w-text_w)/2:y=(h-text_h)/2-50:fontfile=/System/Library/Fonts/Helvetica.ttc:shadowcolor=black:shadowx=5:shadowy=5,
    drawtext=text='SUBSCRIBE NOW':fontcolor=white:fontsize=50:x=(w-text_w)/2:y=(h-text_h)/2+80:fontfile=/System/Library/Fonts/Helvetica.ttc:enable='gte(t,0.5)',
    fade=t=in:st=0:d=0.3,
    fade=t=out:st=4.5:d=0.5
  " -t 5 -c:v libx264 -pix_fmt yuv420p /tmp/v11_scene4.mp4

# 合并所有场景
echo "合并场景..."
ffmpeg -y -f concat -safe 0 -i <(echo -e "file '/tmp/v11_scene1.mp4'\nfile '/tmp/v11_scene2.mp4'\nfile '/tmp/v11_scene3.mp4'\nfile '/tmp/v11_scene4.mp4'") -c copy /tmp/v11_merged.mp4

# 添加动漫风格特效 - 速度线
echo "添加动漫特效..."
ffmpeg -y -i /tmp/v11_merged.mp4 -vf "
  format=gbrp,
  geq=lum='lum(X,Y)':cb='cb(X,Y)':cr='cr(X,Y)',
  noise=alls=10:allf=t+u,
  smartblur=lr=1:ls=1,
  eq=contrast=1.1:saturation=1.2
" -c:v libx264 -pix_fmt yuv420p -crf 23 "$OUTPUT"

echo "视频创建完成: $OUTPUT"
ls -lh "$OUTPUT"
