local LibExtraTip = LibStub("LibExtraTip-1")
AceBIS = LibStub("AceAddon-3.0"):NewAddon("AceBIS")
AceBIS.BIS = {}
AceBIS.Items = {}

local addonName, addonTable = ...
local iconpath = "Interface\\GLUES\\CHARACTERCREATE\\UI-CharacterCreate-Classes"
local iconCutoff = 6

AceBISGears = {}

function AceBIS:OnInitialize()
	local options = {
		name = "AceBIS v" .. GetAddOnMetadata("AceBIS", "Version"),
		handler = AceBIS,
		type = "group",
		args = {
			P0 = {
				name = "Phase 0",
				type = "toggle",
				desc = "show phase 0 gears",
				set = "SetPhase",
				get = "GetPhase"
			},
			P1 = {
				name = "Phase 1",
				type = "toggle",
				desc = "show phase 1 gears",
				set = "SetPhase",
				get = "GetPhase"
			},
			P2 = {
				name = "Phase 2",
				type = "toggle",
				desc = "show phase 2 gears",
				set = "SetPhase",
				get = "GetPhase"
			},
			P3 = {
				name = "Phase 3",
				type = "toggle",
				desc = "show phase 3 gears",
				set = "SetPhase",
				get = "GetPhase"
			},
			Warrior = {
				name = "Warrior",
				type = "group",
				args = {
					Protection = {
						name = "Protection",
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					Arms = {
						name = "Arms",
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					Fury = {
						name = "Fury",
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					}
				}
			},
			Priest = {
				name = "Priest",
				type = "group",
				args = {
					Holy = {
						name = "Holy",
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					Shadow = {
						name = "Shadow",
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					}
				}
			},
			Mage = {
				name = "Mage",
				type = "group",
				args = {
					Arcane = {
						name = "Arcane",
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					Fire = {
						name = "Fire",
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					}
				}
			},
			Warlock = {
				name = "Warlock",
				type = "group",
				args = {
					Affliction = {
						name = "Affliction",
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					Destruction = {
						name = "Destruction",
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					}
				}
			},
			Druid = {
				name = "Druid",
				type = "group",
				args = {
					Balance = {
						name = "Balance",
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					FeralDPS = {
						name = "Feral(DPS)",
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					FeralTank = {
						name = "Feral(Tank)",
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					Restoration = {
						name = "Restoration",
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					}
				}
			},
			Rogue = {
				name = "Rogue",
				type = "group",
				args = {
					Combat = {
						name = "Combat",
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
				}
			},
			Hunter = {
				name = "Hunter",
				type = "group",
				args = {
					BeastMastery = {
						name = "BeastMastery",
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					Survival = {
						name = "Survival",
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					}
				}
			},
			Shaman = {
				name = "Shaman",
				type = "group",
				args = {
					Elemental = {
						name = "Elemental",
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					Enhancement = {
						name = "Enhancement",
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					Restoration = {
						name = "Restoration",
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
				}
			},
			Paladin = {
				name = "Paladin",
				type = "group",
				args = {
					Holy = {
						name = "Holy",
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					Protection = {
						name = "Protection",
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					Retribution = {
						name = "Retribution",
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
				}
			},
		}
	}
	LibStub("AceConfig-3.0"):RegisterOptionsTable("AceBIS", options, nil)
	LibStub("AceConfigDialog-3.0"):AddToBlizOptions("AceBIS", "AceBIS")
end

function AceBIS:SetPhase(info, val)
	AceBISGears[info[#info]] = val
end

function AceBIS:GetPhase(info)
	if AceBISGears[info[#info]] == nil then
		AceBISGears[info[#info]] = true
	end
	return AceBISGears[info[#info]]
end

function dump(o)
   if type(o) == 'table' then
      local s = '{ '
      for k,v in pairs(o) do
         if type(k) ~= 'number' then k = '"'..k..'"' end
	 	if type(v) == 'table' then
         		s = s .. '['..k..'] = ' .. "dump(v)" .. ','
		else
         		s = s .. '['..k..'] = ' .. tostring(v) .. ','
		end

      end
      return s .. '} '
   else
      return tostring(o)
   end
end

function AceBIS:Set(info, val)
	class = info[1]
	tag = info[#info]
	spec = info["options"]["args"][class]["args"][tag]["name"]
	AceBISGears[spec .. class] = val
end

function AceBIS:Get(info)
	class = info[1]
	tag = info[#info]
	spec = info["options"]["args"][class]["args"][tag]["name"]
	if AceBISGears[spec .. class] == nil then
		AceBISGears[spec .. class] = true
	end
	return AceBISGears[spec .. class]
end

local function iconOffset(col, row)
	local offsetString = (col * 64 + iconCutoff) .. ":" .. ((col + 1) * 64 - iconCutoff)
	return offsetString .. ":" .. (row * 64 + iconCutoff) .. ":" .. ((row + 1) * 64 - iconCutoff)
end

local function buildExtraTip(tooltip, entry)
	local r,g,b = .9,.8,.5
	LibExtraTip:AddLine(tooltip," ",r,g,b,true)
	LibExtraTip:AddLine(tooltip,"# BIS:",r,g,b,true)

	
	for k, v in pairs(entry) do
		local entry = AceBIS.BIS[k]
		local class = entry.class:upper()
		local build = entry.spec
		local slot = entry.slot
		local color = RAID_CLASS_COLORS[class]
		local coords = CLASS_ICON_TCOORDS[class]
		local classfontstring = "|T" .. iconpath .. ":14:14:::256:256:" .. iconOffset(coords[1] * 4, coords[3] * 4) .. "|t"
		if AceBISGears[build] == nil then
			AceBISGears[build] = true
		end
		if AceBISGears[entry.phase] == nil then
			AceBISGears[entry.phase] = true
		end
		if AceBISGears[build] and AceBISGears[entry.phase] then
		
			LibExtraTip:AddDoubleLine(tooltip, classfontstring .. " " .. entry.class .. " " .. build, v, color.r, color.g, color.b, color.r, color.g, color.b, true)
		end
	end
	
	LibExtraTip:AddLine(tooltip," ",r,g,b,true)
end

local function onTooltipSetItem(tooltip, itemLink, quantity)
	if not itemLink then return end
    
	local itemString = string.match(itemLink, "item[%-?%d:]+")
	local itemId = ({ string.split(":", itemString) })[2]

	if AceBIS.Items[itemId] then
		buildExtraTip(tooltip, AceBIS.Items[itemId])
	end
end

local eventframe = CreateFrame("FRAME",addonName.."Events")

local function onEvent(self,event,arg)
	if event == "PLAYER_ENTERING_WORLD" then
		eventframe:UnregisterEvent("PLAYER_ENTERING_WORLD")
		LibExtraTip:AddCallback({type = "item", callback = onTooltipSetItem, allevents = true})
		LibExtraTip:RegisterTooltip(GameTooltip)
		LibExtraTip:RegisterTooltip(ItemRefTooltip)
	end
end

eventframe:RegisterEvent("PLAYER_ENTERING_WORLD")
eventframe:SetScript("OnEvent", onEvent)

function AceBIS:RegisterBIS(class, build, phase, slot)
	if not spec then spec = "" end
	if not comment then comment = "" end
	
	local bis = {
		class = class,
		spec = build,
		phase = phase,
		slot, slot
	}
	
	bis.ID = class .. build .. phase

	AceBIS.BIS[bis.ID] = bis
	return bis
end

function AceBIS:BISitem(bisEntry, index, id, phase)
	if not AceBIS.Items[id] then
		AceBIS.Items[id] = {}
	end

	AceBIS.Items[id][bisEntry.ID] = phase .. " #" .. index
end
