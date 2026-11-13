import pathlib,json
exec(pathlib.Path('work/build_take2_dsl.py').read_text().split("parse='",1)[0])
s=json.loads(pathlib.Path('work/hitfix-before.json').read_text(encoding='utf-8-sig'))['returnValue']['dsl']
s=s.replace('(event `self.ReceiveBeginPlay`','''(event `self.ReceiveBeginPlay`
 (set `self.NormalMeshMaterials` (`MeshComponent.GetMaterials` (`self.Mesh`)))
 (if (not (`self.IsEnemy`)) (`PrimitiveComponent.SetCollisionEnabled` (`self.BulletHitbox`) "NoCollision"))''',1)
s=s.replace('(set `self.IsDead` true)','(set `self.IsDead` true)\n      (`PrimitiveComponent.SetCollisionEnabled` (`self.BulletHitbox`) "NoCollision")',1)
s=replace_form(s,'(event `FlashOnHit`','''(event `FlashOnHit`
 (`MeshComponent.SetOverlayMaterial` (`self.Mesh`) null false 0)
 (for (mat index) (`self.NormalMeshMaterials`)
  (`PrimitiveComponent.SetMaterial` (`self.Mesh`) index "/Game/OneMoreTake/Materials/M_HitFlashWhite.M_HitFlashWhite"))
 (`KismetSystemLibrary.RetriggerableDelay` 0.14)
 (for (mat index) (`self.NormalMeshMaterials`)
  (`PrimitiveComponent.SetMaterial` (`self.Mesh`) index mat)))''')
s=s.replace('`KismetSystemLibrary.LineTraceSingle` _returnvalue (`self.GunShotEnd`) "TraceTypeQuery1"','`KismetSystemLibrary.SphereTraceSingle` _returnvalue (`self.GunShotEnd`) 14.0 "TraceTypeQuery1"')
assert 'SphereTraceSingle' in s
s=replace_form(s,'(event `UpdateMouseAim`','''(event `UpdateMouseAim`
 (bind rifleAnim (cast `/Game/OneMoreTake/Animations/ABP_KnightRifle` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`))))
 (set `/Game/OneMoreTake/Animations/ABP_KnightRifle.RifleLocalVelocity` (`KismetMathLibrary.LessLess_VectorRotator` (`self.GetVelocity`) (`self.K2_GetActorRotation`)) :`self` rifleAnim)
 (bind pc (`GameplayStatics.GetPlayerController` 0))
 (bind (origin direction valid) (`PlayerController.DeprojectMousePositionToWorld` pc))
 (set `self.MouseAimValid` false)
 (if valid
  (bind (t point intersects) (`KismetMathLibrary.LinePlaneIntersection_OriginNormal` origin (+ origin (* direction 100000.0)) (- (`self.K2_GetActorLocation`) (0.0 0.0 90.0)) (0.0 0.0 1.0)))
  (if intersects
   (set `self.MouseAimValid` true)
   (set `self.MouseAimPoint` (+ point (0.0 0.0 90.0)))
   (bind (hit hitvalid) (`PlayerController.GetHitResultUnderCursorByChannel` pc "TraceTypeQuery1" false))
   (if hitvalid
    (bind (blocking initial time distance location impact normal impactnormal material actor) (`GameplayStatics.BreakHitResult` hit))
    (bind (guard isguard) (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` actor :!pure true))
    (if isguard
     (if (and (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsEnemy` guard) (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` guard)))
      (set `self.MouseAimPoint` (+ (`self.K2_GetActorLocation` guard) (0.0 0.0 25.0))))))
   (`self.K2_SetActorRotation` (`KismetMathLibrary.ComposeRotators`
    (`KismetMathLibrary.FindLookAtRotation` (`self.K2_GetActorLocation`)
     (`KismetMathLibrary.MakeVector` (.x (`self.MouseAimPoint`)) (.y (`self.MouseAimPoint`)) (.z (`self.K2_GetActorLocation`))))
    (struct :`Yaw` 17.1))))))''')
pathlib.Path('work/hitfix.dsl').write_text(s)
