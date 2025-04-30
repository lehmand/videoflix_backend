import subprocess
import os

def convert_video(source, resolution, suffix):
  split_target = source.split('.')[0]
  target = f'{split_target}_{suffix}.mp4'
  cmd = f'ffmpeg -i "{source}" -s {resolution} -c:v libx264 -crf 23 -c:a aac -strict -2 "{target}"'
  subprocess.run(cmd, shell=True)


def convert_video_hls(source, resolution, suffix):
    base, _ = os.path.splitext(source)
    target_file = f"{base}_{suffix}.mp4"
    cmd_transcode = (
        f'ffmpeg -i "{source}" -s {resolution} -c:v libx264 -crf 23 '
        f'-c:a aac -strict -2 "{target_file}"'
    )
    subprocess.run(cmd_transcode, shell=True)

    hls_directory = f"{base}_{suffix}_hls"
    os.makedirs(hls_directory, exist_ok=True)
    playlist_path = os.path.join(hls_directory, 'playlist.m3u8')

    cmd_hls = (
        f'ffmpeg -i "{target_file}" -codec: copy -start_number 0 '
        f'-hls_time 10 -hls_list_size 0 '
        f'-hls_segment_filename "{hls_directory}/segment_%03d.ts" '
        f'"{playlist_path}"'
    )
    subprocess.run(cmd_hls, shell=True)
