import unreal,json
bp=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Blueprints/BP_KnightPlayer');assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);backup=[{'label':a.get_actor_label(),'location':[a.get_actor_location().x,a.get_actor_location().y,a.get_actor_location().z],'yaw':a.get_actor_rotation().yaw,'extra':a.get_editor_property('ExtraTakeTwoGuard')} for a in sub.get_all_level_actors() if 'BP_Guard' in str(a.get_class())];json.dump(backup,open(unreal.Paths.project_dir()+'work/rifle_guard_backup.json','w'));assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
assert unreal.BlueprintEditorLibrary.add_member_variable(bp,'UseEnemyRagdoll',unreal.BlueprintEditorLibrary.pin_type_from_text('Boolean'));unreal.BlueprintEditorLibrary.set_blueprint_variable_instance_editable(bp,'UseEnemyRagdoll',True);assert unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.get_default_object(unreal.BlueprintEditorLibrary.generated_class(bp)).set_editor_property('UseEnemyRagdoll',True);assert unreal.BlueprintEditorLibrary.compile_blueprint(bp);assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
# Preserve the current guard animation setup as a fallback before changing its output.
assert unreal.EditorAssetLibrary.save_asset('/Game/OneMoreTake/Animations/ABP_GuardStrafe')
assert unreal.EditorAssetLibrary.duplicate_asset('/Game/OneMoreTake/Animations/ABP_GuardStrafe','/Game/OneMoreTake/Animations/ABP_GuardStrafe_BeforeFullBody')
g={'refPath':'/Game/OneMoreTake/Animations/ABP_GuardStrafe.ABP_GuardStrafe:AnimGraph'}
nodes=await call_tool('BlueprintToolsets.BlueprintToolset.FindNodes',graph=g);info=await call_tool('BlueprintToolsets.BlueprintToolset.GetNodeInfos',nodes=nodes)
blend=next(n for n in info if 'BlendSpaces|BlendspacePlayer' in n['typeId']);slot=next(n for n in info if 'Montage|Slot' in n['typeId']);root=next(n for n in info if n['typeId']=='Misc.|OutputPose')
for n in [slot,root]:
 for link in n['inputPins'][0]['connectedPins']:await call_tool('BlueprintToolsets.BlueprintToolset.DisconnectPins',outputPin=link,inputPin=n['inputPins'][0]['pinId'])
for outpin,inpin in [(blend['outputPins'][0]['pinId'],slot['inputPins'][0]['pinId']),(slot['outputPins'][0]['pinId'],root['inputPins'][0]['pinId'])]:await call_tool('BlueprintToolsets.BlueprintToolset.ConnectPins',outputPin=outpin,inputPin=inpin)
abp=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Animations/ABP_GuardStrafe');assert unreal.BlueprintEditorLibrary.compile_blueprint(abp);assert unreal.EditorAssetLibrary.save_loaded_asset(abp)
bs=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Animations/BS_GuardStrafe');samples=list(bs.get_editor_property('sample_data'))
for s in samples:
 v=s.get_editor_property('sample_value');name=s.get_editor_property('animation').get_name()
 if 'Walk' in name:v=unreal.Vector(80 if v.x>0 else -80,0,0)
 elif name!='A_GuardIdle':v=v.normal()*210.0
 s.set_editor_properties({'sample_value':v,'rate_scale':0.95})
bs.set_editor_properties({'sample_data':samples,'target_weight_interpolation_speed_per_sec':7.0});editors=unreal.get_editor_subsystem(unreal.AssetEditorSubsystem);assert editors.open_editor_for_assets([bs]);assert unreal.EditorAssetLibrary.save_loaded_asset(bs);editors.close_all_editors_for_asset(bs)
{'ragdoll_default':True,'guard_full_body_locomotion':True,'death_animation_preserved':unreal.EditorAssetLibrary.does_asset_exist('/Game/OneMoreTake/Animations/A_KnightDeath')}
