from math import ceil

INDY_DRONE_NAME_PRESET = "db_indy_crew_{}{}_drone"
INDY_DRONE_NAME_PRESET_AUTO = "db_indy_crew_{}{}_drone_auto"

DRONE_BAY_HEAL_EFFECT_PRESET = """<statBoost name="healAmount"> <!-- Drones heal regularly in the drone room -->
                <boostType>SET</boostType>
                <amount>{}</amount>
                <shipTarget>ORIGINAL_SHIP</shipTarget>
                <crewTarget>SELF</crewTarget>
                <maxStacks>1</maxStacks>
                <priority>0</priority>
                <whiteList>
                    <{}/>
                </whiteList>
                <systemRoomTarget>ALL</systemRoomTarget>
                <systemPowerDependency>
                    <drones/>
                </systemPowerDependency>
                <systemList>
                    <drones/>
                </systemList>
                <systemPowerScaling>
                    <noSys>0</noSys>
                    <hackedSys>0</hackedSys>
                    <noPwr>1</noPwr>
                    <onePwr>1</onePwr>
                </systemPowerScaling>
            </statBoost>"""

MEDBAY_HEAL_EFFECT_PRESET = """<statBoost name="healSpeed"> <!-- Drones heal at reduced speed in the medbay -->
                <boostType>SET</boostType>
                <amount>{}</amount>
                <shipTarget>ORIGINAL_SHIP</shipTarget>
                <crewTarget>SELF</crewTarget>
                <maxStacks>1</maxStacks>
                <priority>0</priority>
                <whiteList>
                    <{}/>
                </whiteList>
                <systemRoomTarget>ALL</systemRoomTarget>
                <systemList>
                    <medbay/>
                </systemList>
            </statBoost>"""

RECON_DAMAGE_TAKEN_MULTIPLIER_ENEMY_SHIP_EFFECT1 = """<statBoost name="damageTakenMultiplier"> <!-- Increase damage multiplier to 0.5 on enemy ship -->
                <boostType>SET</boostType>
                <amount>0.5</amount>
                <shipTarget>ENEMY_SHIP</shipTarget>
                <crewTarget>SELF</crewTarget>
                <priority>0</priority>
                <whiteList>
                    <db_indy_crew_recon_drone/>
                </whiteList>
            </statBoost>"""

DOCTOR_BURST_HEAL_EFFECT1 = """<cooldown>10</cooldown>
			<jumpCooldown>full</jumpCooldown>
			<powerSounds>
				<powerSound>healBomb</powerSound>
			</powerSounds>
			<activateWhenReady enemiesOnly="false">true</activateWhenReady>
			<friendlyFire>true</friendlyFire>
			<shipFriendlyFire>true</shipFriendlyFire>
			<buttonText>HEAL</buttonText>
            <tooltip>Automatic: activates an ion pulse</tooltip>
			<tooltip>[COOLDOWN:10s] Automatic:
				Heal all other friendly crew in the room for 72 HP and heal self for 12 HP.</tooltip>
			<cooldownColor r="255" g="78" b="69" />
			<effectAnim>explosion_big1_heal</effectAnim>
			<crewHealth>72</crewHealth>
			<selfHealth>12</selfHealth>"""

DOCTOR_BOOST_STAT_BOOST_EFFECT1 = """<statBoost name="repairSpeed">
                <boostType>MULT</boostType>
                <amount>1.5</amount>
                <shipTarget>CURRENT_ROOM</shipTarget>
                <crewTarget>ALLIES</crewTarget>
                <droneTarget>CREW</droneTarget>
                <affectsSelf>true</affectsSelf>
            </statBoost>
            <statBoost name="damageMultiplier">
                <boostType>MULT</boostType>
                <amount>1.25</amount>
                <shipTarget>CURRENT_ROOM</shipTarget>
                <crewTarget>ALLIES</crewTarget>
                <droneTarget>CREW</droneTarget>
                <affectsSelf>true</affectsSelf>
            </statBoost>"""

ION_EFFECT1 = """<cooldown>12</cooldown>
            <jumpCooldown>full</jumpCooldown>
            <powerSounds>
                <powerSound>ionHit1</powerSound>
            </powerSounds>
            <req>
                <systemInRoom />
            </req>
            <friendlyFire>false</friendlyFire>
            <shipFriendlyFire>false</shipFriendlyFire>  
            <ion>3</ion>
            <stun>6</stun>
            <animFrame>-1</animFrame>
            <buttonText>ION</buttonText>
            <tooltip>Automatic: activates an ion pulse</tooltip>
            <cooldownColor r="0" g="235" b="255" />
            <effectAnim>explosion_big1_ion</effectAnim>
            <activateWhenReady enemiesOnly="false">true</activateWhenReady>
            <temporaryEffect>
                <duration>2</duration>
                <cooldownColor r="10" g="255" b="255" />
                <!--<controllable>false</controllable>-->
                <canFight>false</canFight>
                <canRepair>false</canRepair>
                <canSabotage>false</canSabotage>
                <canMan>false</canMan>
                <moveSpeedMultiplier>0</moveSpeedMultiplier>
            </temporaryEffect>"""

ION_EFFECT2 = """<cooldown>12</cooldown>
            <jumpCooldown>full</jumpCooldown>
            <powerSounds>
                <powerSound>ionHit1</powerSound>
            </powerSounds>
            <req>
                <systemInRoom />
            </req>
            <friendlyFire>false</friendlyFire>
            <shipFriendlyFire>false</shipFriendlyFire>  
            <ion>4</ion>
            <stun>8</stun>
            <animFrame>-1</animFrame>
            <buttonText>ION</buttonText>
            <tooltip>Automatic: activates an ion pulse</tooltip>
            <cooldownColor r="0" g="235" b="255" />
            <effectAnim>explosion_big1_ion</effectAnim>
            <activateWhenReady enemiesOnly="false">true</activateWhenReady>
            <temporaryEffect>
                <duration>2</duration>
                <cooldownColor r="10" g="255" b="255" />
                <canFight>false</canFight>
                <canRepair>false</canRepair>
                <canSabotage>false</canSabotage>
                <canMan>false</canMan>
                <moveSpeedMultiplier>0</moveSpeedMultiplier>
            </temporaryEffect>"""

EFFECT_UPGRADES = {ION_EFFECT1: ION_EFFECT2}


class IndyDrone:
    def __init__(
        self,
        name,
        mark,
        description,
        cost,
        fuel_cost,
        drone_cost,
        title,
        short,
        rarity,
        power_list,
        anim_base,
        anim_sheet,
        bp=2,
        max_health=100,
        crew_slots=0.5,
        can_fight=False,
        can_sabotage=False,
        can_man=False,
        can_repair=True,
        no_clone=True,
        heal_speed=1.0,
        can_burn=True,
        can_suffocate=False,
        repair_speed=2.5,
        move_speed_multiplier=1.2,
        stun_multiplier=0.25,
        fire_damage_multiplier=0.35,
        heal_crew_amount=None,
        damage_taken_multiplier=1.0,
        damage_taken_multiplier_enemy_ship_xml=None,
        bonus_power=None,
        resists_mind_control=True,
        is_telepathic=False,
        controllable=True,
        drone_ai=None,
        death_sounds=["sysExplosion"],
        death_effect=None,
        shooting_sounds=None,
        is_anaerobic=False,
        oxygen_change_speed=None,
        drone_bay_heal_amount=1.0,
        medbay_heal_speed=0.1,
        extra_stat_boost_xml="",
        default_skill_level=0,
        power_effect_xml=None,
    ):
        self.name = (
            INDY_DRONE_NAME_PRESET.format(name, mark)
            if controllable
            else INDY_DRONE_NAME_PRESET_AUTO.format(name, mark)
        )
        self.mark = mark
        self.description = description
        self.cost = cost
        self.fuel_cost = fuel_cost
        self.drone_cost = drone_cost
        self.title = title
        self.short = short
        self.rarity = rarity
        self.power_list = power_list
        self.anim_base = anim_base
        self.anim_sheet = anim_sheet
        self.bp = bp
        self.max_health = max_health
        self.power_list.append(
            f"{max_health} hp, {move_speed_multiplier}x movement_speed"
        )
        self.crew_slots = crew_slots
        crew_slot_message = (
            f"Takes up {self.crew_slots} crew slot{'s' if self.crew_slots != 1 else ''}"
        )
        self.description += f" {crew_slot_message}."
        self.power_list.append(crew_slot_message)
        self.can_fight = can_fight
        self.can_sabotage = can_sabotage
        self.can_man = can_man
        self.power_list.append(
            f"Can man systems at the lvl{self.default_skill_level} skill level"
        )
        self.can_repair = can_repair
        self.no_clone = no_clone
        self.heal_speed = heal_speed
        self.can_burn = can_burn
        self.can_suffocate = can_suffocate
        self.repair_speed = repair_speed
        self.move_speed_multiplier = move_speed_multiplier
        self.stun_multiplier = stun_multiplier
        self.power_list.append(f"{self.stun_multiplier}x stun multiplier")
        self.fire_damage_multiplier = fire_damage_multiplier
        self.power_list.append(f"{self.fire_damage_multiplier}x damage from fires")
        self.heal_crew_amount = heal_crew_amount
        if heal_crew_amount is not None:
            self.power_list.append(
                f"Heals ally crew in the same room for {heal_crew_amount} HP/s"
            )
        self.damage_taken_multiplier = damage_taken_multiplier
        self.damage_taken_multiplier_enemy_ship_xml = (
            damage_taken_multiplier_enemy_ship_xml
        )
        self.bonus_power = bonus_power
        if bonus_power is not None and bonus_power > 0:
            self.power_list.append(
                f"Provides {bonus_power} extra power in the current room"
            )
        self.resists_mind_control = resists_mind_control
        self.is_telepathic = is_telepathic
        self.controllable = controllable
        if controllable:
            self.power_list.append("Can be controlled")
        else:
            self.power_list.append("Can't be controlled")
        self.drone_ai = drone_ai
        self.death_sounds = death_sounds
        self.death_effect = death_effect
        self.shooting_sounds = shooting_sounds
        self.is_anaerobic = is_anaerobic
        self.oxygen_change_speed = oxygen_change_speed
        self.drone_bay_heal_amount = drone_bay_heal_amount
        self.medbay_heal_speed = medbay_heal_speed
        self.extra_stat_boost_xml = extra_stat_boost_xml
        self.default_skill_level = default_skill_level
        self.power_effect_xml = power_effect_xml

    def generate_blueprint_xml(self):
        powers_xml = "\n".join(f"<power>{power}</power>" for power in self.power_list)
        xml = f"""<crewBlueprint name="{self.name}">
            <description>{self.description}</description>
            <cost>{self.cost}</cost>
            <bp>{self.bp}</bp>
            <title>{self.title} {self.mark} Drone</title>
            <short>{self.short} {self.mark}</short>
            <rarity>{self.rarity}</rarity>
            <powerList>
            {powers_xml}
            </powerList>
        </crewBlueprint>"""

        return xml

    def generate_hyperspace_xml(self):
        anim_base_xml = (
            f"""<animBase>{self.anim_base}</animBase>""" if self.anim_base else ""
        )
        repair_speed_xml = (
            f"""<repairSpeed>{self.repair_speed}</repairSpeed>"""
            if self.can_repair
            else ""
        )
        drone_ai_instructions_xml = (
            "\n".join(f"<{instruction} />" for instruction in self.drone_ai)
            if self.drone_ai
            else ""
        )
        drone_ai_xml = (
            f"""<droneAI>
            {drone_ai_instructions_xml}
        </droneAI>"""
            if self.drone_ai
            else ""
        )
        death_sounds_inner_xml = (
            "\n".join(
                f"<deathSound>{sound}</deathSound>" for sound in self.death_sounds
            )
            if self.death_sounds
            else ""
        )
        death_sounds_xml = (
            f"""<deathSounds>
            {death_sounds_inner_xml}
        </deathSounds>"""
            if death_sounds_inner_xml
            else ""
        )
        death_effect_inner_xml = (
            "\n".join(
                f"<{key}>{value}</{key}>" for key, value in self.death_effect.items()
            )
            if self.death_effect
            else ""
        )
        death_effect_xml = (
            f"""<deathEffect>
            {death_effect_inner_xml}
        </deathEffect>"""
            if death_effect_inner_xml
            else ""
        )
        dronebay_heal_stat_boost_xml = DRONE_BAY_HEAL_EFFECT_PRESET.format(
            self.drone_bay_heal_amount, self.name
        )
        medbay_heal_stat_boost_xml = MEDBAY_HEAL_EFFECT_PRESET.format(
            self.medbay_heal_speed, self.name
        )
        damage_taken_multiplier_enemy_ship_xml = (
            self.damage_taken_multiplier_enemy_ship_xml
            if self.damage_taken_multiplier_enemy_ship_xml
            else ""
        )
        shooting_sounds_inner_xml = (
            "\n".join(
                f"<shootingSound>{sound}</shootingSound>"
                for sound in self.shooting_sounds
            )
            if self.shooting_sounds
            else ""
        )
        shooting_sounds_xml = (
            f"""<shootingSounds>
            {shooting_sounds_inner_xml}
        </shootingSounds>"""
            if shooting_sounds_inner_xml
            else ""
        )
        oxygen_change_speed_xml = (
            f"""<oxygenChangeSpeed>{self.oxygen_change_speed}</oxygenChangeSpeed>"""
            if self.oxygen_change_speed
            else ""
        )

        extra_stat_boost_xml = (
            self.extra_stat_boost_xml if self.extra_stat_boost_xml else ""
        )

        passive_stats_array = [
            dronebay_heal_stat_boost_xml,
            medbay_heal_stat_boost_xml,
            damage_taken_multiplier_enemy_ship_xml,
        ]
        if extra_stat_boost_xml:
            passive_stats_array.append(extra_stat_boost_xml)
        passive_stat_boosts_inner_xml = "\n".join(passive_stats_array)
        passive_stat_boosts_xml = f"""<passiveStatBoosts>
            {passive_stat_boosts_inner_xml}
        </passiveStatBoosts>"""

        xml = f"""<mod:findLike type="crew">
                    <mod-append:race name="{self.name}" /> 
                        {anim_base_xml}
                        <animSheet>{self.anim_sheet}</animSheet>
                        <maxHealth>{self.max_health}</maxHealth>
                        <crewSlots>{self.crew_slots}</crewSlots>
                        <canFight>{str(self.can_fight).lower()}</canFight>
                        <canSabotage>{str(self.can_sabotage).lower()}</canSabotage>
                        <canMan>{str(self.can_man).lower()}</canMan>
                        <canRepair>{str(self.can_repair).lower()}</canRepair>
                        <noClone>{str(self.no_clone).lower()}</noClone>
                        <healSpeed>{self.heal_speed}</healSpeed>
                        <canBurn>{str(self.can_burn).lower()}</canBurn>
                        <canSuffocate>{str(self.can_suffocate).lower()}</canSuffocate>
                        {repair_speed_xml}
                        <moveSpeedMultiplier>{self.move_speed_multiplier}</moveSpeedMultiplier>
                        <stunMultiplier>{self.stun_multiplier}</stunMultiplier>
                        <fireDamageMultiplier>{self.fire_damage_multiplier}</fireDamageMultiplier>
                        <damageTakenMultiplier>{self.damage_taken_multiplier}</damageTakenMultiplier>
                        <bonusPower>{self.bonus_power}</bonusPower>
                        <resistsMindControl>{str(self.resists_mind_control).lower()}</resistsMindControl>
                        <isTelepathic>{str(self.is_telepathic).lower()}</isTelepathic>
                        <controllable>{str(self.controllable).lower()}</controllable>
                        {drone_ai_xml}
                        {death_sounds_xml}
                        {death_effect_xml}
                        {shooting_sounds_xml}
                        <isAnaerobic>{str(self.is_anaerobic).lower()}</isAnaerobic>
                        {oxygen_change_speed_xml}
                        <defaultSkillLevel>{self.default_skill_level}</defaultSkillLevel>
                        {passive_stat_boosts_xml}
                        {self.power_effect_xml if self.power_effect_xml else ""}
                    </mod-append:race>
                </mod:findLike>
        """

        return xml

    def generate_auto_version(
        self, drone_ai, cost_multiplier=0.9, extra_fuel_cost=0, extra_drone_cost=-1
    ):
        """Generate an automatic version of the drone with adjusted costs and AI instructions."""
        return IndyDrone(
            name=self.name,
            mark=self.mark,
            description=self.description,
            cost=int(ceil(self.cost * cost_multiplier)),
            fuel_cost=self.fuel_cost + extra_fuel_cost,
            drone_cost=self.drone_cost + extra_drone_cost,
            title=self.title,
            short=self.short,
            rarity=self.rarity,
            power_list=self.power_list,
            anim_base=self.anim_base,
            anim_sheet=self.anim_sheet,
            bp=self.bp,
            max_health=self.max_health,
            crew_slots=self.crew_slots,
            can_fight=self.can_fight,
            can_sabotage=self.can_sabotage,
            can_man=self.can_man,
            can_repair=self.can_repair,
            no_clone=self.no_clone,
            heal_speed=self.heal_speed,
            can_burn=self.can_burn,
            can_suffocate=self.can_suffocate,
            repair_speed=self.repair_speed,
            move_speed_multiplier=self.move_speed_multiplier,
            stun_multiplier=self.stun_multiplier,
            fire_damage_multiplier=self.fire_damage_multiplier,
            heal_crew_amount=self.heal_crew_amount,
            damage_taken_multiplier=self.damage_taken_multiplier,
            damage_taken_multiplier_enemy_ship_xml=self.damage_taken_multiplier_enemy_ship_xml,
            bonus_power=self.bonus_power,
            resists_mind_control=self.resists_mind_control,
            is_telepathic=self.is_telepathic,
            controllable=False,
            drone_ai=drone_ai,
            death_sounds=self.death_sounds,
            death_effect=self.death_effect,
            shooting_sounds=self.shooting_sounds,
            is_anaerobic=self.is_anaerobic,
            oxygen_change_speed=self.oxygen_change_speed,
            drone_bay_heal_amount=self.drone_bay_heal_amount,
            medbay_heal_speed=self.medbay_heal_speed,
            default_skill_level=self.default_skill_level,
            power_effect_xml=self.power_effect_xml,
        )

    def generate_upgrade_version(
        self,
        description_suffix,
        power_list,
        cost_multiplier=1.2,
        extra_fuel_cost=0,
        extra_drone_cost=2,
        heal_speed_multiplier=1.0,
        max_health_multiplier=1.0,
        repair_speed_multiplier=1.0,
        move_speed_multiplier_multiplier=1.0,
        stun_multiplier_multiplier=1.0,
        fire_damage_multiplier_multiplier=1.0,
        damage_taken_multiplier_multiplier=1.0,
        heal_crew_amount_multiplier=1.0,
        extra_bonus_power=1,
    ):
        """Generate an upgraded version of the drone with adjusted costs and stats."""
        return IndyDrone(
            name=self.name,
            mark=self.mark + 1,
            description=self.description + description_suffix,
            cost=int(ceil(self.cost * cost_multiplier)),
            fuel_cost=self.fuel_cost + extra_fuel_cost,
            drone_cost=self.drone_cost + extra_drone_cost,
            title=self.title,
            short=self.short,
            rarity=self.rarity,
            power_list=power_list,
            anim_base=self.anim_base,
            anim_sheet=self.anim_sheet,
            bp=self.bp,
            max_health=int(ceil(self.max_health * max_health_multiplier)),
            crew_slots=self.crew_slots,
            can_fight=self.can_fight,
            can_sabotage=self.can_sabotage,
            can_man=self.can_man,
            can_repair=self.can_repair,
            no_clone=self.no_clone,
            heal_speed=self.heal_speed * heal_speed_multiplier,
            can_burn=self.can_burn,
            can_suffocate=self.can_suffocate,
            repair_speed=self.repair_speed * repair_speed_multiplier
            if self.can_repair
            else None,
            move_speed_multiplier=self.move_speed_multiplier
            * move_speed_multiplier_multiplier,
            stun_multiplier=self.stun_multiplier * stun_multiplier_multiplier,
            fire_damage_multiplier=self.fire_damage_multiplier
            * fire_damage_multiplier_multiplier,
            heal_crew_amount=self.heal_crew_amount * heal_crew_amount_multiplier
            if self.heal_crew_amount is not None
            else None,
            damage_taken_multiplier=self.damage_taken_multiplier
            * damage_taken_multiplier_multiplier,
            damage_taken_multiplier_enemy_ship_xml=self.damage_taken_multiplier_enemy_ship_xml,
            bonus_power=self.bonus_power + extra_bonus_power,
            resists_mind_control=self.resists_mind_control,
            is_telepathic=self.is_telepathic,
            controllable=self.controllable,
            drone_ai=self.drone_ai,
            death_sounds=self.death_sounds,
            death_effect=self.death_effect,
            shooting_sounds=self.shooting_sounds,
            is_anaerobic=self.is_anaerobic,
            oxygen_change_speed=self.oxygen_change_speed,
            drone_bay_heal_amount=self.drone_bay_heal_amount,
            medbay_heal_speed=self.medbay_heal_speed * heal_speed_multiplier,
            default_skill_level=self.default_skill_level,
            power_effect_xml=EFFECT_UPGRADES[self.power_effect_xml]
            if self.power_effect_xml in EFFECT_UPGRADES
            else self.power_effect_xml,
        )
