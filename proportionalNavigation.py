from visual import *
from math import hypot

# feel free to mess with pos vectors and velocity vectors to see whether the rocket can catch its target

scene = display(title = 'Simulation', width = 800, height = 800, autocenter = True, center = (0,0,0))                       #making a scene
rocket = cone(pos = vector(100,0,0), axis=(0,5,0), radius = 2, velocity = vector(0,0,0), make_trail = True)                 #rocket object
tgt = cone(pos = vector(-400, 200, 0), axis = (10, 0,0), radius = 5, velocity = vector(50,0,0))                             #'airplane' object

LOSrate = 0                                                                     # at first LOSrate must be set to 0
N = 5.0                                                                         # navigation gain which is usually from 3 to 5
V = 0                                                                           # velocity at which rocket is closing to a target
RTM_old = vector(0,0,0)                                                         # need to make RTM_old vector and make it (0,0,0) in order to work properly in the beginning

while 1:
    rate(60)                                                                    # kind of framerate
    RTM_new = tgt.pos - rocket.pos                                              # it's a 'view' vector - vector that has beginning on rocket and end on target

    if mag(RTM_old) == 0:                                                       # first iteration - need to set some values
        deltaLOS = vector(0,0,0)
        LOSrate = 0
    else:
        deltaLOS = norm(RTM_new) - norm(RTM_old)                                # the difference between old and new 'view' vector
        LOSrate = mag(deltaLOS)                                                 # LOSrate is change between old and new 'view' vector

    RTM_old = RTM_new

    V = -LOSrate

    a = V * N * LOSrate                                                         # main equation which is a 'heart' of proportional navigation

    avec = RTM_new                                                              # avec is acceleration vector, which is added to the velocity of rocket
    avec = rotate(avec, angle = (pi/2))                                         # I needed to make this in order to rotate it 90 degrees as acceleration is perpendicular
    avec.mag = a

    rocket.velocity += avec * 1000                                              # just physics engine, adding vectors etc. needed to multiply avec by 1000 as a is pretty small number
    rocket.pos += rocket.velocity * 0.1                                         # a velocity constant is 0.1 so the cones aren't moving too fast
    rocket.axis = avec * 1000                                                    # changing the heading of rocket so it looks like it's turning
    rocket.axis.mag = 10


    tgt.pos += tgt.velocity * 0.1

    dist = hypot((tgt.pos.x - rocket.pos.x), (tgt.pos.y - rocket.pos.y))        # distance between two bodies

    scene.center = rocket.pos                                                   # still centering view
    if dist <= 1:
        break
