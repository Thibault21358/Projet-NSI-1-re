import pyxel, random
pyxel.init(256,256,title="Fuego Arena",fps=60,)
musique_on=False
boost_on=False
perso_x=128
perso_y=128
perso =1
Bomberman = [120,120]
SceneNiveau =0
Vies = 3
Vitesse = 1
bombes_liste = []
ExplosionsListe = []
BoostsListe = []
Score = 0
Vie1 = [0,0]
Vie2 = [16,0]
Vie3 = [32,0]
pyxel.load("ress.pyxres")

def attendre_début():
    global SceneNiveau
    if SceneNiveau == 0 and  pyxel.btn(pyxel.KEY_RETURN):
        SceneNiveau = 3

def Menu():
    global SceneNiveau
    if SceneNiveau == 3:
        if pyxel.btn(pyxel.KEY_C):
            SceneNiveau = 5
            if pyxel.btn(pyxel.KEY_A):
                SceneNiveau = 3
        if pyxel.btn(pyxel.KEY_R):
            SceneNiveau = 6
            if pyxel.btn(pyxel.KEY_A):
                SceneNiveau = 3
        if pyxel.btn(pyxel.KEY_P):
            SceneNiveau = 4

def credits():
    global SceneNiveau
    if pyxel.btn(pyxel.KEY_A):
        SceneNiveau=3
        
def select_character():
    global SceneNiveau, perso
    if pyxel.btn(pyxel.KEY_A):
        perso =1
    if pyxel.btn(pyxel.KEY_Z):
        perso =2
    if pyxel.btn(pyxel.KEY_E):
        perso =3
    if pyxel.btn(pyxel.KEY_R):
        perso =4
    if pyxel.btn(pyxel.KEY_T):
        perso =5
    if pyxel.btn(pyxel.KEY_Y):
        perso =6
    if pyxel.btn(pyxel.KEY_U):
        perso =7
    if pyxel.btn(pyxel.KEY_I):
        perso =8
    if SceneNiveau==4 and pyxel.btn(pyxel.KEY_M):
        SceneNiveau = 1
       
def Recommencer_niveau():
    global Vies, Score, SceneNiveau, Bomberman, bombes_liste,BoostsListe
    if SceneNiveau == 2 and  pyxel.btn(pyxel.KEY_RETURN):
        Vies = 3
        Score=0
        SceneNiveau=4
        Bomberman=[120,120]
        bombes_liste=[]
        BoostsListe=[]
        pyxel.cls(0)
        
def bomberman_deplacement(bomberman):
    """Cette fonction permet à l'utilisateur de déplacer le personnage."""
    x = bomberman[0]
    y = bomberman[1]
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
        if (x < 240) :
            x = x + Vitesse
    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q):
        if (x > -3) :
            x = x - Vitesse
    if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
        if (y < 238) :
            y = y + Vitesse
    if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_Z):
        if (y > 1) :
            y = y - Vitesse
    bomberman[0] = x
    bomberman[1] = y
    return bomberman
    
def boosts_creation(boosts_liste):
    """Cette fonction créé un boost qui s'affiche sous la forme d'un pixel art d'une botte."""
    if (pyxel.frame_count % 400 == 0 and len(boosts_liste) <3):
        boosts_liste.append([random.randint(48, 216), random.randint(48, 216)])
    return boosts_liste
    
def bomberman_boost(vitesse):
    """Cette fonction permet que lorsque le personnage va sur le pixel art de la botte, il y a un boost pendant 3s. """
    for boost in BoostsListe:
        if boost[0] <= Bomberman[0]+8 and boost[1] <= Bomberman[1]+8 and boost[0]+8 >= Bomberman[0] and boost[1]+8 >= Bomberman[1]:
            BoostsListe.remove(boost)
            vitesse += 2.5
            boost_on=True
            pyxel.playm(0, loop=False)
    if (pyxel.frame_count % 115 == 0 and vitesse > 2.5):
        vitesse -= 2.5
        boost_on=False
        pyxel.playm(2,loop=True)
    return vitesse
    
def bombes_creation(bombes_liste):
    """Cette fonction permet la création aléatoire des bombes de chaque côté de l'écran."""
    direction=random.randint(0,3)
    if Score>0:
        if (pyxel.frame_count % 50 == 0):
            if direction == 0:
                bombes_liste.append([direction, random.randint(0,248),0])
            if direction == 1:
                bombes_liste.append([direction,248,random.randint(0,248)])
            if direction == 2:
                bombes_liste.append([direction,random.randint(0,248),248])
            if direction ==3:
                bombes_liste.append([direction,0,random.randint(0,248)])
    if Score>250:
        if (pyxel.frame_count % 46 == 0):
            if direction == 0:
                bombes_liste.append([direction, random.randint(0,248),0])
            if direction == 1:
                bombes_liste.append([direction,248,random.randint(0,248)])
            if direction == 2:
                bombes_liste.append([direction,random.randint(0,248),248])
            if direction ==3:
                bombes_liste.append([direction,0,random.randint(0,248)])
    if Score>500:
        if (pyxel.frame_count % 42== 0):
            if direction == 0:
                bombes_liste.append([direction, random.randint(0,248),0])
            if direction == 1:
                bombes_liste.append([direction,248,random.randint(0,248)])
            if direction == 2:
                bombes_liste.append([direction,random.randint(0,248),248])
            if direction ==3:
                bombes_liste.append([direction,0,random.randint(0,248)])

def bombes_deplacement(bombes_liste):
    """Cette fonction permet que après la création des bombes, elles se déplacent."""
    for bombes in bombes_liste:
        if bombes[0]==0:
            bombes[2]+=2
        elif bombes[0]==1:
            bombes[1]+=(-2)
        elif bombes[0]==2:
            bombes[2]+=(-2)
        elif bombes[0]==3:
            bombes[1]+=2
    return bombes_liste
    
def detection_collision(vies):
    """Cette fonction permet que lorsqu'il y a une collision, le joueur perde une vie."""
    for bombe in bombes_liste:
        if bombe[1] <= Bomberman[0]+8 and bombe[2] <= Bomberman[1] +8 and bombe[1]+8 >= Bomberman[0] and bombe[2]+8 >= Bomberman[1]:
            bombes_liste.remove(bombe)
            vies -= 1
            explosions_creation(Bomberman[0], Bomberman[1])
    return vies
    
def explosions_creation(x, y):
    """Cette fonction permet la création des explosions."""
    ExplosionsListe.append([x, y, 0])
    
def explosions_animation():
    """Cette fonction fait que lorsqu'une explosion est créé, il y a une certaine animation."""
    global ExplosionsListe
    for explosion in ExplosionsListe:
        explosion[2] +=2
        if explosion[2] == 20:
            ExplosionsListe.remove(explosion)  

def Score_timer(Score):
    """Cette fonction permet de créer et de rajouter des points à score au fur et à mesure du temps."""
    if SceneNiveau== 1 :
        if (pyxel.frame_count % 5== 0):
            Score += 1
        return Score

def musique():
    global musique_on, boost_on
    if SceneNiveau==1 and musique_on==False and boost_on==False:
        pyxel.playm(2,loop=True)
        musique_on=True
    if SceneNiveau==2 and musique_on==True:
        pyxel.playm(1,loop=False)
        musique_on=False
        
def afficher_score():
    pyxel.text(10, 160, "Score: {}".format(Score), 7)

def update():
    global perso_x, perso_y, Bomberman, bombes_liste, Vies, ExplosionsListe, BoostsListe, Vitesse, SceneNiveau, perso, Score_timer, Score
    musique()
    if SceneNiveau == 0:
        attendre_début()
    elif SceneNiveau == 4:
        select_character()
    elif SceneNiveau == 1:
        Bomberman = bomberman_deplacement(Bomberman)
        bombes_creation(bombes_liste)
        bombes_liste = bombes_deplacement(bombes_liste)
        BoostsListe = boosts_creation(BoostsListe)
        Vitesse = bomberman_boost(Vitesse)
        Vies = detection_collision(Vies)
        explosions_animation()
        Score = Score_timer(Score)
    elif SceneNiveau == 2:
        Recommencer_niveau()
    elif SceneNiveau == 3:
        Menu()
    elif SceneNiveau == 5:
        credits()
    elif SceneNiveau == 6:
        credits()
    

    
        
def draw():
    global SceneNiveau, perso, Score_timer
    pyxel.cls(0)
    pyxel.rect(perso_x, perso_y, 8, 8, 1)
    if SceneNiveau == 0:
        pyxel.bltm(0,0,0,512,0,255,255)
        pyxel.text(99, 137, "- PRESS ENTER -", pyxel.frame_count % 9)
        pyxel.text(106, 80, "FUEGO ARENA",4 )
    elif SceneNiveau == 3:
        pyxel.bltm(0,0,0,1280,0,255,255)
        pyxel.text(85,105,"Press C for credits",1)
        pyxel.text(85,120,"Press R for rules",1)
        pyxel.text(85,135,"Press P to play",1)
    elif SceneNiveau == 5:
        pyxel.bltm(0,0,0,1280,0,255,255)
        pyxel.text(45,105,"Creators: Quentin, Louca, Andrea, Thibault",1)
        pyxel.text(85,120,"Musique inspiree de Mario",1)
        pyxel.text(35,135,"Personnages inspires de personnages deja existants",1)
        pyxel.text(85,170,"Press A to return",pyxel.frame_count % 12)
    elif SceneNiveau == 6:
        pyxel.bltm(0,0,0,1280,0,255,255)
        pyxel.text(20,60,"Pour se deplacer, utilisez les fleches de direction ou",1)
        pyxel.text(35,70,"les touches q(gauche),z(haut),d(droite) et s(bas)",1)
        pyxel.text(20,90,"Les bottes apparaissent frequemment et vous permettent ",1)
        pyxel.text(35,100,"d'aller plus vite pendant une petite periode",1)
        pyxel.text(20,120,"Le but du jeu est d'esquiver les bombes. Vous n'avez",1)
        pyxel.text(95,130,"que trois vies!",1)
        pyxel.text(85,150,"Press A to return",pyxel.frame_count % 12)
    elif SceneNiveau == 4:
        pyxel.bltm(0,0,0,768,0,255,255)
        pyxel.text(85,105,"Press M after selection",7)
        pyxel.text(17,175,"Press A",7)
        pyxel.text(82,175,"Press Z",7)
        pyxel.text(145,175,"Press E",7)
        pyxel.text(212,175,"Press R",7)
        pyxel.text(17,237,"Press T",7)
        pyxel.text(82,237,"Press Y",7)
        pyxel.text(145,237,"Press U",7)
        pyxel.text(212,237,"Press I",7)
    elif SceneNiveau == 1:
        if Score<500:
            pyxel.bltm(0,0,0,0,0,255,255)
        else:
            pyxel.bltm(0,0,0,1023,0,255,255)
        if Vies == 3:
            pyxel.blt(Vie1[0], Vie1[1], 0, 16, 64, 16, 16,0)
            pyxel.blt(Vie2[0], Vie2[1], 0, 16, 64, 16, 16,0)
            pyxel.blt(Vie3[0], Vie3[1], 0, 16, 64, 16, 16,0)
        elif Vies == 2:
            pyxel.blt(Vie1[0], Vie1[1], 0, 16, 64, 16, 16,0)
            pyxel.blt(Vie2[0], Vie2[1], 0, 16, 64, 16, 16,0)
            pyxel.blt(Vie3[0], Vie3[1], 0, 0, 64, 16, 16,0)
        elif Vies == 1:
            pyxel.blt(Vie1[0], Vie1[1], 0, 16, 64, 16, 16,0)
            pyxel.blt(Vie2[0], Vie2[1], 0, 0, 64, 16, 16,0)
            pyxel.blt(Vie3[0], Vie3[1], 0, 0, 64, 16, 16,0)
        pyxel.text(210, 5, "Score: "+ str(Score), 0)
        for boost in BoostsListe:
            pyxel.blt(boost[0], boost[1], 0, 64, 0, 16, 16,6)
        for bombe in bombes_liste:
            if Score<500:
                pyxel.blt(bombe[1], bombe[2], 0, 48, 0, 16, 16,0)
            else:
                pyxel.blt(bombe[1], bombe[2], 0, 96, 0, 16, 16, 5)
        if perso==1:
            pyxel.blt(Bomberman[0], Bomberman[1], 0, 16, 0, 16, 16,12)
        if perso==2:
            pyxel.blt(Bomberman[0], Bomberman[1], 0, 0, 80, 16, 16,10)
        if perso==3:
            pyxel.blt(Bomberman[0], Bomberman[1], 0, 16, 80, 16, 16,8)
        if perso==4:
            pyxel.blt(Bomberman[0], Bomberman[1], 0, 32, 80, 16, 16,15)
        if perso==5:
            pyxel.blt(Bomberman[0], Bomberman[1], 0, 48, 80, 16, 16,2)
        if perso==6:
            pyxel.blt(Bomberman[0], Bomberman[1], 0, 64, 80, 16, 16,5)
        if perso==7:
            pyxel.blt(Bomberman[0], Bomberman[1], 0, 80, 80, 16, 16,0)
        if perso==8:
            pyxel.blt(Bomberman[0], Bomberman[1], 0, 96, 80, 16, 16,9)
        
        for explosion in ExplosionsListe:
            pyxel.circb(explosion[0]+4, explosion[1]+4, 2*(explosion[2]//4),8+explosion[2]%3)
    elif SceneNiveau == 2:
        pyxel.bltm(0,0,0,256,0,255,255)
        afficher_score()
        pyxel.text(210,160,"PRESS ENTER",pyxel.frame_count % 12)
    if Vies <= 0:
        SceneNiveau = 2


pyxel.run(update, draw)
pyxel.quit()
