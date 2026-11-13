import unreal
base='/Game/OneMoreTake/'
player=unreal.EditorAssetLibrary.load_asset(base+'Blueprints/BP_KnightPlayer')
for name,typ in [('IsWaveZombie','Boolean'),('ZombieWaveIndex','Integer'),('ZombieWakeOrder','Integer'),('ZombiePhase','Integer')]:
 assert unreal.BlueprintEditorLibrary.add_member_variable(player,name,unreal.BlueprintEditorLibrary.pin_type_from_text(typ));unreal.BlueprintEditorLibrary.set_blueprint_variable_instance_editable(player,name,True)
assert unreal.BlueprintEditorLibrary.compile_blueprint(player);assert unreal.EditorAssetLibrary.save_loaded_asset(player)
director=unreal.EditorAssetLibrary.load_asset(base+'Blueprints/BP_TakeDirector')
for name,typ in [('CurrentZombieWave','Integer'),('CurrentWaveRemaining','Integer'),('WaveRunning','Boolean'),('WaveSpawning','Boolean'),('WakeIndex','Integer'),('WaveZombieTotal','Integer'),('WavesComplete','Boolean'),('WaveTriggerRadius','Float (single-precision)'),('WaveRiseInterval','Float (single-precision)')]:
 assert unreal.BlueprintEditorLibrary.add_member_variable(director,name,unreal.BlueprintEditorLibrary.pin_type_from_text(typ));unreal.BlueprintEditorLibrary.set_blueprint_variable_instance_editable(director,name,True)
assert unreal.BlueprintEditorLibrary.compile_blueprint(director);c=unreal.get_default_object(unreal.BlueprintEditorLibrary.generated_class(director));c.set_editor_properties({'WaveTriggerRadius':700.0,'WaveRiseInterval':.55});assert unreal.BlueprintEditorLibrary.compile_blueprint(director);assert unreal.EditorAssetLibrary.save_loaded_asset(director)
folder=base+'Animations/Retargeted/ZombieWaves'
target=unreal.EditorAssetLibrary.load_asset('/Game/Characters/Zombie/StylizedZombie/Textures/SZombie_Variant_1/SK_SZombie_Variant_1');skel=target.get_editor_property('skeleton');at=unreal.AssetToolsHelpers.get_asset_tools()
f=unreal.BlendSpaceFactory1D();f.set_editor_properties({'target_skeleton':skel,'preview_skeletal_mesh':target});bs=at.create_asset('BS_ZombieRun',folder,unreal.BlendSpace1D,f);assert bs
params=list(bs.get_editor_property('blend_parameters'));params[0].set_editor_properties({'display_name':'Speed','min':0.0,'max':300.0,'grid_num':6});samples=[]
for name,speed,rate in [('ZW_Zombie_Idle',0,1.0),('ZW_Zombie_Running_Anim',280,.9)]:
 s=unreal.BlendSample();s.set_editor_properties({'animation':unreal.EditorAssetLibrary.load_asset(folder+'/'+name),'sample_value':unreal.Vector(speed,0,0),'rate_scale':rate});samples.append(s)
bs.set_editor_properties({'blend_parameters':params,'sample_data':samples,'target_weight_interpolation_speed_per_sec':8.0});editors=unreal.get_editor_subsystem(unreal.AssetEditorSubsystem);assert editors.open_editor_for_assets([bs]);assert unreal.EditorAssetLibrary.save_loaded_asset(bs);editors.close_all_editors_for_asset(bs)
f=unreal.AnimBlueprintFactory();f.set_editor_properties({'target_skeleton':skel,'preview_skeletal_mesh':target,'parent_class':unreal.AnimInstance});abp=at.create_asset('ABP_WaveZombie',folder,unreal.AnimBlueprint,f);assert abp
assert unreal.BlueprintEditorLibrary.add_member_variable(abp,'Speed',unreal.BlueprintEditorLibrary.pin_type_from_text('Float (single-precision)'))
g={'refPath':abp.get_path_name()+':AnimGraph'};nodes=await call_tool('BlueprintToolsets.BlueprintToolset.FindNodes',graph=g);info=await call_tool('BlueprintToolsets.BlueprintToolset.GetNodeInfos',nodes=nodes);root=next(n for n in info if n['typeId']=='Misc.|OutputPose')
refs=[]
for i,t in enumerate(['Animation|BlendSpaces|BlendspacePlayer','Animation|Montage|Slot\'DefaultSlot\'','Variables|Default|GetSpeed']):refs.append(await call_tool('BlueprintToolsets.BlueprintToolset.CreateNode',graph=g,typeId=t,pos={'x':-700+i*250,'y':0}))
infos=await call_tool('BlueprintToolsets.BlueprintToolset.GetNodeInfos',nodes=refs);blend,slot,speed=infos
obj=unreal.load_object(None,blend['node']['refPath']);data=obj.get_editor_property('node');data.set_editor_property('blend_space',bs);obj.set_editor_property('node',data)
for outpin,inpin in [(speed['outputPins'][0]['pinId'],blend['inputPins'][0]['pinId']),(blend['outputPins'][0]['pinId'],slot['inputPins'][0]['pinId']),(slot['outputPins'][0]['pinId'],root['inputPins'][0]['pinId'])]:await call_tool('BlueprintToolsets.BlueprintToolset.ConnectPins',outputPin=outpin,inputPin=inpin)
assert unreal.BlueprintEditorLibrary.compile_blueprint(abp);assert unreal.EditorAssetLibrary.save_loaded_asset(abp)
bp=unreal.BlueprintEditorLibrary.create_blueprint_asset_with_parent(base+'Blueprints/BP_WaveZombie',unreal.EditorAssetLibrary.load_blueprint_class(base+'Blueprints/BP_Guard'));assert bp;assert unreal.BlueprintEditorLibrary.compile_blueprint(bp);c=unreal.get_default_object(unreal.BlueprintEditorLibrary.generated_class(bp));c.set_editor_properties({'IsWaveZombie':True,'IsZombie':True,'IsEnemy':True,'ZombieWaveIndex':1,'ZombieWakeOrder':1,'UseEnemyRagdoll':True});assert unreal.BlueprintEditorLibrary.compile_blueprint(bp);assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
{'wave_blueprint_created':True,'zombie_animation_blueprint_created':True}
