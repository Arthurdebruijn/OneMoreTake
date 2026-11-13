(event `WakeZombie`
  (if (and (`self.IsWaveZombie`) (== (`self.ZombiePhase`) 0) (not (`self.IsDead`)))
    (set `self.ZombiePhase` 1)
    (set `self.bCanBeDamaged` true)
    (`PrimitiveComponent.SetCollisionEnabled` (`self.BulletHitbox`) "QueryOnly")
    (`PrimitiveComponent.SetCollisionResponseToChannel` (`self.CapsuleComponent`) "ECC_Pawn" "ECR_Block")
    (`self.K2_SetActorRotation` (`KismetMathLibrary.FindLookAtRotation` (`self.K2_GetActorLocation`) (`self.K2_GetActorLocation` (`GameplayStatics.GetPlayerCharacter` 0))))
    (`SkeletalMeshComponent.PlayAnimation` (`self.Mesh`) "/Game/OneMoreTake/Animations/Retargeted/ZombieWaves/ZW_Zombie_Stand_Up_Anim.ZW_Zombie_Stand_Up_Anim" false)
    (`SkeletalMeshComponent.SetPlayRate` (`self.Mesh`) 1.25)
    (`KismetSystemLibrary.Delay` 2.48)
    (if (not (`self.IsDead`))
      (set `self.ZombiePhase` 2)
      (`SkeletalMeshComponent.SetAnimInstanceClass` (`self.Mesh`) "/Game/OneMoreTake/Animations/Retargeted/ZombieWaves/ABP_WaveZombie.ABP_WaveZombie_C")
      (`AnimInstance.PlaySlotAnimationAsDynamicMontage` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) "/Game/OneMoreTake/Animations/Retargeted/ZombieWaves/ZW_Zombie_Scream_Anim.ZW_Zombie_Scream_Anim" "DefaultSlot" 0.08 0.12 1.2 1 -1.0 0.0)
      (`KismetSystemLibrary.Delay` 2.334)
      (if (not (`self.IsDead`))
        (set `self.ZombiePhase` 3)
        (`ActorComponent.Activate` (`self.CharacterMovement`) true)))))

(event `SwordAttack`
  (if (and (not (`self.IsAttacking`)) (not (`self.HitStaggered`)) (not (`self.LungePaused`)) (not (`self.HitReacting`)) (not (`self.IsDodging`)) (not (`self.IsDead`)) (not (`self.SceneLocked`)))
    (set `self.IsAttacking` true)
    (set `self.EnemyAttackInterrupted` false)
    (if (not (`self.IsEnemy`))
      (`self.FindMeleeTarget`))
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
    (if (`self.HasMagic`)
      (set `self.FireHeld` true)
      (`self.CastMagic`)
      (elif (`self.HasGun`)
        (set `self.FireHeld` true)
        (`self.FireGun`)
        (else
          (`self.SwordAttack`)))))
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
        (if (and (`self.IsEnemy`) (or (not (`self.IsWaveZombie`)) (== (`self.ZombiePhase`) 3)))
          (`self.StaggerOnHit`))
        (if (not (`self.IsEnemy`))
          (`PlayerCameraManager.StartCameraShake` (`GameplayStatics.GetPlayerCameraManager` 0) "/Game/OneMoreTake/Blueprints/BP_PlayerHitShake.BP_PlayerHitShake_C" 1.0 "CameraLocal" (struct))))))
  (set `self.Health` (`KismetMathLibrary.FMax` (- (`self.Health`) Damage)))
  (if (and (> Damage 0.0) (> (`self.Health`) 0.0))
    (`self.PlayHitReaction`))
  (if (<= (`self.Health`) 0.0)
    (set `self.IsDead` true)
    (if (`self.IsWaveZombie`)
      (set `self.ZombiePhase` 4))
    (`SceneComponent.SetVisibility` (`self.ZombieLabel`) false false)
    (set `self.HitReacting` false)
    (`PrimitiveComponent.SetCollisionEnabled` (`self.BulletHitbox`) "NoCollision")
    (set `self.HasAttackTurn` false)
    (set `self.IsAttacking` false)
    (set `self.IsWindingUp` false)
    (`SceneComponent.SetVisibility` (`self.AttackWarning`) false false)
    (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`))
    (`ActorComponent.Deactivate` (`self.CharacterMovement`))
    (`PrimitiveComponent.SetCollisionEnabled` (`self.CapsuleComponent`) "NoCollision")
    (if (and (`self.IsEnemy`) (not (`self.IsZombie`)))
      (`self.DropSwordOnDeath` DamageCauser))
    (if (and (`self.IsEnemy`) (`self.UseEnemyRagdoll`))
      (if (`self.IsWaveZombie`)
        (`self.StartWaveZombieRagdoll` DamageCauser)
        (else
          (`self.StartEnemyRagdoll` DamageCauser)))
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
  (bind (_asabp_wave_zombie _bsuccess_2) (cast `/Game/OneMoreTake/Animations/Retargeted/ZombieWaves/ABP_WaveZombie` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) :!pure true))
  (if (and (`self.IsWaveZombie`) (not (`self.IsDead`)))
    (if _bsuccess_2
      (set `/Game/OneMoreTake/Animations/Retargeted/ZombieWaves/ABP_WaveZombie.Speed` (`KismetMathLibrary.VSize` (`self.GetVelocity`)) _asabp_wave_zombie)))
  (if (> (`self.MagicPulseTime`) 0.0)
    (`self.TickMagicPulse` DeltaSeconds))
  (if (and (`self.HasMagic`) (`self.FireHeld`) (`self.MagicReady`))
    (`self.CastMagic`))
  (if (and (`self.IsZombie`) (not (`self.IsDead`)) (not (`self.SceneLocked`)))
    (`self.TickZombie`))
  (if (and (`self.IsEnemy`) (or (not (`self.IsWaveZombie`)) (== (`self.ZombiePhase`) 3)) (not (`self.IsDead`)) (not (`self.SceneLocked`)))
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
  (if (and (or (`self.HasGun`) (`self.HasMagic`)) (not (`self.IsDead`)) (not (`self.SceneLocked`)))
    (`self.UpdateMouseAim`))
  (if (and (`self.HasGun`) (`self.FireHeld`) (`self.GunReady`) (not (`self.IsDodging`)))
    (`self.FireGun`))
  (if (and (`self.IsEnemy`) (not (`self.IsZombie`)) (not (`self.SceneLocked`)) (not (`self.IsDead`)))
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
  (set `self.DodgeReady` true)
  (set `self.GunReady` true)
  (set `self.MagicReady` true)
  (set `self.NormalMeshMaterials` (`MeshComponent.GetMaterials` (`self.Mesh`)))
  (if (not (`self.IsEnemy`))
    (`PrimitiveComponent.SetCollisionEnabled` (`self.BulletHitbox`) "NoCollision"))
  (if (`self.IsEnemy`)
    (`SkeletalMeshComponent.SetAnimInstanceClass` (`self.Mesh`) "/Game/OneMoreTake/Animations/ABP_GuardStrafe.ABP_GuardStrafe_C")
    (set `CharacterMovementComponent.bOrientRotationToMovement` false (`self.CharacterMovement`))
    (if (`KismetMathLibrary.RandomBool`)
      (set `self.OrbitDirection` 1.0)
      (else
        (set `self.OrbitDirection` -1.0))))
  (if (== (`GameplayStatics.ParseOption` (`GameModeBase.OptionsString` (`GameplayStatics.GetGameMode`)) "Take") "3")
    (if (`self.IsWaveZombie`)
      (`self.InitializeWaveZombie`)
      (elif (`self.IsEnemy`)
        (`self.K2_DestroyActor`)
        (else
          (`self.EquipGun`))))
    (elif (`self.IsWaveZombie`)
      (`self.K2_DestroyActor`)
      (elif (== (`GameplayStatics.ParseOption` (`GameModeBase.OptionsString` (`GameplayStatics.GetGameMode`)) "Take") "2")
        (if (not (`self.IsEnemy`))
          (`self.EquipGun`))
        (elif (`self.ExtraTakeTwoGuard`)
          (`self.K2_DestroyActor`))))))

(event `EquipGun`
  (bind _returnvalue (`GameplayStatics.GetPlayerController` 0))
  (set `self.HasMagic` false)
  (set `self.HasGun` true)
  (`SkeletalMeshComponent.SetAnimInstanceClass` (`self.Mesh`) "/Game/OneMoreTake/Animations/ABP_KnightRifle.ABP_KnightRifle_C")
  (set `CharacterMovementComponent.bOrientRotationToMovement` false (`self.CharacterMovement`))
  (set `PlayerController.bShowMouseCursor` true _returnvalue)
  (`WidgetBlueprintLibrary.SetInputMode_GameAndUIEx` _returnvalue null "LockAlways" false)
  (`SceneComponent.SetVisibility` (`self.SwordRoot`) false true)
  (`SceneComponent.K2_AttachToComponent` (`self.GunMesh`) (`self.Mesh`) "hand_r" "SnapToTarget" "KeepRelative" "KeepRelative" false)
  (`SceneComponent.SetVisibility` (`self.GunMesh`) true false))

(event `RestartCurrentTake`
  (if (== (`GameplayStatics.ParseOption` (`GameModeBase.OptionsString` (`GameplayStatics.GetGameMode`)) "Take") "3")
    (`GameplayStatics.OpenLevel` "L_MovieSet" true "Take=3")
    (elif (`self.HasGun`)
      (`GameplayStatics.OpenLevel` "L_MovieSet" true "Take=2")
      (else
        (`GameplayStatics.OpenLevel` "L_MovieSet" true "Take=1")))))

(event `FireGun`
  (bind _returnvalue (`KismetMathLibrary.MakeVector` (- (.x (`self.MouseAimPoint`)) (.x (`self.K2_GetActorLocation`))) (- (.y (`self.MouseAimPoint`)) (.y (`self.K2_GetActorLocation`)))))
  (bind _returnvalue_2 (`KismetMathLibrary.VSize` _returnvalue))
  (bind _returnvalue_3 (`SceneComponent.GetForwardVector` (`self.GunMesh`)))
  (bind _returnvalue_4 (+ (`self.K2_GetActorLocation`) (* (`self.GunShotDirection`) (`KismetMathLibrary.FMax` _returnvalue_2 180.0))))
  (if (and (`self.GunReady`) (`self.HasGun`) (`self.MouseAimValid`) (not (`self.IsDodging`)) (not (`self.IsDead`)) (not (`self.SceneLocked`)))
    (`self.UpdateMouseAim`)
    (set `self.GunReady` false)
    (set `self.GunShotStart` (`SceneComponent.K2_GetComponentLocation` (`self.GunMuzzle`)))
    (set `self.GunShotDirection` (`KismetMathLibrary.Normal` (`KismetMathLibrary.MakeVector` (.x _returnvalue_3) (.y _returnvalue_3))))
    (if (> _returnvalue_2 60.0)
      (set `self.GunShotDirection` (`KismetMathLibrary.Normal` _returnvalue)))
    (set `self.GunShotDirection` (`KismetMathLibrary.Normal` (- (`KismetMathLibrary.MakeVector` (.x _returnvalue_4) (.y _returnvalue_4) (`KismetMathLibrary.SelectFloat` (.z (`self.MouseAimPoint`)) (.z (`self.GunShotStart`)) (> _returnvalue_2 180.0))) (`self.GunShotStart`))))
    (set `self.GunShotEnd` (+ (`self.GunShotStart`) (* (`self.GunShotDirection`) 1800.0)))
    (bind (_outhit _returnvalue_5) (`KismetSystemLibrary.SphereTraceSingle` (`self.GunShotStart`) (`self.GunShotEnd`) 14.0 "TraceTypeQuery1" false (`|MakeArray` self :!type "Actor Object Reference")))
    (bind (_bblockinghit _binitialoverlap _time _distance _location _impactpoint _normal _impactnormal _physmat _hitactor) (`GameplayStatics.BreakHitResult` _outhit))
    (bind (_asbp_knight_player _bsuccess) (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` _hitactor :!pure true))
    (if _returnvalue_5
      (set `self.GunShotEnd` (+ (`self.GunShotStart`) (* (`self.GunShotDirection`) _distance)))
      (if _bsuccess
        (if (and (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsEnemy` _asbp_knight_player) (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` _asbp_knight_player)))
          (`GameplayStatics.ApplyDamage` _asbp_knight_player 40.0 (`self.GetController`) self))))
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
  (bind (_asabp_knight_rifle _bsuccess) (cast `/Game/OneMoreTake/Animations/ABP_KnightRifle` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) :!pure true))
  (bind (_asabp_player_magic _bsuccess_2) (cast `/Game/OneMoreTake/Animations/ABP_PlayerMagic` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) :!pure true))
  (bind (_asbp_knight_player _bsuccess_3) (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` _hitactor :!pure true))
  (if _bsuccess
    (set `/Game/OneMoreTake/Animations/ABP_KnightRifle.RifleLocalVelocity` (`KismetMathLibrary.LessLess_VectorRotator` (`self.GetVelocity`) (`self.K2_GetActorRotation`)) _asabp_knight_rifle))
  (if _bsuccess_2
    (set `/Game/OneMoreTake/Animations/ABP_PlayerMagic.RifleLocalVelocity` (`KismetMathLibrary.LessLess_VectorRotator` (`self.GetVelocity`) (`self.K2_GetActorRotation`)) _asabp_player_magic))
  (set `self.MouseAimValid` false)
  (if _returnvalue_2
    (if _returnvalue_3
      (set `self.MouseAimValid` true)
      (set `self.MouseAimPoint` (+ _intersection (0.0 0.0 90.0)))
      (if _returnvalue_4
        (if _bsuccess_3
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
  (if (and (not (`self.IsDead`)) (or (not (`self.IsWaveZombie`)) (== (`self.ZombiePhase`) 3)))
    (set `self.HitReacting` true)
    (set `self.EnemyAttackInterrupted` true)
    (if (`self.IsWaveZombie`)
      (set `self.HitReactionAnimation` "/Game/OneMoreTake/Animations/Retargeted/ZombieWaves/ZW_Zombie_Reaction_Hit_Anim.ZW_Zombie_Reaction_Hit_Anim")
      (elif (== (`self.HitReactionIndex`) 0)
        (set `self.HitReactionAnimation` "/Game/OneMoreTake/Animations/Retargeted/Hits/Knight_Stomach_Hit_Anim.Knight_Stomach_Hit_Anim")
        (elif (== (`self.HitReactionIndex`) 1)
          (set `self.HitReactionAnimation` "/Game/OneMoreTake/Animations/Retargeted/Hits/Knight_Head_Hit_Anim.Knight_Head_Hit_Anim")
          (else
            (set `self.HitReactionAnimation` "/Game/OneMoreTake/Animations/Retargeted/Hits/Knight_Hit_To_Body_Anim.Knight_Hit_To_Body_Anim")))))
    (set `self.HitReactionIndex` (mod (+ (`self.HitReactionIndex`) 1) 3))
    (`AnimInstance.PlaySlotAnimationAsDynamicMontage` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) (`self.HitReactionAnimation`) "DefaultSlot" 0.035 0.1 (`KismetMathLibrary.SelectFloat` 4.0 3.0 (`self.IsWaveZombie`)) 1 -1.0 0.0)
    (`KismetSystemLibrary.RetriggerableDelay` (`KismetMathLibrary.SelectFloat` 0.55 0.36 (`self.IsWaveZombie`)))
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
    (if (`self.HasMagic`)
      (`SceneComponent.SetVisibility` (`self.MagicOrb`) false false)
      (elif (`self.HasGun`)
        (`self.ReleasePlayerWeapon` (`self.GunMesh`))
        (else
          (`self.ReleasePlayerWeapon` (`self.SwordBlade`)))))))

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

(event `EquipMagic`
  (bind _returnvalue (`GameplayStatics.GetPlayerController` 0))
  (set `self.HasMagic` true)
  (set `self.HasGun` false)
  (set `self.MagicReady` true)
  (`SkeletalMeshComponent.SetAnimInstanceClass` (`self.Mesh`) "/Game/OneMoreTake/Animations/ABP_PlayerMagic.ABP_PlayerMagic_C")
  (set `CharacterMovementComponent.bOrientRotationToMovement` false (`self.CharacterMovement`))
  (set `CharacterMovementComponent.MaxWalkSpeed` 300.0 (`self.CharacterMovement`))
  (set `PlayerController.bShowMouseCursor` true _returnvalue)
  (`WidgetBlueprintLibrary.SetInputMode_GameAndUIEx` _returnvalue null "LockAlways" false)
  (`SceneComponent.SetVisibility` (`self.SwordRoot`) false true)
  (`SceneComponent.SetVisibility` (`self.GunMesh`) false false)
  (`SceneComponent.K2_AttachToComponent` (`self.MagicOrb`) (`self.Mesh`) "hand_r" "SnapToTarget" "SnapToTarget" "KeepRelative" false)
  (`SceneComponent.SetVisibility` (`self.MagicOrb`) true false)
  (`PrimitiveComponent.SetMaterial` (`self.GunTracer`) 0 "/Game/OneMoreTake/Materials/M_ArcaneCyan.M_ArcaneCyan"))

(event `BecomeZombie`
  (set `self.IsZombie` true)
  (set `self.AttackDamage` 12.0)
  (set `self.AttackReach` 175.0)
  (set `self.AttackPlayRate` 0.95)
  (set `self.AttackAnimationA` "/Game/OneMoreTake/Animations/A_UndeadSwipe1.A_UndeadSwipe1")
  (set `self.AttackAnimationB` "/Game/OneMoreTake/Animations/A_UndeadSwipe2.A_UndeadSwipe2")
  (set `CharacterMovementComponent.MaxWalkSpeed` 160.0 (`self.CharacterMovement`))
  (`SceneComponent.SetVisibility` (`self.SwordRoot`) false true)
  (`SceneComponent.SetVisibility` (`self.ZombieLabel`) true false)
  (for (_ _array_index) (`MeshComponent.GetMaterials` (`self.Mesh`))
    (if (== _array_index 0)
      (`PrimitiveComponent.SetMaterial` (`self.Mesh`) _array_index "/Game/OneMoreTake/Materials/M_UndeadFlesh.M_UndeadFlesh")
      (else
        (`PrimitiveComponent.SetMaterial` (`self.Mesh`) _array_index "/Game/OneMoreTake/Materials/M_UndeadArmor.M_UndeadArmor"))))
  (set `self.NormalMeshMaterials` (`MeshComponent.GetMaterials` (`self.Mesh`))))

(event `TickZombie`
  (if (and (`self.IsWaveZombie`) (== (`self.ZombiePhase`) 3) (not (`self.HitStaggered`)) (not (`self.HitReacting`)))
    (set `self.AttackRest` (`KismetMathLibrary.FMax` (- (`self.AttackRest`) (`GameplayStatics.GetWorldDeltaSeconds`))))
    (bind _asbp_knight_player (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` (`GameplayStatics.GetPlayerCharacter` 0)))
    (if (and (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` _asbp_knight_player)) (or (not (`self.IsAttacking`)) (`self.EnemyAttackInterrupted`)))
      (if (> (`self.GetDistanceTo` _asbp_knight_player) 170.0)
        (`self.AddMovementInput` (`KismetMathLibrary.Normal` (- (`self.K2_GetActorLocation` _asbp_knight_player) (`self.K2_GetActorLocation`))))
        (elif (and (not (`self.IsAttacking`)) (<= (`self.AttackRest`) 0.0))
          (`self.WaveZombieAttack`))))))

(event `CastMagic`
  (bind _returnvalue (`KismetMathLibrary.MakeVector` (- (.x (`self.MouseAimPoint`)) (.x (`self.K2_GetActorLocation`))) (- (.y (`self.MouseAimPoint`)) (.y (`self.K2_GetActorLocation`)))))
  (if (and (`self.HasMagic`) (`self.MagicReady`) (`self.MouseAimValid`) (not (`self.IsDead`)) (not (`self.SceneLocked`)) (not (`self.IsDodging`)) (not (`self.HitReacting`)))
    (`self.UpdateMouseAim`)
    (set `self.MagicReady` false)
    (set `self.MagicImpactPoint` (+ (`self.K2_GetActorLocation`) (* (`KismetMathLibrary.Normal` _returnvalue) (`KismetMathLibrary.FMin` (`KismetMathLibrary.VSize` _returnvalue) 1400.0))))
    (bind _outactors (`GameplayStatics.GetAllActorsOfClass` "/Game/OneMoreTake/Blueprints/BP_Guard.BP_Guard_C"))
    (for _array_element _outactors
      (bind _asbp_knight_player (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` _array_element))
      (if (and (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` _asbp_knight_player)) (<= (`KismetMathLibrary.VSize` (- (`self.K2_GetActorLocation` _asbp_knight_player) (`self.MagicImpactPoint`))) (`self.MagicRadius`)))
        (`GameplayStatics.ApplyDamage` _asbp_knight_player (`self.MagicDamage`) (`self.GetController`) self)))
    (set `self.GunShotStart` (`SceneComponent.K2_GetComponentLocation` (`self.MagicOrb`)))
    (set `self.GunShotEnd` (+ (`self.MagicImpactPoint`) (0.0 0.0 25.0)))
    (set `self.MagicPulseTime` 0.3)
    (`SceneComponent.K2_SetWorldLocation` (`self.MagicRing`) (`KismetMathLibrary.MakeVector` (.x (`self.MagicImpactPoint`)) (.y (`self.MagicImpactPoint`)) (+ (- (.z (`self.K2_GetActorLocation`)) 90.0) 4.0)) false true)
    (`SceneComponent.SetVisibility` (`self.MagicRing`) true false)
    (`self.ShowMagicBeam`)
    (`AnimInstance.PlaySlotAnimationAsDynamicMontage` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) "/Game/OneMoreTake/Animations/A_UndeadSwipe1.A_UndeadSwipe1" "DefaultSlot" 0.04 0.1 2.5 1 -1.0 0.0)
    (`KismetSystemLibrary.Delay` 0.65)
    (set `self.MagicReady` true)))

(event `ShowMagicBeam`
  (`GameplayStatics.PlaySound2D` "/Game/OneMoreTake/Audio/S_ArcaneBlast.S_ArcaneBlast" 0.4)
  (if (> (`KismetMathLibrary.VSize` (- (`self.GunShotEnd`) (`self.GunShotStart`))) 160.0)
    (`SceneComponent.K2_SetWorldLocationAndRotation` (`self.GunTracer`) (* (+ (`self.GunShotStart`) (`self.GunShotEnd`)) 0.5) (`KismetMathLibrary.FindLookAtRotation` (`self.GunShotStart`) (`self.GunShotEnd`)) false true)
    (`SceneComponent.SetWorldScale3D` (`self.GunTracer`) (`KismetMathLibrary.MakeVector` (/ (`KismetMathLibrary.VSize` (- (`self.GunShotEnd`) (`self.GunShotStart`))) 100.0) 0.065 0.065))
    (`SceneComponent.SetVisibility` (`self.GunTracer`) true false))
  (`KismetSystemLibrary.Delay` 0.09)
  (`SceneComponent.SetVisibility` (`self.GunTracer`) false false))

(event `TickMagicPulse`
  (params (DeltaSeconds :type "Float (single-precision)"))
  (bind _returnvalue (* (/ (`self.MagicRadius`) 50.0) (- 1.0 (/ (`self.MagicPulseTime`) 0.3))))
  (set `self.MagicPulseTime` (`KismetMathLibrary.FMax` (- (`self.MagicPulseTime`) DeltaSeconds)))
  (`SceneComponent.SetWorldScale3D` (`self.MagicRing`) (`KismetMathLibrary.MakeVector` _returnvalue _returnvalue 1.0))
  (if (<= (`self.MagicPulseTime`) 0.0)
    (`SceneComponent.SetVisibility` (`self.MagicRing`) false false)))

(event `InitializeWaveZombie`
  (set `self.IsZombie` true)
  (set `self.ZombiePhase` 0)
  (set `self.UseEnemyRagdoll` true)
  (set `self.bCanBeDamaged` false)
  (set `self.AttackDamage` 15.0)
  (set `self.AttackReach` 185.0)
  (`SkeletalMeshComponent.SetSkeletalMeshAsset` (`self.Mesh`) "/Game/Characters/Zombie/StylizedZombie/Textures/SZombie_Variant_1/SK_SZombie_Variant_1.SK_SZombie_Variant_1")
  (`PrimitiveComponent.SetMaterial` (`self.Mesh`) 0 "/Game/Characters/Zombie/StylizedZombie/Textures/SZombie_Variant_1/SZombie_Variant_1.SZombie_Variant_1")
  (set `self.NormalMeshMaterials` (`MeshComponent.GetMaterials` (`self.Mesh`)))
  (`SceneComponent.SetVisibility` (`self.SwordRoot`) false true)
  (`SceneComponent.SetVisibility` (`self.GunMesh`) false false)
  (`SceneComponent.SetVisibility` (`self.ZombieLabel`) false false)
  (`SceneComponent.SetVisibility` (`self.MagicOrb`) false false)
  (`PrimitiveComponent.SetCollisionEnabled` (`self.BulletHitbox`) "NoCollision")
  (`PrimitiveComponent.SetCollisionResponseToChannel` (`self.CapsuleComponent`) "ECC_Pawn" "ECR_Ignore")
  (`PrimitiveComponent.SetCollisionResponseToChannel` (`self.CapsuleComponent`) "ECC_Visibility" "ECR_Ignore")
  (`ActorComponent.Deactivate` (`self.CharacterMovement`))
  (set `CharacterMovementComponent.MaxWalkSpeed` (+ 220.0 (* (`self.ZombieWaveIndex`) 20.0)) (`self.CharacterMovement`))
  (`SkeletalMeshComponent.PlayAnimation` (`self.Mesh`) "/Game/OneMoreTake/Animations/Retargeted/ZombieWaves/ZW_Zombie_Stand_Up_Anim.ZW_Zombie_Stand_Up_Anim" false)
  (`SkeletalMeshComponent.SetPosition` (`self.Mesh`) 0.0 false)
  (`SkeletalMeshComponent.SetPlayRate` (`self.Mesh`) 0.0))

(event `WaveZombieAttack`
  (bind _returnvalue (`GameplayStatics.GetPlayerCharacter` 0))
  (if (and (== (`self.ZombiePhase`) 3) (not (`self.IsDead`)) (not (`self.IsAttacking`)) (not (`self.HitReacting`)) (not (`self.SceneLocked`)))
    (set `self.IsAttacking` true)
    (set `self.EnemyAttackInterrupted` false)
    (if (`self.UseSecondAttack`)
      (set `self.AttackAnimation` "/Game/OneMoreTake/Animations/Retargeted/ZombieWaves/ZW_Zombie_Kicking_Anim.ZW_Zombie_Kicking_Anim")
      (set `self.AttackPlayRate` 1.6)
      (set `self.AttackImpactTime` 0.542)
      (set `self.LastAttackVariant` 2)
      (else
        (set `self.AttackAnimation` "/Game/OneMoreTake/Animations/Retargeted/ZombieWaves/ZW_Zombie_Punching_Anim.ZW_Zombie_Punching_Anim")
        (set `self.AttackPlayRate` 1.8)
        (set `self.AttackImpactTime` 0.704)
        (set `self.LastAttackVariant` 1)))
    (set `self.UseSecondAttack` (not (`self.UseSecondAttack`)))
    (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`))
    (`self.K2_SetActorRotation` (`KismetMathLibrary.FindLookAtRotation` (`self.K2_GetActorLocation`) (`self.K2_GetActorLocation` (`GameplayStatics.GetPlayerCharacter` 0))))
    (`AnimInstance.PlaySlotAnimationAsDynamicMontage` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) (`self.AttackAnimation`) "DefaultSlot" 0.07 0.12 (`self.AttackPlayRate`) 1 -1.0 0.0)
    (`KismetSystemLibrary.Delay` (`self.AttackImpactTime`))
    (if (and (not (`self.IsDead`)) (not (`self.EnemyAttackInterrupted`)) (not (`self.HitStaggered`)) (not (`self.SceneLocked`)))
      (if (and (<= (`self.GetDistanceTo` _returnvalue) (`self.AttackReach`)) (> (`KismetMathLibrary.Dot_VectorVector` (`self.GetActorForwardVector`) (`KismetMathLibrary.Normal` (- (`self.K2_GetActorLocation` _returnvalue) (`self.K2_GetActorLocation`)))) 0.2))
        (`GameplayStatics.ApplyDamage` _returnvalue (`self.AttackDamage`) (`self.GetController`) self)))
    (`KismetSystemLibrary.Delay` 0.35)
    (if (and (not (`self.IsDead`)) (not (`self.HitReacting`)))
      (`AnimInstance.StopSlotAnimation` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) 0.12 "DefaultSlot"))
    (set `self.IsAttacking` false)
    (set `self.AttackRest` 0.2)))

(event `StartWaveZombieRagdoll`
  (params (HitSource :type "Actor Object Reference"))
  (bind _array (`|MakeArray` "CC_Base_Hip" "CC_Base_L_Foot" "CC_Base_L_CalfTwist01" "CC_Base_L_ThighTwist01" "CC_Base_R_ThighTwist01" "CC_Base_R_Foot" "CC_Base_R_CalfTwist01" "CC_Base_Waist" "CC_Base_Spine02" "CC_Base_Head" "CC_Base_L_Upperarm" "CC_Base_L_Hand" "CC_Base_R_Upperarm" "CC_Base_R_Hand" :!type "Name"))
  (bind _returnvalue (- (`self.K2_GetActorLocation`) (`self.K2_GetActorLocation` HitSource)))
  (set `self.ZombiePhase` 4)
  (`AnimInstance.StopSlotAnimation` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) 0.0 "DefaultSlot")
  (`PrimitiveComponent.SetCollisionProfileName` (`self.Mesh`) "Ragdoll" true)
  (`PrimitiveComponent.SetCollisionResponseToChannel` (`self.Mesh`) "ECC_Visibility" "ECR_Ignore")
  (`PrimitiveComponent.SetCollisionResponseToChannel` (`self.Mesh`) "ECC_Pawn" "ECR_Ignore")
  (`PrimitiveComponent.SetSimulatePhysics` (`self.Mesh`) true)
  (`PhysicsControlBPLibrary.DisableCollisionBetweenBodyArrays` (`self.Mesh`) _array (`self.Mesh`) _array)
  (`PrimitiveComponent.SetAllPhysicsLinearVelocity` (`self.Mesh`) (0.0 0.0 0.0) false)
  (`PrimitiveComponent.SetAllPhysicsAngularVelocityInDegrees` (`self.Mesh`) (0.0 0.0 0.0) false)
  (if (`KismetSystemLibrary.IsValid` HitSource)
    (`SkeletalMeshComponent.AddImpulseToAllBodiesBelow` (`self.Mesh`) (+ (* (`KismetMathLibrary.Normal` (`KismetMathLibrary.MakeVector` (.x _returnvalue) (.y _returnvalue))) (`self.RagdollPushStrength`)) (`KismetMathLibrary.MakeVector` 0.0 0.0 (`self.RagdollLiftStrength`))) "CC_Base_Hip" true true)))

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
  (`SceneComponent.K2_AttachToComponent` (`self.MagicOrb`) (`self.Mesh`) "hand_r" "SnapToTarget" "SnapToTarget" "KeepRelative" false)
  (`SceneComponent.K2_AttachToComponent` (`self.GunMesh`) (`self.Mesh`) "hand_r" "SnapToTarget" "KeepRelative" "KeepRelative" false)
  ; Attach the prop to the animated hand, not the character capsule.
  (`SceneComponent.K2_AttachToComponent` (`self.SwordRoot`) (`self.Mesh`) "hand_r" "SnapToTarget" "SnapToTarget" "KeepRelative" false))

