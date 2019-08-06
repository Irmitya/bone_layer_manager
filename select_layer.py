import bpy

from bpy.props import IntProperty
from .blmfuncs import get_bones


class SELECTLAYER_OT_selectlayer(bpy.types.Operator):
    # Select All Bones in given Layer, Shift + Click to add to selection
    bl_idname = "bone_layer_man.selectboneslayer"
    bl_label = ""
    bl_description = "Select all Bones in Layer.\nShift + Click to add to selection"

    layer_idx: IntProperty(name="Layer Index",
                           description="Index of the layer to select",
                           default=0, min=0, max=31)

    @classmethod
    def poll(self, context):
        return getattr(context.active_object, 'type', False) == 'ARMATURE'

    def execute(self, context):
        ob = bpy.context.active_object
        arm = ob.data
        bones = get_bones(arm, context, False)

        layer_idx = self.layer_idx

        # Non additive selection
        if not self.shift:
            if context.mode == 'EDIT_ARMATURE':
                bpy.ops.armature.select_all(action='DESELECT')
            else:
                bpy.ops.pose.select_all(action='DESELECT')

        for bone in bones:
            if bone.layers[layer_idx]:
                bone.select = True
                bone.select_head = True
                bone.select_tail = True

        return {'FINISHED'}

    def invoke(self, context, event):
        self.shift = event.shift

        return self.execute(context)
