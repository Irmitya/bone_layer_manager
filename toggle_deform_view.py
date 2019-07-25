import bpy

from .blmfuncs import get_bones, prefs


class BLTGGLE_OT_toggledefs(bpy.types.Operator):
    '''Toggle Deform Bones Isolated View (Try Shift Click)'''
    bl_idname = "bone_layer_man.deformerisolate"
    bl_label = "Toggle Deform Bone Only View"

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

    def invoke(self, context, event):
        # ac_ob = context.active_object
        # adding multi object support for this function... fixes an error elsewhere
        arm_list = [o for o in context.selected_objects if (o.type == 'ARMATURE')]
        bones = []

        for arm_ob in arm_list:
            arm = arm_ob.data
            bone_list = get_bones(arm, context, False)
            bones.extend(bone_list)

        if event.shift:
            if prefs().BLM_ToggleView_pose:
                for bone in bones:
                    if bone.use_deform is True:
                        bone.hide = True
                prefs().BLM_ToggleView_pose = False

            else:
                for bone in bones:
                    if bone.use_deform is True:
                        bone.hide = False
                prefs().BLM_ToggleView_pose = True

            return {'FINISHED'}
        else:
            if prefs().BLM_ToggleView_deform:
                for bone in bones:
                    if bone.use_deform is False:
                        bone.hide = True
                prefs().BLM_ToggleView_deform = False

            else:
                for bone in bones:
                    if bone.use_deform is False:
                        bone.hide = False
                prefs().BLM_ToggleView_deform = True

            return {'FINISHED'}
