
import MySQLdb as mdb


def connect(host, user, passwd, name):
	conn = mdb.connect(host, user, passwd, name);
	return conn


def close_connection(conn):
	conn.close()


def get_total_lines(conn, school_id=None):
	cursor = conn.cursor()
	query = "SELECT COUNT(*) FROM `TABLE 1`"
	if school_id:
		query += " WHERE COD_ESCOLA = '%s'" % school_id
	cursor.execute(query)
	return cursor.fetchone()[0]

def get_total_absents(conn, school_id=None):
	cursor = conn.cursor()
	query = "SELECT COUNT(*) FROM `TABLE 1` WHERE IN_STATUS_REDACAO = 6"
	if school_id:
		query += " AND COD_ESCOLA = '%s'" % school_id
	cursor.execute(query)
	return cursor.fetchone()[0]	


def get_score_avg(conn, school_id=None):
	cursor = conn.cursor()
	query = "SELECT AVG(NU_NOTA_COMP1), AVG(NU_NOTA_COMP2), AVG(NU_NOTA_COMP3), "\
					"AVG(NU_NOTA_COMP4), AVG(NU_NOTA_COMP5), AVG(NU_NOTA_REDACAO) FROM `TABLE 1` "\
					"WHERE IN_STATUS_REDACAO != 6"
	if school_id:
		query += " AND COD_ESCOLA = '%s'" % school_id	
	cursor.execute(query)
	avg = cursor.fetchone()
	return avg


def get_score_avg_uf(conn):
	cursor = conn.cursor()
	cursor.execute("SELECT UF_ESC, AVG(NU_NOTA_COMP1), AVG(NU_NOTA_COMP2), AVG(NU_NOTA_COMP3), "\
				  "AVG(NU_NOTA_COMP4), AVG(NU_NOTA_COMP5), AVG(NU_NOTA_REDACAO) FROM `TABLE 1` "\
				  "WHERE UF_ESC IS NOT NULL AND IN_STATUS_REDACAO != 6 GROUP BY (UF_ESC)")
	result = []
	for row in cursor:
		result.append({
			"uf": row[0],
			"score1" : row[1],
			"score2" : row[2],
			"score3" : row[3],
			"score4" : row[4],
			"score5" : row[5],
			"total" : row[6],
		})
	return result


def get_uf_score_avg(conn, uf):
	cursor = conn.cursor()
	cursor.execute("SELECT AVG(NU_NOTA_REDACAO) FROM `TABLE 1` "\
				  "WHERE UF_ESC = '%s' AND IN_STATUS_REDACAO != 6 " % uf)
	avg = cursor.fetchone()[0]
	return avg

def get_city_score_avg(conn, city):
	cursor = conn.cursor()
	cursor.execute("SELECT AVG(NU_NOTA_REDACAO) FROM `TABLE 1` "\
				  "WHERE NO_MUNICIPIO_ESC = '%s' AND IN_STATUS_REDACAO != 6" % city)
	avg = cursor.fetchone()[0]
	return avg


def get_score_avg_age(conn, school_id=None):
	cursor = conn.cursor()
	query = "SELECT IDADE, AVG(NU_NOTA_COMP1), AVG(NU_NOTA_COMP2), AVG(NU_NOTA_COMP3), "\
				  "AVG(NU_NOTA_COMP4), AVG(NU_NOTA_COMP5), AVG(NU_NOTA_REDACAO) FROM `TABLE 1` "\
				  "WHERE IDADE IS NOT NULL AND IN_STATUS_REDACAO != 6 "
	if school_id:
		query += " AND COD_ESCOLA = '%s'" % school_id
	query += " GROUP BY (IDADE);"	
	cursor.execute(query)
	result = []
	for row in cursor:
		result.append({
			"age": row[0],
			"score1" : row[1],
			"score2" : row[2],
			"score3" : row[3],
			"score4" : row[4],
			"score5" : row[5],
			"total" : row[6],
		})
	return result


def get_score_avg_sex(conn, school_id=None):
	cursor = conn.cursor()
	query = "SELECT TP_SEXO, AVG(NU_NOTA_REDACAO) FROM `TABLE 1` "\
				  "WHERE TP_SEXO IS NOT NULL AND IN_STATUS_REDACAO != 6"
	if school_id:
		query += " AND COD_ESCOLA = '%s'" % school_id
	query += " GROUP BY (TP_SEXO);"	
	cursor.execute(query)
	result = []
	for row in cursor:
		result.append({
			"sex": row[0],
			"avg" : row[1]
		})
	return result


def get_count_per_score_interval(conn, start_score, end_score, school_id=None, 
	score_type='NU_NOTA_REDACAO', uf=None):

	cursor = conn.cursor()
	query = "SELECT COUNT(*) FROM `TABLE 1` "\
				  "WHERE %s BETWEEN %d AND %d" \
				  " AND IN_STATUS_REDACAO != 6" % (score_type, start_score, end_score)
	if school_id:
		query += " AND COD_ESCOLA = '%s'" % school_id
	if uf:
		query += " AND UF = '%s'" % uf
	cursor.execute(query)

	return cursor.fetchone()[0]


def get_school_uf(conn, school_id):
	cursor = conn.cursor()
	query = "SELECT UF_ESC FROM `TABLE 1` "\
				  "WHERE COD_ESCOLA = '%s' LIMIT 1" % school_id
	cursor.execute(query)
	result = cursor.fetchone()
	if result is not None and len(result) > 0:
		return result[0]
	else:
		return None


def get_school_city(conn, school_id):
	cursor = conn.cursor()
	query = "SELECT NO_MUNICIPIO_ESC FROM `TABLE 1` "\
				  "WHERE COD_ESCOLA = '%s' LIMIT 1" % school_id
	cursor.execute(query)
	result = cursor.fetchone()
	if result is not None and len(result) > 0:
		return result[0]
	else:
	    return None
