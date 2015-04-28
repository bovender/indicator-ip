SUBDIRS = IndicatorIp
bin_SCRIPTS = indicator-ip
CLEANFILES = $(bin_SCRIPTS)

do_substitution = sed -e 's,[@]pythondir[@],$(pythondir),g'

indicator-ip: indicator-ip.in Makefile
	$(do_substitution) < $(srcdir)/indicator-ip.in > indicator-ip
	chmod +x indicator-ip
