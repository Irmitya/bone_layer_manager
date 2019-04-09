import bpy

from bpy.props import IntProperty, BoolProperty
from .blmfuncs import get_bones


class LOCKLAYER_OT_lock(bpy.types.Operator):
    """Lock All bones on this Layer"""
    bl_idname = "bone_layer_man.bonelockselected"
    bl_label = "Restrict Selection of bones in a layer"

    layer_idx: IntProperty(name="Layer Index",
                           description="Index of the layer to lock",
                           default=0, min=0, max=31)

    lock: BoolProperty(name="Lock Status",
                       description="Wether to lock or not")

    def execute(self, context):
        ob = bpy.context.active_object
        arm = ob.data

        bones = get_bones(arm, context, False)

        for bone in bones:
            if bone.layers[self.layer_idx]:
                bone.select = False
                bone.select_head = False
                bone.select_tail = False
                bone.hide_select = self.lock

                # set lock ID property
                arm[f"layer_lock_{self.layer_idx}"] = self.lock

        return {'FINISHED'}
