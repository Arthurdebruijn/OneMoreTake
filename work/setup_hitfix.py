import unreal,json
bp=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Blueprints/BP_KnightPlayer');assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
backup=[{'label':a.get_actor_label(),'location':[a.get_actor_location().x,a.get_actor_location().y,a.get_actor_location().z],'yaw':a.get_actor_rotation().yaw,'extra':a.get_editor_property('ExtraTakeTwoGuard')} for a in sub.get_all_level_actors() if 'BP_Guard' in str(a.get_class())]
json.dump(backup,open(unreal.Paths.project_dir()+'work/rifle_guard_backup.json','w'));assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
assert unreal.BlueprintEditorLibrary.add_member_variable(bp,'NormalMeshMaterials',unreal.BlueprintEditorLibrary.pin_type_from_text('Array of MaterialInterface Object Reference'))
ss=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);lib=unreal.SubobjectDataBlueprintFunctionLibrary
root=next(h for h in ss.k2_gather_subobject_data_for_blueprint(bp) if str(lib.get_variable_name(lib.get_data(h)))=='CapsuleComponent')
h,reason=ss.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.CapsuleComponent,blueprint_context=bp));assert lib.is_handle_valid(h),str(reason);assert ss.rename_subobject(h,unreal.Text('BulletHitbox'))
box=lib.get_object_for_blueprint(lib.get_data(h),bp);box.set_capsule_size(55.0,105.0,False);box.set_editor_property('relative_location',unreal.Vector(0,0,10));box.set_collision_enabled(unreal.CollisionEnabled.QUERY_ONLY);box.set_collision_response_to_all_channels(unreal.CollisionResponseType.ECR_IGNORE);box.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_BLOCK);box.set_editor_property('generate_overlap_events',False)
assert unreal.BlueprintEditorLibrary.compile_blueprint(bp);assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
'Separate bullet hitbox added; normal collision unchanged'
