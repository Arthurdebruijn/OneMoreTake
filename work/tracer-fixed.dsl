(event `SwordAttack`
  (if (and (not (`self.IsAttacking`)) (not (`self.HitStaggered`)) (not (`self.LungePaused`)) (not (`self.HitReacting`)) (not (`self.IsDodging`)) (not (`self.IsDead`)) (not (`self.SceneLocked`)))
    (set `self.IsAttacking` true)
    (set `self.EnemyAttackInterrupted` false)
    (if (not (`self.IsEnemy`))
      (`self.FindMeleeTarget`))
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
    (if (and (not (`self.IsDead`)) (not (`self.SceneLocked`)) (not (`self.EnemyAttackInterrupted`)) (not (`self.HitStaggered`)) (not (`self.LungePaused`)))
      (`self.DealSwordDamage`))
    (if (`self.IsEnemy`)
      (`KismetSystemLibrary.Delay` 0.12)
      (else
        (`KismetSystemLibrary.Delay` 0.08)))
    (if (and (not (`self.IsDead`)) (not (`self.SceneLocked`)) (not (`self.HitReacting`)))
      (`AnimInstance.StopSlotAnimation` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) 0.12 "DefaultSlot"))
    (if (`self.IsEnemy`)
      (`KismetSystemLibrary.Delay` 0.15))
    (set `self.IsAttacking` false)
    (set `self.MeleeTarget` null)
    (if (`self.IsEnemy`)
      (set `self.HasAttackTurn` false)
      (set `self.AttackRest` 1.0))))

(event `EnemyWindup`
  (if (and (not (`self.IsDead`)) (not (`self.HitStaggered`)) (not (`self.LungePaused`)) (not (`self.SceneLocked`)))
    (`self.SwordAttack`)))

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
  (if (`self.IsDodging`)
    _
    (elif (`self.IsDead`)
      _
      (elif (> Damage 0.0)
        (`self.FlashOnHit`)
        (if (`self.IsEnemy`)
          (`self.StaggerOnHit`))
        (if (not (`self.IsEnemy`))
          (`PlayerCameraManager.StartCameraShake` (`GameplayStatics.GetPlayerCameraManager` 0) "/Game/OneMoreTake/Blueprints/BP_PlayerHitShake.BP_PlayerHitShake_C" 1.0 "CameraLocal" (struct))))))
  (set `self.Health` (`KismetMathLibrary.FMax` (- (`self.Health`) Damage)))
  (if (and (> Damage 0.0) (> (`self.Health`) 0.0))
    (`self.PlayHitReaction`))
  (if (<= (`self.Health`) 0.0)
    (set `self.IsDead` true)
    (set `self.HitReacting` false)
    (`PrimitiveComponent.SetCollisionEnabled` (`self.BulletHitbox`) "NoCollision")
    (set `self.HasAttackTurn` false)
    (set `self.IsAttacking` false)
    (set `self.IsWindingUp` false)
    (`SceneComponent.SetVisibility` (`self.AttackWarning`) false false)
    (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`))
    (`ActorComponent.Deactivate` (`self.CharacterMovement`))
    (`PrimitiveComponent.SetCollisionEnabled` (`self.CapsuleComponent`) "NoCollision")
    (if (`self.IsEnemy`)
      (`self.DropSwordOnDeath` DamageCauser))
    (if (and (`self.IsEnemy`) (`self.UseEnemyRagdoll`))
      (`self.StartEnemyRagdoll` DamageCauser)
      (elif (`self.IsEnemy`)
        (`SkeletalMeshComponent.PlayAnimation` (`self.Mesh`) "/Game/OneMoreTake/Animations/A_KnightDeath.A_KnightDeath" false)
        (else
          (`SkeletalMeshComponent.PlayAnimation` (`self.Mesh`) "/Game/OneMoreTake/Animations/Retargeted/PlayerDeath/Player_Standing_React_Death_Backward_Anim.Player_Standing_React_Death_Backward_Anim" false))))
    (if (`self.IsEnemy`)
      (set `self.StatusMessage` "CUT! Guard defeated. Press R for another take.")
      (else
        (`self.QueuePlayerWeaponDrop`)
        (set `self.StatusMessage` "Take failed. Resetting...")
        (`KismetSystemLibrary.Delay` 4.083)
        (`self.RestartCurrentTake`)))
    (elif (`self.IsEnemy`)
      _
      (else
        (`self.LaunchCharacter` (* (`KismetMathLibrary.Normal` (- (`self.K2_GetActorLocation`) (`self.K2_GetActorLocation` DamageCauser))) 170.0) true)))))

(event `self.ReceiveTick`
  (params (DeltaSeconds :type "Float (single-precision)"))
  (bind (_asabp_guard_strafe _bsuccess) (cast `/Game/OneMoreTake/Animations/ABP_GuardStrafe` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) :!pure true))
  (if (and (`self.IsEnemy`) (not (`self.IsDead`)) (not (`self.SceneLocked`)))
    (if (or (not (`self.IsAttacking`)) (`self.EnemyAttackInterrupted`))
      (`self.K2_SetActorRotation` (`KismetMathLibrary.FindLookAtRotation` (`self.K2_GetActorLocation`) (`self.K2_GetActorLocation` (`GameplayStatics.GetPlayerCharacter` 0)))))
    (if _bsuccess
      (set `/Game/OneMoreTake/Animations/ABP_GuardStrafe.RifleLocalVelocity` (`KismetMathLibrary.LessLess_VectorRotator` (`self.GetVelocity`) (`self.K2_GetActorRotation`)) _asabp_guard_strafe)))
  (if (`self.HitStaggered`)
    (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`)))
  (if (`self.IsDodging`)
    (`self.TickDodge` DeltaSeconds))
  (if (and (not (`self.IsEnemy`)) (`self.IsAttacking`) (not (`self.IsDead`)) (not (`self.SceneLocked`)))
    (`self.TickMeleeAssist` DeltaSeconds))
  (if (and (`self.HasGun`) (not (`self.IsDead`)) (not (`self.SceneLocked`)))
    (`self.UpdateMouseAim`))
  (if (and (`self.HasGun`) (`self.FireHeld`) (`self.GunReady`) (not (`self.IsDodging`)))
    (`self.FireGun`))
  (if (and (`self.IsEnemy`) (not (`self.SceneLocked`)) (not (`self.IsDead`)))
    (set `self.AttackRest` (`KismetMathLibrary.FMax` (- (`self.AttackRest`) DeltaSeconds)))
    (bind _asbp_knight_player (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` (`GameplayStatics.GetPlayerCharacter` 0)))
    (bind _returnvalue (`KismetMathLibrary.Normal` (- (`self.K2_GetActorLocation` _asbp_knight_player) (`self.K2_GetActorLocation`))))
    (bind _returnvalue_2 (`self.GetDistanceTo` _asbp_knight_player))
    (if (and (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` _asbp_knight_player)) (or (not (`self.IsAttacking`)) (`self.EnemyAttackInterrupted`)) (not (`self.IsWindingUp`)) (not (`self.HitStaggered`)) (not (`self.HitReacting`)))
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
      (if (and (`self.HasAttackTurn`) (not (`self.LungePaused`)) (not (`self.IsAttacking`)))
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
      (if (or (not (`self.HasAttackTurn`)) (`self.LungePaused`) (`self.EnemyAttackInterrupted`))
        (`self.AddMovementInput` (`KismetMathLibrary.MakeVector` (- (.y _returnvalue)) (.x _returnvalue)) (* 0.3 (`self.OrbitDirection`))))
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
  (:`Started`
    (`self.Dodge`))
  (:`Completed`
    (`self.StopJumping` :!label _label)))

(event `self.Touch Jump End`
  (goto _label))

(event `self.Touch Jump Start`
  (`self.Dodge`))

(event `self.ReceiveBeginPlay`
  (if (`self.IsEnemy`)
    (`SkeletalMeshComponent.SetAnimInstanceClass` (`self.Mesh`) "/Game/OneMoreTake/Animations/ABP_GuardStrafe.ABP_GuardStrafe_C")
    (set `CharacterMovementComponent.bOrientRotationToMovement` false (`self.CharacterMovement`))
    (if (`KismetMathLibrary.RandomBool`)
      (set `self.OrbitDirection` 1.0)
      (else
        (set `self.OrbitDirection` -1.0))))
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
  (set `self.GunReady` true)))

(event `ShowGunShot`
 (`GameplayStatics.PlaySound2D` "/Game/OneMoreTake/Audio/S_Gunshot.S_Gunshot" 0.4)
 (if (> (`KismetMathLibrary.VSize` (- (`self.GunShotEnd`) (`self.GunShotStart`))) 1.0)
  (`SceneComponent.K2_SetWorldLocationAndRotation` (`self.GunTracer`) (* (+ (`self.GunShotStart`) (`self.GunShotEnd`)) 0.5) (`KismetMathLibrary.FindLookAtRotation` (`self.GunShotStart`) (`self.GunShotEnd`)) false true)
  (`SceneComponent.SetWorldScale3D` (`self.GunTracer`) (`KismetMathLibrary.MakeVector` (/ (`KismetMathLibrary.VSize` (- (`self.GunShotEnd`) (`self.GunShotStart`))) 100.0) 0.025 0.025))
  (`SceneComponent.SetVisibility` (`self.GunTracer`) true false))
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
      (if (> (`KismetMathLibrary.VSize` (- (`self.MouseAimPoint`) (`self.K2_GetActorLocation`))) 60.0)
      (`self.K2_SetActorRotation` (`KismetMathLibrary.ComposeRotators` (`KismetMathLibrary.FindLookAtRotation` (`self.K2_GetActorLocation`) (`KismetMathLibrary.MakeVector` (.x (`self.MouseAimPoint`)) (.y (`self.MouseAimPoint`)) (.z (`self.K2_GetActorLocation`)))) (struct :`Yaw` 17.1)))))))

(event `FlashOnHit`
  (`MeshComponent.SetOverlayMaterial` (`self.Mesh`) null false 0)
  (for (_ _array_index) (`self.NormalMeshMaterials`)
    (`PrimitiveComponent.SetMaterial` (`self.Mesh`) _array_index "/Game/OneMoreTake/Materials/M_HitFlashWhite.M_HitFlashWhite"))
  (`KismetSystemLibrary.RetriggerableDelay` 0.14)
  (for (_array_element _array_index_2) (`self.NormalMeshMaterials`)
    (`PrimitiveComponent.SetMaterial` (`self.Mesh`) _array_index_2 _array_element)))

(event `Dodge`
  (if (and (`self.DodgeReady`) (not (`self.IsDodging`)) (not (`self.IsAttacking`)) (not (`self.IsDead`)) (not (`self.SceneLocked`)) (not (`self.IsEnemy`)))
    (set `self.DodgeReady` false)
    (set `self.IsDodging` true)
    (set `self.MeleeTarget` null)
    (if (and (> (`KismetMathLibrary.VSize` (`self.GetVelocity`)) 10.0) (> (`KismetMathLibrary.VSize` (`self.GetLastMovementInputVector`)) 0.1))
      (set `self.DodgeDirection` (`KismetMathLibrary.Normal` (`self.GetLastMovementInputVector`)))
      (else
        (set `self.DodgeDirection` (`self.GetActorForwardVector`))))
    (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`))
    (if (not (`self.HasGun`))
      (`AnimInstance.PlaySlotAnimationAsDynamicMontage` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) "/Game/OneMoreTake/Animations/A_KnightDodge.A_KnightDodge" "DefaultSlot" 0.025 0.04 4.5 1 -1.0 0.0))
    (`KismetSystemLibrary.Delay` 0.18)
    (set `self.IsDodging` false)
    (`KismetSystemLibrary.Delay` 0.47)
    (set `self.DodgeReady` true)))

(event `TickDodge`
  (params (DeltaSeconds :type "Float (single-precision)"))
  (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`))
  (`self.K2_SetActorLocation` (+ (`self.K2_GetActorLocation`) (* (`self.DodgeDirection`) (* 1450.0 DeltaSeconds))) true))

(event `FindMeleeTarget`
  (set `self.MeleeTarget` null)
  (set `self.MeleeTargetDistance` 370.0)
  (bind _outactors (`GameplayStatics.GetAllActorsOfClass` "/Game/OneMoreTake/Blueprints/BP_Guard.BP_Guard_C"))
  (for _array_element _outactors
    (bind _asbp_knight_player (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` _array_element))
    (if (and (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` _asbp_knight_player)) (< (`self.GetDistanceTo` _asbp_knight_player) (`self.MeleeTargetDistance`)))
      (if (> (`KismetMathLibrary.Dot_VectorVector` (`self.GetActorForwardVector`) (`KismetMathLibrary.Normal` (- (`self.K2_GetActorLocation` _asbp_knight_player) (`self.K2_GetActorLocation`)))) 0.55)
        (set `self.MeleeTarget` _asbp_knight_player)
        (set `self.MeleeTargetDistance` (`self.GetDistanceTo` _asbp_knight_player)))))
  (if (`KismetSystemLibrary.IsValid` (`self.MeleeTarget`))
    (bind _asbp_knight_player_2 (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` (`self.MeleeTarget`)))
    (`self.PauseForPlayerLunge` _asbp_knight_player_2)))

(event `TickMeleeAssist`
  (params (DeltaSeconds :type "Float (single-precision)"))
  (if (`KismetSystemLibrary.IsValid` (`self.MeleeTarget`))
    (bind _asbp_knight_player (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` (`self.MeleeTarget`)))
    (bind _returnvalue (`self.K2_GetActorLocation` _asbp_knight_player))
    (bind _returnvalue_2 (`KismetMathLibrary.MakeVector` (.x _returnvalue) (.y _returnvalue) (.z (`self.K2_GetActorLocation`))))
    (if (and (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` _asbp_knight_player)) (< (`self.GetDistanceTo` _asbp_knight_player) 450.0))
      (`self.K2_SetActorRotation` (`KismetMathLibrary.FindLookAtRotation` (`self.K2_GetActorLocation`) _returnvalue_2))
      (if (> (`self.GetDistanceTo` _asbp_knight_player) 130.0)
        (`self.K2_SetActorLocation` (`KismetMathLibrary.VInterpTo` (`self.K2_GetActorLocation`) (- _returnvalue_2 (* (`KismetMathLibrary.Normal` (- _returnvalue_2 (`self.K2_GetActorLocation`))) 130.0)) DeltaSeconds 18.0) true))
      (else
        (set `self.MeleeTarget` null)))))

(event `StaggerOnHit`
  (set `self.HitStaggered` true)
  (set `self.EnemyAttackInterrupted` true)
  (set `self.IsWindingUp` false)
  (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`))
  (`SceneComponent.SetVisibility` (`self.AttackWarning`) false false)
  (`AnimInstance.StopSlotAnimation` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) 0.045 "DefaultSlot")
  (`KismetSystemLibrary.RetriggerableDelay` 0.24)
  (set `self.HitStaggered` false))

(event `PlayHitReaction`
  (if (not (`self.IsDead`))
    (set `self.HitReacting` true)
    (set `self.EnemyAttackInterrupted` true)
    (if (== (`self.HitReactionIndex`) 0)
      (set `self.HitReactionAnimation` "/Game/OneMoreTake/Animations/Retargeted/Hits/Knight_Stomach_Hit_Anim.Knight_Stomach_Hit_Anim")
      (elif (== (`self.HitReactionIndex`) 1)
        (set `self.HitReactionAnimation` "/Game/OneMoreTake/Animations/Retargeted/Hits/Knight_Head_Hit_Anim.Knight_Head_Hit_Anim")
        (else
          (set `self.HitReactionAnimation` "/Game/OneMoreTake/Animations/Retargeted/Hits/Knight_Hit_To_Body_Anim.Knight_Hit_To_Body_Anim"))))
    (set `self.HitReactionIndex` (mod (+ (`self.HitReactionIndex`) 1) 3))
    (`AnimInstance.PlaySlotAnimationAsDynamicMontage` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) (`self.HitReactionAnimation`) "DefaultSlot" 0.035 0.1 3.0 1 -1.0 0.0)
    (`KismetSystemLibrary.RetriggerableDelay` 0.36)
    (set `self.HitReacting` false)))

(event `StartEnemyRagdoll`
  (params (HitSource :type "Actor Object Reference"))
  (bind _returnvalue (- (`self.K2_GetActorLocation`) (`self.K2_GetActorLocation` HitSource)))
  (`AnimInstance.StopSlotAnimation` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) 0.0 "DefaultSlot")
  (`PrimitiveComponent.SetCollisionProfileName` (`self.Mesh`) "Ragdoll" true)
  (`PrimitiveComponent.SetCollisionResponseToChannel` (`self.Mesh`) "ECC_Visibility" "ECR_Ignore")
  (`PrimitiveComponent.SetCollisionResponseToChannel` (`self.Mesh`) "ECC_Pawn" "ECR_Ignore")
  (`PrimitiveComponent.SetSimulatePhysics` (`self.Mesh`) true)
  (`PhysicsControlBPLibrary.DisableCollisionBetweenBodyArrays` (`self.Mesh`) (`|MakeArray` "pelvis" "spine_03" "spine_04" "spine_05" "upperarm_l" "lowerarm_l" "hand_l" "lowerarm_r" "hand_r" "foot_r" "thigh_l" "calf_l" "foot_l" "spine_02" "neck_01" "neck_02" "head" "clavicle_r" "clavicle_l" "upperarm_r" "thigh_r" "calf_r" :!type "Name") (`self.Mesh`) (`|MakeArray` "pelvis" "spine_03" "spine_04" "spine_05" "upperarm_l" "lowerarm_l" "hand_l" "lowerarm_r" "hand_r" "foot_r" "thigh_l" "calf_l" "foot_l" "spine_02" "neck_01" "neck_02" "head" "clavicle_r" "clavicle_l" "upperarm_r" "thigh_r" "calf_r" :!type "Name"))
  (`PrimitiveComponent.SetAllPhysicsLinearVelocity` (`self.Mesh`) (0.0 0.0 0.0) false)
  (`PrimitiveComponent.SetAllPhysicsAngularVelocityInDegrees` (`self.Mesh`) (0.0 0.0 0.0) false)
  (`PrimitiveComponent.WakeAllRigidBodies` (`self.Mesh`))
  (if (`KismetSystemLibrary.IsValid` HitSource)
    (`SkeletalMeshComponent.AddImpulseToAllBodiesBelow` (`self.Mesh`) (+ (* (`KismetMathLibrary.Normal` (`KismetMathLibrary.MakeVector` (.x _returnvalue) (.y _returnvalue))) (`self.RagdollPushStrength`)) (`KismetMathLibrary.MakeVector` 0.0 0.0 (`self.RagdollLiftStrength`))) "pelvis" true true)
    (else
      (`SkeletalMeshComponent.AddImpulseToAllBodiesBelow` (`self.Mesh`) (+ (* (`self.GetActorForwardVector`) (- (`self.RagdollPushStrength`))) (`KismetMathLibrary.MakeVector` 0.0 0.0 (`self.RagdollLiftStrength`))) "pelvis" true true))))

(event `DropSwordOnDeath`
  (params (HitSource :type "Actor Object Reference"))
  (bind _returnvalue (- (`self.K2_GetActorLocation`) (`self.K2_GetActorLocation` HitSource)))
  (`SceneComponent.K2_DetachFromComponent` (`self.SwordBlade`) "KeepWorld" "KeepWorld" "KeepWorld" false)
  (`PrimitiveComponent.SetCollisionProfileName` (`self.SwordBlade`) "PhysicsActor" true)
  (`PrimitiveComponent.SetCollisionResponseToChannel` (`self.SwordBlade`) "ECC_Pawn" "ECR_Ignore")
  (`PrimitiveComponent.SetCollisionResponseToChannel` (`self.SwordBlade`) "ECC_PhysicsBody" "ECR_Ignore")
  (`PrimitiveComponent.SetCollisionResponseToChannel` (`self.SwordBlade`) "ECC_Visibility" "ECR_Ignore")
  (`PrimitiveComponent.SetCollisionResponseToChannel` (`self.SwordBlade`) "ECC_Camera" "ECR_Ignore")
  (`PrimitiveComponent.SetSimulatePhysics` (`self.SwordBlade`) true)
  (`PrimitiveComponent.SetLinearDamping` (`self.SwordBlade`) 0.7)
  (`PrimitiveComponent.SetAngularDamping` (`self.SwordBlade`) 1.2)
  (`PrimitiveComponent.WakeAllRigidBodies` (`self.SwordBlade`))
  (`PrimitiveComponent.SetPhysicsAngularVelocityInDegrees` (`self.SwordBlade`) (75.0 180.0 90.0) false "None")
  (if (`KismetSystemLibrary.IsValid` HitSource)
    (`PrimitiveComponent.AddImpulse` (`self.SwordBlade`) (+ (* (`KismetMathLibrary.Normal` (`KismetMathLibrary.MakeVector` (.x _returnvalue) (.y _returnvalue))) (* (`self.RagdollPushStrength`) 0.45)) (`KismetMathLibrary.MakeVector` 0.0 0.0 (* (`self.RagdollLiftStrength`) 0.5))) "None" true)
    (else
      (`PrimitiveComponent.AddImpulse` (`self.SwordBlade`) (0.0 0.0 60.0) "None" true))))

(event `PauseForPlayerLunge`
  (if (and (`self.IsEnemy`) (not (`self.IsDead`)))
    (set `self.LungePaused` true)
    (set `self.EnemyAttackInterrupted` true)
    (set `self.IsWindingUp` false)
    (`SceneComponent.SetVisibility` (`self.AttackWarning`) false false)
    (`AnimInstance.StopSlotAnimation` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) 0.05 "DefaultSlot")
    (`KismetSystemLibrary.RetriggerableDelay` 0.48)
    (set `self.LungePaused` false)))

(event `QueuePlayerWeaponDrop`
  (`KismetSystemLibrary.Delay` (`self.PlayerDeathDropTime`))
  (if (and (`self.IsDead`) (not (`self.IsEnemy`)) (not (`self.PlayerWeaponDropped`)))
    (set `self.PlayerWeaponDropped` true)
    (if (`self.HasGun`)
      (`self.ReleasePlayerWeapon` (`self.GunMesh`))
      (else
        (`self.ReleasePlayerWeapon` (`self.SwordBlade`))))))

(event `ReleasePlayerWeapon`
  (params (Weapon :type "StaticMeshComponent Object Reference"))
  (bind (_origin _boxextent) (`KismetSystemLibrary.GetComponentBounds` Weapon))
  (bind _returnvalue (+ (- (.z (`self.K2_GetActorLocation`)) 90.0) 3.0))
  (bind _returnvalue_2 (- (.z _origin) (.z _boxextent)))
  (`SceneComponent.K2_DetachFromComponent` Weapon "KeepWorld" "KeepWorld" "KeepWorld" false)
  (if (< _returnvalue_2 _returnvalue)
    (`SceneComponent.K2_SetWorldLocation` Weapon (+ (`SceneComponent.K2_GetComponentLocation` Weapon) (`KismetMathLibrary.MakeVector` 0.0 0.0 (- _returnvalue _returnvalue_2))) false true))
  (`PrimitiveComponent.SetCollisionProfileName` Weapon "PhysicsActor" true)
  (`PrimitiveComponent.SetCollisionResponseToChannel` Weapon "ECC_Pawn" "ECR_Ignore")
  (`PrimitiveComponent.SetCollisionResponseToChannel` Weapon "ECC_PhysicsBody" "ECR_Ignore")
  (`PrimitiveComponent.SetCollisionResponseToChannel` Weapon "ECC_Visibility" "ECR_Ignore")
  (`PrimitiveComponent.SetCollisionResponseToChannel` Weapon "ECC_Camera" "ECR_Ignore")
  (`PrimitiveComponent.SetSimulatePhysics` Weapon true)
  (`PrimitiveComponent.SetLinearDamping` Weapon 0.7)
  (`PrimitiveComponent.SetAngularDamping` Weapon 1.2)
  (`PrimitiveComponent.WakeAllRigidBodies` Weapon)
  (`PrimitiveComponent.SetPhysicsLinearVelocity` Weapon (`KismetMathLibrary.GreaterGreater_VectorRotator` (-116.5 -250.85 71.14) (`SceneComponent.K2_GetComponentRotation` (`self.Mesh`))) false "None")
  (`PrimitiveComponent.SetPhysicsAngularVelocityInDegrees` Weapon (70.0 150.0 90.0) false "None"))

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
