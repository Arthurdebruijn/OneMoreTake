import unreal
at=unreal.AssetToolsHelpers.get_asset_tools()
mat=unreal.EditorAssetLibrary.load_asset('/Game/OneMoreTake/Materials/M_PixelArt')
if mat: unreal.MaterialEditingLibrary.delete_all_material_expressions(mat)
else: mat=at.create_asset('M_PixelArt','/Game/OneMoreTake/Materials',unreal.Material,unreal.MaterialFactoryNew())
assert mat
mat.set_editor_properties({'material_domain':unreal.MaterialDomain.MD_POST_PROCESS,'blendable_location':unreal.BlendableLocation.BL_SCENE_COLOR_AFTER_TONEMAPPING,'blendable_priority':100})
def expression(cls,x,y):
    return unreal.MaterialEditingLibrary.create_material_expression(mat,cls,x,y)
uv=expression(unreal.MaterialExpressionScreenPosition,-750,-150)
scene=expression(unreal.MaterialExpressionSceneTexture,-750,100)
scene.set_editor_properties({'scene_texture_id':unreal.SceneTextureId.PPI_POST_PROCESS_INPUT0,'filtered':False})
parameters=[]
for index,(name,value) in enumerate([('PixelWidth',640.0),('ColorLevels',32.0),('PaletteStrength',.3)]):
    p=expression(unreal.MaterialExpressionScalarParameter,-750,300+index*150)
    p.set_editor_properties({'parameter_name':name,'default_value':value})
    parameters.append(p)
custom=expression(unreal.MaterialExpressionCustom,-250,0)
custom_inputs=[]
for name in ['UV','InputColor','PixelWidth','ColorLevels','PaletteStrength']:
    entry=unreal.CustomInput()
    entry.set_editor_property('input_name',name)
    custom_inputs.append(entry)
custom.set_editor_properties({'output_type':unreal.CustomMaterialOutputType.CMOT_FLOAT3,'inputs':custom_inputs,'code':'''float2 size = View.ViewSizeAndInvSize.xy;
float blockSize = max(1.0, floor(size.x / max(PixelWidth, 1.0) + 0.5));
float2 pixelUV = (floor(UV * size / blockSize) * blockSize + blockSize * 0.5) / size;
pixelUV = clamp(pixelUV, 0.5 / size, 1.0 - 0.5 / size);
float2 sceneUV = ViewportUVToSceneTextureUV(pixelUV, 14);
float3 color = SceneTextureLookup(sceneUV, 14, false).rgb;
float levels = max(ColorLevels, 2.0);
float3 reduced = floor(saturate(color) * levels + 0.5) / levels;
return lerp(color, reduced, saturate(PaletteStrength));'''})
assert unreal.MaterialEditingLibrary.connect_material_expressions(uv,'ViewportUV',custom,'UV')
assert unreal.MaterialEditingLibrary.connect_material_expressions(scene,'Color',custom,'InputColor')
for p,n in zip(parameters,['PixelWidth','ColorLevels','PaletteStrength']):
    assert unreal.MaterialEditingLibrary.connect_material_expressions(p,'',custom,n)
assert unreal.MaterialEditingLibrary.connect_material_property(custom,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
errors=unreal.MaterialEditingLibrary.recompile_material(mat)
assert not errors,str(errors)
assert unreal.EditorAssetLibrary.save_loaded_asset(mat)
instance=at.create_asset('MI_PixelArt','/Game/OneMoreTake/Materials',unreal.MaterialInstanceConstant,unreal.MaterialInstanceConstantFactoryNew())
assert instance
unreal.MaterialEditingLibrary.set_material_instance_parent(instance,mat)
assert unreal.EditorAssetLibrary.save_loaded_asset(instance)
'Pixel art material compiled and saved'


