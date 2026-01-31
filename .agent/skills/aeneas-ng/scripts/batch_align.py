import argparse
import sys
from pathlib import Path
import subprocess

# 配置
PYTHON_EXEC = "/opt/anaconda3/envs/mybase/bin/python"
ALIGN_SCRIPT = Path(__file__).parent / "align.py"

def batch_process(target_dir):
    """
    遍历目录下的所有 .aac/.mp3 文件，寻找同名 .txt 并进行对齐
    """
    dir_path = Path(target_dir)
    if not dir_path.exists():
        print(f"Directory not found: {target_dir}")
        sys.exit(1)

    # 寻找音频文件
    audio_extensions = {".aac", ".mp3", ".wav"}
    audio_files = [f for f in dir_path.iterdir() if f.suffix.lower() in audio_extensions]
    
    success_count = 0
    fail_count = 0
    
    for audio_file in audio_files:
        # 寻找对应的 .txt
        text_file = audio_file.with_suffix(".txt")
        if not text_file.exists():
            print(f"[SKIP] No transcript found for {audio_file.name}")
            continue
            
        output_file = audio_file.with_suffix(".srt")
        
        print(f"Processing {audio_file.name}...")
        
        cmd = [
            PYTHON_EXEC,
            str(ALIGN_SCRIPT),
            "--audio", str(audio_file),
            "--text", str(text_file),
            "--output", str(output_file)
        ]
        
        try:
            subprocess.run(cmd, check=True)
            success_count += 1
        except subprocess.CalledProcessError:
            print(f"[FAIL] Failed to process {audio_file.name}")
            fail_count += 1
            
    print(f"\nBatch processing complete.")
    print(f"Success: {success_count}")
    print(f"Failed: {fail_count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch align audio and text")
    parser.add_argument("--dir", required=True, help="Directory containing audio and txt files")
    
    args = parser.parse_args()
    batch_process(args.dir)
