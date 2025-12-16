import bpy

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Bottom snowball
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 1))

# Middle snowball  
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.7, location=(0, 0, 2.4))

# Head snowball
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 3.4))

print("Super simple snowman created!")

