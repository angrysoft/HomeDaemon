path = www/static
dart = dart2js -m -o
sasss = sassc -t compressed
INSTALL=install -C
USR=nginx
GRP=uwsgi

all: alldart allcss

alldart: leds main rf rfpilot

leds: $(path)/leds.dart
	$(dart) $(path)/leds.dart.js $(path)/leds.dart

main: $(path)/main.dart
	$(dart) $(path)/main.dart.js $(path)/main.dart

rf: $(path)/rf.dart
	$(dart) $(path)/leds.dart.js $(path)/leds.dart

rfpilot: $(path)/rfpilot/rfpilot.dart
	$(dart) $(path)/rfpilot/rfpilot.dart.js $(path)/rfpilot/rfpilot.dart
	$(dart) $(path)/rfpilot/sw.dart.js $(path)/rfpilot/sw.dart

tvpilot: $(path)/tvpilot/tvpilot.dart
	$(dart) $(path)/tvpilot/tvpilot.dart.js $(path)/tvpilot/tvpilot.dart
	$(dart) $(path)/tvpilot/sw.dart.js $(path)/tvpilot/sw.dart

allcss: stylescss rfpilotcss

stylescss: $(path)/styles.css
	sassc -t compressed $(path)/styles.css $(path)/styles.min.css

rfpilotcss: $(path)/rfpilot/rfpilot.scss
	sassc -t compressed $(path)/rfpilot/rfpilot.scss $(path)/rfpilot/rfpilot.min.css

tvpilotcss: $(path)/tvpilot/tvpilot.scss
	sassc -t compressed $(path)/tvpilot/tvpilot.scss $(path)/tvpilot/tvpilot.min.css

install:
	$(INSTALL) -d -m 755 $(DESTDIR)/var/www/smarthouse/{static,templates}
	$(INSTALL) -g $(USR) -o $(GRP) src/static/* $(DESTDIR)/var/www/smarthouse/static/
	#$(INSTALL) -g $(USR) -o $(GRP) src/static/*.dart $(DESTDIR)/var/www/smarthouse/static/
	#$(INSTALL) --g $(USR) -o $(GRP) src/static/*.dart.js $(DESTDIR)/var/www/smarthouse/static/
	#$(INSTALL) -g $(USR) -o $(GRP) src/static/*.css $(DESTDIR)/var/www/smarthouse/static/
	# templates
	$(INSTALL) -g $(USR) -o $(GRP) src/templates/*.html $(DESTDIR)/var/www/smarthouse/templates/
	# server file
	$(INSTALL) -g $(USR) -o $(GRP) -m 755 src/SmartHouse.py $(DESTDIR)/var/www/smarthouse/
	# daemon files
	$(INSTALL) -d -m 755 $(DESTDIR)/usr/bin
	$(INSTALL) -d -m 755 $(DESTDIR)/usr/lib/systemd/system
	$(INSTALL) -m 755 src/housed.py $(DESTDIR)/usr/bin
	$(INSTALL) -m 644 housed.service $(DESTDIR)/usr/lib/systemd/system
	# config files
	$(INSTALL) -d -m 755 $(DESTDIR)/etc/smarthouse
	$(INSTALL) -m 755 files/*.json $(DESTDIR)/etc/smarthouse/

uninstall:
	rm -rf $(DESTDIR)/var/www/smarthouse
	rm -f $(DESTDIR)/usr/lib/systemd/system/housed.service
	rm -f $(DESTDIR)/usr/bin/housed.py
