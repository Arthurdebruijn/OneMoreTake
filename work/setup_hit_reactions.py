import unreal,json
bp=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Blueprints/BP_KnightPlayer');assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
backup=[{'label':a.get_actor_label(),'location':[a.get_actor_location().x,a.get_actor_location().y,a.get_actor_location().z],'yaw':a.get_actor_rotation().yaw,'extra':a.get_editor_property('ExtraTakeTwoGuard')} for a in sub.get_all_level_actors() if 'BP_Guard' in str(a.get_class())]
json.dump(backup,open(unreal.Paths.project_dir()+'work/rifle_guard_backup.json','w'));assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
for n,t in [('HitReactionIndex','Integer'),('HitReacting','Boolean'),('HitReactionAnimation','AnimSequence Object Reference'),('OrbitDirection','Float (single-precision)')]:
 assert unreal.BlueprintEditorLibrary.add_member_variable(bp,n,unreal.BlueprintEditorLibrary.pin_type_from_text(t));unreal.BlueprintEditorLibrary.set_blueprint_variable_instance_editable(bp,n,True)
assert unreal.BlueprintEditorLibrary.compile_blueprint(bp);assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
at=unreal.AssetToolsHelpers.get_asset_tools();folder='/Game/OneMoreTake/Animations/Retargeted/Hits'
target=unreal.EditorAssetLibrary.load_asset('/Game/CR/LQ/CharacterModular/Modular_012_Grian09/Mesh/SKM_Grian09_1');target_rig=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Animations/Retargeted/IK_KnightCombat')
outputs=[]
for name in ['Stomach_Hit','Head_Hit','Hit_To_Body']:
 sourcepath=next(str(a.package_name) for a in unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_path('/Game/OneMoreTake/Animations/Getting_Hit',True) if str(a.asset_name)==name and str(a.asset_class_path.asset_name)=='SkeletalMesh')
 source=unreal.EditorAssetLibrary.load_asset(sourcepath)
 rig=at.create_asset('IK_'+name,folder,unreal.IKRigDefinition,unreal.IKRigDefinitionFactory());c=unreal.IKRigController.get_controller(rig);assert c.set_skeletal_mesh(source);assert c.apply_auto_generated_retarget_definition()
 rtg=at.create_asset('RTG_'+name,folder,unreal.IKRetargeter,unreal.IKRetargetFactory());rc=unreal.IKRetargeterController.get_controller(rtg);rc.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE,rig);rc.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET,target_rig);rc.set_preview_mesh(unreal.RetargetSourceOrTarget.SOURCE,source);rc.set_preview_mesh(unreal.RetargetSourceOrTarget.TARGET,target);rc.add_default_ops();rc.auto_map_chains(unreal.AutoMapChainType.FUZZY,True);rc.auto_align_all_bones(unreal.RetargetSourceOrTarget.TARGET)
 for a in [rig,rtg]:assert unreal.EditorAssetLibrary.save_loaded_asset(a)
 result=unreal.IKRetargetBatchOperation.duplicate_and_retarget([unreal.EditorAssetLibrary.find_asset_data(sourcepath+'_Anim')],source,target,rtg,prefix='Knight_',target_path=folder,include_referenced_assets=False);assert len(result)==1;outputs.append(str(result[0].package_name))
# Preserve height while removing the retargeter's elevated root and authored travel.
mesh=target
for path in outputs:
 anim=unreal.EditorAssetLibrary.load_asset(path);count=round(anim.get_play_length()*30)+1;poses=[unreal.AnimPoseExtensions.get_anim_pose_at_time(anim,i/30,unreal.AnimPoseEvaluationOptions()) for i in range(count)]
 # These mannequin bones are the direct children of root.
 children=[b for b in ['pelvis','ik_hand_root','ik_foot_root','interaction','center_of_mass'] if b in [str(n) for n in unreal.AnimPoseExtensions.get_bone_names(poses[0])]]
 roots=[unreal.AnimPoseExtensions.get_bone_pose(p,'root',unreal.AnimPoseSpaces.LOCAL) for p in poses];tracks={}
 for bone in children:
  values=[]
  for p,r in zip(poses,roots):
   local=unreal.AnimPoseExtensions.get_bone_pose(p,bone,unreal.AnimPoseSpaces.LOCAL);parent=unreal.Transform();parent.translation=unreal.Vector(0,0,r.translation.z);parent.rotation=r.rotation;parent.scale3d=r.scale3d;values.append(local.multiply(parent))
  tracks[bone]=values
 ctrl=anim.get_editor_property('controller');ctrl.open_bracket('Ground hit reaction')
 for bone,values in tracks.items():assert ctrl.set_bone_track_keys(bone,[t.translation for t in values],[t.rotation for t in values],[t.scale3d for t in values])
 assert ctrl.set_bone_track_keys('root',[unreal.Vector()]*count,[unreal.Quat(0,0,0,1)]*count,[unreal.Vector(1,1,1)]*count);ctrl.close_bracket();anim.set_editor_properties({'enable_root_motion':False,'force_root_lock':True,'root_motion_root_lock':unreal.RootMotionRootLock.REF_POSE});assert unreal.EditorAssetLibrary.save_loaded_asset(anim)
outputs
