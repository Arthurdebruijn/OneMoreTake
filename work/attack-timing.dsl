(event `SwordAttack`
  (if (and (not (`self.IsAttacking`)) (not (`self.IsDead`)) (not (`self.SceneLocked`)))
    (set `self.IsAttacking` true)
    (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`))
    (`SkeletalMeshComponent.PlayAnimation` (`self.Mesh`) (`self.AttackAnimation`) false)
    (`KismetSystemLibrary.Delay` (`self.AttackImpactTime`))
    (if (and (not (`self.IsDead`)) (not (`self.SceneLocked`)))
      (`self.DealSwordDamage`))
    ; Player gets movement back shortly after impact; enemy stays committed.
    (if (`self.IsEnemy`)
      (`KismetSystemLibrary.Delay` 0.48)
      (else (`KismetSystemLibrary.Delay` 0.08)))
    (if (and (not (`self.IsDead`)) (not (`self.SceneLocked`)))
      (`SkeletalMeshComponent.SetAnimationMode` (`self.Mesh`) "AnimationBlueprint" true))
    (if (`self.IsEnemy`)
      (`KismetSystemLibrary.Delay` 0.4))
    (set `self.IsAttacking` false)))

(event `EnemyWindup`
  ; Lock facing before the longer telegraph; do not track the player's dodge.
  (if (and (not (`self.IsDead`)) (not (`self.IsWindingUp`)) (not (`self.SceneLocked`)))
    (set `self.IsWindingUp` true)
    (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`))
    (`SceneComponent.SetVisibility` (`self.AttackWarning`) true false)
    (`KismetSystemLibrary.Delay` (`self.EnemyChargeTime`))
    (`SceneComponent.SetVisibility` (`self.AttackWarning`) false false)
    (set `self.IsWindingUp` false)
    (if (and (not (`self.IsDead`)) (not (`self.SceneLocked`)))
      (`self.SwordAttack`))))

(fn `Move`
  (params (`X Axis` :type "Float (double-precision)") (`Y Axis` :type "Float (double-precision)"))
  (if (and (not (`self.IsDead`)) (not (`self.IsAttacking`)) (not (`self.SceneLocked`)))
    (`self.AddMovementInput` (0 1 0) `X Axis`)
    (`self.AddMovementInput` (1 0 0) `Y Axis`)))

(event `LockForCut`
  (set `self.SceneLocked` true)
  (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`)))
