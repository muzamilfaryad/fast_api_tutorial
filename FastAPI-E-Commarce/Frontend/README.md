# FastAPI-E-Commarce Frontend

React + Vite frontend for the e-commerce tutorial project.

## What It Covers

- Customer-facing browsing flows.
- Authentication screens for login and signup.
- Admin flows for adding categories and products.
- Shared navigation and reusable API helpers.
- Separation between API modules and UI components.

## Folder Structure

- `src/api/` - Axios-based API wrappers.
- `src/components/` - reusable UI components.
- `src/components/admin/` - admin dashboard and modal forms.
- `src/components/customer/` - customer browsing views.
- `src/App.jsx` - application shell and routing setup.

## Install

```bash
npm install
```

## Run

```bash
npm run dev
```

The dev server usually runs on `http://localhost:5173`, which matches the backend CORS configuration.

## Build and Check

```bash
npm run build
npm run lint
```

## Notes

- This project was scaffolded with Vite and uses plain React with React Router and Axios.
- The frontend expects the backend API to be running before you test authenticated or data-driven pages.
