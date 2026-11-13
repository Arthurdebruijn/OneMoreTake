import pathlib,json
s=json.loads(pathlib.Path('work/player-drop-before.json').read_text(encoding='utf-8-sig'))['returnValue']['dsl']
old='(set `self.StatusMessage` "Take failed. Resetting...")'
assert old in s
s=s.replace(old,'(`self.QueuePlayerWeaponDrop`)\n        '+old,1)
s+='''
(event `QueuePlayerWeaponDrop`
 (`KismetSystemLibrary.Delay` (`self.PlayerDeathDropTime`))
 (if (and (`self.IsDead`) (not (`self.IsEnemy`)) (not (`self.PlayerWeaponDropped`)))
  (set `self.PlayerWeaponDropped` true)
  (if (`self.HasGun`)
   (`self.ReleasePlayerWeapon` (`self.GunMesh`))
   (else (`self.ReleasePlayerWeapon` (`self.SwordBlade`))))))
(event `ReleasePlayerWeapon`
 (params (Weapon :type "StaticMeshComponent Object Reference"))
 (`SceneComponent.K2_DetachFromComponent` Weapon "KeepWorld" "KeepWorld" "KeepWorld" false)
 (bind (origin extent radius) (`KismetSystemLibrary.GetComponentBounds` Weapon))
 (bind floor (+ (- (.z (`self.K2_GetActorLocation`)) 90.0) 3.0))
 (bind bottom (- (.z origin) (.z extent)))
 (if (< bottom floor)
  (`SceneComponent.K2_SetWorldLocation` Weapon
   (+ (`SceneComponent.K2_GetComponentLocation` Weapon) (`KismetMathLibrary.MakeVector` 0.0 0.0 (- floor bottom))) false true))
 (`PrimitiveComponent.SetCollisionProfileName` Weapon "PhysicsActor" true)
 (`PrimitiveComponent.SetCollisionResponseToChannel` Weapon "ECC_Pawn" "ECR_Ignore")
 (`PrimitiveComponent.SetCollisionResponseToChannel` Weapon "ECC_PhysicsBody" "ECR_Ignore")
 (`PrimitiveComponent.SetCollisionResponseToChannel` Weapon "ECC_Visibility" "ECR_Ignore")
 (`PrimitiveComponent.SetCollisionResponseToChannel` Weapon "ECC_Camera" "ECR_Ignore")
 (`PrimitiveComponent.SetSimulatePhysics` Weapon true)
 (`PrimitiveComponent.SetLinearDamping` Weapon 0.7)
 (`PrimitiveComponent.SetAngularDamping` Weapon 1.2)
 (`PrimitiveComponent.WakeAllRigidBodies` Weapon)
 (`PrimitiveComponent.SetPhysicsLinearVelocity` Weapon
  (`KismetMathLibrary.GreaterGreater_VectorRotator` (-116.5 -250.85 71.14) (`SceneComponent.K2_GetComponentRotation` (`self.Mesh`))) false "None")
 (`PrimitiveComponent.SetPhysicsAngularVelocityInDegrees` Weapon (70.0 150.0 90.0) false "None"))
'''
pathlib.Path('work/player-drop.dsl').write_text(s)
