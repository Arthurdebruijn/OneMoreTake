import pathlib,json
s=json.loads(pathlib.Path('work/ragdoll-before.json').read_text(encoding='utf-8-sig'))['returnValue']['dsl']
old='(`SkeletalMeshComponent.PlayAnimation` (`self.Mesh`) "/Game/OneMoreTake/Animations/A_KnightDeath.A_KnightDeath" false)'
assert old in s
s=s.replace(old,'''(if (and (`self.IsEnemy`) (`self.UseEnemyRagdoll`))
      (`self.StartEnemyRagdoll` DamageCauser)
      (else (`SkeletalMeshComponent.PlayAnimation` (`self.Mesh`) "/Game/OneMoreTake/Animations/A_KnightDeath.A_KnightDeath" false)))''',1)
s+='''
(event `StartEnemyRagdoll`
 (params (HitSource :type "Actor Object Reference"))
 (`AnimInstance.StopSlotAnimation` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) 0.0 "DefaultSlot")
 (`PrimitiveComponent.SetCollisionProfileName` (`self.Mesh`) "Ragdoll" true)
 (`PrimitiveComponent.SetCollisionResponseToChannel` (`self.Mesh`) "ECC_Visibility" "ECR_Ignore")
 (`PrimitiveComponent.SetCollisionResponseToChannel` (`self.Mesh`) "ECC_Pawn" "ECR_Ignore")
 (`PrimitiveComponent.SetSimulatePhysics` (`self.Mesh`) true)
 (`PrimitiveComponent.WakeAllRigidBodies` (`self.Mesh`))
 (if (`KismetSystemLibrary.IsValid` HitSource)
  (bind offset (- (`self.K2_GetActorLocation`) (`self.K2_GetActorLocation` HitSource)))
  (bind direction (`KismetMathLibrary.Normal` (`KismetMathLibrary.MakeVector` (.x offset) (.y offset) 0.0)))
  (`PrimitiveComponent.AddImpulse` (`self.Mesh`) (+ (* direction 270.0) (0.0 0.0 90.0)) "pelvis" true)
  (else (`PrimitiveComponent.AddImpulse` (`self.Mesh`) (+ (* (`self.GetActorForwardVector`) -200.0) (0.0 0.0 80.0)) "pelvis" true))))
'''
pathlib.Path('work/ragdoll.dsl').write_text(s)
