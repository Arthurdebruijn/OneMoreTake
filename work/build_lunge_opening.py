import pathlib,json
exec(pathlib.Path('work/build_take2_dsl.py').read_text().split("parse='",1)[0])
s=json.loads(pathlib.Path('work/lunge-opening-before.json').read_text(encoding='utf-8-sig'))['returnValue']['dsl']
head=s.index('(event `FindMeleeTarget`');end=s.index('\n\n',head);entry=s[head:end]
entry=entry[:-1]+'''
 (if (`KismetSystemLibrary.IsValid` (`self.MeleeTarget`))
  (bind target (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` (`self.MeleeTarget`)))
  (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.PauseForPlayerLunge` target)))'''
s=s[:head]+entry+s[end:]
s=s.replace('(not (`self.HitStaggered`))','(not (`self.HitStaggered`)) (not (`self.LungePaused`))')
# Stop residual movement during the opening, including previously accumulated input.
s=s.replace('(if (`self.HitStaggered`)','(if (or (`self.HitStaggered`) (`self.LungePaused`))',1)
s+='''
(event `PauseForPlayerLunge`
 (if (and (`self.IsEnemy`) (not (`self.IsDead`)))
  (set `self.LungePaused` true)
  (set `self.EnemyAttackInterrupted` true)
  (set `self.IsWindingUp` false)
  (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`))
  (`SceneComponent.SetVisibility` (`self.AttackWarning`) false false)
  (`AnimInstance.StopSlotAnimation` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) 0.05 "DefaultSlot")
  (`KismetSystemLibrary.RetriggerableDelay` 0.48)
  (set `self.LungePaused` false)))
'''
pathlib.Path('work/lunge-opening.dsl').write_text(s)
