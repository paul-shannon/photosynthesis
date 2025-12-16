import bpy
import pdb

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

def addHat():
   bpy.ops.mesh.primitive_cylinder_add(location=(0,0,3.46), scale=(0.9, 0.9, 0.05))
   hatBrim = bpy.context.active_object
   hatBrim.name = "hatBrim"

   bpy.ops.mesh.primitive_cylinder_add(location=(0,0,3.9), scale=(0.54, 0.54, 0.3))
   stovepipe = bpy.context.active_object
   stovepipe.name = "stovepipe"

   return (stovepipe, hatBrim)

def createSnowman():
    clearScene()
    body = createSnowball(1.0, 0, 0, 1, "body")
    torso = createSnowball(0.75, 0, 0, 2, "torso")
    head = createSnowball(0.5, 0, 0, 3, "head") 
    addSnowMaterial(body)
    addSnowMaterial(torso)
    addSnowMaterial(head)
    addHat()
    return [body, torso, head]

clearScene()
createSnowman()

#addSnowballMaterial(torso)


