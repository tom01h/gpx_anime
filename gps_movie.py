import sys
import matplotlib.pyplot as plt
import moviepy.editor as mp
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage
from moviepy.video.fx.mask_color import mask_color
import gps_lib

extentions=['speed', 'roll', 'pitch', 'yaw']
size = 10 # text size
daxis = "off" # グラフ軸描画の有無 on or off
ratio = 16/9 # 指定した縦横比に収まるようにサイズ調整する 0でアスペクト比を維持しないでサイズ調整する
rotation = 'auto' # 回転角度を指定（度）'auto'指定で自動

#video = mp.VideoFileClip('aa.mp4').subclip(0,10)
#video = mp.VideoFileClip('aa.mp4').subclip(0, len(lon)/10)
video = mp.VideoFileClip('aa.mp4')

inputfile='input.gpx'
if len(sys.argv) > 1:
    inputfile=sys.argv[1]
lon, lat, lpoint = gps_lib.parse(inputfile, extentions, rotation)

fig, ax = plt.subplots(2, 2, gridspec_kw={
                           'width_ratios': [10, 1],
                           'height_ratios': [1, 10]},
                           dpi=100, figsize=(video.w/100, video.h/100))
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

ratio = video.w/video.h

def make_frame(t):
    frame = int(t*10)
    gps_lib.plot(frame, extentions, ax, lon, lat, lpoint, size, daxis, ratio)

    bmp = mplfig_to_npimage(fig)
    return bmp

outputfile='gps.mp4'
if len(sys.argv) > 2:
    outputfile=sys.argv[2]
animation = VideoClip(make_frame, duration = len(lon)/10)
#animation = VideoClip(make_frame, duration = 10)

final = mp.CompositeVideoClip([video, mask_color(animation,(255,255,255))])

final.write_videofile(outputfile, fps = video.fps)