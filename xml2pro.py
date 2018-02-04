#! /usr/bin/env python3

""" Convert MusicXML to Chordpro
"""


import xml.etree.ElementTree as ET


# Translate MusicXML chord quality to Chordpro
qualities = {
   'augmented': '+',
   'diminished': 'dim',
   'diminished-seventh': 'dim7',
   'dominant': '7',
   'dominant-ninth': '9',
   'half-diminished': 'm7b5',
   'major': '' ,
   'major-seventh': 'M7',
   'minor': 'm',
   'minor-seventh': 'm7',
   'minor-sixth': 'm6',
}

# MusicXML knows the number of sharps or flats in the key signature.
# It does not know whether it is the major or relative minor key.
# We might try to guess later.
keys = {
   -7: ('Cb', 'Abmin'),
   -6: ('Gb', 'Ebmin'),
   -5: ('Db', 'Bbmin'),
   -4: ('Ab', 'Fmin'),
   -3: ('Eb', 'Cmin'),
   -2: ('Bb', 'Gmin'),
   -1: ('F', 'Dmin'),
    0: ('C', 'Amin'),
    1: ('G', 'Emin'),
    2: ('D', 'Bmin'),
    3: ('A', 'Fmin'),
    4: ('E', 'C#min'),
    5: ('B', 'G#min'),
    6: ('F#', 'D#min'),
    7: ('C#', 'A#min'),
}


alters = {
   -2: 'bb',
   -1: 'b',
    0: '',
    1: '#',
    2: '##',
}

class XML2Pro:
    def __init__(self, data, fout):
        self.data = data
        self.fout = fout

    def process_file(self):
        self.tree = ET.parse(self.data)
        self.root = self.tree.getroot()

        self.process_root()

    def process_root(self):
        # Get the song name
        title_element = self.root.find('work/work-title')
        self.title = title_element.text
        if title_element != None:
            self.write('{{title:{title}}}\n'.format(title=self.title))

        # Get a list of all of the parts
        partlists = self.root.findall('part-list/score-part')
        for part in partlists:
            part_id = part.attrib['id']
            part_name = part.find('part-name')

        # Then ignore the parts in the part list, and just go through the children.

        self.parts = self.root.findall('part')
        for part in self.parts:
            self.process_part(part)


    def process_part(self, part):
        # Assume that the first key signature is the key for the song
        key_index = int(part.find('measure/attributes/key/fifths').text)
        key = keys[key_index]
        self.write('{{key:{kmaj} {kmin}}}\n'.format(kmaj=key[0], kmin=key[1]))

        # End of the header info, about to start with the chords and music.
        self.write('\n')

        # Process each line of lyrics.
        # Need to work out how many lines there are...
        self.process_line(part, '1')
        self.process_line(part, '2')


    def process_line(self, part, line):
        # Process all measure in this part.
        measures = part.findall('measure')  # Assume measures are sorted. We should really sort them by attribute 'number'


        # Go through each measure, looking for
        #   'harmony', which tells us the chord to use for the next note
        #   'note', which has a lyric syllable attached to it

        stype = ''  # Type of syllable: single, start, middle or end.
        for m in measures:
            measure_number = int(m.get('number'))
            for child in m:
                if child.tag == 'harmony':
                    chord_root = child.find('root/root-step').text
                    try:
                       chord_alter = child.find('root/root-alter').text
                       alter = alters[int(chord_alter)]
                    except AttributeError, KeyError:
                       alter = ''
                    quality = child.find('kind').text
                    q_code = qualities[quality]
                    chord = chord_root + alter + q_code

                    # If we have to print a chord in the middle of a word,
                    # insert a dash/hyphen before the chord
                    if stype in ['begin', 'middle']:
                        self.write('-')
                    self.write('[{chord}]'.format(chord=chord))
                elif child.tag == 'note':
                    lyrics = child.findall('lyric[@number="{}"]'.format(line))
                    for l in lyrics:
                        stype = l.find('syllabic').text
                        syllable = l.find('text').text
                        self.write(syllable)
                        # If this is a single syllable word, or the end of a word, print a space
                        if stype in ['single', 'end']:
                            self.write(' ')

            self.write('[|]')

            # Every 4 bars, start a new line
            if measure_number % 4 == 0:
               self.write('\n')
        self.write('\n')

    def write(self, data):
        self.fout.write(data.encode('utf-8'))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Extract chords and lyrics from MusicXML file.')
    parser.add_argument('filenames', metavar='file', nargs='+', default='-', help='a MusicXML file to process')

    args = parser.parse_args()

    import sys
    fout = sys.stdout
    for filename in args.filenames:
        if filename == '-':
            data = sys.stdin
        else:
            data = filename
        x1 = XML2Pro(data, fout)
        x1.process_file()

