import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import argparse
import gps_lib

parser = argparse.ArgumentParser(
            prog='gps_ani.py',
            description='GPXファイルから軌跡動画を生成',
            add_help=True,
            )
 
parser.add_argument('-i', '--input_file', default='input.gpx', help='input gpx file name')
parser.add_argument('-o', '--output_file', default='gps.mp4', help='output {mp4, gif} file name')
args = parser.parse_args()

extentions=['speed', 'roll', 'pitch', 'yaw']
lw = 5 # line width
size = 30 # speed, roll メーターの text size
size_all = 10 # 軌跡の横のtext size
daxis = "on" # グラフ軸描画の有無 on or off
ratio = 16/9 # 指定した縦横比に収まるようにサイズ調整する 0でアスペクト比を維持しないでサイズ調整する
rotation = 'auto' # 回転角度を指定（度）'auto'指定で自動
grid_m = 5 # grid 間隔(m)
grid_w = 1 # grid line width

lon, lat, lpoint = gps_lib.parse(args.input_file, extentions, rotation)

fig, ax = plt.subplots(2, 2, gridspec_kw={
                           'width_ratios': [10, 1],
                           'height_ratios': [1, 10]},
                           dpi=100, figsize=(19.2,10.8))
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
ani = FuncAnimation(fig, gps_lib.plot, \
    fargs = (extentions, ax, lon, lat, lpoint, lw, size, size_all, daxis, ratio, grid_m, grid_w),\
    frames=len(lat), interval=100)

if '.mp4' in args.output_file:
    ani.save(args.output_file, writer="ffmpeg")
else:
    ani.save(args.output_file)    