import unreal
paths=['/Game/OneMoreTake/Animations/Retargeted/Knight_Sword_And_Shield_Slash_Anim','/Game/OneMoreTake/Animations/Retargeted/Knight_Sword_And_Shield_Slash__1__Anim']
actor=next(a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors() if a.get_class().get_name()=='BP_Guard_C')
mesh=actor.get_component_by_class(unreal.SkeletalMeshComponent)
report=[]
for path in paths:
    anim=unreal.EditorAssetLibrary.load_asset(path)
    count=round(anim.get_play_length()*30)+1
    opts=unreal.AnimPoseEvaluationOptions()
    poses=[unreal.AnimPoseExtensions.get_anim_pose_at_time(anim,i/30,opts) for i in range(count)]
    bones=unreal.AnimPoseExtensions.get_bone_names(poses[0])
    children=[b for b in bones if str(mesh.get_parent_bone(b))=='root']
    assert 'pelvis' in [str(b) for b in children]
    before=[[unreal.AnimPoseExtensions.get_bone_pose(p,b,unreal.AnimPoseSpaces.WORLD).translation.z for b in ['foot_l','foot_r']] for p in poses]
    roots=[unreal.AnimPoseExtensions.get_bone_pose(p,'root',unreal.AnimPoseSpaces.LOCAL) for p in poses]
    tracks={}
    for bone in children:
        values=[]
        for p,r in zip(poses,roots):
            local=unreal.AnimPoseExtensions.get_bone_pose(p,bone,unreal.AnimPoseSpaces.LOCAL)
            # Keep vertical height and body rotation, while gameplay controls horizontal travel.
            parent=unreal.Transform()
            parent.translation=unreal.Vector(0,0,r.translation.z)
            parent.rotation=r.rotation
            parent.scale3d=r.scale3d
            values.append(local.multiply(parent))
        tracks[str(bone)]=values
    controller=anim.get_editor_property('controller')
    controller.open_bracket('Keep sword attacks grounded with an in-place root')
    for bone,values in tracks.items():
        assert controller.set_bone_track_keys(bone,[t.translation for t in values],[t.rotation for t in values],[t.scale3d for t in values]),bone
    assert controller.set_bone_track_keys('root',[unreal.Vector(0,0,0)]*count,[unreal.Quat(0,0,0,1)]*count,[unreal.Vector(1,1,1)]*count)
    controller.close_bracket()
    anim.set_editor_properties({'force_root_lock':True,'enable_root_motion':False,'root_motion_root_lock':unreal.RootMotionRootLock.REF_POSE})
    assert unreal.EditorAssetLibrary.save_loaded_asset(anim)
    error=0
    for i,previous in enumerate(before):
        p=unreal.AnimPoseExtensions.get_anim_pose_at_time(anim,i/30,opts)
        for j,bone in enumerate(['foot_l','foot_r']):
            z=unreal.AnimPoseExtensions.get_bone_pose(p,bone,unreal.AnimPoseSpaces.WORLD).translation.z
            error=max(error,abs(z-previous[j]))
    assert error<.1,error
    report.append({'animation':anim.get_name(),'root_children_corrected':[str(b) for b in children],'max_foot_height_change_cm':round(error,4)})
report

