import csv

class parseCSV:
    def parse(recipeString):

        #split the csv into rows
        recipeList = recipeString.split("\n")

        #Get and delete the header
        headerString = recipeList[0].lower()
        del recipeList[0]
        #get the column number of
        #recipe: Ingredients,cups,tbsp,tsp,oz,lb,grams,...
        #Instructions,Recipe name
        headerList = headerString.split(";")
        for i in range(len(headerList)):
            if(headerList[i] == "ingredients"):
                ingredient_i=i
            elif(headerList[i] == "cups"):
                cups_i=i
            elif(headerList[i] == "tbsp"):
                tbsp_i=i
            elif(headerList[i] == "tsp"):
                tsp_i=i
            elif(headerList[i] == "oz"):
                oz_i=i
            elif(headerList[i] == "lb"):
                lb_i=i
            elif(headerList[i] == "grams"):
                grams_i=i
            elif(headerList[i] == "instructions"):
                instructions_i=i
            elif(headerList[i] == "recipe name"):
                recipe_name_i=i
            else:
                continue

        # Populate the recipe object attributes with values
        for recipe_row in recipeList:
            if(recipe_row==""):
                break
            rowHolder = recipe_row.split(";")
            if(len(rowHolder[ingredient_i])):
                recipe.ingredients.append(rowHolder[ingredient_i])
                recipe.cups.append(rowHolder[cups_i])
                recipe.grams.append(rowHolder[grams_i])
                recipe.lb.append(rowHolder[lb_i])
                recipe.oz.append(rowHolder[oz_i])
                recipe.tbsp.append(rowHolder[tbsp_i])
                recipe.tsp.append(rowHolder[tsp_i])
            if(len(rowHolder[recipe_name_i])):
                recipe.name.append(rowHolder[recipe_name_i])
            if(len(rowHolder[instructions_i])):
                recipe.instructions.append(rowHolder[instructions_i])
        print("recipe.ingredients ")
        print(*recipe.ingredients)
        print("recipe.ingredients ")
        print(*recipe.name)
        print("rrecipe.instructions ")
        print(*recipe.instructions)
        print("recipe.cups ")
        print(*recipe.cups)

        #return the recipe object
        return recipe

# used to hold the parse csv recipe
class recipe:
        name  = []
        ingredients = []
        instructions = []
        cups = []
        tbsp = []
        tsp = []
        oz = []
        lb = []
        grams = []
