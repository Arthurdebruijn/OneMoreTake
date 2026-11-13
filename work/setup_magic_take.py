import unreal,json
base='/Game/OneMoreTake/'
for n in ['BP_KnightPlayer','BP_Guard','BP_TakeDirector','BP_CombatHUD']:assert unreal.EditorAssetLibrary.save_asset(base+'Blueprints/'+n)
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);backup=[{'label':a.get_actor_label(),'location':[a.get_actor_location().x,a.get_actor_location().y,a.get_actor_location().z],'yaw':a.get_actor_rotation().yaw,'extra':a.get_editor_property('ExtraTakeTwoGuard'),'ragdoll':a.get_editor_property('UseEnemyRagdoll'),'push':a.get_editor_property('RagdollPushStrength'),'lift':a.get_editor_property('RagdollLiftStrength'),'attack_rate':a.get_editor_property('AttackPlayRate')} for a in sub.get_all_level_actors() if 'BP_Guard' in str(a.get_class())];json.dump(backup,open(unreal.Paths.project_dir()+'work/rifle_guard_backup.json','w'));assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
bp=unreal.EditorAssetLibrary.load_asset(base+'Blueprints/BP_KnightPlayer')
for n,t in [('HasMagic','Boolean'),('MagicReady','Boolean'),('IsZombie','Boolean'),('MagicImpactPoint','Vector Structure'),('MagicPulseTime','Float (single-precision)'),('MagicDamage','Float (single-precision)'),('MagicRadius','Float (single-precision)')]:
 assert unreal.BlueprintEditorLibrary.add_member_variable(bp,n,unreal.BlueprintEditorLibrary.pin_type_from_text(t));unreal.BlueprintEditorLibrary.set_blueprint_variable_instance_editable(bp,n,True)
assert unreal.BlueprintEditorLibrary.compile_blueprint(bp);c=unreal.get_default_object(unreal.BlueprintEditorLibrary.generated_class(bp));c.set_editor_properties({'MagicDamage':55.0,'MagicRadius':230.0});assert unreal.BlueprintEditorLibrary.compile_blueprint(bp);assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
at=unreal.AssetToolsHelpers.get_asset_tools()
def solid(name,color,unlit=False):
 m=at.create_asset(name,base+'Materials',unreal.Material,unreal.MaterialFactoryNew());assert m;m.set_editor_properties({'used_with_skeletal_mesh':True,'two_sided':True})
 if unlit:m.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_UNLIT)
 x=unreal.MaterialEditingLibrary.create_material_expression(m,unreal.MaterialExpressionConstant3Vector,0,0);x.set_editor_property('constant',unreal.LinearColor(*color,1));assert unreal.MaterialEditingLibrary.connect_material_property(x,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR if unlit else unreal.MaterialProperty.MP_BASE_COLOR)
 if not unlit:
  r=unreal.MaterialEditingLibrary.create_material_expression(m,unreal.MaterialExpressionConstant,0,200);r.set_editor_property('r',.9);unreal.MaterialEditingLibrary.connect_material_property(r,'',unreal.MaterialProperty.MP_ROUGHNESS)
 unreal.MaterialEditingLibrary.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m);return m
magic=solid('M_ArcaneCyan',(.04,2.4,5.0),True);flesh=solid('M_UndeadFlesh',(.16,.32,.075));armor=solid('M_UndeadArmor',(.035,.075,.045))
ring=solid('M_ArcaneRing',(.05,1.6,3.5),True);ring.set_editor_property('blend_mode',unreal.BlendMode.BLEND_MASKED)
uv=unreal.MaterialEditingLibrary.create_material_expression(ring,unreal.MaterialExpressionTextureCoordinate,-600,200)
custom=unreal.MaterialEditingLibrary.create_material_expression(ring,unreal.MaterialExpressionCustom,-300,200);ci=unreal.CustomInput();ci.set_editor_property('input_name','UV');custom.set_editor_properties({'inputs':[ci],'output_type':unreal.CustomMaterialOutputType.CMOT_FLOAT1,'code':'float r=length(UV-float2(0.5,0.5)); return step(0.43,r)*step(r,0.5);'});assert unreal.MaterialEditingLibrary.connect_material_expressions(uv,'',custom,'UV');assert unreal.MaterialEditingLibrary.connect_material_property(custom,'',unreal.MaterialProperty.MP_OPACITY_MASK);unreal.MaterialEditingLibrary.recompile_material(ring);assert unreal.EditorAssetLibrary.save_loaded_asset(ring)
ss=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);lib=unreal.SubobjectDataBlueprintFunctionLibrary;handles=ss.k2_gather_subobject_data_for_blueprint(bp)
mesh=next(h for h in handles if str(lib.get_variable_name(lib.get_data(h)))=='Mesh');capsule=next(h for h in handles if str(lib.get_variable_name(lib.get_data(h)))=='CapsuleComponent')
def add(name,cls,parent):
 h,reason=ss.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=parent,new_class=cls,blueprint_context=bp));assert lib.is_handle_valid(h),str(reason);assert ss.rename_subobject(h,unreal.Text(name));return lib.get_object_for_blueprint(lib.get_data(h),bp)
orb=add('MagicOrb',unreal.StaticMeshComponent,mesh);orb.set_static_mesh(unreal.EditorAssetLibrary.load_asset('/Engine/BasicShapes/Sphere'));orb.set_material(0,magic);orb.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION);orb.set_editor_properties({'relative_scale3d':unreal.Vector(.18,.18,.18),'visible':False,'cast_shadow':False})
impact=add('MagicRing',unreal.StaticMeshComponent,capsule);impact.set_static_mesh(unreal.EditorAssetLibrary.load_asset('/Engine/BasicShapes/Plane'));impact.set_material(0,ring);impact.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION);impact.set_editor_properties({'visible':False,'cast_shadow':False,'absolute_location':True,'absolute_rotation':True,'absolute_scale':True})
label=add('ZombieLabel',unreal.TextRenderComponent,capsule);label.set_editor_properties({'text':unreal.Text('UNDEAD'),'text_render_color':unreal.Color(130,255,100,255),'world_size':22.0,'relative_location':unreal.Vector(0,0,130),'relative_rotation':unreal.Rotator(pitch=0,yaw=180,roll=0),'absolute_rotation':True,'horizontal_alignment':unreal.HorizTextAligment.EHTA_CENTER,'visible':False})
assert unreal.BlueprintEditorLibrary.compile_blueprint(bp);assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
# A common punch animation supplies the zombies' swipes and the player's casting gesture.
for number in [1,2]:
 source=unreal.EditorAssetLibrary.load_asset('/Game/Characters/Mannequins/Anims/Unarmed/Attack/MM_Attack_0'+str(number));f=unreal.AnimSequenceFactory();f.set_editor_property('target_skeleton',unreal.EditorAssetLibrary.load_asset('/Game/CR/Demo/Meshes/SK_Mannequin'));a=at.create_asset('A_UndeadSwipe'+str(number),base+'Animations',unreal.AnimSequence,f);assert a
 frames=max(2,round(source.get_play_length()*30));poses=[unreal.AnimPoseExtensions.get_anim_pose_at_time(source,i/30,unreal.AnimPoseEvaluationOptions()) for i in range(frames+1)];ctrl=a.get_editor_property('controller');ctrl.open_bracket('Undead swipes and magic gesture');ctrl.set_frame_rate(unreal.FrameRate(numerator=30,denominator=1));ctrl.set_number_of_frames(unreal.FrameNumber(value=frames))
 for bone in unreal.AnimPoseExtensions.get_bone_names(poses[0]):
  ts=[unreal.AnimPoseExtensions.get_bone_pose(p,bone,unreal.AnimPoseSpaces.LOCAL) for p in poses]
  if str(bone)=='root':ts=[unreal.Transform()]*len(ts)
  ctrl.add_bone_track(bone);assert ctrl.set_bone_track_keys(bone,[t.translation for t in ts],[t.rotation for t in ts],[t.scale3d for t in ts])
 ctrl.close_bracket();a.set_editor_properties({'enable_root_motion':False,'force_root_lock':True});assert unreal.EditorAssetLibrary.save_loaded_asset(a)
magicbp=unreal.EditorAssetLibrary.duplicate_asset(base+'Animations/ABP_KnightRifle',base+'Animations/ABP_PlayerMagic');assert magicbp
seq=unreal.load_object(None,magicbp.get_path_name()+':AnimGraph.AnimGraphNode_SequencePlayer_0');data=seq.get_editor_property('node');data.set_editor_property('sequence',unreal.EditorAssetLibrary.load_asset(base+'Animations/A_GuardIdle'));seq.set_editor_property('node',data)
blend=unreal.load_object(None,magicbp.get_path_name()+':AnimGraph.AnimGraphNode_BlendSpacePlayer_0');data=blend.get_editor_property('node');data.set_editor_property('blend_space',unreal.EditorAssetLibrary.load_asset(base+'Animations/BS_GuardStrafe'));blend.set_editor_property('node',data)
assert unreal.BlueprintEditorLibrary.compile_blueprint(magicbp);assert unreal.EditorAssetLibrary.save_loaded_asset(magicbp)
{'magic_components_created':True,'undead_materials_created':True,'animation_blueprint_saved':True}
