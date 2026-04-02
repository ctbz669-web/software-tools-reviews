#!/bin/bash
set -e

IMG_DIR="/Volumes/WorkData/ctbzai/v13-images"
OUTPUT="/Volumes/WorkData/ctbzai/outputs/v13-masculine-sample.mp4"
TEMP_DIR="/Volumes/WorkData/ctbzai/v13-images/temp"
mkdir -p "$TEMP_DIR"

# Scene durations (seconds)
D1=8   # Opening
D2=10  # Dataviz
D3=12  # Tools
D4=5   # CTA
FPS=30

# Ken Burns effect function - zoom in with pan
generate_ken_burns() {
    local input=$1
    local duration=$2
    local output=$3
    local zoom_start=$4
    local zoom_end=$5
    local pan_x=$6
    local pan_y=$7
    
    ffmpeg -y -loop 1 -i "$input" -vf "
        zoompan=z='zoom+$zoom_start+($zoom_end-$zoom_start)*on/$duration/$FPS':
        x='iw/2-(iw/zoom/2)+$pan_x*sin(on/$duration/$FPS*3.14)':
        y='ih/2-(ih/zoom/2)+$pan_y*cos(on/$duration/$FPS*3.14)':
        d=$duration*$FPS:s=1920x1080:fps=$FPS,
        format=yuv420p
    " -c:v libx264 -pix_fmt yuv420p -an -t $duration "$output"
}

echo "Generating scene 1: Opening (Logo) - ${D1}s"
generate_ken_burns "$IMG_DIR/01-logo.jpg" $D1 "$TEMP_DIR/scene1.mp4" 1.0 1.15 50 20

echo "Generating scene 2: Data Visualization - ${D2}s"
generate_ken_burns "$IMG_DIR/02-dataviz.jpg" $D2 "$TEMP_DIR/scene2.mp4" 1.05 1.2 -40 30

echo "Generating scene 3: Tools - ${D3}s"
generate_ken_burns "$IMG_DIR/03-tools.jpg" $D3 "$TEMP_DIR/scene3.mp4" 1.0 1.1 30 -20

echo "Generating scene 4: CTA - ${D4}s"
generate_ken_burns "$IMG_DIR/04-cta.jpg" $D4 "$TEMP_DIR/scene4.mp4" 1.1 1.0 0 0

# Create concat list
cat > "$TEMP_DIR/concat.txt" << CONCAT
file '$TEMP_DIR/scene1.mp4'
file '$TEMP_DIR/scene2.mp4'
file '$TEMP_DIR/scene3.mp4'
file '$TEMP_DIR/scene4.mp4'
CONCAT

# Concatenate scenes with fast cuts
echo "Concatenating scenes..."
ffmpeg -y -f concat -safe 0 -i "$TEMP_DIR/concat.txt" -c copy "$TEMP_DIR/combined.mp4"

# Add tech electronic background music (using sine wave for placeholder)
echo "Adding audio..."
ffmpeg -y -i "$TEMP_DIR/combined.mp4" -f lavfi -i "sine=frequency=440:duration=35" \
    -filter_complex "[1:a]volume=0.3,aecho=0.8:0.9:1000:0.3,lowpass=f=800[a]" \
    -map 0:v -map "[a]" -c:v copy -shortest "$OUTPUT"

echo "Video created: $OUTPUT"
ls -lh "$OUTPUT"
