# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from . customprop_panel import BLM_PT_customproperties
from . rigui_panel import BLM_PT_rigui
from . bone_layers_panel import BLM_PT_panel
from . bone_layers_panel import BLM_PT_panel_options
from . bone_layers_panel import BLM_PT_panel_layers
from . write_ui_script import WRITEUI_OT_writeui
from . swap_layers import BLSWAP_OT_swaplayers
from . toggle_deform_prop import BLDEF_OT_deformproptoggle
from . toggle_deform_view import BLTGGLE_OT_toggledefs
from . make_group import BLGROUP_OT_group
from . merge_layers import BLMERGE_OT_merge
from . select_layer import SELECTLAYER_OT_selectlayer
from . lock_layer import LOCKLAYER_OT_lock
from . create_rigui_id import SETUIID_OT_riguiid
from . create_layer_id import CREATEID_OT_name
import bpy

bl_info = {
    'name': 'Bone Layer Manager',
    'description': 'Add Bone Layer Name functionality and Rig UI Creation Tools',
    'author': 'Alfonso Annarumma, Paolo Acampora, Fin, COnLOAR',
    'version': (0, 7, 3),
    'blender': (2, 80, 0),
    'location': 'View3D > Properties  > Bone Layers',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': '3D View'
}


classes = (
    CREATEID_OT_name,
    SETUIID_OT_riguiid,
    LOCKLAYER_OT_lock,
    SELECTLAYER_OT_selectlayer,
    BLMERGE_OT_merge,
    BLGROUP_OT_group,
    BLTGGLE_OT_toggledefs,
    BLDEF_OT_deformproptoggle,
    BLSWAP_OT_swaplayers,
    WRITEUI_OT_writeui,
    BLM_PT_panel,
    BLM_PT_panel_options,
    BLM_PT_panel_layers,
    BLM_PT_rigui,
    BLM_PT_customproperties,
    
)

register, unregister = bpy.utils.register_classes_factory(classes)
