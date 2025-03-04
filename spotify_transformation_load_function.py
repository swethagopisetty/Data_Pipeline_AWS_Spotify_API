import json
import boto3
import pandas as pd
from datetime import datetime
from io import StringIO
import pandas as pd

def album(data):
    album_list = [] #to create a data dictionary for making it a DataFrame
    for row in data['items']:
        album_id = row['track']['album']['id']
        album_name = row['track']['album']['name']
        album_release_date = row['track']['album']['release_date']
        album_total_tracks = row['track']['album']['total_tracks']
        album_url = row['track']['album']['external_urls']['spotify']
        album_element = {'album_id':album_id,'name':album_name,'release_date':album_release_date,
                            'total_tracks':album_total_tracks,'url':album_url}
        album_list.append(album_element)
    return album_list

def artist(data):
    artist_list = []  #One album has multiple atists. So we need a nested loop and extract
    for row in data['items']:
        for key, value in row.items():
            if key == "track":
                for artist in value['artists']:
                    artist_dict = {'artist_id':artist['id'], 'artist_name':artist['name'], 'external_url': artist['href']}
                    artist_list.append(artist_dict)
    return artist_list

def songs(data):
    song_list=[]
    for row in data['items']:
        song_id = row['track']['id']
        song_name = row['track']['name']
        song_duration = row['track']['duration_ms']
        song_url = row['track']['external_urls']['spotify']
        song_popularity = row['track']['popularity']
        song_added = row['added_at']
        album_id = row['track']['album']['id']
        artist_id = row['track']['album']['artists'][0]['id']
        song_element = {'song_id':song_id,'song_name':song_name,'duration_ms':song_duration,'url':song_url,
                        'popularity':song_popularity,'song_added':song_added,'album_id':album_id,
                        'artist_id':artist_id
                    }
        song_list.append(song_element)
    return song_list

def lambda_handler(event, context):
    s3=boto3.client('s3')
    Bucket='spotify-etl-project-swethagopisetty'
    Key='raw_data/to_processed/'

    '''for file in s3.list_objects(Bucket=Bucket,Prefix=Key)['Contents']: #FIles name is available as Key under contents
        if file['Key'].endswith('.json'):
            s3.copy_object(Bucket=Bucket, CopySource={'Bucket': Bucket, 'Key': file['Key']}, Key=file['Key'].replace('raw_data/to_processed/', 'processed_data/'))
            s3.delete_object(Bucket=Bucket, Key=file['Key'])'''

    spotify_data = []
    spotify_key = []
    for file in s3.list_objects(Bucket = Bucket,Prefix=Key)['Contents']:
        file_key = file['Key']
        if file_key.split('.')[-1]=='json':
            response = s3.get_object(Bucket = Bucket,Key = file_key)
            content = response['Body']
            jsonObject = json.loads(content.read())
            spotify_data.append(jsonObject)
            spotify_key.append(file_key)

    for data in spotify_data:
        album_list = album(data)
        artist_list = artist(data)
        song_list = songs(data)

        album_df = pd.DataFrame.from_dict(album_list)
        artist_df = pd.DataFrame.from_dict(artist_list)
        song_df = pd.DataFrame.from_dict(song_list)

        album_df = album_df.drop_duplicates(subset=['album_id']) #Drop Duplicate albums
        artist_df = artist_df.drop_duplicates(subset=['artist_id']) #Drop Duplicate artists
        song_df = song_df.drop_duplicates(subset=['song_id']) #Drop Duplicate songs

        album_df['release_date'] = pd.to_datetime(album_df['release_date'])
        song_df['song_added'] = pd.to_datetime(song_df['song_added'])

        song_key = 'transformed_data/songs_data/song_tranformed_' +str(datetime.now())+'.csv' #import datetime for this
        song_buffer = StringIO() #import StringIO to convert data frame into string file and store intoo csv 
        song_df.to_csv(song_buffer,index=False) # index should be set to False for glue Crawler to detect schema
        song_content= song_buffer.getvalue()
        s3.put_object(Bucket=Bucket, Key=song_key, Body=song_content)

        album_key = "transformed_data/album_data/album_transformed_" + str(datetime.now()) + ".csv"
        album_buffer=StringIO()
        album_df.to_csv(album_buffer, index=False)
        album_content = album_buffer.getvalue()
        s3.put_object(Bucket=Bucket, Key=album_key, Body=album_content)
        
        artist_key = "transformed_data/artist_data/artist_transformed_" + str(datetime.now()) + ".csv"
        artist_buffer=StringIO()
        artist_df.to_csv(artist_buffer, index=False)
        artist_content = artist_buffer.getvalue()
        s3.put_object(Bucket=Bucket, Key=artist_key, Body=artist_content)

    s3_resource = boto3.resource('s3')
    for key in spotify_key:
        copy_source = {
            'Bucket': Bucket,
            'Key': key
        }
        print(copy_source)
        s3_resource.meta.client.copy(copy_source, Bucket, 'raw_data/processed/' + key.split("/")[-1])    
        s3_resource.Object(Bucket, key).delete()
        '''album_key = 'transformed_data/album_data/album_tranformed_' +str(datetime.now())+'.csv' not working : error cannot save into non existent files
        album_df.to_csv(album_key, index=False)
        s3.put_object(Bucket=Bucket, Key=album_key, Body=album_df)

        final_data = pd.merge(song_df,album_df, on='album_id', how = 'inner')
        final_data = pd.merge(final_data,artist_df, on='artist_id', how = 'inner')

        final_data.to_csv('s3://spotify-etl-project-swethagopisetty/processed_data/processed_data.csv', index=False, header=False)
        s3.upload_file('s3://spotify-etl-project-swethagopisetty/processed_data/processed_data.csv', Bucket, 'processed_data/processed_data.csv')
        s3.delete_object(Bucket=Bucket, Key=file_key)'''
