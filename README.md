# musicxml2chordpro
Extract chord charts from MusicXML files


## Proposed usage

* Create score in Musescore

* Export to MusicXML file
      musescore -o Song_name.xml Song_Name.mscz

* Create Chordpro file
      python xml2pro.py Song_name.xml > Song_name.pro

* Transfer Chordpro file to tablet, where Songbook can 
  read it.
  
* Alternatively, use Chordii to create Postscript file
  for printing.
      chordii Song_name.pro > Song_name.ps
      


## Issues

* Does not know where to break a line. Sometimes, a line break
  every 4 bars is OK, sometimes it would be better every 2 bars.
  
* Poor line breaks for pickup bars. The line break algorithm
  always puts in a line break at the start of a bar. However, 
  for pickups, it would be better to break the line on the 
  up-beat, so that the lyrical phrase is printed as a single
  line.
  
* Does not handle multiple lines of lyrics well. If there 
  are multiple verses, each on a separate lyric line, and a
  single chorus line, it makes a bit of a hash.

* Does not handle repeats, first- and second-time endings, 
  codas, and other form markings.


