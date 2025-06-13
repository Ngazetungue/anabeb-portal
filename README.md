# **Anabeb Conservancy - Management Portal**  

For testing purpose: username:admin and password:admin12345
The system divided into two interfave admin and staff, but for testing purpose i share login details of admin only. By the way you can create/register staff member through admin.

## **Project Overview**  
**Anabeb Conservancy Portal** is a secure personnel management system built with **Django**, designed to empower:  
- **Administrators** to manage all users (staff/guards/members)  
- **Staff** to generate and download guard payslips (PDF)  
- **Role-based access control** with admin-only user creation  

The platform combines **Django's security** with **Tailwind CSS's responsive interface** and **ReportLab** for PDF generation.  

## **Key Features**  

### **🔐 Core Functionality**  
- **Role-based authentication system** (admin/staff login)  
- **Personnel management** (members, guards, staff)  
- **PDF payslip generation** with automatic calculations  
- **Admin dashboard** with full system control  
- **Staff dashboard** with limited system access  
- **User creation/management** (staff, members & guards)  

### **User Experience**  
- **Responsive Tailwind design** works on all devices  
- **Intuitive payroll interface** for staff  
- **Quick-search** for personnel records  

## **Technology Stack**  

### **Backend**  
| Technology | Description | Why It Was Chosen |
|------------|-------------|-------------------|
| **<img src="https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white" alt="Django" />** | High-level Python framework | Provides **built-in admin panel**, **secure authentication**, and **rapid development** for conservancy management needs |
| **<img src="https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white" alt="PostgreSQL" />** | Relational database | Handles **personnel records** efficiently with **ACID compliance** and **Django native support** |

### **Frontend**  
| Technology | Description | Why It Was Chosen |
|------------|-------------|-------------------|
| **<img src="https://img.shields.io/badge/Tailwind_CSS-06B6D4?logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />** | Utility-first CSS framework | Enables **rapid UI development** with responsive design and customization |
| **<img src="https://img.shields.io/badge/HTMX-1E4A75?logo=html5&logoColor=white" alt="HTMX" />** | Dynamic HTML | Adds **interactivity** to tables/forms without JavaScript complexity |

### **Services**  
| Technology | Description | Why It Was Chosen |
|------------|-------------|-------------------|
| **<img src="https://img.shields.io/badge/ReportLab-FF6F00?logo=python&logoColor=white" alt="ReportLab" />** | PDF generator | Creates **professional payslips** with precise layout control |
| **<img src="https://img.shields.io/badge/Django_Allauth-44B78B?logo=django&logoColor=white" alt="Django Allauth" />** | Authentication | Provides **secure login** with email verification capabilities |

## **Project Screenshots**  

### **1. Login Page**  
<img width="1419" alt="Login Page" src="https://github.com/user-attachments/assets/cbdded4c-17bd-4d93-b9ef-683aa95d20a6" />  
*Secure role-based authentication gateway*  

### **2. Admin Dashboard**  
<img width="1437" alt="Admin Dashboard" src="https://github.com/user-attachments/assets/b4947763-42f9-469f-8a3e-1046ab316797" />  
- **User management table**  
- **System configuration panel**  
- **Audit log access**  


### **3. Member Management**  
<img width="1437" alt="Member Management" src="https://github.com/user-attachments/assets/8194ef9a-15da-496d-84fa-e53c04b3008c" />  
- Add/edit conservancy members  
- Export member data

### **4. Staff Dashboard**   
- **Guard timesheet entry**  
- **Payslip generation button**  
- **Personnel search**  

### **5. Payslip Generation Workflow**  
<img width="1437" alt="Payslip Interface" src="https://github.com/user-attachments/assets/7cc28cd9-bc74-458c-9663-61b0b913b145" />  
1. Navigate to **Guards** section  
2. Enter hours worked  
3. Click **Download Payslip**  
4. System generates PDF via ReportLab  

**Sample Payslip Output:**  
<img width="1026" alt="Generated Payslip" src="https://github.com/user-attachments/assets/cb5c0aef-0682-43a4-9037-6139ca919397" />  
