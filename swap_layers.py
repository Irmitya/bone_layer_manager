import bpy

from bpy.props import BoolProperty, IntProperty, StringProperty
from .blmfuncs import get_bones, ShowMessageBox, check_used_layer


class BLSWAP_OT_swaplayers(bpy.types.Operator):
    '''Swap selected layers  (bones + layer names + UI Layer)'''
    bl_idname = "bone_layer_man.bonelayerswap"
    bl_label = "Hide Select of Selected"

    layer_idx: IntProperty(name="Layer Index",
                           description="Index of the layer to assign",
                           default=0, min=0, max=31)
    target_idx: IntProperty(name="Target Index",
                           description="Target index to assign for layer",
                           options={'SKIP_SAVE'},
                           default=-1, min=-1, max=32)

    # layer_name: StringProperty(name="Layer Name",
                            #    description="Name of the layer",
                            #    default="")

    # rigui_id: IntProperty(name="RigUI Layer",
                        #   description="Index of the RigUI layer",
                        #   default=0, min=0, max=31, soft_min=0, soft_max=31)

    # lock: BoolProperty(name="Lock Status",
                    #    description="Wether to lock or not")

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
        target_idx = self.target_idx
        # layer_name = self.layer_name
        bones = get_bones(arm, context, False)
        # lock = self.lock

        def is_lock(idx):
            # check if layer is locked (or hidden)
            layer_lock = f"layer_lock_{idx}"
            lock = arm.get(layer_lock, False)

            if idx not in range(32):
                return True
            at_end = idx in [0, 31]

            scn = context.scene
            if not lock and not at_end:
                is_use = check_used_layer(arm, idx, context)
                layer_name = arm.get(f"layer_name_{idx}")

                if not ((is_use or not scn.BLM_LayerVisibility) and
                    (layer_name or not scn.BLM_ShowNamed)):
                    lock = True  # skip hidden layers
            return lock

        if target_idx in range(32):
            # Arrow mode
            first_layer_idx = layer_idx
            second_layer_idx = target_idx

            get_lock = 'is_lock(second_layer_idx) and second_layer_idx in range(32)'
            if second_layer_idx < first_layer_idx:
                # Up
                while eval(get_lock):
                    second_layer_idx -= 1
            elif second_layer_idx > first_layer_idx:
                # Down
                while eval(get_lock):
                    second_layer_idx += 1
        else:
            # Double click mode
            first_layer_idx = arm.get('BLM_TEMP_FIRST_LAYER')
            second_layer_idx = layer_idx

            if first_layer_idx is None:
                # First run
                arm["BLM_TEMP_FIRST_LAYER"] = layer_idx
                return {'PASS_THROUGH'}

        if 'BLM_TEMP_FIRST_LAYER' in arm:
            del(arm["BLM_TEMP_FIRST_LAYER"])

        if first_layer_idx is second_layer_idx:
            return {'CANCELLED'}

        if is_lock(first_layer_idx):
            # Clicked first layer, locked it, then clicked a second layer
            ShowMessageBox("First layer locked!", "Bone Layer Manager", 'ERROR')
            return {'CANCELLED'}
        if second_layer_idx not in range(32):
            # TODO: instead of error cancel, try to loop around
            if second_layer_idx < first_layer_idx:
                txt = "Previous"
            else:
                txt = "Next"
            ShowMessageBox(f"{txt} layer locked!", "Bone Layer Manager", 'ERROR')
            return {'CANCELLED'}

        def swap_layer_vis():
            # Swap layer visibility
            first_layer_vis = arm.layers[first_layer_idx]
            second_layer_vis = arm.layers[second_layer_idx]
            arm.layers[first_layer_idx] = second_layer_vis
            arm.layers[second_layer_idx] = first_layer_vis

        def swap_layer_prop(prop):
            # Swap Layer Props
            first_layer_prop = arm.get(f"{prop}_{first_layer_idx}")
            second_layer_prop = arm.get(f"{prop}_{second_layer_idx}")
            arm[f"{prop}_{first_layer_idx}"] = second_layer_prop
            arm[f"{prop}_{second_layer_idx}"] = first_layer_prop

            # Delete previous prop if it was unassigned
            first_layer_prop_update = arm.get(f"{prop}_{first_layer_idx}")
            second_layer_prop_update = arm.get(f"{prop}_{second_layer_idx}")
            if first_layer_prop_update is None:
                del(arm[f"{prop}_{first_layer_idx}"])
            if second_layer_prop_update is None:
                del(arm[f"{prop}_{second_layer_idx}"])

        def swap_bones():
            # Remember bone layers
            first_layer_cache = []
            second_layer_cache = []
            for bone in bones:
                in_first = bone.layers[first_layer_idx]
                in_second = bone.layers[second_layer_idx]
                if in_first:
                    first_layer_cache.append(bone)
                if in_second:
                    second_layer_cache.append(bone)

            # Optionally deselect all bones not in a layer
                # select = in_first
                # select = in_second
                # select = (in_first or in_second)

                # bone.select = select
                # bone.select_head = select
                # bone.select_tail = select

            def swap_bone_layers(bones, layer1, layer2):
                # select all bones in first layer and move to temp layer
                for bone in bones:
                    in_both = bone.layers[layer2]
                    bone.layers[layer2] = True
                    bone.layers[layer1] = in_both

            swap_bone_layers(first_layer_cache, first_layer_idx, second_layer_idx)
            swap_bone_layers(second_layer_cache, second_layer_idx, first_layer_idx)

        swap_layer_vis()
        swap_layer_prop('layer_name')
        swap_layer_prop('rigui_id')
        swap_bones()

        return {'FINISHED'}
