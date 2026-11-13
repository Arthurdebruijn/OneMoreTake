(event `self.ReceiveDrawHUD`
  (params (SizeX :type Integer) (SizeY :type Integer))
  ; Always-visible controls and health for the first combat prototype.
  (`self.DrawRect` (struct :`R` 0.015 :`G` 0.02 :`B` 0.03 :`A` 0.85) 16.0 16.0 590.0 145.0)
  (`self.DrawText` "ONE MORE TAKE - Sword rehearsal" (struct :`R` 1.0 :`G` 0.85 :`B` 0.4 :`A` 1.0) 30.0 26.0 null 1.5 false)
  (`self.DrawText` "WASD: move   Left click: sword   R: restart" (struct :`R` 1.0 :`G` 1.0 :`B` 1.0 :`A` 1.0) 30.0 55.0 null 1.1 false)
  (bind player (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` (`GameplayStatics.GetPlayerCharacter` 0)))
  (`self.DrawText` (`KismetStringLibrary.Concat_StrStr` "YOU  " (`KismetStringLibrary.Conv_IntToString` (`KismetMathLibrary.FTrunc` (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.Health` player)))) (struct :`R` 0.4 :`G` 1.0 :`B` 0.65 :`A` 1.0) 30.0 84.0 null 1.2 false)
  (`self.DrawRect` (struct :`R` 0.1 :`G` 0.1 :`B` 0.1 :`A` 1.0) 135.0 89.0 180.0 12.0)
  (`self.DrawRect` (struct :`R` 0.1 :`G` 0.8 :`B` 0.35 :`A` 1.0) 135.0 89.0 (* (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.Health` player) 1.8) 12.0)
  (`self.DrawText` (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.StatusMessage` player) (struct :`R` 1.0 :`G` 1.0 :`B` 1.0 :`A` 1.0) 30.0 128.0 null 1.0 false)
  (bind guards (`GameplayStatics.GetAllActorsOfClass` "/Game/OneMoreTake/Blueprints/BP_Guard.BP_Guard_C"))
  (for actor guards
    (bind guard (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` actor))
    (`self.DrawText` (`KismetStringLibrary.Concat_StrStr` "GUARD  " (`KismetStringLibrary.Conv_IntToString` (`KismetMathLibrary.FTrunc` (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.Health` guard)))) (struct :`R` 1.0 :`G` 0.45 :`B` 0.35 :`A` 1.0) 340.0 84.0 null 1.2 false)
    (`self.DrawRect` (struct :`R` 0.1 :`G` 0.1 :`B` 0.1 :`A` 1.0) 435.0 89.0 150.0 12.0)
    (`self.DrawRect` (struct :`R` 0.9 :`G` 0.15 :`B` 0.12 :`A` 1.0) 435.0 89.0 (* (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.Health` guard) 1.5) 12.0)
    (if (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` guard)
      (`self.DrawText` "CUT! Guard defeated - R for another take" (struct :`R` 1.0 :`G` 0.85 :`B` 0.25 :`A` 1.0) 30.0 180.0 null 1.8 false))))
