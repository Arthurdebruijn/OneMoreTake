import unreal
graph={'refPath':'/Game/OneMoreTake/Animations/ABP_KnightRifle.ABP_KnightRifle:AnimGraph'}
nodes=await call_tool('BlueprintToolsets.BlueprintToolset.FindNodes',graph=graph)
infos=await call_tool('BlueprintToolsets.BlueprintToolset.GetNodeInfos',nodes=nodes)
def find(s):return next(n for n in infos if s in n['typeId'])
rig,slot,root,seq,layer=[find(s) for s in ['Misc.|ControlRig','Montage|Slot','Misc.|OutputPose','Sequences|SequencePlayer','Blends|Layered']]
def inp(n,i=0):return n['inputPins'][i]['pinId']
def out(n,i=0):return n['outputPins'][i]['pinId']
await call_tool('BlueprintToolsets.BlueprintToolset.DisconnectPins',outputPin=out(rig),inputPin=inp(slot))
await call_tool('BlueprintToolsets.BlueprintToolset.DisconnectPins',outputPin=out(slot),inputPin=inp(root))
for a,b in [(out(rig),inp(layer)),(out(seq),inp(slot)),(out(slot),inp(layer,1)),(out(layer),inp(root))]:
 await call_tool('BlueprintToolsets.BlueprintToolset.ConnectPins',outputPin=a,inputPin=b)
bp=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Animations/ABP_KnightRifle');assert unreal.BlueprintEditorLibrary.compile_blueprint(bp);assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
# Match rifle local X to mannequin forward Y, relative to the animated right hand.
idle=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Animations/A_KnightRifleIdle')
pose=unreal.AnimPoseExtensions.get_anim_pose_at_time(idle,0,unreal.AnimPoseEvaluationOptions())
hand=unreal.AnimPoseExtensions.get_bone_pose(pose,'hand_r',unreal.AnimPoseSpaces.WORLD)
rotation=hand.rotation.inverse()*unreal.Rotator(pitch=0,yaw=90,roll=0).quaternion()
player=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Blueprints/BP_KnightPlayer');assert unreal.EditorAssetLibrary.save_loaded_asset(player)
ss=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);lib=unreal.SubobjectDataBlueprintFunctionLibrary
h=next(h for h in ss.k2_gather_subobject_data_for_blueprint(player) if str(lib.get_variable_name(lib.get_data(h)))=='GunMesh')
gun=lib.get_object_for_blueprint(lib.get_data(h),player);gun.set_static_mesh(unreal.EditorAssetLibrary.load_asset('/Game/Weapons_Free/Meshes/SM_rifle_001'))
gun.set_editor_properties({'relative_rotation':rotation.rotator(),'relative_location':unreal.Vector(0,0,0),'relative_scale3d':unreal.Vector(.55,.55,.55)})
assert unreal.EditorAssetLibrary.save_loaded_asset(player)
{'compiled':True,'rifle_relative_rotation':str(rotation.rotator())}
