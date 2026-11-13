import unreal,math
folder='/Game/OneMoreTake/Animations/'
samples=[]
for direction,x,y in [('Fwd',400,0),('Bwd',-400,0),('Left',0,-400),('Right',0,400),('Fwd_Left',283,-283),('Fwd_Right',283,283),('Bwd_Left',-283,-283),('Bwd_Right',-283,283)]:
 source=unreal.EditorAssetLibrary.load_asset('/Game/Characters/Mannequins/Anims/Rifle/Jog/MF_Rifle_Jog_'+direction);assert source
 f=unreal.AnimSequenceFactory();f.set_editor_property('target_skeleton',unreal.EditorAssetLibrary.load_asset('/Game/CR/Demo/Meshes/SK_Mannequin'))
 a=unreal.AssetToolsHelpers.get_asset_tools().create_asset('A_KnightRifleJog_'+direction,folder.rstrip('/'),unreal.AnimSequence,f);assert a
 frames=max(2,round(source.get_play_length()*30))
 poses=[unreal.AnimPoseExtensions.get_anim_pose_at_time(source,i/30,unreal.AnimPoseEvaluationOptions()) for i in range(frames+1)]
 ctrl=a.get_editor_property('controller');ctrl.open_bracket('Bake rifle locomotion');ctrl.set_frame_rate(unreal.FrameRate(numerator=30,denominator=1));ctrl.set_number_of_frames(unreal.FrameNumber(value=frames))
 for bone in unreal.AnimPoseExtensions.get_bone_names(poses[0]):
  ts=[unreal.AnimPoseExtensions.get_bone_pose(p,bone,unreal.AnimPoseSpaces.LOCAL) for p in poses]
  if str(bone)=='root':ts=[ts[0]]*len(ts)
  ctrl.add_bone_track(bone);assert ctrl.set_bone_track_keys(bone,[t.translation for t in ts],[t.rotation for t in ts],[t.scale3d for t in ts])
 ctrl.close_bracket();a.set_editor_properties({'enable_root_motion':False,'force_root_lock':True});assert unreal.EditorAssetLibrary.save_loaded_asset(a)
 sample=unreal.BlendSample();sample.set_editor_properties({'animation':a,'sample_value':unreal.Vector(x,y,0),'rate_scale':1.0});samples.append(sample)
f=unreal.BlendSpaceFactoryNew();f.set_editor_property('target_skeleton',unreal.EditorAssetLibrary.load_asset('/Game/CR/Demo/Meshes/SK_Mannequin'))
bs=unreal.AssetToolsHelpers.get_asset_tools().create_asset('BS_KnightRifleMove',folder.rstrip('/'),unreal.BlendSpace,f);assert bs
sample=unreal.BlendSample();sample.set_editor_properties({'animation':unreal.EditorAssetLibrary.load_asset(folder+'A_KnightRifleIdle'),'sample_value':unreal.Vector(0,0,0),'rate_scale':1.0});samples.append(sample)
params=list(bs.get_editor_property('blend_parameters'))
for i,name in enumerate(['Forward','Right']):params[i].set_editor_properties({'display_name':name,'min':-400.0,'max':400.0,'grid_num':8})
bs.set_editor_properties({'blend_parameters':params,'sample_data':samples,'target_weight_interpolation_speed_per_sec':8.0})
assert unreal.EditorAssetLibrary.save_loaded_asset(bs)
'Eight-direction rifle locomotion saved'
