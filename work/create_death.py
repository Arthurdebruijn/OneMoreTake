import unreal
source=unreal.EditorAssetLibrary.load_asset('/Game/Characters/Mannequins/Anims/Death/MM_Death_Front_01')
skel=unreal.EditorAssetLibrary.load_asset('/Game/CR/Demo/Meshes/SK_Mannequin')
f=unreal.AnimSequenceFactory(); f.set_editor_property('target_skeleton',skel)
a=unreal.AssetToolsHelpers.get_asset_tools().create_asset('A_KnightDeath','/Game/OneMoreTake/Animations',unreal.AnimSequence,f)
assert a
opts=unreal.AnimPoseEvaluationOptions()
poses=[unreal.AnimPoseExtensions.get_anim_pose_at_time(source,i/30,opts) for i in range(46)]
ctrl=a.get_editor_property('controller'); ctrl.open_bracket('Bake death to knight skeleton')
ctrl.set_frame_rate(unreal.FrameRate(numerator=30,denominator=1)); ctrl.set_number_of_frames(unreal.FrameNumber(value=45))
bones=unreal.AnimPoseExtensions.get_bone_names(poses[0])
for bone in bones:
    transforms=[unreal.AnimPoseExtensions.get_bone_pose(p,bone,unreal.AnimPoseSpaces.LOCAL) for p in poses]
    if str(bone)=='root': transforms=[transforms[0]]*46
    ctrl.add_bone_track(bone)
    assert ctrl.set_bone_track_keys(bone,[v.translation for v in transforms],[v.rotation for v in transforms],[v.scale3d for v in transforms]),str(bone)
ctrl.close_bracket()
a.set_editor_properties({'enable_root_motion':False,'force_root_lock':True})
assert unreal.EditorAssetLibrary.save_loaded_asset(a)
'Knight death animation saved'
