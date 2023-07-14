# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# + tags=[]
#gets values from all the metadata jsons for HGL records and writes them to a spreadsheet
import os, json
import pandas as pd

path_to_json = '/Users/viviannguyen/Documents/GitHub/harvard-geodata/json'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
jsons_df = pd.DataFrame(columns=['GBL_version', 'identifier', 'title', 'description', 'rights', 'provenance', 'references', 'ID', 'slug', 'geom_type', 'modified', 'creator', 'publisher', 'format', 'type', 'subject', 'spatial', 'issued', 'temporal', 'geom', 'year', 'harvard_collection_ID'])

for index, js in enumerate(json_files):
    with open(os.path.join(path_to_json, js)) as json_file:
        json_text = json.load(json_file)

        # Indicates which version of the GeoBlacklight schema is in use
        GBL_version = json_text['geoblacklight_version']
        # Unique identifier for layer as a URI. It should be globally unique across all institutions, assumed not to be end-user visible
        identifier = json_text['dc_identifier_s']
        # The name of the resource
        title = json_text['dc_title_s']
        description = json_text['dc_description_s']
        # Signals access in the geoportal and is indicated by a padlock icon. Users need to sign in to download restricted items
        # Controlled vocabulary: "Public" or "Restricted"
        rights = json_text['dc_rights_s']
        # The name of the institution that holds the resource or acts as the custodian for the metadata record
        provenance = json_text['dct_provenance_s']
        # This element is a hash of key/value pairs for different types of external links. It integrates external services and references using the CatInterOp approach
        references = json_text['dct_references_s']
        ID = json_text['layer_id_s']
        # This is a string appended to the base URL of a GeoBlacklight installation to create a unique landing page for each resource. It is visible to the user and serves the purpose of forming a persistent URL for each catalog item.
        slug = json_text['layer_slug_s']
        # This element shows up as Data type in GeoBlacklight, and each value has an associated icon
        # Controlled vocabulary: https://opengeometadata.org/1.0-geometry-type/
        geom_type = json_text['layer_geom_type_s']
        # Last modification date for the metadata record
        modified = json_text['layer_modified_dt']
        # The person(s) or organization that created the resource
        creator = json_text['dc_creator_sm']
        try:
            # The organization that made the original resource available
            publisher = json_text['dc_publisher_s']
        except KeyError:
            published = "null"
        # This indicates the file format of the data. If a download link is included, this value displays on the item page in the button under the download widget
        # Controlled vocabulary: https://opengeometadata.org/gbl-1.0/format-values
        format = json_text['dc_format_s']
        # This is a general element to indicate the larger genre of the resource
        # Controlled vocabulary: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-7
        type = json_text['dc_type_s']
        # These are theme or topic keywords
        # Recommended thesauri are ISO Topic Categories and Library of Congress Subject Headings
        subject = json_text['dc_subject_sm']
        try:
            # This field is for place name keywords
            # Controlled vocabulary: https://www.geonames.org/
            spatial = json_text['dct_spatial_sm']
        except KeyError:
            spatial = "null"
        try:
            # This is the publication date for the resource
            issued = json_text['dct_issued_s']
        except KeyError:
            issued = "null"
        try:
            # This represents the "Ground Condition" of the resource, meaning the time period data was collected or is intended to represent. Displays on the item page in the Year value
            temporal = json_text['dct_temporal_sm']
        except KeyError:
            temporal = "null"
        # The rectangular extents of the resource. Note that this field is indexed as a Solr spatial (RPT) field
        geom = json_text['solr_geom']
        try:
            # A four digit integer representing a year of temporal coverage or date issued for the resource. This field is used to populate the Year facet and the optional Blacklight Range Limit gem
            year = json_text['solr_year_i']
        except KeyError:
            year = "null"
        # Collection ID in Harvard Library
        harvard_collection_ID = json_text['harvard_collectionID_sm'] 
        
        # Join all the columns into pandas dataframe
        jsons_df.loc[index] = [GBL_version, identifier, title, description, rights, provenance, references, ID, slug, geom_type, modified, creator, publisher, format, type, subject, spatial, issued, temporal, geom, year, harvard_collection_ID]

# Save to .csv
jsons_df.to_csv('/Users/viviannguyen/Documents/GitHub/vn-may-crane-23-docs/all-metadata.csv', index = False)