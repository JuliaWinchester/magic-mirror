export DISPLAY=:0.0

tmux kill-session -t mode

tmux new -d -s mode "python img_shuffle.py $1 $2"
