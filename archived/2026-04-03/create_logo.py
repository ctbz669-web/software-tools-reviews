from PIL import Image, ImageDraw, ImageFont

# 創建透明背景的 Logo
width, height = 300, 80
img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# 嘗試載入中文字體
try:
    font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 28)
except:
    try:
        font = ImageFont.truetype("/System/Library/Fonts/STHeiti Light.ttc", 28)
    except:
        font = ImageFont.load_default()

# 繪製半透明黑色背景
overlay = Image.new('RGBA', (width, height), (0, 0, 0, 180))
img = Image.alpha_composite(img, overlay)
draw = ImageDraw.Draw(img)

# 繪製文字
text = "草台班子研究室"
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x = (width - text_width) // 2
y = (height - text_height) // 2

draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

# 保存
img.save('/Users/kevin/.openclaw/workspace/logo-canvas.png')
print("Logo created successfully!")
