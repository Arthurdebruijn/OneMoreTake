import unreal, wave, math, random, struct
from pathlib import Path
root=Path(unreal.Paths.project_dir())/'work';rate=44100;rng=random.Random(74)
def save(name,samples):
 peak=max(abs(s) for s in samples) or 1
 with wave.open(str(root/(name+'.wav')),'wb') as f:
  f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate);f.writeframes(b''.join(struct.pack('<h',round(max(-1,min(1,s/peak*.82))*32767)) for s in samples))
 task=unreal.AssetImportTask();task.set_editor_properties({'filename':str(root/(name+'.wav')),'destination_path':'/Game/OneMoreTake/Audio','destination_name':name,'automated':True,'save':True});unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task]);assert task.get_objects()
# A compact pistol crack, a low report, then a short metallic tail.
samples=[];last=0
for i in range(round(rate*.3)):
 t=i/rate;n=rng.uniform(-1,1);last=.72*last+.28*n
 crack=(n-last)*math.exp(-t/0.009)*1.15
 body=math.sin(2*math.pi*(145*t-65*t*t))*math.exp(-t/.045)*.5
 tail=last*math.exp(-t/.065)*.75
 samples.append((crack+body+tail)*min(t/.0007,1))
save('S_PistolShot',samples)
# Cylinder latch, opening movement, cartridge clicks, and a firm closing clack.
samples=[0.0]*round(rate*1.8)
for start,duration,freq,amp in [(.12,.065,1900,.5),(.3,.12,750,.3),(.62,.045,2800,.35),(.77,.045,3200,.32),(.92,.045,2600,.32),(1.32,.14,650,.6),(1.53,.065,1800,.4)]:
 for i in range(round(duration*rate)):
  t=i/rate;env=(1-math.exp(-t/.0015))*math.exp(-t/(duration*.2));value=(rng.uniform(-1,1)*.55+math.sin(2*math.pi*freq*t)*.35+math.sin(2*math.pi*freq*.53*t)*.1)*env*amp
  samples[round(start*rate)+i]+=value
save('S_PistolReload',samples)
'Imported distinct pistol shot and reload sounds'
