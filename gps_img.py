# sedで文字列 ”mytracks:” を削除したgpxファイルを入力
# なぜか、gpxpyがエラー吐くため…

import matplotlib.pyplot as plt
import gps_lib

extentions=['yaw', 'pitch', 'roll', 'speed'] # 下から順に表示する
size = 30 # text size
daxis = "on" # グラフ軸描画の有無 on or off
ratio = 16/9 # 指定した縦横比に収まるようにサイズ調整する 0でアスペクト比を維持しないでサイズ調整する
rotation = 0 # 回転角度を指定（度）

lat, lon, lpoint = gps_lib.parse("input.gpx", extentions, rotation)

fig, ax = plt.subplots(nrows=2, ncols=2, gridspec_kw={
                           'width_ratios': [10, 1],
                           'height_ratios': [1, 10]},
                           dpi=100, figsize=(19.2,10.8))
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

gps_lib.plot(len(lat)-1, extentions, ax, lon, lat, lpoint, size, daxis, ratio)
fig.savefig("gps.png", format="png")
