"""
created by Bradley Sheneman

uses constants defined by SpockBot physics.py
changed the walk, sprint, jump functions to a single getMovementFrames() function for code clarity
added getLookFrames() function to allow for changing head position without moving

more importantly, it allows for single movements that are composites of
different motions (e.g. jump while walking northeast)


"""


# Gravitational constants defined in blocks/(client tick)^2
PLAYER_ENTITY_GAV = 0.08
THROWN_ENTITY_GAV = 0.03
RIDING_ENTITY_GAV = 0.04
BLOCK_ENTITY_GAV  = 0.04
ARROW_ENTITY_GAV  = 0.05

# Air drag constants defined in 1/tick
PLAYER_ENTITY_DRG = 0.02
THROWN_ENTITY_DRG = 0.01
RIDING_ENTITY_DRG = 0.05
BLOCK_ENTITY_DRG  = 0.02
ARROW_ENTITY_DRG  = 0.01

# Player ground acceleration isn't actually linear, but we're going to pretend
# that it is. Max ground velocity for a walking client is 0.215blocks/tick, it
# takes a dozen or so ticks to get close to max velocity. Sprint is 0.28, just
# apply more acceleration to reach a higher max ground velocity
PLAYER_WLK_ACC    = 0.15
PLAYER_SPR_ACC    = 0.20
PLAYER_GND_DRG    = 0.41

# we can add more if there are more speeds that a player can move
motions = { 1: PLAYER_WLK_ACC,
            2: PLAYER_SPR_ACC }

# Seems about right, not based on anything
PLAYER_JMP_ACC    = 0.45

import math
import visibility as vis

# returns as many frames as necessary to go the requested distance
# in a straight line, and at the requested speed
# frames frequency determined by the frequency of 'action_tick' event in Spock
def getMovementFrames(pos, direction, dist, speed, jump):

    d_dist = motions[speed]
    frames = []
    traveled = 0.
    
    while traveled < dist:
        frame = {}
        
        # in this case, direction should be a correct yaw in 'Minecraft terms'
        dx, dy, dz = vis.calcRayStep(0, direction, d_dist)
        
        frame['x'] = x + dx
        frame['z'] = x + dz

        if jump:
            if pos['on_ground']:
                frame['on_ground'] = False
                frame['y'] = PLAYER_JMP_ACC
            else:
                frame['on_ground'] = True
                frame['y'] = pos['y']
            jump = False
        else:
            frame['on_ground'] = pos['on_ground']
            frame['y'] = pos['y']

        frame['pitch'] = pos['pitch']
        frame['yaw'] = pos['yaw']
        
        frames.append(frame)
        traveled += d_dist

    return frames


# currently only one frame returned, may need higher resolution
def getLookFrames(pos, pitch, yaw):
    
    frames = []
    
    frame = pos
    frame['pitch'] = pitch
    frame['yaw'] = yaw
    
    print frame

    frames.append(frame)

    return frames



