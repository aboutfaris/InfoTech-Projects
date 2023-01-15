<p align="center">
<img src="https://i.imgur.com/Clzj7Xs.png" alt="osTicket logo"/>
</p>

<h1>osTicket - Post-Install Configuration</h1>
This tutorial outlines the post-install configuration of the open-source help desk ticketing system osTicket.<br />


<h2>Environments and Technologies Used</h2>

- Microsoft Azure (Virtual Machines/Compute)
- Remote Desktop
- Internet Information Services (IIS)

<h2>Operating Systems Used </h2>

- Windows 10</b> (21H2)

<h2>Post-Install Configuration Objectives</h2>

- Configure Roles
- Configure Departments
- Configure Teams
- Configure Agents
- Configure SLAs
- Configure Help Topics

- <h2>Configuration of Roles</h2>
1. Admin Panel -> Agents -> Roles
2. Supreme Admin
[1](https://i.imgur.com/MTE2IPV.jpeg)

Create the role Supreme Admin, and give it the accessbility that a supreme admin should have. Complete Control.
[2](https://i.imgur.com/uwz8rea.png)

- <h2>Configure Departments<h2>
1. Admin Panel -> Agents -> Departments
2. System Administrators

- <h2>Configure Teams<h2>
1. Admin Panel -> Agents -> Teams
    -A. Level I Support
    -B. Level II Support

- <h2>Allow anyone to create tickets<h2>
    1. Admin Panel -> Settings -> User Settings
    2. Registration Required: Require registration and login to create tickets

**Feel free to use any name to your liking !**

- <h2>Configure [Agents(workers)](https://docs.osticket.com/en/latest/Admin/Agents/Agents.html)<h2>
    1. Admin Panel -> Agents -> Add New
    A. Layla
    B. Jamari

<h2>Configure [Users (customers)](https://docs.osticket.com/en/latest/Agent/Users/User%20Directory.html)<h2>
    - 1. Agent Panel -> Users -> Add New
  A. Dimitri
  B. Byleth
- <h2>Configure [SLA](https://docs.osticket.com/en/latest/Admin/Manage/SLA%20Plans.html)<h2>
    1. Admin Panel -> Manage -> SLA
    A. Sev-A (1 hour, 24/7)
    B. Sev-B (4 hours, 24/7)
    C. Sev-C (8 hours, business hours)

- <h2>Configure Help Topics<h2>
    1. Admin Panel -> Manage -> Help Topics
    A. Business Critical Outage
    B. Personal Computer Issues
    C. Equipment Request
    D. Password Reset

On the [next tutorial](https://github.com/fnabeel/osTicket---Ticket-Lifecycle-Intake-Through-Resolution), we will create Tickets and showcase the Ticket Lifecycle.
