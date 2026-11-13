import unreal,json
source_folder='/Game/OneMoreTake/Animations/Maximo_Rifle'
folder='/Game/OneMoreTake/Animations/Retargeted/Rifle'
for path in ['/Game/OneMoreTake/Animations/ABP_KnightRifle','/Game/OneMoreTake/Animations/BS_KnightRifleMove','/Game/OneMoreTake/Blueprints/BP_KnightPlayer','/Game/OneMoreTake/Blueprints/BP_Guard']:
 assert unreal.EditorAssetLibrary.save_asset(path)
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
guards=[a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors() if 'BP_Guard' in str(a.get_class())]
backup=[{'label':a.get_actor_label(),'location':[a.get_actor_location().x,a.get_actor_location().y,a.get_actor_location().z],'yaw':a.get_actor_rotation().yaw,'extra':a.get_editor_property('ExtraTakeTwoGuard')} for a in guards]
with open(unreal.Paths.project_dir()+'work/rifle_guard_backup.json','w') as f:json.dump(backup,f)
at=unreal.AssetToolsHelpers.get_asset_tools()
source=unreal.EditorAssetLibrary.load_asset(source_folder+'/X_Bot')
target=unreal.EditorAssetLibrary.load_asset('/Game/CR/LQ/CharacterModular/Modular_012_Grian09/Mesh/SKM_Grian09_1')
target_rig=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Animations/Retargeted/IK_KnightCombat')
rig=at.create_asset('IK_XBotRifle',folder,unreal.IKRigDefinition,unreal.IKRigDefinitionFactory());assert rig
c=unreal.IKRigController.get_controller(rig);assert c.set_skeletal_mesh(source);assert c.apply_auto_generated_retarget_definition()
rtg=at.create_asset('RTG_XBotRifleToKnight',folder,unreal.IKRetargeter,unreal.IKRetargetFactory());assert rtg
rc=unreal.IKRetargeterController.get_controller(rtg)
rc.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE,rig);rc.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET,target_rig)
rc.set_preview_mesh(unreal.RetargetSourceOrTarget.SOURCE,source);rc.set_preview_mesh(unreal.RetargetSourceOrTarget.TARGET,target)
rc.add_default_ops();rc.auto_map_chains(unreal.AutoMapChainType.FUZZY,True);rc.auto_align_all_bones(unreal.RetargetSourceOrTarget.TARGET)
for a in [rig,rtg]:assert unreal.EditorAssetLibrary.save_loaded_asset(a)
inputs=[a for a in unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_path(source_folder,True) if str(a.asset_class_path.asset_name)=='AnimSequence' and str(a.asset_name)!='X_Bot_Anim']
results=unreal.IKRetargetBatchOperation.duplicate_and_retarget(inputs,source,target,rtg,prefix='Knight_',target_path=folder,include_referenced_assets=False)
assert len(results)==len(inputs),(len(results),len(inputs))
{'retargeted':[str(a.package_name) for a in results],'guard_backup':len(backup)}
