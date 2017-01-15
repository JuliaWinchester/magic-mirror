export DISPLAY=:0.0

tmux kill-session -t mode

tmux-new() {
	if [[ -n $TMUX ]]; then
		TMUX= tmux new -d -s mode 'chromium-browser --noerrdialogs --kiosk ./html/status.html'
	else
		tmux new -d -s mode 'chromium-browser --noerrdialogs --kiosk ./html/status.html'
	fi
}

tmux-new


