mv shirubed.service /lib/systemd/system/
$ sudo systemctl list-unit-files --type=service | grep shirubed
systemctl enable shirubed
systemctl daemon-reload