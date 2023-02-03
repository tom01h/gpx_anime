# GPXログからMP4動画を作る

lat, lon の軌跡の動画をMP4で出力する  
別にffmpegが必要  
extentionの内容をテキストで出力

### 動画
input.gpxを入力してanim.mp4を出力  
`extentions=['yaw', 'pitch', 'roll', 'speed']` に並べたデータをテキストで出力  
`start = 120 # frame No.`でスタートフレームを指定  
`end = 425 # frame No.`でエンドフレームを指定  
`line_height=0.00008`で1行の高さを指定 (自動にしたい)  

### 静止画
input.gpxを入力してgps.pngを出力  
動画の設定以外にも  
`daxis = "on" # グラフ軸描画の有無 on or off`で枠の出力を指定  

### GPXファイルの例

```
   <trkpt lat="36.533376667" lon="138.334617667">
    <ele>1398.2000</ele>
    <time>2023-01-22T02:11:14.000Z</time>
    <fix>dgps</fix>
    <sat>16</sat>
    <hdop>0.9</hdop>
    <vdop>1.4</vdop>
    <pdop>1.7</pdop>
    <extensions>
    <speed>"0.012346667"</speed>
    <track>"nan"</track>
    <roll>"4.19"</roll>
    <pitch>"0.00"</pitch>
    <yaw>"312.88"</yaw>
    <accl>"0.02, 0.00, 0.00"</accl>
    </extensions>
   </trkpt>```