from mido import MidiFile
import sys
if len(sys.argv) > 1:
    song = sys.argv[1]
else:
    song = raw_input('Song to dump: ')
for msg in MidiFile(song):
    print msg
