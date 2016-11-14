export DISPLAY=:0.0

tmux kill-session

tmux new -d -s status 'python img-shuffle.py $1 $2'