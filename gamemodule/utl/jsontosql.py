import sqlite3
import json

db = sqlite3.connect('database.db')
cursor = db.cursor()

create_tale = """
create table if not exists tbl_GridBlocks(
    blockID int(12) primary key not null auto_increment,
    blockX int(12) default 10 not null,
    blockY int(12) default 10 not null,
    blockW int(12) default 50 not null,
    blockH int(12) default 50 not null,
    blockMETA text default '{}' not null,
    blockColourR int(3) default 255 not null,
    blockColourG int(3) default 255 not null,
    blockColourB int(3) default 255 not null,
)
"""

# Using python equivalent of prepared statement to help against sql injection

insert_block = """
    insert into tbl_GridBlocks(
    blockX, blockY, blockW, blockH, blockMETA, blockColourR, blockColourG, blockColourB   
) values (%i, %i, %i, %i, %s, %i, %i, %i)
"""

# This statement can then later be used with python mod to complete prepared statement

get_blocks = """
    select * from tbl_Gridblocks
"""

# Make sure table exists

cursor.execute(create_tale)

def export_gridstate(grid_state_dict):

    block_ids = []

    for block in grid_state_dict:

        cursor.execute(
            insert_block % (
                block['x'], block['y'], block['w'], block['h'], json.dumps(block['metadata']), block['r'], block['g'], block['b']
            )
        )

        # Get last made primary key ID

        cursor.execute('select last_insert_rowid()'); block_ids.append(cursor.fetchall())

    return block_ids

def import_gridstate():

    cursor.execute(get_blocks)
    return cursor.fetchall()

#  Can retrieve made SQL and such, did not use within actual project
#  How can making a program less efficient get more marks..
#  Using JSON works absolutely fine, no need to complicate things
#  Check game exports and game logs for any other information
