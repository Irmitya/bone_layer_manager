import bpy

from bpy.props import IntProperty
from .blmfuncs import get_bones


class BLMERGE_OT_merge(bpy.types.Operator):
    # Move Selected Bones to this Layer, Shift + Click to assign to multiple layers
    bl_idname = "bone_layer_man.blmergeselected"
    bl_label = ""
    bl_description = "Move selected Bones to this Layer.\nShift + Click to assign to multiple layers"

    layer_idx: IntProperty(name="Layer Index",
                           description="Index of the layer to assign",
                           default=0, min=0, max=31)

    @classmethod
    def poll(self, context):
        arm = getattr(context.active_object, 'data', None)
        not_link = (getattr(arm, 'library', None) is None)
        return not_link

    def __init__(self):
        self.shift = False

    def execute(self, context):
        arm = context.active_object.data

        bones = get_bones(arm, context, True)

        for bone in bones:
            if not self.shift:
                is_layers = [False] * (self.layer_idx)
                is_layers.append(True)
                is_layers.extend([False] * (len(bone.layers) - self.layer_idx - 1))

                bone.layers = is_layers
            else:
                bone.layers[self.layer_idx] ^= True

        return {'FINISHED'}

    def invoke(self, context, event):
        self.shift = event.shift

        return self.execute(context)
