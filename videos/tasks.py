import subprocess

def convert_480p(source):
  split_target = source.split('.')[0]
  target = split_target + '_480p.mp4'
  cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
  subprocess.run(cmd)

def convert_720p(source):
  split_target = source.split('.')[0]
  target = split_target + '_720p.mp4'
  cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
  subprocess.run(cmd)