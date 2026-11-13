import unreal
folder='/Game/OneMoreTake/Animations/Retargeted/Rifle'
assets=[unreal.EditorAssetLibrary.load_asset(str(a.package_name)) for a in unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_path(folder,True) if str(a.asset_class_path.asset_name)=='AnimSequence']
mesh=next(a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors() if 'BP_Guard' in str(a.get_class())).get_editor_property('Mesh')
report=[]
for anim in assets:
 count=round(anim.get_play_length()*30)+1
 poses=[unreal.AnimPoseExtensions.get_anim_pose_at_time(anim,i/30,unreal.AnimPoseEvaluationOptions()) for i in range(count)]
 children=[b for b in unreal.AnimPoseExtensions.get_bone_names(poses[0]) if str(mesh.get_parent_bone(b))=='root']
 roots=[unreal.AnimPoseExtensions.get_bone_pose(p,'root',unreal.AnimPoseSpaces.LOCAL) for p in poses]
 tracks={}
 for bone in children:
  values=[]
  for p,r in zip(poses,roots):
   local=unreal.AnimPoseExtensions.get_bone_pose(p,bone,unreal.AnimPoseSpaces.LOCAL)
   parent=unreal.Transform();parent.translation=unreal.Vector(0,0,r.translation.z);parent.rotation=r.rotation;parent.scale3d=r.scale3d
   values.append(local.multiply(parent))
  tracks[str(bone)]=values
 controller=anim.get_editor_property('controller');controller.open_bracket('Ground rifle animation and remove authored travel')
 for bone,values in tracks.items():assert controller.set_bone_track_keys(bone,[t.translation for t in values],[t.rotation for t in values],[t.scale3d for t in values])
 assert controller.set_bone_track_keys('root',[unreal.Vector(0,0,0)]*count,[unreal.Quat(0,0,0,1)]*count,[unreal.Vector(1,1,1)]*count)
 controller.close_bracket();anim.set_editor_properties({'force_root_lock':True,'enable_root_motion':False,'root_motion_root_lock':unreal.RootMotionRootLock.REF_POSE});assert unreal.EditorAssetLibrary.save_loaded_asset(anim)
 report.append(anim.get_name())
report
