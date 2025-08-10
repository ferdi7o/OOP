# Create an instance of the Guild Master
from project.guild_master import GuildMaster

manager = GuildMaster()

# Add members (warriors & mages)
print(manager.add_member("Warrior", "W02345", 100))
print(manager.add_member("Warrior", "12W34", 200))
print(manager.add_member("Warrior", "789123W", 250))
print(manager.add_member("Warrior", "WW45678999", 150))
print(manager.add_member("Mage", "M321654", 300))
print(manager.add_member("Mage", "654M3211", 320))
print(manager.add_member("Mage", "334654M", 350))
print(manager.add_member("Mage", "MM034654", 400))
print()

# Add guild halls
print(manager.add_guild_hall("MagicTower", "Silver Tower"))
print(manager.add_guild_hall("CombatHall", "Iron Bastion"))
print(manager.add_guild_hall("CombatHall", "Dragon Watch"))
print()

# Assign members to guild halls
print(manager.assign_member("Silver Tower", "Warrior"))
print(manager.assign_member("Silver Tower", "Mage"))
print(manager.assign_member("Silver Tower", "Mage"))
print(manager.assign_member("Dragon Watch", "Mage"))
print(manager.assign_member("Dragon Watch", "Warrior"))
print(manager.assign_member("Dragon Watch", "Warrior"))
print(manager.assign_member("Dragon Watch", "Warrior"))
print()

# Conduct practice sessions
print(manager.practice_members(manager.guild_halls[0], 0))
print(manager.practice_members(manager.guild_halls[0], 1))
print(manager.practice_members(manager.guild_halls[0], 2))
print(manager.practice_members(manager.guild_halls[0], 3))
print(manager.practice_members(manager.guild_halls[0], 5))
print(manager.practice_members(manager.guild_halls[1], 1))
print(manager.practice_members(manager.guild_halls[1], 0))
print(manager.practice_members(manager.guild_halls[2], 1))
print()

# Unassign a member
print(manager.unassign_member(manager.guild_halls[2], "334654M"))
print(manager.unassign_member(manager.guild_halls[0], "W02345"))
print(manager.guild_halls[0].members[0].tag, manager.guild_halls[0].members[0].skill_level)
print(manager.unassign_member(manager.guild_halls[0], "111111"))
print(manager.unassign_member(manager.guild_halls[1], "WW45678999"))
print()

# Perform a guild-wide update
print(manager.guild_update(8))
print()

# Check members gold after the update
print(manager.guild_halls[0].members[0].gold)
print(manager.guild_halls[0].members[1].gold)
print(manager.guild_halls[0].members[2].gold)
print()
print(manager.guild_halls[2].members[0].gold)
print(manager.guild_halls[2].members[1].gold)
print()
print(manager.members[0].gold)
print(manager.members[1].gold)
print(manager.members[2].gold)
