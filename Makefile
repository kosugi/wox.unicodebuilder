
.PHONY: all clean test install

OBJDIR=./build

all: $(OBJDIR)/icon.png $(OBJDIR)/db

$(OBJDIR)/unicodebuilder.wox:


$(OBJDIR)/unicodequery.wox: $(OBJDIR)/icon.png $(OBJDIR)/db clipboard.py main_query.py plugin.query.json lib.py query.py
	mkdir -p $(OBJDIR)/b.wox
	cp plugin.query.json $(OBJDIR)/b.wox/plugin.json
	cp $(OBJDIR)/icon.png $(OBJDIR)/db clipboard.py main_query.py lib.py query.py $(OBJDIR)/b.wox
	zip -j $@ $(OBJDIR)/b.wox/*

$(OBJDIR)/icon.png: icon.svg
	@[ -d $(OBJDIR) ] || mkdir -p $(OBJDIR)
	convert -background None icon.svg $@

$(OBJDIR)/NamesList.txt:
	@[ -d $(OBJDIR) ] || mkdir -p $(OBJDIR)
	wget -O $(OBJDIR)/$(@F) http://unicode.org/Public/UNIDATA/NamesList.txt

$(OBJDIR)/db: $(OBJDIR)/NamesList.txt make-db.py
	python make-db.py

clean:
	rm -rf *.pyc $(OBJDIR)/*
