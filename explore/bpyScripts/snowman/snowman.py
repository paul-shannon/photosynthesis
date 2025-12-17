import bpy
import pdb
import math

def clearScene():
   bpy.ops.object.select_all(action='SELECT')
   bpy.ops.object.delete()


def createSnowball(radius, x, y, z, name):
   bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(x, y, z))
   bpy.ops.object.shade_smooth()
   snowball = bpy.context.active_object
   snowball.name = name
   return snowball
    
def addSnowMaterial(obj):
   mat = bpy.data.materials.new(name="SnowMaterial")
   mat.use_nodes = True
   nodes = mat.node_tree.nodes
   nodes.clear()
   bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
   bsdf.inputs['Base Color'].default_value = (0.8, 0.8, 1, 1.0)  # Slightly blue white
   bsdf.inputs['Roughness'].default_value = 0.3
   output = nodes.new(type='ShaderNodeOutputMaterial')
   mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
   obj.data.materials.append(mat)

def addNoseMaterial(obj):
   mat = bpy.data.materials.new(name="NoseMaterial")
   mat.use_nodes = True
   nodes = mat.node_tree.nodes
   nodes.clear()
   bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
   bsdf.inputs['Base Color'].default_value = (1, 0.4, 0, 1.0)
   bsdf.inputs['Roughness'].default_value = 0.3
   output = nodes.new(type='ShaderNodeOutputMaterial')
   mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
   obj.data.materials.append(mat)

def addHatMaterial(obj):
   mat = bpy.data.materials.new(name="HatMaterial")
   mat.use_nodes = True
   nodes = mat.node_tree.nodes
   nodes.clear()
   bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
   bsdf.inputs['Base Color'].default_value = (0, 0, 0, 1.0)
   bsdf.inputs['Roughness'].default_value = 0.3
   output = nodes.new(type='ShaderNodeOutputMaterial')
   mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
   obj.data.materials.append(mat)

    
def addHat():
   bpy.ops.mesh.primitive_cylinder_add(location=(0,0,3.40),
                                       scale=(0.9, 0.9, 0.05))
   hatBrim = bpy.context.active_object
   hatBrim.name = "hatBrim"

   bpy.ops.mesh.primitive_cylinder_add(location=(0,0,3.7),
                                       scale=(0.54, 0.54, 0.3))
   stovepipe = bpy.context.active_object
   stovepipe.name = "stovepipe"

   return (stovepipe, hatBrim)


def addNose():
   bpy.ops.mesh.primitive_cone_add(location=(0.8, 0.0, 3.0),
                                    rotation=(0.0, math.radians(90.0), 0.0),
                                    radius1=0.1,
                                    radius2=0,
                                    depth=0.8,
                                    vertices=16
                                    )
   nose = bpy.context.active_object
   nose.name = "nose"
   return nose

   #bpy.ops.mesh.primitive_cone_add(location=(1,0,3),
   #                                scale=(0.1, 1, 10),
   #                                rotation=(0,90,0))
    
def createSnowman():
    clearScene()
    body = createSnowball(1.0, 0, 0, 1, "body")
    torso = createSnowball(0.75, 0, 0, 2, "torso")
    head = createSnowball(0.5, 0, 0, 3, "head") 
    addSnowMaterial(body)
    addSnowMaterial(torso)
    addSnowMaterial(head)
    (stovepipe, hatBrim) = addHat()
    addHatMaterial(stovepipe)
    addHatMaterial(hatBrim)
    nose = addNose()
    addNoseMaterial(nose)
    return [body, torso, head]

clearScene()
createSnowman()

#addSnowballMaterial(torso)


