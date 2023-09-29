RACE1:

Use coupon multiple time

Lab Setup:

1. Databse setup
```
CREATE DATABASE coupon_demo;
USE coupon_demo;
CREATE TABLE coupons (id INT AUTO_INCREMENT PRIMARY KEY, code VARCHAR(255) NOT NULL);
INSERT INTO coupons (code) VALUES ('SUMMER2023'), ('FALLSALE');
CREATE TABLE used_coupons (id INT AUTO_INCREMENT PRIMARY KEY, code VARCHAR(255) NOT NULL);
```

The default app has a time delay before adding the coupon in the used_coupons table to simulate any app processing before adding the coupon to user
used coupon list you can reduce the time gap to analyze the race window and remove the sleep line completely to see that intruder is not able
to detect the race condition there but it can be exploited using turbo intruder.


# FIX

The racefix.py contains the fixed code which uses transaction to prevent other requests going through the used coupons query untill the insert query
is completed 

The FOR UPDATE clause in a SQL query is used to lock the selected rows in a table for the duration of a transaction. This prevents other transactions from modifying those rows until the current transaction is completed.

Here's how FOR UPDATE works:

    Transaction Begin: When a transaction begins (typically with a BEGIN or an implicit start in some database systems), the database starts keeping track of the changes made within the transaction.

    SELECT with FOR UPDATE: When a SELECT query includes the FOR UPDATE clause, it indicates that the selected rows are going to be updated later in the current transaction.

    For example:

    sql

    SELECT * FROM table_name WHERE condition FOR UPDATE;

    This locks the selected rows and prevents other transactions from modifying them until the current transaction is completed.

    Lock Acquisition: When the SELECT query with FOR UPDATE is executed, the database acquires locks on the selected rows. These locks prevent other transactions from modifying those rows.

    Transaction Continues: The transaction continues as usual. You can perform other operations within the same transaction.

    UPDATE: When you later perform an UPDATE operation on the selected rows, the locks acquired using FOR UPDATE are still in effect. This means that other transactions will be blocked from modifying the locked rows until the current transaction is committed or rolled back.

    Transaction End: When you commit the transaction, the changes are permanently saved, and the locks are released. If you roll back the transaction, the changes are discarded, and the locks are released.

Using FOR UPDATE is a way to enforce data integrity and prevent race conditions in situations where multiple transactions might attempt to modify the same data concurrently.

Keep in mind that using FOR UPDATE can potentially lead to deadlocks if not used carefully. Deadlocks occur when two or more transactions are waiting for each other to release locks, resulting in a deadlock situation. It's important to handle deadlock scenarios in your application logic or database design.
