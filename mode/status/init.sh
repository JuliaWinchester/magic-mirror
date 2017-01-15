export DISPLAY=:0.0

tmux kill-session -t mode

tmux new -d -s mode 'chromium-browser --noerrdialogs --kiosk ./html/status.html'

