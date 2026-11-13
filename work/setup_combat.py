import unreal
bp=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Blueprints/BP_KnightPlayer')
for name,typ in [('Health','Float (single-precision)'),('AttackDamage','Float (single-precision)'),('AttackReach','Float (single-precision)'),('IsAttacking','Boolean'),('IsDead','Boolean'),('IsEnemy','Boolean'),('IsWindingUp','Boolean'),('StatusMessage','String')]:
    pin=unreal.BlueprintEditorLibrary.pin_type_from_text(typ)
    assert unreal.BlueprintEditorLibrary.add_member_variable(bp,name,pin),name
for name in ['SwordAttack','DealSwordDamage','EnemyWindup']:
    unreal.BlueprintEditorLibrary.add_function_graph(bp,name)
# Attack needs delays, so its entry will be a custom event; remove the empty function of same name.
unreal.BlueprintEditorLibrary.remove_function_graph(bp,'SwordAttack')
unreal.BlueprintEditorLibrary.remove_function_graph(bp,'EnemyWindup')
ss=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
lib=unreal.SubobjectDataBlueprintFunctionLibrary
handles=ss.k2_gather_subobject_data_for_blueprint(bp)
byname={str(lib.get_variable_name(lib.get_data(h))):h for h in handles}
def add(name,cls,parent):
    h,reason=ss.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=parent,new_class=cls,blueprint_context=bp))
    assert lib.is_handle_valid(h),str(reason)
    assert ss.rename_subobject(h,unreal.Text(name))
    return h,lib.get_object_for_blueprint(lib.get_data(h),bp)
sword_h,sword=add('SwordRoot',unreal.SceneComponent,byname['Mesh'])
cube=unreal.EditorAssetLibrary.load_asset('/Engine/BasicShapes/Cube')
for name,loc,scale in [('SwordBlade',(0,0,43),(.055,.12,.78)),('SwordGuard',(0,0,3),(.09,.30,.055)),('SwordGrip',(0,0,-7),(.075,.075,.16))]:
    h,c=add(name,unreal.StaticMeshComponent,sword_h)
    assert c.set_static_mesh(cube)
    c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
    c.set_editor_properties({'relative_location':unreal.Vector(*loc),'relative_scale3d':unreal.Vector(*scale),'can_ever_affect_navigation':False})
h,warn=add('AttackWarning',unreal.TextRenderComponent,byname['CapsuleComponent'])
warn.set_editor_properties({'text':unreal.Text('!'),'world_size':75.0,'text_render_color':unreal.Color(r=255,g=35,b=20,a=255),'relative_location':unreal.Vector(0,0,155),'relative_rotation':unreal.Rotator(pitch=0,yaw=180,roll=0),'absolute_rotation':True,'visible':False,'horizontal_alignment':unreal.HorizTextAligment.EHTA_CENTER})
# Camera change requested by user.
boom=lib.get_object_for_blueprint(lib.get_data(byname['CameraBoom']),bp)
boom.set_editor_property('relative_rotation',unreal.Rotator(pitch=-25,yaw=0,roll=0))
assert unreal.BlueprintEditorLibrary.compile_blueprint(bp)
cdo=unreal.get_default_object(unreal.BlueprintEditorLibrary.generated_class(bp))
cdo.set_editor_properties({'Health':100.0,'AttackDamage':34.0,'AttackReach':210.0,'StatusMessage':'Defeat the guard.','IsEnemy':False})
assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
'Combat variables, sword components, warning, and 25-degree camera created'

