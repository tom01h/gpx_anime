import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import gpxpy
import numpy as np

start_speed = 2  # ipoint['speed'] > start_speed となった後に
stop_speed = 0.1 # ipoint['speed'] < stop_speed となると変換を中止する

def parse(filename, extentions, rotation=0):
    lat = []
    lon = []
    lpoint = []
    # gpxファイルを読む
    gpx_file = open(filename, 'r', encoding='utf-8')
    gpx = gpxpy.parse(gpx_file)

    # データ解析 最初の2ループはほぼ意味なし
    for track in gpx.tracks:
        for segment in track.segments:
            # 終了フレームを決定
            running = False
            for i, point in enumerate(segment.points):
                for ext in point.extensions:
                    if ext.tag == 'speed':
                        speed = float(ext.text.replace('"',''))
                if speed > start_speed:
                    running = True
                if running and speed < stop_speed:
                    break    
            stop_frame = i
            # 緯度と経度で角度当たりの距離が違うので補正する係数
            lon_lat = np.cos(np.radians(segment.points[0].latitude))
            # 回転角度と回転行列を計算
            if rotation == 'auto':
                dx = segment.points[0].longitude - segment.points[stop_frame-1].longitude
                dy = segment.points[0].latitude - segment.points[stop_frame-1].latitude
                rotation = np.arctan2(dy, dx * lon_lat)
                t = np.pi/2 - rotation
            else:
                t = np.deg2rad(rotation)
            R = np.array(   [[np.cos(t), -np.sin(t)],
                            [np.sin(t),  np.cos(t)]])
            # リスト（lat, lon, lpoint）作成
            ipoint = {'time': 'dummy'}
            for i, point in enumerate(segment.points):
                if ipoint['time'] == point.time: # 同時刻のデータが連続した場合は削除する
                    continue    
                u = (point.longitude * lon_lat, point.latitude) # lon_lt は "緯度経度 → x,y座標" 変換時の距離補正
                u = np.dot(R, u) # 回転してからリストに追加
                lon.append(u[0])
                lat.append(u[1])
                ipoint = {}
                ipoint['time'] = point.time
                for ext in point.extensions:
                    for e, s in enumerate(extentions):
                        if ext.tag == extentions[e]:
                            ipoint[extentions[e]] = float(ext.text.replace('"',''))
                lpoint.append(ipoint)
                if i == stop_frame:
                    break    
    return lon, lat, lpoint

def plot(frame_no, extentions, ax, lon, lat, lpoint, lw, size, daxis="off", ratio=0):
    # 速度計 (最大50km/h)
    ax[0][0].cla()
    ax[0][0].axis(daxis)
    ax[0][0].set_xlim([0,50])
    ax[0][0].set_ylim([0,1])
    ax[0][0].barh([0], lpoint[frame_no]['speed'], color="r")
    ax[0][0].spines['bottom'].set_position(('data', 1))
    ax[0][0].set_xticks([0,10,20,30,40,50])
    ax[0][0].set_xticklabels([0,10,20,30,40,50], fontsize=size)


    # 軌跡
    xmin = min(lon)
    xmax = max(lon)
    ymin = min(lat)
    ymax = max(lat)
    if ratio != 0:
        xlen = (xmax-xmin)
        ylen = (ymax-ymin)
        if xlen > ylen * ratio:
            ymin -= (xlen / ratio - ylen) /2
            ymax = ymin + xlen / ratio
        else:
            xmin -= (ylen * ratio - xlen) /2
            xmax = xmin + ylen * ratio
    ax[1][0].cla()
    ax[1][0].axis(daxis)
    ax[1][0].set_xlim([xmin,xmax])
    ax[1][0].set_ylim([ymin,ymax])
    ax[1][0].plot(lon[:frame_no], lat[:frame_no], color="b", lw=lw)
    star = "time: "+str(lpoint[frame_no]['time'])
    for i, s in enumerate(extentions):
        star += "\n"+s+": "+str(lpoint[frame_no][s])
    ax[1][0].text(xmin, ymin, star, size=size)

    # なし
    ax[0][1].axis("off")

    # 傾き (‐90度～90度)
    ax[1][1].cla()
    ax[1][1].axis(daxis)
    ax[1][1].set_ylim([-90,90])
    ax[1][1].bar([0], lpoint[frame_no]['roll'], color="g")
    ax[1][1].set_yticks([-90,-60,-30,0,30,60,90])
    ax[1][1].set_yticklabels([-90,-60,-30,0,30,60,90], fontsize=size)
