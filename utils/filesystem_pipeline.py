import dlt
from dlt.sources.filesystem import filesystem, read_csv
from dlt.common import json # Only needed if you plan to read JSON, here just for context

@dlt.source()
def airbnb_listing_source(): # Renamed source to avoid confusion with resource
    """
    Source function to read Airbnb listing data from CSV files.
    """
    # The key is to define the resource name at the point where `read_csv` is called
    # and then directly return that configured resource.
    airbnb_listing_resource = filesystem(
        bucket_url="file:///Users/mathewspious/MyWorks/projects_publish/dbt_airbnb/source_files/",
        file_glob="listings.csv"
    ) | read_csv()

    airbnb_listing_resource.table_name="airbnb_listing"

    # Return the resource. dlt will then run this resource and load its data.
    return dlt.resource(airbnb_listing_resource) # <--- Return the resource, don't yield it from source

@dlt.source()
def airbnb_hosts_source(): # Renamed source to avoid confusion with resource
    """
    Source function to read Airbnb listing data from CSV files.
    """
    # The key is to define the resource name at the point where `read_csv` is called
    # and then directly return that configured resource.
    airbnb_hosts_resource = filesystem(
        bucket_url="file:///Users/mathewspious/MyWorks/projects_publish/dbt_airbnb/source_files/",
        file_glob="hosts.csv"
    ) | read_csv()

    airbnb_hosts_resource.table_name="airbnb_hosts"

    # Return the resource. dlt will then run this resource and load its data.
    return dlt.resource(airbnb_hosts_resource) # <--- Return the resource, don't yield it from source

@dlt.source()
def airbnb_reviews_source(): # Renamed source to avoid confusion with resource
    """
    Source function to read Airbnb listing data from CSV files.
    """
    # The key is to define the resource name at the point where `read_csv` is called
    # and then directly return that configured resource.
    airbnb_reviews_resource = filesystem(
        bucket_url="file:///Users/mathewspious/MyWorks/projects_publish/dbt_airbnb/source_files/",
        file_glob="reviews.csv"
    ) | read_csv()

    airbnb_reviews_resource.table_name="airbnb_reviews"

    # Return the resource. dlt will then run this resource and load its data.
    return dlt.resource(airbnb_reviews_resource) # <--- Return the resource, don't yield it from source

# Create the pipeline instance
pipeline = dlt.pipeline(
    pipeline_name="my_pipeline",
    destination="postgres",
    dataset_name="raw",
)

# Run the pipeline by passing the source function call
# The source function will return the configured resource
info = pipeline.run(airbnb_listing_source())
print(info)
info = pipeline.run(airbnb_hosts_source())
print(info)
info = pipeline.run(airbnb_reviews_source())
print(info)