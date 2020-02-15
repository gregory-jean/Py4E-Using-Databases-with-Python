import sqlite3

# Make a connection, send sql commands through cursor
conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

# Drop table if it exists
cur.execute('DROP TABLE IF EXISTS Counts')

# Create the table
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'mbox-short.txt'
fh = open(fname)
for line in fh:
    # Ensure only From lines are used
    if not line.startswith('From: '): continue
    pieces = line.split()

    # Grab email address
    email = pieces[1]

    # Split the email addresses into email name and the email organization
    epieces = email.split('@')

    # Extract the email domain
    org = epieces[1]

    # ? is a placeholder, ensures there arent sql injections being performed
    # Multiple ? for each value in tuple
    # (email,) tuple with one thing in it
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))

    # row is a list of the  information we get from the database
    row = cur.fetchone()
    if row is None:
        # Create new row for each new email, set the count to 1
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org,))
    else:
        # Update the database row count value if the email already exists
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org,))

# Commits the updated records to memory
conn.commit()

# https://www.sqlite.org/lang_select.html
# 
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()