(event `SwordAttack`
  (if (and (not (`self.IsAttacking`)) (not (`self.IsDead`)) (not (`self.SceneLocked`)))
    (set `self.IsAttacking` true)
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
      (`KismetSystemLibrary.Delay` 0.48)
      (else
        (`KismetSystemLibrary.Delay` 0.08)))
    (if (and (not (`self.IsDead`)) (not (`self.SceneLocked`)))
      (`AnimInstance.StopSlotAnimation` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) 0.12 "DefaultSlot"))
    (if (`self.IsEnemy`)
      (`KismetSystemLibrary.Delay` 0.4))
    (set `self.IsAttacking` false)))

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
 (:`Pressed` (if (`self.HasGun`) (set `self.FireHeld` true) (`self.FireGun`) (else (`self.SwordAttack`))))
 (:`Released` (set `self.FireHeld` false)))

(event `Key|R`
  (params (Key :type "Key Structure"))
  (:`Pressed`
    (`self.RestartCurrentTake`)))

(event `self.ReceiveAnyDamage`
  (params (Damage :type "Float (single-precision)") (DamageType :type "DamageType Object Reference") (InstigatedBy :type "Controller Object Reference") (DamageCauser :type "Actor Object Reference"))
  (if (not (`self.IsDead`))
    (set `self.Health` (`KismetMathLibrary.FMax` (- (`self.Health`) Damage)))
    (if (<= (`self.Health`) 0.0)
      (set `self.IsDead` true)
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
  (if (and (`self.HasGun`) (`self.FireHeld`) (`self.GunReady`)) (`self.FireGun`))
  (if (and (`self.IsEnemy`) (not (`self.SceneLocked`)) (not (`self.IsDead`)) (not (`self.IsAttacking`)) (not (`self.IsWindingUp`)))
    (bind _asbp_knight_player (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` (`GameplayStatics.GetPlayerCharacter` 0)))
    (if (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` _asbp_knight_player)
      _
      (elif (> (`self.GetDistanceTo` _asbp_knight_player) 160.0)
        (`self.AddMovementInput` (`KismetMathLibrary.Normal` (- (`self.K2_GetActorLocation` _asbp_knight_player) (`self.K2_GetActorLocation`))))
        (else
          (`self.K2_SetActorRotation` (`KismetMathLibrary.FindLookAtRotation` (`self.K2_GetActorLocation`) (`self.K2_GetActorLocation` _asbp_knight_player)))
          (`self.EnemyWindup`))))))

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
    (`self.Jump` :!label _label))
  (:`Completed`
    (`self.StopJumping` :!label _label_2)))

(event `self.Touch Jump Start`
  (goto _label))

(event `self.Touch Jump End`
  (goto _label_2))

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
  (if (and (not (`self.IsDead`)) (not (`self.IsAttacking`)) (not (`self.SceneLocked`)))
    (`self.AddMovementInput` (0.0 1.0 0.0) `X Axis`)
    (`self.AddMovementInput` (1.0 0.0 0.0) `Y Axis`)))

(fn `UserConstructionScript`
  ; Attach the prop to the animated hand, not the character capsule.
  (`SceneComponent.K2_AttachToComponent` (`self.SwordRoot`) (`self.Mesh`) "hand_r" "SnapToTarget" "SnapToTarget" "KeepRelative" false))

(event `self.ReceiveBeginPlay`
 (set `self.GunReady` true)
 (if (== (`GameplayStatics.ParseOption` (`GameModeBase.OptionsString` (`GameplayStatics.GetGameMode`)) "Take") "2")
   (if (not (`self.IsEnemy`)) (`self.EquipGun`))
   (else (if (`self.ExtraTakeTwoGuard`) (`self.K2_DestroyActor`)))))
(event `EquipGun`
 (set `self.HasGun` true)
 (`SceneComponent.SetVisibility` (`self.SwordRoot`) false true)
 (`SceneComponent.K2_AttachToComponent` (`self.GunMesh`) (`self.Mesh`) "hand_r" "SnapToTarget" "SnapToTarget" "KeepRelative" false)
 (`SceneComponent.SetVisibility` (`self.GunMesh`) true false))
(event `RestartCurrentTake`
 (if (`self.HasGun`) (`GameplayStatics.OpenLevel` "L_MovieSet" true "Take=2")
 (else (`GameplayStatics.OpenLevel` "L_MovieSet" true "Take=1"))))
(event `FireGun`
 (if (and (`self.GunReady`) (`self.HasGun`) (not (`self.IsDead`)) (not (`self.SceneLocked`)))
  (set `self.GunTarget` null)
  (set `self.GunTargetDistance` 1500.0)
  (for target (`GameplayStatics.GetAllActorsOfClass` "/Game/OneMoreTake/Blueprints/BP_Guard.BP_Guard_C")
   (bind guard (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` target))
   (if (and (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` guard)) (< (`self.GetDistanceTo` guard) (`self.GunTargetDistance`)))
    (set `self.GunTarget` guard)
    (set `self.GunTargetDistance` (`self.GetDistanceTo` guard))))
  (set `self.GunReady` false)
  (if (`KismetSystemLibrary.IsValid` (`self.GunTarget`))
   (`self.K2_SetActorRotation` (`KismetMathLibrary.FindLookAtRotation` (`self.K2_GetActorLocation`) (`self.K2_GetActorLocation` (`self.GunTarget`))))
   (`GameplayStatics.ApplyDamage` (`self.GunTarget`) 40.0 (`self.GetController`) self)
   (`self.ShowGunShot`)
   (else (`self.ShowGunShot`)))
  (`AnimInstance.PlaySlotAnimationAsDynamicMontage` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) "/Game/OneMoreTake/Animations/A_KnightGunFire.A_KnightGunFire" "DefaultSlot" 0.05 0.1 2.5 1 -1.0 0.0)
  (`KismetSystemLibrary.Delay` 0.25)
  (set `self.GunReady` true)))
(event `ShowGunShot`
 (`GameplayStatics.PlaySound2D` "/Game/OneMoreTake/Audio/S_Gunshot.S_Gunshot" 0.4 1.0)
 (bind start (+ (`self.K2_GetActorLocation`) (0.0 0.0 25.0)))
 (bind end (+ start (* (`self.GetActorForwardVector`) (`self.GunTargetDistance`))))
 (`SceneComponent.K2_SetWorldLocationAndRotation` (`self.GunTracer`) (* (+ start end) 0.5) (`KismetMathLibrary.FindLookAtRotation` start end) false true)
 (`SceneComponent.SetWorldScale3D` (`self.GunTracer`) (`KismetMathLibrary.MakeVector` (/ (`KismetMathLibrary.VSize` (- end start)) 100.0) 0.025 0.025))
 (`SceneComponent.SetVisibility` (`self.GunTracer`) true false)
 (`KismetSystemLibrary.Delay` 0.055)
 (`SceneComponent.SetVisibility` (`self.GunTracer`) false false))


