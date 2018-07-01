from struct import unpack as unp

def assemble_num(bits):
   '''
   assembly_num([0, 1]) => 2
   assembly_num([1, 1]) => 3
   assembly_num([1]*3)  => 7
   '''
   ret = 0
   po = 1
   for z in range(0, len(bits)):
      ret += bits[z] * po
      po *= 2
   return ret


#array of bytes, get bit offset from start
def get_bit_i(data, offset):
   byte_offset = offset // 8
   bit_offset = offset  - (byte_offset*8)

   #return body_data[byte_offset] & (i >> bit_offset)
   #return (body_data[byte_offset] >> (8 - bit_offset - 1)) << (8-1)

   byte = data[byte_offset]
   return (byte & (1 << bit_offset)) >> bit_offset

def unp_3b(x):
   short, byte = unp('>HB', x)
   return short | byte << 16

