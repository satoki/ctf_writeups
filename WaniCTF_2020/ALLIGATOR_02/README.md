# ALLIGATOR_02:Forensics:102pts
コマンドプロンプトの実行履歴からFLAGを見つけてください。  
(ALLIGATOR_01で配布されているファイルを使ってください)  

# Solution
[ALLIGATOR_01](../ALLIGATOR_01)のファイルを使用する。  
コマンドの実行履歴なので、consolesを見ればよい。  
```bash
$ volatility -f ALLIGATOR.raw --profile=Win7SP1x86_23418 consoles
Volatility Foundation Volatility Framework 2.6
**************************************************
ConsoleProcess: conhost.exe Pid: 336
Console: 0x4f81c0 CommandHistorySize: 50
HistoryBufferCount: 2 HistoryBufferMax: 4
OriginalTitle: C:\Program Files\OpenSSH\bin\cygrunsrv.exe
Title: C:\Program Files\OpenSSH\bin\cygrunsrv.exe
AttachedProcess: sshd.exe Pid: 856 Handle: 0x54
----
CommandHistory: 0xb0960 Application: sshd.exe Flags: Allocated
CommandCount: 0 LastAdded: -1 LastDisplayed: -1
FirstCommand: 0 CommandCountMax: 50
ProcessHandle: 0x54
----
CommandHistory: 0xb07f0 Application: cygrunsrv.exe Flags:
CommandCount: 0 LastAdded: -1 LastDisplayed: -1
FirstCommand: 0 CommandCountMax: 50
ProcessHandle: 0x0
----
Screen 0xc6098 X:80 Y:300
Dump:

**************************************************
ConsoleProcess: conhost.exe Pid: 3736
Console: 0x4f81c0 CommandHistorySize: 50
HistoryBufferCount: 1 HistoryBufferMax: 4
OriginalTitle: %SystemRoot%\system32\cmd.exe
Title: Administrator: C:\Windows\system32\cmd.exe
AttachedProcess: cmd.exe Pid: 3728 Handle: 0x5c
----
CommandHistory: 0x350440 Application: cmd.exe Flags: Allocated, Reset
CommandCount: 1 LastAdded: 0 LastDisplayed: 0
FirstCommand: 0 CommandCountMax: 50
ProcessHandle: 0x5c
Cmd #0 at 0x3546d8: type C:\Users\ALLIGATOR\Desktop\flag.txt
----
Screen 0x3363b8 X:80 Y:300
Dump:
Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Users\ALLIGATOR>type C:\Users\ALLIGATOR\Desktop\flag.txt
FLAG{y0u_4re_c0n50les_master}
C:\Users\ALLIGATOR>
```
flagがあった。  

## FLAG{y0u_4re_c0n50les_master}