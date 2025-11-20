# Phase 0: Project Planning

## Project Overview

**Project Name:** Habit Tracker  
**Type:** Full-stack web application  
**Purpose:** Help users develop consistent habits through accountability and tracking  
**Inspired by:** Atomic Habits methodology

### Technology Stack

**Backend:**
- Django 4.x
- Django REST Framework (DRF)
- PostgreSQL 14+
- djangorestframework-simplejwt (JWT authentication)
- django-cors-headers (CORS handling)
- psycopg2 (PostgreSQL adapter)

**Frontend:**
- React 18.x
- React Router (navigation)
- Axios (API calls)
- SASS/SCSS (styling)
- Bootstrap 5.x (base styling + utilities)

**Development Tools:**
- Vite (React build tool)
- Git (version control)

**Deployment:**
- Render (or similar hosting provider)

---

## Project Philosophy & Scope

### Core Concept
Building a habit tracker based on Atomic Habits principles where:
- Users create "Habit Goals" (Routines) with a clear "why" (reason)
- Each routine contains specific "Habit Actions" (daily tasks)
- Users track completions with psychological feedback (difficulty, feeling, confidence)
- Accountability partners receive notifications when habits are missed
- After consistent completion, users are prompted to evaluate if the habit is "clockwork" and can be archived

### MVP Scope (Phase 1)
- User authentication and profile management
- Habit goal (routine) creation and management
- Daily habit action tracking
- Completion tracking with feedback metrics
- 1:1 accountability partnership
- Real-time notifications for missed habits
- Timezone-aware scheduling
- Light/dark theme support

### Phase 2 Features (Deferred)
- Grouped notifications (many-to-many relationship)
- Background job scheduling for delayed notifications
- Direct messaging between users
- Advanced analytics and visualizations
- Habit streaks leaderboard
- Multiple accountability partners
- Habit templates library

---

## Architecture Decisions

### API-First Architecture
- **Backend:** Django REST Framework serves as a pure REST API
- **Frontend:** React SPA consumes the API
- **Communication:** JSON over HTTP
- **Authentication:** JWT tokens (stateless)
- **Separation:** Clear separation of concerns between frontend and backend

### Monorepo Structure
```
project-root/
├── backend/                 # Django REST API
│   ├── manage.py
│   ├── config/             # Project settings
│   ├── apps/
│   │   ├── users/
│   │   ├── habits/
│   │   └── notifications/
│   ├── requirements.txt
│   └── .env
│
├── frontend/               # React App
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/      # API calls
│   │   ├── styles/        # SASS files
│   │   ├── context/       # React Context
│   │   ├── utils/
│   │   └── App.jsx
│   ├── package.json
│   └── .env
│
├── docs/
│   ├── PHASE_0_PLANNING.md
│   └── database_schema.png
├── README.md
└── .gitignore
```

---

## Database Schema

### Terminology Mapping
| Our Term | Assignment Term | Description |
|----------|----------------|-------------|
| User | User | Main user profile |
| Routine | Project | Habit goal container |
| Action | Task | Individual daily habit |
| Accountability Partner | Stakeholder | User who receives notifications |

### Tables & Relationships

#### 1. Users
**Built-in Django User Model + Custom Extensions**

| Field | Type | Notes |
|-------|------|-------|
| id | bigint | Primary key (auto) |
| first_name | varchar | |
| last_name | varchar | |
| email | varchar | Unique, required |
| password | varchar | Hashed (Django handles this) |
| bio | text | Optional |
| date_of_birth | date | Optional |
| profile_picture | varchar | S3 URL for avatar |
| created_at | timestamp | Auto |
| updated_at | timestamp | Auto |

**Relationships:**
- One-to-One with Preferences
- One-to-Many with Routines (owner)
- One-to-Many with Notifications (recipient)
- Many-to-Many with Users via Accountability_Partnership

---

#### 2. Preferences
**User Settings & Customization**

| Field | Type | Notes |
|-------|------|-------|
| id | bigint | Primary key |
| user_id | bigint | FK to Users (One-to-One) |
| theme_mode | enum | 'light', 'dark' |
| color_scheme_name | varchar | For custom themes |
| timezone | varchar | e.g., 'America/New_York', 'Europe/London' |
| notification_window_start | time | Default: 08:00:00 (Phase 2) |
| notification_window_end | time | Default: 22:00:00 (Phase 2) |

**Relationships:**
- One-to-One with Users

---

#### 3. Routines
**Habit Goals (The "why" behind habit formation)**

| Field | Type | Notes |
|-------|------|-------|
| id | bigint | Primary key |
| name | varchar | e.g., "Morning Routine" |
| reason | text | The "why" - purpose/motivation |
| status | enum | 'active', 'paused', 'completed', 'archived' |
| owner | bigint | FK to Users |
| start_date | date | When user started this routine |
| end_date | date | Nullable - for completed routines |
| target_completions | int | Goal number of completions before "clockwork" check |
| created_at | timestamp | Auto |
| updated_at | timestamp | Auto |

**Relationships:**
- Many-to-One with Users (owner)
- One-to-Many with Actions

---

#### 4. Actions
**Individual Habit Actions within a Routine**

| Field | Type | Notes |
|-------|------|-------|
| id | bigint | Primary key |
| name | varchar | e.g., "Meditate 5 minutes" |
| routine_id | bigint | FK to Routines |
| frequency | enum | 'daily' (MVP - all daily) |
| start_time | time | Interpreted in user's timezone from Preferences |
| current_streak | int | Consecutive days completed |
| longest_streak | int | Personal best streak |
| created_at | timestamp | Auto |

**Relationships:**
- Many-to-One with Routines
- One-to-Many with habit_completion
- One-to-Many with Notifications (trigger_action)

**Timezone Handling:**
- `start_time` stored as simple time (e.g., 07:00:00)
- Interpreted in context of user's timezone from Preferences table
- Example: 07:00:00 for user in 'America/New_York' = 7 AM EST/EDT

---

#### 5. habit_completion
**Tracking each completion with psychological feedback**

| Field | Type | Notes |
|-------|------|-------|
| id | bigint | Primary key |
| action_id | bigint | FK to Actions |
| completion_date | date | **CRITICAL** - when completed |
| difficulty | smallint | Scale 1-10: How hard was it? |
| feeling | enum | 'great', 'good', 'okay', 'struggled', 'forced' |
| confidence | smallint | Scale 1-10: Confidence in continuing |

**Relationships:**
- Many-to-One with Actions

**Why separate completion table?**
- Enables historical tracking (analytics)
- Allows streak calculation over time
- Captures psychological patterns
- Better normalization

**Streak Calculation:**
- Query completions by action_id, ordered by completion_date
- Check for consecutive days
- Update current_streak on Actions table

---

#### 6. Accountability_Partnership
**1:1 Accountability relationship between users**

| Field | Type | Notes |
|-------|------|-------|
| id | bigint | Primary key |
| user_id | bigint | FK to Users (person being held accountable) |
| partner_id | bigint | FK to Users (accountability partner) |
| status | enum | 'pending', 'accepted', 'rejected' |
| created_at | timestamp | When partnership was requested |
| notification_id | bigint | FK to Notifications (for linking) |

**Relationships:**
- Many-to-One with Users (user_id)
- Many-to-One with Users (partner_id)
- Many-to-One with Notifications

**Business Rules:**
- One user can have ONE accountability partner at a time (1:1)
- Partner must accept request before activation
- Partner receives notifications for ALL missed habits
- Partnership applies to user-level, not routine-level

---

#### 7. Notifications
**User notification system**

| Field | Type | Notes |
|-------|------|-------|
| id | bigint | Primary key |
| recipient | bigint | FK to Users (who receives notification) |
| message | text | Notification content |
| type | enum | 'habit_missed', 'partner_habit_missed', 'partnership_request', 'streak_milestone' |
| read_status | boolean | Default: false |
| created_at | timestamp | Auto |
| trigger_action | bigint | FK to Actions (nullable - which action caused this) |

**Relationships:**
- Many-to-One with Users (recipient)
- Many-to-One with Actions (trigger_action)

**Notification Types:**
- `habit_missed`: User missed their own habit
- `partner_habit_missed`: Partner missed a habit
- `partnership_request`: Someone requested you as accountability partner
- `streak_milestone`: Achieved streak milestone (7, 14, 30, 60, 90 days)

**Phase 2 Enhancement:**
- Bridge table for grouped notifications (one notification → many actions)
- `scheduled_send_time` and `sent_at` fields for background job queuing

---

### Timezone Strategy

#### Problem Statement
Users in different timezones need notifications at appropriate times:
- User A (NYC, UTC-5): Misses 7 AM meditation
- User B (London, UTC+0): Accountability partner - when to notify?

#### Solution (Phase 1)
1. **Store timezone in Preferences table:** Each user has their own timezone
2. **Action times are local:** `start_time` interpreted in user's timezone
3. **Notification window checking:**
   - When action is missed, check recipient's current local time
   - If within notification window (e.g., 9 AM - 9 PM), send immediately
   - If outside window, notification still created (Phase 2: queue for later)

#### Phase 2 Enhancement
- Add `notification_window_start` and `notification_window_end` to Preferences
- Background job (Celery) checks for pending notifications
- Send notifications when recipient enters their notification window

---

## API Endpoint Design

### Authentication Strategy

**JWT Token Authentication:**
- Access token lifetime: 30 minutes
- Refresh token lifetime: 30 days
- Tokens stored in localStorage (client-side)
- Access token included in `Authorization: Bearer <token>` header
- Automatic token refresh via Axios interceptor

**Token Flow:**
1. User logs in → Receives access + refresh tokens
2. Every API request includes access token in header
3. When access token expires (401) → Use refresh token to get new access token
4. When refresh token expires → User must log in again

**Why JWT vs Session Cookies:**
- Stateless (no server-side session storage)
- Works across multiple services/domains
- No CSRF vulnerability when using Authorization header
- Better for REST API architecture

---

### API Endpoints

**Base URL:** `/api/v1/`

#### Authentication Endpoints

```
POST   /api/v1/auth/register/
POST   /api/v1/auth/login/
POST   /api/v1/auth/refresh/
POST   /api/v1/auth/logout/          (Optional - token blacklisting)
```

**Register:**
```json
// Request
{
  "email": "user@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}

// Response (201 Created)
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "access": "eyJhbGc...",
  "refresh": "eyJhbGc..."
}
```

**Login:**
```json
// Request
{
  "email": "user@example.com",
  "password": "securepassword123"
}

// Response (200 OK)
{
  "access": "eyJhbGc...",
  "refresh": "eyJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

**Refresh Token:**
```json
// Request
{
  "refresh": "eyJhbGc..."
}

// Response (200 OK)
{
  "access": "eyJhbGc..."  // New access token
}
```

---

#### User & Preferences Endpoints

```
GET    /api/v1/users/me/
PATCH  /api/v1/users/me/
GET    /api/v1/users/me/preferences/
PATCH  /api/v1/users/me/preferences/
```

**Get Current User:**
```json
// Response (200 OK)
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Habit enthusiast",
  "date_of_birth": "1990-05-15",
  "profile_picture": "https://s3.amazonaws.com/..."
}
```

**Update Profile:**
```json
// Request (PATCH)
{
  "first_name": "Johnny",
  "bio": "Building better habits every day"
}

// Response (200 OK)
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "Johnny",
  "last_name": "Doe",
  "bio": "Building better habits every day",
  // ... rest of fields
}
```

---

#### Routines (Habit Goals) Endpoints

```
GET    /api/v1/habits/routines/
POST   /api/v1/habits/routines/
GET    /api/v1/habits/routines/{id}/
PATCH  /api/v1/habits/routines/{id}/
DELETE /api/v1/habits/routines/{id}/
```

**List Routines:**
```json
// Response (200 OK)
[
  {
    "id": 1,
    "name": "Morning Routine",
    "reason": "Start my day with energy and focus",
    "status": "active",
    "start_date": "2025-01-01",
    "end_date": null,
    "target_completions": 30,
    "created_at": "2025-01-01T08:00:00Z",
    "updated_at": "2025-01-01T08:00:00Z",
    "actions_count": 3
  },
  // ... more routines
]
```

**Create Routine:**
```json
// Request (POST)
{
  "name": "Evening Wind-Down",
  "reason": "Sleep better and reduce stress",
  "target_completions": 21
}

// Response (201 Created)
{
  "id": 2,
  "name": "Evening Wind-Down",
  "reason": "Sleep better and reduce stress",
  "status": "active",
  "start_date": "2025-01-15",
  "end_date": null,
  "target_completions": 21,
  "created_at": "2025-01-15T20:00:00Z",
  "updated_at": "2025-01-15T20:00:00Z"
}
```

---

#### Actions (Habit Actions) Endpoints

```
GET    /api/v1/habits/actions/?routine={id}
POST   /api/v1/habits/routines/{id}/actions/
GET    /api/v1/habits/actions/{id}/
PATCH  /api/v1/habits/actions/{id}/
DELETE /api/v1/habits/actions/{id}/
POST   /api/v1/habits/actions/{id}/complete/    (Convenience endpoint)
```

**List Actions (filtered by routine):**
```json
// GET /api/v1/habits/actions/?routine=1
// Response (200 OK)
[
  {
    "id": 1,
    "name": "Meditate 5 minutes",
    "routine": 1,
    "frequency": "daily",
    "start_time": "07:00:00",
    "current_streak": 12,
    "longest_streak": 15,
    "created_at": "2025-01-01T08:00:00Z"
  },
  // ... more actions
]
```

**Create Action:**
```json
// POST /api/v1/habits/routines/1/actions/
// Request
{
  "name": "Read 10 pages",
  "start_time": "07:30:00"
}

// Response (201 Created)
{
  "id": 4,
  "name": "Read 10 pages",
  "routine": 1,
  "frequency": "daily",
  "start_time": "07:30:00",
  "current_streak": 0,
  "longest_streak": 0,
  "created_at": "2025-01-15T20:00:00Z"
}
```

**Complete Action (Convenience Endpoint):**
```json
// POST /api/v1/habits/actions/1/complete/
// Request
{
  "difficulty": 3,
  "feeling": "good",
  "confidence": 8
}

// Response (201 Created)
{
  "id": 45,
  "action": 1,
  "completion_date": "2025-01-15",
  "difficulty": 3,
  "feeling": "good",
  "confidence": 8
}
```

---

#### Completions Endpoints

```
GET    /api/v1/habits/completions/?action={id}
GET    /api/v1/habits/completions/{id}/
PATCH  /api/v1/habits/completions/{id}/
DELETE /api/v1/habits/completions/{id}/
```

**List Completions:**
```json
// GET /api/v1/habits/completions/?action=1
// Response (200 OK)
[
  {
    "id": 45,
    "action": 1,
    "completion_date": "2025-01-15",
    "difficulty": 3,
    "feeling": "good",
    "confidence": 8
  },
  // ... more completions (ordered by date DESC)
]
```

---

#### Accountability Partnership Endpoints

```
GET    /api/v1/habits/partnerships/
POST   /api/v1/habits/partnerships/
PATCH  /api/v1/habits/partnerships/{id}/
DELETE /api/v1/habits/partnerships/{id}/
```

**Request Partnership:**
```json
// Request (POST)
{
  "partner_email": "partner@example.com"
}

// Response (201 Created)
{
  "id": 1,
  "user": 1,
  "partner": 2,
  "status": "pending",
  "created_at": "2025-01-15T20:00:00Z"
}
```

**Accept/Reject Partnership:**
```json
// Request (PATCH /api/v1/habits/partnerships/1/)
{
  "status": "accepted"  // or "rejected"
}

// Response (200 OK)
{
  "id": 1,
  "user": 2,
  "partner": 1,
  "status": "accepted",
  "created_at": "2025-01-15T20:00:00Z"
}
```

---

#### Notifications Endpoints

```
GET    /api/v1/notifications/
PATCH  /api/v1/notifications/{id}/
DELETE /api/v1/notifications/{id}/
```

**List Notifications:**
```json
// Response (200 OK)
{
  "unread_count": 3,
  "notifications": [
    {
      "id": 10,
      "message": "You missed 'Meditate 5 minutes' today",
      "type": "habit_missed",
      "read_status": false,
      "created_at": "2025-01-15T19:00:00Z",
      "trigger_action": {
        "id": 1,
        "name": "Meditate 5 minutes"
      }
    },
    // ... more notifications
  ]
}
```

**Mark as Read:**
```json
// Request (PATCH /api/v1/notifications/10/)
{
  "read_status": true
}

// Response (200 OK)
{
  "id": 10,
  "message": "You missed 'Meditate 5 minutes' today",
  "type": "habit_missed",
  "read_status": true,
  "created_at": "2025-01-15T19:00:00Z"
}
```

---

### REST Conventions Used

**HTTP Methods:**
- `GET` - Retrieve resource(s)
- `POST` - Create new resource
- `PATCH` - Partial update (preferred over PUT)
- `DELETE` - Remove resource

**URL Patterns:**
- **Nested for creation context:** `POST /routines/{id}/actions/`
- **Flat for querying:** `GET /actions/?routine={id}`
- **Specific resource:** `GET /actions/{id}/`

**Response Codes:**
- `200 OK` - Successful GET, PATCH, DELETE
- `201 Created` - Successful POST
- `400 Bad Request` - Validation errors
- `401 Unauthorized` - Missing/invalid token
- `403 Forbidden` - Authenticated but not authorized
- `404 Not Found` - Resource doesn't exist
- `500 Internal Server Error` - Server error

---

## React Frontend Architecture

### Page Structure & Routing

#### Public Routes (No Authentication Required)
```
/                    → Landing page (hero + CTA)
/login              → Login page
/register           → Registration page
```

#### Protected Routes (Authentication Required)
```
/dashboard          → Main dashboard (list of routines)
/routines/:id       → Routine detail page (with actions)
/profile            → User profile & settings
```

**Notifications:** Sidebar panel accessible from any authenticated page (Slack-style)

---

### Layout System

**Two distinct layouts:**

**1. AuthLayout** (for public pages)
```jsx
<AuthLayout>
  <main>{children}</main>
  <footer>© 2025 Habit Tracker</footer>
</AuthLayout>
```

**2. AppLayout** (for authenticated pages)
```jsx
<AppLayout>
  <Navbar />
  <NotificationsSidebar />
  <main>{children}</main>
</AppLayout>
```

---

### Component Architecture

#### Directory Structure
```
src/
├── components/
│   ├── layout/
│   │   ├── Navbar.jsx
│   │   ├── NotificationsSidebar.jsx
│   │   ├── AuthLayout.jsx
│   │   └── AppLayout.jsx
│   ├── routines/
│   │   ├── RoutineCard.jsx
│   │   ├── CreateRoutineModal.jsx
│   │   └── RoutineForm.jsx
│   ├── actions/
│   │   ├── ActionItem.jsx
│   │   ├── CreateActionModal.jsx
│   │   ├── CompletionForm.jsx
│   │   └── ActionForm.jsx
│   ├── notifications/
│   │   └── NotificationItem.jsx
│   ├── common/
│   │   ├── Button.jsx
│   │   ├── Input.jsx
│   │   ├── TextArea.jsx
│   │   ├── Select.jsx
│   │   ├── Modal.jsx
│   │   ├── LoadingSpinner.jsx
│   │   ├── StreakBadge.jsx
│   │   ├── ProgressBar.jsx
│   │   └── EmptyState.jsx
│   └── forms/
│       └── Form.jsx
├── pages/
│   ├── Landing.jsx
│   ├── Login.jsx
│   ├── Register.jsx
│   ├── Dashboard.jsx
│   ├── RoutineDetail.jsx
│   └── Profile.jsx
├── context/
│   ├── AuthContext.jsx
│   ├── PreferencesContext.jsx
│   └── NotificationsContext.jsx
├── services/
│   ├── api.js               # Axios instance with interceptors
│   ├── authService.js       # Auth API calls
│   ├── routinesService.js   # Routines API calls
│   ├── actionsService.js    # Actions API calls
│   └── notificationsService.js
├── styles/
│   ├── main.scss            # Main entry point
│   ├── _variables.scss      # SASS variables
│   ├── _mixins.scss         # SASS mixins
│   ├── _themes.scss         # Light/dark themes
│   ├── components/          # Component-specific styles
│   └── pages/               # Page-specific styles
├── utils/
│   ├── dateHelpers.js       # Timezone conversions
│   └── streakCalculator.js  # Streak calculation logic
├── App.jsx
└── main.jsx
```

---

### Context Providers

#### 1. AuthContext
**Purpose:** Manage authentication state globally

```javascript
{
  user: {
    id: number,
    email: string,
    first_name: string,
    last_name: string,
    bio: string,
    profile_picture: string
  },
  isAuthenticated: boolean,
  loading: boolean,
  login: (credentials) => Promise,
  logout: () => void,
  register: (userData) => Promise,
  updateProfile: (updates) => Promise
}
```

**Usage:**
```jsx
const { user, isAuthenticated, login } = useAuth();
```

---

#### 2. PreferencesContext
**Purpose:** Manage user preferences (theme, timezone)

```javascript
{
  preferences: {
    theme_mode: 'light' | 'dark',
    color_scheme_name: string,
    timezone: string
  },
  loading: boolean,
  updatePreferences: (updates) => Promise
}
```

**Usage:**
```jsx
const { preferences, updatePreferences } = usePreferences();
```

**Theme Application:**
```jsx
// App.jsx
function App() {
  const { preferences } = usePreferences();
  
  return (
    <div className={`theme-${preferences.theme_mode}`}>
      <Routes>...</Routes>
    </div>
  );
}
```

---

#### 3. NotificationsContext
**Purpose:** Manage notifications state and sidebar

```javascript
{
  notifications: Array,
  unreadCount: number,
  loading: boolean,
  sidebarOpen: boolean,
  toggleSidebar: () => void,
  markAsRead: (id) => Promise,
  deleteNotification: (id) => Promise,
  fetchNotifications: () => Promise
}
```

**Usage:**
```jsx
const { 
  notifications, 
  unreadCount, 
  sidebarOpen, 
  toggleSidebar 
} = useNotifications();
```

---

### State Management Strategy

**Use Context for:**
- ✅ Authentication state (needed everywhere)
- ✅ User preferences (theme applied globally)
- ✅ Notifications (sidebar accessible from anywhere)

**Don't use Context for:**
- ❌ Routines (page-specific, fetch per-page)
- ❌ Actions (fetch when needed)
- ❌ Completions (fetch when needed)

**Fetch-per-page pattern:**
```jsx
function Dashboard() {
  const [routines, setRoutines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refetchTrigger, setRefetchTrigger] = useState(0);

  useEffect(() => {
    const fetchRoutines = async () => {
      setLoading(true);
      try {
        const data = await routinesService.getRoutines();
        setRoutines(data);
      } catch (error) {
        console.error('Failed to fetch routines:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchRoutines();
  }, [refetchTrigger]); // Refetch when trigger changes

  const handleRoutineCreated = () => {
    setRefetchTrigger(prev => prev + 1); // Triggers refetch
  };

  return (
    // ... component JSX
  );
}
```

---

### Axios Configuration with JWT

**Automatic Token Refresh:**

```javascript
// services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - add token to every request
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If error is 401 and we haven't tried to refresh yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(
          `${process.env.REACT_APP_API_URL}/auth/refresh/`,
          { refresh: refreshToken }
        );

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh token expired - redirect to login
        localStorage.clear();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
```

---

## Styling Strategy

### Bootstrap + Custom SASS Approach

**Philosophy:**
- Use Bootstrap's grid system and utility classes
- Override Bootstrap variables for brand customization
- Write custom SASS for unique components
- Create reusable mixins for common patterns

---

### SASS File Structure

```
src/styles/
├── main.scss              # Main entry, imports everything
├── _variables.scss        # Custom variables
├── _mixins.scss          # Reusable SASS mixins
├── _themes.scss          # Light/dark theme definitions
├── components/
│   ├── _buttons.scss
│   ├── _cards.scss
│   ├── _forms.scss
│   ├── _navbar.scss
│   ├── _sidebar.scss
│   └── _modals.scss
└── pages/
    ├── _dashboard.scss
    ├── _auth.scss
    └── _profile.scss
```

---

### Main SASS Entry Point

```scss
// src/styles/main.scss

// 1. Import Bootstrap functions and variables
@import '~bootstrap/scss/functions';
@import '~bootstrap/scss/variables';

// 2. Override Bootstrap variables
$primary: #6366f1;
$secondary: #8b5cf6;
$success: #10b981;
$danger: #ef4444;
$warning: #f59e0b;
$info: #3b82f6;

$font-family-base: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
$border-radius: 0.5rem;
$border-radius-lg: 0.75rem;
$border-radius-sm: 0.25rem;

// 3. Import Bootstrap (only what we need)
@import '~bootstrap/scss/bootstrap';

// 4. Import our custom styles
@import './variables';
@import './mixins';
@import './themes';

// 5. Import component styles
@import './components/buttons';
@import './components/cards';
@import './components/forms';
@import './components/navbar';
@import './components/sidebar';
@import './components/modals';

// 6. Import page styles
@import './pages/dashboard';
@import './pages/auth';
@import './pages/profile';
```

---

### Custom Variables

```scss
// src/styles/_variables.scss

// Spacing
$spacing-xs: 0.25rem;
$spacing-sm: 0.5rem;
$spacing-md: 1rem;
$spacing-lg: 1.5rem;
$spacing-xl: 2rem;
$spacing-2xl: 3rem;

// Colors (beyond Bootstrap)
$gray-50: #f9fafb;
$gray-100: #f3f4f6;
$gray-200: #e5e7eb;
$gray-300: #d1d5db;
$gray-400: #9ca3af;
$gray-500: #6b7280;
$gray-600: #4b5563;
$gray-700: #374151;
$gray-800: #1f2937;
$gray-900: #111827;

// Z-index layers
$z-dropdown: 1000;
$z-modal: 1050;
$z-notification: 1100;
$z-sidebar: 1200;

// Transitions
$transition-fast: 150ms ease;
$transition-base: 250ms ease;
$transition-slow: 350ms ease;
```

---

### Theme System

```scss
// src/styles/_themes.scss

// Light theme
.theme-light {
  --bg-primary: #{$gray-50};
  --bg-secondary: #ffffff;
  --bg-tertiary: #{$gray-100};
  
  --text-primary: #{$gray-900};
  --text-secondary: #{$gray-600};
  --text-tertiary: #{$gray-400};
  
  --border-color: #{$gray-200};
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
}

// Dark theme
.theme-dark {
  --bg-primary: #{$gray-900};
  --bg-secondary: #{$gray-800};
  --bg-tertiary: #{$gray-700};
  
  --text-primary: #{$gray-50};
  --text-secondary: #{$gray-300};
  --text-tertiary: #{$gray-500};
  
  --border-color: #{$gray-700};
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.5);
}

// Apply theme variables
body {
  background-color: var(--bg-primary);
  color: var(--text-primary);
  transition: background-color $transition-base, color $transition-base;
}

.card {
  background-color: var(--bg-secondary);
  border-color: var(--border-color);
  box-shadow: var(--shadow-md);
}
```

---

### Reusable Mixins

```scss
// src/styles/_mixins.scss

// Flexbox utilities
@mixin flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

@mixin flex-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

// Glass morphism effect
@mixin glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: $border-radius;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

// Responsive typography
@mixin responsive-font($min, $max) {
  font-size: clamp(#{$min}rem, 2vw, #{$max}rem);
}

// Truncate text
@mixin truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

// Hover lift effect
@mixin hover-lift {
  transition: transform $transition-base, box-shadow $transition-base;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
  }
}

// Custom scrollbar
@mixin custom-scrollbar {
  &::-webkit-scrollbar {
    width: 8px;
  }

  &::-webkit-scrollbar-track {
    background: var(--bg-tertiary);
    border-radius: $border-radius;
  }

  &::-webkit-scrollbar-thumb {
    background: var(--text-tertiary);
    border-radius: $border-radius;

    &:hover {
      background: var(--text-secondary);
    }
  }
}
```

---

### Component Variant Pattern

```scss
// src/styles/components/_buttons.scss

.btn-custom {
  padding: 0.75rem 1.5rem;
  border-radius: $border-radius;
  font-weight: 600;
  font-size: 0.875rem;
  transition: all $transition-base;
  border: none;
  cursor: pointer;

  // Primary variant
  &--primary {
    background: linear-gradient(135deg, $primary, $secondary);
    color: white;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 20px rgba($primary, 0.3);
    }

    &:active {
      transform: translateY(0);
    }
  }

  // Secondary variant
  &--secondary {
    background: transparent;
    border: 2px solid $primary;
    color: $primary;

    &:hover {
      background: $primary;
      color: white;
    }
  }

  // Danger variant
  &--danger {
    background: $danger;
    color: white;

    &:hover {
      background: darken($danger, 10%);
    }
  }

  // Sizes
  &--sm {
    padding: 0.5rem 1rem;
    font-size: 0.75rem;
  }

  &--lg {
    padding: 1rem 2rem;
    font-size: 1rem;
  }

  // Disabled state
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    pointer-events: none;
  }
}
```

**React Component:**
```jsx
// components/common/Button.jsx
function Button({ 
  variant = 'primary', 
  size = 'md',
  children, 
  ...props 
}) {
  const className = `btn-custom btn-custom--${variant} ${
    size !== 'md' ? `btn-custom--${size}` : ''
  }`;

  return (
    <button className={className} {...props}>
      {children}
    </button>
  );
}

// Usage:
<Button variant="primary">Create Routine</Button>
<Button variant="secondary" size="sm">Cancel</Button>
<Button variant="danger">Delete</Button>
```

---

## Development Workflow

### Phase 1: Backend Setup
1. Set up Django project + DRF
2. Configure PostgreSQL database
3. Create models (Users, Routines, Actions, etc.)
4. Set up JWT authentication
5. Create serializers
6. Build API endpoints using ViewSets
7. Test with Postman/Thunder Client
8. Configure CORS for frontend

### Phase 2: Frontend Setup
1. Set up React project with Vite
2. Install dependencies (React Router, Axios, Bootstrap, SASS)
3. Create file structure
4. Set up Axios instance with interceptors
5. Create Context providers
6. Build authentication flow (login/register)

### Phase 3: Core Features
1. Dashboard - List routines
2. Routine detail - View actions
3. Complete action with feedback
4. Notifications sidebar
5. Profile & preferences

### Phase 4: Advanced Features
1. Accountability partnerships
2. Streak calculations
3. Progress visualization
4. Theme switching

### Phase 5: Polish & Deploy
1. Error handling
2. Loading states
3. Empty states
4. Responsive design testing
5. Performance optimization
6. Deploy to Render

---

## Testing Strategy

### Backend Testing
- Django's built-in testing framework
- Test models, serializers, views
- Test authentication flow
- Test API endpoints

### Frontend Testing (Optional for MVP)
- React Testing Library
- Test critical user flows
- Test authentication
- Test form submissions

---

## Security Considerations

### Backend
- ✅ Password hashing (Django default)
- ✅ JWT token authentication
- ✅ HTTPS only in production
- ✅ CORS configuration
- ✅ Environment variables for secrets
- ✅ SQL injection protection (Django ORM)
- ✅ Rate limiting (consider django-ratelimit)

### Frontend
- ✅ JWT in localStorage (acceptable for MVP)
- ⚠️ XSS vulnerability (sanitize user inputs)
- ✅ CSRF immunity (JWT in headers)
- ✅ Environment variables for API URLs
- ⚠️ Validate user inputs before sending to API

### Production Considerations (Beyond MVP)
- httpOnly cookies for refresh tokens
- Content Security Policy headers
- Rate limiting on API endpoints
- Input sanitization
- Regular security audits

---

## Environment Variables

### Backend (.env)
```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/habittracker
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME=Habit Tracker
```

---

## Success Criteria (Assignment Rubric Alignment)

### 1. Django Concepts (Distinction Level)
- ✅ Models with proper relationships
- ✅ Custom User model extensions
- ✅ Django REST Framework ViewSets
- ✅ Serializers with validation
- ✅ Authentication & permissions

### 2. Database Integration (Distinction Level)
- ✅ PostgreSQL with proper schema
- ✅ Foreign key relationships
- ✅ Normalized tables
- ✅ Migrations management
- ✅ Query optimization

### 3. Authentication & Authorization (Distinction Level)
- ✅ JWT token authentication
- ✅ User registration & login
- ✅ Password hashing
- ✅ Protected API endpoints
- ✅ Role-based access (owner-only editing)

### 4. Clean Code Structure (Distinction Level)
- ✅ Component-based React architecture
- ✅ Reusable components
- ✅ SASS organization
- ✅ Bootstrap integration
- ✅ Proper file structure
- ✅ Comments & docstrings

### 5. Hosted & Functional (Distinction Level)
- ✅ Deployed on Render
- ✅ Fully functional features
- ✅ Responsive design
- ✅ Error handling
- ✅ Clear documentation

---

## Next Steps: Phase 1 Implementation

**Recommended Approach: Vertical Slice (Feature-by-Feature)**

This means building each feature end-to-end (Django + React) before moving to the next:

1. **Slice 1:** User Authentication
   - Backend: User model, JWT endpoints
   - Frontend: Login/Register pages, AuthContext
   
2. **Slice 2:** Routines Management
   - Backend: Routine model, CRUD endpoints
   - Frontend: Dashboard, RoutineCard, Create modal

3. **Slice 3:** Actions & Completions
   - Backend: Action & Completion models, endpoints
   - Frontend: Action items, completion form

4. **Slice 4:** Notifications
   - Backend: Notification model, generation logic
   - Frontend: Notification sidebar, NotificationContext

5. **Slice 5:** Accountability Partnerships
   - Backend: Partnership model, endpoints
   - Frontend: Partnership request/accept UI

**Benefits of this approach:**
- See progress quickly (motivating!)
- Test full stack integration early
- Identify issues before they compound
- Can deploy working features incrementally

---

## Questions Before Starting Phase 1

1. **Backend or frontend first?** Or vertical slice (recommended)?
2. **Development environment:** Do you have Python, Node.js, PostgreSQL installed?
3. **Editor:** VS Code? (Recommended with extensions)
4. **Version control:** Git repository set up?

**Once you answer these, we'll begin Phase 1: Setting up Django + PostgreSQL!** 🚀
