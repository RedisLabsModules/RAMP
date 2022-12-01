MODULE_CAPABILITIES = [
    {'name': 'types', 'desc': 'module has its own types and not only operate on existing redis types'},
    {'name': 'no_multi_key', 'desc': 'module has no methods that operate on multiple keys'},
    {'name': 'replica_of', 'desc': 'module can work with replicaof capability when it is loaded into a source or a destination database'},
    {'name': 'backup_restore', 'desc': 'module can work with import/export capability'},
    {'name': 'eviction_expiry', 'desc': 'module is able to handle eviction and expiry without an issue'},
    {'name': 'reshard_rebalance', 'desc': 'module is able to operate in a database that is resharded and rebalanced'},
    {'name': 'failover_migrate', 'desc': 'module is able to operate in a database that is failing over and migrating'},
    {'name': 'persistence_aof', 'desc': 'module is able to operate in a database when database chooses AOF persistence option'},
    {'name': 'persistence_rdb', 'desc': 'module is able to operate in a database when database chooses SNAPSHOT persistence option'},
    {'name': 'hash_policy', 'desc': 'module is able to operate in a database with a user defined HASH POLICY'},
    {'name': 'flash', 'desc': 'module is able to operate in a database with Flash memory is enabled or changed over time'},
    {'name': 'crdb', 'desc': 'module is able to operate in a database with crdt for the default redis data types'},    
    {'name': 'clustering', 'desc': 'module is able to operate in a database that is sharded and shards can be migrated'},
    {'name': 'intershard_tls', 'desc': 'module supports two-way encrypted communication between shards'},
    {'name': 'intershard_tls_pass', 'desc': 'module supports `intershard_tls` which requires password'},
    {'name': 'ipv6', 'desc': 'module supports ipv6 communication between shards'}
]
