
from struct import unpack as unp

from utils import *
from mtypes import *
from helpers import *

####parser for MIDI format 1 (Simultaneous tracks)


def parse_meta_event(tr_data, meta_start):
   '''meta start is after delta time
   tr_data[meta_start+1] == '0xFF'
   '''
   s = meta_start
   d = tr_data[s:]

   meta_e_type = None
   e = None
   e_extra = {}
   end = None

   meta_e_type = MetaEventType(int(d[s+2]))

   if meta_e_type == MetaEventType.SequenceNum and d[s+3] == 0x02:
      e = MeSeqNum._make(unp('>H'), d[s+4:s+5])
      end = 5
   elif meta_e_type == MetaEventType.Text:
      pass
   elif meta_e_type == MetaEventType.Copyright:
      pass
   elif meta_e_type == MetaEventType.SeqTrackName:
      pass
   elif meta_e_type == MetaEventType.InstrumentName:
      pass
   #...
   elif meta_e_type == MetaEventType.TimeSig and d[s+3] == 0x04:
      e = MeTimeSig._make(unp('>BBBB', d[s+4:s+8]))
      e_extra['time_sig'] = e.n/(2^e.b)
      end = 8
      pass

   print(meta_e_type, e, e_extra)
   end = None

   return MetaEvent(meta_e_type, e, e_extra), end
   pass

def parse_tracks1(midi_data):

   track_h_start = HEADER_SIZE #track header starts after file header
   track_header, tr_data = parse_track_head(midi_data, track_h_start)

   def get_bit(offset):
      return get_bit_i(tr_data, offset)

   delta_done = False
   delta_acc = []
   delta_byte_i = 0

   while not delta_done:
      print('doing')
      delta_done = get_bit(delta_byte_i*7) == 0
      for x in range(0, 7):
         delta_acc.append(get_bit(delta_byte_i*7+x))
   delta_time = assemble_num(delta_acc)
   print(delta_time)

   print(tr_data[0:5])
   print(tr_data[2]) #ff

   if tr_data[1] == 0xFF:
      print('meta event: ff found')
      meta_e, e_end = parse_meta_event(tr_data, 0)
   elif tr_data[1] == 0xF1:
      pass

   print(

   pass

