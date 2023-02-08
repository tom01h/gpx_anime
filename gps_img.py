# sedで文字列 ”mytracks:” を削除したgpxファイルを入力
# なぜか、gpxpyがエラー吐くため…

import matplotlib.pyplot as plt
import argparse
import gps_lib

parser = argparse.ArgumentParser(
            prog='gps_img.py',
            description='GPXファイルから軌跡画像を生成',
            add_help=True,
            )
 
parser.add_argument('-i', '--input_file', default='input.gpx', help='input gpx file name')
parser.add_argument('-o', '--output_file', default='gps.png', help='output image file name')
args = parser.parse_args()

extentions=['speed', 'roll', 'pitch', 'yaw']
lw = 5 # line width
size = 30 # text size
daxis = "on" # グラフ軸描画の有無 on or off
ratio = 16/9 # 指定した縦横比に収まるようにサイズ調整する 0でアスペクト比を維持しないでサイズ調整する
rotation = 'auto' # 回転角度を指定（度）'auto'指定で自動

lon, lat, lpoint = gps_lib.parse(args.input_file, extentions, rotation)

fig, ax = plt.subplots(nrows=2, ncols=2, gridspec_kw={
                           'width_ratios': [10, 1],
                           'height_ratios': [1, 10]},
                           dpi=100, figsize=(19.2,10.8))
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

gps_lib.plot(len(lat)-1, extentions, ax, lon, lat, lpoint, lw, size, daxis, ratio)
fig.savefig(args.output_file, format="png")