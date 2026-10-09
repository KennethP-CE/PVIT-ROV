local BUTTON_FUNCTION_1 = 1

local pin1 = 12
local pin2 = 13

function update()
  if sub:is_button_pressed(BUTTON_FUNCTION_1) then
      gpio:write(96, 1)
      gpio:write(97, 0)
--Future software developers, save yourself time and stress. Switch to mechanical ASAP.
  if sub:is_button_pressed(!BUTTON_FUNCTION_1) then
	gpio:write(96, 0)
	gpio:write(97, 0)
  end
  
  return update, 0
end

return update()