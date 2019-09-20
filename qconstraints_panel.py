import bpy
import bpy.ops

from bl_ui.properties_constraint import ConstraintButtonsPanel

bpy.types.PoseBone.constraint_active_index = bpy.props.IntProperty()

con_icons = {con.identifier: con.icon for con in bpy.types.Constraint.bl_rna.properties['type'].enum_items}

list_count = 0


class QC_MT_specials(bpy.types.Menu):
    # Constarints specials menu
    bl_label = "Specials"

    def draw(self, context):
        layout = self.layout
        layout.operator("qconstraint.copy", icon='DUPLICATE', text="Copy constraint to selected")
        # TODO
        # layout.operator("qconstraint.copyflipped", icon='DUPLICATE', text="Copy constraint to selected (flipped)")
        layout.separator()
        layout.operator("pose.constraints_copy", icon='DUPLICATE', text="Copy all constraints to selected")
        layout.separator()
        layout.operator("pose.constraints_clear", icon='PANEL_CLOSE', text="Clear all constraints")


class QC_OT_popup(bpy.types.Operator):
    # Ugly Add Constraint Popup (Required for UIList redraw/update)
    bl_idname = "qconstraint.popup"
    bl_label = ""

    def execute(self, context):
        self.report({'INFO'})
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=450)

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        split = row.split(align=True, factor=0.25)
        split.alignment = 'LEFT'

        args = dict(operator='qconstraint.constraint_add', emboss=False)

        # MotionTracking
        col = split.column(align=True)
        col.label(text="Motion Tracking")
        col.operator(**args, text="Camera Solver", icon='CON_CAMERASOLVER').ctype = 'CAMERA_SOLVER'
        col.operator(**args, text="Follow Track", icon='CON_FOLLOWTRACK').ctype = 'FOLLOW_TRACK'
        col.operator(**args, text="Object Solver", icon='CON_OBJECTSOLVER').ctype = 'OBJECT_SOLVER'

        # Transform
        col = split.column(align=True)
        col.label(text="Transform")
        col.operator(**args, text="Copy Location", icon='CON_LOCLIKE').ctype = 'COPY_LOCATION'
        col.operator(**args, text="Copy Rotation", icon='CON_ROTLIKE').ctype = 'COPY_ROTATION'
        col.operator(**args, text="Copy Scale", icon='CON_SIZELIKE').ctype = 'COPY_SCALE'
        col.operator(**args, text="Copy Transforms", icon='CON_TRANSLIKE').ctype = 'COPY_TRANSFORMS'
        col.operator(**args, text="Limit Distance", icon='CON_DISTLIMIT').ctype = 'LIMIT_DISTANCE'
        col.operator(**args, text="Limit Location", icon='CON_LOCLIMIT').ctype = 'LIMIT_LOCATION'
        col.operator(**args, text="Limit Rotation", icon='CON_ROTLIMIT').ctype = 'LIMIT_ROTATION'
        col.operator(**args, text="Limit Scale", icon='CON_SIZELIMIT').ctype = 'LIMIT_SCALE'
        col.operator(**args, text="Maintain Volume", icon='CON_SAMEVOL').ctype = 'MAINTAIN_VOLUME'
        col.operator(**args, text="Transformation", icon='CON_TRANSFORM').ctype = 'TRANSFORM'
        col.operator(**args, text="Transform Cache", icon='CON_TRANSFORM_CACHE').ctype = 'TRANSFORM_CACHE'

        # Tracking
        col = split.column(align=True)
        col.label(text="Tracking")
        col.operator(**args, text="Clamp To", icon='CON_CLAMPTO').ctype = 'CLAMP_TO'
        col.operator(**args, text="Damped Track", icon='CON_TRACKTO').ctype = 'TRACK_TO'
        col.operator(**args, text="Inverse Kinemarics", icon='CON_KINEMATIC').ctype = 'IK'
        col.operator(**args, text="Locked Track", icon='CON_LOCKTRACK').ctype = 'LOCKED_TRACK'
        col.operator(**args, text="Spline IK", icon='CON_SPLINEIK').ctype = 'SPLINE_IK'
        col.operator(**args, text="Stretch To", icon='CON_STRETCHTO').ctype = 'STRETCH_TO'
        col.operator(**args, text="Track To", icon='CON_TRACKTO').ctype = 'TRACK_TO'

        # Relationship
        col = split.column(align=True)
        col.label(text="Relationship")
        col.operator(**args, text="Action", icon='ACTION').ctype = 'ACTION'
        col.operator(**args, text="Armature", icon='CON_ARMATURE').ctype = 'ARMATURE'
        col.operator(**args, text="Child Of", icon='CON_CHILDOF').ctype = 'CHILD_OF'
        col.operator(**args, text="Floor", icon='CON_FLOOR').ctype = 'FLOOR'
        col.operator(**args, text="Follow Path", icon='CON_FOLLOWPATH').ctype = 'FOLLOW_PATH'
        col.operator(**args, text="Pivot", icon='CON_PIVOT').ctype = 'PIVOT'
        col.operator(**args, text="Shrinkwrap", icon='CON_SHRINKWRAP').ctype = 'SHRINKWRAP'


class QC_PT_qcontraints(bpy.types.Panel):
    # Main Quick Constraints Panel
    bl_category = "Bone Layers"
    bl_label = "Quick Constraints"
    bl_idname = "QC_PT_qcontraints"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    @classmethod
    def poll(self, context):
        if getattr(context.active_object, 'pose', None) is not None:
            return context.mode == 'POSE'

    def draw(self, context):
        layout = self.layout


class QC_PT_subqcontraints(bpy.types.Panel):
    # Sub Quick Constraints Panel
    bl_category = "Bone Layers"
    bl_parent_id = "QC_PT_qcontraints"
    bl_label = ""
    bl_idname = "QC_PT_subqcontraints"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(self, context):
        return context.active_pose_bone is not None

    def draw(self, context):
        bone = context.active_pose_bone
        layout = self.layout
        row = layout.row()
        row.template_list("QC_UL_conlist", "", bone, "constraints",
                          bone, "constraint_active_index", rows=4,
                          sort_reverse=False)

        col = row.column(align=True)

        col.operator("bone.constraint_action", icon='ADD', text="").action = 'ADD'
        col.operator("bone.constraint_action", icon='REMOVE', text="").action = 'REMOVE'
        col.separator()
        sub = col.column(align=True)
        sub.menu("QC_MT_specials", icon='DOWNARROW_HLT', text="")
        col.separator()

        if len(bone.constraints) > 1:
            col.operator("bone.constraint_action", icon='TRIA_UP', text="").action = 'UP'
            col.operator("bone.constraint_action", icon='TRIA_DOWN', text="").action = 'DOWN'
            col.separator()


class QC_UL_conlist(bpy.types.UIList):
    # Quick Constraints UIList template
    def draw_item(self, context, layout, data, item, active_data, active_propname, index):

        bone = context.active_pose_bone

        if self.layout_type in {'DEFAULT', 'COMPACT'}:

            self.use_filter_show = False
            global list_count
            list_count += 1
            row = layout.split(factor=0.8)
            row.prop(item, "name", text="", emboss=False, icon=con_icons[item.type])
            row = layout.row(align=True)
            icon = 'HIDE_ON' if item.mute else 'HIDE_OFF'
            row.prop(item, "mute", text="", icon=icon, emboss=False)


class QC_PT_ConSettings(bpy.types.Panel):
    # Contraint Settings Panel
    bl_label = ""
    bl_idname = "DATA_PT_ConSettings"
    bl_context = "constraint"
    bl_category = "Bone Layers"
    bl_parent_id = "QC_PT_qcontraints"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {"HIDE_HEADER"}

    @staticmethod
    def target_template(layout, con, subtargets=True):
        layout.prop(con, "target")  # XXX limiting settings for only 'curves' or some type of object

        if con.target and subtargets:
            if con.target.type == 'ARMATURE':
                layout.prop_search(con, "subtarget", con.target.data, "bones", text="Bone")

                if hasattr(con, "head_tail"):
                    row = layout.row(align=True)
                    row.label(text="Head/Tail:")
                    row.prop(con, "head_tail", text="")
                    # XXX icon, and only when bone has segments?
                    row.prop(con, "use_bbone_shape", text="", icon='IPO_BEZIER')
            elif con.target.type in {'MESH', 'LATTICE'}:
                layout.prop_search(con, "subtarget", con.target, "vertex_groups", text="Vertex Group")

    @staticmethod
    def ik_template(layout, con):
        # only used for iTaSC
        layout.prop(con, "pole_target")

        if con.pole_target and con.pole_target.type == 'ARMATURE':
            layout.prop_search(con, "pole_subtarget", con.pole_target.data, "bones", text="Bone")

        if con.pole_target:
            row = layout.row()
            row.label()
            row.prop(con, "pole_angle")

        split = layout.split(factor=0.33)
        col = split.column()
        col.prop(con, "use_tail")
        col.prop(con, "use_stretch")

        col = split.column()

    @staticmethod
    def Solver_getConstraintClip(context, con):
        if not con.use_active_clip:
            return con.clip
        else:
            return context.scene.active_clip

    @staticmethod
    def space_template(layout, con, target=True, owner=True):
        if target or owner:

            split = layout.split(factor=0.2)

            split.label(text="Space:")
            row = split.row()

            if target:
                row.prop(con, "target_space", text="")

            if target and owner:
                row.label(icon='ARROW_LEFTRIGHT')

            if owner:
                row.prop(con, "owner_space", text="")

    @classmethod
    def poll(self, context):
        if getattr(context.active_object, 'pose', None) is not None:
            return context.active_pose_bone is not None

    def draw(self, context):
        layout = self.layout
        bone = context.active_pose_bone
        idx = getattr(bone, "constraint_active_index", None)

        if len(bone.constraints) > 0:
            const = bone.constraints[idx]
            label = const.name + " :"

            for con in bone.constraints:
                # Not all constraint draw functions are compatible with > getattr(ConstraintButtonsPanel, con.type)(ConstraintButtonsPanel, bone, box, con)
                local_draw = {'OBJECT_SOLVER', 'FOLLOW_PATH', 'FOLLOW_TRACK', 'LIMIT_DISTANCE',
                              'STRETCH_TO', 'ARMATURE', 'CHILD_OF', 'IK'}

                if con.name == const.name:

                    if con.type in local_draw:

                        layout = self.layout.box()
                        row = layout.row()

                        if con.type == 'OBJECT_SOLVER':

                            clip = self.Solver_getConstraintClip(context, con)

                            layout.prop(con, "use_active_clip")

                            if not con.use_active_clip:
                                layout.prop(con, "clip")

                            if clip:
                                layout.prop_search(con, "object", clip.tracking, "objects", icon='OBJECT_DATA')

                            layout.prop(con, "camera")

                            row = layout.row()
                            row.operator("bone.constraint_action", text="Set Inverse").action = 'OB_SET_INVERSE'
                            row.operator("bone.constraint_action", text="Clear Inverse").action = 'OB_CLEAR_INVERSE'

                            layout.operator("clip.constraint_to_fcurve")

                        elif con.type == 'FOLLOW_TRACK':
                            clip = self.Solver_getConstraintClip(context, con)

                            row = layout.row()
                            row.prop(con, "use_active_clip")
                            row.prop(con, "use_3d_position")

                            sub = row.column()
                            sub.active = not con.use_3d_position
                            sub.prop(con, "use_undistorted_position")

                            col = layout.column()

                            if not con.use_active_clip:
                                col.prop(con, "clip")

                            row = col.row()
                            row.prop(con, "frame_method", expand=True)

                            if clip:
                                tracking = clip.tracking

                                col.prop_search(con, "object", tracking, "objects", icon='OBJECT_DATA')

                                tracking_object = tracking.objects.get(con.object, tracking.objects[0])

                                col.prop_search(con, "track", tracking_object, "tracks", icon='ANIM_DATA')

                            col.prop(con, "camera")

                            row = col.row()
                            row.active = not con.use_3d_position
                            row.prop(con, "depth_object")

                            layout.operator("clip.constraint_to_fcurve")

                        elif con.type == 'LIMIT_DISTANCE':
                            self.target_template(layout, con)

                            col = layout.column(align=True)
                            col.prop(con, "distance")
                            # col.operator("constraint.limitdistance_reset")
                            col.operator("bone.constraint_action", text="Reset Distance").action = 'LD_RESET'

                            row = layout.row()
                            row.label(text="Clamp Region:")
                            row.prop(con, "limit_mode", text="")

                            row = layout.row()
                            row.prop(con, "use_transform_limit")
                            row.label()

                            self.space_template(layout, con)

                        elif con.type == 'STRETCH_TO':
                            self.target_template(layout, con)

                            row = layout.row()
                            row.prop(con, "rest_length", text="Rest Length")
                            # row.operator("constraint.stretchto_reset", text="Reset")
                            row.operator("bone.constraint_action", text="Reset").action = 'STRETCH_RESET'

                            layout.prop(con, "bulge", text="Volume Variation")
                            split = layout.split()
                            col = split.column(align=True)
                            col.prop(con, "use_bulge_min", text="Volume Min")
                            sub = col.column()
                            sub.active = con.use_bulge_min
                            sub.prop(con, "bulge_min", text="")
                            col = split.column(align=True)
                            col.prop(con, "use_bulge_max", text="Volume Max")
                            sub = col.column()
                            sub.active = con.use_bulge_max
                            sub.prop(con, "bulge_max", text="")
                            col = layout.column()
                            col.active = con.use_bulge_min or con.use_bulge_max
                            col.prop(con, "bulge_smooth", text="Smooth")

                            row = layout.row()
                            row.label(text="Volume:")
                            row.prop(con, "volume", expand=True)

                            row.label(text="Plane:")
                            row.prop(con, "keep_axis", expand=True)

                        elif con.type == 'IK':
                            # If not standard IK pass iktype to get layout
                            if context.active_object.pose.ik_solver == 'ITASC':
                                layout.prop(con, "ik_type")
                                box = layout.box()
                                iktype = f"IK_{con.ik_type}"
                                getattr(ConstraintButtonsPanel, iktype)(ConstraintButtonsPanel, bone, box, con)

                            else:
                                # Standard IK constraint
                                self.target_template(layout, con)
                                layout.prop(con, "pole_target")

                                if con.pole_target and con.pole_target.type == 'ARMATURE':
                                    layout.prop_search(con, "pole_subtarget", con.pole_target.data, "bones", text="Bone")

                                if con.pole_target:
                                    row = layout.row()
                                    row.prop(con, "pole_angle")
                                    row.label()

                                split = layout.split()
                                col = split.column()
                                col.prop(con, "iterations")
                                col.prop(con, "chain_count")

                                col = split.column()
                                col.prop(con, "use_tail")
                                col.prop(con, "use_stretch")

                                layout.label(text="Weight:")

                                split = layout.split()
                                col = split.column()
                                row = col.row(align=True)
                                row.prop(con, "use_location", text="")
                                sub = row.row(align=True)
                                sub.active = con.use_location
                                sub.prop(con, "weight", text="Position", slider=True)

                                col = split.column()
                                row = col.row(align=True)
                                row.prop(con, "use_rotation", text="")
                                sub = row.row(align=True)
                                sub.active = con.use_rotation
                                sub.prop(con, "orient_weight", text="Rotation", slider=True)

                        elif con.type == 'ARMATURE':
                            topcol = layout.column()
                            topcol.use_property_split = True
                            # topcol.operator("constraint.add_target", text="Add Target Bone")
                            topcol.operator("bone.constraint_action", text="Add Target Bone").action = 'ADD_TARGET'

                            if not con.targets:
                                box = topcol.box()
                                box.label(text="No target bones were added", icon='ERROR')

                            for i, tgt in enumerate(con.targets):
                                box = topcol.box()

                                has_target = tgt.target is not None

                                header = box.row()
                                header.use_property_split = False

                                split = header.split(factor=0.45, align=True)
                                split.prop(tgt, "target", text="")

                                row = split.row(align=True)
                                row.active = has_target
                                if has_target:
                                    row.prop_search(tgt, "subtarget", tgt.target.data, "bones", text="")
                                else:
                                    row.prop(tgt, "subtarget", text="", icon='BONE_DATA')

                                header.operator("qconstraint.remove_target", text="", icon='REMOVE').index = i

                                col = box.column()
                                col.active = has_target and tgt.subtarget != ""
                                col.prop(tgt, "weight", slider=True)

                            # topcol.operator("constraint.normalize_target_weights")
                            topcol.operator("bone.constraint_action", text="Normalize Weights").action = 'NORMALIZE_TARGET'
                            topcol.prop(con, "use_deform_preserve_volume")
                            topcol.prop(con, "use_bone_envelopes")

                            # if context.pose_bone:
                            topcol.prop(con, "use_current_location")

                        elif con.type == 'CHILD_OF':
                            self.target_template(layout, con)

                            split = layout.split()

                            col = split.column()
                            col.label(text="Location:")
                            col.prop(con, "use_location_x", text="X")
                            col.prop(con, "use_location_y", text="Y")
                            col.prop(con, "use_location_z", text="Z")

                            col = split.column()
                            col.label(text="Rotation:")
                            col.prop(con, "use_rotation_x", text="X")
                            col.prop(con, "use_rotation_y", text="Y")
                            col.prop(con, "use_rotation_z", text="Z")

                            col = split.column()
                            col.label(text="Scale:")
                            col.prop(con, "use_scale_x", text="X")
                            col.prop(con, "use_scale_y", text="Y")
                            col.prop(con, "use_scale_z", text="Z")

                            row = layout.row()
                            # row.operator("constraint.childof_set_inverse")
                            row.operator("bone.constraint_action", text="Set Inverse").action = 'CO_SET_INVERSE'
                            # row.operator("constraint.childof_clear_inverse")
                            row.operator("bone.constraint_action", text="Clear Inverse").action = 'CO_CLEAR_INVERSE'

                        elif con.type == 'FOLLOW_PATH':
                            self.target_template(layout, con)
                            # layout.operator("constraint.followpath_path_animate", text="Animate Path", icon='ANIM_DATA')
                            layout.operator("bone.constraint_action", text="Animate Path", icon='ANIM_DATA').action = 'FOLLOW_PATH'

                            split = layout.split()

                            col = split.column()
                            col.prop(con, "use_curve_follow")
                            col.prop(con, "use_curve_radius")

                            col = split.column()
                            col.prop(con, "use_fixed_location")
                            if con.use_fixed_location:
                                col.prop(con, "offset_factor", text="Offset")
                            else:
                                col.prop(con, "offset")

                            row = layout.row()
                            row.label(text="Forward:")
                            row.prop(con, "forward_axis", expand=True)

                            row = layout.row()
                            row.prop(con, "up_axis", text="Up")
                            row.label()
                    else:
                        layout = self.layout
                        box = layout.box()
                        row = layout.row()
                        getattr(ConstraintButtonsPanel, con.type)(ConstraintButtonsPanel, bone, box, con)

                    if con.type in {'RIGID_BODY_JOINT', 'NULL'}:
                        return

                    if con.type in {'IK', 'SPLINE_IK'}:
                        # constraint.disable_keep_transform doesn't work well
                        # for these constraints.
                        if con.type in local_draw:
                            row = layout.row()
                            row.prop(con, "influence")
                        else:
                            box.prop(con, "influence")

                    else:
                        if con.type in local_draw:
                            row = layout.row(align=True)
                        else:
                            row = box.row(align=True)

                        row.prop(con, "influence")
                        row.operator("qconstraint.disable_keep_transform", text="", icon='CANCEL')
