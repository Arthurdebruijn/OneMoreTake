import unreal
folder='/Game/OneMoreTake/Animations/Retargeted/Rifle/'
idle=unreal.EditorAssetLibrary.load_asset(folder+'Knight_rifle_aiming_idle')
bp=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Animations/ABP_KnightRifle')
seq=unreal.load_object(None,bp.get_path_name()+':AnimGraph.AnimGraphNode_SequencePlayer_0');node=seq.get_editor_property('node');node.set_editor_property('sequence',idle);seq.set_editor_property('node',node)
# Use the source clips' real movement directions (Mixamo forward is +Y, right is -X).
bs=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Animations/BS_KnightRifleMove')
values=[('rifle_aiming_idle',0,0),('walking',150,0),('walking_backwards',-150,0),('rifle_run',360,0),('run_backwards',-360,0),('strafe',0,330),('strafe__2_',0,-330)]
samples=[]
for name,x,y in values:
 s=unreal.BlendSample();s.set_editor_properties({'animation':unreal.EditorAssetLibrary.load_asset(folder+'Knight_'+name),'sample_value':unreal.Vector(x,y,0),'rate_scale':1.0});samples.append(s)
bs.set_editor_properties({'sample_data':samples,'target_weight_interpolation_speed_per_sec':10.0})
assert unreal.EditorAssetLibrary.save_loaded_asset(bs)
assert unreal.BlueprintEditorLibrary.compile_blueprint(bp);assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
player=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Blueprints/BP_KnightPlayer')
ss=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);lib=unreal.SubobjectDataBlueprintFunctionLibrary
handles=ss.k2_gather_subobject_data_for_blueprint(player)
def component(name):return lib.get_object_for_blueprint(lib.get_data(next(h for h in handles if str(lib.get_variable_name(lib.get_data(h)))==name)),player)
gun=component('GunMesh');muzzle=component('GunMuzzle')
pose=unreal.AnimPoseExtensions.get_anim_pose_at_time(idle,0,unreal.AnimPoseEvaluationOptions())
r=unreal.AnimPoseExtensions.get_bone_pose(pose,'hand_r',unreal.AnimPoseSpaces.WORLD);l=unreal.AnimPoseExtensions.get_bone_pose(pose,'hand_l',unreal.AnimPoseSpaces.WORLD)
# The mesh's barrel runs along +X. Aim its foregrip through the supporting palm.
forward=(l.translation-r.translation).normal()
rot=unreal.MathLibrary.make_rot_from_x(forward).quaternion()
relative=(r.rotation.inversed()*rot).rotator()
gun.set_editor_properties({'relative_rotation':relative,'relative_location':unreal.Vector(0,0,0),'relative_scale3d':unreal.Vector(.55,.55,.55)})
muzzle.set_editor_property('relative_location',unreal.Vector(119,0,26))
# A short, readable flash, attached to the barrel.
mh=next(h for h in handles if str(lib.get_variable_name(lib.get_data(h)))=='GunMuzzle')
h,reason=ss.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=mh,new_class=unreal.StaticMeshComponent,blueprint_context=player));assert lib.is_handle_valid(h),str(reason);assert ss.rename_subobject(h,unreal.Text('MuzzleFlash'))
flash=lib.get_object_for_blueprint(lib.get_data(h),player);flash.set_static_mesh(unreal.EditorAssetLibrary.load_asset('/Engine/BasicShapes/Sphere'));flash.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
flash.set_editor_properties({'relative_scale3d':unreal.Vector(.16,.07,.07),'visible':False,'cast_shadow':False});flash.set_material(0,unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Materials/MI_SwordBrass'))
assert unreal.BlueprintEditorLibrary.compile_blueprint(player);assert unreal.EditorAssetLibrary.save_loaded_asset(player)
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for actor in sub.get_all_level_actors():
 if actor.get_actor_label()=='TEMP_RifleInspection':sub.destroy_actor(actor)
{'configured':True,'rifle_rotation':str(relative),'left_hand_distance_cm':(l.translation-r.translation).length()}
