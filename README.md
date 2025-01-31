# JobSync

Behold My Awesome Project!

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Settings

Moved to [settings](https://cookiecutter-django.readthedocs.io/en/latest/1-getting-started/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

    ```bash
    $ python manage.py createsuperuser
    ```

- For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

- Running type checks with mypy:

    ```bash
    $ mypy jobsync
    ```

### Test coverage

- To run the tests, check your test coverage, and generate an HTML coverage report:

    ```bash
    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html
    ```

#### Running tests with pytest

    ```bash
    $ pytest
    ```

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally.html#using-webpack-or-gulp).

## Deployment

The following details how to deploy this application.

**JobSync Project Overview**

## Core Features

1. Job listing management
2. User roles (Job Seeker, Recruiter)
3. Organization management
4. Job applications tracking
5. Skills management
6. External job integration

## Models Structure

- **User**
  - Role (job_seeker/recruiter)
  - Organization (Optional)
  - Profile details (name, email, job_title)

- **Organization**
  - Basic details (name, address, website)
  - Related jobs and employees

- **JobListing**
  - Title, description, location
  - Company (Organization)
  - Required skills
  - External URL integration
  - Posted date tracking

- **JobApplication**
  - Job reference
  - Applicant details
  - Cover letter
  - Application date tracking

- **Skill**
  - Name (unique)

## Key API Features

- **Auth**
  - /api/signup/
  - /api/signin/

- **Jobs**
  - /api/listings/ (CRUD)
  - /api/listings/dashboard/
  - /api/listings/employer_insights/

- **Applications**
  - Application management
  - Status tracking

## Key Features

### For Recruiters:

- Post job listings
- Track applications
- View employer insights
- Organization management
- Application statistics

### For Job Seekers:

- View job listings
- Apply to jobs
- Track applications
- Profile management
- Skills matching
- External Integration

## Job Scraping Features
- WeWorkRemotely integration
- Category-based job fetching
- Automated job import
- External URL tracking

# Analytics & Insights
- Total jobs posted
- Application statistics
- Popular job tracking
- Organization metrics

## Security Features
- Token-based authentication
- Role-based access control
- Organization-level permissions
- Secure password handling