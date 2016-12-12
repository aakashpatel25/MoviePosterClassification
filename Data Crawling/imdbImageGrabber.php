<?php
//set time limit to 0 to make it work without timing out
set_time_limit(0);

//providing directory name to store the fetched images
define('DIRECTORY', 'imdbImagesNew/');
ini_set('auto_detect_line_endings',TRUE);
//the csv file which has the movie id which will be needed to crawl the data
$handle = fopen('mymovie.csv','r');
$i = 0;

while ( ($data = fgetcsv($handle) ) !== FALSE ) {
	//creating file name
	$filename = DIRECTORY . $data[0].'.jpg';
	if (!file_exists($filename)) {
	
	
	$i++;
	//fetching the data from IMDB by movie ID
	$homepage = file_get_contents('https://api.themoviedb.org/3/find/'
		.$data[0].'?api_key=eb4b00d1dc3f8849fa4c320e01734cf3'
		.'&external_source=imdb_id');

	//creating php array from the json data
	$arr = json_decode($homepage, true);
	if(sizeof($arr['movie_results']) != 0){
		// gettting the poster path from the array
		$poster_path = $arr['movie_results'][0]['poster_path'];

		$path_forward = 'https://image.tmdb.org/t/p/w500';

		//creating full path to download the image
		$full_path = $path_forward . $poster_path;


/** IMAGE DOWNLOAD **/
$content = file_get_contents($full_path);
file_put_contents($filename, $content);
echo "file added".$filename;
}else{
echo "not available ".$data[0];
}
	}
/** IMAGE DOWNLOAD **/

}
ini_set('auto_detect_line_endings',FALSE);

?>