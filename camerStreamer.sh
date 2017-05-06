raspivid -o - -t 0 -w 1280 -h 720 -rot 180 -vf -fps 24 |cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8160}' :demux=h264
