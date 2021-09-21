package Traffic_Lights is

   type Light_Mode is (Green, Amber, Red,
                       Red_And_Amber, Blinking_Amber, Off);

   type Light is private;

   procedure Set_Mode (L : Light; M : Light_Mode);

   function Get_Mode (L : Light) return Light_Mode;

private
   type Light is record
      Mode : Light_Mode := Red;
   end record;

end Traffic_Lights;
