#!/usr/bin/python3

from utiltools import shellutils as shu
from struct import unpack as unp

from mtypes import *
from utils import *

import parse_simult

class FileHeaderParser:

   def __init__(self, midi_data):
      self.midi_data = midi_data
      self.parse_chunk()
      self.print_info()

   def parse_chunk(self):
      i = 0
      size = 14
      self.header = HeaderChunk._make(unp('>4sLHHH', self.midi_data[:size]))
      i += size

      self.chunk_type = parse_chunk_type(self.header.chunk_type_b)
      self.division_type, self.tpqn, self.fps = FileHeaderParser.get_division_info_(self.header)
      self.midi_format = MidiFormat(self.header.format)

   def print_info(self):
      print('chunk type:', self.chunk_type)
      print(self.header)
      print('ticks per quarter note:', self.tpqn)
      print('midi format:', self.midi_format)

   def get_division_info_(header):
      division_type_bit = header.division & (1 << 15)
      division_type = DivisionType(division_type_bit)

      tpqn = None
      fps = None

      print(division_type)
      if division_type == DivisionType.TPQN:
         tpqn = header.division << 1
      else:
         raise 'Unsupported division type'
      return division_type, tpqn, fps

   pass




def parse_midi_file(file_path):

   data = shu.read_file(file_path, binary=True)

   print('===parsing file header chunk')
   header_chunk = FileHeaderParser(data)
   print('===end parsing file header chunk\n')

   if header_chunk.midi_format == MidiFormat.SINGLE_TRACK:
      pass
   elif header_chunk.midi_format == MidiFormat.SIMULT_TRACKS:
      parse_simult.parse_tracks1(data)
   elif header_chunk.midi_format == MidiFormat.MANY_TRACKS:
      pass

   return header_chunk, data



def get_song_names():
   return shu.ls('songs')

def check_all_songs():
   song_names = get_song_names()
   for song_name in song_names:
      song_path = 'songs/' + song_name
      header_chunk, song1_bin = parse_midi_file(song_path)
#check_all_songs()


song_path = 'songs/confuta.mid'
#song_path = '~/Downloads/sarahs-woven-music.1.mid'
#song_path = '~/Downloads/Adeste_Fideles_sheet_music_sample.mid'
#song_path = '~/Downloads/test.mid'
header_chunk, song1_bin = parse_midi_file(song_path)


