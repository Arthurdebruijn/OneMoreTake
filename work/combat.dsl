(fn `UserConstructionScript`
  ; Attach the prop to the animated hand, not the character capsule.
  (`SceneComponent.K2_AttachToComponent` (`self.SwordRoot`) (`self.Mesh`) "hand_r" "SnapToTarget" "SnapToTarget" "KeepRelative" false))

(fn `Move`
  (params (`X Axis` :type "Float (double-precision)") (`Y Axis` :type "Float (double-precision)"))
  ; Commit to a strike; movement resumes during recovery.
  (if (and (not (`self.IsDead`)) (not (`self.IsAttacking`)))
    (`self.AddMovementInput` (0 1 0) `X Axis`)
    (`self.AddMovementInput` (1 0 0) `Y Axis`)))

(event `Key|LeftMouseButton`
  (:`Pressed`
    (`self.SwordAttack`)))

(event `Key|R`
  (:`Pressed`
    (`GameplayStatics.OpenLevel` "L_MovieSet" true "")))

(event `SwordAttack`
  ; Single impact check per animation prevents repeat damage on one swing.
  (if (and (not (`self.IsAttacking`)) (not (`self.IsDead`)))
    (set `self.IsAttacking` true)
    (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`))
    (`SkeletalMeshComponent.PlayAnimation` (`self.Mesh`) "/Game/OneMoreTake/Animations/A_SwordStrike.A_SwordStrike" false)
    (`KismetSystemLibrary.Delay` 0.32)
    (if (not (`self.IsDead`))
      (`self.DealSwordDamage`))
    (`KismetSystemLibrary.Delay` 0.48)
    (if (not (`self.IsDead`))
      (`SkeletalMeshComponent.SetAnimationMode` (`self.Mesh`) "AnimationBlueprint" true))
    (`KismetSystemLibrary.Delay` 0.15)
    (set `self.IsAttacking` false)))

(fn `DealSwordDamage`
  (bind opponents (`GameplayStatics.GetAllActorsOfClass` "/Game/OneMoreTake/Blueprints/BP_KnightPlayer.BP_KnightPlayer_C"))
  (for actor opponents
    (bind target (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` actor))
    (if (and (!= (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsEnemy` target) (`self.IsEnemy`)) (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` target)) (<= (`self.GetDistanceTo` target) (`self.AttackReach`)))
      (bind direction (`KismetMathLibrary.Normal` (- (`Actor.K2_GetActorLocation` target) (`self.K2_GetActorLocation`)) 0.0001))
      (if (> (`KismetMathLibrary.Dot_VectorVector` (`self.GetActorForwardVector`) direction) 0.2)
        (`GameplayStatics.ApplyDamage` target (`self.AttackDamage`) (`self.GetController`) self null)))))

(event `self.ReceiveAnyDamage`
  (params (Damage :type "Float (single-precision)") (DamageType :type "DamageType Object Reference") (InstigatedBy :type "Controller Object Reference") (DamageCauser :type "Actor Object Reference"))
  (if (not (`self.IsDead`))
    (set `self.Health` (`KismetMathLibrary.FMax` (- (`self.Health`) Damage) 0.0))
    (if (<= (`self.Health`) 0.0)
      ; Death cancels delayed attacks and stops the enemy's chase.
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
          (`GameplayStatics.OpenLevel` "L_MovieSet" true "")))
      (else
        ; Small physical recoil makes successful hits readable.
        (bind recoil (* (`KismetMathLibrary.Normal` (- (`self.K2_GetActorLocation`) (`Actor.K2_GetActorLocation` DamageCauser)) 0.0001) 170.0))
        (`self.LaunchCharacter` recoil true false)))))

(event `self.ReceiveTick`
  (params (DeltaSeconds :type "Float (single-precision)"))
  (if (and (`self.IsEnemy`) (not (`self.IsDead`)) (not (`self.IsAttacking`)) (not (`self.IsWindingUp`)))
    (bind player (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` (`GameplayStatics.GetPlayerCharacter` 0)))
    (if (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` player))
      (if (> (`self.GetDistanceTo` player) 160.0)
        (bind toward (`KismetMathLibrary.Normal` (- (`Actor.K2_GetActorLocation` player) (`self.K2_GetActorLocation`)) 0.0001))
        (`self.AddMovementInput` toward 1.0)
        (else
          (`self.K2_SetActorRotation` (`KismetMathLibrary.FindLookAtRotation` (`self.K2_GetActorLocation`) (`Actor.K2_GetActorLocation` player)) false)
          (`self.EnemyWindup`))))))

(event `EnemyWindup`
  ; The enemy locks its direction before the warning so stepping aside works.
  (if (and (not (`self.IsDead`)) (not (`self.IsWindingUp`)))
    (set `self.IsWindingUp` true)
    (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`))
    (`SceneComponent.SetVisibility` (`self.AttackWarning`) true false)
    (`KismetSystemLibrary.Delay` 0.55)
    (`SceneComponent.SetVisibility` (`self.AttackWarning`) false false)
    (set `self.IsWindingUp` false)
    (if (not (`self.IsDead`))
      (`self.SwordAttack`))))


