#Author:
#Alexander Kuemmel
#02.06.2020

global swarm
global hunter
global bump
global vary
global friendspace
global avoidspace
global rule1
global rule2
global rule3
swarm = []
hunter = []
bump = []
vary = 10
friendspace = 50
avoidspace = 20
rule1 = False
rule2 = False
rule3 = False

def setup():
    size( 800, 600 )
    
def draw():
    global vary
    global friendspace
    global avoidspace
    background(0)
    for i in swarm:
        friends = grouping(i, swarm, friendspace)
        avoids = grouping(i, swarm, avoidspace)
        avoids += grouping(i, bump, avoidspace)
        avoids += grouping(i, hunter, avoidspace)
        v = i.velocity
        l = len(friends)
        la = len(avoids)
        v.add(alignment(friends, l))
        v.add(cohesion(i, friends, l))
        v.add(avoiding(i, avoids, la))
        changeRS(i, random(-vary, vary), 0)
        limitV(i, 0.2, 4)
        reentry(i)
        i.c = color(l*10, 100+l*10, 255-l*5)
        animate(i, v)
        
    for i in hunter:
        friends = grouping(i, swarm, friendspace)
        friends += grouping(i, hunter, friendspace)
        avoids = grouping(i, hunter, avoidspace)
        avoids += grouping(i, bump, avoidspace)
        v = i.velocity
        l = len(friends)
        la = len(avoids)
        v.add(alignment(friends, l))
        v.add(cohesion(i, friends, l))
        v.add(avoiding(i, avoids, la))
        changeRS(i, random(-vary, vary), 0)
        limitV(i, 0.1, 3.5)
        reentry(i)
        i.c = color(100+l*10, l*10, l*10)
        animate(i, v)
        
    for bumper in bump:
        fill(200, 0, 0)
        circle(bumper.pos.x, bumper.pos.y, 10)
    
    fill(255, 255, 255)
    if rule1 == True: text("1) Seperation", 5, 20)
    if rule2 == True: text("2) Ausrichtung", 5, 30)
    if rule3 == True: text("3) Zusammenhalt", 5, 40)
        

#Limitiert Speed um vmin und vmax. Angleich an mittlere Geschwindigkeit
def limitV(i, vmin, vmax):
    rs = rotSpeed(i.velocity)
    if rs.y < vmin:
        changeRS(i, 0, vmin-rs.y)
    if rs.y > vmax:
        changeRS(i, 0, vmax-rs.y)
    average = (vmin+vmax)/2
    changeRS(i, 0, (average-rs.y)/100)

#Aendert Rotation und Speed einer Instanz
def changeRS(i, alfa, c):
    rs = rotSpeed(i.velocity)
    pushMatrix()
    rotate(radians(rs.x + alfa))
    translate(0, -rs.y - c)
    v = PVector(screenX(0,0), screenY(0,0))
    i.velocity = v
    popMatrix()

#Animation der Instanzen
def animate(i, v):    
    rs = rotSpeed(v)
    pushMatrix()
    translate( i.pos.x, i.pos.y)
    rotate(radians(rs.x))
    fill(i.c)
    triangle( 0, -10, -5, 10, 5, 10 )
    translate( 0, -rs.y )
    i.pos = PVector(screenX(0,0), screenY(0,0))
    popMatrix()
    
#return: Winkel und Laenge eines Richtungsvektors
def rotSpeed(vec):
    a = vec.x
    b = vec.y
    c = sqrt((a*a)+(b*b))
    alfa = degrees( acos( -b/c ) )
    if a < 0:
        alfa = 360 - alfa
    return PVector(alfa, c)

#return: Distanz zwischen 2 Instanzen
def distance(i, target):
    a = target.pos.x - i.pos.x
    b = target.pos.y -i.pos.y
    return sqrt( (a*a) + (b*b) )

#return: Gruppe aus Array, Umkreis und abzueglich sich selbst
def grouping(i, crowd, space):
    group = []
    for target in crowd:
        if i != target and distance(i, target) < space:
            group.append(target)
    return group

#return: Richtungsvektor der von Mittelpunkt der Kollisionen weg zeigt
def avoiding(i, avoids, l):
    v = PVector(0,0)
    if rule1 == True and l > 0:
        for a in avoids:
            v.add(a.pos)
        v.div(l)
        v.sub(i.pos)
        v.div(-1)
        v.div(10) #Manuelle Anpassung
    return v
    
#return: Direction+Speed der Gruppe als Richtungsvektor
def alignment(friends, l):
    v = PVector(0,0)
    if rule2 == True and l > 0:
        for f in friends:
            v.add(f.velocity)
        v.div(l)
        v.div(8) #Manuelle Anpassung
    return v

#return: Mittelpunkt der Gruppe als Richtungsvektor
def cohesion(i, friends, l):
    v = PVector(0,0)
    if rule3 == True and l > 0:
        for f in friends:
            v.add(f.pos)
        v.div(l)
        v.sub(i.pos)
        v.div(100) #Manuelle Anpassung
    return v

#Instanzen die Screen verlassen, betreten screen auf gegenueberliegender Seite
def reentry(i):
    if i.pos.x > width:
        i.pos = PVector(0, height - i.pos.y)
    if i.pos.y > height:
        i.pos = PVector(width - i.pos.x, 0)
    if i.pos.x < 0:
        i.pos = PVector(width, height - i.pos.y)
    if i.pos.y < 0:
        i.pos = PVector(width - i.pos.x, height)

class Fish:
    def __init__(self):
        self.pos = PVector(mouseX, mouseY)
        self.velocity = PVector(random(-5, 5), random(-5, 5))
        self.c = color(255, 255, 255)

class Bumper:
    def __init__(self):
        self.pos = PVector(mouseX, mouseY)

#Erzeugt Instanzen: Fish, Bumper, Hunter
def mousePressed():
    global swarm
    if mouseButton == LEFT: swarm.append(Fish())
    if mouseButton == RIGHT: bump.append(Bumper())
    if mouseButton == CENTER: hunter.append(Fish())
    
def keyPressed():
    global rule1, rule2, rule3
    if key == "1":
        if rule1 == True: rule1 = False 
        else: rule1 = True
    if key == "2":
        if rule2 == True: rule2 = False 
        else: rule2 = True
    if key == "3":
        if rule3 == True: rule3 = False 
        else: rule3 = True
