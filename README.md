# Overview

I have created this program as a way to teach myself how to use SQLite commands to access and manipulate databases.  This program is the first step in working with a startup company to track inventory.  It is a thought practice to work through how the properties of each product relate to each other, how they are recorded, and how they are tracked.  Using databases to interact with the data is very useful. As a new software engineer this is a great first step in understanding and gaining necessary skills to create useful products.

I have created a software product that allows product managers to add a product to the tracking system and designate how much product is stored at each location.  It tallies the 3 locations and shows total quantities as well.  If product changes at one or more location that can be updated and the program recalculates the total quantity.  If the quantity of a flavor at any location drops below 200 that line will turn red as an alert to order more of that flavor.  When stock is replenished and above 200 it will return to normal color.  To add a product, the user needs to merely select the product id from the drop down menu.  It will then set the product name, price, and pack size.  All of that is built into the ID.  The letters are the initials of the flavor, the end 2 numbers indicate if it's a 12 pack or 24 pack with also determines the price. The update button allows quantities to be adjusted and the sort by button reveals 3 new buttons to sort the data by.

[Inventory Management System Walkthrough](https://youtu.be/PjwnravrZ18)

# Relational Database

- SQLite
- The structure of the table includes fields for storing inventory data on drink products

# Development Environment

- VS Code
- SQLite Python
- Tkinter Library

# Useful Websites

- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [W3 Schools SQL](https://www.w3schools.com/sql/default.asp)
- [Python SQLite3 Library](https://docs.python.org/3.8/library/sqlite3.html)
- [Tutorials Point](https://www.tutorialspoint.com/sqlite/sqlite_python.htm)
- [Python Tkinter Library](https://docs.python.org/3/library/tkinter.ttk.html#treeview)
- [Mastery Protein](https://www.masteryprotein.com/)

# Future Work

- Item 1- I would like to build out on this program.  I would like to add customers, vendors, have the orders come out of the inventory directly.

- Item 2- I would like to use a different framework.  I have recently been exposed to the .NET framework and I think I could have better control and separation between data.

- Item 3- I would fix the interaction between flavor and Id. Right now Id can pick flavor, but flavor does not pick ID since there are 2 ID (pack sizes) for every 1 flavor.  I tried to get the math to work on this and gave up for now.
