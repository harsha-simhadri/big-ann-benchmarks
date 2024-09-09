su - postgres -c "/usr/lib/postgresql/16/bin/pg_ctl -D /var/lib/postgresql/test_database -l /var/lib/postgresql/test_database_logfile -o \"-F -p 5432\" start"
