local BUTTON_FUNCTION_1 = 3
local BUTTON_FUNCTION_2 = 4

local pin1 = 10
local pin2 = 11

function update()
  if sub:is_button_pressed(BUTTON_FUNCTION_1) then
      gpio:write(96, 1)
      gpio:write(97, 0)
  if sub:is_button_pressed(BUTTON_FUNCTION_2) then
      gpio:write(96, 0)
      gpio:write(97, 1)
--if we use this code in 2027 just why
  if sub:is_button_pressed(!BUTTON_FUNCTION_1) then
      if sub:is_button_pressed(!BUTTON_FUNCTION_2) then
	gpio:write(96, 0)
	gpio:write(97, 0)
  end
  

  return update, 0
end

return update()