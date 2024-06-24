import hypothesis.strategies as st
from hypothesis import given
from Enemy import Enemy
import unittest

@given(st.sampled_from(list(Enemy.enemy_types.keys())))
def test_enemy_str(enemy_type):
        enemy = Enemy(enemy_type)
        expected_str = f"Enemy(life={Enemy.enemy_types[enemy_type]['hp']}, speed={Enemy.enemy_types[enemy_type]['speed']})"
        assert expected_str == str(enemy)

if __name__ == '__main__':
    unittest.main()