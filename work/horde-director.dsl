(event `WakeNextZombie`
  (bind _outactors (`GameplayStatics.GetAllActorsOfClass` "/Game/OneMoreTake/Blueprints/BP_WaveZombie.BP_WaveZombie_C"))
  (for _array_element _outactors
    (bind _asbp_knight_player (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` _array_element))
    (if (and (== (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.ZombieWaveIndex` _asbp_knight_player) (`self.CurrentZombieWave`)) (== (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.ZombieWakeOrder` _asbp_knight_player) (`self.WakeIndex`)))
      (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.WakeZombie` _asbp_knight_player)))
  (set `self.WakeIndex` (+ (`self.WakeIndex`) 1))
  (if (<= (`self.WakeIndex`) (`self.WaveZombieTotal`))
    (`KismetSystemLibrary.Delay` (`KismetMathLibrary.SelectFloat` (`KismetMathLibrary.RandomFloatInRange` 1.25 2.2) (`KismetMathLibrary.RandomFloatInRange` 0.65 0.95) (> (`self.CurrentZombieWave`) 1)))
    (`self.WakeNextZombie`)
    (else
      (set `self.WaveSpawning` false))))
