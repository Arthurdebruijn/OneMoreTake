import unreal
folder='/Game/OneMoreTake/Animations'
skel=unreal.EditorAssetLibrary.load_asset('/Game/CR/Demo/Meshes/SK_Mannequin')
inputs=[('Idle','MM_Idle',0,0),('Walk','Walk/MF_Unarmed_Walk_Fwd',150,0),('BackWalk','Walk/MF_Unarmed_Walk_Bwd',-150,0),('Run','Jog/MF_Unarmed_Jog_Fwd',360,0),('BackRun','Jog/MF_Unarmed_Jog_Bwd',-360,0),('Right','Jog/MF_Unarmed_Jog_Right',0,330),('Left','Jog/MF_Unarmed_Jog_Left',0,-330)]
samples=[]
for name,path,x,y in inputs:
 source=unreal.EditorAssetLibrary.load_asset('/Game/Characters/Mannequins/Anims/Unarmed/'+path);assert source,path
 f=unreal.AnimSequenceFactory();f.set_editor_property('target_skeleton',skel);a=unreal.AssetToolsHelpers.get_asset_tools().create_asset('A_Guard'+name,folder,unreal.AnimSequence,f);assert a
 frames=max(2,round(source.get_play_length()*30));poses=[unreal.AnimPoseExtensions.get_anim_pose_at_time(source,i/30,unreal.AnimPoseEvaluationOptions()) for i in range(frames+1)]
 ctrl=a.get_editor_property('controller');ctrl.open_bracket('Guard strafe locomotion');ctrl.set_frame_rate(unreal.FrameRate(numerator=30,denominator=1));ctrl.set_number_of_frames(unreal.FrameNumber(value=frames))
 for bone in unreal.AnimPoseExtensions.get_bone_names(poses[0]):
  ts=[unreal.AnimPoseExtensions.get_bone_pose(p,bone,unreal.AnimPoseSpaces.LOCAL) for p in poses]
  if str(bone)=='root':ts=[unreal.Transform()]*len(ts)
  ctrl.add_bone_track(bone);assert ctrl.set_bone_track_keys(bone,[t.translation for t in ts],[t.rotation for t in ts],[t.scale3d for t in ts])
 ctrl.close_bracket();a.set_editor_properties({'enable_root_motion':False,'force_root_lock':True});assert unreal.EditorAssetLibrary.save_loaded_asset(a)
 s=unreal.BlendSample();s.set_editor_properties({'animation':a,'sample_value':unreal.Vector(x,y,0),'rate_scale':1.0});samples.append(s)
bs=unreal.EditorAssetLibrary.duplicate_asset(folder+'/BS_KnightRifleMove',folder+'/BS_GuardStrafe');assert bs;bs.set_editor_property('sample_data',samples)
# Opening the Blend Space builds its runtime interpolation data after changing samples.
editors=unreal.get_editor_subsystem(unreal.AssetEditorSubsystem);assert editors.open_editor_for_assets([bs]);assert unreal.EditorAssetLibrary.save_loaded_asset(bs);editors.close_all_editors_for_asset(bs)
bp=unreal.EditorAssetLibrary.duplicate_asset(folder+'/ABP_KnightRifle',folder+'/ABP_GuardStrafe');assert bp
seq=unreal.load_object(None,bp.get_path_name()+':AnimGraph.AnimGraphNode_SequencePlayer_0');data=seq.get_editor_property('node');data.set_editor_property('sequence',unreal.EditorAssetLibrary.load_asset(folder+'/A_GuardIdle'));seq.set_editor_property('node',data)
blend=unreal.load_object(None,bp.get_path_name()+':AnimGraph.AnimGraphNode_BlendSpacePlayer_0');data=blend.get_editor_property('node');data.set_editor_property('blend_space',bs);blend.set_editor_property('node',data)
assert unreal.BlueprintEditorLibrary.compile_blueprint(bp);assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
'Guard directional locomotion saved'
