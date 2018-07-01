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

def rev_bits(n):
   return int('{:08b}'.format(n)[::-1], 2)

def unp_3b(x):
   b1 = unp('>B', x[0:1])[0]
   b2 = unp('>B', x[1:2])[0]
   b3 = unp('>B', x[2:3])[0]

   b1 = b1 #>> 2
   b2 = b2 #rev_bits(b2) #>> 2

   #x = bytes([b, s & 0x00FF, (s>>8) & 0x00ff])
   x = bytes([b1, b2, b3])

   print(''.join([str(get_bit_i(x, i)) for i in range(0,8)]))
   print(''.join([str(get_bit_i(x, i)) for i in range(8,16)]))
   print(''.join([str(get_bit_i(x, i)) for i in range(16,24)]))


   #ret = b << 16 | s #s | b >> 16 #short | byte << 16
   #ret = b1 | b2 << 8 | b3 << 16
   ret = b1 << 16 | b2 << 8 | b3
   print(ret)
   return ret


