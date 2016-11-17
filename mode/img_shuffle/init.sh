export DISPLAY=:0.0

tmux kill-session -t shuffle

tmux new -d -s shuffle "python img_shuffle.py $1 $2"
