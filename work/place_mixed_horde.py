import unreal, math, random, json
rng=random.Random(193)
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);cls=unreal.EditorAssetLibrary.load_blueprint_class('/Game/OneMoreTake/Blueprints/BP_WaveZombie')
target=unreal.EditorAssetLibrary.load_asset('/Game/Characters/Zombie/StylizedZombie/Textures/SZombie_Variant_1/SK_SZombie_Variant_1');material=unreal.EditorAssetLibrary.load_asset('/Game/Characters/Zombie/StylizedZombie/Textures/SZombie_Variant_1/SZombie_Variant_1');stand=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Animations/Retargeted/ZombieWaves/ZW_Zombie_Stand_Up_Anim')
existing={a.get_actor_label():a for a in sub.get_all_level_actors() if a.get_class()==cls}
points=[]
for ring,radius in enumerate([700,950,1200]):
 for j in range(9):
  angle=j*2*math.pi/9+ring*.21;x=-150+radius*math.cos(angle);y=750+radius*math.sin(angle)
  # Keep the market stall and the crown/finish route clear.
  if x>440 and 100<y<1250:y=80 if y<650 else 1320
  points.append((round(x),round(y)))
eligible=[i for i,(x,y) in enumerate(points) if math.hypot(x,y)>670]
chosen=[]
for angle in [0,math.pi/3,2*math.pi/3,math.pi,4*math.pi/3,5*math.pi/3]:
 def score(i):
  x,y=points[i];a=math.atan2(y-750,x+150);return abs(math.atan2(math.sin(a-angle),math.cos(a-angle)))+abs(math.hypot(x+150,y-750)-850)*.0003
 index=min((i for i in eligible if i not in chosen),key=score);chosen.append(index)
rest=[i for i in range(27) if i not in chosen];rng.shuffle(rest)
groups={1:chosen,2:rest[:9],3:rest[9:]};report=[]
for wave,indices in groups.items():
 rng.shuffle(indices)
 for order,index in enumerate(indices,1):
  x,y=points[index];label=f'Zombie_Wave{wave}_{order}';a=existing.get(label) or sub.spawn_actor_from_class(cls,unreal.Vector(x,y,92),unreal.Rotator())
  a.set_actor_label(label);a.set_actor_location(unreal.Vector(x,y,92),False,False);a.set_actor_rotation(unreal.Rotator(pitch=0,yaw=math.degrees(math.atan2(750-y,-150-x)),roll=0),False)
  a.set_editor_properties({'IsWaveZombie':True,'IsZombie':True,'ZombieWaveIndex':wave,'ZombieWakeOrder':order,'ExtraTakeTwoGuard':False})
  m=a.get_editor_property('Mesh');m.set_skeletal_mesh_asset(target);m.set_material(0,material);m.play_animation(stand,False);m.set_position(0,False);m.set_play_rate(0)
  data=m.get_editor_property('animation_data');data.set_editor_properties({'anim_to_play':stand,'saved_looping':False,'saved_playing':False,'saved_position':0.0,'saved_play_rate':0.0});m.set_editor_property('animation_data',data)
  for name in ['SwordRoot','GunMesh','ZombieLabel','MagicOrb']:a.get_editor_property(name).set_visibility(False,True)
  report.append({'label':label,'wave':wave,'order':order,'x':x,'y':y})
for a in sub.get_all_level_actors():
 if a.get_class().get_name()=='BP_TakeDirector_C':a.set_editor_property('WaveTriggerRadius',450.0)
font=unreal.EditorAssetLibrary.load_asset('/Game/Fonts/Alagard_World');mat=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Materials/M_AlagardWorldTextEngine')
for a in sub.get_all_level_actors():
 for c in a.get_components_by_class(unreal.TextRenderComponent):c.set_font(font);c.set_text_material(mat)
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
json.dump(report,open(unreal.Paths.project_dir()+'work/mixed-horde-layout.json','w'))
{'counts':{k:len(v) for k,v in groups.items()},'mixedBodies':len(report)}
