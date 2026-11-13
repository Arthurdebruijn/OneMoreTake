import unreal
graph={'refPath':'/Game/OneMoreTake/Animations/ABP_KnightRifle.ABP_KnightRifle:AnimGraph'}
nodes=await call_tool('BlueprintToolsets.BlueprintToolset.FindNodes',graph=graph)
infos=await call_tool('BlueprintToolsets.BlueprintToolset.GetNodeInfos',nodes=nodes)
def find(s):return next(n for n in infos if s in n['typeId'])
def inp(n,i=0):return n['inputPins'][i]['pinId']
def out(n,i=0):return n['outputPins'][i]['pinId']
blend,char,vel,rot,unrot,split,rig=[find(s) for s in ['BlendSpaces|BlendspacePlayer','GetCharacter','GetVelocity','GetActorRotation','Math|Vector|UnrotateVector','Math|Vector|BreakVector','Misc.|ControlRig']]
for link in rig['inputPins'][0]['connectedPins']:await call_tool('BlueprintToolsets.BlueprintToolset.DisconnectPins',outputPin=link,inputPin=inp(rig))
for a,b in [(out(char),inp(rot)),(out(vel),inp(unrot)),(out(rot),inp(unrot,1)),(out(unrot),inp(split)),(out(split),inp(blend)),(out(split,1),inp(blend,1)),(out(blend),inp(rig))]:await call_tool('BlueprintToolsets.BlueprintToolset.ConnectPins',outputPin=a,inputPin=b)
n=unreal.load_object(None,blend['node']['refPath']);data=n.get_editor_property('node');data.set_editor_property('blend_space',unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Animations/BS_KnightRifleMove'));n.set_editor_property('node',data)
bp=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Animations/ABP_KnightRifle');assert unreal.BlueprintEditorLibrary.compile_blueprint(bp);assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
player=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Blueprints/BP_KnightPlayer')
ss=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);lib=unreal.SubobjectDataBlueprintFunctionLibrary
h=next(h for h in ss.k2_gather_subobject_data_for_blueprint(player) if str(lib.get_variable_name(lib.get_data(h)))=='GunMesh')
gun=lib.get_object_for_blueprint(lib.get_data(h),player)
idle=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Animations/A_KnightRifleIdle');pose=unreal.AnimPoseExtensions.get_anim_pose_at_time(idle,0,unreal.AnimPoseEvaluationOptions());hand=unreal.AnimPoseExtensions.get_bone_pose(pose,'hand_r',unreal.AnimPoseSpaces.WORLD)
rotation=(hand.rotation.inversed()*unreal.Rotator(pitch=0,yaw=-90,roll=0).quaternion()).rotator()
gun.set_editor_property('relative_rotation',rotation)
mh,reason=ss.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=h,new_class=unreal.SceneComponent,blueprint_context=player));assert lib.is_handle_valid(mh),str(reason);assert ss.rename_subobject(mh,unreal.Text('GunMuzzle'))
muzzle=lib.get_object_for_blueprint(lib.get_data(mh),player);muzzle.set_editor_property('relative_location',unreal.Vector(-117,0,25))
assert unreal.BlueprintEditorLibrary.compile_blueprint(player);assert unreal.EditorAssetLibrary.save_loaded_asset(player)
{'rifle_blend_compiled':True,'muzzle_added':True}
