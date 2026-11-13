import pathlib,json
s=json.loads(pathlib.Path('work/drop-before.json').read_text(encoding='utf-8-sig'))['returnValue']['dsl']
s=s.replace('(if (and (`self.IsEnemy`) (`self.UseEnemyRagdoll`))','(if (`self.IsEnemy`) (`self.DropSwordOnDeath` DamageCauser))\n    (if (and (`self.IsEnemy`) (`self.UseEnemyRagdoll`))',1)
s=s.replace('160.0','(`self.RagdollPushStrength`)').replace('(0.0 0.0 60.0)','(`KismetMathLibrary.MakeVector` 0.0 0.0 (`self.RagdollLiftStrength`))').replace('-140.0','(- (`self.RagdollPushStrength`))').replace('(0.0 0.0 55.0)','(`KismetMathLibrary.MakeVector` 0.0 0.0 (`self.RagdollLiftStrength`))')
s+='''
(event `DropSwordOnDeath`
 (params (HitSource :type "Actor Object Reference"))
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
  (bind offset (- (`self.K2_GetActorLocation`) (`self.K2_GetActorLocation` HitSource)))
  (`PrimitiveComponent.AddImpulse` (`self.SwordBlade`)
   (+ (* (`KismetMathLibrary.Normal` (`KismetMathLibrary.MakeVector` (.x offset) (.y offset) 0.0)) (* (`self.RagdollPushStrength`) 0.45))
      (`KismetMathLibrary.MakeVector` 0.0 0.0 (* (`self.RagdollLiftStrength`) 0.5))) "None" true)
  (else (`PrimitiveComponent.AddImpulse` (`self.SwordBlade`) (0.0 0.0 60.0) "None" true))))
'''
pathlib.Path('work/sword-drop.dsl').write_text(s)
