from robotpy_ext.autonomous import state, timed_state, StatefulAutonomous
from components import intake, drive
import wpilib

class LowBar(StatefulAutonomous):
    DEFAULT = False
    
    intake = intake.Arm
    drive = drive.Drive
    def initialize(self):
        self.register_sd_var('Drive_Distance', 17.8)
        self.register_sd_var('Rotate_Angle', 55)
        self.register_sd_var('Ramp_Distance', 8.4)
    
    @state
    def LowBarStart(self):
        self.next_state('lower_arm')
    
    @timed_state(duration = 1, next_state='drive_forward')
    def lower_arm(self, initial_call):
        print('lower_arm')
        self.intake.set_arm_bottom()
            
        if self.intake.on_target(): 
            self.next_state('drive_forward')
    
    @state
    def drive_forward(self):
        #self.intake.set_arm_middle()
        if self.drive.drive_distance(self.Drive_Distance*12):
            self.next_state('transition')
    
class ChevalDeFrise(StatefulAutonomous):
    DEFAULT = False
    
    intake = intake.Arm
    drive = drive.Drive
    def initialize(self):
        self.register_sd_var("Drive_to_distance", 4.2)
        self.register_sd_var("Drive_on_distance", 1)
    
    @state
    def A1Start(self):
        self.next_state('drive_to')
    
    @timed_state(duration = 2, next_state='lower_arms')
    def A1_drive_to(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()
        
        if self.drive.drive_distance(self.Drive_to_distance*12):
            self.next_state('lower_arms')
            
    @timed_state(duration = .2, next_state='drive_on')
    def A1_lower_arms(self, initial_call):
        self.intake.set_arm_bottom()
        
        if self.intake.on_target():
            self.next_state('drive_on')
        
    @timed_state(duration = 2, next_state='drive_over')
    def A1_drive_on(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()
            
        if self.drive.drive_distance(self.Drive_on_distance*12):
            self.next_state('drive_over')
        
    @timed_state(duration = 4, next_state='transition')
    def A1_drive_over(self, initial_call):
        self.intake.set_arm_top()
        
        self.drive.move(0.3, 0)
        
class Portcullis(StatefulAutonomous):
    DEFAULT = False
    
    intake = intake.Arm
    drive = drive.Drive
    def initialize(self):
        self.register_sd_var("A0_Drive_Encoder_Distance", 4.70)
        self.register_sd_var("A0_Arm_To_Position", 1000)
        self.register_sd_var("A0_DriveThru_Speed", 0.4)
    
    @state
    def A0Start(self):
        self.next_state('A0_lower_arm')
    
    @timed_state(duration = 1.5, next_state='A0_drive_forward')
    def A0_lower_arm(self, initial_call):
        print('A0Lower_Arm')
        #self.intake.set_arm_bottom()
        self.intake.set_manual(1)
            
        #if self.intake.on_target():
        #    self.next_state('A0_drive_forward')
    
    @state
    def A0_drive_forward(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()
        
        if self.drive.drive_distance(self.A0_Drive_Encoder_Distance*12):
            self.next_state('A0_raise_arm')
    
    @timed_state(duration = 0.5, next_state='A0_drive_thru')
    def A0_raise_arm(self):
        self.intake.set_target_position(self.A0_Arm_To_Position)
        
        if self.intake.on_target():
            self.next_state('A0_drive_thru')
    
    @timed_state(duration = 3, next_state = 'transition')
    def A0_drive_thru(self):
        self.intake.set_arm_top()
        
        self.drive.move(self.A0_DriveThru_Speed, 0)

class Charge(StatefulAutonomous):
    DEFAULT = False
    
    @timed_state(duration = 3)
    def E0Start(self, initial_call):
        self.drive.move(1,0)