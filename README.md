# Habit Tracker - Full Stack Web Application

## Project Overview
A habit tracking application built with Django REST Framework and React, inspired by Atomic Habits methodology. Users can create habit goals, track daily actions, receive accountability notifications, and build consistent routines.

---

## 📚 Planning Documentation

This repository contains comprehensive planning documentation created during Phase 0:

### Core Documents
1. **[PHASE_0_PLANNING.md](./PHASE_0_PLANNING.md)** - Complete project planning document including:
   - Technology stack decisions
   - Database schema design
   - API endpoint specifications
   - React component architecture
   - SASS styling strategy
   - Development workflow
   - Security considerations

2. **[database_schema_ERD.png](./database_schema_ERD.png)** - Entity Relationship Diagram showing:
   - 7 tables with relationships
   - Field types and constraints
   - Foreign key relationships
   - Many-to-many associations

---

## 🏗️ Architecture Overview

### Backend
- **Framework:** Django 4.x + Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT tokens (stateless)
- **API Style:** RESTful with JSON responses

### Frontend
- **Framework:** React 18.x
- **Styling:** Bootstrap 5.x + Custom SASS
- **State Management:** Context API
- **Routing:** React Router
- **HTTP Client:** Axios with interceptors

### Project Structure
```
project-root/
├── backend/                 # Django REST API
├── frontend/                # React SPA
├── docs/                    # Documentation
│   ├── PHASE_0_PLANNING.md
│   └── database_schema_ERD.png
└── README.md
```

---

## 🎯 Core Features (MVP)

1. **User Management**
   - Registration and login with JWT
   - Profile management
   - User preferences (theme, timezone)

2. **Habit Goals (Routines)**
   - Create routines with purpose/"why"
   - Track multiple habit goals
   - Set target completions
   - Monitor progress

3. **Habit Actions**
   - Daily actions within routines
   - Scheduled times (timezone-aware)
   - Streak tracking (current & longest)
   - Quick completion interface

4. **Completion Tracking**
   - Mark actions complete/incomplete
   - Rate difficulty (1-10 scale)
   - Record feeling (enum: great, good, okay, struggled, forced)
   - Track confidence (1-10 scale)

5. **Accountability Partnerships**
   - 1:1 accountability relationships
   - Request/accept partnership flow
   - Notification when partner misses habits
   - Timezone-aware notifications

6. **Notifications**
   - Real-time notification system
   - Slack-style sidebar panel
   - Notification types: habit missed, partner missed, streak milestones
   - Read/unread status tracking

---

## 📊 Database Schema

### Key Tables
- **Users** - User accounts with profile data
- **Preferences** - User settings (theme, timezone)
- **Routines** - Habit goals with reasoning
- **Actions** - Individual habits within routines
- **habit_completion** - Track each completion with feedback
- **Accountability_Partnership** - Link users as accountability partners
- **Notifications** - User notification queue

See [database_schema_ERD.png](./database_schema_ERD.png) for visual representation.

---

## 🔐 Authentication Flow

1. User logs in → Receives access token (30min) + refresh token (30 days)
2. Access token stored in localStorage
3. All API requests include: `Authorization: Bearer <access_token>`
4. When access token expires → Automatically refresh using refresh token
5. When refresh token expires → Redirect to login

**Security Notes:**
- Passwords hashed with Django's default hasher
- JWT tokens signed and verified
- CSRF-safe (tokens in Authorization header, not cookies)
- CORS configured for frontend domain

---

## 🎨 Styling Approach

### Bootstrap + Custom SASS
- Bootstrap provides grid system and utility classes
- Override Bootstrap variables for brand colors
- Custom SASS for unique components
- Component variant system using BEM-like naming
- Light/dark theme support via CSS variables

### Theme System
```scss
.theme-light { /* Light theme variables */ }
.theme-dark  { /* Dark theme variables */ }
```

Applied dynamically based on user preference from database.

---

## 📱 React Component Strategy

### Page-Level Components
- Landing, Login, Register (public)
- Dashboard, RoutineDetail, Profile (protected)

### Reusable Components
- Layout (Navbar, Sidebar)
- Forms (Button, Input, TextArea, Select)
- Display (RoutineCard, ActionItem, StreakBadge)
- Modals (Generic Modal, Confirm Dialog)

### State Management
- **Context for:** Auth, Preferences, Notifications (global state)
- **Local state for:** Routines, Actions, Completions (fetch per-page)

---

## 🚀 Development Phases

### Phase 0: Planning ✅
- Database schema design
- API endpoint planning
- Component architecture
- Technology decisions

### Phase 1: Backend Setup (Next)
- Django project initialization
- PostgreSQL configuration
- Model creation & migrations
- JWT authentication setup
- API endpoints with DRF ViewSets

### Phase 2: Frontend Setup
- React + Vite initialization
- Context providers
- Axios configuration
- Authentication flow

### Phase 3: Core Features
- Routines CRUD
- Actions & completions
- Notifications system
- Accountability partnerships

### Phase 4: Polish & Deploy
- Error handling
- Loading states
- Responsive design
- Performance optimization
- Deployment to Render

---

## 🎓 Learning Objectives

This project demonstrates:
- ✅ Django REST Framework proficiency
- ✅ PostgreSQL database design
- ✅ JWT authentication implementation
- ✅ React hooks and Context API
- ✅ SASS preprocessing
- ✅ RESTful API design
- ✅ Full-stack integration
- ✅ Modern deployment practices

---

## 📝 Assignment Alignment

**Course Requirement:** Building a Web Application with Django and a Database (12% of grade)

**Rubric Criteria Met:**
1. **Django Concepts** - Models, ViewSets, Serializers, Authentication
2. **Database Integration** - PostgreSQL with normalized schema
3. **Authentication & Authorization** - JWT with role-based access
4. **Clean Code Structure** - Component architecture, SASS organization
5. **Hosted Application** - Fully functional deployment on Render

**Enhancements Beyond Requirements:**
- Modern React SPA (vs traditional templates)
- JWT authentication (vs session-based)
- Timezone-aware scheduling
- Psychological tracking metrics
- Real-time notification system

---

## 🛠️ Prerequisites

### Development Environment
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Git

### Recommended Tools
- VS Code with extensions:
  - Python
  - Pylance
  - ES7+ React snippets
  - SASS
  - Thunder Client (API testing)

---

## 📦 Dependencies

### Backend (requirements.txt)
```
Django>=4.2
djangorestframework>=3.14
djangorestframework-simplejwt>=5.3
psycopg2-binary>=2.9
django-cors-headers>=4.3
python-decouple>=3.8
```

### Frontend (package.json)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.0",
    "bootstrap": "^5.3.0",
    "sass": "^1.69.0"
  }
}
```

---

## 🎯 Next Steps

Ready to begin Phase 1! Choose your implementation approach:

**Option A:** Backend-first (build API, test with Postman, then build frontend)
**Option B:** Frontend-first (build UI with mock data, then connect to API)
**Option C:** Vertical slice (build features end-to-end, one at a time) ⭐ **Recommended**

---

## 📖 Additional Resources

- [Django REST Framework Docs](https://www.django-rest-framework.org/)
- [React Documentation](https://react.dev/)
- [JWT.io](https://jwt.io/) - JWT debugger
- [Bootstrap Docs](https://getbootstrap.com/)
- [SASS Documentation](https://sass-lang.com/)

---

## 👨‍💻 Development Principles

Throughout this project, we follow:
- **Incremental development** - Build and test in small pieces
- **Best practices** - Clean code, documentation, version control
- **Problem-solving** - Debug independently before asking for help
- **Iterative improvement** - MVP first, enhancements later

---