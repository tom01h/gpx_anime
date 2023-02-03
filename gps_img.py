# sedで文字列 ”mytracks:” を削除したgpxファイルを入力
# なぜか、gpxpyがエラー吐くため…

import matplotlib.pyplot as plt
import gps_lib

extentions=['yaw', 'pitch', 'roll', 'speed'] # 下から順に表示する
start = 120 # frame No.
end = 425 # frame No.
line_height=0.00008

daxis = "on" # グラフ軸描画の有無 on or off

lat, lon, lpoint = gps_lib.parse("input.gpx", extentions, start, end)

fig, ax = plt.subplots(dpi=100, figsize=(19.2,10.8))
gps_lib.plot(len(lat)-1, extentions, ax, lon, lat, lpoint, line_height, daxis)
fig.savefig("gps.png", format="png")
