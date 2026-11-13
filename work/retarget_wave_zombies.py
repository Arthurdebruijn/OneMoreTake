import unreal,json
folder='/Game/OneMoreTake/Animations/Retargeted/ZombieWaves'
base='/Game/OneMoreTake/'
for n in ['BP_KnightPlayer','BP_Guard','BP_TakeDirector','BP_CombatHUD']:assert unreal.EditorAssetLibrary.save_asset(base+'Blueprints/'+n)
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);backup=[{'label':a.get_actor_label(),'location':[a.get_actor_location().x,a.get_actor_location().y,a.get_actor_location().z],'yaw':a.get_actor_rotation().yaw,'extra':a.get_editor_property('ExtraTakeTwoGuard'),'ragdoll':a.get_editor_property('UseEnemyRagdoll'),'push':a.get_editor_property('RagdollPushStrength'),'lift':a.get_editor_property('RagdollLiftStrength'),'attack_rate':a.get_editor_property('AttackPlayRate')} for a in sub.get_all_level_actors() if a.get_class().get_name()=='BP_Guard_C'];json.dump(backup,open(unreal.Paths.project_dir()+'work/rifle_guard_backup.json','w'));assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
at=unreal.AssetToolsHelpers.get_asset_tools()
def asset(name,cls,factory):
 old=unreal.EditorAssetLibrary.load_asset(folder+'/'+name)
 return old if old else at.create_asset(name,folder,cls,factory)
target=unreal.EditorAssetLibrary.load_asset('/Game/Characters/Zombie/StylizedZombie/Textures/SZombie_Variant_1/SK_SZombie_Variant_1')
target_rig=asset('IK_StylizedZombie',unreal.IKRigDefinition,unreal.IKRigDefinitionFactory());ctl=unreal.IKRigController.get_controller(target_rig);assert ctl.set_skeletal_mesh(target)
if not ctl.get_retarget_chains():
 assert ctl.set_retarget_root('CC_Base_Hip')
 chains=[('Spine','CC_Base_Waist','CC_Base_Spine02'),('Neck','CC_Base_NeckTwist01','CC_Base_NeckTwist02'),('Head','CC_Base_Head','CC_Base_Head')]
 for side,letter in [('Left','L'),('Right','R')]:
  prefix='CC_Base_'+letter+'_';chains.extend([(side+'Leg',prefix+'Thigh',prefix+'Foot'),(side+'Foot',prefix+'ToeBase',prefix+'ToeBase'),(side+'Clavicle',prefix+'Clavicle',prefix+'Clavicle'),(side+'Arm',prefix+'Upperarm',prefix+'Hand')])
  for chain,bone in [('Thumb','Thumb'),('Index','Index'),('Middle','Mid'),('Ring','Ring'),('Pinky','Pinky')]:chains.append((side+chain,prefix+bone+'1',prefix+bone+'3'))
 names={str(n) for n in unreal.AnimPoseExtensions.get_bone_names(unreal.AnimPoseExtensions.get_reference_pose(target.get_editor_property('skeleton')))}
 for name,start,end in chains:
  if start in names and end in names:assert str(ctl.add_retarget_chain(name,start,end,'None'))==name
assert unreal.EditorAssetLibrary.save_loaded_asset(target_rig)
inputs=[('StandUp','Zombie_Stand_Up'),('Scream','Zombie_Scream'),('Running','Zombie_Running'),('AttackPunch','Zombie_Punching'),('AttackKick','Zombie_Kicking'),('GettingHit','Zombie_Reaction_Hit')]
outputs=[]
for dirname,name in inputs:
 sourcepath=base+'Animations/Zombie_Animations/'+dirname+'/'+name;source=unreal.EditorAssetLibrary.load_asset(sourcepath);assert source
 rig=asset('IK_Source_'+dirname,unreal.IKRigDefinition,unreal.IKRigDefinitionFactory());c=unreal.IKRigController.get_controller(rig);assert c.set_skeletal_mesh(source);assert c.apply_auto_generated_retarget_definition()
 rtg=asset('RTG_'+dirname,unreal.IKRetargeter,unreal.IKRetargetFactory());rc=unreal.IKRetargeterController.get_controller(rtg);rc.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE,rig);rc.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET,target_rig);rc.set_preview_mesh(unreal.RetargetSourceOrTarget.SOURCE,source);rc.set_preview_mesh(unreal.RetargetSourceOrTarget.TARGET,target);rc.add_default_ops();rc.auto_map_chains(unreal.AutoMapChainType.FUZZY,True);rc.auto_align_all_bones(unreal.RetargetSourceOrTarget.TARGET)
 for a in [rig,rtg]:assert unreal.EditorAssetLibrary.save_loaded_asset(a)
 result=unreal.IKRetargetBatchOperation.duplicate_and_retarget([unreal.EditorAssetLibrary.find_asset_data(sourcepath+'_Anim')],source,target,rtg,prefix='ZW_',target_path=folder,include_referenced_assets=False);assert len(result)==1;outputs.append(str(result[0].package_name))
report={'animations':outputs,'target':target.get_path_name()};json.dump(report,open(unreal.Paths.project_dir()+'work/zombie_wave_assets.json','w'));report
