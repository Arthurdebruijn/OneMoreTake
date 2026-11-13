import unreal
at=unreal.AssetToolsHelpers.get_asset_tools()
target=unreal.EditorAssetLibrary.load_asset('/Game/CR/LQ/CharacterModular/Modular_012_Grian09/Mesh/SKM_Grian09_1')
folder='/Game/OneMoreTake/Animations/Retargeted'
target_rig=at.create_asset('IK_KnightCombat',folder,unreal.IKRigDefinition,unreal.IKRigDefinitionFactory())
ctl=unreal.IKRigController.get_controller(target_rig)
assert ctl.set_skeletal_mesh(target)
assert ctl.apply_auto_generated_retarget_definition()
unreal.EditorAssetLibrary.save_loaded_asset(target_rig)
inputs=[('/Game/OneMoreTake/Animations/Sword_And_Shield_Slash/Sword_And_Shield_Slash','/Game/OneMoreTake/Animations/Sword_And_Shield_Slash/Sword_And_Shield_Slash_Anim'),('/Game/OneMoreTake/Animations/Sword_And_Shield_Slash_2/Sword_And_Shield_Slash__1_','/Game/OneMoreTake/Animations/Sword_And_Shield_Slash_2/Sword_And_Shield_Slash__1__Anim')]
outputs=[]
for i,(mesh_path,anim_path) in enumerate(inputs):
    source=unreal.EditorAssetLibrary.load_asset(mesh_path)
    rig=at.create_asset('IK_MixamoSlash'+str(i+1),folder,unreal.IKRigDefinition,unreal.IKRigDefinitionFactory())
    c=unreal.IKRigController.get_controller(rig)
    assert c.set_skeletal_mesh(source)
    assert c.apply_auto_generated_retarget_definition()
    rtg=at.create_asset('RTG_Slash'+str(i+1)+'ToKnight',folder,unreal.IKRetargeter,unreal.IKRetargetFactory())
    rc=unreal.IKRetargeterController.get_controller(rtg)
    rc.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE,rig)
    rc.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET,target_rig)
    rc.set_preview_mesh(unreal.RetargetSourceOrTarget.SOURCE,source)
    rc.set_preview_mesh(unreal.RetargetSourceOrTarget.TARGET,target)
    rc.add_default_ops()
    rc.auto_map_chains(unreal.AutoMapChainType.FUZZY,True)
    rc.auto_align_all_bones(unreal.RetargetSourceOrTarget.TARGET)
    for a in [rig,rtg]: assert unreal.EditorAssetLibrary.save_loaded_asset(a)
    result=unreal.IKRetargetBatchOperation.duplicate_and_retarget([unreal.EditorAssetLibrary.find_asset_data(anim_path)],source,target,rtg,prefix='Knight_',target_path=folder,include_referenced_assets=False)
    assert len(result)==1,str(result)
    outputs.extend(str(a.package_name) for a in result)
    await asyncio.sleep(0)
outputs
