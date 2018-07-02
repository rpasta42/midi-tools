
from struct import unpack as unp

from utils import *
from mtypes import *
from helpers import *

####parser for MIDI format 1 (Simultaneous tracks)



def parse_mode_voice_event(tr_data, event_start):

   d = tr_data[event_start:] #in-efficient

   print('first 2 bytes:', d[0:2])
   print('first 2 bytes ints:', d[0], d[1])
   print('hex 1:', format(d[0], '02x'))
   print('hex 2:', format(d[1], '02x'))

   e = None
   e_end = None

   return e, e_end


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
   elif meta_e_type == MetaEventType.KkTrackStart and d[2] == 0x1:
      end = 4
      e = MeTrackStart._make(unp('>B', d[3:end]))
   elif meta_e_type == MetaEventType.EndOfTrack and d[2] == 0x0:
      end = 3
      e = MeEndOfTrack()
   elif meta_e_type == MetaEventType.SetTempo and d[2] == 0x03:
      end = 6
      e = MeSetTempo._make((unp_3b(d[3:end]), ))
   elif meta_e_type == MetaEventType.TimeSig and d[2] == 0x04:
      end = 7
      e = MeTimeSig._make(unp('>BBBB', d[3:end]))
      e_extra['time_sig'] = e.n/(2^e.b)
   elif meta_e_type == MetaEventType.KeySig and d[2] == 0x02:
      end = 5
      e = MeKeySig._make(unp('>BB', d[3:end]))
   else:
      print('unknown meta event')

   print(meta_e_type, e, e_extra)
   #print('kk:', d[:10])

   return MetaEvent(meta_e_type, e, e_extra), (end + meta_start)


def parse_delta(tr_data, delta_start):

   def get_bit(offset):
      return get_bit_i(tr_data, offset)

   delta_done = False
   delta_acc = []
   delta_byte_i = delta_start
   delta_len = 0

   while not delta_done:
      delta_done = get_bit(delta_byte_i*8+7) == 0

      r = list(range(0, 7))
      r.reverse()
      for x in r:
         delta_acc.append(get_bit(delta_byte_i*8+x))

      delta_len += 1
      delta_byte_i += 1

   delta_acc.reverse()
   delta_time = assemble_num(delta_acc)

   return delta_time, delta_len


def parse_delta_and_event(tr_data, delta_start):

   delta_time, delta_len = parse_delta(tr_data, delta_start)
   print('delta time:', delta_time)

   event_start = delta_start + delta_len
   #print('event start byte:', tr_data[event_start])

   if tr_data[event_start] == 0xFF:
      print('meta event:', format(tr_data[event_start], '02x'))
      print('meta event type: ', format(tr_data[event_start+1], '02x'))
      print('meta event len: ', format(tr_data[event_start+2], '02x'))

      meta_e, e_end = parse_meta_event(tr_data, event_start)
   elif tr_data[event_start] in [0xF0, 0xF7]:
      print('sysex event')
   else:
      print(tr_data[event_start])
      print('prolly Channel Mode/Voice message')
      #TODO: not meta_e!!
      meta_e, e_end = parse_mode_voice_event(tr_data, event_start)


   print(tr_data[e_end:e_end+5])

   return delta_time, meta_e, e_end



def parse_sound_track(midi_data, start):
   print('=======================')
   print(start)
   track_header, tr_data = parse_track_head(midi_data, start)

   x = parse_chunk_type(track_header.chunk_type_b)
   print(x)

   delta_start = 0
   delta_time, delta_len = parse_delta(tr_data, delta_start)

   event_start = delta_start + delta_len
   print(tr_data[event_start:event_start+5])

   if tr_data[event_start] == 0xFF:

      meta_e, e_end = parse_meta_event(tr_data, event_start)
   elif tr_data[event_start] in [0xF0, 0xF7]:
      print('sysex event')
   else:
      print(tr_data[event_start])
      print('prolly Channel Mode/Voice message')
      #TODO: not meta_e!!
      meta_e, e_end = parse_mode_voice_event(tr_data, event_start)


   print(tr_data[e_end:e_end+5])

   return delta_time, meta_e, e_end

   pass


def parse_tracks1(midi_data):

   track_h_start = HEADER_SIZE #track header starts after file header
   track_header, tr_data = parse_track_head(midi_data, track_h_start)

   start = 0
   done = False
   delta_times, events = ([], [])

   while not done: #meta track
      print('====')
      delta_time, meta_e, e_end = parse_delta_and_event(tr_data, start)
      print(delta_time, meta_e, e_end)
      delta_times.append(delta_time)
      events.append(meta_e)
      start = e_end

      print(start, track_header.len)
      if start >= track_header.len:
         done = True
      #if start >= 478:
      #   done = True

      pass

   parse_sound_track(midi_data, track_h_start + track_header.len + 8)

   '''print(tr_data[start:start+5])
   print(' '.join([str(x) for x in tr_data[start:start+5]]))
   print(' '.join(str(get_bit_i(tr_data[start:], i)) for i in range(0, 8)))'''

   pass


