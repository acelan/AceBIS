-- Thanks Zentarg and his great work, BiSTracker
-- https://www.curseforge.com/wow/addons/bis-tracker-tbcc-classic
-- With his permission, I incorporate the paper doll system from BiSTracker to my addon.
-- In this file, most of the code are copied from BiSTracker/core/{AceGUILayouts.lua,Init.lua,GUI.lua}
AceBIS.GearWindow = AceBIS.AceGUI:Create("Window")
AceBIS.GearWindow.EditSlot = AceBIS.AceGUI:Create("Window")
AceBIS.GearWindow.ConfirmDelete = AceBIS.AceGUI:Create("Window")
AceBIS.GearWindow:Hide()
AceBIS.GearWindow.EditSlot:Hide()
AceBIS.GearWindow.ConfirmDelete:Hide()

local PhaseList = {"P0", "P1"}

AceBIS.SelectedPhase = 0
AceBIS.SelectedPhaseName = ""

local inventorySlotName = {
    Helm = "HEADSLOT",
    Neck = "NECKSLOT",
    Shoulder = "SHOULDERSLOT",
    Back = "BACKSLOT",
    Chest = "CHESTSLOT",
    Shirt = "SHIRTSLOT",
    Tabard = "TABARDSLOT",
    Bracers = "WRISTSLOT",
    Hands = "HANDSSLOT",
    Waist = "WAISTSLOT",
    Pants = "LEGSSLOT",
    Boots = "FEETSLOT",
    Finger = "FINGER0SLOT",
    RFinger = "FINGER1SLOT",
    Trinket = "TRINKET0SLOT",
    RTrinket = "TRINKET1SLOT",
    MainHand = "MAINHANDSLOT",
    TwoHand = "MAINHANDSLOT",
    SecondaryHand = "SECONDARYHANDSLOT",
    OffHand = "SECONDARYHANDSLOT",
    Ranged = "RANGEDSLOT"
}

local function tablecopy(tbl)
    if type(tbl) ~= "table" then return tbl end
    local t = {}
    for i,v in pairs(tbl) do
        t[i] = tablecopy(v)
    end
    return t
end

local function UpdateSelectedSetList()
    local class = AceBIS.SelectedClass
    local spec = AceBIS.SelectedSetName
    local phase = AceBIS.SelectedPhaseName
    local rank = 1
    local SelectedSetList = tablecopy(AceBIS.ClassSetList[AceBIS.SelectedClass][AceBIS.SelectedSetName][AceBIS.SelectedPhaseName]["1"])

    --AceBIS:Print("Update SetList to " .. AceBIS.SelectedClass .. " " .. AceBIS.SelectedSetName .. " " .. AceBIS.SelectedPhaseName)

    if AceBISGears["Gears"] == nil then
        AceBISGears["Gears"] = {}
    end

    for gear, rank in pairs(AceBISGears["Gears"]) do
        local matched = true
        local class = ({ string.split(":", gear) })[1]
        local spec = ({ string.split(":", gear) })[2]
        local phase = ({ string.split(":", gear) })[3]
        local slot = ({ string.split(":", gear) })[4]
        if class ~= AceBIS.SelectedClass then
            AceBIS:Print(class .. " != " .. AceBIS.SelectedClass)
            matched = false
        end
        if spec ~= AceBIS.SelectedSetName then
            AceBIS:Print(spec .. " != " .. AceBIS.SelectedSetName)
            matched = false
        end
        if phase ~= AceBIS.SelectedPhaseName then
            AceBIS:Print(phase .. " != " .. AceBIS.SelectedPhaseName)
            matched = false
        end

        if matched then
            local sslot = slot
            if slot == "RFinger" or slot == "RTrinket" then
                sslot = slot:sub(2)
            end
            while AceBIS.ClassSetList[class][spec][phase][tostring(rank)][sslot] == nil do
                if rank == 1 then
                    break
                end
                rank = rank - 1
            end

            SelectedSetList[slot] = AceBIS.ClassSetList[class][spec][phase][tostring(rank)][sslot]
            --AceBIS:Print(class .. spec .. phase .. slot .. " #" .. tostring(rank))
        end
    end

    -- Get RFINGER and RTRINKET
    rank = 1
    if SelectedSetList["RTrinket"] == nil then
        if AceBIS.ClassSetList[class][spec][phase][tostring(rank+1)]["Trinket"] == nil then
            rank = rank - 1
        else
            rank = rank + 1
        end
        SelectedSetList["RTrinket"] = AceBIS.ClassSetList[class][spec][phase][tostring(rank)]["Trinket"]
    end
    rank = 1
    if SelectedSetList["RFinger"] == nil then
        if AceBIS.ClassSetList[class][spec][phase][tostring(rank+1)]["Finger"] == nil then
            rank = rank - 1
        else
            rank = rank + 1
        end
        SelectedSetList["RFinger"] = AceBIS.ClassSetList[class][spec][phase][tostring(rank)]["Finger"]
    end

    return SelectedSetList
end

local function SetSelectedSet(set)
    --AceBIS:Print("Set " .. AceBIS.SelectedClass .. " to spec " .. set)
    AceBISGears[AceBIS.SelectedClass .. "Set"] = set
end

local function GetSelectedSet()
    if AceBISGears[AceBIS.SelectedClass .. "Set"] == nil then
        --AceBIS:Print("Get " .. AceBIS.SelectedClass .. " spec is nil")
        return nil
    end
    --AceBIS:Print("Get " .. AceBIS.SelectedClass .. " to spec " .. AceBISGears[AceBIS.SelectedClass .. "Set"])
    return AceBISGears[AceBIS.SelectedClass .. "Set"]
end

local function SetConfig(class, set, phase, slot, rank)
    if AceBISGears["Gears"] == nil then
        AceBISGears["Gears"] = {}
    end

    if rank == 1 then
        AceBISGears["Gears"][class .. ":" .. set .. ":" .. phase .. ":" .. slot] = nil
    else
        AceBISGears["Gears"][class .. ":" .. set .. ":" .. phase .. ":" .. slot] = rank
    end
    --AceBIS:Print("Set " .. slot .. " to " .. AceBIS.ClassSetList[class][set][phase][tostring(rank)][slot])
end

local function GetConfig(class, set, phase, slot)
    if AceBISGears["Gears"] == nil then
        AceBISGears["Gears"] = {}
    end

    if AceBISGears["Gears"][class .. ":" .. set .. ":" .. phase .. ":" .. slot] == nil then
        AceBISGears["Gears"][class .. ":" .. set .. ":" .. phase .. ":" .. slot] = 1
    end

    return AceBISGears["Gears"][class .. ":" .. set .. ":" .. phase .. ":" .. slot]
end

AceBIS.AceGUI:RegisterLayout("AceBISSheet",
    function(content, children)

    local height = 0
    local width = content.width or content:GetWidth() or 0
    for i = 1, #children do
        local child = children[i]

        local frame = child.frame
        frame:ClearAllPoints()
        frame:Show()

        if i == 1 then
            frame:SetPoint("TOPLEFT", content, 0, 10)     -- TopLeftButtonGroup
        elseif i == 2 then
            frame:SetPoint("TOPRIGHT", content, 0, 10)     -- TopRightButtonGroup
        elseif i == 3 then
            frame:SetPoint("TOP", content, 0, 5)         -- SetName
        elseif i == 4 then
            frame:SetPoint("TOPLEFT", content, 0, -30)     -- LeftSlots
        elseif i == 5 then
            frame:SetPoint("BOTTOM", content, 0, 40)    -- BottomSlots
        elseif i == 6 then
            frame:SetPoint("TOPRIGHT", content, 0, -30) -- RightSlots
        elseif i == 7 then
            frame:SetPoint("BOTTOM", content, 0, -5)     -- ActionsGroup
        end

        if child.width == "fill" then
            child:SetWidth(width)
            frame:SetPoint("RIGHT", content)

            if child.DoLayout then
                child:DoLayout()
            end
        elseif child.width == "relative" then
            child:SetWidth(width * child.relWidth)

            if child.DoLayout then
                child:DoLayout()
            end
        end

        height = height + (frame.height or frame:GetHeight() or 0)
    end
end)

AceBIS.AceGUI:RegisterLayout("AceBISEditSlot",
    function(content, children)

    local height = 0
    local width = content.width or content:GetWidth() or 0
    for i = 1, #children do
        local child = children[i]

        local frame = child.frame
        frame:ClearAllPoints()
        frame:Show()

        if i == 1 then
            frame:SetPoint("TOP", content, 0, 10) -- ID
        elseif i == 2 then
            frame:SetPoint("TOP", content, 0, -35) -- Obtain Method
        elseif i == 3 then
            frame:SetPoint("TOP", content, 0, -80) -- Obtain ID
        elseif i == 4 then
            frame:SetPoint("TOP", content, 0, -125) -- Zone
        elseif i == 5 then
            frame:SetPoint("TOP", content, 0, -170) -- Npc Name
        elseif i == 6 then
            frame:SetPoint("TOP", content, 0, -215) -- Drop Chance
        elseif i == 7 then
            frame:SetPoint("BOTTOMLEFT", content, 0, 0) -- Cancel Button
        elseif i == 8 then
            frame:SetPoint("BOTTOMRIGHT", content, 0, 0) -- Save Button
        end

        if child.width == "fill" then
            child:SetWidth(width)
            frame:SetPoint("RIGHT", content)

            if child.DoLayout then
                child:DoLayout()
            end
        elseif child.width == "relative" then
            child:SetWidth(width * child.relWidth)

            if child.DoLayout then
                child:DoLayout()
            end
        end

        height = height + (frame.height or frame:GetHeight() or 0)
    end
end)

AceBIS.AceGUI:RegisterLayout("AceBISConfirmDelete",
    function(content, children)

    local height = 0
    local width = content.width or content:GetWidth() or 0
    for i = 1, #children do
        local child = children[i]

        local frame = child.frame
        frame:ClearAllPoints()
        frame:Show()

        if i == 1 then
            frame:SetPoint("TOP", content, 0, 0) -- Text
        elseif i == 2 then
            frame:SetPoint("BOTTOMLEFT", content, 0, 0) -- Cancel Button
        elseif i == 3 then
            frame:SetPoint("BOTTOMRIGHT", content, 0, 0) -- Confirm Button
        end

        if child.width == "fill" then
            child:SetWidth(width)
            frame:SetPoint("RIGHT", content)

            if child.DoLayout then
                child:DoLayout()
            end
        elseif child.width == "relative" then
            child:SetWidth(width * child.relWidth)

            if child.DoLayout then
                child:DoLayout()
            end
        end

        height = height + (frame.height or frame:GetHeight() or 0)
    end
end)

local function UpdateModelFrame()
    AceBIS.GearWindow.Model:SetAllPoints(AceBIS.GearWindow.frame)
    AceBIS.GearWindow.Model:SetModelScale(0.75)
    AceBIS.GearWindow.Model:SetUnit("PLAYER")
    AceBIS.GearWindow.Model:SetCustomCamera(1)
    AceBIS.GearWindow.Model:SetPosition(0,0,0)
    AceBIS.GearWindow.Model:SetLight(true, false, 0, 0.8, -1, 1, 1, 1, 1, 0.3, 1, 1, 1)
end

function AceBIS.GearWindow.ConfirmDelete:RemoveSet(setName)
    if (setName ~= nil) then
        AceBIS.GearWindow.ConfirmDelete.Values.Text:SetText("Are you sure you want to delete the set |cffff0000"..setName.."|r?")
        AceBIS.GearWindow.ConfirmDelete:Show()
    end
end

function AceBIS.GearWindow:UpdateSetDisplay()
    UpdateModelFrame()
    AceBIS.GearWindow.SetName:SetText(AceBIS.SelectedSetName .. " - " .. AceBIS.SelectedPhaseName)
    AceBIS.GearWindow.Model:Undress()
    if (AceBIS.SelectedSetName == nil) then
        for k, v in pairs(AceBIS.GearWindow.Slots) do
            if (type(k) == "number") then
                AceBIS.GearWindow.Slots[v]:SetImage(AceBIS.GearWindow.DefaultSlotIcons[v])
                AceBIS.GearWindow.Slots[v]:SetCallback("OnEnter", function()
                    GameTooltip:SetText("")
                end)
            end
        end
    else
        local SelectedSetSlots = UpdateSelectedSetList()
        for key, value in pairs(SelectedSetSlots) do -- key = Wrists, value = 30684
            --AceBIS:Print("key = " .. key .. ", value = " .. value)
            local item = Item:CreateFromItemID(tonumber(value))
            local _,_,_,_,itemTexture = GetItemInfoInstant(tonumber(value))
            if itemTexture then
                if pcall(function(...)
                    AceBIS.GearWindow.Slots[key]:SetImage(itemTexture)
                    end) == false then
                    AceBIS:Print(value .. ",")
                end
            end
            item:ContinueOnItemLoad(function(id)
                local itemLink = item:GetItemLink()
                itemTexture = item:GetItemIcon()
                if itemLink then
                    if (key ~= "Ranged" or AceBIS.SelectedClass == "Hunter") then
                        AceBIS.GearWindow.Model:TryOn(itemLink)
                    end
                    AceBIS.GearWindow.Slots[key]:SetCallback("OnEnter", function()
                        if (IsControlKeyDown()) then
                            ShowInspectCursor()
                        end
                        AceBIS.IsHoveringItemSlot = key
                        GameTooltip:SetOwner(AceBIS.GearWindow.Slots[key].frame, "ANCHOR_RIGHT")
                        GameTooltip:SetHyperlink(itemLink)
                        GameTooltip:Show()
                    end)
                    if AceBIS.IsHoveringItemSlot and AceBIS.IsHoveringItemSlot == key then
                        GameTooltip:SetHyperlink(itemLink)
                    end
                end
                if itemTexture then
                    AceBIS.GearWindow.Slots[key]:SetImage(itemTexture)
                end
            end)
        end
    end
end

local function CreateIcon(imageHeight, imageWidth, height, width, image)
    local o = AceBIS.AceGUI:Create("Icon")
    o:SetImageSize(imageHeight, imageWidth)
    o:SetHeight(height)
    o:SetWidth(width)
    o:SetImage(image)
    return o
end

local function CreateButton(text, disabled, width)
    local o = AceBIS.AceGUI:Create("Button")
    o:SetText(text)
    o:SetDisabled(disabled)
    o:SetWidth(width)
    return o
end

local function CreateLabel(text, centered, r, g, b, font)
    local o = AceBIS.AceGUI:Create("Label")
    o:SetText(text)
    if (centered ~= nil and centered ~= false) then
        o:SetJustifyH("TOP")
    end 
    if (font ~= nil) then
        o:SetFontObject(font)
    end
    if (r ~= nil and g ~= nil and b ~= nil) then
        o:SetColor(r, g, b)
    end
    return o
end

local function CreateInteractiveLabel(text, centered, r, g, b, font)
    local o = AceBIS.AceGUI:Create("InteractiveLabel")
    o:SetText(text)
    if (centered ~= nil and centered ~= false) then
        o:SetJustifyH("TOP")
    end 
    if (font ~= nil) then
        o:SetFontObject(font)
    end
    if (r ~= nil and g ~= nil and b ~= nil) then
        o:SetColor(r, g, b)
    end
    return o
end

local function CreateEditBox(text, label, disabled, disableButton, maxLetters, width)
    local o = AceBIS.AceGUI:Create("EditBox")
    o:SetText(text)
    o:SetLabel(label)
    o:SetDisabled(disabled)
    o:DisableButton(disableButton)
    o:SetMaxLetters(maxLetters)
    o:SetWidth(width)
    return o
end

local function CreateSimpleGroup(layout, width, height)
    local o = AceBIS.AceGUI:Create("SimpleGroup")
    o:SetLayout(layout)
    if (width ~= 0) then o:SetWidth(width) end
    if (height ~= 0) then o:SetHeight(height) end
    return o
end

local function CreateDropdownMenu(label, defaultValue, children, width)
    local o = AceBIS.AceGUI:Create("Dropdown")
    o:SetList(children)
    o:SetValue(defaultValue)
    o:SetLabel(label)
    o:SetWidth(width)
    return o
end

local function ObtainMethodValueChanged(self)
    local val = self:GetValue()
    AceBIS.GearWindow.EditSlot.Values.ObtainID.frame:Show()
    AceBIS.GearWindow.EditSlot.Values.ObtainID:SetText("")
    AceBIS.GearWindow.EditSlot.Values.NpcName:SetText("")
    AceBIS.GearWindow.EditSlot.Values.DropChance:SetText("")
    AceBIS.GearWindow.EditSlot.Values.Zone:SetText("")

    AceBIS.GearWindow.EditSlot.Values.NpcName.frame:Hide()
    AceBIS.GearWindow.EditSlot.Values.DropChance.frame:Hide()
    AceBIS.GearWindow.EditSlot.Values.Zone.frame:Hide()

    if (val == 1) then
        AceBIS.GearWindow.EditSlot.Values.NpcName.frame:Show()
        AceBIS.GearWindow.EditSlot.Values.DropChance.frame:Show()
        AceBIS.GearWindow.EditSlot.Values.Zone.frame:Show()
        AceBIS.GearWindow.EditSlot.Values.ObtainID:SetLabel("Npc ID")
        AceBIS.GearWindow.EditSlot.Values.NpcName:SetLabel("Npc Name")
    elseif (val == 2) then
        AceBIS.GearWindow.EditSlot.Values.NpcName.frame:Show()
        AceBIS.GearWindow.EditSlot.Values.Zone.frame:Show()
        AceBIS.GearWindow.EditSlot.Values.ObtainID:SetLabel("Npc ID")
        AceBIS.GearWindow.EditSlot.Values.NpcName:SetLabel("Npc Name")
    elseif (val == 3) then
        AceBIS.GearWindow.EditSlot.Values.NpcName.frame:Show()
        AceBIS.GearWindow.EditSlot.Values.Zone.frame:Show()
        AceBIS.GearWindow.EditSlot.Values.ObtainID:SetLabel("Container ID")
        AceBIS.GearWindow.EditSlot.Values.NpcName:SetLabel("Container Name")
    elseif (val == 4) then
        AceBIS.GearWindow.EditSlot.Values.Zone.frame:Show()
        AceBIS.GearWindow.EditSlot.Values.ObtainID:SetLabel("Quest ID")
    elseif (val == 5) then
        AceBIS.GearWindow.EditSlot.Values.ObtainID:SetLabel("Recipe ID")
    elseif (val == 6) then
        AceBIS.GearWindow.EditSlot.Values.ObtainID.frame:Hide()
    end
end

function AceBIS.GearWindow:UpdateSetDropdown(set)
    AceBIS.GearWindow.ActionsGroup.SetDropdown:SetList(AceBIS.ClassSpecList[AceBIS.SelectedClass])
    local _
    if (set == nil) then
        set, _ = next(AceBIS.ClassSpecList[AceBIS.SelectedClass])
    end
    AceBIS.GearWindow.ActionsGroup.SetDropdown:SetValue(set)
    AceBIS.SelectedSetName = set
end

local function CreateSlotIcon(slot, image, imagex, imagey, width, height)
    local o = CreateIcon(imagex, imagey, width, height, image)

    o:SetCallback("OnClick", function(self)
        local sslot = slot
        if slot == "RFinger" or slot == "RTrinket" then
            sslot = slot:sub(2)
        end
        local Rank = GetConfig(AceBIS.SelectedClass, AceBIS.SelectedSetName, AceBIS.SelectedPhaseName, slot)
        if (IsShiftKeyDown()) then
            local itemLink, _
            _, itemLink = GetItemInfo(AceBIS.ClassSetList[AceBIS.SelectedClass][AceBIS.SelectedSetName][AceBIS.SelectedPhaseName][tostring(Rank)][sslot])
            ChatEdit_InsertLink(itemLink)
        else
            local val, startval, endval, stepval = Rank

            -- keep search  it only happens when there are less than 15 listed items
            while true do
                if IsControlKeyDown() then
                    startval = 16
                    endval = 1
                    stepval = -1
                else
                    startval = 0
                    endval = 15
                    stepval = 1
                end
                if val == endval then
                    val = startval
                end

                for rank=val+stepval, endval, stepval do
                    --AceBIS:Print("rank = " .. rank .. ", val = " .. val .. ", endval = " .. endval)
                    if AceBIS.ClassSetList[AceBIS.SelectedClass][AceBIS.SelectedSetName][AceBIS.SelectedPhaseName][tostring(rank)][sslot] ~= nil then
                        SetConfig(AceBIS.SelectedClass, AceBIS.SelectedSetName, AceBIS.SelectedPhaseName, slot, rank)
                        AceBIS.GearWindow:UpdateSetDisplay()
                        return
                    else
                        val = endval
                    end
                end
            end
        end
    end)

    o:SetCallback("OnLeave", function(self)
        SetCursor(nil)
        AceBIS.IsHoveringItemSlot = false
        GameTooltip:SetText("")
    end)

    return o
end

function AceBIS.GearWindow.EditSlot:ResetWindow()
    for key, value in pairs(AceBIS.GearWindow.EditSlot.Values) do
        if (key ~= "CancelButton" and key ~= "SaveButton") then
            if (key ~= "ObtainMethod") then
                value:SetText("")
            else
                value:SetValue(1)
            end
        end
    end
    AceBIS.GearWindow.EditSlot:SetTitle("Edit Slot")
    AceBIS.GearWindow.EditSlot.Values.ObtainID:SetLabel("Npc ID")
    AceBIS.GearWindow.EditSlot.Values.NpcName.frame:Show()
    AceBIS.GearWindow.EditSlot.Values.DropChance.frame:Show()
    AceBIS.GearWindow.EditSlot.Values.Zone.frame:Show()
    AceBIS.GearWindow.EditSlot:Hide()
end

local function InitFrame(frame, enableResize, title, height, width, layout)
    frame:EnableResize(enableResize)
    frame:SetTitle(title)
    frame:SetHeight(height)
    frame:SetWidth(width)
    frame:SetLayout(layout)
end

local function InitFullUI()
    InitFrame(AceBIS.GearWindow, true, "AceBIS Gears", 520, 360, "AceBISSheet")
    
    AceBIS.GearWindow.frame:SetMinResize(300,520)

    AceBIS.GearWindow.LeftSlots = CreateSimpleGroup("list", 45, 0)
    AceBIS.GearWindow.BottomSlots = CreateSimpleGroup("flow", 195, 45)
    AceBIS.GearWindow.BottomSlots:SetAutoAdjustHeight(false)
    AceBIS.GearWindow.RightSlots = CreateSimpleGroup("list", 45, 0)
    AceBIS.GearWindow.ActionsGroup = CreateSimpleGroup("flow", 0, 46)
    AceBIS.GearWindow.ActionsGroup:SetFullWidth(true)

    AceBIS.SelectedClass = AceBIS.CurrentClass
    AceBIS.GearWindow.ActionsGroup.ClassDropdown = CreateDropdownMenu(" Class", AceBIS.ClassList[AceBIS.SelectedClass], AceBIS.ClassList, 95)
    AceBIS.GearWindow.ActionsGroup.ClassDropdown:SetCallback("OnValueChanged", function(self)
        AceBIS.SelectedClass = self.list[self.value]
        AceBIS.GearWindow:UpdateSetDropdown()
        AceBIS.GearWindow:UpdateSetDisplay()
        AceBIS.GearWindow.SetName:SetDisabled(true)
        AceBIS.GearWindow.TopRightButtonGroup.CreateSet:SetDisabled(true)
        AceBIS.GearWindow.TopRightButtonGroup.RemoveSet:SetDisabled(true)
        SetSelectedSet(AceBIS.SelectedSetName)
    end)

    local firstSetInClass, _ = next(AceBIS.ClassSpecList[AceBIS.CurrentClass])
    if GetSelectedSet() ~= nil then
        firstSetInClass = GetSelectedSet()
    end
    AceBIS.SelectedSetName = firstSetInClass
    AceBIS.GearWindow.ActionsGroup.SetDropdown = CreateDropdownMenu(" Build", firstSetInClass, AceBIS.ClassSpecList[AceBIS.CurrentClass], 160)
    AceBIS.GearWindow.ActionsGroup.SetDropdown:SetCallback("OnValueChanged", function(self)
        AceBIS.SelectedSetName = self.list[self.value]
        AceBIS.GearWindow:UpdateSetDisplay()
        AceBIS.GearWindow.SetName:SetDisabled(true)
        SetSelectedSet(AceBIS.SelectedSetName)
    end)

    AceBIS.SelectedPhase = #PhaseList
    AceBIS.SelectedPhaseName = PhaseList[AceBIS.SelectedPhase]
	AceBIS.GearWindow.ActionsGroup.PhaseDropdown = CreateDropdownMenu(" Phase", AceBIS.SelectedPhase, PhaseList, 60)
    AceBIS.GearWindow.ActionsGroup.PhaseDropdown:SetCallback("OnValueChanged", function(self)
        AceBIS.SelectedPhase = self.value
        AceBIS.SelectedPhaseName = self.list[self.value]
        AceBIS.GearWindow:UpdateSetDisplay()
        AceBIS.GearWindow.SetName:SetDisabled(true)
    end)

    AceBIS.GearWindow.ActionsGroup:AddChild(AceBIS.GearWindow.ActionsGroup.ClassDropdown)
    AceBIS.GearWindow.ActionsGroup:AddChild(AceBIS.GearWindow.ActionsGroup.SetDropdown)
    AceBIS.GearWindow.ActionsGroup:AddChild(AceBIS.GearWindow.ActionsGroup.PhaseDropdown)

    local GearWindowAddChildren = {
        "LeftSlots",
        "BottomSlots",
        "RightSlots",
        "ActionsGroup"
    }

    for key, value in pairs(GearWindowAddChildren) do
        AceBIS.GearWindow:AddChild(AceBIS.GearWindow[value])
    end

    for key, value in pairs(AceBIS.GearWindow.Slots) do
        if (type(key) == "number") then
            AceBIS.GearWindow.Slots[value] = CreateSlotIcon(value, AceBIS.GearWindow.DefaultSlotIcons[value], 40, 40, 45, 45)
            if (key <= 8) then
                AceBIS.GearWindow.LeftSlots:AddChild(AceBIS.GearWindow.Slots[value])
            elseif (key <= 16) then
                AceBIS.GearWindow.RightSlots:AddChild(AceBIS.GearWindow.Slots[value])
            else
                AceBIS.GearWindow.Slots[value].image:SetPoint("TOP", 0, 0)
                AceBIS.GearWindow.BottomSlots:AddChild(AceBIS.GearWindow.Slots[value])
            end
        end
    end
	
    AceBIS.GearWindow.Model = CreateFrame("DressUpModel",nil,AceBIS.GearWindow.frame)    
    AceBIS.GearWindow.Model:SetScript("OnMousewheel", function(self, offset)
        if ((self:GetCameraDistance() - offset/10) > 0.35 and (self:GetCameraDistance() - offset/10) < 4) then
            self:SetCameraDistance(self:GetCameraDistance()-offset/10)
        end
    end)
    AceBIS.GearWindow.Model:SetScript("OnMouseDown", function(self, button)
        self.DragButton = button
        self.IsDragging = true
        self.LastMousePosX, self.LastMousePosY = GetCursorPosition()
    end)
    AceBIS.GearWindow.Model:SetScript("OnMouseUp", function(self, button)
        self.IsDragging = false
    end)
    AceBIS.GearWindow.Model:SetScript("OnUpdate", function(self, timeLapsed)
        if (AceBIS.GearWindow.Model.IsDragging and AceBIS.GearWindow.Model.LastMousePosX ~= nil) then
            if (AceBIS.GearWindow.Model.DragButton == "LeftButton") then
                local currentCursor = GetCursorPosition()
                local currentRotationInDegrees = (180/math.pi)*self:GetFacing()
                local newRotationInDegrees = 0
                newRotationInDegrees = currentRotationInDegrees + (currentCursor - self.LastMousePosX)

                if (newRotationInDegrees > 360) then
                    newRotationInDegrees = newRotationInDegrees - 360
                elseif (newRotationInDegrees < 0) then
                    newRotationInDegrees = 360 - newRotationInDegrees
                end
                local newRotationInRadiens = (math.pi/180)*newRotationInDegrees

                self:SetFacing(newRotationInRadiens)
                self.LastMousePosX, self.LastMousePosY = GetCursorPosition()
            elseif (self.DragButton == "RightButton") then
                local currentCursorX, currentCursorY = GetCursorPosition()
                local currentZ, currentX, currentY = self:GetPosition()
                local newX, newY = 0
                newX = currentX + ((currentCursorX - self.LastMousePosX) / 150 * self:GetCameraDistance())
                newY = currentY + ((currentCursorY - self.LastMousePosY) / 150 * self:GetCameraDistance())
                local maxX = 0.4
                local maxY = 0.6
                if (newX < -maxX * self:GetCameraDistance() or newX > maxX * self:GetCameraDistance()) then
                    if (newX > 0) then
                        newX = maxX * self:GetCameraDistance()
                    else
                        newX = -maxX * self:GetCameraDistance()
                    end
                end

                if (newY < -maxY * self:GetCameraDistance() or newY > maxY * self:GetCameraDistance()) then
                    if (newY > 0) then
                        newY = maxY * self:GetCameraDistance()
                    else
                        newY = -maxY * self:GetCameraDistance()
                    end
                end

                self:SetPosition(0, newX, newY)
                self.LastMousePosX, self.LastMousePosY = GetCursorPosition()
            end
        end
    end)
end

function AceBIS:InitUI()
    AceBIS.GearWindow.DefaultSlotIcons = {
        Helm = "Interface\\PaperDoll\\UI-PaperDoll-Slot-Head",
        Neck = "Interface\\PaperDoll\\UI-PaperDoll-Slot-Neck",
        Shoulder = "Interface\\PaperDoll\\UI-PaperDoll-Slot-Shoulder",
        Back = "Interface\\PaperDoll\\UI-PaperDoll-Slot-Chest",
        Chest = "Interface\\PaperDoll\\UI-PaperDoll-Slot-Chest",
        Shirt = "Interface\\PaperDoll\\UI-PaperDoll-Slot-Shirt",
        Tabard = "Interface\\PaperDoll\\UI-PaperDoll-Slot-Tabard",
        Bracers = "Interface\\PaperDoll\\UI-PaperDoll-Slot-Wrists",
        Hands = "Interface\\PaperDoll\\UI-PaperDoll-Slot-Hands",
        Waist = "Interface\\PaperDoll\\UI-PaperDoll-Slot-Waist",
        Pants = "Interface\\PaperDoll\\UI-PaperDoll-Slot-Legs",
        Boots = "Interface\\PaperDoll\\UI-PaperDoll-Slot-Feet",
        Finger = "Interface\\PaperDoll\\UI-PaperDoll-Slot-Finger",
        RFinger = "Interface\\PaperDoll\\UI-PaperDoll-Slot-Finger",
        Trinket = "Interface\\PaperDoll\\UI-PaperDoll-Slot-Trinket",
        RTrinket = "Interface\\PaperDoll\\UI-PaperDoll-Slot-Trinket",
        MainHand = "Interface\\PaperDoll\\UI-PaperDoll-Slot-MainHand",
        TwoHand = "Interface\\PaperDoll\\UI-PaperDoll-Slot-MainHand",
        OffHand = "Interface\\PaperDoll\\UI-PaperDoll-Slot-SecondaryHand",
        SecondaryHand = "Interface\\PaperDoll\\UI-PaperDoll-Slot-SecondaryHand",
        Ranged = "Interface\\PaperDoll\\UI-PaperDoll-Slot-Relic"
    }
    
    AceBIS.GearWindow.Slots = {
        "Helm",
        "Neck",
        "Shoulder",
        "Back",
        "Chest",
        "Shirt",
        "Tabard",
        "Bracers",
        "Hands",
        "Waist",
        "Pants",
        "Boots",
        "Finger",
        "RFinger",
        "Trinket",
        "RTrinket",
        "TwoHand",
        "MainHand",
        "OffHand",
        "Ranged"
    }

    AceBIS.GearWindow:SetCallback("OnClose", function()
        AceBIS.GearWindow.EditSlot:Hide()
    end)

    AceBIS.GearWindow:SetCallback("OnShow", function()
        AceBIS.GearWindow:UpdateSetDisplay()
    end)

    InitFrame(AceBIS.GearWindow.EditSlot, false, "Edit Slot", 335, 250, "AceBISEditSlot")
    AceBIS.GearWindow.EditSlot:ClearAllPoints()
    AceBIS.GearWindow.EditSlot:SetPoint("TOPLEFT", AceBIS.GearWindow.frame, "TOPRIGHT")
    AceBIS.GearWindow.EditSlot:SetCallback("OnClose", function()
        AceBIS.GearWindow.EditSlot:ResetWindow()
    end)

    InitFrame(AceBIS.GearWindow.ConfirmDelete, false, "Confirm Deletion", 100, 250, "AceBISConfirmDelete")
    AceBIS.GearWindow.ConfirmDelete:ClearAllPoints()
    AceBIS.GearWindow.ConfirmDelete:SetPoint("BOTTOMRIGHT", AceBIS.GearWindow.frame, "TOPRIGHT")

    AceBIS.GearWindow.ConfirmDelete.ValuesOrder = {
        "Text",
        "CancelButton",
        "ConfirmButton"
    }

    AceBIS.GearWindow.ConfirmDelete.Values = {
        Text = CreateLabel("Are you sure you want to delete this set?", true, 1, 1, 1, GameFontHighlight),
        CancelButton = CreateButton("Cancel", false, 100),
        ConfirmButton = CreateButton("Confirm", false, 100)
    }
    AceBIS.GearWindow.ConfirmDelete.Values.CancelButton:SetCallback("OnClick", function()
        AceBIS.GearWindow.ConfirmDelete:Hide()
    end)
    AceBIS.GearWindow.ConfirmDelete.Values.ConfirmButton:SetCallback("OnClick", function()
        AceBIS.ClassSetList["Custom"][AceBIS.SelectedSetName] = nil
        AceBIS.Settings.CustomSets[AceBIS.SelectedSetName] = nil
        AceBIS.GearWindow:UpdateSetDropdown()
        AceBIS.GearWindow:UpdateSetDisplay()
        if (AceBIS.SelectedSetName == nil) then
            AceBIS.GearWindow.SetName:SetDisabled(true)
        end
        AceBIS.GearWindow.ConfirmDelete:Hide()
        AceBIS.GearWindow.EditSlot:ResetWindow()
    end)

    for key, value in pairs(AceBIS.GearWindow.ConfirmDelete.ValuesOrder) do
        AceBIS.GearWindow.ConfirmDelete:AddChild(AceBIS.GearWindow.ConfirmDelete.Values[value])
    end

    AceBIS.GearWindow.EditSlot.SelectedSlot = ""

    AceBIS.GearWindow.EditSlot.ValuesOrder = {
        "ID",
        "ObtainMethod",
        "ObtainID",
        "Zone",
        "NpcName",
        "DropChance",
        "CancelButton",
        "SaveButton"
    }

    AceBIS.GearWindow.EditSlot.Values = {
        ID = CreateEditBox("", "Item ID", false, false, 0, 200),
        ObtainMethod = CreateDropdownMenu("Obtain Method", 1, {"Kill", "Purchase", "Container", "Quest", "Recipe", "Unknown"}, 200),
        ObtainID = CreateEditBox("", "Npc ID", false, false, 0, 200),
        Zone = CreateEditBox("", "Zone", false, false, 0, 200),
        NpcName = CreateEditBox("", "Npc Name", false, false, 0, 200),
        DropChance = CreateEditBox("", "Drop Chance", false, false, 0, 200),
        CancelButton = CreateButton("Cancel", false, 100),
        SaveButton = CreateButton("Save", false, 100)
    }
    local obtainMethods = {
        [1] = "Kill",
        [2] = "Purchase",
        [3] = "Container",
        [4] = "Quest",
        [5] = "Recipe",
        [6] = "Unknown"
    }
    AceBIS.GearWindow.EditSlot.Values.ID:SetCallback("OnTextChanged", function(self, callback, val)
        val = tonumber(val)
        local item = AceBIS.ItemDB:GetItemWithID(val)
        
        local sourceID, sourceName, sourceType, dropChance, zone = "", "", "Kill", "", ""

        if (item ~= nil) then
            sourceID, sourceName, sourceType, dropChance, zone = item.source.ID, item.source.SourceName, item.source.SourceType, item.source.DropChance, item.source.Zone
        end

        AceBIS.GearWindow.EditSlot.Values.ObtainMethod:SetValue(obtainMethods[sourceType])
        ObtainMethodValueChanged(AceBIS.GearWindow.EditSlot.Values.ObtainMethod)

        AceBIS.GearWindow.EditSlot.Values.ObtainID:SetText(sourceID)
        AceBIS.GearWindow.EditSlot.Values.NpcName:SetText(sourceName)
        AceBIS.GearWindow.EditSlot.Values.DropChance:SetText(dropChance)
        AceBIS.GearWindow.EditSlot.Values.Zone:SetText(zone)
    end)

    AceBIS.GearWindow.EditSlot.Values.CancelButton:SetCallback("OnClick", function(self, button)
        AceBIS.GearWindow.EditSlot:ResetWindow()
    end)

    AceBIS.GearWindow.EditSlot.Values.SaveButton:SetCallback("OnClick", function(self, button)
        local values = AceBIS.GearWindow.EditSlot.Values
        local newItem
        local itemID, obtainID, npcName, zone, dropChance
        itemID = tonumber(values.ID:GetText())
        obtainID = tonumber(values.ObtainID:GetText()) or 0
        zone = values.Zone:GetText() or ""
        npcName = values.NpcName:GetText() or ""
        dropChance = values.DropChance:GetText() or "0"
        newItem = AceBIS.Item:New(itemID, "", obtainID, npcName, obtainMethods[AceBIS.GearWindow.EditSlot.Values.ObtainMethod:GetValue()], dropChance, zone)
        AceBIS.Settings.CustomSets[AceBIS.SelectedSetName].Slots[AceBIS.GearWindow.EditSlot.SelectedSlot] = newItem
        AceBIS.GearWindow:UpdateSetDisplay()
        AceBIS.GearWindow.EditSlot:ResetWindow()
    end)

    AceBIS.GearWindow.EditSlot.Values.ObtainMethod:SetCallback("OnValueChanged", ObtainMethodValueChanged)

    for key, value in pairs(AceBIS.GearWindow.EditSlot.ValuesOrder) do
        AceBIS.GearWindow.EditSlot:AddChild(AceBIS.GearWindow.EditSlot.Values[value])
    end

    AceBIS.GearWindow.EditSlot.frame:SetParent(AceBIS.GearWindow.frame)
    
    AceBIS.GearWindow.TopLeftButtonGroup = CreateSimpleGroup("flow", 50, 20)
    AceBIS.GearWindow.TopRightButtonGroup = CreateSimpleGroup("flow", 50, 20)
    
    AceBIS.GearWindow.TopLeftButtonGroup.Reload = CreateIcon(20, 20, 25, 25, "Interface\\AddOns\\AceBIS\\assets\\reload")
    AceBIS.GearWindow.TopLeftButtonGroup.Reload:SetCallback("OnEnter", function()
        GameTooltip:SetOwner(AceBIS.GearWindow.TopLeftButtonGroup.Reload.frame, "ANCHOR_RIGHT")
        GameTooltip:SetText("Reload")
    end)
    AceBIS.GearWindow.TopLeftButtonGroup.Reload:SetCallback("OnLeave", function()
        GameTooltip:SetText("")
    end)
    AceBIS.GearWindow.TopLeftButtonGroup.Reload:SetCallback("OnClick", function()
        AceBIS.GearWindow:UpdateSetDisplay()
    end)

    AceBIS.GearWindow.TopLeftButtonGroup:AddChild(AceBIS.GearWindow.TopLeftButtonGroup.Reload)


    AceBIS.GearWindow.TopRightButtonGroup.CreateSet = CreateIcon(20, 20, 25, 25, "Interface\\AddOns\\AceBIS\\assets\\pen50")
    AceBIS.GearWindow.TopRightButtonGroup.RemoveSet = CreateIcon(20, 20, 25, 25, "Interface\\AddOns\\AceBIS\\assets\\delete")
    

    AceBIS.GearWindow.TopRightButtonGroup:AddChild(AceBIS.GearWindow.TopRightButtonGroup.CreateSet)
    AceBIS.GearWindow.TopRightButtonGroup:AddChild(AceBIS.GearWindow.TopRightButtonGroup.RemoveSet)
    AceBIS.GearWindow.TopRightButtonGroup.CreateSet:SetCallback("OnClick", function()
        local newSetName = "New Set"
        while (AceBIS.ClassSetList["Custom"][newSetName] ~= nil) do
            local n = tonumber(strsub(newSetName, 8))
            if (n == nil) then
                n = 1
            else
                n = n + 1
            end
            newSetName = "New Set" .. tostring(n)
        end

        -- local tempItem = AceBIS.Item:New(0, 0, "", false, false, 0, false, 0, 0, "")
        local tempItem = AceBIS.Item:New(0, "", 0, "", "", "", "")
        AceBIS.ClassSetList["Custom"][newSetName] = newSetName
        AceBIS.Settings.CustomSets[newSetName] = AceBIS.Set:New(newSetName, tempItem, tempItem, tempItem, tempItem, tempItem, tempItem, tempItem, tempItem, tempItem, tempItem, tempItem, tempItem, tempItem, tempItem, tempItem, tempItem, tempItem, tempItem, tempItem)
        AceBIS.GearWindow:UpdateSetDropdown(newSetName)
        AceBIS.GearWindow:UpdateSetDisplay()
        AceBIS.GearWindow.SetName:SetDisabled(false)
    end)
    AceBIS.GearWindow.TopRightButtonGroup.CreateSet:SetCallback("OnEnter", function()
        GameTooltip:SetOwner(AceBIS.GearWindow.TopRightButtonGroup.RemoveSet.frame, "ANCHOR_RIGHT")
        GameTooltip:SetText("Create Custom Set")
    end)
    AceBIS.GearWindow.TopRightButtonGroup.CreateSet:SetCallback("OnLeave", function()
        GameTooltip:SetText("")
    end)

    AceBIS.GearWindow.TopRightButtonGroup.RemoveSet:SetCallback("OnClick", function()
        AceBIS.GearWindow.ConfirmDelete:RemoveSet(AceBIS.SelectedSetName)
    end)
    AceBIS.GearWindow.TopRightButtonGroup.RemoveSet:SetCallback("OnEnter", function()
        GameTooltip:SetOwner(AceBIS.GearWindow.TopRightButtonGroup.RemoveSet.frame, "ANCHOR_RIGHT")
        GameTooltip:SetText("Delete Custom Set")
    end)
    AceBIS.GearWindow.TopRightButtonGroup.RemoveSet:SetCallback("OnLeave", function()
        GameTooltip:SetText("")
    end)

    AceBIS.GearWindow.TopRightButtonGroup.CreateSet:SetDisabled(true)
    AceBIS.GearWindow.TopRightButtonGroup.RemoveSet:SetDisabled(true)

    AceBIS.GearWindow.SetName = CreateEditBox("Set Name", nil, true, false, 25, 160)
    AceBIS.GearWindow.SetName:SetCallback("OnEnterPressed", function(self)
        local value = self:GetText()
        if (value == AceBIS.SelectedSetName) then
            return
        end
        if (strlen(value) < 1) then
            AceBIS:PrintError("Set name cannot be shorter than 1 character.")
            self:SetText(AceBIS.SelectedSetName)
            return
        end
        if (AceBIS.Settings.CustomSets[value] ~= nil and value ~= AceBIS.SelectedSetName) then
            AceBIS:PrintError("A set with the name |cffffff00" .. value .. " |cffffffffalready exists.")
            self:SetText(AceBIS.SelectedSetName)
            return
        end
        AceBIS.ClassSetList["Custom"][value] = value
        AceBIS.ClassSetList["Custom"][AceBIS.SelectedSetName] = nil
        AceBIS.Settings.CustomSets[value] = AceBIS.Settings.CustomSets[AceBIS.SelectedSetName]
        AceBIS.Settings.CustomSets[AceBIS.SelectedSetName] = nil
        AceBIS.GearWindow:UpdateSetDropdown(value)
        AceBIS.GearWindow:UpdateSetDisplay()
    end)

    local GearWindowAddChildren = {
        "TopLeftButtonGroup",
        "TopRightButtonGroup",
        "SetName"
    }

    for key, value in pairs(GearWindowAddChildren) do
        AceBIS.GearWindow:AddChild(AceBIS.GearWindow[value])
    end

    InitFullUI();
end
