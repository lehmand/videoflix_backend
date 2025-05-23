import subprocess
import os

def convert_video(source, resolution, suffix):
  """Convert video to a specific resolution"""
  split_target = source.split('.')[0]
  target = f'{split_target}_{suffix}.mp4'
  cmd = f'ffmpeg -i "{source}" -s {resolution} -c:v libx264 -crf 23 -c:a aac -strict -2 "{target}"'
  subprocess.run(cmd, shell=True)
