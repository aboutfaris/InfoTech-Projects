<p align="center">
<img src="https://i.imgur.com/Clzj7Xs.png" alt="osTicket logo"/>
</p>

<h1>osTicket - Prerequisites and Installation</h1>
Hi there, I am Faris, an IT Professional. Welcome to my first tutorial on setting up osTicket. This tutorial outlines the prerequisites and installation of the open-source help desk ticketing system osTicket.<br />


<h2>What is osTicket?</h2>
-<b>osTicket is a widely-used open source support ticket system. It seamlessly integrates inquiries created via email, phone and web-based forms into a simple easy-to-use multi-user web interface. Manage, organize and archive all your support requests and responses in one place while providing your customers with accountability and responsiveness they deserve.<b>


<h2>Environments and Technologies Used</h2>

- Microsoft Azure (Virtual Machines/Compute)
- Remote Desktop
- Internet Information Services (IIS)
- Heidi SQL

<h2>Operating Systems Used </h2>

- Windows 10</b> (21H2)

<h2>List of Prerequisites</h2>

- Azure Virtual Machine
- osTicket Installation files

<h2>Installation Steps</h2>


![vivaldi_h0YbKLPXqp](https://user-images.githubusercontent.com/109401839/212542603-e23e4232-fa2d-461d-9f9e-9da2ca6f5c73.png)

First, we will create a Resource Group (RG) in Microsoft Azure Cloud Service. Think of the resoruce group as a folder. We will name this resource group as "osTickets". I personally used US East to create my RG. Take note of what region you create your RG and will be creating future instances with. 

![vivaldi_GuBbMJuwmI](https://user-images.githubusercontent.com/109401839/212542800-61c916ab-94a8-4e5f-bc6b-8ccdbe768612.png)

Now, it is time for us to create a virtual machine under the RG. Think of the virtual machine as a computer on the internet or harddrive you can access within your own computer. Pretty cool. As before, I will set my VM region to US East. We will be using Windows 10 with 4vCPUs. We can name this VM "VM-osTicket". 

Create a username and password for your VM. You will be logining in to it like a regular computer ! So, take notes to not forget your login credentials. I set my username to be "labuser" and set my password to be "Password1". In the real world, never do this. However, for this demonstration it is fine. Great.

Now that our machine is ready, we will connect to it using Remote Desktop Connection. before that, let us grab the public IP address of the VM. 

![vivaldi_cILQq943KL](https://user-images.githubusercontent.com/109401839/212543295-70198323-8ddc-4091-ab3d-98b064fc42f3.png)

There, for me the IP address is "20.127.163.23". This is what we will be using to connect to the VM using Remote Desktop Connection. 
![mstsc_4uxVzSdsCJ](https://user-images.githubusercontent.com/109401839/212543384-8d5b81de-1a03-47ad-8ac9-62934412295f.png)
Now, <b>Connect<b>

Now we are connected, let us enable  IIS (Internet Information Services ) ISS is aMicrosoft web server that runs on Windows operating system and is used to exchange static and dynamic web content with internet users. IIS can be used to host, deploy, and manage web applications using technologies such as ASP.NET and PHP.

Start Menu > Windows Feature > Internet Information Services > World Wide Web Services > Application Development Features > CGI

![mstsc_mqJ3Oc0RpT](https://user-images.githubusercontent.com/109401839/212543578-18f011ed-b6e4-4d34-9a41-8093904acb3b.png)

Now we have this installed, lets [download](https://drive.google.com/drive/u/0/folders/1APMfNyfNzcxZC6EzdaNfdZsUwxWYChf6) the installations files needed for osTicket and HeidiSQL.

![ssc](https://user-images.githubusercontent.com/109401839/212543822-5cb9dd90-a14e-4931-96dd-5682964fe37d.jpg)2445aff130bd.jpg)

Great, now head to the installation folders. 
- From the Installation Files, download and install PHP Manager for IIS (PHPManagerForIIS_V1.5.0.msi)
- From the Installation Files, download and install the Rewrite Module (rewrite_amd64_en-US.msi)

Create a directory C:\PHP

![mstsc_LevY5lX29v](https://user-images.githubusercontent.com/109401839/212543951-2d85a000-9828-487c-b661-69e1c5b2f983.png)

- From the Installation Files, download PHP 7.3.8 (php-7.3.8-nts-Win32-VC15-x86.zip) and unzip the contents into C:\PHP
- From the Installation Files, download and install VC_redist.x86.exe.
- From the Installation Files, download and install MySQL 5.5.62 (mysql-5.5.62-win32.msi)

Now, Open IIS as admin by typing it in the start menu. 

