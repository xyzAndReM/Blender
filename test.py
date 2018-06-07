import bpy,bmesh
from bpy import data as D
from bpy import context as C
from mathutils import *
from math import *
import random
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()


GROUND_SIZE = 1.0;
POSITION_RADIUS = 1.2;
NUMBER_OF_CRISTALS = 8;
ANGLE_STEP = 2*pi/NUMBER_OF_CRISTALS;
DEPTH_RANDOM = (1.6,3.5)
CRYSTAL_RADIUS_RANDOM = (1.4,1.8)

def GetMeshVerts():
    bpy.ops.object.mode_set(mode = 'EDIT')
    obj = bpy.context.active_object
    bm = bmesh.from_edit_mesh(obj.data)
    return (bm.verts,obj);
def CreateGround():
    bpy.ops.mesh.primitive_ico_sphere_add(location=(0,0,0),size = GROUND_SIZE)
    bpy.context.active_object.name = 'GROUND'
    (verts,obj) = GetMeshVerts()
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
        v.co.x *= random.uniform(2.0,4.0)
        v.co.y *= random.uniform(2.0,4.0)
    for v in up:
        v.co.x *= random.uniform(2.0,3.0)
        v.co.y *= random.uniform(2.0,3.0)
        v.co.z *= random.uniform(1.3,2.2)
def CreateCrystalRing(NUMBER_OF_CRISTALS,POSITION_RADIUS):
    ANGLE_STEP = 2*pi/NUMBER_OF_CRISTALS;
    for i in range(NUMBER_OF_CRISTALS):
        loc = (POSITION_RADIUS*cos(i*ANGLE_STEP),POSITION_RADIUS*sin(i*ANGLE_STEP),1.0)
        RM= random.uniform(0.4,0.7)
        N_VERTICES = random.randint(3,4)
        rot = (-sin(i*ANGLE_STEP)*RM,cos(i*ANGLE_STEP)*RM,0.0)
        DEPTH = random.uniform(DEPTH_RANDOM[0],DEPTH_RANDOM[1])
        RADIUS = random.uniform(CRYSTAL_RADIUS_RANDOM[0],CRYSTAL_RADIUS_RANDOM[1]) 
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.mesh.primitive_cylinder_add(vertices = N_VERTICES, radius = RADIUS/2,location = loc,rotation =rot,depth = DEPTH)
        (verts,obj) = GetMeshVerts()
        CreateSpike(verts,DEPTH,obj)

def CreateSpike(verts,depth,obj):
    x,y,z = 0,0,0
    n = 0
    up = []
    for v in verts:
        co_final =  v.co
        if(co_final.z > depth*0.25):
            x += co_final.x
            y += co_final.y
            z += co_final.z
            n += 1;
            up.append(v)
    x *= 1.5/n;
    y *= 1.5/n;
    z *= 1.5/n;
    print(x,y,z)
    #bpy.ops.mesh.primitive_ico_sphere_add(location=(x,y,z),size = 0.2)
    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.new((x,y,z))
    bm.verts.ensure_lookup_table()
    for i in range(n-1):
        bm.faces.new((bm.verts[-1], up[i],up[i+1]))
        bm.faces.ensure_lookup_table()
    
            
            
CreateGround()
CreateCrystalRing(8,1.2)
CreateCrystalRing(4,0.6)
CreateCrystalRing(1,0.2)



    
