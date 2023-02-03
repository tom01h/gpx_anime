# sedで文字列 ”mytracks:” を削除したgpxファイルを入力
# なぜか、gpxpyがエラー吐くため…

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import gps_lib

extentions=['yaw', 'pitch', 'roll', 'speed'] # 下から順に表示する
start = 120 # frame No.
end = 425 # frame No.
size = 30 # text size

daxis = "off" # グラフ軸描画の有無 on or off

lat, lon, lpoint = gps_lib.parse("input.gpx", extentions, start, end)

fig, ax = plt.subplots(dpi=100, figsize=(19.2,10.8))
ani = FuncAnimation(fig, gps_lib.plot, \
    fargs = (extentions, ax, lon, lat, lpoint, size, daxis),\
    frames=len(lat), interval=100)

ani.save('gps.mp4', writer="ffmpeg")