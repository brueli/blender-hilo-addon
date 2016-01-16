﻿


bl_info = {
	"name": "High- and Lowpoly Mesh Tools",
	"author": "Ramon Brülisauer",
	"version": (0, 0, 20160116),
	"blender": (2, 76, 0),
	"location": "Properties > Scene > High-/Lowpoly Mesh, Properties > Object > High-/Lowpoly Mesh",
	"description": "Blender addon for working with high and lowpoly meshes",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Mesh"}


import bpy


# properties
# enum_items = [(id, name, desc, icon, number), ... ]
lowpolysuffix_prop = bpy.props.StringProperty(name="Low Poly Suffix", description="Contains the low poly mesh name suffix, which declares a mesh as a `lowpoly` mesh", default="_low")
highpolysuffix_prop = bpy.props.StringProperty(name="High Poly Suffix", description="Contains the high poly mesh name suffix, which declares a mesh as a `highpoly mesh`", default="_high")
outputpath_prop = bpy.props.StringProperty(name="Output Directory", description="Stores the output directory path used for export", default="//")
lowpolyfilename_prop = bpy.props.StringProperty(name="Lowpoly Filename", description="Lowpoly model filename", default="model_low")
highpolyfilename_prop = bpy.props.StringProperty(name="Highpoly Filename", description="Highpoly model filename", default="model_high")
lowpolymodelname_prop = bpy.props.StringProperty(name="Lowpoly Model", description="Selected Lowpoly Model Object/Group", default="")
highpolymodelname_prop = bpy.props.StringProperty(name="Highpoly Model", description="Selected Highpoly Model Object/Group", default="")


meshtype_enum = [("ignore", "Ignore", "Ignore mesh in lowpoly and highpoly model"),
                 ("lowpoly", "Lowpoly Mesh", "Use mesh for lowpoly model"),
                 ("highpoly", "Highpoly Mesh", "Use mesh for highpoly model")]
meshtype_prop = bpy.props.EnumProperty(name="Mesh Type", items=meshtype_enum, description="Contains the mesh type", default="ignore")

outputformat_enum = [("fbx", "Export as .fbx", "Export models in .fbx Format")]
outputformat_prop = bpy.props.EnumProperty(name="Output Format", items=outputformat_enum, description="Selected output format for export operations")


bpy.types.Scene.hilo_lowpolysuffix = lowpolysuffix_prop
bpy.types.Scene.hilo_highpolysuffix = highpolysuffix_prop
bpy.types.Scene.hilo_outputformat = outputformat_prop
bpy.types.Scene.hilo_outputpath = outputpath_prop
bpy.types.Scene.hilo_lowpolyfilename = lowpolyfilename_prop
bpy.types.Scene.hilo_highpolyfilename = highpolyfilename_prop
bpy.types.Scene.hilo_lowpolymodelname = lowpolymodelname_prop
bpy.types.Scene.hilo_highpolymodelname = highpolymodelname_prop

bpy.types.Object.hilo_meshtype = meshtype_prop



class HiloMeshToolObjectPanel(bpy.types.Panel):
    bl_label = "High-/Lowpoly Mesh"
    bl_idname = "HiloMeshToolsObjectPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):

        layout = self.layout

        # set mesh type
        row = layout.row()
        rowcol = row.column(align=True)
        rowcol.label(text="Mesh Type")
        rowcol = row.column(align=True)
        rowcol.prop(context.object, "hilo_meshtype", text="")

        # show export button
        row = layout.row()
        rowcol = row.column(align=True)
        rowcol.label(text="Export")
        rowcol = row.column(align=True)
        rowcol2 = rowcol.column(align=True)
        if (context.object.hilo_meshtype == 'lowpoly'):
            rowcol2.operator("objects.hiloexportlowpoly", text="Lowpoly To File")
        if (context.object.hilo_meshtype == 'highpoly'):
            rowcol2.operator("objects.hiloexporthighpoly", text="Highpoly To File")


class HiloMeshToolScenePanel(bpy.types.Panel):
    bl_label = "High-/Lowpoly Mesh"
    bl_idname = "HiloMeshToolScenePanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"

    def draw(self, context):

        layout = self.layout

        # set low poly suffix
        row = layout.row()
        rowcol = row.column(align=True)
        rowcol.label(text="Low Poly Object Suffix")
        rowcol = row.column(align=True)
        rowcol.prop(context.scene, "hilo_lowpolysuffix", text="")

        # set high poly suffix
        row = layout.row()
        rowcol = row.column(align=True)
        rowcol.label(text="High Poly Object Suffix")
        rowcol = row.column(align=True)
        rowcol.prop(context.scene, "hilo_highpolysuffix", text="")

        # output format
        row = layout.row()
        rowcol = row.column(align=True)
        rowcol.label(text="Output Format")
        rowcol = row.column(align=True)
        rowcol.prop(context.scene, "hilo_outputformat", text="")

        # output directory
        row = layout.row()
        rowcol = row.column(align=True)
        rowcol.label(text="Output Path")
        rowcol = row.column(align=True)
        rowcol.prop(context.scene, "hilo_outputpath", text="")

        # lowpoly filename
        row = layout.row()
        rowcol = row.column(align=True)
        rowcol.label(text="Lowpoly Filename")
        rowcol = row.column(align=True)
        rowcol.prop(context.scene, "hilo_lowpolyfilename", text="")

        # highpoly filename
        row = layout.row()
        rowcol = row.column(align=True)
        rowcol.label(text="Highpoly Filename")
        rowcol = row.column(align=True)
        rowcol.prop(context.scene, "hilo_highpolyfilename", text="")

        # export options
        # join objects (--> join all meshes following a name pattern before export)
        # apply suffixes (--> add `_low` and `_high` suffixes to resulting meshes)
        # keep modifiers (--> use duplicates for mesh-join)


class HiloSetObjectOriginToCursor(bpy.types.Operator):
    """Set object origin to 3D cursor position"""
    bl_idname = "objects.hilosetobjectorigintocursor"
    bl_label = "Set Object Origin to 3D cursor"

    def execute(self, context):
        # get context object
        # get context object name
        source_obj = context.object
        source_obj_name = context.object.name
        
        # add a new mesh at cursor position
        bpy.ops.object.add(type='MESH')
        new_obj = bpy.context.object
        new_mesh = new_obj.data

        # remove it's vertices
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.object.mode_set(mode='OBJECT')

        # clone modifiers
        source_obj.select = True 
        new_obj.select = True
        context.scene.objects.active = source_obj
        bpy.ops.object.make_links_data(type='MODIFIERS')
        
        # join context object into new mesh
        context.scene.objects.active = new_obj
        bpy.ops.object.join()

        # rename new mesh
        new_obj.name = source_obj_name

        return {'FINISHED'}


class HiloSelectLowPolyMeshes(bpy.types.Operator):
    """Select all low poly mesh objects"""
    bl_idname = "objects.hiloselectlowpoly"
    bl_label = "Select Lowpoly Objects"

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        context.scene.objects.active = None
        for obj in context.scene.objects:
            if (obj.hilo_meshtype == 'lowpoly'):
                obj.select = True 
        return {'FINISHED'}


class HiloSelectHighPolyMeshes(bpy.types.Operator):
    """Select all high poly mesh objects"""
    bl_idname = "objects.hiloselecthighpoly"
    bl_label = "Select Highpoly Objects"

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = None
        for obj in context.scene.objects:
            if (obj.hilo_meshtype == 'highpoly'):
                obj.select = True 
        return {'FINISHED'}


class HiloExportLowPolyMeshes(bpy.types.Operator):
    """Export low poly mesh objects to file"""
    bl_idname = "objects.hiloexportlowpoly"
    bl_label = "Export Lowpoly To File"

    def execute(self, context):

        # select low poly meshes
        bpy.ops.objects.hiloselectlowpoly('INVOKE_DEFAULT')
        self.report({'INFO'}, "%d lowpoly objects selected" % (len(context.selected_objects)))

        # use to_mesh() to duplicate the meshes and apply their modifiers
        # then create a .final object with the new mesh
        # and append it to the list of final meshes
        final_meshes = []
        for lowpoly_obj in bpy.context.selected_objects:
            self.report({'INFO'}, "  creating final mesh %s" % (lowpoly_obj.name))
            final_mesh = lowpoly_obj.to_mesh(scene=context.scene, apply_modifiers=True, settings='PREVIEW')
            final_mesh_obj = bpy.data.objects.new(lowpoly_obj.name + ".final", final_mesh)
            context.scene.objects.link(final_mesh_obj)
            final_mesh_obj.location = lowpoly_obj.location
            final_meshes.append(final_mesh_obj)
        
        # create empty result object
        self.report({'INFO'}, "  creating result object")
        bpy.ops.object.add(type='MESH')
        result_obj = context.active_object
        
        # join final meshes into empty result object
        self.report({'INFO'}, "  joining final meshes")
        bpy.ops.object.select_all(action='DESELECT')
        for final_mesh in final_meshes:
            final_mesh.select = True
        result_obj.select = True
        result_obj.name = context.scene.hilo_lowpolyfilename
        context.scene.objects.active = result_obj
        bpy.ops.object.join()

        # export as .fbx
        self.report({'INFO'}, "  export to .fbx file")
        exportFilepath = bpy.path.abspath(context.scene.hilo_outputpath + context.scene.hilo_lowpolyfilename + ".fbx")
        bpy.ops.export_scene.fbx(filepath=exportFilepath, 
                                 check_existing=False, 
                                 use_selection=True, 
                                 object_types={'MESH'}, 
                                 use_mesh_modifiers=True, 
                                 bake_anim=False, 
                                 batch_mode='OFF')

        return {'FINISHED'}


class HiloExportHighPolyMeshes(bpy.types.Operator):
    """Export high poly mesh objects to file"""
    bl_idname = "objects.hiloexporthighpoly"
    bl_label = "Export Highpoly To File"

    def execute(self, context):
        # select high poly meshes
        bpy.ops.objects.hiloselecthighpoly()
        self.report({'INFO'}, "%d highpoly objects selected" % (len(context.selected_objects)))

        # use to_mesh() to duplicate the meshes and apply their modifiers
        # then create a .final object with the new mesh
        # and append it to the list of final meshes
        final_meshes = []
        for lowpoly_obj in bpy.context.selected_objects:
            self.report({'INFO'}, "  creating final mesh %s" % (lowpoly_obj.name))
            final_mesh = lowpoly_obj.to_mesh(scene=context.scene, apply_modifiers=True, settings='PREVIEW')
            final_mesh_obj = bpy.data.objects.new(lowpoly_obj.name + ".final", final_mesh)
            context.scene.objects.link(final_mesh_obj)
            final_mesh_obj.location = lowpoly_obj.location
            final_meshes.append(final_mesh_obj)
        
        # create empty result object
        self.report({'INFO'}, "  creating result object")
        bpy.ops.object.add(type='MESH')
        result_obj = context.active_object
        
        # join final meshes into empty result object
        self.report({'INFO'}, "  joining final meshes")
        bpy.ops.object.select_all(action='DESELECT')
        for final_mesh in final_meshes:
            final_mesh.select = True
        result_obj.select = True
        result_obj.name = context.scene.hilo_highpolyfilename
        context.scene.objects.active = result_obj
        bpy.ops.object.join()

        # export as .fbx
        self.report({'INFO'}, "  export to .fbx file")
        exportFilepath = bpy.path.abspath(context.scene.hilo_outputpath + context.scene.hilo_highpolyfilename + ".fbx")
        bpy.ops.export_scene.fbx(filepath=exportFilepath, 
                                 check_existing=False, 
                                 use_selection=True, 
                                 object_types={'MESH'}, 
                                 use_mesh_modifiers=True, 
                                 bake_anim=False, 
                                 batch_mode='OFF')

        return {'FINISHED'}




# register/unregister classes in blender
# when blender executes the script as addon, `__name__` is "__main__"
def register():
    # panels
    bpy.utils.register_class(HiloMeshToolObjectPanel);
    bpy.utils.register_class(HiloMeshToolScenePanel);
    # operators
    bpy.utils.register_class(HiloSetObjectOriginToCursor);
    bpy.utils.register_class(HiloSelectLowPolyMeshes);
    bpy.utils.register_class(HiloSelectHighPolyMeshes);
    bpy.utils.register_class(HiloExportLowPolyMeshes);
    bpy.utils.register_class(HiloExportHighPolyMeshes);
    

def unregister():
    # panels
    bpy.utils.unregister_class(HiloMeshToolObjectPanel);
    bpy.utils.unregister_class(HiloMeshToolScenePanel);
    # operators
    bpy.utils.unregister_class(HiloSetObjectOriginToCursor);
    bpy.utils.unregister_class(HiloSelectLowPolyMeshes);
    bpy.utils.unregister_class(HiloSelectHighPolyMeshes);
    bpy.utils.unregister_class(HiloExportLowPolyMeshes);
    bpy.utils.unregister_class(HiloExportHighPolyMeshes);
    

if (__name__ == "__main__"):
    register()
