local L = LibStub("AceLocale-3.0"):GetLocale("AceBIS")
AceBIS = LibStub("AceAddon-3.0"):NewAddon("AceBIS", "AceConsole-3.0")
AceBIS.AceGUI = LibStub("AceGUI-3.0")
AceBIS.BIS = {}
AceBIS.Items = {}

AceBIS.ClassList = {}
AceBIS.ClassSpecList = {}
AceBIS.ClassSetList = {}

AceBIS.SelectedSetName = ""
AceBIS.CurrentClass = ""

local addonName, addonTable = ...
local iconpath = "Interface\\GLUES\\CHARACTERCREATE\\UI-CharacterCreate-Classes"
local iconCutoff = 6
local class, tag, spec, build, comment

AceBISGears = {}

function AceBIS:PrintError(text)
    AceBIS:Print("|cffff0000An error has occured: |cffffffff" .. text)
end

function AceBIS:InitOptions()
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
			Warrior = {
				name = L["Warrior"],
				type = "group",
				args = {
					Protection = {
						name = L["ProtectionWarrior"],
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					Arm = {
						name = L["ArmWarrior"],
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					Fury = {
						name = L["FuryWarrior"],
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					}
				}
			},
			Priest = {
				name = L["Priest"],
				type = "group",
				args = {
					Holy = {
						name = L["DisciplinePriest"],
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					Shadow = {
						name = L["ShadowPriest"],
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					}
				}
			},
			Mage = {
				name = L["Mage"],
				type = "group",
				args = {
					Arcane = {
						name = L["ArcaneMage"],
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					Fire = {
						name = L["FireMage"],
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					}
				}
			},
			Warlock = {
				name = L["Warlock"],
				type = "group",
				args = {
					Affliction = {
						name = L["AfflictionWarlock"],
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					}
				}
			},
			Druid = {
				name = L["Druid"],
				type = "group",
				args = {
					Balance = {
						name = L["BalanceDruid"],
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					Feral = {
						name = L["FeralDruid"],
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					Restoration = {
						name = L["RestorationDruid"],
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					}
				}
			},
			Rogue = {
				name = L["Rogue"],
				type = "group",
				args = {
					Combat = {
						name = L["AssassinationRogue"],
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
				}
			},
			Hunter = {
				name = L["Hunter"],
				type = "group",
				args = {
					Survival = {
						name = L["SurvivalHunter"],
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					}
				}
			},
			Shaman = {
				name = L["Shaman"],
				type = "group",
				args = {
					Elemental = {
						name = L["ElementalShaman"],
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					Enhancement = {
						name = L["EnhancementShaman"],
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					Restoration = {
						name = L["RestorationShaman"],
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
				}
			},
			Paladin = {
				name = L["Paladin"],
				type = "group",
				args = {
					Holy = {
						name = L["HolyPaladin"],
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					Protection = {
						name = L["ProtectionPaladin"],
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
					Retribution = {
						name = L["RetributionPaladin"],
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					},
				}
			},
			DK = {
				name = L["DK"],
				type = "group",
				args = {
					Unholy = {
						name = L["UnholyDK"],
						type = "toggle",
						desc = "Show gears for this class/spec on tooltips",
						set = "Set",
						get = "Get"
					}
				}
			},
		}
	}
	LibStub("AceConfig-3.0"):RegisterOptionsTable("AceBIS", options, nil)
	LibStub("AceConfigDialog-3.0"):AddToBlizOptions("AceBIS", "AceBIS")
end

function AceBIS:OnInitialize()
	local _,englishClass,_ = UnitClass("player")
    AceBIS.CurrentClass = englishClass:lower():gsub("^%l", string.upper)

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

local function dump(o)
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
	build = spec .. L[class]
	AceBISGears[build] = val
end

function AceBIS:Get(info)
	class = info[1]
	tag = info[#info]
	spec = info["options"]["args"][class]["args"][tag]["name"]
	build = spec .. L[class]
	if AceBISGears[build] == nil then
		AceBISGears[build] = true
	end
	return AceBISGears[build]
end

local function iconOffset(col, row)
	local offsetString = (col * 64 + iconCutoff) .. ":" .. ((col + 1) * 64 - iconCutoff)
	return offsetString .. ":" .. (row * 64 + iconCutoff) .. ":" .. ((row + 1) * 64 - iconCutoff)
end

function AceBIS:SlashCmd(cmd)
	if not cmd then cmd="" end

	cmd = cmd:lower()
	if cmd == "help" or cmd == "?" then
		print("|cFFE5CC7F[AceBIS]|r " .. "Shows the ranks of gears")
		print("|cFFE5CC7F[AceBIS]|r " .. "|cFFFFFF00/AceBIS|r to toggle the AceBIS window")
		print("|cFFE5CC7F[AceBIS]|r " .. "|cFFFFFF00/AceBIS options|r to toggle the AceBIS options window")
		print("|cFFE5CC7F[AceBIS]|r " .. "|cFFFFFF00/AceBIS help|?|r to show this help")
	elseif cmd == "options" then
		LibStub("AceConfigDialog-3.0"):Open("AceBIS")
	else
		-- toggle AceBIS window
		if (AceBIS.GearWindow:IsVisible()) then
			AceBIS.GearWindow:Hide()
		else
			AceBIS.GearWindow:Show()
		end
	end
end

local function AttachTooltip(self)
	local itemLink = select(2, self:GetItem())
	if not itemLink then
		return false
	end

	local itemString = string.match(itemLink, "item[%-?%d:]+")
	local itemId = ({ string.split(":", itemString) })[2]

	if AceBIS.Items[itemId] then
		local r,g,b = .9,.8,.5

		self:AddLine(" ",r,g,b,true)
		self:AddLine("# BIS:",r,g,b,true)
		
		for k, v in pairs(AceBIS.Items[itemId]) do
			local id = ({string.split(":", k)})[1]
			local entry = AceBIS.BIS[id]
			local class = entry.class:upper()
			if class == "DK" then
				class = "DEATHKNIGHT"
			end
			local spec = L[entry.spec]
			local build = L[entry.spec] .. L[entry.class]
			local slot = ({string.split(":", k)})[2]
			local color = RAID_CLASS_COLORS[class]
			local coords = CLASS_ICON_TCOORDS[class]
			local classfontstring = "|T" .. iconpath .. ":14:14:::256:256:" .. iconOffset(coords[1] * 4, coords[3] * 4) .. "|t"
			if class == "WARRIOR" or class == "ROGUE" or class == "SHAMAN" then
				if slot == "MainHand" or slot == "OffHand" then
					spec = spec .. "(" .. L[slot] .. ")"
				end
			end
			if AceBISGears[build] == nil then
				AceBISGears[build] = true
			end
			if AceBISGears[entry.phase] == nil then
				AceBISGears[entry.phase] = true
			end
			if AceBISGears[build] and AceBISGears[entry.phase] then
				self:AddDoubleLine(classfontstring .. " " .. L[entry.class] .. " " .. spec, v, color.r, color.g, color.b, color.r, color.g, color.b, true)
			end
		end
		
		self:AddLine(" ",r,g,b,true)
		self:Show()
	end

	return true
end

function AceBIS:OnEnable()
	SLASH_ACEBIS1 = "/acebis";
	SLASH_ACEBIS2 = "/ab";
	SlashCmdList["ACEBIS"] = function(msg)
		AceBIS:SlashCmd(msg);
	end

	GameTooltip:HookScript("OnTooltipSetItem", AttachTooltip)
	ItemRefTooltip:HookScript("OnTooltipSetItem", AttachTooltip)
	ItemRefShoppingTooltip1:HookScript("OnTooltipSetItem", AttachTooltip)
	ItemRefShoppingTooltip2:HookScript("OnTooltipSetItem", AttachTooltip)
	ShoppingTooltip1:HookScript("OnTooltipSetItem", AttachTooltip)
	ShoppingTooltip2:HookScript("OnTooltipSetItem", AttachTooltip)

	AceBIS:InitOptions()
	AceBIS.InitUI()
end

function AceBIS:RegisterBIS(class, build, phase)
	if not spec then spec = "" end
	if not comment then comment = "" end
	
	local bis = {
		class = class,
		spec = build,
		phase = phase
	}
	
	bis.ID = class .. build .. phase

	AceBIS.BIS[bis.ID] = bis

	AceBIS.ClassList[class] = class
	if not AceBIS.ClassSpecList[class] then
		AceBIS.ClassSpecList[class] = {}
	end
	AceBIS.ClassSpecList[class][build] = build

	return bis
end

function AceBIS:BISitem(bisEntry, index, id, phase, slot)
	if not AceBIS.Items[id] then
		AceBIS.Items[id] = {}
	end
	AceBIS.Items[id][bisEntry.ID .. ":" .. slot] = phase .. " #" .. index

	local class = bisEntry.class
	local spec = bisEntry.spec
	if not AceBIS.ClassSetList[class] then
		AceBIS.ClassSetList[class] = {}
	end
	if not AceBIS.ClassSetList[class][spec] then
		AceBIS.ClassSetList[class][spec] = {}
	end
	if not AceBIS.ClassSetList[class][spec][phase] then
		AceBIS.ClassSetList[class][spec][phase] = {}
	end
	if not AceBIS.ClassSetList[class][spec][phase][index] then
		AceBIS.ClassSetList[class][spec][phase][index] = {}
	end
	AceBIS.ClassSetList[class][spec][phase][index][slot] = id
end
