import unreal
at=unreal.AssetToolsHelpers.get_asset_tools()
mat=at.create_asset('M_WeaponColor','/Game/OneMoreTake/Materials',unreal.Material,unreal.MaterialFactoryNew())
assert mat
color=unreal.MaterialEditingLibrary.create_material_expression(mat,unreal.MaterialExpressionVectorParameter)
color.set_editor_properties({'parameter_name':'Color','default_value':unreal.LinearColor(.65,.7,.8,1)})
assert unreal.MaterialEditingLibrary.connect_material_property(color,'',unreal.MaterialProperty.MP_BASE_COLOR)
assert not unreal.MaterialEditingLibrary.recompile_material(mat)
assert unreal.EditorAssetLibrary.save_loaded_asset(mat)
materials={}
for name,c in [('Steel',(.65,.75,.9,1)),('Brass',(.6,.32,.06,1)),('Leather',(.055,.018,.009,1))]:
    instance=at.create_asset('MI_Sword'+name,'/Game/OneMoreTake/Materials',unreal.MaterialInstanceConstant,unreal.MaterialInstanceConstantFactoryNew())
    assert instance
    unreal.MaterialEditingLibrary.set_material_instance_parent(instance,mat)
    assert unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(instance,'Color',unreal.LinearColor(*c))
    assert unreal.EditorAssetLibrary.save_loaded_asset(instance)
    materials[name]=instance
bp=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Blueprints/BP_KnightPlayer')
ss=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);lib=unreal.SubobjectDataBlueprintFunctionLibrary
handles=ss.k2_gather_subobject_data_for_blueprint(bp)
parts={str(lib.get_variable_name(lib.get_data(h))):lib.get_object_for_blueprint(lib.get_data(h),bp) for h in handles}
root=next(h for h in handles if str(lib.get_variable_name(lib.get_data(h)))=='SwordRoot')
h,reason=ss.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.StaticMeshComponent,blueprint_context=bp))
assert lib.is_handle_valid(h),str(reason)
assert ss.rename_subobject(h,unreal.Text('SwordTip'))
tip=lib.get_object_for_blueprint(lib.get_data(h),bp)
tip.set_static_mesh(unreal.EditorAssetLibrary.load_asset('/Engine/BasicShapes/Cone'))
tip.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
tip.set_editor_properties({'relative_location':unreal.Vector(0,0,87),'relative_scale3d':unreal.Vector(.055,.12,.1),'can_ever_affect_navigation':False})
tip.set_material(0,materials['Steel'])
parts['SwordBlade'].set_material(0,materials['Steel'])
parts['SwordGuard'].set_material(0,materials['Brass'])
parts['SwordGrip'].set_material(0,materials['Leather'])
assert unreal.BlueprintEditorLibrary.compile_blueprint(bp)
assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
guard=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Blueprints/BP_Guard')
assert unreal.BlueprintEditorLibrary.compile_blueprint(guard)
assert unreal.EditorAssetLibrary.save_loaded_asset(guard)
assert unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True,True)
'Sword materials and tip saved; death now stops character movement'
