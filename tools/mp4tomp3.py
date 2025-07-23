# 输入文件路径
input_file = "/Users/walter/Downloads/xiaorenwu.mp4"
# 输出文件路径
output_file = "/Users/walter/Downloads/xiaorenwu123.mp3"


# 导入所需模块
from moviepy.editor import VideoFileClip


clip = VideoFileClip(input_file)
audio = clip.audio
audio.write_audiofile(output_file)