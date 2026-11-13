import pathlib,json
exec(pathlib.Path('work/build_take2_dsl.py').read_text().split("parse='",1)[0])
s=json.loads(pathlib.Path('work/stagger-before.json').read_text(encoding='utf-8-sig'))['returnValue']['dsl']
s=replace_form(s,'(event `EnemyWindup`','''(event `EnemyWindup`
 (if (and (not (`self.IsDead`)) (not (`self.HitStaggered`)) (not (`self.SceneLocked`)))
  (`self.SwordAttack`)))''')
s=s.replace('(not (`self.IsAttacking`)) (not (`self.IsDodging`))','(not (`self.IsAttacking`)) (not (`self.HitStaggered`)) (not (`self.IsDodging`))',1)
s=s.replace('(set `self.IsAttacking` true)','(set `self.IsAttacking` true)\n    (set `self.EnemyAttackInterrupted` false)',1)
s=s.replace('(if (and (not (`self.IsDead`)) (not (`self.SceneLocked`)))\n      (`self.DealSwordDamage`))','(if (and (not (`self.IsDead`)) (not (`self.SceneLocked`)) (not (`self.EnemyAttackInterrupted`)) (not (`self.HitStaggered`)))\n      (`self.DealSwordDamage`))',1)
s=s.replace('(not (`self.IsWindingUp`)))','(not (`self.IsWindingUp`)) (not (`self.HitStaggered`)))')
s=s.replace('(`self.FlashOnHit`)','(`self.FlashOnHit`)\n      (if (`self.IsEnemy`) (`self.StaggerOnHit`))',1)
# Guards freeze instead of being launched during their hit reaction.
s=s.replace('(`self.LaunchCharacter` (* (`KismetMathLibrary.Normal` (- (`self.K2_GetActorLocation`) (`self.K2_GetActorLocation` DamageCauser))) 170.0) true)','(if (not (`self.IsEnemy`)) (`self.LaunchCharacter` (* (`KismetMathLibrary.Normal` (- (`self.K2_GetActorLocation`) (`self.K2_GetActorLocation` DamageCauser))) 170.0) true))',1)
# Sweep away residual movement input while staggered.
i=s.index('(event `self.ReceiveTick`');at=s.index('  (if ',i)
s=s[:at]+'''  (if (`self.HitStaggered`) (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`)))
'''+s[at:]
s+='''
(event `StaggerOnHit`
 (set `self.HitStaggered` true)
 (set `self.EnemyAttackInterrupted` true)
 (set `self.IsWindingUp` false)
 (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`))
 (`SceneComponent.SetVisibility` (`self.AttackWarning`) false false)
 (`AnimInstance.StopSlotAnimation` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) 0.045 "DefaultSlot")
 (`KismetSystemLibrary.RetriggerableDelay` 0.24)
 (set `self.HitStaggered` false))
'''
pathlib.Path('work/stagger.dsl').write_text(s)
