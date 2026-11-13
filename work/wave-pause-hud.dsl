(event `self.ReceiveDrawHUD`
  (params (SizeX :type Integer) (SizeY :type Integer))
  (`self.DrawRect` (struct :`R` 0.015 :`G` 0.02 :`B` 0.03 :`A` 0.85) 16.0 16.0 650.0 145.0)
  (`self.DrawText` "ONE MORE TAKE" (struct :`R` 1.0 :`G` 0.85 :`B` 0.4 :`A` 1.0) 30.0 26.0 "/Game/Fonts/alagard_Font.alagard_Font" 2.025)
  (`self.DrawText` "WASD: move | Click: attack | Space: dodge | R: retry" (struct :`R` 1.0 :`G` 1.0 :`B` 1.0 :`A` 1.0) 30.0 55.0 "/Game/Fonts/alagard_Font.alagard_Font" 1.485)
  (bind _asbp_knight_player (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` (`GameplayStatics.GetPlayerCharacter` 0)))
  (`self.DrawText` (`KismetStringLibrary.Concat_StrStr` "YOU  " (`KismetStringLibrary.Conv_IntToString` (`KismetMathLibrary.FTrunc` (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.Health` _asbp_knight_player)))) (struct :`R` 0.4 :`G` 1.0 :`B` 0.65 :`A` 1.0) 30.0 84.0 "/Game/Fonts/alagard_Font.alagard_Font" 1.62)
  (`self.DrawRect` (struct :`R` 0.1 :`G` 0.1 :`B` 0.1 :`A` 1.0) 135.0 89.0 180.0 12.0)
  (`self.DrawRect` (struct :`R` 0.1 :`G` 0.8 :`B` 0.35 :`A` 1.0) 135.0 89.0 (* (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.Health` _asbp_knight_player) 1.8) 12.0)
  (bind _returnvalue (`GameplayStatics.GetActorOfClass` "/Game/OneMoreTake/Blueprints/BP_TakeDirector.BP_TakeDirector_C"))
  (bind _asbp_take_director (cast `/Game/OneMoreTake/Blueprints/BP_TakeDirector` _returnvalue))
  (if (== (`/Game/OneMoreTake/Blueprints/BP_TakeDirector.TakeNumber` _asbp_take_director) 3)
    (`self.DrawText` (`KismetStringLibrary.Concat_StrStr` (`KismetStringLibrary.Concat_StrStr` "WAVE " (`KismetStringLibrary.Conv_IntToString` (`/Game/OneMoreTake/Blueprints/BP_TakeDirector.CurrentZombieWave` _asbp_take_director))) (`KismetStringLibrary.Concat_StrStr` "/3  LEFT: " (`KismetStringLibrary.Conv_IntToString` (`/Game/OneMoreTake/Blueprints/BP_TakeDirector.CurrentWaveRemaining` _asbp_take_director)))) (struct :`R` 0.65 :`G` 1.0 :`B` 0.4 :`A` 1.0) 340.0 84.0 "/Game/Fonts/alagard_Font.alagard_Font" 1.62)
    (else
      (`self.DrawText` (`KismetStringLibrary.Concat_StrStr` "GUARDS LEFT: " (`KismetStringLibrary.Conv_IntToString` (`/Game/OneMoreTake/Blueprints/BP_TakeDirector.EnemiesRemaining` _asbp_take_director))) (struct :`R` 1.0 :`G` 0.5 :`B` 0.3 :`A` 1.0) 340.0 84.0 "/Game/Fonts/alagard_Font.alagard_Font" 1.62)))
  (if (== (`/Game/OneMoreTake/Blueprints/BP_TakeDirector.TakeNumber` _asbp_take_director) 3)
    (`self.DrawText` "TAKE 3: ZOMBIE WAVES | Hold click: rifle | Space: dodge" (struct :`R` 0.3 :`G` 1.0 :`B` 1.0 :`A` 1.0) 30.0 165.0 "/Game/Fonts/alagard_Font.alagard_Font" 1.485)
    (elif (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.HasGun` _asbp_knight_player)
      (`self.DrawText` "TAKE 2: Mouse aim | Hold click: shoot | Unlimited ammo" (struct :`R` 1.0 :`G` 0.85 :`B` 0.4 :`A` 1.0) 30.0 165.0 "/Game/Fonts/alagard_Font.alagard_Font" 1.485)
      (else
        (`self.DrawText` "TAKE 1: Sword fight" (struct :`R` 1.0 :`G` 0.85 :`B` 0.4 :`A` 1.0) 30.0 165.0 "/Game/Fonts/alagard_Font.alagard_Font" 1.485))))
  (`self.DrawText` (`/Game/OneMoreTake/Blueprints/BP_TakeDirector.Objective` _asbp_take_director) (struct :`R` 1.0 :`G` 1.0 :`B` 1.0 :`A` 1.0) 30.0 128.0 "/Game/Fonts/alagard_Font.alagard_Font" 1.35)
  (if (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` _asbp_knight_player)
    (`self.DrawText` "Take failed. Resetting..." (struct :`R` 1.0 :`G` 0.4 :`B` 0.3 :`A` 1.0) 30.0 180.0 "/Game/Fonts/alagard_Font.alagard_Font" 2.43))
  (if (and (== (`/Game/OneMoreTake/Blueprints/BP_TakeDirector.TakeNumber` _asbp_take_director) 3) (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` _asbp_knight_player)) (< (`GameplayStatics.GetTimeSeconds`) (`/Game/OneMoreTake/Blueprints/BP_TakeDirector.WaveBannerUntil` _asbp_take_director)))
    (`self.DrawRect` (struct :`R` 0.015 :`G` 0.02 :`B` 0.03 :`A` 0.88) (- (* SizeX 0.5) 230.0) (* SizeY 0.22) 460.0 80.0)
    (`self.DrawText` (`/Game/OneMoreTake/Blueprints/BP_TakeDirector.WaveBanner` _asbp_take_director) (struct :`R` 1.0 :`G` 0.85 :`B` 0.4 :`A` 1.0) (- (* SizeX 0.5) 200.0) (+ (* SizeY 0.22) 18.0) "/Game/Fonts/alagard_Font.alagard_Font" 2.97))
  (if (== (`/Game/OneMoreTake/Blueprints/BP_TakeDirector.Stage` _asbp_take_director) 3)
    ; A large final-slate overlay appears only after all objectives are complete.
    (`self.DrawRect` (struct :`A` 0.8) 0.0 (* SizeY 0.32) (`KismetMathLibrary.Conv_IntToDouble` SizeX) 180.0)
    (`self.DrawText` "CUT!" (struct :`R` 1.0 :`G` 0.85 :`B` 0.25 :`A` 1.0) (- (* SizeX 0.5) 85.0) (* SizeY 0.35) "/Game/Fonts/alagard_Font.alagard_Font" 6.75)
    (`self.DrawText` (`/Game/OneMoreTake/Blueprints/BP_TakeDirector.DirectorNote` _asbp_take_director) (struct :`R` 1.0 :`G` 1.0 :`B` 1.0 :`A` 1.0) 30.0 (+ (* SizeY 0.35) 85.0) "/Game/Fonts/alagard_Font.alagard_Font" 1.62)))

(event `self.ReceiveBeginPlay`)

(event `self.ReceiveActorBeginOverlap`
  (params (OtherActor :type "Actor Object Reference")))

(event `self.ReceiveTick`
  (params (DeltaSeconds :type "Float (single-precision)")))

(fn `UserConstructionScript`)

