
with open('recipe_qaunts.txt', "r") as f:
    res = f.readlines()
    n = []
    for line in res:
        x = line.split(" ")
        start = x[0]
        if start == 'insert':
            try:
                n.append(int(x[-1]))
            except:
                try:
                    n.append(int(x[-2]))
                except:
                    try:
                        n.append(int(x[-3]))
                    except:
                        try:
                            n.append(int(x[-4]))
                        except:
                            print(x[-4])

print(n)
print(len(n))



# with PSQL.Database() as db:
#     for value, index in zip(x, range(len(x))):

#             db.cursor.execute("""
#             UPDATE recipe_ingredients
#             SET ingredient_quantity=%s
#             WHERE recipe_ingredient_id=%s
#             """, (value, (index+1),))

#             print(f'{index} completed')