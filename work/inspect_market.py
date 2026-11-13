import struct,zlib,pathlib,json
b=pathlib.Path('work/market-source-texture.png').read_bytes();at=8;raw=b''
while at+12<=len(b):
 n=struct.unpack_from('>I',b,at)[0];t=b[at+4:at+8];data=b[at+8:at+8+n];at+=12+n
 if t==b'IHDR':w,h,depth,color,*_=struct.unpack('>IIBBBBB',data)
 if t==b'IDAT':raw+=data
print('PNG',w,h,depth,color)
assert depth==8 and color in (2,6)
channels=4 if color==6 else 3;stride=w*channels;data=zlib.decompress(raw);rows=[];prev=[0]*stride;at=0
for y in range(h):
 f=data[at];at+=1;row=list(data[at:at+stride]);at+=stride
 for x in range(stride):
  a=row[x-channels] if x>=channels else 0;b=prev[x];c=prev[x-channels] if x>=channels else 0
  if f==1:v=a
  elif f==2:v=b
  elif f==3:v=(a+b)//2
  elif f==4:
   p=a+b-c;pa,pb,pc=abs(p-a),abs(p-b),abs(p-c);v=a if pa<=pb and pa<=pc else b if pb<=pc else c
  else:v=0
  row[x]=(row[x]+v)%256
 rows.append(row);prev=row
print('alpha rows',[(y,sum(rows[y][x*channels+3]==0 for x in range(w))) for y in range(h)] if channels==4 else 'opaque')

