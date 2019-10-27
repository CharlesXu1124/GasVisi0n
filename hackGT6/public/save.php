<?php 
if ( isset($_POST["image"]) && !empty($_POST["image"]) ) { 
	$data = $_POST["image"];
	$uri =  substr($data,strpos($data,","));
	
	$folder = "images";
	//create a filename for the new image
	$file = md5(uniqid()) . ".jpg";
	//decode the image data and save it to file
	file_put_contents($folder . "/" . $file, base64_decode($uri));
      //$content = //file_get_contents('http://localhost/image.php');
//file_put_contents('flower.jpg', $content);
     $firebase->set([
        'picture' => $uri,
     ], 'https://xuzheyuan1014.firebaseio.com/xuzheyuan1014');

     $firebase->set('my/data/key_1', 'value_1');
	echo $file;
}
?>
