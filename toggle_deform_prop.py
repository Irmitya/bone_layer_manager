import bpy

from bpy.props import BoolProperty

class BLDEF_OT_deformproptoggle(bpy.types.Operator):
    '''Toggle All Selected Bones Deform Property'''
    bl_idname = "bone_layer_man.deformtoggle"
    bl_label = "Toggle Deform Property of Bones"

    is_deform : BoolProperty(name="Bone Status", description="Active Bone Deform State")



    @classmethod
    def poll(self, context):

        if context.mode == 'OBJECT':
            return False
        try:
            return (context.active_object.type == 'ARMATURE')
        except (AttributeError, KeyError, TypeError):
            return False



    def execute(self, context):
        scn = context.scene
        ac_ob = context.active_object
        arm = ac_ob.data

        if context.mode == 'POSE':
            pbones = context.selected_pose_bones

            if scn.BLM_UseDeform :
                for pbone in pbones:
                    ebone = pbone.bone
                    if ebone.use_deform == True:
                        ebone.use_deform = False
                scn.BLM_UseDeform = False

            else:
                for pbone in pbones:
                    ebone = pbone.bone
                    if ebone.use_deform == False:
                        ebone.use_deform = True
                scn.BLM_UseDeform = True
        else:
            ebones = context.selected_bones

            if scn.BLM_UseDeform :
                for bone in ebones:
                    if bone.use_deform == True:
                        bone.use_deform = False
                scn.BLM_UseDeform = False

            else:
                for bone in ebones:
                    if bone.use_deform == False:
                        bone.use_deform = True
                scn.BLM_UseDeform = True


        return {'FINISHED'}
