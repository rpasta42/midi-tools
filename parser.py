#!/usr/bin/python3

from utiltools import shellutils as shu
from struct import unpack as unp


from collections import namedtuple


def parse_chunk_type(data):
   chunk_type_b = data[:4]
   chunk_type = None
   if chunk_type_b == 'MThd':
      chunk_type = 'header'
   elif chunk_type_b == 'MTrk':
      chunk_type = 'track'

   return chunk_type, chunk_type_b



def unp_6b(x):
   s, i = unp('>IH', x)
   return s | (i << 16)

def parse_chunk(chunk_data):
   i = 0
   chunk_type, chunk_type_b = parse_chunk_type(chunk_data)
   i += 4
   print('chunk type:', chunk_type_b, chunk_type)


   chunk_len = unp('>L', chunk_data[i:i+4])[0]
   i += 4
   print('chunk len:', chunk_len)


   format_, track, division = unp('>HHH', chunk_data[i:i+6])
   i += 6
   print('h data', format_, track, division)


   return chunk_data


def parse_midi_file(file_path):

   data = shu.read_file(file_path, binary=True)

   HeaderChunk = namedtuple('HeaderChunk', 'chunk_type len format tracks division')
   header = HeaderChunk._make(unp('>4sLHHH', data[:14]))
   print(header)


   return parse_chunk(data)


song1 = parse_midi_file('songs/confuta.mid')


