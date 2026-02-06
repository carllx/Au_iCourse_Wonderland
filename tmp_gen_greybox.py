
import os
from PIL import Image, ImageDraw, ImageFont

def create_greybox(id, text, output_path):
    # Standard 16:9 for UI or 1:1 for diagrams
    # For UI let's use 1920x1080
    width, height = 1920, 1080
    background_color = (15, 15, 15) # Dark charcoal
    text_color = (200, 200, 200)   # Light grey
    border_color = (60, 60, 60)
    
    img = Image.new('RGB', (width, height), color=background_color)
    draw = ImageDraw.Draw(img)
    
    # Draw a dashed border
    for i in range(0, width, 40):
        draw.line([(i, 0), (min(i+20, width), 0)], fill=border_color, width=5)
        draw.line([(i, height-1), (min(i+20, width), height-1)], fill=border_color, width=5)
    for i in range(0, height, 40):
        draw.line([(0, i), (0, min(i+20, height))], fill=border_color, width=5)
        draw.line([(width-1, i), (width-1, min(i+20, height))], fill=border_color, width=5)

    # Try to load a font
    try:
        # Common macOS font paths
        font_main = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        
    # Draw text
    draw.text((width//2, height//2 - 100), f"GREYBOX: {id}", fill=text_color, font=font_main, anchor="mm")
    draw.text((width//2, height//2 + 50), text, fill=(150, 150, 150), font=font_sub, anchor="mm")
    draw.text((width//2, height - 100), "[ ACTION REQUIRED: CAPTURE AUDITION UI SCREENSHOT ]", fill=(255, 100, 100), font=font_sub, anchor="mm")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f"Created greybox: {output_path}")

assets_dir = "/Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/02_Visuals/assets/S04_Phase3_Space"
items = [
    ("S04_UI_PreDelay_80ms", "Close-up of Pre-Delay knob set specifically to 80ms."),
    ("S04_UI_RoomSize_150", "Room Size parameter pulled to 150% maximum."),
    ("S04_UI_Width_150", "Width parameter pulled to 150% (or Stereo Expander)."),
    ("S04_UI_IR_Types", "Split screen showing 3 IR types: Small Closet, Large Hall, The Void."),
    ("S04_UI_Conv_EQ", "The EQ tab in Convolution Reverb plugin: Low Cut (200Hz), Damping HF active."),
    ("S04_UI_OutputGain_Headroom", "Output Gain set to -6dB.")
]

for id, desc in items:
    path = os.path.join(assets_dir, f"{id}_cap.png")
    create_greybox(id, desc, path)
