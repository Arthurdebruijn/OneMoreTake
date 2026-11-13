import pathlib,json
exec(pathlib.Path('work/build_take2_dsl.py').read_text().split("parse='",1)[0])
s=json.loads(pathlib.Path('work/tracer-before.json').read_text(encoding='utf-8-sig'))['returnValue']['dsl']
s=replace_form(s,'(event `FireGun`','''(event `FireGun`
 (if (and (`self.GunReady`) (`self.HasGun`) (`self.MouseAimValid`) (not (`self.IsDodging`)) (not (`self.IsDead`)) (not (`self.SceneLocked`)))
  (`self.UpdateMouseAim`)
  (set `self.GunReady` false)
  (set `self.GunShotStart` (`SceneComponent.K2_GetComponentLocation` (`self.GunMuzzle`)))
  (bind flat (`KismetMathLibrary.MakeVector` (- (.x (`self.MouseAimPoint`)) (.x (`self.K2_GetActorLocation`))) (- (.y (`self.MouseAimPoint`)) (.y (`self.K2_GetActorLocation`))) 0.0))
  (bind distance (`KismetMathLibrary.VSize` flat))
  (bind forward (`SceneComponent.GetForwardVector` (`self.GunMesh`)))
  (set `self.GunShotDirection` (`KismetMathLibrary.Normal` (`KismetMathLibrary.MakeVector` (.x forward) (.y forward) 0.0)))
  (if (> distance 60.0) (set `self.GunShotDirection` (`KismetMathLibrary.Normal` flat)))
  (bind goalXY (+ (`self.K2_GetActorLocation`) (* (`self.GunShotDirection`) (`KismetMathLibrary.FMax` distance 180.0))))
  (bind goal (`KismetMathLibrary.MakeVector` (.x goalXY) (.y goalXY) (.z (`self.MouseAimPoint`))))
  (set `self.GunShotDirection` (`KismetMathLibrary.Normal` (- goal (`self.GunShotStart`))))
  (set `self.GunShotEnd` (+ (`self.GunShotStart`) (* (`self.GunShotDirection`) 1800.0)))
  (bind trace (`KismetSystemLibrary.SphereTraceSingle` (`self.GunShotStart`) (`self.GunShotEnd`) 14.0 "TraceTypeQuery1" false (`|MakeArray` self :!type "Actor Object Reference") "None" true))
  (if (.ReturnValue trace)
   (bind (blocking initial time travel location impact normal impactnormal material actor) (`GameplayStatics.BreakHitResult` (.OutHit trace)))
   (set `self.GunShotEnd` (+ (`self.GunShotStart`) (* (`self.GunShotDirection`) travel)))
   (bind (guard ok) (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` actor :!pure true))
   (if ok
    (if (and (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsEnemy` guard) (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` guard)))
     (`GameplayStatics.ApplyDamage` guard 40.0 (`self.GetController`) self))))
  (`self.ShowGunShot`)
  (`AnimInstance.PlaySlotAnimationAsDynamicMontage` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) "/Game/OneMoreTake/Animations/Retargeted/Rifle/Knight_firing_rifle.Knight_firing_rifle" "DefaultSlot" 0.018 0.035 6.5 1 -1.0 0.0)
  (`KismetSystemLibrary.Delay` 0.18)
  (set `self.GunReady` true)))''')
s=replace_form(s,'(event `ShowGunShot`','''(event `ShowGunShot`
 (`GameplayStatics.PlaySound2D` "/Game/OneMoreTake/Audio/S_Gunshot.S_Gunshot" 0.4)
 (if (> (`KismetMathLibrary.VSize` (- (`self.GunShotEnd`) (`self.GunShotStart`))) 1.0)
  (`SceneComponent.K2_SetWorldLocationAndRotation` (`self.GunTracer`) (* (+ (`self.GunShotStart`) (`self.GunShotEnd`)) 0.5) (`KismetMathLibrary.FindLookAtRotation` (`self.GunShotStart`) (`self.GunShotEnd`)) false true)
  (`SceneComponent.SetWorldScale3D` (`self.GunTracer`) (`KismetMathLibrary.MakeVector` (/ (`KismetMathLibrary.VSize` (- (`self.GunShotEnd`) (`self.GunShotStart`))) 100.0) 0.025 0.025))
  (`SceneComponent.SetVisibility` (`self.GunTracer`) true false))
 (`SceneComponent.SetVisibility` (`self.MuzzleFlash`) true false)
 (`KismetSystemLibrary.Delay` 0.055)
 (`SceneComponent.SetVisibility` (`self.GunTracer`) false false)
 (`SceneComponent.SetVisibility` (`self.MuzzleFlash`) false false))''')
# Keep aim height independent of ragdoll tuning.
a=s.index('(event `UpdateMouseAim`');b=s.index('\n\n',a);entry=s[a:b]
entry=entry.replace('(`KismetMathLibrary.MakeVector` 0.0 0.0 (`self.RagdollLiftStrength`))','(0.0 0.0 90.0)')
needle='(`self.K2_SetActorRotation` (`KismetMathLibrary.ComposeRotators`'
# Avoid jitter when the cursor is almost exactly over the player.
p=entry.index(needle);entry=entry[:p]+'(if (> (`KismetMathLibrary.VSize` (- (`self.MouseAimPoint`) (`self.K2_GetActorLocation`))) 60.0)\n      '+entry[p:-1]+'))'
s=s[:a]+entry+s[b:]
pathlib.Path('work/tracer-fixed.dsl').write_text(s)
