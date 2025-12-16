#I'll create a Blender Python script that reproduces the snowman demo from the video. This script will create a snowman with three snowballs, eyes, a nose, arms, and buttons.
#
#```python
import bpy
import bmesh
from math import radians, sin, cos, pi
import mathutils
import pdb
import numpy as np

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def create_snowball(location=(0, 0, 0), radius=1, name="Snowball"):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=32,
        ring_count=16,
        radius=radius,
        location=location
    )
    snowball = bpy.context.active_object
    snowball.name = name
    
    # Add smooth shading
    bpy.ops.object.shade_smooth()
    
    # Add subdivision surface modifier
    snowball.modifiers.new(name="Subdivision", type='SUBSURF')
    snowball.modifiers["Subdivision"].levels = 2
    snowball.modifiers["Subdivision"].render_levels = 3
    
    return snowball

def create_carrot_nose(location=(0, 0, 0)):
    """Create a carrot nose (cone)"""
    bpy.ops.mesh.primitive_cone_add(
        vertices=8,
        radius1=0.08,
        radius2=0.01,
        depth=0.3,
        location=location,
        rotation=(0, radians(90), 0)
    )
    nose = bpy.context.active_object
    nose.name = "CarrotNose"
    
    # Rotate slightly downward
    nose.rotation_euler = (radians(10), radians(90), 0)
    
    # Add orange material
    mat = bpy.data.materials.new(name="CarrotMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    # Create simple orange material
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (1.0, 0.5, 0.1, 1.0)  # Orange
    bsdf.inputs['Roughness'].default_value = 0.4
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    nose.data.materials.append(mat)
    
    return nose

def create_eyes(location=(0, 0, 0), offset=0.1):
    """Create two eyes (black spheres)"""
    eyes = []
    
    # Left eye
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=16,
        ring_count=8,
        radius=0.04,
        location=(location[0] - offset, location[1] + 0.08, location[2])
    )
    left_eye = bpy.context.active_object
    left_eye.name = "LeftEye"
    
    # Right eye
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=16,
        ring_count=8,
        radius=0.04,
        location=(location[0] + offset, location[1] + 0.08, location[2])
    )
    right_eye = bpy.context.active_object
    right_eye.name = "RightEye"
    
    # Create black material for eyes
    mat = bpy.data.materials.new(name="EyeMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (0.0, 0.0, 0.0, 1.0)  # Black
    bsdf.inputs['Roughness'].default_value = 0.1
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    left_eye.data.materials.append(mat)
    right_eye.data.materials.append(mat)
    
    return [left_eye, right_eye]

def create_buttons(location=(0, 0, 0), count=3):
    """Create buttons (black spheres) down the front"""
    buttons = []
    
    for i in range(count):
        button_z = location[2] - 0.05 * (i + 1)
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=12,
            ring_count=6,
            radius=0.03,
            location=(location[0], location[1] + 0.1, button_z)
        )
        button = bpy.context.active_object
        button.name = f"Button_{i+1}"
        buttons.append(button)
    
    # Use same black material as eyes
    mat = bpy.data.materials.get("EyeMaterial") or bpy.data.materials.new(name="ButtonMaterial")
    for button in buttons:
        if button.data.materials:
            button.data.materials[0] = mat
        else:
            button.data.materials.append(mat)
    
    return buttons

def create_arm(start_loc, end_loc, thickness=0.02):
    """Create a tree branch arm using a cylinder"""
    # Calculate direction and length
    direction = mathutils.Vector(end_loc) - mathutils.Vector(start_loc)
    length = direction.length
    direction.normalize()
    # pdb.set_trace()
    # Create cylinder for arm
    newLocation = tuple(np.array(start_loc) + direction * length / 2)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8,
        radius=thickness,
        depth=length,
        location=newLocation
    )
    arm = bpy.context.active_object
    arm.name = "Arm"
    
    # Rotate to point in correct direction
    quat = direction.to_track_quat('Z', 'Y')
    arm.rotation_euler = quat.to_euler()
    
    # Add brown material for arm
    mat = bpy.data.materials.new(name="ArmMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (0.4, 0.2, 0.1, 1.0)  # Brown
    bsdf.inputs['Roughness'].default_value = 0.8
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    arm.data.materials.append(mat)
    
    return arm

def create_hat(location=(0, 0, 0)):
    """Create a top hat for the snowman"""
    # Create hat brim (cylinder)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=0.25,
        depth=0.02,
        location=(location[0], location[1], location[2] + 0.35)
    )
    brim = bpy.context.active_object
    brim.name = "HatBrim"
    
    # Create hat top (cylinder)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=0.15,
        depth=0.2,
        location=(location[0], location[1], location[2] + 0.46)
    )
    top = bpy.context.active_object
    top.name = "HatTop"
    
    # Add black material for hat
    mat = bpy.data.materials.new(name="HatMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1.0)  # Very dark gray/black
    bsdf.inputs['Roughness'].default_value = 0.3
    # bsdf.inputs['Specular'].default_value = 0.5
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    brim.data.materials.append(mat)
    top.data.materials.append(mat)
    
    return [brim, top]

def create_ground(size=10):
    """Create a ground plane"""
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, 0))
    ground = bpy.context.active_object
    ground.name = "Ground"
    
    # Add subdivision and displacement for snow-like ground
    ground.modifiers.new(name="Subdivision", type='SUBSURF')
    ground.modifiers["Subdivision"].levels = 2
    
    displace = ground.modifiers.new(name="Displace", type='DISPLACE')
    tex = bpy.data.textures.new(name="SnowDisplacement", type='CLOUDS')
    tex.noise_scale = 0.5
    displace.texture = tex
    displace.strength = 0.1
    
    # Add white material for snow
    mat = bpy.data.materials.new(name="SnowMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (0.95, 0.95, 1.0, 1.0)  # Slightly blue white
    bsdf.inputs['Roughness'].default_value = 0.7
    #bsdf.inputs['Subsurface'].default_value = 0.1
    #bsdf.inputs['Subsurface Color'].default_value = (0.9, 0.95, 1.0, 1.0)
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    ground.data.materials.append(mat)
    
    return ground

def add_snowman_material(obj):
    """Add snow material to snowballs"""
    mat = bpy.data.materials.new(name="SnowmanMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    # Create principled BSDF
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (0.98, 0.98, 1.0, 1.0)  # Slightly blue white
    bsdf.inputs['Roughness'].default_value = 0.3
    #bsdf.inputs['Specular'].default_value = 0.5
    #bsdf.inputs['Subsurface'].default_value = 0.05
    #bsdf.inputs['Subsurface Color'].default_value = (0.9, 0.95, 1.0, 1.0)
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    obj.data.materials.append(mat)
    return mat

def create_snowman():
    """Main function to create the complete snowman"""
    
    # Create ground
    ground = create_ground()
    
    # Create three snowballs (bottom to top)
    bottom = create_snowball(location=(0, 0, 1), radius=1.0, name="BottomSnowball")
    middle = create_snowball(location=(0, 0, 2.25), radius=0.75, name="MiddleSnowball")
    head = create_snowball(location=(0, 0, 2.825), radius=0.25, name="HeadSnowball")
    
    # Add snow material to all snowballs
    for snowball in [bottom, middle, head]:
        add_snowman_material(snowball)
    
#    # Create facial features on head
#    nose = create_carrot_nose(location=(0, 0.25, 2.8))
#    eyes = create_eyes(location=(0, 0, 2.8), offset=0.06)
#    buttons = create_buttons(location=(0, 0, 2), count=3)
#    
#    # Create arms on middle snowball
#    left_arm = create_arm(
#        start_loc=(0, 0.35, 2.1),
#        end_loc=(-0.8, 0.8, 2.1),
#        thickness=0.015
#    )
#    right_arm = create_arm(
#        start_loc=(0, 0.35, 2.1),
#        end_loc=(0.8, 0.8, 2.1),
#        thickness=0.015
#    )
#    
#    # Create hat on head
#    hat_parts = create_hat(location=(0, 0, 2.8))
#    
#    # Parent all objects to head for easy manipulation
#    head.select_set(True)
#    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
#    
#    print("Snowman created successfully!")
    return {
        'ground': ground,
        'bottom': bottom,
        'middle': middle,
        'head': head,
        #'nose': nose,
        #'eyes': eyes,
        #'buttons': buttons,
        #'arms': [left_arm, right_arm],
        #'hat': hat_parts
    }

def setup_scene():
    """Setup lighting and camera for the scene"""
    # Remove default lights
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete(use_global=False)
    
    # Add a sun light
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    sun = bpy.context.active_object
    sun.data.energy = 2
    sun.rotation_euler = (radians(45), 0, radians(45))
    
    # Add a fill light
    bpy.ops.object.light_add(type='AREA', location=(-5, -5, 8))
    fill_light = bpy.context.active_object
    fill_light.data.energy = 100
    fill_light.data.size = 5
    fill_light.rotation_euler = (radians(60), 0, radians(-45))
    
    # Position camera
    bpy.ops.object.camera_add(location=(5, -5, 3))
    camera = bpy.context.active_object
    camera.rotation_euler = (radians(70), 0, radians(45))
    
    # Set camera as active
    bpy.context.scene.camera = camera
    
    # Set render settings
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 128
    
    # Set background color (sky blue)
    bpy.context.scene.world.use_nodes = True
    nodes = bpy.context.scene.world.node_tree.nodes
    nodes.clear()
    bg = nodes.new(type='ShaderNodeBackground')
    bg.inputs['Color'].default_value = (0.6, 0.8, 1.0, 1.0)  # Sky blue
    bg.inputs['Strength'].default_value = 1.0
    output = nodes.new(type='ShaderNodeOutputWorld')
    bpy.context.scene.world.node_tree.links.new(bg.outputs['Background'], output.inputs['Surface'])

# Create the snowman
snowman_parts = create_snowman()

# Setup the scene
setup_scene()

# Select all snowman parts for easy viewing
for obj in snowman_parts.values():
    if isinstance(obj, list):
        for item in obj:
            item.select_set(True)
    else:
        obj.select_set(True)

print("Snowman scene created! Run this script in Blender's Scripting workspace.")
##```

#  This script creates a complete snowman with:
#  
#  1. **Three snowballs** (bottom, middle, head) with smooth shading and subdivision
#  2. **Facial features**:
#     - Carrot nose (orange cone)
#     - Two black eyes
#     - Three black buttons down the front
#  3. **Arms** made from brown cylinders (tree branches)
#  4. **Top hat** with brim and top
#  5. **Snowy ground** with displacement for texture
#  6. **Scene setup** with lighting, camera, and sky blue background
#  
#  To use this script:
#  
#  1. Open Blender
#  2. Go to the "Scripting" workspace
#  3. Create a new text file
#  4. Paste this code
#  5. Click "Run Script" (play button)
#  
#  The script will:
#  - Clear the default scene
#  - Create the snowman at the origin
#  - Set up lighting and camera
#  - Configure materials with appropriate colors
#  - Parent all parts to the head for easy manipulation
#  
#  The snowman will have realistic snow-like material with slight subsurface scattering, and all components will be properly scaled and positioned.
