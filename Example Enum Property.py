import bpy


def update_enum(self, context):
    print(self, self.name, context)

bpy.types.PoseBone.propnam = bpy.props.EnumProperty(
    items=(
          ('state_1', 'Name 1', 'Tooltip_1'),
          ('state_2', 'Name 2', 'Tooltip_2'),
          ('state_3', 'Name 3', 'Tooltip_3'),
        ),
    name="Set Property",
    default="state_1",
    update=update_enum
    )

bpy.data.objects["Armature"].pose.bones["Bone"].propname = "state_1"
