
from struct import unpack as unp

from utils import *
from mtypes import *
from helpers import *

####parser for MIDI format 1 (Simultaneous tracks)


def parse_meta_event(tr_data, meta_start):
   '''meta_start is after delta time
   tr_data[meta_start+1] == '0xFF'
   '''

   d = tr_data[meta_start:] #might be in-efficient but meh

   meta_e_type = None
   e = None
   e_extra = {}
   end = None

   meta_e_type = MetaEventType(int(d[1]))

   if meta_e_type == MetaEventType.SequenceNum and d[2] == 0x02:
      end = 4
      e = MeSeqNum._make(unp('>H'), d[3:end])
   elif meta_e_type == MetaEventType.Text:
      pass
   elif meta_e_type == MetaEventType.Copyright:
      pass
   elif meta_e_type == MetaEventType.SeqTrackName:
      pass
   elif meta_e_type == MetaEventType.InstrumentName:
      pass
   #...
   elif meta_e_type == MetaEventType.TimeSig and d[2] == 0x04:
      end = 7
      e = MeTimeSig._make(unp('>BBBB', d[3:end]))
      e_extra['time_sig'] = e.n/(2^e.b)
      pass
   elif meta_e_type == MetaEventType.KeySig and d[2] == 0x02:
      end = 5
      e = MeKeySig._make(unp('>BB', d[3:end]))

   print(meta_e_type, e, e_extra)

   return MetaEvent(meta_e_type, e, e_extra), (end + meta_start)



def parse_delta_and_event(tr_data, delta_start):

   def get_bit(offset):
      return get_bit_i(tr_data, offset)

   delta_done = False
   delta_acc = []
   delta_byte_i = delta_start
   delta_len = 0

   while not delta_done:
      print('doing delta')
      delta_done = get_bit(delta_byte_i*7) == 0
      for x in range(0, 7):
         delta_acc.append(get_bit(delta_byte_i*7+x))
      delta_len += 1

   delta_time = assemble_num(delta_acc)
   print(delta_time)

   print(tr_data[delta_start:delta_start+5])
   print(tr_data[delta_start+2]) #ff

   event_start = delta_start + delta_len
   if tr_data[event_start] == 0xFF:
      meta_e, e_end = parse_meta_event(tr_data, event_start)
   elif tr_data[event_start] == 0xF1:
      pass

   print(tr_data[e_end:e_end+5])

   return delta_time, meta_e, e_end



def parse_tracks1(midi_data):

   track_h_start = HEADER_SIZE #track header starts after file header
   track_header, tr_data = parse_track_head(midi_data, track_h_start)

   delta_time_1, meta_e_1, e_end_1 = parse_delta_and_event(tr_data, 0)
   print(delta_time_1, meta_e_1, e_end_1)
   delta_time_2, meta_e_2, e_end_2 = parse_delta_and_event(tr_data, e_end_1)
   print(delta_time_2, meta_e_2, e_end_2)



