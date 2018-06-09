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
DEPTH_RANDOM = (1.0,4.0)
CRYSTAL_RADIUS_RANDOM = (1.4,1.8)
SPIKE_RANDOM = (1.3,1.6)
UP_RANDOM = (1.0,1.5);
ROTATION_RANDOM = (0.1,0.3)
def AddMaterial(material,ob):
   
    # Get material
    mat = bpy.data.materials.get(material)
    #mat = bpy.data.materials.new(name="Crystal")
    #bpy.context.object.active.data.materials.append(mat)
    #bpy.context.object.active_material.diffuse_color = (1, 0, 0)
    if mat is None:
        # create material
        mat = bpy.data.materials.new(name=material)
    # Assign it to object
    if ob.data.materials:
        ob.data.materials[0] = mat
    else:
        ob.data.materials.append(mat)

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
        if(v.co.z >= 0):
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
    mod = obj.modifiers.new('Bevel', 'BEVEL')
    mod.segments = 4
    mod.width = 0.02
    AddMaterial('Ground',obj)
def CreateCrystalRing(NUMBER_OF_CRISTALS,POSITION_RADIUS,HIGHT,ROTATION):
    ANGLE_STEP = 2*pi/NUMBER_OF_CRISTALS;
    for i in range(NUMBER_OF_CRISTALS):
        DEPTH = HIGHT*random.uniform(DEPTH_RANDOM[0],DEPTH_RANDOM[1])
        EXPOSURE = random.uniform(DEPTH_RANDOM[0],DEPTH_RANDOM[1])* 0.25;
        loc = (POSITION_RADIUS*cos(i*ANGLE_STEP),POSITION_RADIUS*sin(i*ANGLE_STEP),DEPTH*0.5 +EXPOSURE)
        RM= ROTATION*random.uniform(ROTATION_RANDOM[0],ROTATION_RANDOM[1])
        RM2= ROTATION*random.uniform(ROTATION_RANDOM[0],ROTATION_RANDOM[1])
        N_VERTICES = random.randint(5,6)
        rot = (-sin(i*ANGLE_STEP)*RM,cos(i*ANGLE_STEP)*RM2,0.0)
        RADIUS = random.uniform(CRYSTAL_RADIUS_RANDOM[0],CRYSTAL_RADIUS_RANDOM[1]) 
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.mesh.primitive_cylinder_add(vertices = N_VERTICES, radius = RADIUS/2,location = loc,rotation =rot,depth = DEPTH)
        (verts,obj) = GetMeshVerts()
        CreateSpike(verts,DEPTH,obj)
        mod = obj.modifiers.new('Bevel', 'BEVEL')
        mod.segments = 4
        mod.width = 0.005
        AddMaterial('Crystal',obj)

def CreateSpike(verts,depth,obj):
    x,y,z = 0,0,0
    n = 0
    up = []
    for v in verts:
        co_final =  v.co
        if(co_final.z > depth*0.25):
            co_final.x *= random.uniform(UP_RANDOM[0],UP_RANDOM[1])
            x += co_final.x
            co_final.y *= random.uniform(UP_RANDOM[0],UP_RANDOM[1])
            y += co_final.y
            co_final.z *= random.uniform(UP_RANDOM[0],UP_RANDOM[1])
            z += co_final.z
            n += 1;
            up.append(v)
    SPIKE = random.uniform(SPIKE_RANDOM[0],SPIKE_RANDOM[1])
    x *= SPIKE/n;
    y *= SPIKE/n;
    z *= SPIKE/n;
    print(x,y,z)
    #bpy.ops.mesh.primitive_ico_sphere_add(location=(x,y,z),size = 0.2)
    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.new((x,y,z))
    bm.verts.ensure_lookup_table()
    for i in range(n):
        bm.faces.new((bm.verts[-1], up[i],up[(i+1) % n]))
        bm.faces.ensure_lookup_table()
    
            
            
CreateGround()
CreateCrystalRing(8,1.4,0.7,1.2)
CreateCrystalRing(4,0.7,1.3,1.1)
CreateCrystalRing(1,0.3,1.9,1.0)

