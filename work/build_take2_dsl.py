import json,pathlib
w=pathlib.Path('work')
def read(n):return json.loads((w/f'take2-{n}.json').read_text(encoding='utf-8-sig'))['returnValue']['dsl']
def replace_form(s,head,new):
 start=s.index(head); depth=0; quoted=False;tick=False;esc=False
 for i in range(start,len(s)):
  c=s[i]
  if c=='"' and not tick and not esc:quoted=not quoted
  if c=='`' and not quoted:tick=not tick
  if not quoted and not tick:
   if c=='(':depth+=1
   if c==')':
    depth-=1
    if depth==0:return s[:start]+new+s[i+1:]
  esc=(c=='\\' and not esc)
 raise Exception(head)
parse='(`GameplayStatics.ParseOption` (`GameModeBase.OptionsString` (`GameplayStatics.GetGameMode`)) "Take")'
s=read('BP_KnightPlayer')
s=replace_form(s,'(event `Key|LeftMouseButton`','''(event `Key|LeftMouseButton`
 (params (Key :type "Key Structure"))
 (:`Pressed` (if (`self.HasGun`) (set `self.FireHeld` true) (`self.FireGun`) (else (`self.SwordAttack`))))
 (:`Released` (set `self.FireHeld` false)))''')
s=s.replace('(`GameplayStatics.OpenLevel` "L_MovieSet")','(`self.RestartCurrentTake`)')
# Preserve the guard AI, and fire repeatedly without blocking movement.
tickstart=s.index('(event `self.ReceiveTick`')
insert=s.index('  (if ',tickstart)
s=s[:insert]+'''  (if (and (`self.HasGun`) (`self.FireHeld`) (`self.GunReady`)) (`self.FireGun`))
'''+s[insert:]
s=s.replace('(and (`self.IsEnemy`) (not (`self.IsDead`)) (not (`self.IsAttacking`)) (not (`self.IsWindingUp`)))','(and (`self.IsEnemy`) (not (`self.SceneLocked`)) (not (`self.IsDead`)) (not (`self.IsAttacking`)) (not (`self.IsWindingUp`)))')
s+='''
(event `self.ReceiveBeginPlay`
 (set `self.GunReady` true)
 (if (== PARSE "2")
   (if (not (`self.IsEnemy`)) (`self.EquipGun`))
   (else (if (`self.ExtraTakeTwoGuard`) (`self.K2_DestroyActor`)))))
(event `EquipGun`
 (set `self.HasGun` true)
 (`SceneComponent.SetVisibility` (`self.SwordRoot`) false true)
 (`SceneComponent.K2_AttachToComponent` (`self.GunMesh`) (`self.Mesh`) "hand_r" "SnapToTarget" "SnapToTarget" "KeepRelative" false)
 (`SceneComponent.SetVisibility` (`self.GunMesh`) true false))
(event `RestartCurrentTake`
 (if (`self.HasGun`) (`GameplayStatics.OpenLevel` "L_MovieSet" true "Take=2")
 (else (`GameplayStatics.OpenLevel` "L_MovieSet" true "Take=1"))))
(event `FireGun`
 (if (and (`self.GunReady`) (`self.HasGun`) (not (`self.IsDead`)) (not (`self.SceneLocked`)))
  (set `self.GunTarget` null)
  (set `self.GunTargetDistance` 1500.0)
  (for target (`GameplayStatics.GetAllActorsOfClass` "/Game/OneMoreTake/Blueprints/BP_Guard.BP_Guard_C")
   (bind guard (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` target))
   (if (and (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` guard)) (< (`self.GetDistanceTo` guard) (`self.GunTargetDistance`)))
    (set `self.GunTarget` guard)
    (set `self.GunTargetDistance` (`self.GetDistanceTo` guard))))
  (set `self.GunReady` false)
  (if (`KismetSystemLibrary.IsValid` (`self.GunTarget`))
   (`self.K2_SetActorRotation` (`KismetMathLibrary.FindLookAtRotation` (`self.K2_GetActorLocation`) (`self.K2_GetActorLocation` (`self.GunTarget`))))
   (`GameplayStatics.ApplyDamage` (`self.GunTarget`) 40.0 (`self.GetController`) self)
   (`self.ShowGunShot`)
   (else (`self.ShowGunShot`)))
  (`AnimInstance.PlaySlotAnimationAsDynamicMontage` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) "/Game/OneMoreTake/Animations/A_KnightGunFire.A_KnightGunFire" "DefaultSlot" 0.05 0.1 2.5 1 -1.0 0.0)
  (`KismetSystemLibrary.Delay` 0.25)
  (set `self.GunReady` true)))
'''.replace('PARSE',parse)
(w/'take2-player.dsl').write_text(s)
d=read('BP_TakeDirector')
d=d.replace('(set `self.Stage` 0)','''(set `self.Stage` 0)
 (set `self.TakeNumber` 1)
 (if (== PARSE "2") (set `self.TakeNumber` 2))'''.replace('PARSE',parse))
d=d.replace('"Defeat the guard"','"Defeat all guards, then collect the crown"')
d=replace_form(d,'(event `self.ReceiveTick`','''(event `self.ReceiveTick`
 (params (DeltaSeconds :type "Float (single-precision)"))
 (set `self.EnemiesRemaining` 0)
 (for enemy (`GameplayStatics.GetAllActorsOfClass` "/Game/OneMoreTake/Blueprints/BP_Guard.BP_Guard_C")
  (bind guard (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` enemy))
  (if (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` guard)) (set `self.EnemiesRemaining` (+ (`self.EnemiesRemaining`) 1))))
 (if (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` (`self.PlayerRef`)))
  (if (and (== (`self.Stage`) 0) (== (`self.EnemiesRemaining`) 0))
   (set `self.Stage` 1) (set `self.Objective` "Collect the crown - continue right")
   (bind crown (cast `/Game/OneMoreTake/Blueprints/BP_CrownPickup` (`self.CrownRef`)))
   (`/Game/OneMoreTake/Blueprints/BP_CrownPickup.UnlockCrown` crown))
  (if (and (== (`self.Stage`) 1) (< (`self.GetDistanceTo` (`self.PlayerRef`) (`self.CrownRef`)) 135.0)) (`self.CollectCrown`))
  (if (and (== (`self.Stage`) 2) (< (`self.GetDistanceTo` (`self.PlayerRef`) (`self.MarkRef`)) 150.0)) (`self.EndTake`))))''')
d=replace_form(d,'(event `EndTake`','''(event `EndTake`
 (if (and (== (`self.Stage`) 2) (< (`self.GetDistanceTo` (`self.PlayerRef`) (`self.MarkRef`)) 150.0))
  (set `self.Stage` 3) (set `self.Objective` "CUT!")
  (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.LockForCut` (`self.PlayerRef`))
  (`GameplayStatics.PlaySound2D` "/Game/OneMoreTake/Audio/S_DirectorCut.S_DirectorCut" 1.0 0.9)
  (if (== (`self.TakeNumber`) 1)
   (set `self.DirectorNote` "Good. Now give the knight a GUN. And double the guards!")
   (`KismetSystemLibrary.Delay` 3.5)
   (`GameplayStatics.OpenLevel` "L_MovieSet" true "Take=2")
   (else (set `self.DirectorNote` "That's a wrap! Both takes complete. R to replay Take 2.")))))''')
(w/'take2-director.dsl').write_text(d)
h=read('BP_CombatHUD')
h=h.replace('  (`self.DrawText` "TAKE ONE - The Crown"','  (`self.DrawText` "ONE MORE TAKE"')
h=h.replace('"WASD: move   Left click: sword   R: restart"','"WASD: move   Left click: attack   R: retry current take"')
start=h.index('  (bind _outactors');end=h.index('  (bind _returnvalue',start)
h=h[:start]+h[end:]
point=h.index('  (`self.DrawText` (`/Game/OneMoreTake/Blueprints/BP_TakeDirector.Objective`')
h=h[:point]+'''  (`self.DrawText` (`KismetStringLibrary.Concat_StrStr` "GUARDS LEFT: " (`KismetStringLibrary.Conv_IntToString` (`/Game/OneMoreTake/Blueprints/BP_TakeDirector.EnemiesRemaining` _asbp_take_director))) (struct :`R` 1.0 :`G` 0.5 :`B` 0.3 :`A` 1.0) 340.0 84.0 null 1.2)
 (if (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.HasGun` _asbp_knight_player)
  (`self.DrawText` "TAKE 2: Hold click to shoot | Auto aim | Unlimited ammo" (struct :`R` 1.0 :`G` 0.85 :`B` 0.4 :`A` 1.0) 30.0 165.0 null 1.1)
  (else (`self.DrawText` "TAKE 1: Sword fight" (struct :`R` 1.0 :`G` 0.85 :`B` 0.4 :`A` 1.0) 30.0 165.0 null 1.1)))
'''+h[point:]
h=h.replace('(- (* SizeX 0.5) 180.0)','30.0').replace('null 1.5)))','null 1.2)))')
(w/'take2-hud.dsl').write_text(h)
