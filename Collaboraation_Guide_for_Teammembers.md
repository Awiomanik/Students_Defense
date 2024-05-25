# Team Collaboration Guide for Students Defense Game

This document is designed to guide us through working collaboratively on our tower defense game project using Git and GitHub. This guide aims to provide step-by-step instructions on how to manage tasks, write code, and contribute effectively.



## The Repository Structure

Our project repository is organized into several key folders:

- **Classes**: This is where each of you will develop and store your individual class files. Each class, such as `Game`, `Player`, `Map`, etc., should be coded here.

- **Documentation**: All documentation related to the project, including game design documents, specifications, and meeting notes, should be stored in this folder.

- **Playground_for_ideas_and_testing**: Use this space to experiment with new code, test features, or try out ideas without affecting the main project code. When you start a new test, create a folder for it to avoid interference with others when merging.

All files used by given class (like graphics, audio, text files with level data, etc..) should be within the class folder. In the future we might change repository structure and so it will be best practice to not hard code any dependencies and to describe them in the docstring at the begginning of a file.
We will build UI renderer separately from remaining classes, so in principle other classes should not need any media dependencies, but in case of some kind of testing or any unpredicted yet event, pack it all within the folder.

Additionally **Classes** folder will contain **Utilities.py** file for functions, classes and data type definitions that might be usefull in many different places around the project (eg. Coord - Data type for storing coordinates with defined operations like addition, created to standardize the data type in which classes exchange information about placement of objects on the map.). Feel free to add there any functionality (class, function, method, constant, etc...) that you think might be usefull.



## Working with Git

Contrary to our initial decision during the first meeting, at today's gathering the present members decided we will be using a single branch for simplicity. This means everyone will be working on the `main` branch, just in separate folders. We will test interoperability at meetings at the end of each sprint (for now, at least). I will merge all current branches today and notify you through another form of communication.



## Notice
It is most important to familiarize yourselves with lectures about object-oriented programming on the lecturer's website and (of high importance) with a guide that Marta found on the internet and shared with us in the group chat!



# Additional information to help with the project
(feel free to add something if you think it will help others)

## Detailed Guide on Using Markdown

Markdown is a lightweight markup language with plain text formatting syntax that is often used for writing documentation. Here’s how to use some basic Markdown syntax:

### Headers
Use `#` for headers. More `#`s mean smaller headers.

### Lists
To create a bullet list, start lines with `-` or `*`.
To create a numbered list, start with `1.`, `2.`, etc.

### Links and Images
To create a link, wrap the link text in brackets `[ ]`, and then wrap the link in parentheses `( )`.
To add an image, add an exclamation mark `!`, followed by the alt text in brackets `[ ]`, and the URL in parentheses `( )`.

### Code Blocks
To format text as a code block, use three backticks ``` before and after the code.