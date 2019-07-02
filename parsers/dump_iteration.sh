#!/bin/bash
FILES="enwiki-20150403-pages-meta-history20.xml-p011125001p011424955.bz2
enwiki-20150403-pages-meta-history20.xml-p011424972p011880102.bz2
enwiki-20150403-pages-meta-history20.xml-p011880103p012229210.bz2
enwiki-20150403-pages-meta-history20.xml-p012229211p012697370.bz2
enwiki-20150403-pages-meta-history20.xml-p012697371p013086693.bz2
enwiki-20150403-pages-meta-history20.xml-p013086694p013324998.bz2"
BASEURL="http://dumps.wikimedia.org/enwiki/20150403/"
for f in $FILES
do
    echo "Processing $f"
    wget -c "$BASEURL$f"
    python processing/botlike_sampling.py "$f" >> logfile.txt
    rm -f "$f"
done
