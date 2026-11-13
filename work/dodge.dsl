(event `SwordAttack`
  (if (and (not (`self.IsAttacking`)) (not (`self.IsDodging`)) (not (`self.IsDead`)) (not (`self.SceneLocked`)))
    (set `self.IsAttacking` true)
    (if (not (`self.IsEnemy`)) (`self.FindMeleeTarget`))
    ; Each combatant independently alternates A, B, A, B on accepted attacks.
    (if (`self.UseSecondAttack`)
      (set `self.AttackAnimation` (`self.AttackAnimationB`))
      (set `self.AttackImpactTime` (/ 0.6 (`self.AttackPlayRate`)))
      (set `self.LastAttackVariant` 2)
      (else
        (set `self.AttackAnimation` (`self.AttackAnimationA`))
        (set `self.AttackImpactTime` (/ 0.5 (`self.AttackPlayRate`)))
        (set `self.LastAttackVariant` 1)))
    (set `self.UseSecondAttack` (not (`self.UseSecondAttack`)))
    (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`))
    (`AnimInstance.PlaySlotAnimationAsDynamicMontage` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) (`self.AttackAnimation`) "DefaultSlot" 0.08 0.12 (`self.AttackPlayRate`) 1 -1.0 0.0)
    (`KismetSystemLibrary.Delay` (`self.AttackImpactTime`))
    (if (and (not (`self.IsDead`)) (not (`self.SceneLocked`)))
      (`self.DealSwordDamage`))
    (if (`self.IsEnemy`)
      (`KismetSystemLibrary.Delay` 0.12)
      (else
        (`KismetSystemLibrary.Delay` 0.08)))
    (if (and (not (`self.IsDead`)) (not (`self.SceneLocked`)))
      (`AnimInstance.StopSlotAnimation` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) 0.12 "DefaultSlot"))
    (if (`self.IsEnemy`)
      (`KismetSystemLibrary.Delay` 0.15))
    (set `self.IsAttacking` false)
    (set `self.MeleeTarget` null)
    (if (`self.IsEnemy`)
      (set `self.HasAttackTurn` false)
      (set `self.AttackRest` 1.0))))

(event `EnemyWindup`
  (if (and (not (`self.IsDead`)) (not (`self.IsWindingUp`)) (not (`self.SceneLocked`)))
    (set `self.IsWindingUp` true)
    (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`))
    (`SceneComponent.SetVisibility` (`self.AttackWarning`) true false)
    (`KismetSystemLibrary.Delay` (`self.EnemyChargeTime`))
    (`SceneComponent.SetVisibility` (`self.AttackWarning`) false false)
    (set `self.IsWindingUp` false)
    (if (and (not (`self.IsDead`)) (not (`self.SceneLocked`)))
      (`self.SwordAttack`))))

(event `LockForCut`
  (set `self.SceneLocked` true)
  (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`)))

(event `Key|LeftMouseButton`
  (params (Key :type "Key Structure"))
  (:`Pressed`
    (if (`self.HasGun`)
      (set `self.FireHeld` true)
      (`self.FireGun`)
      (else
        (`self.SwordAttack`))))
  (:`Released`
    (set `self.FireHeld` false)))

(event `Key|R`
  (params (Key :type "Key Structure"))
  (:`Pressed`
    (`self.RestartCurrentTake`)))

(event `self.ReceiveAnyDamage`
  (params (Damage :type "Float (single-precision)") (DamageType :type "DamageType Object Reference") (InstigatedBy :type "Controller Object Reference") (DamageCauser :type "Actor Object Reference"))
  (if (not (`self.IsDodging`))
  (if (`self.IsDead`)
    _
    (elif (> Damage 0.0)
      (`self.FlashOnHit`)
      (if (not (`self.IsEnemy`))
        (`PlayerCameraManager.StartCameraShake` (`GameplayStatics.GetPlayerCameraManager` 0) "/Game/OneMoreTake/Blueprints/BP_PlayerHitShake.BP_PlayerHitShake_C" 1.0 "CameraLocal" (struct)))))
  (set `self.Health` (`KismetMathLibrary.FMax` (- (`self.Health`) Damage)))
  (if (<= (`self.Health`) 0.0)
    (set `self.IsDead` true)
    (`PrimitiveComponent.SetCollisionEnabled` (`self.BulletHitbox`) "NoCollision")
    (set `self.HasAttackTurn` false)
    (set `self.IsAttacking` false)
    (set `self.IsWindingUp` false)
    (`SceneComponent.SetVisibility` (`self.AttackWarning`) false false)
    (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`))
    (`ActorComponent.Deactivate` (`self.CharacterMovement`))
    (`PrimitiveComponent.SetCollisionEnabled` (`self.CapsuleComponent`) "NoCollision")
    (`SkeletalMeshComponent.PlayAnimation` (`self.Mesh`) "/Game/OneMoreTake/Animations/A_KnightDeath.A_KnightDeath" false)
    (if (`self.IsEnemy`)
      (set `self.StatusMessage` "CUT! Guard defeated. Press R for another take.")
      (else
        (set `self.StatusMessage` "Take failed. Resetting...")
        (`KismetSystemLibrary.Delay` 2.0)
        (`self.RestartCurrentTake`)))
    (else
      (`self.LaunchCharacter` (* (`KismetMathLibrary.Normal` (- (`self.K2_GetActorLocation`) (`self.K2_GetActorLocation` DamageCauser))) 170.0) true)))))

(event `self.ReceiveTick`
  (params (DeltaSeconds :type "Float (single-precision)"))
  (if (`self.IsDodging`) (`self.TickDodge` DeltaSeconds))
  (if (and (not (`self.IsEnemy`)) (`self.IsAttacking`) (not (`self.IsDead`)) (not (`self.SceneLocked`))) (`self.TickMeleeAssist` DeltaSeconds))
  (if (and (`self.HasGun`) (not (`self.IsDead`)) (not (`self.SceneLocked`)))
    (`self.UpdateMouseAim`))
  (if (and (`self.HasGun`) (`self.FireHeld`) (`self.GunReady`) (not (`self.IsDodging`)))
    (`self.FireGun`))
  (if (and (`self.IsEnemy`) (not (`self.SceneLocked`)) (not (`self.IsDead`)))
    (set `self.AttackRest` (`KismetMathLibrary.FMax` (- (`self.AttackRest`) DeltaSeconds)))
    (bind _asbp_knight_player (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` (`GameplayStatics.GetPlayerCharacter` 0)))
    (bind _returnvalue (`KismetMathLibrary.Normal` (- (`self.K2_GetActorLocation` _asbp_knight_player) (`self.K2_GetActorLocation`))))
    (bind _returnvalue_2 (`self.GetDistanceTo` _asbp_knight_player))
    (if (and (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` _asbp_knight_player)) (not (`self.IsAttacking`)) (not (`self.IsWindingUp`)))
      (if (not (`self.HasAttackTurn`))
        (set `self.CanTakeAttackTurn` (<= (`self.AttackRest`) 0.0))
        (bind _outactors (`GameplayStatics.GetAllActorsOfClass` "/Game/OneMoreTake/Blueprints/BP_Guard.BP_Guard_C"))
        (for _array_element _outactors
          (bind _asbp_knight_player_2 (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` _array_element))
          (if (and (!= _array_element self) (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` _asbp_knight_player_2)))
            (if (or (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.HasAttackTurn` _asbp_knight_player_2) (and (<= (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.AttackRest` _asbp_knight_player_2) 0.0) (< (`self.GetDistanceTo` _asbp_knight_player_2 _asbp_knight_player) _returnvalue_2)))
              (set `self.CanTakeAttackTurn` false))))
        (if (`self.CanTakeAttackTurn`)
          (set `self.HasAttackTurn` true)))
      (if (`self.HasAttackTurn`)
        (if (> _returnvalue_2 165.0)
          (`self.AddMovementInput` _returnvalue)
          (else
            (`self.K2_SetActorRotation` (`KismetMathLibrary.FindLookAtRotation` (`self.K2_GetActorLocation`) (`self.K2_GetActorLocation` _asbp_knight_player)))
            (`self.EnemyWindup`)))
        (elif (< _returnvalue_2 330.0)
          (`self.AddMovementInput` _returnvalue -0.8)
          (elif (> _returnvalue_2 440.0)
            (`self.AddMovementInput` _returnvalue 0.65))))
      (bind _outactors_2 (`GameplayStatics.GetAllActorsOfClass` "/Game/OneMoreTake/Blueprints/BP_Guard.BP_Guard_C"))
      (for _array_element_2 _outactors_2
        (if (and (!= _array_element_2 self) (< (`self.GetDistanceTo` _array_element_2) 150.0))
          (`self.AddMovementInput` (`KismetMathLibrary.Normal` (- (`self.K2_GetActorLocation`) (`self.K2_GetActorLocation` _array_element_2))) 0.7))))))

(event `EnhancedInput|/Game/Input/Actions/IA_Move`
  (params (ActionValue :type "Vector2D Structure") (ElapsedSeconds :type "Float (double-precision)") (TriggeredSeconds :type "Float (double-precision)") (InputAction :type "InputAction Object Reference" :default "/Game/Input/Actions/IA_Move.IA_Move"))
  (:`Triggered`
    (`self.Move` ActionValue_X ActionValue_Y)))

(event `EnhancedInput|/Game/Input/Actions/IA_Look`
  (params (ActionValue :type "Vector2D Structure") (ElapsedSeconds :type "Float (double-precision)") (TriggeredSeconds :type "Float (double-precision)") (InputAction :type "InputAction Object Reference" :default "/Game/Input/Actions/IA_Look.IA_Look"))
  (:`Triggered`
    (`self.Aim` ActionValue_X ActionValue_Y)))

(event `self.Primary Thumbstick`
  (params (Axis :type "Vector2D Structure"))
  (`self.Move` Axis_X Axis_Y))

(event `self.Secondary Thumbstick`
  (params (Axis :type "Vector2D Structure"))
  (`self.Aim` Axis_X Axis_Y))

(event `EnhancedInput|/Game/Input/Actions/IA_MouseLook`
  (params (ActionValue :type "Vector2D Structure") (ElapsedSeconds :type "Float (double-precision)") (TriggeredSeconds :type "Float (double-precision)") (InputAction :type "InputAction Object Reference" :default "/Game/Input/Actions/IA_MouseLook.IA_MouseLook"))
  (:`Triggered`
    (`self.Aim` ActionValue_X ActionValue_Y)))

(event `EnhancedInput|/Game/Input/Actions/IA_Jump`
 (params (ActionValue :type Boolean) (ElapsedSeconds :type "Float (double-precision)") (TriggeredSeconds :type "Float (double-precision)") (InputAction :type "InputAction Object Reference" :default "/Game/Input/Actions/IA_Jump.IA_Jump"))
 (:`Started` (`self.Dodge`)))

(event `self.Touch Jump Start` (`self.Dodge`))

(event `self.Touch Jump End`)

(event `self.ReceiveBeginPlay`
  (set `self.DodgeReady` true)
  (set `self.NormalMeshMaterials` (`MeshComponent.GetMaterials` (`self.Mesh`)))
  (if (not (`self.IsEnemy`))
    (`PrimitiveComponent.SetCollisionEnabled` (`self.BulletHitbox`) "NoCollision"))
  (set `self.GunReady` true)
  (if (== (`GameplayStatics.ParseOption` (`GameModeBase.OptionsString` (`GameplayStatics.GetGameMode`)) "Take") "2")
    (if (not (`self.IsEnemy`))
      (`self.EquipGun`))
    (elif (`self.ExtraTakeTwoGuard`)
      (`self.K2_DestroyActor`))))

(event `EquipGun`
  (bind _returnvalue (`GameplayStatics.GetPlayerController` 0))
  (set `self.HasGun` true)
  (`SkeletalMeshComponent.SetAnimInstanceClass` (`self.Mesh`) "/Game/OneMoreTake/Animations/ABP_KnightRifle.ABP_KnightRifle_C")
  (set `CharacterMovementComponent.bOrientRotationToMovement` false (`self.CharacterMovement`))
  (set `PlayerController.bShowMouseCursor` true _returnvalue)
  (`WidgetBlueprintLibrary.SetInputMode_GameAndUIEx` _returnvalue null "LockAlways" false)
  (`SceneComponent.SetVisibility` (`self.SwordRoot`) false true)
  (`SceneComponent.K2_AttachToComponent` (`self.GunMesh`) (`self.Mesh`) "hand_r" "SnapToTarget" "KeepRelative" "KeepRelative" false)
  (`SceneComponent.SetVisibility` (`self.GunMesh`) true false))

(event `RestartCurrentTake`
  (if (`self.HasGun`)
    (`GameplayStatics.OpenLevel` "L_MovieSet" true "Take=2")
    (else
      (`GameplayStatics.OpenLevel` "L_MovieSet" true "Take=1"))))

(event `FireGun`
  (bind _returnvalue (`SceneComponent.K2_GetComponentLocation` (`self.GunMuzzle`)))
  (if (and (`self.GunReady`) (`self.HasGun`) (`self.MouseAimValid`) (not (`self.IsDead`)) (not (`self.SceneLocked`)))
    (`self.UpdateMouseAim`)
    (set `self.GunReady` false)
    (set `self.GunShotEnd` (+ _returnvalue (* (`KismetMathLibrary.Normal` (- (`self.MouseAimPoint`) (`SceneComponent.K2_GetComponentLocation` (`self.GunMuzzle`)))) 1800.0)))
    (bind (_outhit _returnvalue_2) (`KismetSystemLibrary.SphereTraceSingle` _returnvalue (`self.GunShotEnd`) 14.0 "TraceTypeQuery1" false (`|MakeArray` self :!type "Actor Object Reference")))
    (bind (_bblockinghit _binitialoverlap _time _distance _location _impactpoint _normal _impactnormal _physmat _hitactor) (`GameplayStatics.BreakHitResult` _outhit))
    (bind (_asbp_knight_player _bsuccess) (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` _hitactor :!pure true))
    (if _returnvalue_2
      (set `self.GunShotEnd` _impactpoint)
      (if _bsuccess
        (if (and (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsEnemy` _asbp_knight_player) (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` _asbp_knight_player)))
          (`GameplayStatics.ApplyDamage` _asbp_knight_player 40.0 (`self.GetController`) self))))
    (`self.ShowGunShot`)
    (`AnimInstance.PlaySlotAnimationAsDynamicMontage` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) "/Game/OneMoreTake/Animations/Retargeted/Rifle/Knight_firing_rifle.Knight_firing_rifle" "DefaultSlot" 0.018 0.035 6.5 1 -1.0 0.0)
    (`KismetSystemLibrary.Delay` 0.18)
    (set `self.GunReady` true)))

(event `ShowGunShot`
  (bind _returnvalue (`SceneComponent.K2_GetComponentLocation` (`self.GunMuzzle`)))
  (bind _gunshotend (`self.GunShotEnd`))
  (`GameplayStatics.PlaySound2D` "/Game/OneMoreTake/Audio/S_Gunshot.S_Gunshot" 0.4)
  (`SceneComponent.K2_SetWorldLocationAndRotation` (`self.GunTracer`) (* (+ _returnvalue _gunshotend) 0.5) (`KismetMathLibrary.FindLookAtRotation` _returnvalue _gunshotend) false true)
  (`SceneComponent.SetWorldScale3D` (`self.GunTracer`) (`KismetMathLibrary.MakeVector` (/ (`KismetMathLibrary.VSize` (- _gunshotend _returnvalue)) 100.0) 0.025 0.025))
  (`SceneComponent.SetVisibility` (`self.GunTracer`) true false)
  (`SceneComponent.SetVisibility` (`self.MuzzleFlash`) true false)
  (`KismetSystemLibrary.Delay` 0.055)
  (`SceneComponent.SetVisibility` (`self.GunTracer`) false false)
  (`SceneComponent.SetVisibility` (`self.MuzzleFlash`) false false))

(event `UpdateMouseAim`
  (bind _returnvalue (`GameplayStatics.GetPlayerController` 0))
  (bind (_worldlocation _worlddirection _returnvalue_2) (`PlayerController.DeprojectMousePositionToWorld` _returnvalue))
  (bind (_t _intersection _returnvalue_3) (`KismetMathLibrary.LinePlaneIntersection_OriginNormal` _worldlocation (+ _worldlocation (* _worlddirection 100000.0)) (- (`self.K2_GetActorLocation`) (0.0 0.0 90.0)) (0.0 0.0 1.0)))
  (bind (_hitresult _returnvalue_4) (`PlayerController.GetHitResultUnderCursorByChannel` _returnvalue "TraceTypeQuery1" false))
  (bind (_bblockinghit _binitialoverlap _time _distance _location _impactpoint _normal _impactnormal _physmat _hitactor) (`GameplayStatics.BreakHitResult` _hitresult))
  (bind (_asbp_knight_player _bsuccess) (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` _hitactor :!pure true))
  (bind _asabp_knight_rifle (cast `/Game/OneMoreTake/Animations/ABP_KnightRifle` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`))))
  (set `/Game/OneMoreTake/Animations/ABP_KnightRifle.RifleLocalVelocity` (`KismetMathLibrary.LessLess_VectorRotator` (`self.GetVelocity`) (`self.K2_GetActorRotation`)) _asabp_knight_rifle)
  (set `self.MouseAimValid` false)
  (if _returnvalue_2
    (if _returnvalue_3
      (set `self.MouseAimValid` true)
      (set `self.MouseAimPoint` (+ _intersection (0.0 0.0 90.0)))
      (if _returnvalue_4
        (if _bsuccess
          (if (and (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsEnemy` _asbp_knight_player) (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` _asbp_knight_player)))
            (set `self.MouseAimPoint` (+ (`self.K2_GetActorLocation` _asbp_knight_player) (0.0 0.0 25.0))))))
      (`self.K2_SetActorRotation` (`KismetMathLibrary.ComposeRotators` (`KismetMathLibrary.FindLookAtRotation` (`self.K2_GetActorLocation`) (`KismetMathLibrary.MakeVector` (.x (`self.MouseAimPoint`)) (.y (`self.MouseAimPoint`)) (.z (`self.K2_GetActorLocation`)))) (struct :`Yaw` 17.1))))))

(event `FlashOnHit`
  (`MeshComponent.SetOverlayMaterial` (`self.Mesh`) null false 0)
  (for (_ _array_index) (`self.NormalMeshMaterials`)
    (`PrimitiveComponent.SetMaterial` (`self.Mesh`) _array_index "/Game/OneMoreTake/Materials/M_HitFlashWhite.M_HitFlashWhite"))
  (`KismetSystemLibrary.RetriggerableDelay` 0.14)
  (for (_array_element _array_index_2) (`self.NormalMeshMaterials`)
    (`PrimitiveComponent.SetMaterial` (`self.Mesh`) _array_index_2 _array_element)))

(fn `Aim`
  (params (`X Axis` :type "Float (single-precision)") (`Y Axis` :type "Float (double-precision)"))
  (`self.AddControllerYawInput` `X Axis`)
  (`self.AddControllerPitchInput` `Y Axis`))

(fn `DealSwordDamage`
  (bind _outactors (`GameplayStatics.GetAllActorsOfClass` "/Game/OneMoreTake/Blueprints/BP_KnightPlayer.BP_KnightPlayer_C"))
  (for _array_element _outactors
    (bind _asbp_knight_player (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` _array_element))
    (if (and (!= (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsEnemy` _asbp_knight_player) (`self.IsEnemy`)) (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` _asbp_knight_player)) (<= (`self.GetDistanceTo` _asbp_knight_player) (`self.AttackReach`)))
      (if (> (`KismetMathLibrary.Dot_VectorVector` (`self.GetActorForwardVector`) (`KismetMathLibrary.Normal` (- (`self.K2_GetActorLocation` _asbp_knight_player) (`self.K2_GetActorLocation`)))) 0.2)
        (`GameplayStatics.ApplyDamage` _asbp_knight_player (`self.AttackDamage`) (`self.GetController`) self)))))

(fn `Move`
  (params (`X Axis` :type "Float (double-precision)") (`Y Axis` :type "Float (double-precision)"))
  (if (and (not (`self.IsDead`)) (not (`self.IsAttacking`)) (not (`self.IsDodging`)) (not (`self.SceneLocked`)))
    (`self.AddMovementInput` (0.0 1.0 0.0) `X Axis`)
    (`self.AddMovementInput` (1.0 0.0 0.0) `Y Axis`)))

(fn `UserConstructionScript`
  (`SceneComponent.K2_AttachToComponent` (`self.GunMesh`) (`self.Mesh`) "hand_r" "SnapToTarget" "KeepRelative" "KeepRelative" false)
  ; Attach the prop to the animated hand, not the character capsule.
  (`SceneComponent.K2_AttachToComponent` (`self.SwordRoot`) (`self.Mesh`) "hand_r" "SnapToTarget" "SnapToTarget" "KeepRelative" false))

(event `Dodge`
 (if (and (`self.DodgeReady`) (not (`self.IsDodging`)) (not (`self.IsAttacking`)) (not (`self.IsDead`)) (not (`self.SceneLocked`)) (not (`self.IsEnemy`)))
  (set `self.DodgeReady` false)
  (set `self.IsDodging` true)
  (set `self.MeleeTarget` null)
  (if (and (> (`KismetMathLibrary.VSize` (`self.GetVelocity`)) 10.0) (> (`KismetMathLibrary.VSize` (`self.GetLastMovementInputVector`)) 0.1))
   (set `self.DodgeDirection` (`KismetMathLibrary.Normal` (`self.GetLastMovementInputVector`)))
   (else (set `self.DodgeDirection` (`self.GetActorForwardVector`))))
  (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`))
  (`KismetSystemLibrary.Delay` 0.18)
  (set `self.IsDodging` false)
  (`KismetSystemLibrary.Delay` 0.47)
  (set `self.DodgeReady` true)))
(event `TickDodge`
 (params (DeltaSeconds :type "Float (single-precision)"))
 (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`))
 (`self.K2_SetActorLocation` (+ (`self.K2_GetActorLocation`) (* (`self.DodgeDirection`) (* 1450.0 DeltaSeconds))) true false))
(event `FindMeleeTarget`
 (set `self.MeleeTarget` null)
 (set `self.MeleeTargetDistance` 370.0)
 (for enemy (`GameplayStatics.GetAllActorsOfClass` "/Game/OneMoreTake/Blueprints/BP_Guard.BP_Guard_C")
  (bind guard (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` enemy))
  (if (and (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` guard)) (< (`self.GetDistanceTo` guard) (`self.MeleeTargetDistance`)))
   (if (> (`KismetMathLibrary.Dot_VectorVector` (`self.GetActorForwardVector`) (`KismetMathLibrary.Normal` (- (`self.K2_GetActorLocation` guard) (`self.K2_GetActorLocation`)))) 0.55)
    (set `self.MeleeTarget` guard)
    (set `self.MeleeTargetDistance` (`self.GetDistanceTo` guard))))))
(event `TickMeleeAssist`
 (params (DeltaSeconds :type "Float (single-precision)"))
 (if (`KismetSystemLibrary.IsValid` (`self.MeleeTarget`))
  (bind guard (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` (`self.MeleeTarget`)))
  (if (and (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` guard)) (< (`self.GetDistanceTo` guard) 450.0))
   (bind enemy (`self.K2_GetActorLocation` guard))
   (bind flat (`KismetMathLibrary.MakeVector` (.x enemy) (.y enemy) (.z (`self.K2_GetActorLocation`))))
   (bind direction (`KismetMathLibrary.Normal` (- flat (`self.K2_GetActorLocation`))))
   (`self.K2_SetActorRotation` (`KismetMathLibrary.FindLookAtRotation` (`self.K2_GetActorLocation`) flat))
   (if (> (`self.GetDistanceTo` guard) 130.0)
    (`self.K2_SetActorLocation` (`KismetMathLibrary.VInterpTo` (`self.K2_GetActorLocation`) (- flat (* direction 130.0)) DeltaSeconds 18.0) true false))
   (else (set `self.MeleeTarget` null)))))
