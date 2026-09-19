from qa_workflow_lab.harness import run_check

def test_single_result():
    result = run_check('single_result')
    assert result['actual'] == 1

def test_stale_equip():
    result = run_check('stale_equip')
    assert result['actual'] == 'carbine'

def test_single_upgrade():
    result = run_check('single_upgrade')
    assert result['actual'] == 15

def test_encounter_target():
    result = run_check('encounter_target')
    assert result['actual'] == False

def test_current_recovery():
    result = run_check('current_recovery')
    assert result['actual'] == 'carbine'

def test_cleanup():
    result = run_check('cleanup')
    assert result['actual'] == 1
