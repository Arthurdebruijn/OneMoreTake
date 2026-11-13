import unreal
base='/Game/OneMoreTake/Blueprints/'
for name in ['BP_KnightPlayer','BP_Guard','BP_TakeDirector','BP_CombatHUD']:
    assert unreal.EditorAssetLibrary.save_asset(base+name)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
for name,variables in {
 'BP_KnightPlayer':[('HasGun','Boolean'),('FireHeld','Boolean'),('GunReady','Boolean'),('ExtraTakeTwoGuard','Boolean'),('GunTarget','Actor Object Reference'),('GunTargetDistance','Float (single-precision)')],
 'BP_TakeDirector':[('TakeNumber','Integer'),('EnemiesRemaining','Integer')]
}.items():
    bp=unreal.EditorAssetLibrary.load_asset(base+name)
    for var,typ in variables:
        assert unreal.BlueprintEditorLibrary.add_member_variable(bp,var,unreal.BlueprintEditorLibrary.pin_type_from_text(typ)),var
        unreal.BlueprintEditorLibrary.set_blueprint_variable_instance_editable(bp,var,True)
    assert unreal.BlueprintEditorLibrary.compile_blueprint(bp)
    unreal.EditorAssetLibrary.save_loaded_asset(bp)
bp=unreal.EditorAssetLibrary.load_asset(base+'BP_KnightPlayer')
ss=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);lib=unreal.SubobjectDataBlueprintFunctionLibrary
handles=ss.k2_gather_subobject_data_for_blueprint(bp)
root=next(h for h in handles if str(lib.get_variable_name(lib.get_data(h)))=='Mesh')
h,reason=ss.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.StaticMeshComponent,blueprint_context=bp))
assert lib.is_handle_valid(h),str(reason)
assert ss.rename_subobject(h,unreal.Text('GunMesh'))
c=lib.get_object_for_blueprint(lib.get_data(h),bp)
c.set_static_mesh(unreal.EditorAssetLibrary.load_asset('/Game/Weapons/M1911/Meshes/NonRigged_M1911'))
c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
c.set_editor_properties({'visible':False,'relative_location':unreal.Vector(0,0,0),'relative_rotation':unreal.Rotator(pitch=0,yaw=0,roll=0)})
assert unreal.BlueprintEditorLibrary.compile_blueprint(bp)
assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
# The template firing animation uses the same bone names; bake it onto the knight skeleton.
source=unreal.EditorAssetLibrary.load_asset('/Game/Characters/Mannequins/Anims/Pistol/MM_Pistol_Fire')
f=unreal.AnimSequenceFactory();f.set_editor_property('target_skeleton',unreal.EditorAssetLibrary.load_asset('/Game/CR/Demo/Meshes/SK_Mannequin'))
a=unreal.AssetToolsHelpers.get_asset_tools().create_asset('A_KnightGunFire','/Game/OneMoreTake/Animations',unreal.AnimSequence,f)
assert a
frames=max(2,round(source.get_play_length()*30))
poses=[unreal.AnimPoseExtensions.get_anim_pose_at_time(source,i/30,unreal.AnimPoseEvaluationOptions()) for i in range(frames+1)]
ctrl=a.get_editor_property('controller');ctrl.open_bracket('Knight pistol fire');ctrl.set_frame_rate(unreal.FrameRate(numerator=30,denominator=1));ctrl.set_number_of_frames(unreal.FrameNumber(value=frames))
for bone in unreal.AnimPoseExtensions.get_bone_names(poses[0]):
    ts=[unreal.AnimPoseExtensions.get_bone_pose(p,bone,unreal.AnimPoseSpaces.LOCAL) for p in poses]
    if str(bone)=='root': ts=[ts[0]]*len(ts)
    ctrl.add_bone_track(bone);assert ctrl.set_bone_track_keys(bone,[t.translation for t in ts],[t.rotation for t in ts],[t.scale3d for t in ts])
ctrl.close_bracket();a.set_editor_properties({'enable_root_motion':False,'force_root_lock':True});assert unreal.EditorAssetLibrary.save_loaded_asset(a)
guard=unreal.EditorAssetLibrary.load_blueprint_class(base+'BP_Guard')
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for i,(x,y) in enumerate([(-430,1200),(0,1350),(430,1200)]):
    actor=sub.spawn_actor_from_class(guard,unreal.Vector(x,y,92),unreal.Rotator(pitch=0,yaw=-90,roll=0))
    actor.set_actor_label('Take2_ExtraGuard_'+str(i+1));actor.set_editor_property('ExtraTakeTwoGuard',True)
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
{'success':True,'fire_length':a.get_play_length()}
