export DISPLAY=:0.0

tmux kill-session

tmux new -d -s shuffle "python img-shuffle.py $1 $2"
