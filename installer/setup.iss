; Inno Setup Script for Pi Bitcoin Miner
; Compile with Inno Setup Compiler (https://jrsoftware.org/isinfo.php)

#define MyAppName "Pi Bitcoin Miner"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Pi Bitcoin Miner Team"
#define MyAppURL "https://github.com/yourusername/pi-bitcoin-miner"
#define MyAppExeName "pi-bitcoin-miner.exe"
#define MyAppDescription "Distributed Bitcoin mining using Raspberry Pi 4 and Pico boards"

[Setup]
; NOTE: The value of AppId uniquely identifies this application
AppId={{A8F7B9C2-3D4E-5F6A-7B8C-9D0E1F2A3B4C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=..\LICENSE
InfoBeforeFile=installer_info.txt
OutputDir=output
OutputBaseFilename=PiBitcoinMiner-Setup-{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=lowest
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "..\dist\pi-bitcoin-miner\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\pi-bitcoin-miner\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\config\*"; DestDir: "{app}\config"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\docs\*"; DestDir: "{app}\docs"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\scripts\*.bat"; DestDir: "{app}\scripts"; Flags: ignoreversion
Source: "..\pico_firmware\*"; DestDir: "{app}\pico_firmware"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:ProgramOnTheWeb,{#MyAppName}}"; Filename: "{#MyAppURL}"
Name: "{group}\Configuration"; Filename: "{app}\config\mining_config.json"
Name: "{group}\Documentation"; Filename: "{app}\docs"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  
  // Check if Python is installed (optional warning)
  if not FileExists(ExpandConstant('{pf}\Python38\python.exe')) and
     not FileExists(ExpandConstant('{pf}\Python39\python.exe')) and
     not FileExists(ExpandConstant('{pf}\Python310\python.exe')) and
     not FileExists(ExpandConstant('{pf}\Python311\python.exe')) then
  begin
    if MsgBox('Python does not appear to be installed. While the standalone executable includes most dependencies, you may need Python for advanced features.' + #13#10#13#10 + 'Continue with installation?', 
              mbConfirmation, MB_YESNO) = IDNO then
    begin
      Result := False;
    end;
  end;
end;
