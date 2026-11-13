import unreal
bp=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Blueprints/BP_KnightPlayer')
ss=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);lib=unreal.SubobjectDataBlueprintFunctionLibrary
handles=ss.k2_gather_subobject_data_for_blueprint(bp)
root=next(h for h in handles if str(lib.get_variable_name(lib.get_data(h)))=='CapsuleComponent')
h,r=ss.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.StaticMeshComponent,blueprint_context=bp));assert lib.is_handle_valid(h)
assert ss.rename_subobject(h,unreal.Text('GunTracer'))
c=lib.get_object_for_blueprint(lib.get_data(h),bp)
c.set_static_mesh(unreal.EditorAssetLibrary.load_asset('/Engine/BasicShapes/Cube'));c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
c.set_material(0,unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Materials/MI_SwordBrass'))
c.set_editor_properties({'visible':False,'cast_shadow':False,'absolute_scale':True,'absolute_rotation':True,'absolute_location':True})
assert unreal.BlueprintEditorLibrary.compile_blueprint(bp);assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
t=unreal.AssetImportTask();t.set_editor_properties({'filename':unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()+'work/gunshot.wav'),'destination_path':'/Game/OneMoreTake/Audio','destination_name':'S_Gunshot','automated':True,'save':True})
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t]);assert t.get_objects()
'Gun feedback created'
