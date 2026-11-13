import unreal
at=unreal.AssetToolsHelpers.get_asset_tools()
task=unreal.AssetImportTask()
task.set_editor_properties({'filename':unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()+'work/director_cut.wav'),'destination_path':'/Game/OneMoreTake/Audio','destination_name':'S_DirectorCut','automated':True,'save':True})
at.import_asset_tasks([task])
assert len(task.get_objects())>0
created={}
for name in ['BP_CrownPickup','BP_FinishMark','BP_TakeDirector']:
    bp=unreal.BlueprintEditorLibrary.create_blueprint_asset_with_parent('/Game/OneMoreTake/Blueprints/'+name,unreal.Actor)
    assert bp,name
    created[name]=bp
ss=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);lib=unreal.SubobjectDataBlueprintFunctionLibrary
crown=unreal.EditorAssetLibrary.load_asset('/Game/Cartoony_Crown/fbx/lowpoly_cartoony_crown_extracted/source/Cartoony_Crown')
cube=unreal.EditorAssetLibrary.load_asset('/Engine/BasicShapes/Cube')
cylinder=unreal.EditorAssetLibrary.load_asset('/Engine/BasicShapes/Cylinder')
def add(bp,parent,name,cls):
    h,reason=ss.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=parent,new_class=cls,blueprint_context=bp))
    assert lib.is_handle_valid(h),str(reason)
    assert ss.rename_subobject(h,unreal.Text(name))
    return h,lib.get_object_for_blueprint(lib.get_data(h),bp)
def text(bp,parent,name,words,position,visible=True):
    h,c=add(bp,parent,name,unreal.TextRenderComponent)
    c.set_editor_properties({'text':unreal.Text(words),'world_size':32.0,'relative_location':unreal.Vector(*position),'relative_rotation':unreal.Rotator(pitch=0,yaw=180,roll=0),'absolute_rotation':True,'horizontal_alignment':unreal.HorizTextAligment.EHTA_CENTER,'visible':visible})
    return c
for name,bp in created.items():
    handles=ss.k2_gather_subobject_data_for_blueprint(bp)
    root=next(h for h in handles if lib.is_root_component(lib.get_data(h)))
    if name=='BP_CrownPickup':
        h,c=add(bp,root,'CrownMesh',unreal.StaticMeshComponent); c.set_static_mesh(crown)
        c.set_editor_properties({'relative_location':unreal.Vector(0,0,10),'relative_scale3d':unreal.Vector(1.2,1.2,1.2)})
        c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
        h,c=add(bp,root,'Pedestal',unreal.StaticMeshComponent); c.set_static_mesh(cylinder)
        c.set_editor_properties({'relative_location':unreal.Vector(0,0,-60),'relative_scale3d':unreal.Vector(.9,.9,.8)})
        c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
        text(bp,root,'LockedLabel','CROWN - LOCKED',(0,0,75))
        text(bp,root,'PickupLabel','COLLECT CROWN',(0,0,75),False)
    elif name=='BP_FinishMark':
        for cname,scale,rot in [('MarkStripeA',(.16,1.5,.025),45),('MarkStripeB',(.16,1.5,.025),-45)]:
            h,c=add(bp,root,cname,unreal.StaticMeshComponent);c.set_static_mesh(cube)
            c.set_editor_properties({'relative_scale3d':unreal.Vector(*scale),'relative_rotation':unreal.Rotator(pitch=0,yaw=rot,roll=0)})
            c.set_material(0,unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Materials/MI_SwordBrass'))
            c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
        text(bp,root,'MarkLabel','HIT YOUR MARK',(0,0,75))
    assert unreal.BlueprintEditorLibrary.compile_blueprint(bp)
    assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
player=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Blueprints/BP_KnightPlayer')
handles=ss.k2_gather_subobject_data_for_blueprint(player)
root=next(h for h in handles if str(lib.get_variable_name(lib.get_data(h)))=='CapsuleComponent')
h,c=add(player,root,'CarriedCrown',unreal.StaticMeshComponent)
c.set_static_mesh(crown);c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
c.set_editor_properties({'relative_location':unreal.Vector(0,0,105),'relative_scale3d':unreal.Vector(.8,.8,.8),'visible':False})
for name,typ in [('SceneLocked','Boolean'),('AttackImpactTime','Float (single-precision)'),('EnemyChargeTime','Float (single-precision)'),('AttackAnimation','AnimSequence Object Reference')]:
    assert unreal.BlueprintEditorLibrary.add_member_variable(player,name,unreal.BlueprintEditorLibrary.pin_type_from_text(typ)),name
    unreal.BlueprintEditorLibrary.set_blueprint_variable_instance_editable(player,name,True)
assert unreal.BlueprintEditorLibrary.compile_blueprint(player)
cdo=unreal.get_default_object(unreal.BlueprintEditorLibrary.generated_class(player))
cdo.set_editor_properties({'AttackImpactTime':.32,'EnemyChargeTime':1.2,'AttackAnimation':unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Animations/A_SwordStrike')})
assert unreal.EditorAssetLibrary.save_loaded_asset(player)
director=created['BP_TakeDirector']
for name,typ in [('Stage','Integer'),('Objective','String'),('DirectorNote','String'),('CrownRef','Actor Object Reference'),('MarkRef','Actor Object Reference'),('PlayerRef','/Game/OneMoreTake/Blueprints/BP_KnightPlayer Object Reference'),('EnemyRef','/Game/OneMoreTake/Blueprints/BP_KnightPlayer Object Reference')]:
    assert unreal.BlueprintEditorLibrary.add_member_variable(director,name,unreal.BlueprintEditorLibrary.pin_type_from_text(typ)),name
assert unreal.BlueprintEditorLibrary.compile_blueprint(director)
unreal.get_default_object(unreal.BlueprintEditorLibrary.generated_class(director)).set_editor_property('Objective','Defeat the guard')
assert unreal.EditorAssetLibrary.save_loaded_asset(director)
{'created':list(created),'audio':list(task.get_editor_property('imported_object_paths'))}
