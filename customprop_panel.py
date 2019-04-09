import bpy

class BLM_PT_customproperties(bpy.types.Panel):
    """Creates a Rig Properties Panel (Pose Bone Custom Properties) """
    bl_category = "Bone Layers"
    bl_label = "Rig Properties"
    bl_idname = "BLM_PT_customproperties"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}


    @classmethod
    def poll(self, context):

        if context.mode != 'POSE':
            return False
        try:
            return (context.active_object.type == 'ARMATURE')
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        layout = self.layout
        pose_bones = context.active_object.pose.bones
        try:
            selected_bones = [bone.name for bone in context.selected_pose_bones]
            selected_bones += [context.active_pose_bone.name]
        except (AttributeError, TypeError):
            return


        def assign_props(row, val, key, index):
            row.data_path = f"selected_pose_bones[{index}]"
            row.property = key

            try:
                row.value = str(val)
            except:
                pass

        showedit = bpy.context.scene.BLM_ShowPropEdit

        active_pose_bone = context.active_pose_bone

        # Iterate through selected bones add each prop property of each bone to the panel.

        for (index, bone) in enumerate(context.selected_pose_bones):
            if showedit == True:
                row = layout.row(align = True).split(align=True, factor=0.3)
                row.label(text=bone.name, icon='BONE_DATA')
                row.context_pointer_set('active_pose_bone', bone)
                row = row.operator("wm.properties_add", text="Add")
                row.data_path = "active_pose_bone"


            if len(bone.keys()) > 0:
                box = layout.box()
            #row = box.row()
            for key in bone.keys():
                if key not in '_RNA_UI':
                    #box = layout.box()
                    val = bone.get(key, "value")

                    row = box.row()
                    split = row.split(align=True, factor=0.3)
                    row = split.row(align=True)
                    row.label(text=key, translate=False)

                    row = split.row(align=True)
                    row.prop(bone, '["%s"]' % str(key), text = "", slider=True)


                    if showedit == True:
                        split = row.split(align=True, factor=0)

                        row = split.row(align=True)
                        row = row.operator("wm.properties_edit", text="", icon='SETTINGS')
                        assign_props(row, val, key, index)

                        row = split.row(align=False)
                        row = row.operator("wm.properties_remove", text="", icon='X')
                        assign_props(row, val, key, index)
