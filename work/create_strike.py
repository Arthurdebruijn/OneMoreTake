import unreal
skel=unreal.EditorAssetLibrary.load_asset('/Game/CR/Demo/Meshes/SK_Mannequin')
mesh=unreal.EditorAssetLibrary.load_asset('/Game/CR/LQ/CharacterModular/Modular_012_Grian09/Mesh/SKM_Grian09_1')
idle=unreal.EditorAssetLibrary.load_asset('/Game/CR/Demo/Animations/Manny/MM_Idle')
source=unreal.EditorAssetLibrary.load_asset('/Game/Characters/Mannequins/Anims/Unarmed/Attack/MM_Attack_01')
opts=unreal.AnimPoseEvaluationOptions()
idle_pose=unreal.AnimPoseExtensions.get_anim_pose_at_time(idle,0,opts)
bones=unreal.AnimPoseExtensions.get_bone_names(idle_pose)
f=unreal.AnimSequenceFactory()
f.set_editor_properties({'target_skeleton':skel,'preview_skeletal_mesh':mesh})
a=unreal.AssetToolsHelpers.get_asset_tools().create_asset('A_SwordStrike','/Game/OneMoreTake/Animations',unreal.AnimSequence,f)
assert a
ctrl=a.get_editor_property('controller')
ctrl.open_bracket('Bake prototype sword strike')
ctrl.set_frame_rate(unreal.FrameRate(numerator=30,denominator=1))
ctrl.set_number_of_frames(unreal.FrameNumber(value=24))
poses=[unreal.AnimPoseExtensions.get_anim_pose_at_time(source,i/24,opts) for i in range(25)]
source_bones=set(str(b) for b in unreal.AnimPoseExtensions.get_bone_names(poses[0]))
for bone in bones:
    base=unreal.AnimPoseExtensions.get_bone_pose(idle_pose,bone,unreal.AnimPoseSpaces.LOCAL)
    positions=[]; rotations=[]; scales=[]
    for i,pose in enumerate(poses):
        t=i/30
        weight=min(1.0,t/.1,max(0.0,(.8-t)/.16))
        value=base
        if str(bone) in source_bones and str(bone)!='root':
            strike=unreal.AnimPoseExtensions.get_bone_pose(pose,bone,unreal.AnimPoseSpaces.LOCAL)
            value=base.lerp(strike,weight)
        positions.append(value.translation); rotations.append(value.rotation); scales.append(value.scale3d)
    ctrl.add_bone_track(bone)
    assert ctrl.set_bone_track_keys(bone,positions,rotations,scales),str(bone)
ctrl.close_bracket()
a.set_editor_properties({'enable_root_motion':False,'force_root_lock':True})
assert unreal.EditorAssetLibrary.save_loaded_asset(a)
{'animation':a.get_path_name(),'length':a.get_play_length(),'bones':len(bones)}
