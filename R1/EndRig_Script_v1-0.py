bl_info = {
    "name": "Endertainer Rig Add-On",
    "author": "Endertainer007 & BlueEvil",
    "version": (1, 0, 0),
    "blender": (3, 1, 2),
    "location": "View3d > Tool",
    "description": "Adds a Rig UI panel for the Endertainer Rig",
    "warning": "",
    "tracker_url": "",
    "category": "EndRig",
}

import bpy
from bpy.props import (StringProperty,
                        BoolProperty,
                        IntProperty,
                        FloatProperty,
                        FloatVectorProperty,
                        EnumProperty,
                        PointerProperty,
                        )

#━━━━━━━━━━━━━━━━━━━
#     Operators     
#━━━━━━━━━━━━━━━━━━━

def toggleButton(obj, pos, propName, text):
    
    context = "Show"
    if(getattr(obj, propName, True)):
        context = "Hide"
        
    text = text.replace("s/h", context)
    
    context = "SHOW"
    if(getattr(obj, propName, True)):
        context = "HIDE"
        
    text = text.replace("S/H", context)
    
    if(getattr(obj, propName, True)):
        pos.prop(obj, propName, toggle=True, text="", icon="CHECKBOX_HLT")
    else:
        pos.prop(obj, propName, toggle=True, text="", icon="CHECKBOX_DEHLT")
    return getattr(obj, propName, True)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     Custom Properties     
#━━━━━━━━━━━━━━━━━━━━━━━━━━━

bpy.types.Object.SettingsTab1= EnumProperty(
    items = [('Default', 'Default', 'EndRig Default properties'), 
            ('Custom', 'Custom ', 'EndRig Custom properties')  ],
    override = {"LIBRARY_OVERRIDABLE"},
    name = "SettingsTab1")

bpy.types.Object.SettingsTab2= EnumProperty(
    items = [('Control', 'Control', 'A collection of System & Kinematic settings'), 
            ('Design', 'Design ', 'A collection of Customization settings'), 
            ('Render', 'Render ', 'A collection of Render & Visibility settings')  ],
    override = {"LIBRARY_OVERRIDABLE"},
    name = "SettingsTab2")
    
bpy.types.Object.HeadSettings = bpy.props.BoolProperty(
    name = "Togle Visibility",
    override = {"LIBRARY_OVERRIDABLE"},
    default = False)
    
bpy.types.Object.ArmLegSettings = bpy.props.BoolProperty(
    name = "Togle Visibility",
    override = {"LIBRARY_OVERRIDABLE"},
    default = False)
    
bpy.types.Object.IKParentSettings = bpy.props.BoolProperty(
    name = "Togle Visibility",
    override = {"LIBRARY_OVERRIDABLE"},
    default = False)
    
bpy.types.Object.BodyCustom = bpy.props.BoolProperty(
    name = "Togle Visibility",
    override = {"LIBRARY_OVERRIDABLE"},
    default = False)
    
bpy.types.Object.DeformSettings = bpy.props.BoolProperty(
    name = "Togle Visibility",
    override = {"LIBRARY_OVERRIDABLE"},
    default = False)
    
bpy.types.Object.ViewportRender = bpy.props.BoolProperty(
    name = "Togle Visibility",
    override = {"LIBRARY_OVERRIDABLE"},
    default = False)
    
bpy.types.Object.SubsurfSettings = bpy.props.BoolProperty(
    name = "Togle Visibility",
    override = {"LIBRARY_OVERRIDABLE"},
    default = False)
    
bpy.types.Object.AntilagSettings = bpy.props.BoolProperty(
    name = "Togle Visibility",
    override = {"LIBRARY_OVERRIDABLE"},
    default = False)

#━━━━━━━━━━━━━━━━━━━━
#     Info Panel     
#━━━━━━━━━━━━━━━━━━━━

class InfoPanel(bpy.types.Panel):
    bl_label = "Rig Info"
    bl_idname = "EndRig_InfoPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EndRig'
    
    @classmethod
    def poll(self, context):
        try:
            return (bpy.context.active_object.get("rig_id") == "EndRig")
        except (AttributeError, KeyError, TypeError):
            return False
    
    def draw(self, context):
        layout = self.layout
        obj = context.object
        b = layout.box()
        r = b.row(align=True)
        r.label(text= "Rig UI v1.0", icon= 'TEXT')
        r = b.row(align=True)
        
        # Rig Version Identifier
        
        if obj.get("rig_version") == "R1_v1-0":
            r.label(text= "Endertainer Rig R1 v1.0", icon= 'OUTLINER_OB_ARMATURE')
        
        # Experimental Tag
        
        #bb = b.box()
        #b1 = bb.row(align=True)
        #b1.label(text= "Experimental Version", icon= 'ERROR')

#━━━━━━━━━━━━━━━━━━━━
#     Main Panel     
#━━━━━━━━━━━━━━━━━━━━

class MainPanel(bpy.types.Panel):
    bl_label = "Rig Settings"
    bl_idname = "EndRig_MainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EndRig'
    bl_parent_id = "EndRig_InfoPanel"
    
    propBone = "PROP_Custom_Settings"
    
    @classmethod
    def poll(self, context):
        try:
            return (bpy.context.active_object.get("rig_id") == "EndRig")
        except (AttributeError, KeyError, TypeError):
            return False
    
    def getProperties(self, rig) -> list:
        props = []
        for k in rig.pose.bones[self.propBone].keys():
            props.append(k)
        return props
    
    def draw(self, context):
        layout = self.layout
        obj = context.object
        pose_bones = context.active_object.pose.bones
        rig = bpy.context.active_object
        
#======================
#     Settings Tab     
#======================

        b = layout.box()
        r = b.row(align=True)
        r.label(text= "PROP Dashboard", icon= 'MENU_PANEL')
        r = b.row(align=True)
        r.prop(obj, "SettingsTab1", text = "SettingsTab1", expand=True)

#----------------------------
#     Default Settings     
#----------------------------

        if obj.get('SettingsTab1') == 0:
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~
#     Control Settings     
#~~~~~~~~~~~~~~~~~~~~~~~~~~

            if obj.get('SettingsTab2') == 0:
                b = layout.box()
                r = b.row(align=True)
                r.label(text= "Default Settings", icon= 'PROPERTIES')
                r = b.row(align=True)
                r.prop(obj, "SettingsTab2", text = "SettingsTab2", expand=True)
                
                # Head Settings
                
                b1 = b.box()
                r1 = b1.row(align=True)
                r1.label(text= "Head Settings", icon= 'MATSHADERBALL')
                if(toggleButton(obj, r1, "HeadSettings", "")):
                    r1 = b1.row(align=True)
                    c1 = r1.column(align = True)
                    c1.prop(pose_bones['PROP_Main_Settings'], '["Face_Editor_Extras"]', text='Face Editor Extras')
                    c1.prop(pose_bones['PROP_Main_Settings'], '["Dynamic_Face"]', text='Dynamic Face')
                    c1.prop(pose_bones['PROP_Main_Settings'], '["Dynamic_Head"]', text='Dynamic Head')
                    c1.prop(pose_bones['PROP_Main_Settings'], '["Eye_Tracker"]', text='Eye Tracker')
                
                # Arm Settings
                
                b2 = b.box()
                r2 = b2.row(align=True)
                r2.label(text= "Arm & Leg Settings", icon= 'CON_KINEMATIC')
                if(toggleButton(obj, r2, "ArmLegSettings", "")):
                    r2 = b2.row(align=True)
                    r2.label(text= "      Right Arm")
                    r2.label(text= "      Left Arm")
                    c2 = b2.column(align=True)
                    g2 = c2.grid_flow(columns=2, align=True)
                    g2.prop(pose_bones['PROP_Main_Settings'], '["RArm_IKFK_Switch"]', text='IK/FK')
                    g2.prop(pose_bones['PROP_Main_Settings'], '["RArm_IK_Pole"]', text='IK Pole')
                    g2.prop(pose_bones['PROP_Main_Settings'], '["LArm_IKFK_Switch"]', text='IK/FK')
                    g2.prop(pose_bones['PROP_Main_Settings'], '["LArm_IK_Pole"]', text='IK Pole')
                    g2 = c2.grid_flow(columns=1, align=True)
                    g2.prop(pose_bones['PROP_Main_Settings'], '["Arm_IKFK_Switch_Mode"]', text='IK-FK Switch Mode')
                    g2.prop(pose_bones['PROP_Main_Settings'], '["Finger_Rig"]', text='Finger Rig')
                    r2 = b2.row(align=True)
                    r2.label(text= "      Right Leg")
                    r2.label(text= "      Left Leg")
                    c2 = b2.column(align=True)
                    g2 = c2.grid_flow(columns=2, align=True)
                    g2.prop(pose_bones['PROP_Main_Settings'], '["RLeg_IKFK_Switch"]', text='IK/FK')
                    g2.prop(pose_bones['PROP_Main_Settings'], '["RLeg_IK_Pole"]', text='IK Pole')
                    g2.prop(pose_bones['PROP_Main_Settings'], '["LLeg_IKFK_Switch"]', text='IK/FK')
                    g2.prop(pose_bones['PROP_Main_Settings'], '["LLeg_IK_Pole"]', text='IK Pole')
                    g2 = c2.grid_flow(columns=1, align=True)
                    g2.prop(pose_bones['PROP_Main_Settings'], '["Leg_IKFK_Switch_Mode"]', text='IK-FK Switch Mode')
                    g2.prop(pose_bones['PROP_Main_Settings'], '["Ankle_Swap"]', text='Ankle Swap')
                
                # IK Parent Tree
                
                b3 = b.box()
                r3 = b3.row(align=True)
                r3.label(text= "IK Parent Tree", icon= 'CON_CHILDOF')
                if(toggleButton(obj, r3, "IKParentSettings", "")):
                    r3 = b3.row(align=True)
                    r3.label(text= "      Right Arm")
                    r3.label(text= "      Left Arm")
                    c3 = b3.column(align=True)
                    g3 = c3.grid_flow(columns=2, align=True)
                    g3.prop(pose_bones['PROP_Main_Settings'], '["RArm_IK_Hybrid"]', text='IK Hybrid')
                    g3.prop(pose_bones['PROP_Main_Settings'], '["LArm_IK_Hybrid"]', text='IK Hybrid')
                    g3 = c3.grid_flow(columns=2, align=True)
                    if pose_bones['PROP_Main_Settings'].get('RArm_IK_Hybrid') == 0:
                        # RArm IK Parent Tree List
                        if pose_bones['PROP_Main_Settings'].get('RArm_IK_Parent_Tree') == 0:
                            g3.prop(pose_bones['PROP_Main_Settings'], '["RArm_IK_Parent_Tree"]', text='Parent: Flip Bone')
                        if pose_bones['PROP_Main_Settings'].get('RArm_IK_Parent_Tree') == 1:
                            g3.prop(pose_bones['PROP_Main_Settings'], '["RArm_IK_Parent_Tree"]', text='Parent: Torso')
                        if pose_bones['PROP_Main_Settings'].get('RArm_IK_Parent_Tree') == 2:
                            g3.prop(pose_bones['PROP_Main_Settings'], '["RArm_IK_Parent_Tree"]', text='Parent: Chest')
                        if pose_bones['PROP_Main_Settings'].get('RArm_IK_Parent_Tree') == 3:
                            g3.prop(pose_bones['PROP_Main_Settings'], '["RArm_IK_Parent_Tree"]', text='Parent: Arm Offset')
                        if pose_bones['PROP_Main_Settings'].get('RArm_IK_Parent_Tree') == 4:
                            g3.prop(pose_bones['PROP_Main_Settings'], '["RArm_IK_Parent_Tree"]', text='Parent: Root')
                        #---
                    if pose_bones['PROP_Main_Settings'].get('RArm_IK_Hybrid') == 1:
                        g3.label(text= "Hybrid", icon= 'CON_CHILDOF')
                    if pose_bones['PROP_Main_Settings'].get('LArm_IK_Hybrid') == 0:
                        # LArm IK Parent Tree List
                        if pose_bones['PROP_Main_Settings'].get('LArm_IK_Parent_Tree') == 0:
                            g3.prop(pose_bones['PROP_Main_Settings'], '["LArm_IK_Parent_Tree"]', text='Parent: Flip Bone')
                        if pose_bones['PROP_Main_Settings'].get('LArm_IK_Parent_Tree') == 1:
                            g3.prop(pose_bones['PROP_Main_Settings'], '["LArm_IK_Parent_Tree"]', text='Parent: Torso')
                        if pose_bones['PROP_Main_Settings'].get('LArm_IK_Parent_Tree') == 2:
                            g3.prop(pose_bones['PROP_Main_Settings'], '["LArm_IK_Parent_Tree"]', text='Parent: Chest')
                        if pose_bones['PROP_Main_Settings'].get('LArm_IK_Parent_Tree') == 3:
                            g3.prop(pose_bones['PROP_Main_Settings'], '["LArm_IK_Parent_Tree"]', text='Parent: Arm Offset')
                        if pose_bones['PROP_Main_Settings'].get('LArm_IK_Parent_Tree') == 4:
                            g3.prop(pose_bones['PROP_Main_Settings'], '["LArm_IK_Parent_Tree"]', text='Parent: Root')
                        #---
                    if pose_bones['PROP_Main_Settings'].get('LArm_IK_Hybrid') == 1:
                        g3.label(text= "Hybrid", icon= 'CON_CHILDOF')
                    r3 = b3.row(align=True)
                    r3.label(text= "      Right Leg")
                    r3.label(text= "      Left Leg")
                    c3 = b3.column(align=True)
                    g3 = c3.grid_flow(columns=2, align=True)
                    g3.prop(pose_bones['PROP_Main_Settings'], '["RLeg_IK_Hybrid"]', text='IK Hybrid')
                    g3.prop(pose_bones['PROP_Main_Settings'], '["LLeg_IK_Hybrid"]', text='IK Hybrid')
                    g3 = c3.grid_flow(columns=2, align=True)
                    if pose_bones['PROP_Main_Settings'].get('RLeg_IK_Hybrid') == 0:
                        # RLeg IK Parent Tree List
                        if pose_bones['PROP_Main_Settings'].get('RLeg_IK_Parent_Tree') == 0:
                            g3.prop(pose_bones['PROP_Main_Settings'], '["RLeg_IK_Parent_Tree"]', text='Parent: Flip Bone')
                        if pose_bones['PROP_Main_Settings'].get('RLeg_IK_Parent_Tree') == 1:
                            g3.prop(pose_bones['PROP_Main_Settings'], '["RLeg_IK_Parent_Tree"]', text='Parent: Torso')
                        if pose_bones['PROP_Main_Settings'].get('RLeg_IK_Parent_Tree') == 2:
                            g3.prop(pose_bones['PROP_Main_Settings'], '["RLeg_IK_Parent_Tree"]', text='Parent: Root')
                        #---
                    if pose_bones['PROP_Main_Settings'].get('RLeg_IK_Hybrid') == 1:
                        g3.label(text= "Hybrid", icon= 'CON_CHILDOF')
                    if pose_bones['PROP_Main_Settings'].get('LLeg_IK_Hybrid') == 0:
                        # LLeg IK Parent Tree List
                        if pose_bones['PROP_Main_Settings'].get('LLeg_IK_Parent_Tree') == 0:
                            g3.prop(pose_bones['PROP_Main_Settings'], '["LLeg_IK_Parent_Tree"]', text='Parent: Flip Bone')
                        if pose_bones['PROP_Main_Settings'].get('LLeg_IK_Parent_Tree') == 1:
                            g3.prop(pose_bones['PROP_Main_Settings'], '["LLeg_IK_Parent_Tree"]', text='Parent: Torso')
                        if pose_bones['PROP_Main_Settings'].get('LLeg_IK_Parent_Tree') == 2:
                            g3.prop(pose_bones['PROP_Main_Settings'], '["LLeg_IK_Parent_Tree"]', text='Parent: Root')
                        #---
                    if pose_bones['PROP_Main_Settings'].get('LLeg_IK_Hybrid') == 1:
                        g3.label(text= "Hybrid", icon= 'CON_CHILDOF')
                
#~~~~~~~~~~~~~~~~~~~~~~~~~
#     Design Settings     
#~~~~~~~~~~~~~~~~~~~~~~~~~

            if obj.get('SettingsTab2') == 1:
                b = layout.box()
                r = b.row(align=True)
                r.label(text= "Default Settings", icon= 'PROPERTIES')
                r = b.row(align=True)
                r.prop(obj, "SettingsTab2", text = "SettingsTab2", expand=True)
                
                # Body Customization
                
                b1 = b.box()
                r1 = b1.row(align=True)
                r1.label(text= "Rig Customization", icon= 'ARMATURE_DATA')
                if(toggleButton(obj, r1, "BodyCustom", "")):
                    c1 = b1.column(align=True)
                    # Arm Type List
                    if pose_bones['PROP_Customization_Settings'].get('Arm_Type') == 0:
                        c1.prop(pose_bones['PROP_Customization_Settings'], '["Arm_Type"]', text='Arm Type: Steve')
                    if pose_bones['PROP_Customization_Settings'].get('Arm_Type') == 1:
                        c1.prop(pose_bones['PROP_Customization_Settings'], '["Arm_Type"]', text='Arm Type: Alex')
                    if pose_bones['PROP_Customization_Settings'].get('Arm_Type') == 2:
                        c1.prop(pose_bones['PROP_Customization_Settings'], '["Arm_Type"]', text='Arm Type: Slim')
                    #---
                    c1.prop(pose_bones['PROP_Customization_Settings'], '["Texture_Deform"]', text='Texture Deform')
                    g1 = c1.grid_flow(columns=2, align=True)
                    g1.prop(pose_bones['PROP_Customization_Settings'], '["Tongue"]', text='Tongue')
                    g1.prop(pose_bones['PROP_Customization_Settings'], '["Eyelash"]', text='Eyelash')
                    g1.prop(pose_bones['PROP_Customization_Settings'], '["Lips"]', text='Lips')
                    g1.prop(pose_bones['PROP_Customization_Settings'], '["Jaw"]', text='Jaw')
                    g1 = c1.grid_flow(columns=1, align=True)
                    if pose_bones['PROP_Customization_Settings'].get('Jaw') == 1:
                        g1.prop(pose_bones['PROP_Customization_Settings'], '["Jaw_Size"]', text='Jaw Size')
                    
                # Deformation Settings
                
                b2 = b.box()
                r2 = b2.row(align=True)
                r2.label(text= "Deform Settings", icon= 'OUTLINER_OB_LATTICE')
                if(toggleButton(obj, r2, "DeformSettings", "")):
                    c2 = b2.column(align=True)
                    # Bend Type List
                    if pose_bones['PROP_Customization_Settings'].get('Bend_Type') == 0:
                        c2.prop(pose_bones['PROP_Customization_Settings'], '["Bend_Type"]', text='Bend Type: Sharp')
                    if pose_bones['PROP_Customization_Settings'].get('Bend_Type') == 1:
                        c2.prop(pose_bones['PROP_Customization_Settings'], '["Bend_Type"]', text='Bend Type: Round')
                    if pose_bones['PROP_Customization_Settings'].get('Bend_Type') == 2:
                        c2.prop(pose_bones['PROP_Customization_Settings'], '["Bend_Type"]', text='Bend Type: Smooth')
                    #---
                    c2 = b2.column(align=True)
                    c2.prop(pose_bones['PROP_Customization_Settings'], '["Head_Squash"]', text='Head Squash')
                    c2.prop(pose_bones['PROP_Customization_Settings'], '["Body_Squash"]', text='Body Squash')
                    r2 = b2.row(align=True)
                    r2.label(text= "      Right Arm")
                    r2.label(text= "      Left Arm")
                    c2 = b2.column(align=True)
                    g2 = c2.grid_flow(columns=2, align=True)
                    g2.prop(pose_bones['PROP_Customization_Settings'], '["RArm_Stretch"]', text='Stretch')
                    g2.prop(pose_bones['PROP_Customization_Settings'], '["RArm_Squash"]', text='Squash')
                    g2.prop(pose_bones['PROP_Customization_Settings'], '["LArm_Stretch"]', text='Stretch')
                    g2.prop(pose_bones['PROP_Customization_Settings'], '["LArm_Squash"]', text='Squash')
                    r2 = b2.row(align=True)
                    r2.label(text= "      Right Leg")
                    r2.label(text= "      Left Leg")
                    c2 = b2.column(align=True)
                    g2 = c2.grid_flow(columns=2, align=True)
                    g2.prop(pose_bones['PROP_Customization_Settings'], '["RLeg_Stretch"]', text='Stretch')
                    g2.prop(pose_bones['PROP_Customization_Settings'], '["RLeg_Squash"]', text='Squash')
                    g2.prop(pose_bones['PROP_Customization_Settings'], '["LLeg_Stretch"]', text='Stretch')
                    g2.prop(pose_bones['PROP_Customization_Settings'], '["LLeg_Squash"]', text='Squash')
                    c2 = b2.column(align=True)
                    # Breast Type List
                    if pose_bones['PROP_Customization_Settings'].get('Breast_Type') == 0:
                        c2.prop(pose_bones['PROP_Customization_Settings'], '["Breast_Type"]', text='Breast Type: Sharp')
                    if pose_bones['PROP_Customization_Settings'].get('Breast_Type') == 1:
                        c2.prop(pose_bones['PROP_Customization_Settings'], '["Breast_Type"]', text='Breast Type: Round')
                    #---
                    c2.prop(pose_bones['PROP_Customization_Settings'], '["Breast_Size"]', text='Breast Size')
                    if pose_bones['PROP_Customization_Settings'].get('Breast_Type') == 0:
                        c2.prop(pose_bones['PROP_Customization_Settings'], '["Breast_Sharp_Edge"]', text='Breast Sharp Edge')
                    c2 = b2.column(align=True)
                    c2.prop(pose_bones['PROP_Customization_Settings'], '["Chest_Deform"]', text='Chest Deform')
                    c2.prop(pose_bones['PROP_Customization_Settings'], '["Breathe_Deform"]', text='Breathe Deform')
                    c2.prop(pose_bones['PROP_Customization_Settings'], '["Hip_Deform"]', text='Hip Deform')
                
#~~~~~~~~~~~~~~~~~~~~~~~~~
#     Render Settings     
#~~~~~~~~~~~~~~~~~~~~~~~~~

            if obj.get('SettingsTab2') == 2:
                b = layout.box()
                r = b.row(align=True)
                r.label(text= "Default Settings", icon= 'PROPERTIES')
                r = b.row(align=True)
                r.prop(obj, "SettingsTab2", text = "SettingsTab2", expand=True)
                
                # Anti-Lag Settings
                
                b1 = b.box()
                r1 = b1.row(align=True)
                r1.label(text= "Anti-Lag Settings", icon= 'RESTRICT_VIEW_ON')
                if(toggleButton(obj, r1, "AntilagSettings", "")):
                    c1 = b1.column(align=True)
                    c1.prop(pose_bones['PROP_Render_Settings'], '["Antilag_Head"]', text='Anti-Lag (Head)')
                    c1.prop(pose_bones['PROP_Render_Settings'], '["Antilag_Body"]', text='Anti-Lag (Body)')
                    c1.prop(pose_bones['PROP_Render_Settings'], '["Antilag_Arm"]', text='Anti-Lag (Arm)')
                    c1.prop(pose_bones['PROP_Render_Settings'], '["Antilag_Leg"]', text='Anti-Lag (Leg)')
                
                # Vewport Render
                
                b2 = b.box()
                r2 = b2.row(align=True)
                r2.label(text= "Vewport Render", icon= 'RESTRICT_VIEW_ON')
                if(toggleButton(obj, r2, "ViewportRender", "")):
                    c2 = b2.column(align=True)
                    c2.prop(pose_bones['PROP_Render_Settings'], '["Head_Visibility"]', text='Head Visibility')
                    c2 = b2.column(align=True)
                    c2.prop(pose_bones['PROP_Render_Settings'], '["Body_Visibility"]', text='Body Visibility')
                    c2 = b2.column(align=True)
                    c2.prop(pose_bones['PROP_Render_Settings'], '["RArm_Visibility"]', text='RArm Visibility')
                    c2.prop(pose_bones['PROP_Render_Settings'], '["LArm_Visibility"]', text='LArm Visibility')
                    c2 = b2.column(align=True)
                    c2.prop(pose_bones['PROP_Render_Settings'], '["RLeg_Visibility"]', text='RLeg Visibility')
                    c2.prop(pose_bones['PROP_Render_Settings'], '["LLeg_Visibility"]', text='LLeg Visibility')
                
                # Vewport Render
                
                b3 = b.box()
                r3 = b3.row(align=True)
                r3.label(text= "SubSurf Settings", icon= 'MOD_SUBSURF')
                if(toggleButton(obj, r3, "SubsurfSettings", "")):
                    c3 = b3.column(align=True)
                    c3.prop(pose_bones['PROP_Render_Settings'], '["Head_SubSurf_Viewport"]', text='Head Viewport')
                    c3.prop(pose_bones['PROP_Render_Settings'], '["Head_SubSurf_Render"]', text='Head Render')
                    c3 = b3.column(align=True)
                    c3.prop(pose_bones['PROP_Render_Settings'], '["Body_SubSurf_Viewport"]', text='Body Viewport')
                    c3.prop(pose_bones['PROP_Render_Settings'], '["Body_SubSurf_Render"]', text='Body Render')
                    c3 = b3.column(align=True)
                    c3.prop(pose_bones['PROP_Render_Settings'], '["RArm_SubSurf_Viewport"]', text='RArm Viewport')
                    c3.prop(pose_bones['PROP_Render_Settings'], '["RArm_SubSurf_Render"]', text='RArm Render')
                    c3.prop(pose_bones['PROP_Render_Settings'], '["LArm_SubSurf_Viewport"]', text='LArm Viewport')
                    c3.prop(pose_bones['PROP_Render_Settings'], '["LArm_SubSurf_Render"]', text='LArm Render')
                    c3 = b3.column(align=True)
                    c3.prop(pose_bones['PROP_Render_Settings'], '["RLeg_SubSurf_Viewport"]', text='RLeg Viewport')
                    c3.prop(pose_bones['PROP_Render_Settings'], '["RLeg_SubSurf_Render"]', text='RLeg Render')
                    c3.prop(pose_bones['PROP_Render_Settings'], '["LLeg_SubSurf_Viewport"]', text='LLeg Viewport')
                    c3.prop(pose_bones['PROP_Render_Settings'], '["LLeg_SubSurf_Render"]', text='LLeg Render')

#-------------------------
#     Custom Settings     
#-------------------------

        if obj.get('SettingsTab1') == 1:
            b = layout.box()
            r = b.row(align=True)
            r.label(text= "Custom Settings", icon= 'PROPERTIES')
            c = b.column(align=True)
        
            for p in self.getProperties(rig):
                c.prop(bpy.context.active_object.pose.bones[f'{self.propBone}'], '["%s"]' % str(p))

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     Register & Unregister     
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
def register():
    bpy.utils.register_class(InfoPanel)
    bpy.utils.register_class(MainPanel)
    
def unregister():
    bpy.utils.unregister_class(InfoPanel)
    bpy.utils.unregister_class(MainPanel)
    
if __name__== "__main__":
    register()