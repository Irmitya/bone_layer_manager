import bpy

from bpy.props import BoolProperty, IntProperty, StringProperty
from .blmfuncs import get_bones, ShowMessageBox, check_used_layer


class BLSWAP_OT_swaplayers(bpy.types.Operator):
    '''Swap active (visible) layers'''
    bl_idname = "bone_layer_man.bonelayerswap"
    bl_label = "Hide Select of Selected"

    layer_idx: IntProperty(name="Layer Index",
                           description="Index of the layer to assign",
                           default=0, min=0, max=31)

    layer_name: StringProperty(name="Layer Name",
                               description="Name of the layer",
                               default="")

    rigui_id: IntProperty(name="RigUI Layer",
                          description="Index of the RigUI layer",
                          default=0, min=0, max=31, soft_min=0, soft_max=31)

    lock: BoolProperty(name="Lock Status",
                       description="Wether to lock or not")

    @classmethod
    def poll(self, context):

        if context.mode == 'OBJECT':
            return False
        try:
            return (context.active_object.type == 'ARMATURE')
        except (AttributeError, KeyError, TypeError):
            return False

    def execute(self, context):

        ac_ob = context.active_object
        arm = ac_ob.data
        layer_idx = self.layer_idx
        layer_name = self.layer_name
        scene = context.scene
        pose = context.active_object.pose
        bones = get_bones(arm, context, True)
        lock = self.lock

        first_layer = True
        second_layer = True
        first_layer_idx = 0
        second_layer_idx = 0
        swap_layer_idx = 0

        # count visable layers and check lock status, error if not == 2 or locked
        count = 0
        for i in range(len(ac_ob.data.layers)):
            if arm.layers[i] is True:

                # check if layer is locked
                layer_lock = f"layer_lock_{i}"
                lock = ac_ob.data.get(layer_lock, False)
                count += 1

                if lock is True:
                    ShowMessageBox("Layer locked ", "Bone Layer Manager", 'ERROR')
                    return {'FINISHED'}

        if count != 2:
            ShowMessageBox("Please highlight only 2 layers ", "Bone Layer Manager", 'ERROR')
            return {'FINISHED'}

        # find first empty to use as swap layer or diplay error message
        for i in range(len(ac_ob.data.layers)):
            layer_idx = i

            is_use = check_used_layer(arm, layer_idx, context)

            if is_use == 1:
                if layer_idx == 31:
                    ShowMessageBox("No empty layer available for swap", "Bone Layer Manager", 'ERROR')
                continue

            else:
                arm["BLM_TEMP_LAYER"] = self.layer_name
                arm["BLM_TEMP_LAYER"] = f"Layer {layer_idx + 1}"
                swap_layer_idx = layer_idx
                break

        for i in range(len(ac_ob.data.layers)):

            if arm.layers[i] is True and first_layer is True:
                first_layer_idx = i
                arm["BLM_TEMP_LAYER"] = ac_ob.data.get(f"layer_name_{i}", False)

                if context.mode == 'EDIT_ARMATURE':
                    bpy.ops.armature.select_all(action='DESELECT')
                else:
                    bpy.ops.pose.select_all(action='DESELECT')

                # select all bones in first layer and move to temp layer
                bones = get_bones(arm, context, False)
                for bone in bones:
                    if bone.layers[i]:
                        bone.select = True
                        bone.select_head = True
                        bone.select_tail = True
                        is_layers = [False] * (swap_layer_idx)
                        is_layers.append(True)
                        is_layers.extend(
                            [False] * (len(bone.layers) - swap_layer_idx - 1))
                        bone.layers = is_layers

                first_layer = False

                continue

            if arm.layers[i] is True and first_layer is False and second_layer is True:
                second_layer_idx = i

                # swap names
                arm[f"layer_name_{first_layer_idx}"] = ac_ob.data.get(f"layer_name_{i}", False)

                if context.mode == 'EDIT_ARMATURE':
                    bpy.ops.armature.select_all(action='DESELECT')
                else:
                    bpy.ops.pose.select_all(action='DESELECT')

                # select all bones in second layer and move to first layer
                bones = get_bones(arm, context, False)
                for bone in bones:
                    if bone.layers[second_layer_idx]:
                        bone.select = True
                        bone.select_head = True
                        bone.select_tail = True
                        is_layers = [False] * (first_layer_idx)
                        is_layers.append(True)
                        is_layers.extend([False] * (len(bone.layers) - first_layer_idx - 1))
                        bone.layers = is_layers

                second_layer = False

                continue

            if second_layer is False and first_layer is False:

                # swap names
                arm[f"layer_name_{second_layer_idx}"] = ac_ob.data.get("BLM_TEMP_LAYER", False)

                if context.mode == 'EDIT_ARMATURE':
                    bpy.ops.armature.select_all(action='DESELECT')
                else:
                    bpy.ops.pose.select_all(action='DESELECT')

                # select all bones in temp layer and move to second layer
                bones = get_bones(arm, context, False)
                for bone in bones:
                    if bone.layers[swap_layer_idx]:
                        bone.select = True
                        bone.select_head = True
                        bone.select_tail = True
                        is_layers = [False] * (second_layer_idx)
                        is_layers.append(True)
                        is_layers.extend([False] * (len(bone.layers) - second_layer_idx - 1))
                        bone.layers = is_layers

                first_layer = True
                second_layer = True

                break

        return {'FINISHED'}
