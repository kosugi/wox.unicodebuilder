
.PHONY: all clean test install

OBJDIR=./build

all: $(OBJDIR)/unicodebuilder.wox $(OBJDIR)/unicodequery.wox

install: $(OBJDIR)/unicodebuilder.wox $(OBJDIR)/unicodequery.wox
	@[ -d "$(WOX_PLUGIN_DIR)" ] || (echo "WOX_PLUGIN_DIR not defined or bad directory" && exit 1)
	mkdir -p $(WOX_PLUGIN_DIR)/unicodebuilder
	rsync -r build/b.wox/ $(WOX_PLUGIN_DIR)/unicodebuilder/
	mkdir -p $(WOX_PLUGIN_DIR)/unicodequery
	rsync -r build/q.wox/ $(WOX_PLUGIN_DIR)/unicodequery/

$(OBJDIR)/unicodebuilder.wox: $(OBJDIR)/icon.png $(OBJDIR)/db clipboard.py main_builder.py plugin.builder.json lib.py builder.py
	mkdir -p $(OBJDIR)/b.wox
	cp plugin.builder.json $(OBJDIR)/b.wox/plugin.json
	cp $(OBJDIR)/icon.png $(OBJDIR)/db clipboard.py main_builder.py lib.py builder.py $(OBJDIR)/b.wox
	zip -j $@ $(OBJDIR)/b.wox/*

$(OBJDIR)/unicodequery.wox: $(OBJDIR)/icon.png $(OBJDIR)/db clipboard.py main_query.py plugin.query.json lib.py query.py
	mkdir -p $(OBJDIR)/q.wox
	cp plugin.query.json $(OBJDIR)/q.wox/plugin.json
	cp $(OBJDIR)/icon.png $(OBJDIR)/db clipboard.py main_query.py lib.py query.py $(OBJDIR)/q.wox
	zip -j $@ $(OBJDIR)/q.wox/*

$(OBJDIR)/icon.png: icon.svg
	@[ -d "$(OBJDIR)" ] || mkdir -p $(OBJDIR)
	convert -background None icon.svg $@

$(OBJDIR)/NamesList.txt:
	@[ -d "$(OBJDIR)" ] || mkdir -p $(OBJDIR)
	wget -O $(OBJDIR)/$(@F) http://unicode.org/Public/UNIDATA/NamesList.txt

$(OBJDIR)/db: $(OBJDIR)/NamesList.txt make-db.py
	python make-db.py

clean:
	rm -rf *.pyc $(OBJDIR)/*
