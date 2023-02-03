import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import gpxpy

def parse(filename, extentions, start, end):
    lat = []
    lon = []
    lpoint = []
    # gpxファイルを読む
    gpx_file = open(filename, 'r', encoding='utf-8')
    gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            for i, point in enumerate(segment.points):
                if i < start or i > end:
                    continue
                lat.append(point.latitude)
                lon.append(point.longitude)
                ipoint = {}
                ipoint['time'] = point.time
                for ext in point.extensions:
                    for e, s in enumerate(extentions):
                        if ext.tag == extentions[e]:
                            ipoint[extentions[e]] = float(ext.text.replace('"',''))
                lpoint.append(ipoint)
    return lat, lon, lpoint

def plot(frame_no, extentions, ax, lon, lat, lpoint, line_height, daxis):
    xmin = min(lon)
    xmax = max(lon)
    ymin = min(lat)
    ymax = max(lat)
    ax.cla()
    ax.axis(daxis)
    ax.set_xlim([xmin,xmax])
    ax.set_ylim([ymin,ymax])
    ax.plot(lon[:frame_no], lat[:frame_no], color="b")
    ax.text(xmin, ymin+line_height*len(extentions), "time: "+str(lpoint[frame_no]['time']), size=30)
    for i, s in enumerate(extentions):
        ax.text(xmin, ymin+line_height*i, s+": "+str(lpoint[frame_no][s]), size=30)
