import numpy as np
from random import randint

def gogocalculate(input_vars):

    # total_level = 0
    damage_dice = []
    extra_attack = 0
    attack_mod = 5
    advantage = int(input_vars['adv'])
    crit_range = [20]
    spell_slots=[0,0,0,0,0,0]

    num_trials = int(input_vars['trials'])
    num_short_rests_per_long_rest = int(input_vars['SRs'])
    fight_rounds = int(input_vars['rounds'])
    sneak_attack_pct = int(input_vars['sneak'])

    barbarian = False
    bard = False
    fighter = False
    monk = False
    paladin = False
    ranger = False
    rogue = False
    warlock = False

    classes = [[input_vars['class_1'], int(input_vars['class_1_level'])]]
    total_level = int(input_vars['class_1_level'])
    if input_vars['class_2'] != "Choose class": 
        classes.append([input_vars['class_2'],int(input_vars['class_2_level'])])
        total_level += int(input_vars['class_2_level'])
    
    prof_bonus = int(np.floor((total_level-1)/4)+2)

    weapon_rarity = int(input_vars['weapon_rarity'])

    two_weapon_fighting = False #add ability mod to damage of second (offhand) attack ADDED
    archery = False #+2 to attack rolls with ranged weapons ADDED
    great_weapon_fighting = False #reroll 1s and 2s and must take new roll ADDED
    dueling = False #If melee in one hand and no other weapons, +2 to damage rolls with that weapon ADDED

    fs = input_vars['fighting_style']
    if fs == "Two-Weapon Fighting":
        two_weapon_fighting = True
    elif fs == "Archery":
        archery = True
    elif fs == "Great Weapon Fighting":
        great_weapon_fighting = True
    elif fs == "Dueling":
        dueling = True

    great_weapon_master = False #ADDED
    sharpshooter = False #ADDED
    elven_accuracy = False #if advantage, roll 3rd die ADDED
    polearm_master = False #bonus action attack with butt of GLAIVE, HALBERD, QSTAFF, SPEAR, for 1d4 ADDED
    crossbow_expert = False #ignore loading property of crossbows (extra attacks work)
            #if needed, code the "when you use Attack and attack with a 1H weapon, bonus action hand crossbow other hand"

    feats = input_vars.getlist('feats')
    for _ in feats:
        if _ == "Great Weapon Master":
            great_weapon_master = True
        elif _ == "Sharpshooter":
            sharpshooter = True
        elif _ == "Elven Accuracy":
            elven_accuracy = True
        elif _ == "Polearm Master":
            polearm_master = True
        elif _ == "Crossbow Expert":
            crossbow_expert = True
    
    dual_wield = True if int(input_vars.get('dualwield')) == 1 else False
    blessed = True if int(input_vars.get('bless')) == 1 else False
    weapon_choice = input_vars.get("weapon_chosen")
    
    if weapon_choice == "Greataxe":
        weapon_chosen = ["Greataxe",1,12,["Two-Handed","Heavy"]]
    elif weapon_choice == "Greatsword":
        weapon_chosen = ["Greatsword",2,6,["Two-Handed","Heavy"]]
    elif weapon_choice == "Hand Crossbow":
        weapon_chosen = ["Hand Crossbow",1,6,["Loading"]]
    elif weapon_choice == "Mace":
        weapon_chosen = ["Mace",1,6,[]]
    elif weapon_choice == "Rapier":
        weapon_chosen = ["Rapier",1,8,["Finesse"]]
    elif weapon_choice == "Shortsword":
        weapon_chosen = ["Shortsword",1,8,["Finesse","Light"]]
    elif weapon_choice == "Warhammer":
        weapon_chosen = ["Warhammer",1,10,["Two-Handed"]]
    elif weapon_choice == "Longbow":
        weapon_chosen = ["Longbow",1,8,["Two-Handed","Heavy"]]
    elif weapon_choice == "Glaive":
        weapon_chosen = ["Glaive",1,10,["Two-Handed","Heavy"]]

    #barbarian:
    reckless_attack = False
    brutal_critical = False
    rage_damage_mod = 0

    #bard
    bardic_inspiration = False
    master_flourish = False
    bi_dice = [5,6]

    #fighter
    combat_superiority = False
    sup_dice = [4,8]

    #monk
    ki = False
    martial_arts = False
    martial_arts_dice = 4
    flurry_of_blows = False

    #paladin
    smite = False
    imp_smite = False

    #ranger
    hunters_mark = False

    #rogue
    sneak_attack = False

    #warlock
    hexblade_curse = False

    for each_class in classes:
        if each_class[0] == "Barbarian":
            barbarian = True
            rage_damage_mod = int(np.floor((each_class[1]-2)/7)+2)
            if each_class[1] >= 5 and extra_attack == 0:
                extra_attack = 1
            if reckless_attack:
                advantage = 100
            if each_class[1] >= 9:
                brutal_critical = True
                brutal_critical_dice = [int(np.floor((each_class[1]-9)/4)+1),weapon_chosen[2]]
        
        elif each_class[0] == "Bard": #college of swords
            bard = True
            bardic_inspiration = True
            if each_class[1] >= 6 and extra_attack == 0:
                extra_attack = 1
                
            if each_class[1] >= 15:
                bi_dice[1] = 12
            elif each_class[1] >= 10:
                bi_dice[1] = 10
            elif each_class[1] >= 5:
                bi_dice[1] = 8
            
            if each_class[1] >= 14:
                master_flourish = True

            if not two_weapon_fighting and not dueling:
                print("Should prob choose a fighting style")
            
        #elif each_class[0] == "Cleric": #skipping cleric
        
        elif each_class[0] == "Fighter": #should work on its own
            fighter =  True
            if each_class[1] == 20:
                extra_attack = 3
            elif each_class[1] >= 11:
                extra_attack = 2
            elif each_class[1] >= 5:
                extra_attack = 1
            
            if each_class[2] == "Battle Master": #added superiority dice
                combat_superiority = True
                if each_class[1] >=15:
                    sup_dice[0] = 6
                elif each_class[1] >=7:
                    sup_dice[0] = 5
                if each_class[1] >= 18:
                    sup_dice[1] = 12
                elif each_class[1] >= 10:
                    sup_dice[1] = 10
            elif each_class[2] == "Champion": #should work automaticailly
                if each_class[1]>=15:
                    crit_range = [18,19,20]
                else:
                    crit_range = [19,20]

        elif each_class[0] == "Monk":
            monk = True
            martial_arts = True
            if each_class[1] > 1:
                ki = True
                ki_points = each_class[1]

            if each_class[1] >= 5 and extra_attack == 0:
                extra_attack = 1

            if each_class[1] >= 17:
                martial_arts_dice = 10
            elif each_class[1] >=11:
                martial_arts_dice = 8
            elif each_class[1] >=5:
                martial_arts_dice = 6

            if each_class[1] >= 2:
                flurry_of_blows = True

        elif each_class[0] == "Paladin":
            paladin = True
            if each_class[1] >= 5 and extra_attack == 0:
                extra_attack = 1
            if each_class[1] >= 11:
                imp_smite = True
                imp_smite_dice = [1,8]

            smite = True
            
            if int(np.floor((each_class[1]-1)/2))+2>4:
                spell_slots[1] = 4
            else: 
                spell_slots[1] = int(np.floor((each_class[1]-1)/2))+2
            if each_class[1] >= 5:
                if each_class[1] <= 6:
                    spell_slots[2] = 2
                else:
                    spell_slots[2] = 3
            if each_class[1] >= 9:
                if each_class[1] <= 10:
                    spell_slots[3] = 2
                else:
                    spell_slots[3] = 3
            if each_class[1] >= 13:
                if each_class[1] <= 14:
                    spell_slots[4] = 1
                elif each_class[1] <=16:
                    spell_slots[4] = 2
                else:
                    spell_slots[4] = 3
            if each_class[1] >= 17:
                if each_class[1] <= 18:
                    spell_slots[5] = 1
                else:
                    spell_slots[5] = 2

        elif each_class[0] == "Ranger":
            ranger = True
            if each_class[1] >= 5 and extra_attack == 0:
                extra_attack = 1
            hunters_mark = True
        
        elif each_class[0] == "Rogue":
            rogue = True
            # sneak_attack_pct = 97.5
            sneak_attack_dice = [int(np.ceil(each_class[1]/2)),6]
        
        elif each_class[0] == "Warlock":
            warlock = True
            hexblade_curse = True
            if each_class[1] >= 3:
                imp_pact_weapon = True
            if each_class[1] >= 12:
                lifedrinker =  True
            if each_class[1] >= 5:
                thirsting_blade = True
            #could not figure out a good way to code spell slots and spell levels so hard coded a list
            warlock_level = each_class[1]
            warlock_spell_slots = [0,1,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,4,4,4,4]
            warlock_spell_levels = [0,1,1,2,2,3,3,4,4,5,5,5,5,5,5,5,5,5,5,5,5]


###############################################################################
###               LOOPS START HERE                                         ####
###############################################################################

    list_DPRs = []

    for target_ac in range(15,26):
        total_damage_each_trial = []
        for i in range(num_trials):
            
            if paladin:
                smite_slots = []
                smite_slots += spell_slots[4]*[[5,8]]
                smite_slots += spell_slots[3]*[[4,8]]
                smite_slots += spell_slots[2]*[[3,8]]
                smite_slots += spell_slots[1]*[[2,8]]
                smite_slots += spell_slots[5]*[[5,8]]
                
            average_dpr_each_fight_in_long_rest = []
            for shortrests in range(num_short_rests_per_long_rest+1):
                #reset short rest limited specials AND SHORT REST WARLOCK SPELLSLOTS FFS
                #assuming short rest per fight of "fight_rounds" length
                #warlock spell slot reset:
                if paladin and warlock:
                    for _ in range(warlock_spell_slots[warlock_level]):
                        if warlock_spell_levels[warlock_level] == 5:
                            warlock_smite = [5,8]
                        else:
                            warlock_smite = [warlock_spell_levels[warlock_level]+1,8]
                        smite_slots.insert(0,warlock_smite)
                if bard:
                    BI_spent_count = 0
                if combat_superiority:
                    SD_spent_count = 0
                if flurry_of_blows:
                    ki_spent_count = 0

                total_damage_each_fight = []

                for j in range(fight_rounds):

                    attack_rolls = []
                    damage_dice = []
                    round_damage = 0
                    BI_spent = False
                    use_ki = False
                    already_sneak_attacked = False

                    adv_roll = randint(1,100)

                    if flurry_of_blows and ki_spent_count< ki_points:
                        use_ki = True
                        ki_spent_count += 1

                    if adv_roll <= advantage:
                        if elven_accuracy:
                            for k in range(extra_attack + 1 + 2*use_ki):
                                attack_rolls.append(max(randint(1,20),randint(1,20),randint(1,20)))
                        else:
                            for k in range(extra_attack + 1 + 2*use_ki):
                                attack_rolls.append(max(randint(1,20),randint(1,20)))

                    else:
                        for k in range(extra_attack + 1 + 2*use_ki):
                            attack_rolls.append(randint(1,20))

                    if rogue:
                        if randint(1,100) <= sneak_attack_pct:
                            sneak_attack = True
                        else:
                            sneak_attack = False
                    
                    #base dice first then adjust for crit?

                    # damage_dice_base += [weapon_chosen[2]]
                    # damage_dice_base += imp_smite*[8]
                    #     #if smite add here
                    # damage_dice_base += hunters_mark*[8]

                    # for attack_roll in attack_rolls:
                    #     #if crit:
                    #     if attack_roll in crit_range:
                    #         damage_dice_test = damage_dice_base*2
                    #         if smite and len(smite_slots)>0:
                    #             spend_smite = smite_slots.pop(0)
                    #             damage_dice_test += 2*spend_smite[0]*[spend_smite[1]]
                    #         if brutal_critical:
                    #             damage_dice_test += brutal_critical_dice[0]*[brutal_critical_dice[1]]
                    #         if sneak_attack and not already_sneak_attacked:
                    #             damage_dice_test += 2* sneak_attack_dice*[6]
                    #             already_sneak_attacked = True
                    #         if bardic_inspiration and BI_spent_count < bi_dice[0] and not BI_spent:
                    #             damage_dice_test += 2*[bi_dice[1]]
                    #             BI_spent = True
                    #             BI_spent_count += 1
                    #         elif bardic_inspiration and BI_spent_count >= bi_dice[0] and not BI_spent and master_flourish:
                    #             damage_dice += 2* [6]
                    #             BI_spent = True
                    #             BI_spent_count += 1
                    #if using bardic inspiration
                    #elif master's flourish bard feature
                    #if crit
                        #double dice, add brutal critical


                    for attack_roll in attack_rolls:
                        #print(attack_roll + prof_bonus + 2*archery + attack_mod - 5*great_weapon_master - 5* sharpshooter + weapon_rarity)
                        #if crit
                        if attack_roll in crit_range:
                            #monk martial
                            if martial_arts:
                                damage_dice += 2*[martial_arts_dice]
                            else:
                                if imp_smite:
                                    damage_dice += 2*[imp_smite_dice[1]]
                                damage_dice += 2*[weapon_chosen[2]]

                                if smite and len(smite_slots)>0:
                                    spend_smite = smite_slots.pop(0)
                                    damage_dice += 2*spend_smite[0]*[spend_smite[1]]

                                if hunters_mark:
                                    damage_dice += 2*[8]
                                #Barbarian Brutal Critical 
                                if brutal_critical:
                                    damage_dice += brutal_critical_dice[0]*[brutal_critical_dice[1]]
                                    #print("Brutal")
                                    #print(damage_dice)

                                if sneak_attack and not already_sneak_attacked:
                                    damage_dice += 2*sneak_attack_dice[0]*[sneak_attack_dice[1]]
                                    already_sneak_attacked = True

                                #Bard Flourish!
                                if bardic_inspiration and BI_spent_count < bi_dice[0] and not BI_spent:
                                    damage_dice += 2* [bi_dice[1]]
                                    BI_spent = True
                                    BI_spent_count += 1
                                #master's flourish
                                elif bardic_inspiration and BI_spent_count >= bi_dice[0] and not BI_spent and master_flourish:
                                    damage_dice += 2* [6]
                                    BI_spent = True
                                    BI_spent_count += 1

                                #Battlemaster Combat Superiority!
                                if combat_superiority and SD_spent_count < sup_dice[0]:
                                    damage_dice += 2* [sup_dice[1]]
                                    SD_spent_count +=1

                            round_damage += (10*great_weapon_master + 10* sharpshooter + attack_mod + 
                                            hexblade_curse*prof_bonus + rage_damage_mod + weapon_rarity +
                                            2*dueling)

                        elif (attack_roll + prof_bonus + 2*archery + attack_mod - 5*great_weapon_master 
                            - 5* sharpshooter + weapon_rarity) + blessed*randint(1,4) >= target_ac:
                            if martial_arts:
                                damage_dice.append(martial_arts_dice)
                            else:
                                if imp_smite:
                                    damage_dice += [imp_smite_dice[1]]
                                damage_dice += [weapon_chosen[2]]

                                if smite and len(smite_slots)>0 and randint(1,2)>=2:
                                    spend_smite = smite_slots.pop(0)
                                    #print(spend_smite)
                                    damage_dice += spend_smite[0]*[spend_smite[1]]

                                if hunters_mark:
                                    damage_dice += [8]                    

                                if sneak_attack and not already_sneak_attacked:
                                    damage_dice += sneak_attack_dice[0]*[sneak_attack_dice[1]]                    
                                    already_sneak_attacked = True

                                #Bard Flourish!
                                if bardic_inspiration and BI_spent_count < bi_dice[0] and not BI_spent:
                                    damage_dice.append(bi_dice[1])
                                    BI_spent = True
                                    BI_spent_count += 1
                                #master's flourish
                                elif bardic_inspiration and BI_spent_count >= bi_dice[0] and not BI_spent and master_flourish:
                                    damage_dice.append(6)
                                    BI_spent = True
                                    BI_spent_count += 1

                                if combat_superiority and SD_spent_count < sup_dice[0]:
                                    damage_dice += [sup_dice[1]]
                                    SD_spent_count +=1

                            round_damage += (10*great_weapon_master + 10* sharpshooter + attack_mod + 
                                            hexblade_curse*prof_bonus + rage_damage_mod + weapon_rarity +
                                            2*dueling)

                    #polearm master 1d4 attack with full modifiers
                    if polearm_master:
                        if adv_roll <= advantage:
                            if elven_accuracy:
                                pam_attack = max(randint(1,20),randint(1,20),randint(1,20))
                            else:
                                pam_attack = max(randint(1,20),randint(1,20))
                        else:
                            pam_attack = randint(1,20)

                        if pam_attack in crit_range:
                            damage_dice += 2*[4]
                            if imp_smite:
                                damage_dice += 2*[imp_smite_dice[1]]
                            if smite and len(smite_slots)>0:
                                spend_smite = smite_slots.pop(0)
                                damage_dice += 2*spend_smite[0]*[spend_smite[1]]
                            round_damage += (10*great_weapon_master + 10* sharpshooter + attack_mod + 
                                            hexblade_curse*prof_bonus + rage_damage_mod + weapon_rarity + 
                                            2* dueling)       
                        elif (pam_attack + prof_bonus + 2*archery + attack_mod - 5*great_weapon_master 
                            - 5* sharpshooter + weapon_rarity) + blessed*randint(1,4) >= target_ac:
                            damage_dice += [4]
                            if imp_smite:
                                damage_dice += [imp_smite_dice[1]]
                            if smite and len(smite_slots)>0 and randint(1,2)>=2:
                                spend_smite = smite_slots.pop(0)
                                damage_dice += spend_smite[0]*[spend_smite[1]]
                            round_damage += (10*great_weapon_master + 10* sharpshooter + attack_mod + 
                                            hexblade_curse*prof_bonus + rage_damage_mod + weapon_rarity + 
                                            2*dueling)


                    #two weapon attacking!
                    if dual_wield:
                        if adv_roll <= advantage:
                            if elven_accuracy:
                                off_attack = max(randint(1,20),randint(1,20),randint(1,20))
                            else:
                                off_attack = max(randint(1,20),randint(1,20))
                        else:
                            off_attack = randint(1,20)

                        if off_attack in crit_range:
                            damage_dice += 2*[weapon_chosen[2]]
                            if sneak_attack and not already_sneak_attacked:
                                damage_dice += 2*sneak_attack_dice[0]*[sneak_attack_dice[1]]
                                already_sneak_attacked = True
                            round_damage += (10*great_weapon_master + 10* sharpshooter + 
                                            hexblade_curse*prof_bonus + rage_damage_mod + weapon_rarity)       
                            #ability mod only added with fighting style
                            if two_weapon_fighting:
                                round_damage += attack_mod
                        elif (off_attack + prof_bonus + 2*archery + attack_mod - 5*great_weapon_master 
                            - 5* sharpshooter + weapon_rarity) + blessed*randint(1,4) >= target_ac:
                            damage_dice += [weapon_chosen[2]]
                            if sneak_attack and not already_sneak_attacked:
                                damage_dice += sneak_attack_dice[0]*[sneak_attack_dice[1]]
                                already_sneak_attacked = True
                            round_damage += (10*great_weapon_master + 10* sharpshooter + 
                                            hexblade_curse*prof_bonus + rage_damage_mod + weapon_rarity)       
                            #ability mod only added with fighting style
                            if two_weapon_fighting:
                                round_damage += attack_mod

                    for each_die in damage_dice:
                        each_dmg_die_roll = randint(1,each_die)
                        if great_weapon_fighting:
                            if each_dmg_die_roll <= 2:
                                each_dmg_die_roll = randint(1,each_die)
                        round_damage += each_dmg_die_roll

                    total_damage_each_fight.append(round_damage)
                average_dpr_each_fight_in_long_rest.append(np.mean(total_damage_each_fight))
            total_damage_each_trial.append(np.mean(average_dpr_each_fight_in_long_rest))
                #print(len(total_damage_each_trial))
        list_DPRs.append(np.mean(total_damage_each_trial))
    
    if len(classes) == 1:
        desc_string = f'{classes[0][0]} {classes[0][1]}'
    else:
        desc_string = f'{classes[0][0]} {classes[0][1]} / {classes[1][0]} {classes[1][1]}'

    desc_string += f' {weapon_chosen[0]}'
    if weapon_rarity > 0:
        desc_string += f' +{weapon_rarity}'

    desc_string += f'{dual_wield*" Dual Wield"}'
        
    desc_string += f'{sharpshooter*" SS"}'
    desc_string += f'{great_weapon_master*" GWM"}'
    desc_string += f'{crossbow_expert*" CBX"}'
    desc_string += f'{polearm_master*" PAM"}'
    desc_string += f'{elven_accuracy*" Elven Accuracy"}'

    desc_string += f'{dueling*" Dueling"}'
    desc_string += f'{great_weapon_fighting*" GWF"}'
    desc_string += f'{two_weapon_fighting*" TWF"}'
    desc_string += f'{archery*" Archery"}'

    desc_string += f' advantage {advantage}%'

    desc_string += f' {num_short_rests_per_long_rest} Short Rests between fights of {fight_rounds} rounds'
    #print(desc_string)
    list_DPRs.insert(0,desc_string)
    
    return list_DPRs