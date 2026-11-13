import unreal,json
folder='/Game/OneMoreTake/Animations/Retargeted/ZombieWaves/'
target=unreal.EditorAssetLibrary.load_asset('/Game/Characters/Zombie/StylizedZombie/Textures/SZombie_Variant_1/SK_SZombie_Variant_1')
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);tmp=sub.spawn_actor_from_class(unreal.SkeletalMeshActor,unreal.Vector(10000,0,1000),unreal.Rotator());mesh=tmp.get_component_by_class(unreal.SkeletalMeshComponent);mesh.set_skeletal_mesh_asset(target)
paths=json.load(open(unreal.Paths.project_dir()+'work/zombie_wave_assets.json'))['animations'];report={}
for path in paths:
 a=unreal.EditorAssetLibrary.load_asset(path);count=round(a.get_play_length()*30)+1;poses=[unreal.AnimPoseExtensions.get_anim_pose_at_time(a,i/30,unreal.AnimPoseEvaluationOptions()) for i in range(count)]
 children=[str(b) for b in unreal.AnimPoseExtensions.get_bone_names(poses[0]) if str(mesh.get_parent_bone(b))=='RL_BoneRoot'];roots=[unreal.AnimPoseExtensions.get_bone_pose(p,'RL_BoneRoot',unreal.AnimPoseSpaces.LOCAL) for p in poses];tracks={}
 for b in children:
  values=[]
  for p,r in zip(poses,roots):
   parent=unreal.Transform();parent.translation=unreal.Vector(r.translation.x if 'Stand_Up' in path else 0,r.translation.y if 'Stand_Up' in path else 0,r.translation.z);parent.rotation=r.rotation;parent.scale3d=r.scale3d;values.append(unreal.AnimPoseExtensions.get_bone_pose(p,b,unreal.AnimPoseSpaces.LOCAL).multiply(parent))
  tracks[b]=values
 ctrl=a.get_editor_property('controller');ctrl.open_bracket('Ground zombie animation and remove locomotion travel')
 for b,values in tracks.items():assert ctrl.set_bone_track_keys(b,[t.translation for t in values],[t.rotation for t in values],[t.scale3d for t in values])
 assert ctrl.set_bone_track_keys('RL_BoneRoot',[unreal.Vector()]*count,[unreal.Quat(0,0,0,1)]*count,[unreal.Vector(1,1,1)]*count);ctrl.close_bracket();a.set_editor_properties({'enable_root_motion':False,'force_root_lock':True,'root_motion_root_lock':unreal.RootMotionRootLock.REF_POSE});assert unreal.EditorAssetLibrary.save_loaded_asset(a)
 if 'Punching' in path or 'Kicking' in path:
  candidates=[]
  for i in range(count):
   p=unreal.AnimPoseExtensions.get_anim_pose_at_time(a,i/30,unreal.AnimPoseEvaluationOptions());hip=unreal.AnimPoseExtensions.get_bone_pose(p,'CC_Base_Hip',unreal.AnimPoseSpaces.WORLD).translation
   bones=['CC_Base_L_Hand','CC_Base_R_Hand'] if 'Punching' in path else ['CC_Base_L_Foot','CC_Base_R_Foot']
   candidates.append(max(unreal.AnimPoseExtensions.get_bone_pose(p,b,unreal.AnimPoseSpaces.WORLD).translation.y-hip.y for b in bones))
  peak=max(range(count),key=lambda i:candidates[i]);report['punch_impact' if 'Punching' in path else 'kick_impact']=peak/30
sub.destroy_actor(tmp)
source=unreal.EditorAssetLibrary.load_asset(folder+'ZW_Zombie_Scream_Anim');pose=unreal.AnimPoseExtensions.get_anim_pose_at_time(source,0,unreal.AnimPoseEvaluationOptions());f=unreal.AnimSequenceFactory();f.set_editor_property('target_skeleton',target.get_editor_property('skeleton'));idle=unreal.AssetToolsHelpers.get_asset_tools().create_asset('ZW_Zombie_Idle',folder.rstrip('/'),unreal.AnimSequence,f);assert idle;ctrl=idle.get_editor_property('controller');ctrl.open_bracket('Zombie standing idle');ctrl.set_frame_rate(unreal.FrameRate(numerator=30,denominator=1));ctrl.set_number_of_frames(unreal.FrameNumber(value=1))
for b in unreal.AnimPoseExtensions.get_bone_names(pose):
 t=unreal.AnimPoseExtensions.get_bone_pose(pose,b,unreal.AnimPoseSpaces.LOCAL);ctrl.add_bone_track(b);assert ctrl.set_bone_track_keys(b,[t.translation]*2,[t.rotation]*2,[t.scale3d]*2)
ctrl.close_bracket();idle.set_editor_properties({'force_root_lock':True,'enable_root_motion':False});assert unreal.EditorAssetLibrary.save_loaded_asset(idle)
json.dump(report,open(unreal.Paths.project_dir()+'work/zombie_attack_timing.json','w'));report
