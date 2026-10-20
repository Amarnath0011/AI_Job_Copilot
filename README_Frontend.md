# AI Job Copilot Frontend Interview Notes

> This document is intended as a complete revision guide for the
> **frontend** of the AI Job Copilot project. Read this before frontend
> interviews.

------------------------------------------------------------------------

# 1. Project Overview

AI Job Copilot is a React + Vite application that helps users:

-   Upload a resume
-   Perform ATS analysis
-   Receive AI feedback
-   Practice AI mock interviews
-   View a final interview report

Tech Stack

-   React 19
-   Vite
-   React Router DOM
-   Axios
-   Tailwind CSS
-   FastAPI Backend

------------------------------------------------------------------------

# 2. Folder Structure

``` text
src/
│
├── api/
│   └── axios.js
│
├── components/
│   └── ui/
│       └── Card.jsx
│
├── features/
│   ├── landing/
│   ├── resume/
│   ├── interview/
│   └── report/
│
├── layouts/
│   └── MainLayout.jsx
│
├── pages/
│   ├── LandingPage.jsx
│   ├── ResumePage.jsx
│   ├── InterviewPage.jsx
│   └── ReportPage.jsx
│
├── routes/
│   └── AppRoutes.jsx
│
├── services/
│   ├── resumeService.js
│   ├── atsService.js
│   └── interviewService.js
│
├── App.jsx
└── main.jsx
```

------------------------------------------------------------------------

# 3. Architecture

Pattern used:

    Page
      ↓
    Feature Components
      ↓
    Service Layer
      ↓
    Axios
      ↓
    FastAPI

Pages coordinate state. Feature components render UI. Services perform
API communication.

------------------------------------------------------------------------

# 4. Routing

React Router is used.

Flow:

    Browser URL
            ↓
    BrowserRouter
            ↓
    Routes
            ↓
    Route
            ↓
    Component

Main routes:

-   /
-   /resume
-   /interview
-   /report

Use `Link` instead of `<a>` to avoid full page reloads.

------------------------------------------------------------------------

# 5. Layout

MainLayout contains shared UI:

-   Navbar
-   Outlet
-   Footer

Outlet renders the current page.

------------------------------------------------------------------------

# 6. Feature Modules

## Landing

Hero Features CTA

## Resume

ResumeUpload ATSScore ResumeFeedback

## Interview

InterviewHeader StartInterview ProgressBar QuestionCard AnswerInput
ScoreCard LoadingScreen InterviewComplete

## Report

FinalReport StrengthCard WeaknessCard

------------------------------------------------------------------------

# 7. API Layer

Axios instance:

-   Centralized baseURL
-   Common headers
-   Cleaner API calls

Example pattern:

    Page
     ↓
    Service
     ↓
    axios.post(...)

Services:

resumeService

-   uploadResume()

atsService

-   analyzeResume()

interviewService

-   startInterview()
-   submitAnswer()
-   endInterview()

------------------------------------------------------------------------

# 8. Backend APIs

## Resume Upload

POST /resume/upload

Request: multipart/form-data

Response:

-   session_id
-   resume text
-   filename

------------------------------------------------------------------------

## ATS Analysis

POST /ats/analyze

Request

    {
     session_id,
     job_description
    }

Response

-   ats_score
-   semantic_similarity
-   matching_skills
-   missing_skills
-   ai_feedback

------------------------------------------------------------------------

## Interview Start

POST /interview/start

Request

    {
     job_description
    }

Returns

-   session_id
-   question
-   question_number
-   total_questions

------------------------------------------------------------------------

## Submit Answer

POST /interview/answer

Request

    {
     session_id,
     answer
    }

Returns

-   evaluation
-   next_question
-   interview_completed

------------------------------------------------------------------------

## End Interview

POST /interview/end

Request

    {
     session_id
    }

Returns final report.

------------------------------------------------------------------------

# 9. Resume Flow

User uploads resume

↓

Resume uploaded

↓

session_id received

↓

User enters Job Description

↓

ATS API

↓

ATS Score

↓

Resume Feedback

------------------------------------------------------------------------

# 10. Interview Flow

User enters JD

↓

Start Interview

↓

Question 1

↓

Answer

↓

Evaluation

↓

Next Question

↓

Question 5

↓

End Interview API

↓

Report Page

------------------------------------------------------------------------

# 11. React Fundamentals

## Component

Reusable UI function.

## Props

Read-only data passed parent → child.

## State

Mutable data owned by a component.

Example uses:

-   loading
-   question
-   score

## useState

Stores local component state.

Rules

-   Causes re-render.
-   Setter is asynchronous.
-   Never mutate state directly.

## useEffect

Runs side effects.

Uses

-   API calls
-   subscriptions
-   timers

Dependency array

\[\]

Runs once.

[state](#state)

Runs when state changes.

No array

Runs every render.

## Controlled Component

Input value controlled by React state.

Example:

textarea value={state}

onChange updates state.

------------------------------------------------------------------------

# 12. Event Handling

Examples

onClick

onChange

onSubmit

Functions are passed, not executed:

Correct

onClick={handleClick}

Incorrect

onClick={handleClick()}

------------------------------------------------------------------------

# 13. Conditional Rendering

Patterns

    condition && <Component/>

    condition ? A : B

Used for:

Loading

Interview started

Evaluation

Report

------------------------------------------------------------------------

# 14. Lifting State

Parent owns state.

Children receive:

-   value
-   callback

Example:

ResumePage owns ATS data.

ATSScore only displays props.

------------------------------------------------------------------------

# 15. Service Layer

Never call axios directly from components.

Instead

Component

↓

Service

↓

Axios

Advantages

-   reusable
-   testable
-   maintainable

------------------------------------------------------------------------

# 16. React Router Concepts

BrowserRouter

Provides routing context.

Routes

Collection of Route.

Route

Maps URL to component.

Link

Client-side navigation.

Outlet

Placeholder for nested routes.

Navigate

Programmatic redirect.

useNavigate

Navigate inside JS.

useLocation

Receive route state.

------------------------------------------------------------------------

# 17. Tailwind CSS

Utility-first CSS framework.

Benefits

-   Fast
-   Responsive
-   No separate CSS files

Common utilities

Layout

flex grid

Spacing

p- m- gap-

Typography

text- font-

Colors

bg- text-

Responsive

sm: md: lg: xl:

------------------------------------------------------------------------

# 18. Axios

Promise-based HTTP client.

Methods

get

post

put

delete

Error Handling

try

catch

finally

------------------------------------------------------------------------

# 19. Common Interview Questions

Why React?

Virtual DOM improves UI updates and reusable components improve
maintainability.

Why Vite?

Faster startup and HMR than CRA.

Why Link instead of a?

Avoids full page reload.

Why Service Layer?

Separates UI from networking.

Why Feature Folder?

Groups related components together.

Difference between Props and State?

Props are read-only. State is mutable.

Controlled vs Uncontrolled Components?

Controlled uses React state.

Why use useState?

To store data that changes and trigger UI updates.

Why use lifting state?

To share data between siblings.

------------------------------------------------------------------------

# 20. Improvements

-   Add authentication
-   Theme switch
-   Toast notifications
-   Protected routes
-   Context API
-   Global error handling
-   Unit testing
-   Deployment

------------------------------------------------------------------------

# 21. Final Revision Checklist

Understand:

-   React component lifecycle
-   JSX
-   Props
-   State
-   useState
-   useEffect
-   Controlled components
-   React Router
-   Axios
-   Tailwind
-   Feature-based architecture
-   API integration
-   Parent-child communication
-   Conditional rendering
-   Loading states
-   Responsive design
-   Error handling

If you can explain every section in this document without looking at
code, you are well prepared to discuss the frontend architecture of AI
Job Copilot in an interview.
