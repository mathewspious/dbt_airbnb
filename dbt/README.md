Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
- dbt run
- dbt test


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices

### Source files for the project
- The dlt pipeline in the utils folder is used to insert the data to the data warehouse
 * https://dbtlearn.s3.amazonaws.com/hosts.csv
 * https://dbtlearn.s3.amazonaws.com/reviews.csv
 * https://dbtlearn.s3.amazonaws.com/listings.csv

### Inserting csv content to the warehouse
- The dlt pipeline in the utils folder is used to insert the data to the data warehouse
- The pipeline reads the csv files from the source_files folder and inserts the data to the warehouse

### source file to DB Warehouse 
- hosts.csv --> airbnb_hosts
- reviews.csv --> airbnb_reviews
- listings.csv --> airbnb_listings

### Data Modeling

![Alt text](image.png)

### First Model creation
- The first sets of models are created on top of the source tables created using the csv file
- The models are materialized as view
- Model Mapping
   - airbnb_hosts -> raw_hosts
   - airbnb_reviews -> raw_reviews
   - airbnb_listings -> raw_listings
- The models are created in the models/src folder

### Creating dimension models
- The dimension models are created on top of the raw models
- The dimension models are materialized as view
- Model Mapping
- src_listings --> dim_listings_cleansed
   - Model Name : `dim_listings_cleansed.sql`
   - Few Data cleansing is also done as part of the model creation
      - because of the data irregularity, minimum nights can be 0 or 1. The minimum nights are set to 1 as part of data cleansing
      - In the src table price per night is a string value with a `$` added to the numeric value. As part of cleansing the `$` sign is removed and data is converted to `NUMERIC` value
- src_hosts --> dim_hosts_cleansed  
   - Model Name : `dim_hosts_cleansed.sql`
   - Data cleansing : to make sure all the record's host_name column is not null, we have used the `COALESCE` function to set the value as `Anonymous` if the `NULL`

### Materialization
- by default the models are materialized as views 
- the materialization can be changed to table or view by changing the `materialized` property in project.yml file
- View materializarion are used for models which are reffered once lke our src models
- Table materialization are used for models which are reffered multiple times like our dimension models
- Incremental Materialization
  This is used when data needs to be added incrementally to a db table. The materialization can be set at `profile.yml` or in the model file. We will use the model file here. Below code snippet creates our facts table with incremental matrialization. `is_incremental()` method can be used to fetch only the required data from source table
  ```sql

    {{
        config(
            materialized='incremental',
            on_schema_change='fail'
        )
    }}
    WITH src_reviews AS (
        SELECT * FROM {{ ref('src_reviews') }}
    )
    SELECT * FROM src_reviews
    WHERE review_text is not null
    {% if is_incremental() %}
    and review_date >= coalesce((select max(review_date) from {{ this }}), '1900-01-01')
    {% endif %}

  ```

  The normal `dbt run` command will materialize the fct table incremetally. For complete rebuild can be done using the command `dbt run --full-refresh`

### Ephemeral Matrialization
- Ephemeral materialization in dbt referes to a materialization strategy where a dbt model doesnot create a physical object (like view or tables) in the database. Instead, the SQL code defined within an ephmeral model is directly inlined as common table expression (CTE) into any downstream model that reference it.
- Ephemeral materialization is useful when you want to avoid creating a physical object in the databas
- Restrategizing our models
    - The src tables in our project are not really needed to be matrialized as views, these models can be converted to ephemeral. Only the dimensional models are referring to it.
