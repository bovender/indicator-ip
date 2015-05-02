PREFIX ?= /usr
BINDIR ?= $(PREFIX)/bin
MANDIR ?= $(PREFIX)/share/man
SHAREDIR ?= $(PREFIX)/share

.PHONY: clean install upload

clean:
	rm -f indicator-ip.1* NEWS README
	find -name '*.pyc' -delete

install: src/* indicator-ip.1 NEWS README
	install -d $(DESTDIR)$(SHAREDIR)/indicator-ip/IndicatorIp
	install -m 755 src/indicator-ip $(DESTDIR)$(SHAREDIR)/indicator-ip
	cp -r src/IndicatorIp $(DESTDIR)$(SHAREDIR)/indicator-ip
	install -d $(DESTDIR)$(MANDIR)/man1
	install -m 644 indicator-ip.1 $(DESTDIR)$(MANDIR)/man1
	rm -f indicator-ip.1

indicator-ip.1: README.md make-manpage.sh
	./make-manpage.sh README.md indicator-ip.1

NEWS: NEWS.md
	pandoc NEWS.md -t plain -o NEWS

README: README.md
	pandoc README.md -t plain -o README
	
upload:
	debuild -S
	dput ppa:bovender/bovender ../indicator-ip_*_source.changes
	rm ../indicator-ip_*_source.changes
