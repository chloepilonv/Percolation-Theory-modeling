import numpy as np
import matplotlib.pyplot as plt
import time
import csv

t0 = time.time()

#Creation grille n*n
n = 50
it = 10

#grille principale
grille = np.zeros(n**2).reshape(n, n)
plt.imshow(grille)

#grille de comptage
grille2 = np.zeros(n**2).reshape(n, n)

#Activation de x pts infectés
x = 10
coord_x = np.ones(x, dtype=int)
coord_y = np.ones(x, dtype=int)
i = 0
while i<x:
    coord_x[i] = int(round(np.random.random()*n-1))
    coord_y[i] = int(round(np.random.random()*n-1))
    i += 1

i = 0
while i<x:
    grille[coord_x[i], coord_y[i]] = 1
    i += 1

#Iterations de contamination
b = 0.190 #taux d'infection
k = 0.035 #taux de retablissement (apres le temps de retablissement)
m = 0.02 #taux de personnes decedees
v = 0.01 #taux de vaccination
t = 15 #temps avant le debut de la vaccination
R0=4 #taux de reproduction de base
duree_infection = 14
duree_immunisation = 70
duree_vaccin = 180
efficacite_vaccin_initiale = 0.9
perte_efficacite = 0.1

# nombre de voisins affectés par la contamination
voisins = 3 # il faut modifier le code dans les iterations pour modifier le nombre de voisins

save = 10
s = save

f = 0
plt.imshow(grille, cmap = 'jet')
plt.colorbar()

# Variables pour graphique SIR
sain = np.zeros(it)
infecte = np.zeros(it)
retabli = np.zeros(it)
decede = np.zeros(it)
vaccine = np.zeros(it)

# Taux de reproduction de base
reprod1=np.zeros(it)
reprod2=np.zeros(it)
reprodv=np.zeros(it)
reprod1[0] = R0
reprod2[0] = R0
reprodv[0] = R0

while f<it:

    #nombre de voisins a considerer pour l'infection
    if f >= 100:
        voisins = 2
    if f >= 200:
        voisins = 1

    #Contamination aleatoire de personnes (proportionnel au nb d'infecte)
    cont_rand = round(infecte[f-1]/100*voisins)
    p = 0
    while p < cont_rand:
        x = int(round(np.random.random() * n - 1))
        y = int(round(np.random.random() * n - 1))
        if grille[x, y] == 0:
            grille[x, y] = 1

        p += 1

    print("Iteration:", f)
    points_a_infecter = np.ones(1, dtype=int)
    points_a_retablir = np.ones(1, dtype=int)

    # compilation des etats de la grille (pour graphique final) et infections
    i = 0
    while i< n:
        j = 0
        while j<n:
            if f >= t:
                #points vaccines
                r = np.random.random()
                if grille[i, j] == 0 or grille[i, j] == 0.5 and grille2[i, j]<=0:
                    r2 = np.random.random()
                    if r < v:
                        if r2 < efficacite_vaccin_initiale:
                            grille[i, j] = 0.75
                            grille2[i, j] = -1

                if grille2[i, j] <= -duree_vaccin and grille[i, j] == 0.75:
                    grille2[i, j] = 0
                    grille[i, j] = 0

                if grille[i, j] == 0.75:
                    grille2[i, j] -= 1
                    vaccine[f] += 1
                    r2 = np.random.random()
                    if r2 < perte_efficacite:
                        grille[i, j] = 0
                        grille2[i, j] = 0

            #points infectes
            if grille[i, j] == 1:

                infecte[f] += 1

                #infection selon le nombre de voisins

                # juste premiers plus proches voisins
                if voisins == 1:
                    r = np.random.random()
                    if i+1 <n: #conditions frontiere de la grille
                        if (grille[i + 1, j] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i + 1)
                            points_a_infecter = np.append(points_a_infecter, j)

                    r = np.random.random()
                    if i-1>=0: #conditions frontiere de la grille
                        if (grille[i - 1, j] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i - 1)
                            points_a_infecter = np.append(points_a_infecter, j)

                    r = np.random.random()
                    if j+1<n: #conditions frontiere de la grille
                        if (grille[i, j + 1] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i)
                            points_a_infecter = np.append(points_a_infecter, j + 1)

                    r = np.random.random()
                    if j-1>=0: #conditions frontiere de la grille
                        if (grille[i, j - 1] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i)
                            points_a_infecter = np.append(points_a_infecter, j - 1)

                #deuxiemes et premiers plus proches voisins
                if voisins == 2:
                    r = np.random.random()
                    if i + 1 < n:  # conditions frontiere de la grille
                        if (grille[i + 1, j] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i + 1)
                            points_a_infecter = np.append(points_a_infecter, j)

                    r = np.random.random()
                    if i - 1 >= 0:  # conditions frontiere de la grille
                        if (grille[i - 1, j] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i - 1)
                            points_a_infecter = np.append(points_a_infecter, j)

                    r = np.random.random()
                    if j + 1 < n:  # conditions frontiere de la grille
                        if (grille[i, j + 1] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i)
                            points_a_infecter = np.append(points_a_infecter, j + 1)

                    r = np.random.random()
                    if j - 1 >= 0:  # conditions frontiere de la grille
                        if (grille[i, j - 1] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i)
                            points_a_infecter = np.append(points_a_infecter, j - 1)

                    r = np.random.random()
                    if i + 1 < n and j + 1 < n:  # conditions frontiere de la grille
                        if (grille[i + 1, j+1] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i + 1)
                            points_a_infecter = np.append(points_a_infecter, j+1)

                    r = np.random.random()
                    if i - 1 >= 0 and j-1 >= 0:  # conditions frontiere de la grille
                        if (grille[i - 1, j-1] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i - 1)
                            points_a_infecter = np.append(points_a_infecter, j-1)

                    r = np.random.random()
                    if j + 1 < n and i-1>=0:  # conditions frontiere de la grille
                        if (grille[i-1, j + 1] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i-1)
                            points_a_infecter = np.append(points_a_infecter, j + 1)

                    r = np.random.random()
                    if j - 1 >= 0 and i+1 < n:  # conditions frontiere de la grille
                        if (grille[i+1, j - 1] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i+1)
                            points_a_infecter = np.append(points_a_infecter, j - 1)

                #1er, 2e et 3e plus proches voisins
                if voisins == 3:
                    r = np.random.random()
                    if i + 1 < n:  # conditions frontiere de la grille
                        if (grille[i + 1, j] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i + 1)
                            points_a_infecter = np.append(points_a_infecter, j)

                    r = np.random.random()
                    if i - 1 >= 0:  # conditions frontiere de la grille
                        if (grille[i - 1, j] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i - 1)
                            points_a_infecter = np.append(points_a_infecter, j)

                    r = np.random.random()
                    if j + 1 < n:  # conditions frontiere de la grille
                        if (grille[i, j + 1] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i)
                            points_a_infecter = np.append(points_a_infecter, j + 1)

                    r = np.random.random()
                    if j - 1 >= 0:  # conditions frontiere de la grille
                        if (grille[i, j - 1] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i)
                            points_a_infecter = np.append(points_a_infecter, j - 1)

                    r = np.random.random()
                    if i + 1 < n and j + 1 < n:  # conditions frontiere de la grille
                        if (grille[i + 1, j + 1] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i + 1)
                            points_a_infecter = np.append(points_a_infecter, j + 1)

                    r = np.random.random()
                    if i - 1 >= 0 and j - 1 >= 0:  # conditions frontiere de la grille
                        if (grille[i - 1, j - 1] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i - 1)
                            points_a_infecter = np.append(points_a_infecter, j - 1)

                    r = np.random.random()
                    if j + 1 < n and i - 1 >= 0:  # conditions frontiere de la grille
                        if (grille[i - 1, j + 1] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i - 1)
                            points_a_infecter = np.append(points_a_infecter, j + 1)

                    r = np.random.random()
                    if j - 1 >= 0 and i + 1 < n:  # conditions frontiere de la grille
                        if (grille[i + 1, j - 1] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i + 1)
                            points_a_infecter = np.append(points_a_infecter, j - 1)

                    r = np.random.random()
                    if i + 2 < n:  # conditions frontiere de la grille
                        if (grille[i + 2, j] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i + 2)
                            points_a_infecter = np.append(points_a_infecter, j)

                    r = np.random.random()
                    if i - 2 >= 0:  # conditions frontiere de la grille
                        if (grille[i - 2, j] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i - 2)
                            points_a_infecter = np.append(points_a_infecter, j)

                    r = np.random.random()
                    if j + 2 < n:  # conditions frontiere de la grille
                        if (grille[i, j + 2] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i)
                            points_a_infecter = np.append(points_a_infecter, j + 2)

                    r = np.random.random()
                    if j - 2 >= 0:  # conditions frontiere de la grille
                        if (grille[i, j - 2] == 0) and b > r:
                            points_a_infecter = np.append(points_a_infecter, i)
                            points_a_infecter = np.append(points_a_infecter, j - 2)


                #Conditions de retablissement (min 14 jours)
                if grille2[i, j] < duree_infection:
                    grille2[i, j] += 1
                #Ajout des ppoints a la liste de points a retablir
                if grille2[i, j] >= duree_infection:
                    r = np.random.random()
                    r2 = np.random.random()
                    if r < k:
                        grille2[i, j] = -1
                        points_a_retablir = np.append(points_a_retablir, i)
                        points_a_retablir = np.append(points_a_retablir, j)
                    else: #Si le point ne se retablis pas il a une chance de mourir
                        if r2 < m:
                            grille[i, j] = 0.25


            #points morts
            if grille[i, j] == 0.25:
                decede[f] += 1

            #points sains
            if grille[i, j] == 0:
                sain[f] += 1

            #points retablis
            if grille[i, j] == 0.5:
                retabli[f] += 1

                #Conditions pour passer de retabli a sain
                if grille2[i, j] > -duree_immunisation:
                    grille2[i, j] -= 1

                if grille2[i, j] <= -duree_immunisation and grille[i, j] ==0.5:
                    grille2[i, j] = 0
                    grille[i, j] = 0

            j = j+1
        i = i+1


    #boucle d'infection avec liste des points a infecter
    i = 1
    while i<len(points_a_infecter):
        grille[points_a_infecter[i], points_a_infecter[i + 1]] = 1
        i = i+2

    #boucle de retablissement avec liste des points a retablir
    i = 1
    while i < len(points_a_retablir):
        grille[points_a_retablir[i], points_a_retablir[i + 1]] = 0.5
        i = i + 2

    plt.imshow(grille, cmap = 'jet')
    plt.pause(0.05)
    #if f == save:
        #savename = 'grilles/grille'+str(save)+'.png'
        #plt.savefig(savename)
        #save += s

    #boucle calcul du taux de reproduction
    if f >= 1:
            # OPTION 1, NISHIURA
            reprod1[f] = R0 * sain[f] / sain[f-1]

            # OPTION 2, Cori, avec différents b
            reprod2[f] = b * (sain[f] / sain[0]) * duree_infection  # ou / n**2

            reprodv[f] = R0  # la vaccination na pas commence

    if f >= t:
            # OPTION UNIQUE, Calcul du taux de reproduction avec vaccin Rv(t)
            p = vaccine[f] / (n ** 2)
            reprodv[f] = R0 * (1 - p)
    f += 1

t1 = time.time()
print(t1-t0)
print("Simulation terminee")
plt.show()

temps = np.arange(0, it, 1)
plt.plot(temps, sain, label = "sain")
plt.plot(temps, infecte, label = "infecte")
plt.plot(temps, retabli, label ="retabli")
plt.plot(temps, decede, label ="morts")
plt.plot(temps, vaccine, label = "vaccine")
plt.ylabel('Nombre d’individus')
plt.xlabel('Itérations/Journées')
plt.title('Variation des états SIRDV dans le temps')
plt.legend()
plt.show()

#NOUVEAU
plt.plot(temps,reprod1, label = "Option 1")
plt.plot(temps, reprod2, label = "Option 2, b=0.4", linestyle='dashed')
plt.plot(temps, reprodv, label = "Apres vaccination")
plt.title('Variation du taux de reproduction instantanée')
plt.xlabel('Temps (j)')
plt.ylabel('R(t)')
plt.legend()
plt.show()

with open('data.csv', mode = 'w') as csv_file:
    fieldnames = ['S', 'I', 'R', 'D', 'V']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    i = 0
    while i < len(temps):
        writer.writerow({'S': sain[i], 'I': infecte[i], 'R': retabli[i], 'D': decede[i], 'V': vaccine[i]})
        i += 1




