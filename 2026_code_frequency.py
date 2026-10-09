import numpy as np

print("Enter the count for each species:")
snow = input("Snow: ")
hermit = input("Hermit: ")
atlantic = input("Atlantic: ")
green = input("Green: ")
rock = input("Rock: ")
jonah = input("Jonah: ")
sunstar = input("Sunstar: ")
urchin = input("Urchin: ")
boreal = input("Boreal: ")
daisy = input("Daisy: ")


crabs = np.array([
    "Snow crab", "Acadian hermit crab", "Western Atlantic Hairy Hermit Crab", 
    "European Green Crab", "Rock Crab", "Jonah Crab", "Spiny Sunstar", 
    "Sea Urchin", "Boreal Sea Star", "Daisy brittle star"
])


crab_counts = np.array([snow, hermit, atlantic, green, rock, jonah, sunstar, urchin, boreal, daisy], dtype=int)
total_sum = np.sum(crab_counts)

if total_sum > 0:
    proportions = crab_counts / total_sum
    for i in range(len(crabs)):
        print(f"{crabs[i]}: Count = {crab_counts[i]}, Proportion = {proportions[i]:.4f}")