
from struct import unpack as unp

from mtypes import *


HEADER_SIZE = 14


def parse_track_head(midi_data, track_h_start):
   track_h_end = track_h_start + 8

   track_h_bytes = midi_data[track_h_start:track_h_end]
   track_h_parsed = unp('>4sL', track_h_bytes)
   track_header = TrackHeader._make(track_h_parsed)
   print('track header:', track_header)

   #track data
   track_start = track_h_end
   track_end  = track_start + track_header.len #track_end
   tr_data = midi_data[track_start:track_end] #track body data

   return track_header, tr_data


