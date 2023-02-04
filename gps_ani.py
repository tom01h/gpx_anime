# sedで文字列 ”mytracks:” を削除したgpxファイルを入力
# なぜか、gpxpyがエラー吐くため…

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import gps_lib

extentions=['yaw', 'pitch', 'roll', 'speed'] # 下から順に表示する
size = 10 # text size

daxis = "off" # グラフ軸描画の有無 on or off

lat, lon, lpoint = gps_lib.parse("input.gpx", extentions)

fig, ax = plt.subplots(2, 2, gridspec_kw={
                           'width_ratios': [10, 1],
                           'height_ratios': [1, 10]},
                           dpi=100, figsize=(19.2,10.8))
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
ani = FuncAnimation(fig, gps_lib.plot, \
    fargs = (extentions, ax, lon, lat, lpoint, size, daxis),\
    frames=len(lat), interval=100)

ani.save('gps.mp4', writer="ffmpeg")