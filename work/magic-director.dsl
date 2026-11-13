(event `self.ReceiveBeginPlay`
  (set `self.Stage` 0)
  (set `self.TakeNumber` 1)
  (if (== (`GameplayStatics.ParseOption` (`GameModeBase.OptionsString` (`GameplayStatics.GetGameMode`)) "Take") "3") (set `self.TakeNumber` 3))
  (if (== (`GameplayStatics.ParseOption` (`GameModeBase.OptionsString` (`GameplayStatics.GetGameMode`)) "Take") "2")
    (set `self.TakeNumber` 2))
  (set `self.Objective` "Defeat all guards, then collect the crown")
  (if (== (`self.TakeNumber`) 3) (set `self.Objective` "Blast the undead horde, then collect the crown"))
  (bind _asbp_knight_player (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` (`GameplayStatics.GetPlayerCharacter` 0)))
  (set `self.PlayerRef` _asbp_knight_player)
  (bind _returnvalue (`GameplayStatics.GetActorOfClass` "/Game/OneMoreTake/Blueprints/BP_Guard.BP_Guard_C"))
  (bind _asbp_knight_player_2 (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` _returnvalue))
  (set `self.EnemyRef` _asbp_knight_player_2)
  (bind _returnvalue_2 (`GameplayStatics.GetActorOfClass` "/Game/OneMoreTake/Blueprints/BP_CrownPickup.BP_CrownPickup_C"))
  (set `self.CrownRef` _returnvalue_2)
  (bind _returnvalue_3 (`GameplayStatics.GetActorOfClass` "/Game/OneMoreTake/Blueprints/BP_FinishMark.BP_FinishMark_C"))
  (set `self.MarkRef` _returnvalue_3)
  (`self.SetActorHiddenInGame` _returnvalue_3 true))

(event `self.ReceiveTick`
  (params (DeltaSeconds :type "Float (single-precision)"))
  (set `self.EnemiesRemaining` 0)
  (bind _outactors (`GameplayStatics.GetAllActorsOfClass` "/Game/OneMoreTake/Blueprints/BP_Guard.BP_Guard_C"))
  (for _array_element _outactors
    (bind _asbp_knight_player (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` _array_element))
    (if (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` _asbp_knight_player))
      (set `self.EnemiesRemaining` (+ (`self.EnemiesRemaining`) 1))))
  (if (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` (`self.PlayerRef`))
    _
    (elif (and (== (`self.Stage`) 0) (== (`self.EnemiesRemaining`) 0))
      (set `self.Stage` 1)
      (set `self.Objective` "Collect the crown - continue right")
      (bind _asbp_crown_pickup (cast `/Game/OneMoreTake/Blueprints/BP_CrownPickup` (`self.CrownRef`)))
      (`/Game/OneMoreTake/Blueprints/BP_CrownPickup.UnlockCrown` _asbp_crown_pickup)))
  (if (and (== (`self.Stage`) 1) (< (`self.GetDistanceTo` (`self.PlayerRef`) (`self.CrownRef`)) 135.0))
    (`self.CollectCrown`))
  (if (and (== (`self.Stage`) 2) (< (`self.GetDistanceTo` (`self.PlayerRef`) (`self.MarkRef`)) 150.0))
    (`self.EndTake`)))

(event `CollectCrown`
  ; Guard and distance gates prevent pickup before combat is complete.
  (if (and (== (`self.Stage`) 1) (< (`self.GetDistanceTo` (`self.PlayerRef`) (`self.CrownRef`)) 135.0))
    (set `self.Stage` 2)
    (set `self.Objective` "Hit your mark beside the princess - continue right")
    (`self.SetActorHiddenInGame` (`self.CrownRef`) true)
    (`SceneComponent.SetVisibility` (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.CarriedCrown` (`self.PlayerRef`)) true false)
    (`self.SetActorHiddenInGame` (`self.MarkRef`) false)))

(event `EndTake`
  (if (and (== (`self.Stage`) 2) (< (`self.GetDistanceTo` (`self.PlayerRef`) (`self.MarkRef`)) 150.0))
    (set `self.Stage` 3)
    (set `self.Objective` "CUT!")
    (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.LockForCut` (`self.PlayerRef`))
    (`GameplayStatics.PlaySound2D` "/Game/OneMoreTake/Audio/S_DirectorCut.S_DirectorCut" 1.0 0.9)
    (if (== (`self.TakeNumber`) 1)
      (set `self.DirectorNote` "Good. Now give the knight a GUN. And double the guards!")
      (`KismetSystemLibrary.Delay` 3.5)
      (`GameplayStatics.OpenLevel` "L_MovieSet" true "Take=2")
      (elif (== (`self.TakeNumber`) 2)
        (set `self.DirectorNote` "Lose the gun. Give me MAGIC! Bring those dead extras back!")
        (`KismetSystemLibrary.Delay` 3.5)
        (`GameplayStatics.OpenLevel` "L_MovieSet" true "Take=3")
        (else (set `self.DirectorNote` "That's a wrap! Three takes complete. Next: AIR SUPPORT!"))))))

(event `self.ReceiveActorBeginOverlap`
  (params (OtherActor :type "Actor Object Reference")))

(fn `UserConstructionScript`)
