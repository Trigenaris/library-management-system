<h1 align='center'> 📚 Library Management System </h1>

In this project, we create a **library database** for the users to borrow and return books from a made-up library system called Daisy Library. 

### 📌 Required Modules:
* tkinter
* os
* csv
* sqlite3
* webbrowser

### 📌 Main features:

* Showing Books
* Showing Members
* Showing Lent Books
* Adding a Book
* Removing a Book
* Registering a Member
* Removing a Member
* Lending a Book
* Returning a Book
* Adding Multiple Books (with a csv file)
* Adding Multiple Members (with a csv file)

### 📌 Extra features:

* Some of the main features are hidden in a paned window. (*More options* button has to be clicked to see)
* *About us* link to see the website of the made-up Daisy Library System

<hr>

<h2 align='center' > 📖~☕ Main Features  </h2>

#### Main Layout

![daisy](https://github.com/Trigenaris/library-management-system/assets/122381599/4b95f2dc-6985-49c0-b1a3-794cf16d6a26)

#### Showing Books:

![daisy_1](https://github.com/Trigenaris/library-management-system/assets/122381599/de3d186b-80d7-4e80-a8db-5f6efa7d1e52)

#### No Book Error:

If the system has no books in it, the user is informed by the warning message which is shown below:

![daisy_2](https://github.com/Trigenaris/library-management-system/assets/122381599/42429456-cd6a-49cf-80cd-d62757421cbc)

#### Showing Members:

![daisy_3](https://github.com/Trigenaris/library-management-system/assets/122381599/2e9e2856-0662-4498-9971-1fcbb6d23be7)

#### No Member Error:

If the system has no members in it, the user is informed by the warning message which is shown below:

![daisy_4](https://github.com/Trigenaris/library-management-system/assets/122381599/a75002aa-debb-46a3-8bf2-27846702ab3b)

#### More Options: 

As the user clicks the `More Options` button, a paned window appears on the main window's right side with other buttons.

![daisy_5](https://github.com/Trigenaris/library-management-system/assets/122381599/f0a7055d-cee7-4531-ad9b-89bf116e0eaf)

#### More Options Layout:

* Adding a book to the system
* Removing a book by their name
* Registering a new member to the system
* Removing a member by their member ID
* Lending a book to a member
* Returning a book to the system
* Adding multiple books to the system (only CSV files supported)
* Registering multiple members to the system (only CSV files supported)
* A URL linked to the website of the Daisy Library System

![daisy_7](https://github.com/Trigenaris/library-management-system/assets/122381599/b299e837-193f-46c1-b176-cf7742f8a5e4)

#### 📘 ➕ 📚 Adding a Book:

To do so; first, the user clicks the `Add Book` button:

![daisy_8](https://github.com/Trigenaris/library-management-system/assets/122381599/8bcf2d7b-7079-4990-b798-8a1ff0f45e05)

Then it is expected from the user to fill in the required information about the book:

![daisy_10](https://github.com/Trigenaris/library-management-system/assets/122381599/0fd7cbb6-b2d1-41f4-970c-ed2422bdd438)

An error message will be shown if the user does not fill in all the fields in the window:

![daisy_12](https://github.com/Trigenaris/library-management-system/assets/122381599/9e1740b6-da62-42d9-9e21-c53e9e79c6d4)
![daisy_13](https://github.com/Trigenaris/library-management-system/assets/122381599/f4ace495-aff3-45ae-a2ca-dfbd5e315d3e)

As the user fills in all the fields; they will answer a question box if they are certain about the book's information. If the answer is yes, another message box informs the user:

![daisy_14](https://github.com/Trigenaris/library-management-system/assets/122381599/623a2214-df61-422c-9e9d-77087bc10823)
![daisy_15](https://github.com/Trigenaris/library-management-system/assets/122381599/964d6aca-717f-40b6-be23-a8edc2569a0b)
![daisy_16](https://github.com/Trigenaris/library-management-system/assets/122381599/833669f9-284b-44fa-af9a-5db50373ce4a)

#### 📖 ~ 📋 Show Books:

The user can see the book when they click the `Show Books` button this time as the database has a book in the system now:

![daisy_1](https://github.com/Trigenaris/library-management-system/assets/122381599/5cb26333-c9cd-4a16-acd6-945de6950120)
![daisy_17](https://github.com/Trigenaris/library-management-system/assets/122381599/7c474023-7ac4-40e8-9405-1d9a8f600370)

#### 📚 ➖ 📘 Removing a Book:

First, the user clicks the `Remove Book` button:

![daisy_18](https://github.com/Trigenaris/library-management-system/assets/122381599/8237b737-c94a-425a-a69e-3e8a15413bf8)

Then, the user writes down the name of the book that they want to remove, and after a confirmation, the referred book will be removed from the system:

![daisy_19](https://github.com/Trigenaris/library-management-system/assets/122381599/d1a4db1d-f63f-4e91-97b5-eb1743cf1e0c)
![daisy_20](https://github.com/Trigenaris/library-management-system/assets/122381599/b4009104-d813-4019-b72d-7eb99124d11e)
![daisy_21](https://github.com/Trigenaris/library-management-system/assets/122381599/52fd5b2d-201e-4268-82b2-227ed3533540)

#### 👤 ➕ 👥 Registering a Member:

To do so; first; the user clicks the `Register Member` button:

![daisy_18](https://github.com/Trigenaris/library-management-system/assets/122381599/9aa3bf89-3be8-4f42-9d1d-763551a23247)

Then it is expected from the user to fill in the required information about the member:

![daisy_22](https://github.com/Trigenaris/library-management-system/assets/122381599/3ca4fb83-a328-4019-bf67-91be7f2ce51d)

After a confirmation, the member is added to the system:

![daisy_23](https://github.com/Trigenaris/library-management-system/assets/122381599/af4362b6-e61f-4c33-9ed9-5927ab35a008)

#### 👥 ~ 📋 Show Members:

The user can see the member when they click the `Show Members` button this time as the database has a member in the system now:

![daisy_3](https://github.com/Trigenaris/library-management-system/assets/122381599/34c24127-053d-484c-b185-c2591fe3700b)
![daisy_24](https://github.com/Trigenaris/library-management-system/assets/122381599/96b5da4c-6669-4418-9d00-fa7eaa3ed287)

#### 👥 ➖ 👤 Removing a Member:

First, the user clicks the `Remove Member` button:

![daisy_18](https://github.com/Trigenaris/library-management-system/assets/122381599/8237b737-c94a-425a-a69e-3e8a15413bf8)

Then, the user writes down the member no of the referring member that they want to remove, and after confirmation, the referred member will be removed from the system:

![daisy_25](https://github.com/Trigenaris/library-management-system/assets/122381599/994a09c0-f4b6-4ca3-aa88-f1c75e2c306c)
![daisy_26](https://github.com/Trigenaris/library-management-system/assets/122381599/24d70104-0bb4-42d4-b092-13ebfdfa7755)
![daisy_27](https://github.com/Trigenaris/library-management-system/assets/122381599/4a1f9920-4e3d-48ce-a1ea-2c75300c4e37)





