all:
	python3 main.py

systemd:
	sudo sh -c 'echo "[Unit]\n\
	Description=tinyblog service\n\
	After=network.target\n\
	StartLimitIntervalSec=0\n\
	\n\
	[Service]\n\
	Type=simple\n\
	Restart=always\n\
	RestartSec=1\n\
	User=$(USER)\n\
	ExecStart=sh -c \"cd /home/$(USER)/blog; python3 main.py\"\n\
	\n\
	[Install]\n\
	WantedBy=multi-user.target\n" > /etc/systemd/system/tinyblog.service'
	sudo systemctl enable tinyblog
	sudo systemctl start tinyblog
	sudo systemctl status tinyblog
