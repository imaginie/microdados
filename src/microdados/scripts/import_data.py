# coding=utf-8

import MySQLdb as mdb
import sys
import sys, getopt


DB_USER = 'root'
DB_PASSWD = 'root'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'microdados'
DB_TABLE = 'TABLE 1'


def connect(host, user, passwd, name):
    conn = mdb.connect(host, user, passwd, name);
    return conn

def close_connection(conn):
    conn.close()

def import_data(conn, csv_file):
    """ Import data

    Read data from "microdados" csv file.
    First line must be the list of field labels.
    """
    with open(csv_file, 'r') as f:
        labels = f.readline().rstrip()

        for line in f:
            # get data
            entry = line.rstrip()
            entry_data = entry.split(',')

            query = "INSERT INTO `" + DB_TABLE + "`(" + labels + ") VALUES ("
            for field in entry_data:
                if len(field):
                    query += "'" + field + "',"
                else:
                    query += "NULL,"
            # remove last ,
            if query[-1] == ',':
                query = query[:-1]
            query += ");"

            # apply query
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

    close_connection(conn)


def main(argv):
    # load parameters
    inputfile = None

    help_msg = "import_data.py -i <inputfile>"
    try:
        opts, args = getopt.getopt(argv,"hi:",["inputfile=",])
    except getopt.GetoptError:
        print help_msg
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print help_msg
            sys.exit()
        elif opt in ("-i", "--inputfile"):
            inputfile = arg
    if inputfile is None:
        print help_msg
        sys.exit()
    # import
    conn = connect(DB_HOST, DB_USER, DB_PASSWD, DB_NAME)
    import_data(conn, inputfile)


if __name__ == "__main__":
    main(sys.argv[1:])


