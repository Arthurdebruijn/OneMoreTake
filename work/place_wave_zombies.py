import unreal
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);cls=unreal.EditorAssetLibrary.load_blueprint_class('/Game/OneMoreTake/Blueprints/BP_WaveZombie');target=unreal.EditorAssetLibrary.load_asset('/Game/Characters/Zombie/StylizedZombie/Textures/SZombie_Variant_1/SK_SZombie_Variant_1');material=unreal.EditorAssetLibrary.load_asset('/Game/Characters/Zombie/StylizedZombie/Textures/SZombie_Variant_1/SZombie_Variant_1');stand=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Animations/Retargeted/ZombieWaves/ZW_Zombie_Stand_Up_Anim')
existing={a.get_actor_label():a for a in sub.get_all_level_actors() if a.get_class()==cls}
layouts={1:[(-220,950),(0,1050),(220,950)],2:[(-420,1350),(-140,1450),(140,1450),(420,1350)],3:[(-600,1800),(-300,1900),(0,1950),(300,1900),(600,1800)]}
created=[]
for wave,positions in layouts.items():
 for order,(x,y) in enumerate(positions,1):
  label='Zombie_Wave'+str(wave)+'_'+str(order);actor=existing.get(label) or sub.spawn_actor_from_class(cls,unreal.Vector(x,y,92),unreal.Rotator(pitch=0,yaw=-90,roll=0));actor.set_actor_label(label);actor.set_editor_properties({'IsWaveZombie':True,'IsZombie':True,'ZombieWaveIndex':wave,'ZombieWakeOrder':order,'ExtraTakeTwoGuard':False})
  m=actor.get_editor_property('Mesh');m.set_skeletal_mesh_asset(target);m.set_material(0,material);m.play_animation(stand,False);m.set_position(0,False);m.set_play_rate(0)
  data=m.get_editor_property('animation_data');data.set_editor_properties({'anim_to_play':stand,'saved_looping':False,'saved_playing':False,'saved_position':0.0,'saved_play_rate':0.0});m.set_editor_property('animation_data',data)
  for name in ['SwordRoot','GunMesh','ZombieLabel','MagicOrb']:actor.get_editor_property(name).set_visibility(False,True)
  created.append(actor.get_actor_label())
for actor in sub.get_all_level_actors():
 if actor.get_class().get_name()=='BP_TakeDirector_C':actor.set_editor_properties({'WaveTriggerRadius':700.0,'WaveRiseInterval':.55})
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level();{'placed':created}
