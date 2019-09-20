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
        if getattr(context.active_object, 'pose', None):
            return True
        for ob in context.selected_objects:
            if ob.type == 'ARMATURE':
                return True

    def draw(self, context):
        layout = self.layout


class BLM_PT_customproperties_options(bpy.types.Panel):
    # Creates a Custom Properties Options Subpanel
    bl_idname = "BLM_PT_customproperties_options"
    bl_label = "Display Options"
    bl_parent_id = "BLM_PT_customproperties"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.prop(prefs(), "BLM_ShowPropEdit", text="Edit Mode")
        row.prop(prefs(), "BLM_ShowDeveloperUI", text="Developer Extras ")
        row = layout.row(align=True)
        row.prop(prefs(), "BLM_ShowArmatureName", text="Armature Name")
        row.prop(prefs(), "BLM_ShowBoneLabels", text="Bone Name")


class BLM_PT_customproperties_layout(bpy.types.Panel):
    # Displays a Rig Custom Properties in Subpanel
    bl_category = "Bone Layers"
    bl_label = ""
    bl_idname = "BLM_PT_customproperties_layout"
    bl_parent_id = "BLM_PT_customproperties"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        if context.mode == 'POSE':
            bones = context.selected_pose_bones
        else:
            obs = (
                # List of selected rigs, starting with the active object (if it's a rig)
                *[o for o in {obj} if o and o.type == 'ARMATURE'],
                *[o for o in context.selected_objects
                  if (o != obj and o.type == 'ARMATURE')],
            )
            bones = [
                b
                for o in obs
                for b in getattr(o.pose, 'bones', [])
                if b.bone.select
            ]

        # Store the indexes of selected objects, as a dict()
        objs = {o: i for (i, o) in enumerate(context.selected_objects)}

        showedit = prefs().BLM_ShowPropEdit
        showbone = prefs().BLM_ShowBoneLabels
        showarm = prefs().BLM_ShowArmatureName
        showrna = prefs().BLM_ShowDeveloperUI

        rna_properties = {
            prop.identifier for prop in bpy.types.PoseBone.bl_rna.properties
            if prop.is_runtime
        }

        has_ui = False

        def assign_props(op, val, key, bone):
            if bone.id_data == obj:
                op.data_path = f'active_object.pose.bones["{bone.name}"]'
            else:
                index = objs[bone.id_data]
                op.data_path = f'selected_objects[{index}].pose.bones["{bone.name}"]'
            op.property = key

            try:
                op.value = str(val)
            except:
                pass

        # Iterate through selected bones add each prop property of each bone to the panel.

        for (index, bone) in enumerate(bones):
            items = tuple((
                (k, v) for (k, v) in sorted(bone.items())
                if k != '_RNA_UI' and ((showrna) or (k not in rna_properties))
            ))

            if (items or showedit):
                has_ui = True
                if (showarm or showbone):
                    row = layout.row(align=True)
                    row.alignment = 'LEFT'
                    if showarm:
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

<<<<<<< HEAD
            # offset for '_RNA_UI' and 'constraint_active_index'
            i = 2 if 'constraint_active_index' in bone.keys() else 1

            if len(bone.keys()) > i:
                box = layout.box()
            else:
                has_ui = False

            for key in sorted(bone.keys()):
                if key not in ('_RNA_UI', 'constraint_active_index'):
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

=======
            if items:
                box = layout.box()
            for key, val in items:
                is_rna = key in rna_properties

                to_dict = getattr(val, "to_dict", None)
                to_list = getattr(val, "to_list", None)

                if to_dict:
                    val = to_dict()
                    val_draw = str(val)
                elif to_list:
                    val = to_list()
                    val_draw = str(val)
                else:
                    val_draw = val

                # explicit exception for arrays.
                show_array_ui = to_list and not is_rna and 0 < len(val) <= 4

                row = box.row()
                split = row.split(align=True, factor=prefs().BLM_CustomPropSplit)
                row = split.row(align=True)
                row.label(text=key, translate=False)

                row = split.row(align=True)

                if show_array_ui and isinstance(val[0], (int, float)):
                    row.prop(bone, f'["{key}"]', text="")
                elif to_dict or to_list:
                    row.label(text=val_draw, translate=False)
                else:
>>>>>>> upstream/master
                    if is_rna:
                        row.prop(bone, key, text="")
                    else:
                        row.prop(bone, f'["{key}"]', text="", slider=True)

                if showedit:
                    if is_rna:
                        row.label(text="API Defined")
                    else:
                        split = row.split(align=True, factor=0)

                        row = split.row(align=True)
                        row.context_pointer_set('active_pose_bone', bone)
                        op = row.operator("wm.properties_edit", text="", icon='SETTINGS')
                        assign_props(op, val, key, bone)

                        row = split.row(align=False)
                        row.context_pointer_set('active_pose_bone', bone)
                        op = row.operator("wm.properties_remove", text="", icon='X')
                        assign_props(op, val, key, bone)

            if showedit:
                row = layout.row(align=True)
                row.context_pointer_set('active_pose_bone', bone)
                add = row.operator("wm.properties_add", text="Add")
                add.data_path = "active_pose_bone"

        if not bones:
            layout.label(text="No bones selected", icon='INFO')
        elif not has_ui:
            layout.label(text="No available bone properties", icon='INFO')
