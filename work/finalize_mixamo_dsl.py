import pathlib,json
exec(pathlib.Path('work/build_take2_dsl.py').read_text().split("parse='",1)[0])
s=json.loads(pathlib.Path('work/mixamo-rifle-player-before.json').read_text(encoding='utf-8-sig'))['returnValue']['dsl']
s=s.replace('/Game/OneMoreTake/Animations/A_KnightRifleFire.A_KnightRifleFire','/Game/OneMoreTake/Animations/Retargeted/Rifle/Knight_firing_rifle.Knight_firing_rifle')
s=s.replace('"DefaultSlot" 0.025 0.07 1.5 1','"DefaultSlot" 0.018 0.035 6.5 1').replace('(`KismetSystemLibrary.Delay` 0.14)','(`KismetSystemLibrary.Delay` 0.18)')
s=s.replace('(`SceneComponent.SetVisibility` (`self.GunTracer`) true false)','(`SceneComponent.SetVisibility` (`self.GunTracer`) true false)\n  (`SceneComponent.SetVisibility` (`self.MuzzleFlash`) true false)')
s=s.replace('(`SceneComponent.SetVisibility` (`self.GunTracer`) false false)','(`SceneComponent.SetVisibility` (`self.GunTracer`) false false)\n  (`SceneComponent.SetVisibility` (`self.MuzzleFlash`) false false)')
start=s.index('(event `UpdateMouseAim`');end=s.find('\n\n',start)
part=s[start:end]
# The imported aim stance shoulders the rifle slightly across the body.
old='(`self.K2_SetActorRotation` (`KismetMathLibrary.FindLookAtRotation` (`SceneComponent.K2_GetComponentLocation` (`self.GunMuzzle`)) _intersection))'
assert old in part,part
part=part.replace(old,'(`self.K2_SetActorRotation` (`KismetMathLibrary.ComposeRotators` (`KismetMathLibrary.FindLookAtRotation` (`SceneComponent.K2_GetComponentLocation` (`self.GunMuzzle`)) _intersection) (struct :`Yaw` 17.1)))')
s=s[:start]+part+s[end:]
pathlib.Path('work/mixamo-rifle-final.dsl').write_text(s)
