import unreal,json
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
guards=[a for a in sub.get_all_level_actors() if 'BP_Guard' in str(a.get_class())]
if not guards:
 cls=unreal.EditorAssetLibrary.load_blueprint_class('/Game/OneMoreTake/Blueprints/BP_Guard')
 for v in json.load(open(unreal.Paths.project_dir()+'work/rifle_guard_backup.json')):
  a=sub.spawn_actor_from_class(cls,unreal.Vector(*v['location']),unreal.Rotator(pitch=0,yaw=v['yaw'],roll=0));a.set_actor_label(v['label']);a.set_editor_property('ExtraTakeTwoGuard',v['extra'])
  if 'ragdoll' in v:a.set_editor_property('UseEnemyRagdoll',v['ragdoll'])
  if 'push' in v:a.set_editor_property('RagdollPushStrength',v['push'])
  if 'lift' in v:a.set_editor_property('RagdollLiftStrength',v['lift'])
  if 'attack_rate' in v:a.set_editor_property('AttackPlayRate',v['attack_rate'])
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
{'saved_guards':len([a for a in sub.get_all_level_actors() if 'BP_Guard' in str(a.get_class())])}
