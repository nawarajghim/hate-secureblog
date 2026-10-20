# HATE SecureBlog

This is a simple blog application I built using Python and Flask. 
The main purpose of this project is to explore the security risks that can appear in AI-generated code and learn how to find and fix them using the HATE (Hypothesise, Ask, Test, Enhance) method.

## What the Application Does

The application allows users to write blog posts in Markdown and view them as HTML.

It has two main features:
 - Create a new blog post using `POST /posts`.
 - View an existing blog post using `GET /posts/<id>`.

A simple token is used to access these endpoints.

## Security Testing

During testing, I focused on two security issues:

- Stored XSS: The original code allowed HTML and JavaScript to be included in blog posts without proper escaping.
- Large requests: The application initially had no limit on how much data users could submit.

I tested both issues and then made changes to improve the application's security.

## Changes I Made

To address these issues, I:

- Added HTML escaping to prevent submitted scripts from being rendered as executable code.
- Added a 1 MiB request-size limit so the application rejects oversized requests.

The Git commit history shows both the original AI-generated code and the updated version after the fixes.

## How to Run the Application

You will need Python installed on your computer.

First, open a terminal in the project folder and install the required packages:

    python -m pip install Flask Markdown

Then start the application:


    python app.py


The application runs locally at:

    http://127.0.0.1:5000

To create or view posts, include this header in your requests:

    Authorization: Bearer my-secret-token

## Tools Used

- Python
- Flask
- Python-Markdown
- Visual Studio Code
- Git and GitHub

## Important Note

This application is only intended for learning and local security testing. It stores posts temporarily in memory and uses a demonstration authentication token, so it should not be used as a real production blog.