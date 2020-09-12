<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
$requestPayload = file_get_contents("php://input");
$object = json_decode($requestPayload);

var_dump($object);
?> 
