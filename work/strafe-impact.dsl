(event `self.ReceiveBeginPlay`
 (`SceneComponent.SetVisibility` (`self.Flash`) true false)
 (`SceneComponent.SetVisibility` (`self.Smoke`) false false)
 (`NiagaraFunctionLibrary.SpawnSystemAtLocation` "/Game/OneMoreTake/Effects/NS_StrafeImpact.NS_StrafeImpact" (`self.K2_GetActorLocation`) (struct) (0.25 0.25 0.25) true true)
 (`self.SetLifeSpan` 0.8))
(event `self.ReceiveTick`
 (params (DeltaSeconds :type "Float (single-precision)"))
 (set `self.Age` (+ (`self.Age`) DeltaSeconds))
 (`SceneComponent.SetVisibility` (`self.Flash`) (< (`self.Age`) 0.12) false)
 (`SceneComponent.SetRelativeScale3D` (`self.Smoke`) (`KismetMathLibrary.MakeVector` (+ 0.3 (* (`self.Age`) 0.8)) (+ 0.3 (* (`self.Age`) 0.8)) (+ 0.5 (* (`self.Age`) 1.1))))
 (`SceneComponent.K2_SetRelativeLocation` (`self.Smoke`) (`KismetMathLibrary.MakeVector` 0.0 0.0 (+ 15.0 (* (`self.Age`) 90.0))) false true))

