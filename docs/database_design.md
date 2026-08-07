# Database Design Plan

This project will use a normalized relational design before any models are created.

## Core tables
- Users
- Roles
- Permissions
- Schools
- Departments
- Authors
- Publishers
- Categories
- Books
- TeacherMaterials
- PastPapers
- Videos
- ResearchRepository
- Borrowing
- Downloads
- Reviews
- Bookmarks
- Notifications
- ActivityLogs
- AuditLogs
- ReadingHistory
- Settings

## Design principles
- Use separate tables for lookup values such as categories, departments, roles, and schools.
- Keep many-to-many relationships in linking tables.
- Store audit and activity history separately from core transactional tables.
- Avoid duplicate user, book, and department records.
- Use foreign keys and indexes for relational integrity.

## Example relationships
- Users -> Roles
- Users -> Departments
- Books -> Authors
- Books -> Publishers
- Books -> Categories
- Borrowing -> Users and Books
- Reviews -> Users and Books
- Notifications -> Users
- ActivityLogs -> Users
- AuditLogs -> Users
