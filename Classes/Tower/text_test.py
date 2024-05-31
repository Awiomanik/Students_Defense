from Tower_Classes import Tower, Tower_Manager # type: ignore
Tower_Manager.reset()
enemy1_hp = 10
enemy1_coord = [1,0]
enemy2_hp = 5
enemy2_coord = [0,0]
enemy_list=[[enemy1_hp,enemy1_coord],[enemy2_hp,enemy2_coord]]

default_tower = Tower(3,1,1,1,True,False,"../gfx/tower_placeholder.png","../gfx/shot_placeholder.png")
tower1 = Tower_Manager(default_tower,[5,-1],enemy_list)
def text_test(tower : Tower_Manager,enemies):
    lst1=[]
    lst2=[]
    for x in range(10):
        lst1.append('-')
        lst2.append('-')
        #print(Tower_Manager.towers)
    while enemies:
        for enemy in enemies:
            print('distance:',((enemy[1][0]-tower.coord[0])**2 + (enemy[1][1]-tower.coord[1])**2)**0.5)
            print('range',tower.tower_type.range)
        for x in range(len(lst1)):
            places_1_row = [enemy[1][0] for enemy in enemies]
            places_2_row = [test_tower[1][0] for test_tower in Tower_Manager.towers]
            #print(places_2_row)
            #print(places_1_row)
            if x in places_1_row:
                lst1[x] = '*'
            else:
                lst1[x] = '-'
            if x in places_2_row:
                lst2[x] = 'O'
            else:
                lst2[x] = '-'
        print(lst1)
        print(lst2)
        tower.attack()
        for enemy in enemies:
            print('hp:',enemy[0])
        if len(enemies)>0:
            for enemy in enemies:
                enemy[1][0]+=1
            
        for enemy in enemies:
            if enemy[1][0]>10:
                return
            if len(enemies)==0:
                return
text_test(tower1,enemy_list)