(event `self.ReceiveBeginPlay`
  (set `self.Stage` 0)
  (set `self.Objective` "Defeat the guard")
  (bind player (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` (`GameplayStatics.GetPlayerCharacter` 0)))
  (set `self.PlayerRef` player)
  (bind guardActor (`GameplayStatics.GetActorOfClass` "/Game/OneMoreTake/Blueprints/BP_Guard.BP_Guard_C"))
  (bind guard (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` guardActor))
  (set `self.EnemyRef` guard)
  (bind crown (`GameplayStatics.GetActorOfClass` "/Game/OneMoreTake/Blueprints/BP_CrownPickup.BP_CrownPickup_C"))
  (set `self.CrownRef` crown)
  (bind mark (`GameplayStatics.GetActorOfClass` "/Game/OneMoreTake/Blueprints/BP_FinishMark.BP_FinishMark_C"))
  (set `self.MarkRef` mark)
  (`Actor.SetActorHiddenInGame` mark true))

(event `self.ReceiveTick`
  (params (DeltaSeconds :type "Float (single-precision)"))
  (if (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` (`self.PlayerRef`)))
    (if (and (== (`self.Stage`) 0) (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` (`self.EnemyRef`)))
      (set `self.Stage` 1)
      (set `self.Objective` "Collect the crown - continue right")
      (bind crown (cast `/Game/OneMoreTake/Blueprints/BP_CrownPickup` (`self.CrownRef`)))
      (`/Game/OneMoreTake/Blueprints/BP_CrownPickup.UnlockCrown` crown))
    (if (and (== (`self.Stage`) 1) (< (`Actor.GetDistanceTo` (`self.PlayerRef`) (`self.CrownRef`)) 135.0))
      (`self.CollectCrown`))
    (if (and (== (`self.Stage`) 2) (< (`Actor.GetDistanceTo` (`self.PlayerRef`) (`self.MarkRef`)) 150.0))
      (`self.EndTake`))))

(event `CollectCrown`
  ; Guard and distance gates prevent pickup before combat is complete.
  (if (and (== (`self.Stage`) 1) (< (`Actor.GetDistanceTo` (`self.PlayerRef`) (`self.CrownRef`)) 135.0))
    (set `self.Stage` 2)
    (set `self.Objective` "Hit your mark beside the princess - continue right")
    (`Actor.SetActorHiddenInGame` (`self.CrownRef`) true)
    (`SceneComponent.SetVisibility` (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.CarriedCrown` (`self.PlayerRef`)) true false)
    (`Actor.SetActorHiddenInGame` (`self.MarkRef`) false)))

(event `EndTake`
  ; A successful take can end only once, while carrying the crown at the mark.
  (if (and (== (`self.Stage`) 2) (< (`Actor.GetDistanceTo` (`self.PlayerRef`) (`self.MarkRef`)) 150.0))
    (set `self.Stage` 3)
    (set `self.Objective` "CUT!")
    (set `self.DirectorNote` "That's the shot!")
    (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.LockForCut` (`self.PlayerRef`))
    (`GameplayStatics.PlaySound2D` "/Game/OneMoreTake/Audio/S_DirectorCut.S_DirectorCut" 1.0 0.9)
    (`KismetSystemLibrary.Delay` 1.1)
    (set `self.DirectorNote` "Back to one! Reset the scene.")
    (`KismetSystemLibrary.Delay` 1.9)
    (`GameplayStatics.OpenLevel` "L_MovieSet" true "")))
