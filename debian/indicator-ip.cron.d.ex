#
# Regular cron jobs for the indicator-ip package
#
0 4	* * *	root	[ -x /usr/bin/indicator-ip_maintenance ] && /usr/bin/indicator-ip_maintenance
