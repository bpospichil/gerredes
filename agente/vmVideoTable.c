/*
 * Note: this file originally auto-generated by mib2c using
 *        $
 */

#include <net-snmp/net-snmp-config.h>
#include <net-snmp/net-snmp-includes.h>
#include <net-snmp/agent/net-snmp-agent-includes.h>
#include "vmVideoTable.h"

/** Initialize the vmVideoTable table by defining its contents and how it's structured */
void
initialize_table_vmVideoTable(void)
{
    const oid vmVideoTable_oid[] = {1,3,6,1,4,1,12619,1,5};
    netsnmp_table_data_set *table_set;

    /* create the table structure itself */
    table_set = netsnmp_create_table_data_set("vmVideoTable");

    /* comment this out or delete if you don't support creation of new rows */
    table_set->allow_creation = 1;

    /***************************************************
     * Adding indexes
     */
    DEBUGMSGTL(("initialize_table_vmVideoTable",
                "adding indexes to table vmVideoTable\n"));
    netsnmp_table_set_add_indexes(table_set,
                           ASN_INTEGER,  /* index: vmVideoIndex */
                           0);

    DEBUGMSGTL(("initialize_table_vmVideoTable",
                "adding column types to table vmVideoTable\n"));		 
    netsnmp_table_set_multi_add_default_row(table_set,
                                            COLUMN_VMVIDEOINDEX, ASN_INTEGER, 0,
                                            NULL, 0,
                                            COLUMN_VMVIDEOID, ASN_INTEGER, 0,
                                            NULL, 0,
                                            COLUMN_VMVIDEOAUDIENCE, ASN_INTEGER, 0,
                                            NULL, 0,
                                            COLUMN_VMVIDEOADVERTISINGMETRICS, ASN_INTEGER, 1,
                                            NULL, 0,
                                            COLUMN_VMVIDEOKINDVOD, ASN_INTEGER, 0,
                                            NULL, 0,
                                            COLUMN_VMVIDEOKINDLIVE, ASN_INTEGER, 0,
                                            NULL, 0,
                              0);
    
    /* registering the table with the master agent */
    /* note: if you don't need a subhandler to deal with any aspects
       of the request, change vmVideoTable_handler to "NULL" */
    netsnmp_register_table_data_set(netsnmp_create_handler_registration("vmVideoTable", vmVideoTable_handler,
                                                        vmVideoTable_oid,
                                                        OID_LENGTH(vmVideoTable_oid),
                                                        HANDLER_CAN_RWRITE),
                            table_set, NULL);
}

/** Initializes the vmVideoTable module */
void
init_vmVideoTable(void)
{

  /* here we initialize all the tables we're planning on supporting */
    initialize_table_vmVideoTable();
}

/** handles requests for the vmVideoTable table, if anything else needs to be done */
int
vmVideoTable_handler(
    netsnmp_mib_handler               *handler,
    netsnmp_handler_registration      *reginfo,
    netsnmp_agent_request_info        *reqinfo,
    netsnmp_request_info              *requests) {
    /* perform anything here that you need to do.  The requests have
       already been processed by the master table_dataset handler, but
       this gives you chance to act on the request in some other way
       if need be. */
    return SNMP_ERR_NOERROR;
}
