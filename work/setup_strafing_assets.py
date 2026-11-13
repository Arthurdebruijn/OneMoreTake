import unreal,math,random,wave,struct
from pathlib import Path
base='/Game/OneMoreTake';at=unreal.AssetToolsHelpers.get_asset_tools();lib=unreal.MaterialEditingLibrary
def material(name,color,emission=False,opacity=None):
 m=unreal.EditorAssetLibrary.load_asset(base+'/Materials/'+name)
 if m:return m
 m=at.create_asset(name,base+'/Materials',unreal.Material,unreal.MaterialFactoryNew())
 if emission:m.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_UNLIT)
 if opacity is not None:m.set_editor_property('blend_mode',unreal.BlendMode.BLEND_TRANSLUCENT)
 c=lib.create_material_expression(m,unreal.MaterialExpressionConstant3Vector,-300,0);c.set_editor_property('constant',unreal.LinearColor(*color,1));lib.connect_material_property(c,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR if emission else unreal.MaterialProperty.MP_BASE_COLOR)
 r=lib.create_material_expression(m,unreal.MaterialExpressionConstant,-300,200);r.set_editor_property('r',.65 if opacity is None else opacity);lib.connect_material_property(r,'',unreal.MaterialProperty.MP_ROUGHNESS if opacity is None else unreal.MaterialProperty.MP_OPACITY)
 lib.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m);return m
red=material('M_StrafeWarning',(1,.035,.005),True,.25);edge=material('M_StrafeEdge',(2,.14,.01),True);flash=material('M_StrafeFlash',(7,2,.1),True);smoke=material('M_StrafeSmoke',(.08,.07,.06));gray=material('M_FighterJetGray',(.32,.38,.43))
jetmesh=unreal.EditorAssetLibrary.load_asset(base+'/Art/FighterJet/Source/Main_LOD0_00_low_004');jetmesh.set_material(0,gray);assert unreal.EditorAssetLibrary.save_loaded_asset(jetmesh)
ss=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);bl=unreal.SubobjectDataBlueprintFunctionLibrary
def create(name):
 bp=unreal.EditorAssetLibrary.load_asset(base+'/Blueprints/'+name) or unreal.BlueprintEditorLibrary.create_blueprint_asset_with_parent(base+'/Blueprints/'+name,unreal.Actor);assert bp
 hs=ss.k2_gather_subobject_data_for_blueprint(bp);root=next(h for h in hs if str(bl.get_variable_name(bl.get_data(h)))=='DefaultSceneRoot');return bp,root
def component(bp,root,name,mesh,loc,scale,mat,rot=None):
 existing=next((h for h in ss.k2_gather_subobject_data_for_blueprint(bp) if str(bl.get_variable_name(bl.get_data(h)))==name),None)
 if existing:return bl.get_object_for_blueprint(bl.get_data(existing),bp)
 h,reason=ss.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.StaticMeshComponent,blueprint_context=bp));assert bl.is_handle_valid(h),str(reason);assert ss.rename_subobject(h,unreal.Text(name));c=bl.get_object_for_blueprint(bl.get_data(h),bp);c.set_static_mesh(mesh);c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION);c.set_editor_properties({'relative_location':unreal.Vector(*loc),'relative_scale3d':unreal.Vector(*scale),'visible':False,'cast_shadow':False});c.set_material(0,mat)
 if rot:c.set_editor_property('relative_rotation',rot)
 return c
cube=unreal.EditorAssetLibrary.load_asset('/Engine/BasicShapes/Cube');sphere=unreal.EditorAssetLibrary.load_asset('/Engine/BasicShapes/Sphere')
bp,root=create('BP_StrafingRun')
component(bp,root,'DangerStrip',cube,(0,0,4),(22,3,.025),red)
component(bp,root,'BorderLeft',cube,(0,-150,7),(22,.035,.035),edge)
component(bp,root,'BorderRight',cube,(0,150,7),(22,.035,.035),edge)
for i in range(7):component(bp,root,'Stripe'+str(i),cube,(-900+i*300,0,7),(.05,3,.025),edge)
component(bp,root,'Jet',jetmesh,(-2400,0,350),(.27,.27,.27),gray,unreal.Rotator(pitch=0,yaw=-90,roll=0))
for n,t in [('AttackState','Integer'),('RunsCompleted','Integer'),('RequiredRuns','Integer'),('StateTime','Float (single-precision)'),('NextRunDelay','Float (single-precision)'),('WarningDuration','Float (single-precision)'),('RunCooldown','Float (single-precision)'),('FlightTime','Float (single-precision)'),('JetX','Float (single-precision)'),('ImpactIndex','Integer'),('LastImpactIndex','Integer'),('PlayerHitThisRun','Boolean'),('ReverseRun','Boolean'),('PlayerRef','Actor Object Reference'),('DirectorRef','Actor Object Reference'),('ImpactPoint','Vector Structure')]:
 unreal.BlueprintEditorLibrary.add_member_variable(bp,n,unreal.BlueprintEditorLibrary.pin_type_from_text(t));unreal.BlueprintEditorLibrary.set_blueprint_variable_instance_editable(bp,n,True)
assert unreal.BlueprintEditorLibrary.compile_blueprint(bp);c=unreal.get_default_object(unreal.BlueprintEditorLibrary.generated_class(bp));c.set_editor_properties({'RequiredRuns':5,'NextRunDelay':4.0,'WarningDuration':1.8,'RunCooldown':3.5});assert unreal.BlueprintEditorLibrary.compile_blueprint(bp);assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
impact,root=create('BP_StrafeImpact');component(impact,root,'Flash',sphere,(0,0,20),(.75,.75,.6),flash);component(impact,root,'Smoke',sphere,(0,0,25),(.4,.4,.7),smoke)
assert unreal.BlueprintEditorLibrary.add_member_variable(impact,'Age',unreal.BlueprintEditorLibrary.pin_type_from_text('Float (single-precision)'));assert unreal.BlueprintEditorLibrary.compile_blueprint(impact);assert unreal.EditorAssetLibrary.save_loaded_asset(impact)
# Short synthetic alert, cannon rattle, and low jet roar for this first playable.
rate=22050;rng=random.Random(82);out=Path(unreal.Paths.project_dir())/'work'
def sound(name,duration,fn):
 vals=[];low=0
 for i in range(round(rate*duration)):
  t=i/rate;n=rng.uniform(-1,1);low=.92*low+.08*n;vals.append(fn(t,n,low))
 peak=max(abs(v) for v in vals) or 1
 with wave.open(str(out/(name+'.wav')),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate);f.writeframes(b''.join(struct.pack('<h',round(v/peak*.75*32767)) for v in vals))
 task=unreal.AssetImportTask();task.set_editor_properties({'filename':str(out/(name+'.wav')),'destination_path':base+'/Audio','destination_name':name,'automated':True,'save':True});at.import_asset_tasks([task]);assert task.get_objects()
sound('S_StrafeAlert',.5,lambda t,n,l:math.sin(2*math.pi*760*t)*max(0,math.sin(math.pi*t/.5))*(1 if t%.22<.13 else 0)*.5)
sound('S_JetFlyby',3.1,lambda t,n,l:(l*2+math.sin(2*math.pi*(95*t-6*t*t))*.08)*math.sin(math.pi*t/3.1)**.7)
sound('S_StrafeCannon',1.5,lambda t,n,l:(n*.65+math.sin(2*math.pi*95*t)*.35)*math.exp(-(t%.075)/.018)*math.sin(math.pi*t/1.5)**.4)
{'created':['BP_StrafingRun','BP_StrafeImpact'],'jetTriangles':jetmesh.get_num_triangles(0)}

