import pathlib,json
exec(pathlib.Path('work/build_take2_dsl.py').read_text().split("parse='",1)[0])
s=json.loads(pathlib.Path('work/hitreaction-before.json').read_text(encoding='utf-8-sig'))['returnValue']['dsl']
s=s.replace('(event `self.ReceiveBeginPlay`','''(event `self.ReceiveBeginPlay`
 (if (`self.IsEnemy`)
  (`SkeletalMeshComponent.SetAnimInstanceClass` (`self.Mesh`) "/Game/OneMoreTake/Animations/ABP_GuardStrafe.ABP_GuardStrafe_C")
  (set `CharacterMovementComponent.bOrientRotationToMovement` false :`self` (`self.CharacterMovement`))
  (if (`KismetMathLibrary.RandomBool`) (set `self.OrbitDirection` 1.0) (else (set `self.OrbitDirection` -1.0))))''',1)
s=s.replace('(not (`self.HitStaggered`)) (not (`self.IsDodging`))','(not (`self.HitStaggered`)) (not (`self.HitReacting`)) (not (`self.IsDodging`))',1)
s=s.replace('(not (`self.IsWindingUp`)) (not (`self.HitStaggered`)))','(not (`self.IsWindingUp`)) (not (`self.HitStaggered`)) (not (`self.HitReacting`)))')
# Old sword-recovery timers must not stop a newer hit reaction.
s=s.replace('(if (and (not (`self.IsDead`)) (not (`self.SceneLocked`)))\n      (`AnimInstance.StopSlotAnimation`','(if (and (not (`self.IsDead`)) (not (`self.SceneLocked`)) (not (`self.HitReacting`)))\n      (`AnimInstance.StopSlotAnimation`',1)
health='(set `self.Health` (`KismetMathLibrary.FMax` (- (`self.Health`) Damage)))'
assert health in s
s=s.replace(health,health+'\n    (if (and (> Damage 0.0) (> (`self.Health`) 0.0)) (`self.PlayHitReaction`))',1)
s=s.replace('(set `self.IsDead` true)','(set `self.IsDead` true)\n      (set `self.HitReacting` false)',1)
i=s.index('(event `self.ReceiveTick`');at=s.index('  (if ',i)
s=s[:at]+'''  (if (and (`self.IsEnemy`) (not (`self.IsDead`)) (not (`self.SceneLocked`)))
    (bind player (`GameplayStatics.GetPlayerCharacter` 0))
    (if (not (`self.IsAttacking`))
      (`self.K2_SetActorRotation` (`KismetMathLibrary.FindLookAtRotation` (`self.K2_GetActorLocation`) (`self.K2_GetActorLocation` player))))
    (bind (anim ok) (cast `/Game/OneMoreTake/Animations/ABP_GuardStrafe` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) :!pure true))
    (if ok
      (set `/Game/OneMoreTake/Animations/ABP_GuardStrafe.RifleLocalVelocity` (`KismetMathLibrary.LessLess_VectorRotator` (`self.GetVelocity`) (`self.K2_GetActorRotation`)) :`self` anim)))
'''+s[at:]
# The waiting branch already corrects distance and separates guards. Add a gentle tangent.
old='(elif (> _returnvalue_2 440.0)'
# Canonical local names vary; insert immediately before the separation loop in the tick.
start=s.index('(event `self.ReceiveTick`');end=s.index('\n\n',start);part=s[start:end]
marker='(for _array_element_2'
if marker not in part:
 marker='(for _array_element'
 # Select the final foreach: the first is attack-turn coordination, the last is separation.
pos=part.rfind(marker)
assert pos>=0,part
tangent='''(if (not (`self.HasAttackTurn`))
 (`self.AddMovementInput` (`KismetMathLibrary.MakeVector` (- (.y _returnvalue)) (.x _returnvalue) 0.0) (* 0.30 (`self.OrbitDirection`))))
            '''
part=part[:pos]+tangent+part[pos:];s=s[:start]+part+s[end:]
s+='''
(event `PlayHitReaction`
 (if (not (`self.IsDead`))
  (set `self.HitReacting` true)
  (set `self.EnemyAttackInterrupted` true)
  (if (== (`self.HitReactionIndex`) 0)
   (set `self.HitReactionAnimation` "/Game/OneMoreTake/Animations/Retargeted/Hits/Knight_Stomach_Hit_Anim.Knight_Stomach_Hit_Anim")
   (elif (== (`self.HitReactionIndex`) 1)
    (set `self.HitReactionAnimation` "/Game/OneMoreTake/Animations/Retargeted/Hits/Knight_Head_Hit_Anim.Knight_Head_Hit_Anim")
    (else (set `self.HitReactionAnimation` "/Game/OneMoreTake/Animations/Retargeted/Hits/Knight_Hit_To_Body_Anim.Knight_Hit_To_Body_Anim"))))
  (set `self.HitReactionIndex` (mod (+ (`self.HitReactionIndex`) 1) 3))
  (`AnimInstance.PlaySlotAnimationAsDynamicMontage` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) (`self.HitReactionAnimation`) "DefaultSlot" 0.035 0.10 3.0 1 -1.0 0.0)
  (`KismetSystemLibrary.RetriggerableDelay` 0.36)
  (set `self.HitReacting` false)))
'''
pathlib.Path('work/hitreactions.dsl').write_text(s)
