import pathlib,json
exec(pathlib.Path('work/build_take2_dsl.py').read_text().split("parse='",1)[0])
s=json.loads(pathlib.Path('work/dodge-before.json').read_text(encoding='utf-8-sig'))['returnValue']['dsl']
s=s.replace('(event `self.ReceiveBeginPlay`','(event `self.ReceiveBeginPlay`\n  (set `self.DodgeReady` true)',1)
s=s.replace('(not (`self.IsAttacking`)) (not (`self.IsDead`)) (not (`self.SceneLocked`))','(not (`self.IsAttacking`)) (not (`self.IsDodging`)) (not (`self.IsDead`)) (not (`self.SceneLocked`))',1)
s=s.replace('(set `self.IsAttacking` true)','(set `self.IsAttacking` true)\n    (if (not (`self.IsEnemy`)) (`self.FindMeleeTarget`))',1)
s=s.replace('(set `self.IsAttacking` false)\n    (if (`self.IsEnemy`)', '(set `self.IsAttacking` false)\n    (set `self.MeleeTarget` null)\n    (if (`self.IsEnemy`)',1)
s=s.replace('(if (and (`self.HasGun`) (`self.FireHeld`) (`self.GunReady`))','(if (and (`self.HasGun`) (`self.FireHeld`) (`self.GunReady`) (not (`self.IsDodging`)))',1)
tick=s.index('(event `self.ReceiveTick`');start=s.index('  (if ',tick)
s=s[:start]+'''  (if (`self.IsDodging`) (`self.TickDodge` DeltaSeconds))
  (if (and (not (`self.IsEnemy`)) (`self.IsAttacking`) (not (`self.IsDead`)) (not (`self.SceneLocked`))) (`self.TickMeleeAssist` DeltaSeconds))
'''+s[start:]
# Dodge replaces every jump input route, with no jump calls left.
s=replace_form(s,'(event `EnhancedInput|/Game/Input/Actions/IA_Jump`','''(event `EnhancedInput|/Game/Input/Actions/IA_Jump`
 (params (ActionValue :type Boolean) (ElapsedSeconds :type "Float (double-precision)") (TriggeredSeconds :type "Float (double-precision)") (InputAction :type "InputAction Object Reference" :default "/Game/Input/Actions/IA_Jump.IA_Jump"))
 (:`Started` (`self.Dodge`)))''')
s=replace_form(s,'(event `self.Touch Jump Start`','(event `self.Touch Jump Start` (`self.Dodge`))')
s=replace_form(s,'(event `self.Touch Jump End`','(event `self.Touch Jump End`)')
# Leave movement responsive immediately after the short dash ends.
pos=s.index('(fn `Move`');part=s[pos:];part=part.replace('(not (`self.IsAttacking`))','(not (`self.IsAttacking`)) (not (`self.IsDodging`))',1);s=s[:pos]+part
# Gate the whole damage response, not just the health number.
start=s.index('(event `self.ReceiveAnyDamage`');end=s.index('\n\n',start);part=s[start:end];body=part.index('\n  (if ');part=part[:body]+'\n  (if (not (`self.IsDodging`))'+part[body:-1]+'))';s=s[:start]+part+s[end:]
s+='''
(event `Dodge`
 (if (and (`self.DodgeReady`) (not (`self.IsDodging`)) (not (`self.IsAttacking`)) (not (`self.IsDead`)) (not (`self.SceneLocked`)) (not (`self.IsEnemy`)))
  (set `self.DodgeReady` false)
  (set `self.IsDodging` true)
  (set `self.MeleeTarget` null)
  (if (and (> (`KismetMathLibrary.VSize` (`self.GetVelocity`)) 10.0) (> (`KismetMathLibrary.VSize` (`self.GetLastMovementInputVector`)) 0.1))
   (set `self.DodgeDirection` (`KismetMathLibrary.Normal` (`self.GetLastMovementInputVector`)))
   (else (set `self.DodgeDirection` (`self.GetActorForwardVector`))))
  (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`))
  (`KismetSystemLibrary.Delay` 0.18)
  (set `self.IsDodging` false)
  (`KismetSystemLibrary.Delay` 0.47)
  (set `self.DodgeReady` true)))
(event `TickDodge`
 (params (DeltaSeconds :type "Float (single-precision)"))
 (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`))
 (`self.K2_SetActorLocation` (+ (`self.K2_GetActorLocation`) (* (`self.DodgeDirection`) (* 1450.0 DeltaSeconds))) true false))
(event `FindMeleeTarget`
 (set `self.MeleeTarget` null)
 (set `self.MeleeTargetDistance` 370.0)
 (for enemy (`GameplayStatics.GetAllActorsOfClass` "/Game/OneMoreTake/Blueprints/BP_Guard.BP_Guard_C")
  (bind guard (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` enemy))
  (if (and (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` guard)) (< (`self.GetDistanceTo` guard) (`self.MeleeTargetDistance`)))
   (if (> (`KismetMathLibrary.Dot_VectorVector` (`self.GetActorForwardVector`) (`KismetMathLibrary.Normal` (- (`self.K2_GetActorLocation` guard) (`self.K2_GetActorLocation`)))) 0.55)
    (set `self.MeleeTarget` guard)
    (set `self.MeleeTargetDistance` (`self.GetDistanceTo` guard))))))
(event `TickMeleeAssist`
 (params (DeltaSeconds :type "Float (single-precision)"))
 (if (`KismetSystemLibrary.IsValid` (`self.MeleeTarget`))
  (bind guard (cast `/Game/OneMoreTake/Blueprints/BP_KnightPlayer` (`self.MeleeTarget`)))
  (if (and (not (`/Game/OneMoreTake/Blueprints/BP_KnightPlayer.IsDead` guard)) (< (`self.GetDistanceTo` guard) 450.0))
   (bind enemy (`self.K2_GetActorLocation` guard))
   (bind flat (`KismetMathLibrary.MakeVector` (.x enemy) (.y enemy) (.z (`self.K2_GetActorLocation`))))
   (bind direction (`KismetMathLibrary.Normal` (- flat (`self.K2_GetActorLocation`))))
   (`self.K2_SetActorRotation` (`KismetMathLibrary.FindLookAtRotation` (`self.K2_GetActorLocation`) flat))
   (if (> (`self.GetDistanceTo` guard) 130.0)
    (`self.K2_SetActorLocation` (`KismetMathLibrary.VInterpTo` (`self.K2_GetActorLocation`) (- flat (* direction 130.0)) DeltaSeconds 18.0) true false))
   (else (set `self.MeleeTarget` null)))))
'''
pathlib.Path('work/dodge.dsl').write_text(s)
