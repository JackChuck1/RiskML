
with open("ActionTable.txt", "w") as file:
    for i in range(42):
        for j in range(42):
            file.write(f"({i}, {j}),\n")
    file.close()