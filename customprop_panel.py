import bpy

from .blmfuncs import prefs


class BLM_PT_customproperties(bpy.types.Panel):
    # Creates a Rig Properties Panel (Pose Bone Custom Properties)
    bl_category = "Bone Layers"
    bl_label = "Rig Properties"
    bl_idname = "BLM_PT_customproperties"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    @classmethod
    def poll(self, context):
        return getattr(context.active_object, 'pose', None)

    def draw(self, context):
        layout = self.layout


class BLM_PT_customproperties_options(bpy.types.Panel):
    # Creates a Custom Properties Options Subpanel
    bl_idname = "BLM_PT_customproperties_options"
    bl_label = "Display Options"
    bl_parent_id = "BLM_PT_customproperties"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    @classmethod
    def poll(self, context):
        return getattr(context.active_object, 'pose', None)

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop(prefs(), "BLM_ShowPropEdit", text="Edit Mode")
        row.prop(prefs(), "BLM_ShowBoneLabels", text="Bone Name")
        row.prop(prefs(), "BLM_ShowArmatureName", text="Armature Name")


class BLM_PT_customproperties_layout(bpy.types.Panel):
    # Displays a Rig Custom Properties in Subpanel
    bl_category = "Bone Layers"
    bl_label = ""
    bl_idname = "BLM_PT_customproperties_layout"
    bl_parent_id = "BLM_PT_customproperties"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(self, context):
        return getattr(context.active_object, 'pose', None)

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        obj = context.active_object

        if context.mode == 'POSE':
            active_pose_bone = context.active_pose_bone
            bones = context.selected_pose_bones
        else:
            bone = obj.data.bones.active
            active_pose_bone = obj.pose.bones[bone.name]
            bones = [
                b
                for o in context.selected_objects
                for b in getattr(o.pose, 'bones', [])
                if o.data.edit_bones[f'{b.name}'].select
            ]
        objs = {o: i for (i, o) in enumerate(context.selected_objects)}

        showedit = prefs().BLM_ShowPropEdit
        showbone = prefs().BLM_ShowBoneLabels
        showarm = prefs().BLM_ShowArmatureName

        has_ui = False

        def assign_props(op, val, key, bone):
            index = objs[bone.id_data]
            op.data_path = f'selected_objects[{index}].pose.bones["{bone.name}"]'
            op.property = key

            try:
                op.value = str(val)
            except:
                pass

        # Iterate through selected bones add each prop property of each bone to the panel.

        for (index, bone) in enumerate(bones):
            if (bone.keys() or showedit):
                has_ui = True
                if (showarm or showbone):
                    row = layout.row(align=True)
                    row.alignment = 'LEFT'
                    if showarm:
                        # row.label(text=obj.name, icon='ARMATURE_DATA')
                        row.label(text=bones[index].id_data.name, icon='ARMATURE_DATA')
                        if showbone:
                            row.label(icon='RIGHTARROW')
                    if showbone:
                        row.label(icon='BONE_DATA')
                        if showedit:
                            row.emboss = 'PULLDOWN_MENU'
                            row.prop(bone, 'name', text="")
                        else:
                            row.label(text=bone.name)

            # offset for '_RNA_UI'
            i = 1

            if 'constraint_active_index' in bone.keys():
                # offset for '_RNA_UI' + 'constraint_active_index'
                i = 2

            if len(bone.keys()) > i:
                box = layout.box()
            # row = box.row()

            for key in sorted(bone.keys()):
                if key not in ('_RNA_UI', 'constraint_active_index'):
                    # box = layout.box()
                    val = bone.get(key, "value")

                    # enum support WIP (TODO better enum check)
                    enum_type = getattr(bone, key, None)
                    is_rna = False

                    row = box.row()
                    split = row.split(align=True, factor=prefs().BLM_CustomPropSplit)
                    row = split.row(align=True)
                    row.label(text=key, translate=False)

                    row = split.row(align=True)

                    if enum_type is not None:
                        is_rna = True

                    if is_rna:
                        row.prop(bone, key, text="")
                        # row.prop(bone, f'["{key}"]', text="", slider=True)
                    else:
                        row.prop(bone, f'["{key}"]', text="", slider=True)

                    if showedit is True:
                        split = row.split(align=True, factor=0)
                        if not is_rna:
                            row = split.row(align=True)
                            row.context_pointer_set('active_pose_bone', bone)
                            op = row.operator("wm.properties_edit", text="", icon='SETTINGS')
                            assign_props(op, val, key, bone)

                            row = split.row(align=False)
                            row.context_pointer_set('active_pose_bone', bone)
                            op = row.operator("wm.properties_remove", text="", icon='X')
                            assign_props(op, val, key, bone)
                        else:
                            row.label(text="API Defined")

            if showedit:
                row = layout.row(align=True)
                row.context_pointer_set('active_pose_bone', bone)
                add = row.operator("wm.properties_add", text="Add")
                add.data_path = "active_pose_bone"

        if not bones:
            layout.label(text="No bones selected", icon='INFO')
        elif not has_ui:
            layout.label(text="No available bone properties", icon='INFO')
