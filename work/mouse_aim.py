import pathlib,json
exec(pathlib.Path('work/build_take2_dsl.py').read_text().split("parse='",1)[0])
s=json.loads(pathlib.Path('work/mouse-aim-before.json').read_text(encoding='utf-8-sig'))['returnValue']['dsl']
s=s.replace('(if (and (`self.HasGun`) (`self.FireHeld`) (`self.GunReady`))','(if (and (`self.HasGun`) (not (`self.IsDead`)) (not (`self.SceneLocked`))) (`self.UpdateMouseAim`))\n  (if (and (`self.HasGun`) (`self.FireHeld`) (`self.GunReady`))',1)
s=s.replace('(set `self.HasGun` true)','''(set `self.HasGun` true)
 (bind pc (`GameplayStatics.GetPlayerController` 0))
 (set `PlayerController.bShowMouseCursor` pc true)
 (`WidgetBlueprintLibrary.SetInputMode_GameAndUIEx` pc null "LockAlways" false false)''',1)
s=replace_form(s,'(event `FireGun`','''(event `FireGun`
 (if (and (`self.GunReady`) (`self.HasGun`) (`self.MouseAimValid`) (not (`self.IsDead`)) (not (`self.SceneLocked`)))
  (`self.UpdateMouseAim`)
  (set `self.GunReady` false)
  (bind start (+ (`self.K2_GetActorLocation`) (0.0 0.0 25.0)))
  (set `self.GunShotEnd` (+ start (* (`self.GetActorForwardVector`) 1800.0)))
  (bind trace (`KismetSystemLibrary.LineTraceSingle` start (`self.GunShotEnd`) "TraceTypeQuery1" false (`|MakeArray` self :!type "Actor Object Reference") "None" true))
  (if trace.ReturnValue
   (bind (blocking initial time distance location impact normal impactnormal material actor) (`GameplayStatics.BreakHitResult` trace.OutHit))
   (set `self.GunShotEnd` impact)
   (bind (guard isguard) (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` actor :!pure true))
   (if isguard
    (if (and (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsEnemy` guard) (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` guard)))
     (`GameplayStatics.ApplyDamage` guard 40.0 (`self.GetController`) self))))
  (`self.ShowGunShot`)
  (`AnimInstance.PlaySlotAnimationAsDynamicMontage` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) "/Game/OneMoreTake/Animations/A_KnightGunFire.A_KnightGunFire" "DefaultSlot" 0.05 0.1 2.5 1 -1.0 0.0)
  (`KismetSystemLibrary.Delay` 0.25)
  (set `self.GunReady` true)))''')
s=replace_form(s,'(event `ShowGunShot`','''(event `ShowGunShot`
 (bind start (+ (`self.K2_GetActorLocation`) (0.0 0.0 25.0)))
 (bind end (`self.GunShotEnd`))
 (`GameplayStatics.PlaySound2D` "/Game/OneMoreTake/Audio/S_Gunshot.S_Gunshot" 0.4)
 (`SceneComponent.K2_SetWorldLocationAndRotation` (`self.GunTracer`) (* (+ start end) 0.5) (`KismetMathLibrary.FindLookAtRotation` start end) false true)
 (`SceneComponent.SetWorldScale3D` (`self.GunTracer`) (`KismetMathLibrary.MakeVector` (/ (`KismetMathLibrary.VSize` (- end start)) 100.0) 0.025 0.025))
 (`SceneComponent.SetVisibility` (`self.GunTracer`) true false)
 (`KismetSystemLibrary.Delay` 0.055)
 (`SceneComponent.SetVisibility` (`self.GunTracer`) false false))''')
s+='''
(event `UpdateMouseAim`
 (bind (origin direction valid) (`PlayerController.DeprojectMousePositionToWorld` (`GameplayStatics.GetPlayerController` 0)))
 (set `self.MouseAimValid` false)
 (if valid
  (bind (t point intersects) (`KismetMathLibrary.LinePlaneIntersection_OriginNormal` origin (+ origin (* direction 100000.0)) (+ (`self.K2_GetActorLocation`) (0.0 0.0 25.0)) (0.0 0.0 1.0)))
  (if intersects
   (set `self.MouseAimValid` true)
   (set `self.MouseAimPoint` point)
   (`self.K2_SetActorRotation` (`KismetMathLibrary.FindLookAtRotation` (+ (`self.K2_GetActorLocation`) (0.0 0.0 25.0)) point)))))
'''
pathlib.Path('work/mouse-aim.dsl').write_text(s)
