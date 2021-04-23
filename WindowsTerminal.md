# Window Terminal 
## PowerLine Fonts
- MesloLGS NF: https://github.com/romkatv/dotfiles-public/tree/master/.local/share/fonts/NerdFonts

## Download (Last Version)
> Microsoft Store 
```
Window Terminal Preview
```

## Settings
> Start
```
Default Profile | {YourDistro}
```

> Profile </p>
>> All Appearance
```
Color: Solarized Dark
Font: MesloLGS NF
Size: 14
Acryl: On, -transparency: 80
```
>> {YourLinuxDistro}
```
Normal | Command | wsl.exe ~ -u {YourDesto}
```

## {YourLinuxDistro} Backup
> Export
```
wsl -l -v
wsl --shutdown
wsl --export {Distro} {FileName}.tar
```

> Import
```
wsl --import {Distro} {InstallPath} {FileName}.tar
```

## Power Shell Setting
### Oh-My-Posh (V3)
> Run with Adminstrator
```
Install-Module oh-my-posh -Scope CurrentUser
Install-Module -Name PSReadLine -Scope CurrentUser -Force -SkipPublisherCheck
```
> [Option] Update
```
Update-Module -Name oh-my-posh
```

### Check theme
```
Get-PoshThemes
```

### PowerShell Profile Setting
> Execution Policy 
```
Set-ExecutionPolicy Unrestricted
ExecutionPolicy
```

> notepad $PROFILE
```
Import-Module oh-my-posh
Set-PoshPrompt -Theme honukai
```
