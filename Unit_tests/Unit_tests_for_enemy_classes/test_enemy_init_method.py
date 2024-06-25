import hypothesis.strategies as st
from hypothesis import given
from Enemy import Enemy
import unittest

@given(st.sampled_from(list(Enemy.enemy_types.keys())))
def test_enemy_init(enemy_type):
    enemy = Enemy(enemy_type)
    result1 = enemy.life
    result2 = enemy.speed
    assert result1 == Enemy.enemy_types[enemy_type]['hp']
    assert result2 == Enemy.enemy_types[enemy_type]['speed']


if __name__ == '__main__':
    unittest.main()