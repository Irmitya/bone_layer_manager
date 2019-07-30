import bpy

from bpy.props import BoolProperty
from .blmfuncs import prefs


class BLDEF_OT_deformproptoggle(bpy.types.Operator):
    # '''Toggle All Selected Bones Deform Property'''
    bl_idname = "bone_layer_man.deformtoggle"
    bl_label = "Toggle Deform Property of Selected Bones"

    is_deform: BoolProperty(name="Bone Status", description="Active Bone Deform State")

    @classmethod
    def poll(self, context):
        if context.mode == 'OBJECT':
            return False
        for ob in context.selected_objects:  # Check for armature in all objects (Add support for Weight Painting)
            if ob.type == 'ARMATURE':
                return True
            else:
                continue
            return False
        # return getattr(context.active_object, 'type', False) == 'ARMATURE'

    def execute(self, context):
        ac_ob = context.active_object
        arm = ac_ob.data

        if context.mode == 'POSE' or context.mode == 'PAINT_WEIGHT':
            pbones = context.selected_pose_bones

            if prefs().BLM_UseDeform:
                for pbone in pbones:
                    ebone = pbone.bone
                    if ebone.use_deform is True:
                        ebone.use_deform = False
                prefs().BLM_UseDeform = False

            else:
                for pbone in pbones:
                    ebone = pbone.bone
                    if ebone.use_deform is False:
                        ebone.use_deform = True
                prefs().BLM_UseDeform = True
        else:
            ebones = context.selected_bones

            if prefs().BLM_UseDeform:
                for bone in ebones:
                    if bone.use_deform is True:
                        bone.use_deform = False
                prefs().BLM_UseDeform = False

            else:
                for bone in ebones:
                    if bone.use_deform is False:
                        bone.use_deform = True
                prefs().BLM_UseDeform = True

        return {'FINISHED'}
