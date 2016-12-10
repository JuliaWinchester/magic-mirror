export DISPLAY=:0.0

tmux kill-session

tmux new -d -s status 'chromium-browser --noerrdialogs --kiosk ./html/status.html'

