treasure_bag = []
treasure_bag.extend(["gold coin", "silver coin", "ruby", "pearl"])
print(treasure_bag)

rare_treasures = ("diamond", "magic ring")
treasure_bag.extend(rare_treasures)
print(treasure_bag)

treasure_bag.remove("silver coin")
treasure_bag[treasure_bag.index("ruby")] = "emerald"
print(treasure_bag)

print(treasure_bag.count("gold coin"))

treasure_bag.sort()
print(treasure_bag)

treasure_bag.reverse()
print(treasure_bag)

print("magic ring" in treasure_bag)
print(treasure_bag.index("emerald"))

mid = len(treasure_bag) // 2
my_share = treasure_bag[:mid]
friend_share = treasure_bag[mid:]

print(my_share)
print(friend_share)

islands = ("island_1", "island_2", "island_3")
for island in islands:
    print(f"Searching {island} for treasures...")

new_treasure = input()
treasure_bag.append(new_treasure)
print(treasure_bag)

remove_treasure = input()
if remove_treasure in treasure_bag:
    treasure_bag.remove(remove_treasure)

print(treasure_bag)