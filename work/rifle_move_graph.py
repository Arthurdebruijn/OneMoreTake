import unreal
graph={'refPath':'/Game/OneMoreTake/Animations/ABP_KnightRifle.ABP_KnightRifle:AnimGraph'}
refs=[]
for i,t in enumerate(['Animation|BlendSpaces|BlendspacePlayer','Variables|References|GetCharacter','Variables|EssentialMovementData|GetVelocity','Transformation|GetActorRotation','Math|Vector|UnrotateVector','Math|Vector|BreakVector']):
 refs.append(await call_tool('BlueprintToolsets.BlueprintToolset.CreateNode',graph=graph,typeId=t,pos={'x':-1500+i*200,'y':650}))
infos=await call_tool('BlueprintToolsets.BlueprintToolset.GetNodeInfos',nodes=refs)
[{ 'node':n['node'],'type':n['typeId'],'inputs':[(p['name'],p['pinId']) for p in n['inputPins']],'outputs':[(p['name'],p['pinId']) for p in n['outputPins']]} for n in infos]
