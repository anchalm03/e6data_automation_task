# e6data_Automation Task Assignment Details

This document outlines the tasks automated by the `automation_script.py` script in this repository.

## Objective

The script automates the following steps in a web application:

1. **Login**: Logs into the application with provided credentials.
2. **Navigation Listing**: Lists down the options available in the left navigation.
3. **Record Listing Details**: Lists details for records available under "Catalog" and "Cluster" options, including name, creator, status, and the total count of records.
4. **Cluster Creation**: Creates a new cluster with specified inputs, enabling "Auto Suspension" and setting "Suspension Time" to 10 minutes.
5. **Cluster Deletion**: Deletes the newly created cluster once its status is active.
6. **Query History Records**: Navigates to the "Query History" option to get records for the last 7 days by applying filters.

