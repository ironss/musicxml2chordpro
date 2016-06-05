#! /usr/bin/env python3

""" Convert MusicXML to Chordpro
"""


import xml.etree.ElementTree as ET


# Translate MusicXML chord quality to Chordpro
qualities = {
   'augmented': '+',
   'diminished': 'dim',
   'dominant': '7',
   'dominant-ninth': '9',
   'major': '' ,
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


def xml2pro(filename, fout):
    tree = ET.parse(filename)
    root = tree.getroot()

    # Get the song name
    title_element = root.find('work/work-title')
    title = title_element.text
    fout.write('{{title:{title}}}\n'.format(title=title))

    # Get a list of all of the parts
    partlists = root.findall('part-list/score-part')
    for part in partlists:
        part_id = part.attrib['id']
        part_name = part.find('part-name')

    # Then ignore the parts in the part list, and just go through the children.

    parts = root.findall('part')
    part = parts[0] # This score has a single part. We should be doing this for each part

    # Assume that the first key signature is the key for the song
    key_index = int(part.find('measure/attributes/key/fifths').text)
    key = keys[key_index]
    fout.write('{{key:{kmaj} {kmin}}}\n'.format(kmaj=key[0], kmin=key[1]))

    # End of the header info, about to start with the chords and music.
    fout.write('\n')

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
                quality = child.find('kind').text
                q_code = qualities[quality]
                chord = chord_root + q_code

                # If we have to print a chord in the middle of a word,
                # insert a dash/hyphen before the chord
                if stype in ['begin', 'middle']:
                    fout.write('-')
                fout.write('[{chord}]'.format(chord=chord))
            elif child.tag == 'note':
                lyrics = child.findall('lyric[@number="1"]')
                for l in lyrics:
                    stype = l.find('syllabic').text
                    syllable = l.find('text').text
                    fout.write(syllable)
                    # If this is a single syllable word, or the end of a word, print a space
                    if stype in ['single', 'end']:
                       fout.write(' ')

        # Every 4 bars, start a new line
        if measure_number % 4 == 0:
           fout.write('\n')


if __name__ == '__main__':
    import sys
    fout = sys.stdout
    filename = 'test/An Affair to Remember.xml'
    xml2pro(filename, fout)

