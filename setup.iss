; This file is a script for generating the setup of the app using Inno Setup (http://www.jrsoftware.org/isinfo.php)
#define MyAppName "Start Menu Helper"
#define MyAppVersion "1.2.2"
#define MyAppPublisher "Jarik Marwede"
#define MyAppURL "https://github.com/jarikmarwede/Start-Menu-Helper"
#define MyAppExeName "Start Menu Helper.exe"
#define MySetupName "Start_Menu_Helper_Setup"
#define MyAppLicenseName "LICENSE"
#define MyAppIconName "icon.ico"
#define MyReadmeName "README.md"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{D26A734D-25ED-4801-8E7D-A7A28A307C04}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile={#MyAppLicenseName}
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputDir=setup
OutputBaseFilename={#MySetupName}
SetupIconFile={#MyAppIconName}
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\{#MyAppName}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
Source: "{#MyReadmeName}"; DestDir: "{app}"; Flags: ignoreversion isreadme
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
