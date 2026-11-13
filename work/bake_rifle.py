import unreal
for short,sourcepath in [('Idle','MF_Rifle_Idle_ADS'),('Fire','MM_Rifle_Fire')]:
 source=unreal.EditorAssetLibrary.load_asset('/Game/Characters/Mannequins/Anims/Rifle/'+sourcepath)
 f=unreal.AnimSequenceFactory();f.set_editor_property('target_skeleton',unreal.EditorAssetLibrary.load_asset('/Game/CR/Demo/Meshes/SK_Mannequin'))
 a=unreal.AssetToolsHelpers.get_asset_tools().create_asset('A_KnightRifle'+short,'/Game/OneMoreTake/Animations',unreal.AnimSequence,f);assert a
 frames=max(2,round(source.get_play_length()*30))
 poses=[unreal.AnimPoseExtensions.get_anim_pose_at_time(source,i/30,unreal.AnimPoseEvaluationOptions()) for i in range(frames+1)]
 ctrl=a.get_editor_property('controller');ctrl.open_bracket('Bake rifle '+short);ctrl.set_frame_rate(unreal.FrameRate(numerator=30,denominator=1));ctrl.set_number_of_frames(unreal.FrameNumber(value=frames))
 for bone in unreal.AnimPoseExtensions.get_bone_names(poses[0]):
  ts=[unreal.AnimPoseExtensions.get_bone_pose(p,bone,unreal.AnimPoseSpaces.LOCAL) for p in poses]
  if str(bone)=='root':ts=[ts[0]]*len(ts)
  ctrl.add_bone_track(bone);assert ctrl.set_bone_track_keys(bone,[t.translation for t in ts],[t.rotation for t in ts],[t.scale3d for t in ts])
 ctrl.close_bracket();a.set_editor_properties({'enable_root_motion':False,'force_root_lock':True});assert unreal.EditorAssetLibrary.save_loaded_asset(a)
bp=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Animations/ABP_KnightRifle')
seq=unreal.load_object(None,bp.get_path_name()+':AnimGraph.AnimGraphNode_SequencePlayer_0')
node=seq.get_editor_property('node');node.set_editor_properties({'sequence':unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Animations/A_KnightRifleIdle'),'loop_animation':True});seq.set_editor_property('node',node)
layer=unreal.load_object(None,bp.get_path_name()+':AnimGraph.AnimGraphNode_LayeredBoneBlend_0')
node=layer.get_editor_property('node');f=unreal.BranchFilter();f.set_editor_properties({'bone_name':'spine_01','blend_depth':3});pose=unreal.InputBlendPose();pose.set_editor_property('branch_filters',[f]);node.set_editor_properties({'layer_setup':[pose],'blend_weights':[1.0],'mesh_space_rotation_blend':True});layer.set_editor_property('node',node)
idle=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Animations/A_KnightRifleIdle');pose=unreal.AnimPoseExtensions.get_anim_pose_at_time(idle,0,unreal.AnimPoseEvaluationOptions())
{'baked':True,'hands':{b:str(unreal.AnimPoseExtensions.get_bone_pose(pose,b,unreal.AnimPoseSpaces.WORLD)) for b in ['hand_r','hand_l']}}
