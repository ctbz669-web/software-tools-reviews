#!/bin/bash
cd /Users/kevin/.openclaw/workspace
mkdir -p /tmp/ep1_video

cat > /tmp/ep1_video/inputs.txt << 'EOF'
file 'ep1_segment_01_hook.png'
duration 31.56
file 'ep1_segment_02_method.png'
duration 37.88
file 'ep1_segment_03_stocks_re.png'
duration 44.19
file 'ep1_segment_04_startup.png'
duration 25.25
file 'ep1_segment_05_passive.png'
duration 25.25
file 'ep1_segment_06_crypto_fire.png'
duration 50.50
file 'ep1_segment_07_skills.png'
duration 31.56
file 'ep1_segment_08_conclusion.png'
duration 56.81
file 'ep1_segment_08_conclusion.png'
EOF

echo "輸入文件已創建"
