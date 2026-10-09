local UP_CH = 2
local DOWN_CH = 1

local VERTICAL_THRUSTER_1 = 5
local VERTICAL_THRUSTER_2 = 6

local UP_THRUST = 1660      -- Ascend
local DOWN_THRUST = 1340    -- Descend
local STOP_THRUST = 1500    -- Neutral / Stop

function update()
    local up = rc:get_pwm(UP_CH)
    local down = rc:get_pwm(DOWN_CH)

    if up ~= nil and up > 1800 then
        SRV_Channels:set_output_pwm(VERTICAL_THRUSTER_1, UP_THRUST)
        SRV_Channels:set_output_pwm(VERTICAL_THRUSTER_2, UP_THRUST)

    else if down ~= nil and down > 1800 then
        SRV_Channels:set_output_pwm(VERTICAL_THRUSTER_1, DOWN_THRUST)
        SRV_Channels:set_output_pwm(VERTICAL_THRUSTER_2, DOWN_THRUST)
--Kenneth John Preston III has infinite aura trust me
    else
        SRV_Channels:set_output_pwm(VERTICAL_THRUSTER_1, STOP_THRUST)
        SRV_Channels:set_output_pwm(VERTICAL_THRUSTER_2, STOP_THRUST)
    end

    return update, 50  -- run every 50 ms
end
return update()