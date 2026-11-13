import unreal,json
b=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Blueprints/BP_KnightPlayer');assert unreal.EditorAssetLibrary.save_loaded_asset(b)
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);backup=[{'label':a.get_actor_label(),'location':[a.get_actor_location().x,a.get_actor_location().y,a.get_actor_location().z],'yaw':a.get_actor_rotation().yaw,'extra':a.get_editor_property('ExtraTakeTwoGuard'),'ragdoll':a.get_editor_property('UseEnemyRagdoll')} for a in sub.get_all_level_actors() if 'BP_Guard' in str(a.get_class())];json.dump(backup,open(unreal.Paths.project_dir()+'work/rifle_guard_backup.json','w'));assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
for n in ['RagdollPushStrength','RagdollLiftStrength']:
 assert unreal.BlueprintEditorLibrary.add_member_variable(b,n,unreal.BlueprintEditorLibrary.pin_type_from_text('Float (single-precision)'));unreal.BlueprintEditorLibrary.set_blueprint_variable_instance_editable(b,n,True)
assert unreal.BlueprintEditorLibrary.compile_blueprint(b)
c=unreal.get_default_object(unreal.BlueprintEditorLibrary.generated_class(b));c.set_editor_properties({'RagdollPushStrength':380.0,'RagdollLiftStrength':120.0});assert unreal.BlueprintEditorLibrary.compile_blueprint(b);assert unreal.EditorAssetLibrary.save_loaded_asset(b)
s=unreal.EditorAssetLibrary.load_asset('/Game/FREE_Medieval_sword/gltf/free_medieval_sword_extracted/scene/StaticMeshes/scene');assert unreal.EditorAssetLibrary.save_loaded_asset(s);tools=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
if tools.get_simple_collision_count(s)==0:assert tools.add_simple_collisions(s,unreal.ScriptCollisionShapeType.BOX)>=0
assert unreal.EditorAssetLibrary.save_loaded_asset(s)
{'force_controls_added':True,'sword_collision_shapes':tools.get_simple_collision_count(s)}
