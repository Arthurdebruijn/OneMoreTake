import pathlib,json
exec(pathlib.Path('work/build_take2_dsl.py').read_text().split("parse='",1)[0])
s=json.loads(pathlib.Path('work/lunge-mobile-before.json').read_text(encoding='utf-8-sig'))['returnValue']['dsl']
a=s.index('(event `self.ReceiveTick`');b=s.index('\n\n',a);tick=s[a:b]
tick=tick.replace('(if (or (`self.HitStaggered`) (`self.LungePaused`))','(if (`self.HitStaggered`)')
tick=tick.replace('(not (`self.IsAttacking`))','(or (not (`self.IsAttacking`)) (`self.EnemyAttackInterrupted`))')
tick=tick.replace(' (not (`self.LungePaused`))','')
tick=tick.replace('(if (`self.HasAttackTurn`)','(if (and (`self.HasAttackTurn`) (not (`self.LungePaused`)) (not (`self.IsAttacking`)))')
# A canceled swing keeps its timer alive, but no longer freezes locomotion.
tick=tick.replace('(if (not (`self.HasAttackTurn`))\n        (`self.AddMovementInput`','(if (or (not (`self.HasAttackTurn`)) (`self.LungePaused`) (`self.EnemyAttackInterrupted`))\n        (`self.AddMovementInput`')
s=s[:a]+tick+s[b:]
a=s.index('(event `PauseForPlayerLunge`');b=s.index('\n\n',a);pause=s[a:b]
pause=pause.replace('    (`MovementComponent.StopMovementImmediately` (`self.CharacterMovement`))\n','')
s=s[:a]+pause+s[b:]
pathlib.Path('work/lunge-mobile.dsl').write_text(s)
