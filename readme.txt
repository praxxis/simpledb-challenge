Your task is create a very simple in-memory database, which has a very limited command set. All of the commands are going to be fed to you one line at a time via stdin, and your job is the process the commands and perform whatever operation the command dictates. Here are the basic commands you need to handle:

    SET [name] [value]: Set a variable [name] to the value [value]. Neither variable names or values will ever contain spaces.
    GET [name]: Print out the value stored under the variable [name]. Print NULL if that variable name hasn't been set.
    UNSET [name]: Unset the variable [name]
    NUMEQUALTO [value]: Return the number of variables equal to [value]. If no values are equal, this should output 0.
    END: Exit the program

So here is a sample input:

SET a 10
GET a
UNSET a
GET a
END

And its corresponding output:

10
NULL

And another one:

SET a 10
SET b 10
NUMEQUALTO 10
NUMEQUALTO 20
UNSET a
NUMEQUALTO 10
SET b 30
NUMEQUALTO 10
END

And its corresponding output:

2
0
1
0

Now, as I said this was a database, and because of that we want to add in a few transactional features to help us maintain data integrity. So there are 3 additional commands you will need to support:

    BEGIN: Open a transactional block
    ROLLBACK: Rollback all of the commands from the most recent transaction block. If no transactional block is open, print out INVALID ROLLBACK
    COMMIT: Permanently store all of the operations from any presently open transactional blocks

Our database supports nested transactional blocks as you can tell by the above commands. Remember, ROLLBACK only rolls back the most recent transaction block, while COMMIT closes all open transactional blocks. Any command issued outside of a transactional block commits automatically.

The most commonly used commands are GET, SET, UNSET and NUMEQUALTO, and each of these commands should be faster than O(N) expected worst case, where N is the number of total variables stored in the database.

Typically, we will already have committed a lot of data when we begin a new transaction, but the transaction will only modify a few values. So, your solution should be efficient about how much memory is allocated for new transactions, i.e., it is bad if beginning a transaction nearly doubles your program's memory usage.

Here are some sample inputs and expected outputs using these commands:

Input:

BEGIN
SET a 10
GET a
BEGIN
SET a 20
GET a
ROLLBACK
GET a
ROLLBACK
GET a
END

Output:

10
20
10
NULL

Input:

BEGIN
SET a 30
BEGIN
SET a 40
COMMIT
GET a
ROLLBACK
END

Output:

40
INVALID ROLLBACK

Input:

SET a 50
BEGIN
GET a
SET a 60
BEGIN
UNSET a
GET a
ROLLBACK
GET a
COMMIT
GET a
END

Output:

50
NULL
60
60

Input:

SET a 10
BEGIN
NUMEQUALTO 10
BEGIN
UNSET a
NUMEQUALTO 10
ROLLBACK
NUMEQUALTO 10
END

Output:

1
0
1
