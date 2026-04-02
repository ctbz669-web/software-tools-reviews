#!/bin/bash
# v11 动漫风格测试样片 - 简化版
OUTPUT="/Volumes/WorkData/ctbzai/outputs/v11-anime-sample.mp4"

# 场景1: 开场Logo (0-8秒) - 深蓝背景
ffmpeg -y -f lavfi -i "color=c=1a3775:s=1920x1080:r=30" -t 8 \
  -vf "drawtext=text='草台班子研究室':fontcolor=white:fontsize=100:x=(w-text_w)/2:y=(h-text_h)/2:fontfile=/System/Library/Fonts/PingFang.ttc:shadowcolor=FF8C42:shadowx=5:shadowy=5,drawtext=text='Grassroots Research Lab':fontcolor=white:fontsize=40:x=(w-text_w)/2:y=(h+120)/2:fontfile=/System/Library/Fonts/PingFang.ttc:enable='gte(t,1)',fade=t=in:st=0:d=0.5,fade=t=out:st=7.5:d=0.5" \
  -pix_fmt yuv420p /tmp/s1.mp4 2>/dev/null

# 场景2: 频道定位 (8-18秒) - 紫蓝背景  
ffmpeg -y -f lavfi -i "color=c=2d1e5a:s=1920x1080:r=30" -t 10 \
  -vf "drawtext=text='财经深度研究':fontcolor=white:fontsize=80:x=(w-text_w)/2:y=(h-text_h)/2-80:fontfile=/System/Library/Fonts/PingFang.ttc:enable='between(t,0,4)',drawtext=text='数据驱动决策':fontcolor=64C8FF:fontsize=70:x=(w-text_w)/2:y=(h-text_h)/2+20:fontfile=/System/Library/Fonts/PingFang.ttc:enable='between(t,3,7)',drawtext=text='洞察市场趋势':fontcolor=white:fontsize=70:x=(w-text_w)/2:y=(h-text_h)/2+120:fontfile=/System/Library/Fonts/PingFang.ttc:enable='between(t,6,10)',fade=t=in:st=0:d=0.3" \
  -pix_fmt yuv420p /tmp/s2.mp4 2>/dev/null

# 场景3: 核心价值 (18-30秒) - 深紫背景
ffmpeg -y -f lavfi -i "color=c=3c2864:s=1920x1080:r=30" -t 12 \
  -vf "drawtext=text='严谨研究方法':fontcolor=white:fontsize=75:x=(w-text_w)/2:y=(h-text_h)/2-80:fontfile=/System/Library/Fonts/PingFang.ttc:enable='between(t,0,4)',drawtext=text='独立客观分析':fontcolor=FF6464:fontsize=75:x=(w-text_w)/2:y=(h-text_h)/2+20:fontfile=/System/Library/Fonts/PingFang.ttc:enable='between(t,4,8)',drawtext=text='专业投资视角':fontcolor=white:fontsize=75:x=(w-text_w)/2:y=(h-text_h)/2+120:fontfile=/System/Library/Fonts/PingFang.ttc:enable='between(t,8,12)',fade=t=in:st=0:d=0.3" \
  -pix_fmt yuv420p /tmp/s3.mp4 2>/dev/null

# 场景4: CTA结尾 (30-35秒) - 亮橙背景
ffmpeg -y -f lavfi -i "color=c=FF6432:s=1920x1080:r=30" -t 5 \
  -vf "drawtext=text='立即订阅！':fontcolor=white:fontsize=120:x=(w-text_w)/2:y=(h-text_h)/2-40:fontfile=/System/Library/Fonts/PingFang.ttc:shadowcolor=black:shadowx=5:shadowy=5,drawtext=text='SUBSCRIBE NOW':fontcolor=white:fontsize=50:x=(w-text_w)/2:y=(h-text_h)/2+80:fontfile=/System/Library/Fonts/PingFang.ttc:enable='gte(t,0.5)',fade=t=in:st=0:d=0.3,fade=t=out:st=4.5:d=0.5" \
  -pix_fmt yuv420p /tmp/s4.mp4 2>/dev/null

# 合并所有场景
echo "file '/tmp/s1.mp4'" > /tmp/concat.txt
echo "file '/tmp/s2.mp4'" >> /tmp/concat.txt
echo "file '/tmp/s3.mp4'" >> /tmp/concat.txt
echo "file '/tmp/s4.mp4'" >> /tmp/concat.txt

ffmpeg -y -f concat -safe 0 -i /tmp/concat.txt -c copy "$OUTPUT" 2>/dev/null

echo "✅ 视频创建完成: $OUTPUT"
ls -lh "$OUTPUT"
