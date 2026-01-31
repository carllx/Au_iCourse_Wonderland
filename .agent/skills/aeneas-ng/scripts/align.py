import sys
import argparse
from pathlib import Path
import subprocess

# 配置 Aeneas NG API 的绝对路径
AENEAS_API_PATH = "/Users/yamlam/Downloads/aeneas-ng-api"
PYTHON_EXEC = "/opt/anaconda3/envs/mybase/bin/python"

def run_alignment(audio_path, text_path, output_path):
    """
    调用外部 aeneas-ng-api 的 cli.py 进行对齐
    """
    cli_script = Path(AENEAS_API_PATH) / "cli.py"
    
    if not cli_script.exists():
        print(f"Error: Aeneas NG CLI not found at {cli_script}")
        sys.exit(1)

    cmd = [
        PYTHON_EXEC,
        str(cli_script),
        "align",
        str(audio_path),
        str(text_path),
        "-o",
        str(output_path),
        "--lang", "zh" # 默认为中文
    ]

    print(f"Executing: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
        print(f"Successfully aligned: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during alignment: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wrapper for Aeneas NG Alignment")
    parser.add_argument("--audio", required=True, help="Input audio file (.aac, .mp3, .wav)")
    parser.add_argument("--text", required=True, help="Input transcript file (.txt)")
    parser.add_argument("--output", required=True, help="Output subtitle file (.srt)")
    
    args = parser.parse_args()
    
    run_alignment(args.audio, args.text, args.output)
