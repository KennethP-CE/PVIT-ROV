local LIGHT_FUNCTION = 94
local LIGHT_FUNCTION2 = 95
local OFF_VALUE = 1100
local ON_VALUE = 1900
local BUTTON_FUNCTION_1 = 2

local lights_on = false
local last_button_state = false

function update()
    local button_state = sub:is_button_pressed(BUTTON_FUNCTION_1)
--  I am insanely bord borad boerd HOW DO YOU SPELL BOARD.
    if button_state and not last_button_state then
        lights_on = not lights_on
        local pwm_value = lights_on and ON_VALUE or OFF_VALUE
        SRV_Channels:set_output_pwm(LIGHT_FUNCTION, pwm_value)
        SRV_Channels:set_output_pwm(LIGHT_FUNCTION2, pwm_value)
    end

    last_button_state = button_state
    return update, 50 -- Run every 50ms
end

return update()

