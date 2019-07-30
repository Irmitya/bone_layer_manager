import bpy

from bpy.props import IntProperty


class BLGROUP_OT_group(bpy.types.Operator):
    # '''Create a Bone Group for the bones in this layer'''
    bl_idname = "bone_layer_man.bonelayergroup"
    bl_label = "Create a Bone Group for the bones in this layer"

    layer_idx: IntProperty(name="Layer Index",
                           description="Index of the layer to assign",
                           default=0, min=0, max=31)

    @classmethod
    def poll(self, context):
        o = context.active_object
        return (o and o.pose is not None)

    def execute(self, context):
        ac_ob = context.active_object
        arm = ac_ob.data
        layer_idx = self.layer_idx
        scene = context.scene
        pose = context.active_object.pose

        # create the empty group
        bpy.ops.pose.group_add()

        name_id_prop = f"layer_name_{layer_idx}"
        try:
            grp_name = ac_ob.data[name_id_prop]
        except KeyError:
            grp_name = f"Layer {layer_idx + 1}"

        groups = pose.bone_groups
        groups[-1].name = grp_name

        import random
        n = random.randrange(1, 15)
        # bone_group color_set is two padded
        Nstr = f"{n :02d}"

        groups[-1].color_set = f'THEME{Nstr}'

        # cycle all bones in the layer
        for bone in pose.bones:
            if bone.bone.layers[layer_idx]:
                # print(bone.name, "is in")
                bone.bone_group = groups[-1]
            # else:
                # print(bone.name, "is not")

        return {'FINISHED'}
