import unreal,json
b=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Blueprints/BP_KnightPlayer');assert unreal.EditorAssetLibrary.save_loaded_asset(b)
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);backup=[{'label':a.get_actor_label(),'location':[a.get_actor_location().x,a.get_actor_location().y,a.get_actor_location().z],'yaw':a.get_actor_rotation().yaw,'extra':a.get_editor_property('ExtraTakeTwoGuard'),'ragdoll':a.get_editor_property('UseEnemyRagdoll'),'push':a.get_editor_property('RagdollPushStrength'),'lift':a.get_editor_property('RagdollLiftStrength'),'attack_rate':a.get_editor_property('AttackPlayRate')} for a in sub.get_all_level_actors() if 'BP_Guard' in str(a.get_class())];json.dump(backup,open(unreal.Paths.project_dir()+'work/rifle_guard_backup.json','w'));assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
for n in ['GunShotStart','GunShotDirection']:
 assert unreal.BlueprintEditorLibrary.add_member_variable(b,n,unreal.BlueprintEditorLibrary.pin_type_from_text('Vector Structure'));unreal.BlueprintEditorLibrary.set_blueprint_variable_instance_editable(b,n,True)
assert unreal.BlueprintEditorLibrary.compile_blueprint(b);assert unreal.EditorAssetLibrary.save_loaded_asset(b)
'Stable shot position and direction added'
