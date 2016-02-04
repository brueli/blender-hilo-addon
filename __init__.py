


bl_info = {
	"name": "High- and Lowpoly Mesh Tools",
	"author": "Ramon Brülisauer",
	"version": (0, 0, 20160119),
	"blender": (2, 76, 0),
	"location": "Properties > Scene > High-/Lowpoly Mesh, Properties > Object > High-/Lowpoly Mesh",
	"description": "Blender addon for working with high and lowpoly meshes",
	"warning": "Beta Version",
	"wiki_url": "https://github.com/brueli/blender-hilo-addon/wiki",
	"tracker_url": "https://github.com/brueli/blender-hilo-addon/issues",
	"category": "Mesh"}


import bpy
import re


# properties
# hint: enum_items = [(id, name, desc, icon, number), ... ]
lowpolymeshsuffix_prop = bpy.props.StringProperty(name="Low Poly Suffix", description="Contains the low poly mesh name suffix, which declares a mesh as a `lowpoly` mesh", default="_low")
highpolymeshsuffix_prop = bpy.props.StringProperty(name="High Poly Suffix", description="Contains the high poly mesh name suffix, which declares a mesh as a `highpoly mesh`", default="_high")
groupdetectionmode_enum = [("mesh-group-by-name", "Mesh-Group-by-name", "Use `Group Name Pattern` and object names to detect model features."),
                           ("mesh-group-by-property", "Mesh-Group-by-property", "Use hilo's object properties `Mesh Type` and `Mesh Group` to detect model features.")]
groupdetectionmode_prop = bpy.props.EnumProperty(name="Mesh Group Detection", items=groupdetectionmode_enum, description="Select a strategy to detect model features (=Blender Objects) which are joined together into a single mesh when final mesh operators are applied.", default='mesh-group-by-name')
groupnamepattern_prop = bpy.props.StringProperty(name="Group Name Pattern", description="Object Naming Pattern for `Detect Mesh-Group-by-object-name`-feature", default="$group$res.*")
helpernamepattern_prop = bpy.props.StringProperty(name="Helper Object Name Pattern", description="Helper Object Naming Pattern for `Detect Mesh-Group-by-object-name`-feature", default="$group:*")
outputformat_enum = [("fbx", "Export as .fbx", "Export models in .fbx Format (FBX)"),
                     ("obj", "Export as .obj", "Export models in .obj Format (Wavefront)")]
outputformat_prop = bpy.props.EnumProperty(name="Output Format", items=outputformat_enum, description="Selected output format for export operations")
outputpath_prop = bpy.props.StringProperty(name="Output Directory", description="Stores the output directory path used for export", default="//")
lowpolyfilename_prop = bpy.props.StringProperty(name="Lowpoly Filename", description="Lowpoly model filename", default="mymodel_low")
highpolyfilename_prop = bpy.props.StringProperty(name="Highpoly Filename", description="Highpoly model filename", default="mymodel_high")
cagefilename_prop = bpy.props.StringProperty(name="Cage Filename (if any)", description="Cage model filename. A cage file is only created if there are any cage objects defined.", default="mymodel_cage")
meshtype_enum = [("ignore", "Ignore", "Ignore mesh in lowpoly and highpoly model"),
                 ("lowpoly", "Lowpoly Mesh", "Use mesh for lowpoly model"),
                 ("highpoly", "Highpoly Mesh", "Use mesh for highpoly model"),
                 ("origin", "Origin", "Use this object's location as origin for the model")]
meshtype_prop = bpy.props.EnumProperty(name="Mesh Type", items=meshtype_enum, description="Contains the mesh type", default="ignore")
meshgroup_prop = bpy.props.StringProperty(name="Mesh Group", description="Adds this object to the named Mesh Group when using `Detect Mesh-Group-by-property`-feature", default="")
autounwrap_enum = [("none", "None", "No UV unwrap"),
                   ("smart-unwrap", "Smart Project", "Use `Smart Project` method for UV unwrap"),
                   ("cube-project", "Cube Project", "Use `Cube Projection` method for UV unwrap"),
                   ("unwrap", "Angle Based", "Use default `Angle Based Unwrap` method for UV unwrap")]
autounwrap_prop = bpy.props.EnumProperty(name="Lowpoly UV Unwrap", items = autounwrap_enum, description="Select unwrap method for automatic UV unwrapping on final lowpoly mesh", default="none")
unwrap_mode_prop = bpy.props.EnumProperty(name="UV Unwrap", items = autounwrap_enum, description="Select unwrap method for this object", default="none")
unwrap_sharedCorrectAspect_prop = bpy.props.BoolProperty(name="Correct Aspect", description="`Correct Aspect` parameter for `Unwrap` amd `Cube Project` mode", default=True)
unwrap_sharedMargin_prop = bpy.props.FloatProperty(name="Margin", description="`Margin` parameter for `Unwrap` and `Smart Project` mode", default=0.001)
unwrap_defaultFillHoles_prop = bpy.props.BoolProperty(name="Fill Holes", description="`Fill Holes` parameter for `Unwrap` mode", default=True)
unwrap_defaultUseSubsurf_prop = bpy.props.BoolProperty(name="Use Subsurf", description="`Use Subsurf` parameter for `Unwrap` mode", default=False)
unwrap_cubeScale_prop = bpy.props.FloatProperty(name="Cube Scale", description="`Cube Scale` parameter for 'Cube Projection' mode", default=1.0)
unwrap_cubeClipToBounds_prop = bpy.props.BoolProperty(name="Clip To Bounds", description="`Clip To Bounds` parameter for `Cube Project` mode", default=False)
unwrap_cubeScaleToBounds_prop = bpy.props.BoolProperty(name="Scale To Bounds", description="`Scale To Bounds` parameter for `Cube Project` mode", default=False)
unwrap_smartAngleLimit_prop = bpy.props.FloatProperty(name="Angle Limit", description="`Angle Limit` parameter for `Smart Project` mode", default=66.0)
unwrap_smartUserAreaWeight_prop = bpy.props.FloatProperty(name="User Area Weight", description="`User Area Weight` parameter for `Smart Project` mode", default=0.0)
unwrap_smartUseAspect_prop = bpy.props.BoolProperty(name="Use Aspect", description="`Use Aspect` parameter for `Smart Project` mode", default=True)

# properties to store general hilo module settings per-scene
bpy.types.Scene.hilo_lowpolymeshsuffix = lowpolymeshsuffix_prop
bpy.types.Scene.hilo_highpolymeshsuffix = highpolymeshsuffix_prop
bpy.types.Scene.hilo_autounwrapmode = autounwrap_prop
bpy.types.Scene.hilo_groupdetectionmode = groupdetectionmode_prop
bpy.types.Scene.hilo_groupnamepattern = groupnamepattern_prop
bpy.types.Scene.hilo_helpernamepattern = helpernamepattern_prop
bpy.types.Scene.hilo_outputformat = outputformat_prop
bpy.types.Scene.hilo_outputpath = outputpath_prop
bpy.types.Scene.hilo_lowpolyfilename = lowpolyfilename_prop
bpy.types.Scene.hilo_highpolyfilename = highpolyfilename_prop
bpy.types.Scene.hilo_cagefilename = cagefilename_prop

# properties to store unwrap settings per-object
# these are used by (hilo) unwrap operators to persist the unwrap settings
bpy.types.Object.hilo_unwrap_mode = unwrap_mode_prop
bpy.types.Object.hilo_unwrap_sharedCorrectAspect = unwrap_sharedCorrectAspect_prop
bpy.types.Object.hilo_unwrap_sharedMargin = unwrap_sharedMargin_prop
bpy.types.Object.hilo_unwrap_defaultFillHoles = unwrap_defaultFillHoles_prop
bpy.types.Object.hilo_unwrap_defaultUseSubsurf = unwrap_defaultUseSubsurf_prop
bpy.types.Object.hilo_unwrap_cubeScale = unwrap_cubeScale_prop
bpy.types.Object.hilo_unwrap_cubeClipToBounds = unwrap_cubeClipToBounds_prop
bpy.types.Object.hilo_unwrap_cubeScaleToBounds = unwrap_cubeScaleToBounds_prop
bpy.types.Object.hilo_unwrap_smartAngleLimit = unwrap_smartAngleLimit_prop
bpy.types.Object.hilo_unwrap_smartUserAreaWeight = unwrap_smartUserAreaWeight_prop
bpy.types.Object.hilo_unwrap_smartUseAspect = unwrap_smartUseAspect_prop

# properties to store meshtype and meshgroup per-object
# these are used by the `Detect Mesh-Group-by-property`-feature to determine the mesh/object usage
bpy.types.Object.hilo_meshtype = meshtype_prop   # object type: 'lowpoly', 'highpoly', 'origin' or 'ignore'
bpy.types.Object.hilo_meshgroup = meshgroup_prop # name of the mesh group this object belongs to


class HiloMeshGroupDetectionStrategy:
    def __init__(self, objects, options):
        self.object_list = objects
        self.options = options
    def findGroupNames(self):
        return []
    def findGroupObjects(self, group):
        return []
    def isOrigin(self, obj):
        return False
    def isLowpolyMesh(self, obj):
        return False
    def isHighpolyMesh(self, obj):
        return False
    

class HiloDetectMeshGroupByNamePattern(HiloMeshGroupDetectionStrategy):
    def __init__(self, objects, options):
        self.groupname_pattern = options['name_pattern']         # bpy.context.scene.hilo_groupnamepattern
        self.helpername_pattern = options['helper_pattern']      # bpy.context.scene.hilo_helpernamepattern
        self.lowpolymeshsuffix = options['lowpolymesh_suffix']   # bpy.context.scene.hilo_lowpolymeshsuffix
        self.highpolymeshsuffix = options['highpolymesh_suffix'] # bpy.context.scene.hilo_highpolymeshsuffix
        return super(HiloDetectMeshGroupByNamePattern, self).__init__(objects, options)
    def groupPattern(self, group_name=None):
        if ((self.groupname_pattern is None) or (self.groupname_pattern == '')):
            self.groupname_pattern = '$group$res.*'
        if (group_name is None):
            group_repl = "(\w+)"
        else:
            group_repl = re.escape(group_name)
        rep = {"$group": group_repl, 
                "$res": "(%s|%s)" % (re.escape(self.lowpolymeshsuffix), re.escape(self.highpolymeshsuffix)),
                ".": re.escape("."),
                ":": re.escape(":"),
                "_": re.escape("_"),
                "*": ".*?"} # define desired replacements here
        rep = dict((re.escape(k), v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        return pattern.sub(lambda m: rep[re.escape(m.group(0))], self.groupname_pattern)
    def helperPattern(self, group_name=None, helper_name=None):
        if (group_name is None):
            group_repl = "(\w+)"
        else:
            group_repl = re.escape(group_name)
        if (helper_name is None): 
            helper_repl = ".*?"
        else: 
            helper_repl = re.escape(helper_name)
        rep = {"$group": group_repl, 
                ".": re.escape("."),
                ":": re.escape(":"),
                "_": re.escape("_"),
                "*": helper_repl } # define desired replacements here
        rep = dict((re.escape(k), v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        return pattern.sub(lambda m: rep[re.escape(m.group(0))], self.helpername_pattern)
    def findGroupNames(self):
        result = []
        for obj in self.object_list:
            m = re.search(self.groupPattern(), obj.name)
            if (not m is None):
                group_name = m.group(1)
                if (not group_name in result):
                    result.append(group_name)
        return result 
    def findGroupObjects(self, group):
        result = []
        for i_obj in range(0, len(self.object_list)):
            obj = self.object_list[i_obj]
            is_pattern_match = not re.search(self.groupPattern(group_name=group), obj.name) is None
            is_aux_match = not re.search(self.helperPattern(group_name=group), obj.name) is None
            if (is_pattern_match or is_aux_match):
                result.append(obj)
        return result
    def isOrigin(self, obj):
        is_match = not re.search(self.helperPattern(helper_name="origin"), obj.name) is None
        return is_match
    def isCage(self, obj):
        is_match = not re.search(self.helperPattern(helper_name="cage"), obj.name) is None
        return is_match
    def isLowpolyMesh(self, obj):
        is_pattern_match = not re.search(self.groupPattern(), obj.name) is None
        is_res_match = obj.name.find(self.lowpolymeshsuffix) > -1
        return is_pattern_match and is_res_match
    def isHighpolyMesh(self, obj):
        is_pattern_match = not re.search(self.groupPattern(), obj.name) is None
        is_res_match = obj.name.find(self.highpolymeshsuffix) > -1
        return is_pattern_match and is_res_match


class HiloDetectMeshGroupByProperty(HiloMeshGroupDetectionStrategy):
    def __init__(self, objects, options):
        return super(HiloDetectMeshGroupByProperty, self).__init__(objects, options)
    def findGroupNames(self):
        result = []
        for obj in self.object_list:
            if ( (not obj.hilo_meshgroup is None) and (obj.hilo_meshgroup != '')):
                group_name = obj.hilo_meshgroup
                if (not group_name in result):
                    result.append(group_name)
        return result 
    def findGroupObjects(self, group):
        result = []
        for i_obj in range(0, len(self.object_list)):
            obj = self.object_list[i_obj]
            is_group = obj.hilo_meshgroup == group
            if (is_group):
                result.append(obj)
        return result
    def isOrigin(self, obj):
        return obj.hilo_meshtype == 'origin'
    def isLowpolyMesh(self, obj):
        return obj.hilo_meshtype == 'lowpoly'
    def isHighpolyMesh(self, obj):
        return obj.hilo_meshtype == 'highpoly'


class HiloMeshGroups:
    def __init__(self, objects=[]):
        self.lowpolymeshsuffix = bpy.context.scene.hilo_lowpolymeshsuffix
        self.highpolymeshsuffix = bpy.context.scene.hilo_highpolymeshsuffix
        self.groupname_pattern = bpy.context.scene.hilo_groupnamepattern
        self.helpername_pattern = bpy.context.scene.hilo_helpernamepattern
        self.object_list = []
        self.group_names = []
        self.groups = {}
        self.addObjects(objects)
    def getMeshGroupDetector(self, more_objects):
        if (bpy.context.scene.hilo_groupdetectionmode == 'mesh-group-by-name'):
            return HiloDetectMeshGroupByNamePattern(more_objects, {
                'name_pattern':        self.groupname_pattern,
                'helper_pattern':      self.helpername_pattern,
                'lowpolymesh_suffix':  self.lowpolymeshsuffix,
                'highpolymesh_suffix': self.highpolymeshsuffix
                })
        elif (bpy.context.scene.hilo_groupdetectionmode == 'mesh-group-by-property'):
            return HiloDetectMeshGroupByProperty(more_objects, {})
    def addObjects(self, more_objects):
        # get the group detector
        groupDetector = self.getMeshGroupDetector(more_objects)
        # find group names and add them to the list of group names
        new_groups = groupDetector.findGroupNames()
        for group_name in new_groups:
            if (not group_name in self.group_names):
                self.group_names.append(group_name)
        # find group members and add them to the object list and to the group list
        for i_group in range(0, len(self.group_names)):
            group_objects = groupDetector.findGroupObjects(self.group_names[i_group])
            for obj in group_objects:
                if (not obj in self.object_list):
                    i_obj = len(self.object_list)
                    self.object_list.append(obj)
                    if (not i_group in self.groups):
                        self.groups[i_group] = []
                    self.groups[i_group].append(i_obj)
    def getGroup(self, group, types=['ANY']):
        if (type(group)==str):
            group = self.group_names.index(group)
        result = []
        for i_obj in self.groups[group]:
            if ('ANY' in types):
                result.append(self.object_list[i_obj])
            elif (self.object_list[i_obj].type in types):
                result.append(self.object_list[i_obj])
        return result
    def getOrigin(self, group):
        mg = self.getMeshGroupDetector([])
        if (type(group)==str):
            group = self.group_names.index(group)
        for i_obj in self.groups[group]:
            if (mg.isOrigin(self.object_list[i_obj])):
                return self.object_list[i_obj].location
        return bpy.context.scene.cursor_location
    def getCage(self, group):
        mg = self.getMeshGroupDetector([])
        if (type(group)==str):
            group = self.group_names.index(group)
        for i_obj in self.groups[group]:
            if (mg.isCage(self.object_list[i_obj])):
                return self.object_list[i_obj]
        return None
    def getLowpolyMeshes(self, group):
        mg = self.getMeshGroupDetector([])
        result = []
        for group_obj in self.getGroup(group, ['MESH']):
            if (mg.isLowpolyMesh(group_obj)):
                result.append(group_obj)
        return result
    def getHighpolyMeshes(self, group):
        mg = self.getMeshGroupDetector([])
        result = []
        for group_obj in self.getGroup(group, ['MESH']):
            if (mg.isHighpolyMesh(group_obj)):
                result.append(group_obj)
        return result
    def groupCount(self):
        return len(self.group_names)


class HiloObjectUnwrapSettingsPanel(bpy.types.Panel):
    bl_label = "Unwrap Settings"
    bl_idname = "HiloObjectUnwrapSettingsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        # set unwrap mode
        row = layout.row()
        rowcol = row.column(align=True)
        rowcol.label(text="Unwrap Mode")
        rowcol = row.column(align=True)
        rowcol.prop(context.object, "hilo_unwrap_mode", text="")
        if (context.object.hilo_unwrap_mode == 'unwrap'):
            # set fill holes
            row = layout.row()
            rowcol = row.column(align=True)
            rowcol.label(text="Fill Holes")
            rowcol = row.column(align=True)
            rowcol.prop(context.object, "hilo_unwrap_defaultFillHoles", text="")
            # set correct aspect
            row = layout.row()
            rowcol = row.column(align=True)
            rowcol.label(text="Correct Aspect")
            rowcol = row.column(align=True)
            rowcol.prop(context.object, "hilo_unwrap_sharedCorrectAspect", text="")
            # set use subsurf
            row = layout.row()
            rowcol = row.column(align=True)
            rowcol.label(text="Use Subsurf")
            rowcol = row.column(align=True)
            rowcol.prop(context.object, "hilo_unwrap_defaultUseSubsurf", text="")
            # set margin
            row = layout.row()
            rowcol = row.column(align=True)
            rowcol.label(text="Margin")
            rowcol = row.column(align=True)
            rowcol.prop(context.object, "hilo_unwrap_sharedMargin", text="")
        # cube-project mode:
        elif (context.object.hilo_unwrap_mode == 'cube-project'):
            # set cube scale
            row = layout.row()
            rowcol = row.column(align=True)
            rowcol.label(text="Cube Scale")
            rowcol = row.column(align=True)
            rowcol.prop(context.object, "hilo_unwrap_cubeScale", text="")
            # set correct aspect
            row = layout.row()
            rowcol = row.column(align=True)
            rowcol.label(text="Correct Aspect")
            rowcol = row.column(align=True)
            rowcol.prop(context.object, "hilo_unwrap_sharedCorrectAspect", text="")
            # set clip to bounds
            row = layout.row()
            rowcol = row.column(align=True)
            rowcol.label(text="Clip To Bounds")
            rowcol = row.column(align=True)
            rowcol.prop(context.object, "hilo_unwrap_cubeClipToBounds", text="")
            # set scale to bounds
            row = layout.row()
            rowcol = row.column(align=True)
            rowcol.label(text="Scale To Bounds")
            rowcol = row.column(align=True)
            rowcol.prop(context.object, "hilo_unwrap_cubeScaleToBounds", text="")
        # smart-unwrap mode
        elif (context.object.hilo_unwrap_mode == 'smart-unwrap'):
            # set angle limit
            row = layout.row()
            rowcol = row.column(align=True)
            rowcol.label(text="Angle Limit")
            rowcol = row.column(align=True)
            rowcol.prop(context.object, "hilo_unwrap_smartAngleLimit", text="")
            # set island margin
            row = layout.row()
            rowcol = row.column(align=True)
            rowcol.label(text="Island Margin")
            rowcol = row.column(align=True)
            rowcol.prop(context.object, "hilo_unwrap_sharedMargin", text="")
            # set user area weight
            row = layout.row()
            rowcol = row.column(align=True)
            rowcol.label(text="User Area Weight")
            rowcol = row.column(align=True)
            rowcol.prop(context.object, "hilo_unwrap_smartUserAreaWeight", text="")
            # set use aspect
            row = layout.row()
            rowcol = row.column(align=True)
            rowcol.label(text="Use Aspect")
            rowcol = row.column(align=True)
            rowcol.prop(context.object, "hilo_unwrap_smartUseAspect", text="")


class HiloMeshToolObjectPanel(bpy.types.Panel):
    bl_label = "High-/Lowpoly Object"
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

        # set mesh group name for Mesh-Group-by-property
        row = layout.row()
        rowcol = row.column(align=True)
        rowcol.label(text="Mesh Group")
        rowcol = row.column(align=True)
        rowcol.prop(context.object, "hilo_meshgroup", text="")


class HiloMeshToolScenePanel(bpy.types.Panel):
    bl_label = "High-/Lowpoly Settings"
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
        rowcol.prop(context.scene, "hilo_lowpolymeshsuffix", text="")

        # set high poly suffix
        row = layout.row()
        rowcol = row.column(align=True)
        rowcol.label(text="High Poly Object Suffix")
        rowcol = row.column(align=True)
        rowcol.prop(context.scene, "hilo_highpolymeshsuffix", text="")

        # group detection mode
        row = layout.row()
        rowcol = row.column(align=True)
        rowcol.label(text="Mesh Group Detection")
        rowcol = row.column(align=True)
        rowcol.prop(context.scene, "hilo_groupdetectionmode", text="")

        # group name pattern
        row = layout.row()
        rowcol = row.column(align=True)
        rowcol.label(text="Group Name Pattern")
        rowcol = row.column(align=True)
        rowcol.prop(context.scene, "hilo_groupnamepattern", text="")

        # helper object name pattern
        row = layout.row()
        rowcol = row.column(align=True)
        rowcol.label(text="Helper Object Name Pattern")
        rowcol = row.column(align=True)
        rowcol.prop(context.scene, "hilo_helpernamepattern", text="")

        # auto-unwrap mode
        row = layout.row()
        rowcol = row.column(align=True)
        rowcol.label(text="Lowpoly Auto-Unwrap")
        rowcol = row.column(align=True)
        rowcol.prop(context.scene, "hilo_autounwrapmode", text="")

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

        # cage filename
        row = layout.row()
        rowcol = row.column(align=True)
        rowcol.label(text="Cage Filename")
        rowcol = row.column(align=True)
        rowcol.prop(context.scene, "hilo_cagefilename", text="")

        # create final mesh button
        row = layout.row()
        rowcol = row.column(align=True)
        rowcol.label(text="Mesh Generation")

        # export final mesh button
        rowcol = row.column(align=True)
        rowcol.operator("objects.hilorefreshfinalmesh", text="Regenerate Final Meshes")
        rowcol.operator("objects.hiloexportfinalmesh", text="Export Final Meshes")


class HiloCopyUnwrapSettingsToSelected(bpy.types.Operator)  :
    '''Copy unwrap settings from active object to all selected objects'''
    bl_idname = "objects.hilocopyunwrapsettingstoselected"
    bl_label = "Copy unwrap settings from active object to all selected objects"

    def execute(self, context):
        # the active and selected objects
        active_obj = context.active_object
        selected_objects = context.selected_objects
        # report progress
        self.report({'INFO'}, 'copying unwrap settings from `%s`...' % (active_obj.name))
        # loop through selected objects
        for selected_obj in selected_objects:
            # copy unwrap settings from active
            selected_obj.hilo_unwrap_mode = active_obj.hilo_unwrap_mode
            selected_obj.hilo_unwrap_cubeScale = active_obj.hilo_unwrap_cubeScale
            # report progress
            self.report({'INFO'}, '  ... to `%s`' % (selected_obj.name))
        return {'FINISHED'}


class HiloUnwrapSelectedObjects(bpy.types.Operator):
    '''Unwrap all selected objects, according to their unwrap mode'''
    bl_idname = "objects.hilounwrapselectedobjects"
    bl_label = "Unwrap all selected objects"

    def execute(self, context):
        # get the selected objects
        selected_objects = context.selected_objects
        # report progress
        self.report({'INFO'}, 'uv unwrapping `%d` objects' % (len(selected_objects)))
        # ensure object mode
        if (not context.edit_object is None):
            bpy.ops.object.editmode_toggle()
        # unselect all objects
        bpy.ops.object.select_all(action='DESELECT')
        # loop objects
        for selected_obj in selected_objects:
            # skip object if unwrap mode is 'None'
            if (selected_obj.hilo_unwrap_mode == 'none'):
                self.report({'INFO'}, '  uv unwrap `%s`: skip' % (selected_obj.name))
                continue
            # switch object to edit mode
            context.scene.objects.active = selected_obj
            selected_obj.select = True
            bpy.ops.object.editmode_toggle()
            # select all vertices
            bpy.ops.mesh.select_all(action='SELECT')
            # unwrap current object
            if (selected_obj.hilo_unwrap_mode == 'unwrap'):
                op_result = bpy.ops.uv.unwrap(method='ANGLE_BASED',
                                              fill_holes=selected_obj.hilo_unwrap_defaultFillHoles,
                                              correct_aspect=selected_obj.hilo_unwrap_sharedCorrectAspect,
                                              use_subsurf_data=selected_obj.hilo_unwrap_defaultUseSubsurf,
                                              margin=selected_obj.hilo_unwrap_sharedMargin)
                if (op_result == {'FINISHED'}):
                    self.report({'INFO'}, '  uv unwrap `%s`: angle-based unwrap successful' % (selected_obj.name))
                else:
                    self.report({'ERROR'}, '  uv unwrap `%s`: angle-based unwrap failed' % (selected_obj.name))
            elif (selected_obj.hilo_unwrap_mode == 'cube-project'):
                op_result = bpy.ops.uv.cube_project(cube_size=selected_obj.hilo_unwrap_cubeScale, 
                                                    correct_aspect=selected_obj.hilo_unwrap_sharedCorrectAspect, 
                                                    clip_to_bounds=selected_obj.hilo_unwrap_cubeClipToBounds, 
                                                    scale_to_bounds=selected_obj.hilo_unwrap_cubeScaleToBounds)
                if (op_result == {'FINISHED'}):
                    self.report({'INFO'}, '  uv unwrap `%s`: cube projection (scale=%.2f) successful' % (selected_obj.name, selected_obj.hilo_unwrap_cubeScale))
                else:
                    self.report({'ERROR'}, '  uv unwrap `%s`: cube projection (scale=%.2f) failed' % (selected_obj.name, selected_obj.hilo_unwrap_cubeScale))
            elif (selected_obj.hilo_unwrap_mode == 'smart-project'):
                op_result = bpy.ops.uv.smart_project(angle_limit=selected_obj.hilo_unwrap_smartAngleLimit, 
                                                    island_margin=selected_obj.hilo_unwrap_sharedMargin, 
                                                    user_area_weight=selected_obj.hilo_unwrap_smartUserAreaWeight, 
                                                    useAspect=selected_obj.hilo_unwrap_sharedUseAspect)
                if (op_result == {'FINISHED'}):
                    self.report({'INFO'}, '  uv unwrap `%s`: smart unwrap (angle_limit=%.2f) successful' % (selected_obj.name, selected_obj.hilo_unwrap_smartAngleLimit))
                else:
                    self.report({'ERROR'}, '  uv unwrap `%s`: smart unwrap (angle_limit=%.2f) failed' % (selected_obj.name, selected_obj.hilo_unwrap_smartAngleLimit))
            # switch back to object mode
            bpy.ops.object.editmode_toggle()
            # deselect object
            selected_obj.select = False
        # return success
        return {'FINISHED'}


class HiloSetObjectOriginToCursor(bpy.types.Operator):
    """Set object origin to 3D cursor position"""
    bl_idname = "objects.hilosetobjectorigintocursor"
    bl_label = "Set Object Origin to 3D cursor"

    def execute(self, context):
        # get active object
        # get active object name
        source_obj = context.scene.objects.active
        source_obj_name = context.scene.objects.active.name
        
        # add a new mesh at cursor position
        bpy.ops.object.add(type='MESH')
        new_obj = context.scene.objects.active
        new_mesh = new_obj.data

        # remove it's vertices
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.object.mode_set(mode='OBJECT')

        # clone modifiers
        bpy.ops.object.select_all(action='DESELECT')
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


class HiloCreateFinalMesh(bpy.types.Operator):
    """Create final high- and lowpoly meshes"""
    bl_idname = "objects.hilocreatefinalmesh"
    bl_label = "Hilo - Create Final Meshes"

    def execute(self, context):
        # find mesh groups in scene
        groups = HiloMeshGroups(context.scene.objects.values())

        # update scene
        context.scene.update()
        
        # for each group:
        for i_group in range(0, groups.groupCount()):

            # create lowpoly result object
            bpy.ops.object.add(type='MESH')
            lowpoly_result = context.active_object

            # for each lowpoly mesh in group
            final_meshes = []
            for lowpoly_obj in groups.getLowpolyMeshes(i_group):
                # duplicate mesh and apply modifiers
                final_mesh = lowpoly_obj.to_mesh(scene=context.scene, apply_modifiers=True, settings='PREVIEW')
                final_mesh_obj = bpy.data.objects.new(lowpoly_obj.name + ".final", final_mesh)
                context.scene.objects.link(final_mesh_obj)
                final_mesh_obj.location = lowpoly_obj.location
                final_mesh_obj.rotation_euler = lowpoly_obj.rotation_euler.copy()
                final_meshes.append(final_mesh_obj)
            # join temp objects into lowpoly result
            bpy.ops.object.select_all(action='DESELECT')
            for final_mesh in final_meshes:
                final_mesh.select = True
            lowpoly_result.select = True
            context.scene.objects.active = lowpoly_result
            bpy.ops.object.join()
            # rename lowpoly result
            lowpoly_result.name = groups.group_names[i_group] + groups.lowpolymeshsuffix
            # update scene
            context.scene.update()
            # move to group origin
            context.scene.cursor_location = groups.getOrigin(i_group)
            context.scene.objects.active = lowpoly_result
            bpy.ops.objects.hilosetobjectorigintocursor()

            # uv unwrap lowpoly model
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            unwrap_mode = context.scene.hilo_autounwrapmode
            if (unwrap_mode == 'smart-unwrap'):
                bpy.ops.uv.smart_project(island_margin=0.01)
            elif (unwrap_mode == 'unwrap'):
                bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.1)
            elif (unwrap_mode == 'cube-project'):
                bpy.ops.uv.cube_project()
            else:
                pass # none = No auto-unwrap
            bpy.ops.object.mode_set(mode='OBJECT')

            # create highpoly result object
            bpy.ops.object.add(type='MESH')
            highpoly_result = context.active_object

            # for each highpoly mesh
            final_meshes = []
            for highpoly_obj in groups.getHighpolyMeshes(i_group):
                # duplicate mesh and apply modifiers
                final_mesh = highpoly_obj.to_mesh(scene=context.scene, apply_modifiers=True, settings='PREVIEW')
                final_mesh_obj = bpy.data.objects.new(highpoly_obj.name + ".final", final_mesh)
                context.scene.objects.link(final_mesh_obj)
                final_mesh_obj.location = highpoly_obj.location
                final_mesh_obj.rotation_euler = highpoly_obj.rotation_euler.copy()
                final_meshes.append(final_mesh_obj)
            # join temp object into highpoly result
            bpy.ops.object.select_all(action='DESELECT')
            for final_mesh in final_meshes:
                final_mesh.select = True
            highpoly_result.select = True
            context.scene.objects.active = highpoly_result
            bpy.ops.object.join()
            # rename highpoly result
            highpoly_result.name = groups.group_names[i_group] + groups.highpolymeshsuffix
            # update scene
            context.scene.update()
            # move to group origin
            context.scene.cursor_location = groups.getOrigin(i_group)
            context.scene.objects.active = highpoly_result
            bpy.ops.objects.hilosetobjectorigintocursor()

            # get cage mesh for group (if there is one specified)
            cage_obj = groups.getCage(i_group)
            if (not cage_obj is None):
                # create cage result object
                bpy.ops.object.add(type='MESH')
                cage_result = context.active_object
                # duplicate mesh and apply modifiers
                final_mesh = cage_obj.to_mesh(scene=context.scene, apply_modifiers=True, settings='PREVIEW')
                final_mesh_obj = bpy.data.objects.new(cage_obj.name + ".final", final_mesh)
                context.scene.objects.link(final_mesh_obj)
                final_mesh_obj.location = cage_obj.location
                final_mesh_obj.rotation_euler = cage_obj.rotation_euler.copy()
                # join temp object into cage result
                bpy.ops.object.select_all(action='DESELECT')
                final_mesh_obj.select = True
                cage_result.select = True
                context.scene.objects.active = cage_result
                bpy.ops.object.join()
                # rename cage result
                cage_result.name = groups.group_names[i_group] + "_cage"
                # update scene
                context.scene.update()
                # move to group origin
                context.scene.cursor_location = groups.getOrigin(i_group)
                context.scene.objects.active = cage_result
                bpy.ops.objects.hilosetobjectorigintocursor()

        return {'FINISHED'}


class HiloRefreshFinalMesh(bpy.types.Operator):
    '''Recreate final meshes. Existing final meshes are overwritten'''
    bl_idname = "objects.hilorefreshfinalmesh"
    bl_label = "Hilo - Refresh Final Meshes"

    def execute(self, context):
        # create mesh groups
        groups = HiloMeshGroups(context.scene.objects.values())
        # remove existing final meshes
        for i_group in range(0, groups.groupCount()):
            bpy.ops.object.select_all(action='DESELECT')
            for group_name in groups.group_names:
                if (bpy.data.objects.find(group_name + '_low') > -1):
                    lowpoly_final = bpy.data.objects[group_name + '_low']
                    context.scene.objects.unlink(lowpoly_final)
                    bpy.data.objects.remove(lowpoly_final)
                if (bpy.data.objects.find(group_name + '_high') > -1):
                    highpoly_final = bpy.data.objects[group_name + '_high']
                    context.scene.objects.unlink(highpoly_final)
                    bpy.data.objects.remove(highpoly_final)
                if (bpy.data.objects.find(group_name + '_cage') > -1):
                    cage_final = bpy.data.objects[group_name + '_cage']
                    context.scene.objects.unlink(cage_final)
                    bpy.data.objects.remove(cage_final)
        # recreate lowpoly meshes
        bpy.ops.objects.hilocreatefinalmesh()
        return {'FINISHED'}


class HiloExportMeshes(bpy.types.Operator):
    bl_idname = 'objects.hiloexportfinalmesh'
    bl_label = 'Hilo - Export Final Meshes'

    def execute(self, context):
        # find mesh groups in scene
        groups = HiloMeshGroups(context.scene.objects.values())

        # select final lowpoly meshes
        bpy.ops.object.select_all(action='DESELECT')
        for i_group in range(0, groups.groupCount()):
            group_name = groups.group_names[i_group]
            lowpoly_name = group_name + context.scene.hilo_lowpolymeshsuffix
            if (bpy.data.objects.find(lowpoly_name) == -1):
                self.report({'ERROR'}, 'could not find lowpoly mesh %s. Recreate meshes and try again.' % (lowpoly_name))
                return {'FINISHED'}
            bpy.data.objects[lowpoly_name].select = True

        # export selected objects as .fbx
        self.report({'INFO'}, "  export lowpoly to .fbx file")
        exportFilepath = bpy.path.abspath(context.scene.hilo_outputpath + context.scene.hilo_lowpolyfilename + ".fbx")
        bpy.ops.export_scene.fbx(filepath=exportFilepath, 
                                 check_existing=False, 
                                 use_selection=True, 
                                 object_types={'MESH'}, 
                                 use_mesh_modifiers=True, 
                                 bake_anim=False, 
                                 batch_mode='OFF')

        # select final highpoly meshes
        bpy.ops.object.select_all(action='DESELECT')
        for i_group in range(0, groups.groupCount()):
            group_name = groups.group_names[i_group]
            highpoly_name = group_name + context.scene.hilo_highpolymeshsuffix
            if (bpy.data.objects.find(highpoly_name) == -1):
                self.report({'ERROR'}, 'could not find highpoly mesh %s. Recreate meshes and try again.' % (lowpoly_name))
                return {'FINISHED'}
            bpy.data.objects[highpoly_name].select = True

        # export selected objects as .fbx
        self.report({'INFO'}, "  export highpoly to .fbx file")
        exportFilepath = bpy.path.abspath(context.scene.hilo_outputpath + context.scene.hilo_highpolyfilename + ".fbx")
        bpy.ops.export_scene.fbx(filepath=exportFilepath, 
                                 check_existing=False, 
                                 use_selection=True, 
                                 object_types={'MESH'}, 
                                 use_mesh_modifiers=True, 
                                 bake_anim=False, 
                                 batch_mode='OFF')

        # select cage meshes
        bpy.ops.object.select_all(action='DESELECT')
        for i_group in range(0, groups.groupCount()):
            group_name = groups.group_names[i_group]
            cage_name = group_name + '_cage'
            if (bpy.data.objects.find(cage_name) == -1):
                pass
            else:
                bpy.data.objects[cage_name].select = True

        # export selected objects as .fbx
        self.report({'INFO'}, "  export cage to .fbx file")
        export_filepath = bpy.path.abspath(context.scene.hilo_outputpath + context.scene.hilo_cagefilename + ".fbx")
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
    bpy.utils.register_class(HiloObjectUnwrapSettingsPanel)
    bpy.utils.register_class(HiloMeshToolObjectPanel)
    bpy.utils.register_class(HiloMeshToolScenePanel)
    # operators
    bpy.utils.register_class(HiloUnwrapSelectedObjects)
    bpy.utils.register_class(HiloCopyUnwrapSettingsToSelected)
    bpy.utils.register_class(HiloSetObjectOriginToCursor)
    bpy.utils.register_class(HiloCreateFinalMesh)
    bpy.utils.register_class(HiloRefreshFinalMesh)
    bpy.utils.register_class(HiloExportMeshes)
    

def unregister():
    # panels
    bpy.utils.unregister_class(HiloObjectUnwrapSettingsPanel)
    bpy.utils.unregister_class(HiloMeshToolObjectPanel)
    bpy.utils.unregister_class(HiloMeshToolScenePanel)
    # operators
    bpy.utils.unregister_class(HiloUnwrapSelectedObjects)
    bpy.utils.unregister_class(HiloCopyUnwrapSettingsToSelected)
    bpy.utils.unregister_class(HiloSetObjectOriginToCursor)
    bpy.utils.unregister_class(HiloCreateFinalMesh)
    bpy.utils.unregister_class(HiloRefreshFinalMesh)
    bpy.utils.unregister_class(HiloExportMeshes)
    

if (__name__ == "__main__"):
    register()
