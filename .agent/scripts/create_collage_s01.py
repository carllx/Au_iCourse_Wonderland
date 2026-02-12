from PIL import Image
import os

def create_collage():
    base_path = "/Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/02_Visuals/assets"
    files = [
        "S02_Phase1_Purify/S02_Cover.png",
        "S03_Phase2_Sculpt/S03_Cover.png",
        "S04_Phase3_Space/S04_Cover.png",
        "S05_Phase4_Position/S05_Cover.png"
    ]
    
    images = []
    for f in files:
        full_path = os.path.join(base_path, f)
        if os.path.exists(full_path):
            images.append(Image.open(full_path))
        else:
            print(f"Warning: {f} not found")
            return

    # Assuming all covers are same size (likely 1920x1080)
    # We want a square result? Or just a grid? 
    # User said "combine square image" (合并方形图).
    # If inputs are 16:9, a 2x2 grid will be 16:9.
    # To make it square, we might need to crop or resize, or maybe the user just meant "grid".
    # I will stick to 2x2 grid first. If "square image" implies the *output* must be 1:1, I would need to crop the inputs to 1:1 first.
    # Given they are covers (Title Cards), they are likely 16:9.
    # A 2x2 grid of 16:9 images is still 16:9. 
    # If the user specifically said "square", maybe they want the *result* to be square.
    # detailed: "combine square image" -> "合并方形图". 
    # Let's crop the center square of each cover then combine them into a 2x2 grid. Then the result is square.
    
    w, h = images[0].size
    min_dim = min(w, h)
    
    cropped_images = []
    for img in images:
        # Center crop to square
        left = (w - min_dim)/2
        top = (h - min_dim)/2
        right = (w + min_dim)/2
        bottom = (h + min_dim)/2
        cropped_images.append(img.crop((left, top, right, bottom)))
        
    # Result size
    final_w = min_dim * 2
    final_h = min_dim * 2
    
    result = Image.new('RGB', (int(final_w), int(final_h)))
    
    result.paste(cropped_images[0], (0, 0))
    result.paste(cropped_images[1], (int(min_dim), 0))
    result.paste(cropped_images[2], (0, int(min_dim)))
    result.paste(cropped_images[3], (int(min_dim), int(min_dim)))
    
    output_path = "/Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/02_Visuals/assets/S01_Intro/S01_Map_Four_Phases.png"
    result.save(output_path)
    print(f"Saved to {output_path}")

create_collage()
