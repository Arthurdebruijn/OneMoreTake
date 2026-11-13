(event `ShowGunShot`
  (if (`self.IsPistol`)
    (`GameplayStatics.PlaySound2D` "/Game/Sounds/Guns/Revolver_Fire_Sound.Revolver_Fire_Sound" 0.55)
    (else
      (`GameplayStatics.PlaySound2D` "/Game/Sounds/Guns/AK47_Fire_Sound.AK47_Fire_Sound" 0.4)))
  (if (> (`KismetMathLibrary.VSize` (- (`self.GunShotEnd`) (`self.GunShotStart`))) 1.0)
    (`SceneComponent.K2_SetWorldLocationAndRotation` (`self.GunTracer`) (* (+ (`self.GunShotStart`) (`self.GunShotEnd`)) 0.5) (`KismetMathLibrary.FindLookAtRotation` (`self.GunShotStart`) (`self.GunShotEnd`)) false true)
    (`SceneComponent.SetWorldScale3D` (`self.GunTracer`) (`KismetMathLibrary.MakeVector` (/ (`KismetMathLibrary.VSize` (- (`self.GunShotEnd`) (`self.GunShotStart`))) 100.0) 0.025 0.025))
    (`SceneComponent.SetVisibility` (`self.GunTracer`) true false))
  (`SceneComponent.SetVisibility` (`self.MuzzleFlash`) true false)
  (`KismetSystemLibrary.Delay` 0.055)
  (`SceneComponent.SetVisibility` (`self.GunTracer`) false false)
  (`SceneComponent.SetVisibility` (`self.MuzzleFlash`) false false))
