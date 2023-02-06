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

    running = False

    for track in gpx.tracks:
        for segment in track.segments:
            if rotation == 'auto':
                dx = segment.points[-1].latitude - segment.points[0].latitude
                dy = segment.points[-1].longitude - segment.points[0].longitude
                rotation = np.pi - np.arctan2(dy, dx)
                t = rotation
            else:
                t = np.deg2rad(rotation)
            R = np.array(   [[np.cos(t), -np.sin(t)],
                            [np.sin(t),  np.cos(t)]])
            for i, point in enumerate(segment.points):
                u = (point.latitude, point.longitude)
                u = np.dot(R, u)
                lat.append(u[0])
                lon.append(u[1])
                ipoint = {}
                ipoint['time'] = point.time
                for ext in point.extensions:
                    for e, s in enumerate(extentions):
                        if ext.tag == extentions[e]:
                            ipoint[extentions[e]] = float(ext.text.replace('"',''))
                lpoint.append(ipoint)
                if ipoint['speed'] > start_speed:
                    running = True
                if running and ipoint['speed'] < stop_speed:
                    break    
    return lat, lon, lpoint

def plot(frame_no, extentions, ax, lon, lat, lpoint, size, daxis="off", ratio=0):
    ax[0][0].cla()
    ax[0][0].axis(daxis)
    ax[0][0].set_xlim([0,50])
    ax[0][0].barh([0], lpoint[frame_no]['speed'], color="r")

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
    line_height = (ymax-ymin)*size/1080*1.5
    ax[1][0].cla()
    ax[1][0].axis(daxis)
    ax[1][0].set_xlim([xmin,xmax])
    ax[1][0].set_ylim([ymin,ymax])
    ax[1][0].plot(lon[:frame_no], lat[:frame_no], color="b")
    ax[1][0].text(xmin, ymin+line_height*len(extentions), "time: "+str(lpoint[frame_no]['time']), size=size)
    for i, s in enumerate(extentions):
        ax[1][0].text(xmin, ymin+line_height*i, s+": "+str(lpoint[frame_no][s]), size=size)

    ax[0][1].axis("off")

    ax[1][1].cla()
    ax[1][1].axis(daxis)
    ax[1][1].set_ylim([-90,90])
    ax[1][1].bar([0], lpoint[frame_no]['roll'], color="g")
