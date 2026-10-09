local ServoPin = 96
--Script function value for the Servo might not be 96. If that is the case, change the number (May be 94-97 if a function)
local Val1 = 1000
local Val2 = 1500
local Val3 = 2000
local ValToggle = 1
local ButtonFunction = 2
local ButtonState = false
local LastButtonState = false
function update()
    ButtonState = sub:is_button_pressed(ButtonFunction)
    if ButtonState and not LastButtonState then
        if ValToggle == 1 then
            SRV_Channels:set_output_pwm(ServoPin, Val1)
            ValToggle = 2
        elseif ValToggle == 2 then
            SRV_Channels:set_output_pwm(ServoPin, Val2)
            ValToggle = 3
        elseif ValToggle == 3 then
            SRV_Channels:set_output_pwm(ServoPin, Val3)
            ValToggle = 1
        end
    end
    LastButtonState = ButtonState
    return update, 50
end
return update, 50