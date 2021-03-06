import enum
from collections import namedtuple


class ChunkType(enum.Enum):
   HEADER = 0
   TRACK = 1
   UNKNOWN = 2

class DivisionType(enum.Enum):
   TPQN = 0 #tickes per quarter note
   FPS = 1 #frames/second, ticks/frame
   UNKNOWN = 2

class MidiFormat(enum.Enum):
   SINGLE_TRACK  = 0
   SIMULT_TRACKS = 1
   MANY_TRACKS   = 2
   UNKNOWN       = 3

HeaderChunk = namedtuple('HeaderChunk', 'chunk_type_b len format tracks division')

TrackHeader = namedtuple('TrackHeader', 'chunk_type_b len')




##############EVENTS

#class MetaEvent:
'''class EventName(enum.Enum):
   SequenceNum
'''



class MetaEventType(enum.Enum):
   SequenceNum = 0x0
   Text = 0x1
   Copyright = 0x2
   SeqTrackName = 0x3
   InstrumentName = 0x4
   Lyric = 0x5
   Marker = 0x06
   CuePoint = 0x07
   ChannelPrefix = 0x20
   KkTrackStart = 0x21
   EndOfTrack = 0x2F
   SetTempo = 0x51
   SMTPE_offset = 0x54
   TimeSig = 0x58
   KeySig = 0x59

#Me = Meta Event
MeSeqNum = namedtuple('MeSeqNum', 'seq_num')
MeSeqTrackName = namedtuple('MySeqTrackName', 'len name')
MeTrackStart = namedtuple('MeTrackStart', 'x')
MeEndOfTrack = namedtuple('MeEndOfTrack', '')
MeSetTempo = namedtuple('MeSetTempo', 'tt')

MeTimeSig = namedtuple('MeTimeSig', 'n d c b')
MeKeySig = namedtuple('MeKeySig', 'sf mi')


class MetaEvent:
   def __init__(self, e_type, e, e_extra=None):
      self.e_type = e_type
      self.e = e
      self.e_extra = e_extra
   def __repr__(self):
      fmt_args = [self.e_type, self.e, self.e_extra]
      fmt_args = tuple(list(map(lambda x: str(x), fmt_args)))
      return '%s %s %s' % fmt_args
   pass


