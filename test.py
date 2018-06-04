import bpy,bmesh
from bpy import data as D
from bpy import context as C
from mathutils import *
from math import *
import random

RADIUS = 1.2;
NUMBER_OF_CRISTALS = 8;
ANGLE_STEP = 2*pi/NUMBER_OF_CRISTALS;



bpy.ops.mesh.primitive_ico_sphere_add(location=(0,0,0))
bpy.ops.object.editmode_toggle()
obj = bpy.context.active_object

if obj.mode == 'EDIT':
    # this works only in edit mode,
    bm = bmesh.from_edit_mesh(obj.data)
    verts =  bm.verts

else:
    # this works only in object mode,
    verts = obj.data.vertices

floor = []
up = []
for v in verts:
    if(v.co[2] >= 0):
        v.select = False
        if(v.co[2] == 0):
            floor.append(v)
        else:
            up.append(v)
bpy.ops.mesh.delete(type='VERT')
for v in floor:
    v.co.x *= random.uniform(1.5,3.0)
    v.co.y *= random.uniform(1.5,3.0)
for v in up:
    v.co.x *= random.uniform(1.2,2.5)
    v.co.y *= random.uniform(1.5,2.5)
    v.co.z *= random.uniform(1.3,2.4)
for i in range(8):
    loc = (RADIUS*cos(i*ANGLE_STEP),RADIUS*sin(i*ANGLE_STEP),1.0)
    RM= random.uniform(0.4,0.7)
    N_VERTICES = random.randint(3,4)
    rot = (-sin(i*ANGLE_STEP)*RM,cos(i*ANGLE_STEP)*RM,0.0)
    print(loc)
    bpy.ops.mesh.primitive_cylinder_add(vertices = N_VERTICES, radius = RADIUS/2,location = loc,rotation =rot,depth = 2.0)