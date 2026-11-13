import unreal, math
folder='/Game/OneMoreTake/Animations/Retargeted/Pistol'
at=unreal.AssetToolsHelpers.get_asset_tools()
source=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Animations/Pistol/Pistol_Idle')
target=unreal.EditorAssetLibrary.load_asset('/Game/CR/LQ/CharacterModular/Modular_012_Grian09/Mesh/SKM_Grian09_1')
rig=at.create_asset('IK_PistolSource',folder,unreal.IKRigDefinition,unreal.IKRigDefinitionFactory());assert rig
c=unreal.IKRigController.get_controller(rig);assert c.set_skeletal_mesh(source);assert c.apply_auto_generated_retarget_definition()
rtg=at.create_asset('RTG_PistolToKnight',folder,unreal.IKRetargeter,unreal.IKRetargetFactory());assert rtg
rc=unreal.IKRetargeterController.get_controller(rtg)
rc.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE,rig);rc.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET,unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Animations/Retargeted/IK_KnightCombat'))
rc.set_preview_mesh(unreal.RetargetSourceOrTarget.SOURCE,source);rc.set_preview_mesh(unreal.RetargetSourceOrTarget.TARGET,target)
rc.add_default_ops();rc.auto_map_chains(unreal.AutoMapChainType.FUZZY,True);rc.auto_align_all_bones(unreal.RetargetSourceOrTarget.TARGET)
for a in [rig,rtg]:assert unreal.EditorAssetLibrary.save_loaded_asset(a)
data=unreal.AssetRegistryHelpers.get_asset_registry().get_asset_by_object_path('/Game/OneMoreTake/Animations/Pistol/Pistol_Idle_Anim.Pistol_Idle_Anim')
results=unreal.IKRetargetBatchOperation.duplicate_and_retarget([data],source,target,rtg,prefix='Knight_',target_path=folder,include_referenced_assets=False);assert len(results)==1
idle=unreal.EditorAssetLibrary.load_asset(str(results[0].package_name));count=round(idle.get_play_length()*30)+1
poses=[unreal.AnimPoseExtensions.get_anim_pose_at_time(idle,i/30,unreal.AnimPoseEvaluationOptions()) for i in range(count)]
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);tmp=sub.spawn_actor_from_class(unreal.SkeletalMeshActor,unreal.Vector(10000,0,1000),unreal.Rotator());mesh=tmp.get_component_by_class(unreal.SkeletalMeshComponent);mesh.set_skeletal_mesh_asset(target)
children=[b for b in unreal.AnimPoseExtensions.get_bone_names(poses[0]) if str(mesh.get_parent_bone(b))=='root'];roots=[unreal.AnimPoseExtensions.get_bone_pose(p,'root',unreal.AnimPoseSpaces.LOCAL) for p in poses]
ctrl=idle.get_editor_property('controller');ctrl.open_bracket('Ground pistol idle')
for bone in children:
 values=[]
 for p,r in zip(poses,roots):
  parent=unreal.Transform();parent.translation=unreal.Vector(0,0,r.translation.z);parent.rotation=r.rotation;parent.scale3d=r.scale3d;values.append(unreal.AnimPoseExtensions.get_bone_pose(p,bone,unreal.AnimPoseSpaces.LOCAL).multiply(parent))
 assert ctrl.set_bone_track_keys(bone,[t.translation for t in values],[t.rotation for t in values],[t.scale3d for t in values])
assert ctrl.set_bone_track_keys('root',[unreal.Vector()]*count,[unreal.Quat(0,0,0,1)]*count,[unreal.Vector(1,1,1)]*count);ctrl.close_bracket();idle.set_editor_properties({'enable_root_motion':False,'force_root_lock':True});assert unreal.EditorAssetLibrary.save_loaded_asset(idle)
pose=unreal.AnimPoseExtensions.get_anim_pose_at_time(idle,0,unreal.AnimPoseEvaluationOptions())
names=unreal.AnimPoseExtensions.get_bone_names(pose)
local={str(b):unreal.AnimPoseExtensions.get_bone_pose(pose,b,unreal.AnimPoseSpaces.LOCAL) for b in names}
world={str(b):unreal.AnimPoseExtensions.get_bone_pose(pose,b,unreal.AnimPoseSpaces.WORLD) for b in names}
forward=world['hand_r'].translation-world['upperarm_r'].translation;forward.z=0;forward=forward.normal();axis=unreal.MathLibrary.cross_vector_vector(forward,unreal.Vector(0,0,-1)).normal()
def axisquat(degrees):
 half=math.radians(degrees)*.5;return unreal.Quat(axis.x*math.sin(half),axis.y*math.sin(half),axis.z*math.sin(half),math.cos(half))
for name,duration in [('A_PistolFire',.24),('A_PistolReload',1.8)]:
 f=unreal.AnimSequenceFactory();f.set_editor_property('target_skeleton',target.get_editor_property('skeleton'));a=at.create_asset(name,folder,unreal.AnimSequence,f);assert a
 frames=round(duration*30);ctrl=a.get_editor_property('controller');ctrl.open_bracket('Simple pistol upper-body motion');ctrl.set_frame_rate(unreal.FrameRate(numerator=30,denominator=1));ctrl.set_number_of_frames(unreal.FrameNumber(value=frames))
 for b in names:
  bone=str(b);values=[]
  for i in range(frames+1):
   t=i/frames;v=unreal.Transform();v.translation=local[bone].translation;v.rotation=local[bone].rotation;v.scale3d=local[bone].scale3d
   if bone in ['upperarm_r','upperarm_l']:
    if 'Reload' in name:
     amount=math.sin(min(t/.22,1)*math.pi/2) if t<.22 else (1 if t<.75 else math.cos((t-.75)/.25*math.pi/2))
     angle=38*amount+(3*math.sin(t*math.pi*8)*math.sin(t*math.pi)**2 if bone=='upperarm_l' else 0)
    else:angle=-7*math.sin(min(t/.22,1)*math.pi/2)*(1-t)**2
    parent=world[str(mesh.get_parent_bone(b))].rotation;v.rotation=parent.inversed()*axisquat(angle)*world[bone].rotation
   values.append(v)
  ctrl.add_bone_track(b);assert ctrl.set_bone_track_keys(b,[v.translation for v in values],[v.rotation for v in values],[v.scale3d for v in values])
 ctrl.close_bracket();a.set_editor_properties({'enable_root_motion':False,'force_root_lock':True});assert unreal.EditorAssetLibrary.save_loaded_asset(a)
sub.destroy_actor(tmp)
bp=unreal.EditorAssetLibrary.duplicate_asset('/Game/OneMoreTake/Animations/ABP_KnightRifle','/Game/OneMoreTake/Animations/ABP_KnightPistol');assert bp
seq=unreal.load_object(None,bp.get_path_name()+':AnimGraph.AnimGraphNode_SequencePlayer_0');node=seq.get_editor_property('node');node.set_editor_property('sequence',idle);seq.set_editor_property('node',node);assert unreal.BlueprintEditorLibrary.compile_blueprint(bp);assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
# Point the barrel forward from the right palm, retaining a horizontal grip.
hand=world['hand_r'];rotation=(hand.rotation.inversed()*unreal.MathLibrary.make_rot_from_x(forward).quaternion()).rotator()
import json
json.dump({'rotation':{'Pitch':rotation.pitch,'Yaw':rotation.yaw,'Roll':rotation.roll},'idle':idle.get_path_name(),'hand':str(hand.translation),'left':str(world['hand_l'].translation)},open(unreal.Paths.project_dir()+'work/pistol-pose-info.json','w'))
{'retargeted':idle.get_name(),'generated':['A_PistolFire','A_PistolReload'],'gripRotation':str(rotation)}
